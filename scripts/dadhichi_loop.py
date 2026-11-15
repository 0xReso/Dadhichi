#!/usr/bin/env python3
"""Run Dadhichi work rounds back to back, waiting out Claude usage limits.

Each round is a fresh headless Claude Code session given loop/LOOP.md.
When a round hits the usage limit, the runner reads the reset time from the
message, sleeps until then (plus a small margin) and carries on.

Control files (create them with `touch`, delete to undo):
  loop/PAUSE  - finish the current round, then wait until the file is removed
  loop/STOP   - finish the current round, then exit

Usage:
  scripts/dadhichi-loop.sh              run forever (until IDLE, BLOCKED or STOP)
  scripts/dadhichi-loop.sh --once       run one round and exit
  scripts/dadhichi-loop.sh --selftest   check the limit-message parser, run nothing
"""

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOP = os.path.join(ROOT, "loop")
LOGS = os.path.join(LOOP, "logs")
RUNLOG = os.path.join(LOOP, "runner.log")

ROUND_TIMEOUT = 2 * 60 * 60      # a round that runs longer than 2 hours is killed
RESET_MARGIN = 3 * 60            # wait 3 minutes past the stated reset time
FALLBACK_WAIT = 30 * 60          # limit hit but no reset time found
ERROR_WAIT = 5 * 60              # other failures
MAX_ERRORS_IN_A_ROW = 5

ALLOWED_TOOLS = ",".join([
    "Read", "Write", "Edit", "Glob", "Grep", "Agent", "WebSearch", "WebFetch",
    "Bash(git add:*)", "Bash(git commit:*)", "Bash(git status:*)",
    "Bash(git diff:*)", "Bash(git log:*)", "Bash(ls:*)", "Bash(wc:*)",
    "Bash(mkdir:*)", "Bash(cp:*)",
])

LIMIT_WORDS = re.compile(
    r"usage limit|limit reached|hit your limit|rate limit|limit will reset|resets? at|resets \d",
    re.I)


def log(msg):
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with open(RUNLOG, "a") as f:
        f.write(line + "\n")


def find_claude():
    """The CLI ships inside the desktop app under a versioned folder; take the newest."""
    if os.environ.get("CLAUDE_BIN"):
        return os.environ["CLAUDE_BIN"]
    base = os.path.expanduser("~/Library/Application Support/Claude/claude-code")
    hits = glob.glob(os.path.join(base, "*", "*", "claude.app", "Contents", "MacOS", "claude"))

    def version_key(path):
        v = path[len(base) + 1:].split(os.sep)[0]
        return [int(x) if x.isdigit() else 0 for x in v.split(".")]

    hits.sort(key=version_key)
    for path in reversed(hits):
        if os.access(path, os.X_OK):
            return path
    for name in ("claude",):
        for d in os.environ.get("PATH", "").split(os.pathsep):
            p = os.path.join(d, name)
            if os.access(p, os.X_OK):
                return p
    sys.exit("Could not find the Claude CLI. Set CLAUDE_BIN=/path/to/claude.")


def reset_time(text, now=None):
    """Return the datetime the limit resets, or None if the text gives none."""
    now = now or dt.datetime.now()
    # Form 1: "...limit reached|1763290800" (unix seconds)
    m = re.search(r"\|\s*(\d{10})\b", text) or re.search(r"reset[^0-9]{0,20}(\d{10})\b", text, re.I)
    if m:
        return dt.datetime.fromtimestamp(int(m.group(1)))
    # Form 2: "resets 3pm", "resets at 3:30 PM", "reset at 15:00"
    m = re.search(r"resets?\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*([ap]\.?m\.?)?", text, re.I)
    if m:
        hour, minute = int(m.group(1)), int(m.group(2) or 0)
        ampm = (m.group(3) or "").lower().replace(".", "")
        if ampm == "pm" and hour != 12:
            hour += 12
        if ampm == "am" and hour == 12:
            hour = 0
        if hour > 23 or minute > 59:
            return None
        t = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if t <= now:
            t += dt.timedelta(days=1)
        return t
    # Form 3: "resets in 2h 15m" / "in 45 minutes"
    m = re.search(r"(?:resets?|again)\s+in\s+(?:(\d+)\s*h(?:ours?)?)?\s*(?:(\d+)\s*m(?:in(?:utes?)?)?)?", text, re.I)
    if m and (m.group(1) or m.group(2)):
        return now + dt.timedelta(hours=int(m.group(1) or 0), minutes=int(m.group(2) or 0))
    return None


def sleep_until(when, why):
    secs = max(0, (when - dt.datetime.now()).total_seconds())
    log(f"{why}; sleeping until {when:%a %H:%M} ({secs / 60:.0f} min)")
    while True:
        left = (when - dt.datetime.now()).total_seconds()
        if left <= 0 or os.path.exists(os.path.join(LOOP, "STOP")):
            return
        time.sleep(min(left, 60))


def run_round(claude, model):
    stamp = f"{dt.datetime.now():%Y%m%d-%H%M%S}"
    out_path = os.path.join(LOGS, f"round-{stamp}.json")
    with open(os.path.join(LOOP, "LOOP.md")) as f:
        prompt = f.read()
    cmd = [claude, "-p", prompt, "--output-format", "json",
           "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED_TOOLS]
    if model:
        cmd += ["--model", model]
    log(f"round {stamp} started")
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=ROUND_TIMEOUT)
        stdout, stderr, code = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout or ""
        stderr = (e.stderr or "") + "\n[runner] round timed out"
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
        code = -1
    with open(out_path, "w") as f:
        f.write(stdout)
        if stderr.strip():
            f.write("\n\n--- stderr ---\n" + stderr)

    result_text, is_error = stdout, code != 0
    try:
        data = json.loads(stdout)
        result_text = str(data.get("result", "")) or stdout
        is_error = is_error or bool(data.get("is_error"))
        cost = data.get("total_cost_usd")
        turns = data.get("num_turns")
        log(f"round {stamp} ended: exit {code}, {turns} turns" + (f", ${cost:.2f} equiv" if cost else ""))
    except (ValueError, AttributeError):
        log(f"round {stamp} ended: exit {code} (output not JSON)")
    return result_text + "\n" + stderr, is_error


def push_if_remote():
    r = subprocess.run(["git", "remote"], cwd=ROOT, capture_output=True, text=True)
    if "origin" not in r.stdout.split():
        return
    p = subprocess.run(["git", "push", "-q", "origin", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    log("pushed to origin" if p.returncode == 0 else f"push failed: {p.stderr.strip()[:200]}")


def selftest():
    now = dt.datetime(2026, 11, 16, 13, 0)
    cases = {
        "Claude AI usage limit reached|1763290800": dt.datetime.fromtimestamp(1763290800),
        "5-hour limit reached ∙ resets 3pm": dt.datetime(2026, 11, 16, 15, 0),
        "You've hit your limit · resets 11:30 AM (Asia/Calcutta)": dt.datetime(2026, 11, 17, 11, 30),
        "Usage limit reached. Your limit will reset at 18:00.": dt.datetime(2026, 11, 16, 18, 0),
        "limit reached, resets in 2h 15m": dt.datetime(2026, 11, 16, 15, 15),
        "limit reached": None,
    }
    ok = True
    for text, want in cases.items():
        got = reset_time(text, now)
        good = got == want and bool(LIMIT_WORDS.search(text))
        ok &= good
        print(("ok  " if good else "FAIL"), repr(text), "->", got)
    print("status line:", status_of("blah\nDADHICHI-STATUS: BLOCKED needs a GitHub login"))
    sys.exit(0 if ok else 1)


def status_of(text):
    m = re.findall(r"DADHICHI-STATUS:\s*(CONTINUE|IDLE|BLOCKED)(.*)", text)
    return (m[-1][0], m[-1][1].strip()) if m else (None, "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--model", default=os.environ.get("DADHICHI_MODEL"))
    args = ap.parse_args()
    if args.selftest:
        selftest()

    os.makedirs(LOGS, exist_ok=True)
    claude = find_claude()
    log(f"runner started (pid {os.getpid()}), CLI: {claude}")
    errors = 0
    while True:
        if os.path.exists(os.path.join(LOOP, "STOP")):
            log("STOP file found; exiting")
            return
        while os.path.exists(os.path.join(LOOP, "PAUSE")):
            time.sleep(60)

        text, is_error = run_round(claude, args.model)
        status, reason = status_of(text)

        if "not logged in" in text.lower() or "/login" in text:
            log("the Claude CLI is not logged in: run the CLI once in a terminal and use /login; exiting")
            return

        if is_error and LIMIT_WORDS.search(text) and status is None:
            when = reset_time(text) or dt.datetime.now() + dt.timedelta(seconds=FALLBACK_WAIT)
            push_if_remote()
            sleep_until(when + dt.timedelta(seconds=RESET_MARGIN), "usage limit reached")
            errors = 0
            continue

        push_if_remote()
        if status == "IDLE":
            log("backlog empty; exiting")
            return
        if status == "BLOCKED":
            log(f"blocked: {reason}; exiting")
            return
        if status is None:
            errors += 1
            log(f"round ended without a status line ({errors} in a row); see loop/logs")
            if errors >= MAX_ERRORS_IN_A_ROW:
                log("too many failed rounds in a row; exiting")
                return
            sleep_until(dt.datetime.now() + dt.timedelta(seconds=ERROR_WAIT), "waiting before retry")
        else:
            errors = 0
        if args.once:
            return


if __name__ == "__main__":
    main()

Topic: The Dadhichi round protocol | Depth: low (30 questions)
Assumptions: Answers follow the provided Dadhichi round protocol verbatim. Unless a question specifies a cloud session, assume a local Mac session driven by the runner script. Backlog markers are `[ ]` (open), `[~]` (skipped), and `[x]` (complete).

## Band 1: Core Mechanisms

**Q1 ·** A fresh round starts and reads these two files:

```markdown
# loop/STATE.md
Next step: Run test set B for pattern-a.

# loop/BACKLOG.md
- [x] Item 1: Build pattern-a
- [~] Item 2: Refactor pattern-b
- [ ] Item 3: Write pattern-c
- [ ] Item 4: Audit pattern-d
```

Which step or item must the agent work on in this round?

---

**Q2 ·** An agent is about to run 3 test cases for `pattern-a` inside `runs/r1/`. It has the prompt file, 3 filled-in input files, and a short note explaining which edge case each test is meant to catch. What must the agent do with `runs/r1/prompt.md` and how must it run the tests?

(a) Save an exact copy of the prompt as `runs/r1/prompt.md` beforehand; pass fresh general-purpose subagents only the prompt with its inputs filled in.
(b) Save `runs/r1/prompt.md` beforehand; pass fresh general-purpose subagents the filled-in prompt plus the edge-case note.
(c) Pass fresh general-purpose subagents only the filled-in prompt; save `runs/r1/prompt.md` after all 3 outputs finish.
(d) Save `runs/r1/prompt.md` beforehand; generate the 3 test outputs directly in the builder session using only the filled-in prompt.

---

**Q3 ·** A round agent finishes collecting outputs in `runs/r2/` for `pattern-a`. Only 2 outputs exist, and both visibly omit a required section. How must `runs/r2/` be graded?

(a) The round agent grades both outputs itself since the failure is obvious, then moves straight to fixing the prompt.
(b) The round agent gives `dadhichi-head` the relevant file paths and a target review output path, and lets `dadhichi-head` write the grade.
(c) The round agent writes a summary of both omissions and asks `dadhichi-head` to confirm its verdict.
(d) The round agent spawns a fresh general-purpose subagent on the same model to grade the 2 outputs.

---

**Q4 ·** `dadhichi-head` compares new `v1.1` against released `v1.0` of `pattern-a`:

```text
v1.0: C1 PASS, C2 PASS, C3 FAIL, C4 FAIL, C5 FAIL  (2/5)
v1.1: C1 PASS, C2 FAIL, C3 PASS, C4 PASS, C5 PASS  (4/5)
```

May the agent promote `v1.1` to replace `v1.0`? Answer `Yes` or `No`, and name the specific check that decides it.

---

**Q5 ·** At the end of a local Mac round (driven by the runner script), an agent plans to run these three commands:

```bash
1. git add -A
2. git commit -m "Write pattern-a tests"
3. git push
```

Which numbered command must the agent NOT run?

---

**Q6 ·** A round completes Item 1 with no blockers and leaves `loop/BACKLOG.md` in this state (with no unfinished step in `loop/STATE.md`):

```markdown
- [x] Item 1: Write pattern-a
- [~] Item 2: Hold pattern-b for redesign
- [ ] Item 3: Run tests for pattern-a
```

Write the exact final line the agent must output.

---

## Band 2: Applied Scenarios

**Q7 ·** Midway through an unattended round on `pattern-b`, the agent sees two reasonable ways to format an optional table inside a test case. Neither choice conflicts with the System Design document. What should the agent do?

(a) Stop the round, emit `DADHICHI-STATUS: BLOCKED`, and wait for a human to choose the format.
(b) Pick the sensible format, write down why in files (including the decision in `loop/STATE.md` for user review), and keep going.
(c) Pick the sensible format and keep going, explaining the choice only in the final chat reply so the user sees it.
(d) Build both variants in parallel and leave the round's files uncommitted until a human chooses one.

---

**Q8 ·** A fresh round starts on an item that modifies `patterns/p1/prompt.md`. Before editing anything, the agent must read these five files:

- A. `CHANGELOG.md`
- B. `Dadhichi Master Prompt Library System Design.md`
- C. `loop/BACKLOG.md`
- D. `patterns/p1/prompt.md`
- E. `loop/STATE.md`

In what exact order must the agent read them? List the letters in order, grouping in parentheses any files that share the same numbered step.

---

**Q9 ·** Before a round starts, `loop/BACKLOG.md` contains:

```markdown
- [ ] Build pattern-c
```

In a 45-minute round, the agent splits this item into three sub-items under it—(1) write prompt and tests, (2) run tests, (3) grade run—and completes only sub-item 1. What markers should appear on the parent item and the three sub-items when the round finishes?

(a) Parent `[x]`; sub-items `[x]`, `[ ]`, `[ ]`
(b) Parent `[ ]`; sub-items `[x]`, `[ ]`, `[ ]`
(c) Parent `[~]`; sub-items `[x]`, `[ ]`, `[ ]`
(d) Parent `[ ]`; sub-items `[ ]`, `[ ]`, `[ ]`

---

**Q10 ·** `patterns/pattern-b/failures.md` currently contains 2 lines, each recording an earlier failure. `dadhichi-head` grades `runs/r1/` for `pattern-b`:

```text
- Case 1: PASS
- Case 2: FAIL (missing section header)
- Case 3: FAIL (wrong output order)
- Case 4: FAIL (invented default value)
```

After logging this run, how many total lines should `patterns/pattern-b/failures.md` contain?

---

**Q11 ·** `pattern-a` version `v1.0` is already released. During a later round, the agent spots a one-word typo in `v1.0` that causes a minor formatting slip. How must the agent apply the fix?

(a) Edit `v1.0` directly in place, since a one-word typo is not a behavioral change.
(b) Create a new version (such as `v1.1`) with the fix, leave `v1.0` untouched, and promote only after `dadhichi-head` confirms it passes more checks with no regressions.
(c) Edit `v1.0` in place, then ask `dadhichi-head` to re-grade `v1.0` to confirm nothing broke.
(d) Create `v1.1` with the fix and promote it immediately, because a one-word fix cannot regress passing checks.

---

**Q12 ·** A round runs in a cloud session (no runner script). After updating `CHANGELOG.md`, `loop/BACKLOG.md`, and `loop/STATE.md`, the agent runs:

```bash
git add -A
git commit -m "Grade pattern-b v1.0 run"
```

and ends its turn. What required step is missing, and how does the answer change if the same round runs on a local Mac with the runner script?

---

**Q13 ·** A fresh round starts and reads these two files:

```markdown
# loop/STATE.md
Finished: Graded pattern-a v1.0.
Next step: None (item complete).

# loop/BACKLOG.md
- [x] Item 1: Grade pattern-a v1.0
- [~] Item 2: Rewrite pattern-b (waiting on design note)
- [~] Item 3: Expand pattern-c
- [ ] Item 4: Write tests for pattern-d
- [ ] Item 5: Grade pattern-e
```

Which item does this round select?

---

**Q14 ·** An agent drafts four test inputs for a summarization pattern:

```text
Input 1: A fictional memo from "Acme Corp" about a delayed release.
Input 2: A paragraph with a realistic-sounding quote attributed to a real CEO, invented by the agent.
Input 3: A support ticket copied from a real customer's email, including their phone number and address.
Input 4: A short public-domain recipe using plain ingredient amounts.
```

Which input numbers violate the protocol, and which rule does each break?

---

**Q15 ·** To test `pattern-c v1.0`, a round agent executes four steps:

```text
1. Copies patterns/pattern-c/v1.0.md to runs/r1/prompt.md.
2. Fills the prompt with Test Input 1.
3. Spawns a fresh general-purpose subagent and sends the filled prompt plus:
   "Watch out—earlier runs forgot to include the rule line at the end."
4. Saves the subagent's reply to runs/r1/out-1.md.
```

Which numbered step invalidates the test evidence, and why?

---

**Q16 ·** A round finishes Item 3 cleanly, leaves no unfinished step in `loop/STATE.md`, and leaves `loop/BACKLOG.md` as:

```markdown
- [x] Item 1: Build pattern-a
- [~] Item 2: Parked pattern-b
- [x] Item 3: Grade pattern-c
```

Write the exact final line the agent must output.

---

**Q17 ·** At the end of Round 4, the agent appends its handoff summary to the bottom of `loop/STATE.md`, leaving Round 3's `Next step: Run test set A` intact at the top of the file. What rule did Round 4 break, and what bug does that cause in Round 5?

(a) `loop/STATE.md` must be overwritten, not appended; Round 5 can read Round 3's stale unfinished step and re-run test set A.
(b) `loop/STATE.md` is only written when a round fails; appending after a clean round corrupts `CHANGELOG.md`.
(c) `loop/STATE.md` must be deleted when an item finishes; leaving it prevents Round 5 from reading `loop/BACKLOG.md`.
(d) Appending is required to preserve history; the only error is omitting a blank separator line between rounds.

---

**Q18 ·** `dadhichi-head` compares new `v1.1` against released `v1.0` of `pattern-b`:

```text
v1.0: C1 PASS, C2 PASS, C3 PASS, C4 FAIL  (3/4)
v1.1: C1 PASS, C2 PASS, C3 PASS, C4 FAIL  (3/4)
```

`v1.1` is 20% shorter and easier to read than `v1.0`, and it fails no check that `v1.0` passed. May the agent promote `v1.1`? Answer `Yes` or `No`, and state why.

---

**Q19 ·** During an unattended round, an agent runs four actions:

```text
1. Creates tests/pattern-d/runs/v0.1/prompt.md inside the project folder.
2. Runs `brew install jq` to parse JSON outputs faster.
3. Edits `~/.gitconfig` to set a custom commit message template.
4. Runs `git add -A` and `git commit -m "Add pattern-d run"`.
```

Which numbered actions violate the protocol's environment boundaries?

---

**Q20 ·** A round agent finishes drafting `patterns/p2/v0.1.md` and needs a gate review from `dadhichi-head`, saved at `patterns/p2/gate-review.md`. What must the agent give `dadhichi-head`?

(a) The relevant file paths to review and the output path `patterns/p2/gate-review.md` where `dadhichi-head` writes its review.
(b) A written summary of the prompt's strengths and risks, asking `dadhichi-head` to reply in chat so the builder can copy it into `gate-review.md`.
(c) Only the prompt path; `dadhichi-head` chooses where to save the review and the builder fills in the final pass/fail verdict.
(d) The file paths plus the builder's pre-filled grade sheet so `dadhichi-head` only verifies borderline items.

---

**Q21 ·** In today's round (`2026-05-12`), the agent writes no prompt edits. It only sends `runs/r3/` of `pattern-a` to `dadhichi-head` for grading and decides to wait for an extra test case before editing `pattern-a`. Must the agent add a line to `CHANGELOG.md` before finishing? Answer `Yes` or `No`, and explain why.

---

## Band 3: Combined Rules and Edge Cases

**Q22 ·** At the start of a round, these files read:

```markdown
# loop/STATE.md
Item: Item 2 — Build and grade pattern-b
Next step: Run the 5 test cases for pattern-b v0.1.

# loop/BACKLOG.md
- [x] Item 1: Build pattern-a
- [ ] Item 2: Build and grade pattern-b
```

In 50 minutes, the agent runs all 5 test cases and saves the outputs, leaving grading for the next round. No blockers occur. At the end of this round: (1) what is Item 2's marker in `loop/BACKLOG.md`, and (2) what is the exact final line of the agent's output?

---

**Q23 ·** During a test run in `runs/v1.0-check/`, an agent performs these steps:

```text
1. Copies released patterns/p1/v1.0.md to runs/v1.0-check/prompt.md.
2. Fresh subagent runs Test 1 and fails due to a missing constraint.
3. Agent edits both patterns/p1/v1.0.md and runs/v1.0-check/prompt.md to add the constraint.
4. Fresh subagents run Tests 2 and 3 against the edited file.
```

Name the two distinct protocol rules violated in Step 3.

---

**Q24 ·** `dadhichi-head` grades `pattern-c v2.1` against released `v2.0`:

```text
v2.0: C1 PASS, C2 FAIL, C3 PASS, C4 FAIL  (2/4)
v2.1: C1 PASS, C2 PASS, C3 FAIL, C4 PASS  (3/4)
```

The round agent believes `dadhichi-head` misread the output on C3 and proposes three actions: (1) overriding `dadhichi-head` to mark C3 as PASS itself, (2) promoting `v2.1`, and (3) skipping `patterns/pattern-c/failures.md` for C3. Answer `Yes` or `No` for whether each proposed action is allowed.

---

**Q25 ·** Compare two unattended rounds:

- **Situation X:** While drafting a test input, the agent isn't sure whether to use 3 rows or 5 rows in a sample table; the System Design document allows either.
- **Situation Y:** `dadhichi-head` is unreachable due to an expired API credential that only a human can renew, and the only remaining `[ ]` item is grading a completed test run.

Which status lines must end Situation X and Situation Y?

(a) X: `DADHICHI-STATUS: CONTINUE`; Y: `DADHICHI-STATUS: BLOCKED <one-sentence reason>`
(b) X: `DADHICHI-STATUS: BLOCKED <one-sentence reason>`; Y: `DADHICHI-STATUS: BLOCKED <one-sentence reason>`
(c) X: `DADHICHI-STATUS: CONTINUE`; Y: `DADHICHI-STATUS: IDLE`
(d) X: `DADHICHI-STATUS: CONTINUE`; Y: `DADHICHI-STATUS: CONTINUE` (after the builder grades the run itself)

---

**Q26 ·** In a cloud session (no runner script), an agent spends 45 minutes writing `pattern-c` and its tests—half of a `[ ]` backlog item—and decides to stop cleanly before running tests so it does not hit the usage limit mid-run. Five closing steps remain:

- A. Run `git push` to the session's branch
- B. Overwrite `loop/STATE.md` with date/time, item, finished work, exact next step, and decisions
- C. Add a line to `CHANGELOG.md` under today's date
- D. Run `git add -A` then `git commit -m "Write pattern-c and tests"`
- E. Output `DADHICHI-STATUS: CONTINUE` as the final line

Put steps A–E in the exact protocol order.

---

**Q27 ·** Two consecutive rounds work on `Item 1: Test and grade pattern-a v0.2` (the only `[ ]` item in `loop/BACKLOG.md`):

- **Round 1** freezes `runs/r1/prompt.md`, runs fresh general-purpose subagents with only filled inputs to write `out-1.md` through `out-3.md`, updates `CHANGELOG.md`, overwrites `loop/STATE.md` with `Next step: Have dadhichi-head grade runs/r1/ into runs/r1/review.md`, commits, and ends with `DADHICHI-STATUS: CONTINUE`.
- **Round 2** starts fresh with no memory of Round 1, completes the grading with all checks passing, and ticks Item 1 `[x]`.

State: (1) which file tells Round 2 to grade `runs/r1/` instead of re-running tests, (2) which agent writes `runs/r1/review.md`, and (3) Round 2's exact final line.

---

**Q28 ·** Before running tests for `pattern-e v0.1`, a round agent prepares `runs/r1/` like this:

```text
- Writes input-1.md using a real coworker's pasted performance review (name and salary included).
- Writes input-2.md citing a made-up "2025 industry survey showing 78% of teams fail."
- Passes the live path patterns/pattern-e/v0.1.md directly to fresh subagents without copying it into runs/r1/.
```

List all three protocol violations in this setup.

---

**Q29 ·** Released `pattern-d v1.0` passed Checks 1, 2, and 3 and failed Check 4. Compare two possible `dadhichi-head` grades for new `pattern-d v1.1`:

```text
Case A: v1.1 passes C1, C2, C3, C4  (4/4)
Case B: v1.1 passes C1, C2, C4; fails C3  (3/4)
```

For both Case A and Case B, answer `Yes` or `No` to: (1) is `v1.1` promoted, (2) is a line added to `patterns/pattern-d/failures.md`, and (3) is a line added to `CHANGELOG.md`?

---

**Q30 ·** Round 8 runs in a cloud session (no runner script). At the start of the round, `loop/STATE.md` names no unfinished step, and `loop/BACKLOG.md` reads:

```markdown
- [x] Item 1: Build pattern-a
- [~] Item 2: Redesign pattern-b
- [ ] Item 3: Log 2 failures from runs/r2/review.md for pattern-a
```

Round 8 completes Item 3 cleanly with no blockers. State all four closing outcomes: (1) how many new lines are added to `patterns/pattern-a/failures.md`, (2) Item 3's marker in `loop/BACKLOG.md`, (3) whether Round 8 runs `git push`, and (4) the exact final line of Round 8's output.

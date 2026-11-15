You are running one unattended round of work on Dadhichi, a library of tested, reusable prompts. Nobody is watching this round, so you cannot ask questions; make the sensible choice, write down why, and keep going. Another round will start after you finish, with no memory of this one, so everything the next round needs must be written to files.

Read first, in this order:
1. `loop/STATE.md`: what the last round did and what it left half-done.
2. `loop/BACKLOG.md`: the work list.
3. `Dadhichi Master Prompt Library System Design.md`: the library's rules, before you build or change any prompt.
4. `CHANGELOG.md` and the files the current item touches.

Pick the work:
- If STATE.md names an unfinished step, finish that.
- Otherwise take the first item in BACKLOG.md marked `[ ]`. Skip `[~]` and `[x]`.

Do one solid step of it, about 30 to 60 minutes of work: for example write a pattern and its tests, or run a gate review, or run one test set, or grade one run. A step that ends with files saved and the state written is worth more than a bigger step cut off by the usage limit.

The rules that make the library trustworthy, because a prompt is only worth keeping if the evidence for it is real:
- Test outputs are written by fresh general-purpose subagents given only the prompt with its inputs filled in, never your notes or opinions.
- Reviews and grades come from the `dadhichi-head` agent (a different model). Give it file paths and the path to write its review to. You build and edit; it judges. Never grade your own outputs.
- Freeze an exact copy of the prompt as `prompt.md` in every run folder before running it.
- A released version is never edited; a fix is a new version. Promote only when the head says the new version passes more checks and fails none the old one passed.
- Every failure goes into that pattern's `failures.md`, one line each.
- Do not use real people's private data or invent quotes or statistics in test inputs.
- Stay inside this project folder. Do not install software, change settings, or contact anyone. On the Mac, the runner script handles git push; in a cloud session (no runner), push your commit to the session's branch at the end.

Before you finish:
1. Add a line to `CHANGELOG.md` under today's date for anything built, tested or decided.
2. Tick `[x]` a backlog item only when the whole item is done. If you split it, add the new sub-items under it.
3. Overwrite `loop/STATE.md` with: date and time, the item, what you finished, the exact next step, and any decision you made that the user should review.
4. Commit: `git add -A` then `git commit -m "<short summary of the round>"`.

Your last line must be exactly one of these:
DADHICHI-STATUS: CONTINUE
DADHICHI-STATUS: IDLE   (only if no `[ ]` items are left)
DADHICHI-STATUS: BLOCKED <one-sentence reason a human must fix>

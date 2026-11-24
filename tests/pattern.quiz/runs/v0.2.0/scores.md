# v0.2.0 scores

Writer: fresh general-purpose subagents on Claude Opus 5.5, sheet mode, file output, 2026-11-24. Inputs 1, 3 and 4 had shell access available; input 5 was rerun with code execution forbidden after its first output was lost (see below). Grader: the dadhichi-head agent on Opus, because its usual model was out of usage credits. Input 3 was graded in two halves: checks 2–3 for Q1–50 in part 1, Q51–100 plus all other checks in part 2.

| Input | Questions | Answers verified correct | Pass | Borderline | Fail | Fails on |
| --- | --- | --- | --- | --- | --- | --- |
| 1 React effects (low) | 30 | 30/30 | 14 | 1 | 0 | — (16 Borderline) |
| 3 PostgreSQL isolation (high) | 100 | 100/100 answers; 2 traces with a misordered step | 12 | 2 | 1 | 9 coverage |
| 4 Bond prices (medium) | 60 | 60/60 | 11 | 1 | 3 | 16 copying, 9 coverage, 10 distractors |
| 5 Python list.map (low, false premise) | 30 | 30/30 | 12 | 3 | 0 | — |

Every answer in all 220 questions agreed with the grader's independent work. The weaknesses are in question design, not correctness: copying or near-copying calibration examples, restaged near-duplicates passed off as "different shapes", distractors that no stated belief produces, and stem wording that leaks the outcome. v0.3.0 applies the graders' quoted edits for all four.

Not run this round: inputs 2, 6, 7, 8, 9 (interactive mode is untested).

Incident: another agent working in the same checkout moved this run folder to `../v0.2.0-gemini-4-neon/` at 02:41 while the writers were running. The frozen prompt and filled prompts were restored by copy from built/ and that folder; the first input-5 output was lost and rerun. Treat `../v0.2.0-gemini-4-neon/` as that agent's separate run.

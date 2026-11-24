# v0.2.0 scores (Gemini 4 Neon, graded by GPT-6.2 Astra)

Writer: fresh `gemini-4-neon` subagents given only the filled frozen prompt (`v0.2.0`), 2026-11-24, with no code execution. Independent grader: `gpt-6.2-astra` (Codex, `reasoningEffort: high`), which worked every answer independently and verified code/math outputs with Python 3 / Node where applicable.

| Input | Mode & depth | Questions graded | Independent answer match | Pass | Borderline | Fail | N/A | Key failures / findings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [1 React effects](1-react-effects/head-grading.md) | sheet, low | 30 | 29/30 literal (Q23 `2**53` precision) | 9 | 3 | 3 | 1 | Check 2 (Q23 literal nontermination, Q1 paint claim), Check 3 (Q19 two lines, Q23), Check 10 (Q8 distractor arithmetic), Check 16 Borderline (Q1) |
| [3 PostgreSQL isolation](3-postgres-isolation/head-grading.md) | sheet, high | 100 | 98/100 (Q54 wrong; Q91 overstates guarantee) | 8 | 1 | 6 | 1 | Check 2 & 14 (Q54 wrongly teaches `ON CONFLICT DO NOTHING` avoids `40001` in RR), Check 3 (Q46, Q83, Q91, Q99), Check 4 (fresh sequence assumptions), Check 9 (Q1/Q2, Q32/Q75), Check 10 (Q38(d), Q46(d)) |
| [4 Bond prices](4-bond-prices/head-grading.md) | sheet, medium | 60 | 60/60 keyed answers (several trace rounding slips) | 8 | 1 | 6 | 1 | Check 16 (Q8 copies calibration example), Check 9 (Q10/Q28, Q26/Q36), Check 10 (Q15(d) impossible fall from $100 to $102), Check 11 (Q25 leaks 6% yield), Check 4 (Q2/Q29/Q32 settings), Check 14 (Q56 overclaimed call rule) |
| [5 Python list.map](5-python-list-map/head-grading.md) | sheet, low | 30 | 30/30 CPython 3.12.14 (Q22 trace global vs closure) | 11 | 1 | 3 | 1 | Check 13 (opening scope note gives away Q1), Check 9 (combined mechanism 9 hides missing 2nd closure Q), Check 10 (Q8(b)/(d) distractors) |
| [7 Dadhichi loop (`SOURCE`)](7-dadhichi-loop/head-grading.md) | sheet, low | 30 | 27/30 (Q12, Q25, Q29 overclaim beyond `LOOP.md`) | 8 | 0 | 7 | 1 | Check 2 & 14 (Q12 says Mac needs nothing else, omitting status line; Q25/Q29 overclaim), Check 3 (Q25, Q29), Check 9 (Q3/Q20 duplicate), Check 10 (Q17(b)/(c) filler), Check 11 & 13 (Q27 quotes file & agent verbatim) |
| [9 JS closures](9-js-closures/head-grading.md) | interactive, low | 10 graded (+10 Part 2) | 10/10 Node v24 (3 Why traces misattribute `console.log`) | 13 | 1 | 1 | 1 | Check 9 (Q15 repeats Q4 counter shape); **Check 15 Diagnosis: Pass (3/3 wrong beliefs diagnosed)**; early-stop scorecard places mechanism map at head |

**Totals across 6 inputs (90 applicable checks):** 57 Pass, 7 Borderline, 26 Fail (6 N/A).

Not run in this batch: inputs 2 (JS event loop), 6 (Kubernetes vague), 8 (Chess pawn endgames — timed out thinking after retrograde-tablebase exec was blocked).

## Cross-model takeaways for v0.3.0

1. **Interactive mode works well out of the box** (13/15 Pass on Input 9; 10/10 JS answers correct; 3/3 deliberate learner misses accurately diagnosed; early-stop scorecard properly structured).
2. **High-volume accuracy is strong, with subtle edge-case risks:** 254/260 graded answers matched independent verification (including 60/60 bond math and 30/30 CPython executions), but `gpt-6.2-astra` caught one genuine PostgreSQL 16 engine misconception (Q54 `ON CONFLICT DO NOTHING` in `REPEATABLE READ`), one JS floating-point literalism issue (React Q23), and three source-extrapolation slips on Input 7.
3. **Recurring prompt-level gaps beyond Claude's 4-input run:**
   - **Opening / stem answer leakage** (Input 5 opening scope note spoiling Q1; Input 7 Q27 quoting file/agent; Input 4 Q25 stating the 6% yield).
   - **Strict source entailment** (Input 7 turning permissive rules into mandatory outcomes and omitting a required step stated elsewhere in `SOURCE`).
   - Both gaps were folded into `built/quiz.upskill.md` v0.3.0 alongside the copying, near-duplicate, stem-wording, and distractor-derivation fixes.

# Loop state

2026-11-18, cloud session (GitHub push works again).

Item: Explain, backlog Stage 1 items 2 and 3 (test run, grading, promotion).

Finished:
- v0.2.2 gate review (head on Opus): REVISE, 5 edits -> v0.3.0.
- v0.3.0 test run (inputs 1x3, 2, 3, 4, 5, 7, 9) graded: PROMOTE over v0.2.1, still draft.
- domains/finance.md 0.1.0 draft; input 8 run on v0.3.0 (runs/v0.3.0-finance), not yet graded.
- v0.3.1 = the head's five v0.3.0 grading edits, applied verbatim. Gate review skipped because every change is the head's own wording; the grading of the v0.3.1 run doubles as its review.
- v0.3.1 test run started: inputs 1, 2, 3, 4, 5, 7, 8 (finance), 9 twice.

- v0.3.1 graded: NOT PROMOTED (tie with 0.3.0). Released version stays 0.3.0.
- v0.4.0 = v0.3.1 + the head's five v0.3.1 edits; finance domain 0.1.1. Test run started at n=2 on inputs 2, 3, 7, 8, 9 and n=1 on 1, 4, 5 (13 outputs, runs/v0.4.0 and runs/v0.4.0-finance).

Also done: built/grade.md 0.2.0 (grader, meta pack) after a head gate review; tests/pattern.grade/ with 8 inputs, a planted-fault input and a 9-check rubric. Backlog extended with stages 3a, 5 and 6 from MASTER_PLAN.

Since then:
- Explainer v0.4.0 PROMOTED (released). v0.4.1 = the head's five v0.4.0 edits; 13 outputs written (input 6 now uses the design doc as long source). Head grading of v0.4.1 in progress -> runs/v0.4.1/head-grading.md.
- Grader v0.2.0 graded: NOT USABLE (89% agreement, 9/10 recall, lenient on padding). Grader v0.3.0 written; test set gained conventions.md, relabels and saved filled prompts. v0.3.0 run (8 inputs, Sonnet) in progress -> tests/pattern.grade/runs/v0.3.0/.

Since then:
- Grader 0.3.0 is TESTED (94.5% agreement, 10/10 recall, on claude-sonnet-5-5).
- Explainer: 0.4.1 not promoted; 0.4.2 not promoted (tie on Passes; 1b over 600 words); 0.4.3 = the head's v0.4.2 edits. Released explainer is still 0.4.0.
- Rubric writer 0.2.0 written after a gate review; its test run has not started.

Exact next steps:
1. When the 18 v0.4.3 outputs (runs/v0.4.3, runs/v0.4.3-finance) and the 3 extra v0.4.0 samples (runs/v0.4.0/1b, 4b, 5b) exist: head grades v0.4.3 against v0.4.0 at matched n=2 -> runs/v0.4.3/head-grading.md. Promote / tested decision.
2. Rubric writer 0.2.0 test run: 11 outputs (inputs 1, 1b, 2-8, input 7 twice), then head grading.
3. BACKLOG Stage 3a: test input writer, cold reader.

Decisions for the owner:
- The head ran on Opus (claude-opus-5-5) because Fable 5.2 was out of credits. Builder and test writers are also Opus; grader tests run on Sonnet. Regrade with Fable when credits return.
- The human phone check on explain inputs 1 and 2 (design section 7) has not been done; it needs a person.

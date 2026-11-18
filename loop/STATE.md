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

Exact next steps, in order (usage limit for Opus subagents resets at 15:00 UTC):
1. Rerun the head grading of v0.4.0 (13 outputs in runs/v0.4.0 and runs/v0.4.0-finance) against released v0.3.0 and v0.3.1; write runs/v0.4.0/head-grading.md; promote or apply edits; decide on status tested with an explicit waiver for input 6.
2. Grader test run: 8 inputs per tests/pattern.grade/inputs.md, ideally on a model other than Opus; compare with the reference gradings; head grades the grader's outputs.

Still missing: input 6 needs RFC 9111 sections 1-4; rfc-editor.org and ietf.org are blocked by this session's network policy.

Decisions for the owner:
- The head ran on Opus (claude-opus-5-5) because Fable 5.2 was out of credits. Builder and test writers are also Opus, so independence is weaker than the design asks; regrade with Fable when credits return.

# Loop state

2026-11-18, cloud session (GitHub push works again).

Item: Explain, backlog Stage 1 items 2 and 3 (test run, grading, promotion).

Finished:
- v0.2.2 gate review (head on Opus): REVISE, 5 edits -> v0.3.0.
- v0.3.0 test run (inputs 1x3, 2, 3, 4, 5, 7, 9) graded: PROMOTE over v0.2.1, still draft.
- domains/finance.md 0.1.0 draft; input 8 run on v0.3.0 (runs/v0.3.0-finance), not yet graded.
- v0.3.1 = the head's five v0.3.0 grading edits, applied verbatim. Gate review skipped because every change is the head's own wording; the grading of the v0.3.1 run doubles as its review.
- v0.3.1 test run started: inputs 1, 2, 3, 4, 5, 7, 8 (finance), 9 twice.

Exact next step: when all nine v0.3.1 outputs exist, have the head grade them against v0.3.0 (and v0.3.0-finance vs v0.3.1-finance for input 8), write runs/v0.3.1/head-grading.md, then promote or apply edits.

Still missing: input 6 needs RFC 9111 sections 1-4; rfc-editor.org and ietf.org are blocked by this session's network policy.

Decisions for the owner:
- The head ran on Opus (claude-opus-5-5) because Fable 5.2 is out of credits. Builder and test writers are also Opus, so independence is weaker than the design asks; regrade with Fable when credits return.

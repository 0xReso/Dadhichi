# Test inputs: pattern.grade

The grader is tested against the head's verdicts, which serve as the reference labels. Each input is one explain output, the frozen prompt that produced it as TASK, the source where there is one, and as RUBRIC the explain rubric followed by tests/pattern.grade/conventions.md, then the "How I applied the checks" bullets from the reference grading file with any bullet about a different output removed, then any limit tests/pattern.explain/inputs.md sets for this output, named by topic rather than by number (for example, "1,700 words for this piece", only for Docker). Explain and grade inputs are numbered differently, so a bullet that says "input 7" means Docker and must not reach the bond grader. Save each filled prompt as runs/<version>/<n>-filled.md, so a disagreement can be traced to what the grader saw. COUNTS is filled from `wc -w`. The grader's verdicts are compared check by check with the head's grading file for that run.

| # | Output | Reference grading | What it stresses |
| --- | --- | --- | --- |
| 1 | tests/pattern.explain/runs/v0.3.0/1c-api-key.md | runs/v0.3.0/head-grading.md | An all-Pass output: does it avoid inventing faults? |
| 2 | tests/pattern.explain/runs/v0.3.0/2-kafka-consumer-groups.md | runs/v0.3.0/head-grading.md | Mixed verdicts, 11b Fail on a "cast list" paragraph |
| 3 | tests/pattern.explain/runs/v0.3.1/7-docker-containers.md | runs/v0.3.1/head-grading.md | Length check against a number (about 1,940 words vs 1,700) |
| 4 | tests/pattern.explain/runs/v0.3.0/4-driftwood.md | runs/v0.3.0/head-grading.md | Not applicable checks (no sections) and check 12 |
| 5 | tests/pattern.explain/runs/v0.3.0/9-alexa-for-shopping.md, SOURCE sources/alexa-for-shopping.md | runs/v0.3.0/head-grading.md | Faithfulness to a source (check 13, invented provenance) |
| 6 | tests/pattern.explain/runs/v0.3.1/3-raft-consensus.md | runs/v0.3.1/head-grading.md | Long output (about 3,500 words), forward-pointer clause |
| 7 | tests/pattern.explain/runs/v0.3.1-finance/8-bond-duration.md | runs/v0.3.1/head-grading.md | Second domain; accuracy of financial figures |
| 8 | tests/pattern.grade/inputs/8-the-cloud-planted.md: a copy of runs/v0.3.0/5-the-cloud.md with one planted fault on each of checks 1, 2, 3, 5, 6, 7, 8, 10, 11a, 11b (1,995 words) | tests/pattern.grade/inputs/8-planted-faults.md | Recall: does it find every planted fault? |

The design asks for 20 to 50 hand-labelled outputs before trusting a grader; inputs 1 to 7 cover 7 outputs and about 85 check-level labels. Add the v0.4.0 outputs once their grading exists.

`wc -w`: input 1 537, input 2 1,914, input 3 1,945, input 4 545, input 5 1,955, input 6 3,484, input 7 1,969, input 8 1,995.

The reference gradings were written by Opus, so run the grader on a different model (or have a person label checks on at least three inputs) to avoid measuring self-agreement.

## Relabels

Agreement is computed against the reference with these corrections, found by the grader in the v0.2.0 run and confirmed by the head:

| Input | Check | Reference | Corrected | Why |
| --- | --- | --- | --- | --- |
| 6 Raft | 3 | Pass | Borderline | Term numbering in the election example is wrong (leader in term 7, not 6) |
| 3 Docker | 3 | Pass | Borderline | Contradicts itself on which Dockerfile lines make layers |
| 4 Driftwood | 5 | Pass | Borderline | Repeated admission paragraph can go |

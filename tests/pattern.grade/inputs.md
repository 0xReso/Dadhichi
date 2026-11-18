# Test inputs: pattern.grade

The grader is tested against the head's verdicts, which serve as the reference labels. Each input is one explain output, the explain rubric, the frozen prompt that produced it as TASK, and the source where there is one. The grader's verdicts are compared check by check with the head's grading file for that run.

| # | Output | Reference grading | What it stresses |
| --- | --- | --- | --- |
| 1 | tests/pattern.explain/runs/v0.3.0/1c-api-key.md | runs/v0.3.0/head-grading.md | An all-Pass output: does it avoid inventing faults? |
| 2 | tests/pattern.explain/runs/v0.3.0/2-kafka-consumer-groups.md | runs/v0.3.0/head-grading.md | Mixed verdicts, 11b Fail on a "cast list" paragraph |
| 3 | tests/pattern.explain/runs/v0.3.1/7-docker-containers.md | runs/v0.3.1/head-grading.md | Length check against a number (about 1,940 words vs 1,700) |
| 4 | tests/pattern.explain/runs/v0.3.0/4-driftwood.md | runs/v0.3.0/head-grading.md | Not applicable checks (no sections) and check 12 |
| 5 | tests/pattern.explain/runs/v0.3.0/9-alexa-for-shopping.md, SOURCE sources/alexa-for-shopping.md | runs/v0.3.0/head-grading.md | Faithfulness to a source (check 13, invented provenance) |
| 6 | tests/pattern.explain/runs/v0.3.1/3-raft-consensus.md | runs/v0.3.1/head-grading.md | Long output (about 3,500 words), forward-pointer clause |
| 7 | tests/pattern.explain/runs/v0.3.1-finance/8-bond-duration.md | runs/v0.3.1/head-grading.md | Second domain; accuracy of financial figures |
| 8 | A copy of input 1 with one planted fault per check (to be written) | the planted faults | Recall: does it find every planted fault? |

The design asks for 20 to 50 hand-labelled outputs before trusting a grader; inputs 1 to 7 cover 7 outputs and about 85 check-level labels. Add the v0.4.0 outputs once their grading exists.

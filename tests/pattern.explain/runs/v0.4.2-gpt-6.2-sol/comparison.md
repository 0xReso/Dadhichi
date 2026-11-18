# Matched explainer evaluation, 2026-11-18

## Test conditions

The released v0.4.0 prompt and the v0.4.2 candidate each received two samples on all nine inputs. The writer was `gpt-6.2-sol`. Each sample started in a fresh ephemeral Codex CLI session in an empty directory with user configuration ignored. Only the filled prompt block was supplied. A sample that used a tool was excluded. Both versions used the repository design document for input 6, the same backend-developer note for input 7, their frozen finance variants for input 8, and the same Alexa source pack for input 9. The Driftwood writer received the topic name without the evaluator's fictional-tool label. All other optional fields were empty. The prompt and fixture revisions come from commit `cab1c11`.

A fresh `gpt-6.2-astra` session graded each saved output with the library's [Grader v0.3.0](../../../../built/grade.md), the [explainer rubric](../../rubric.md), and the project's [grading conventions](../../../pattern.grade/conventions.md). Each call received its filled task, the source separately where applicable, the Markdown word count and the full output. Other samples and previous grades were withheld. The grader also received the historic pacing convention for check 11b, the simple tier for inputs 1 and 4, the deep tier for input 3, the moderate tier for the rest, and the 1,700-word test threshold on input 7. Checks 6 and 11a are inapplicable to simple articles without chapters or a whole-picture section. Check 12 applies to input 4 and check 13 applies to sourced inputs.

This measures performance with these two GPT models. The project has separately calibrated Grader v0.3.0 on Claude Sonnet. Its recorded agreement on Sonnet does not establish the same agreement here. The historical Claude scorecards remain evidence for the Claude runs.

## Comparison

Each input contributes the worse of its two verdicts on each applicable check. This gives 107 paired cells. All samples agreed on applicability. Counts below are Pass / Borderline / Fail.

| Input | v0.4.0 | v0.4.2 | Candidate words A | Candidate words B | Candidate grades |
| --- | --- | --- | --- | --- | --- |
| 1 | 7/2/1 | 8/1/1 | 430 | 483 | [a](../v0.4.2-gpt-6.2-sol/grades/1a-api-key.md) · [b](../v0.4.2-gpt-6.2-sol/grades/1b-api-key.md) |
| 2 | 9/2/1 | 7/4/1 | 1264 | 1043 | [a](../v0.4.2-gpt-6.2-sol/grades/2a-kafka-consumer-groups.md) · [b](../v0.4.2-gpt-6.2-sol/grades/2b-kafka-consumer-groups.md) |
| 3 | 9/1/2 | 8/4/0 | 1363 | 1405 | [a](../v0.4.2-gpt-6.2-sol/grades/3a-raft-consensus.md) · [b](../v0.4.2-gpt-6.2-sol/grades/3b-raft-consensus.md) |
| 4 | 9/1/1 | 9/2/0 | 318 | 374 | [a](../v0.4.2-gpt-6.2-sol/grades/4a-driftwood.md) · [b](../v0.4.2-gpt-6.2-sol/grades/4b-driftwood.md) |
| 5 | 10/2/0 | 9/2/1 | 1086 | 1373 | [a](../v0.4.2-gpt-6.2-sol/grades/5a-the-cloud.md) · [b](../v0.4.2-gpt-6.2-sol/grades/5b-the-cloud.md) |
| 6 | 7/2/4 | 6/3/4 | 1352 | 1219 | [a](../v0.4.2-gpt-6.2-sol/grades/6a-dadhichi-library.md) · [b](../v0.4.2-gpt-6.2-sol/grades/6b-dadhichi-library.md) |
| 7 | 7/2/3 | 8/3/1 | 1061 | 818 | [a](../v0.4.2-gpt-6.2-sol/grades/7a-docker-containers.md) · [b](../v0.4.2-gpt-6.2-sol/grades/7b-docker-containers.md) |
| 8 | 8/1/3 | 9/1/2 | 980 | 958 | [a](../v0.4.2-finance-gpt-6.2-sol/grades/8a-bond-duration.md) · [b](../v0.4.2-finance-gpt-6.2-sol/grades/8b-bond-duration.md) |
| 9 | 9/1/3 | 9/2/2 | 1057 | 1068 | [a](../v0.4.2-gpt-6.2-sol/grades/9a-alexa-for-shopping.md) · [b](../v0.4.2-gpt-6.2-sol/grades/9b-alexa-for-shopping.md) |
| Total | 75/14/18 | 73/22/12 | | | |


## Decision

Keep v0.4.0 as the promoted draft. v0.4.2 removed six Fail verdicts on balance, but lost two Passes. Two cells moved from Pass to Fail. The cloud article uses “requests” before introducing the computing meaning. The library article asks the reader to interpret “Kafka consumer groups” before explaining what the phrase means. [Cloud evidence](grades/5a-the-cloud.md) · [Library evidence](grades/6b-dadhichi-library.md)

The most direct change to try is to open each example with the problem in everyday language and introduce the technical label where its meaning becomes clear. Check the example's opening and subtitle as well as the body. Verify the change on the two regression cases before another full comparison.

One limit of the terminology grades is how literally the judge treats titles and familiar words. For instance, it counted “API” in the requested title against input 1a. Treat close calls as items for human review. No human phone-read was performed. The existing Claude scorecard uses different models and covers fewer paired cells.

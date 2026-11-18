# Rubric writer v0.2.0 evaluation

Ten fresh samples cover the nine input definitions. Input 7 was repeated. Each sample used the frozen rubric writer and the same session settings and writer/grader pairing as the [explainer comparison](../../../pattern.explain/runs/v0.4.2-gpt-6.2-sol/comparison.md). Input 1 included the frozen v0.4.0 explainer, while 1b omitted it. Both received the five suspected causes with the original check labels removed. The grader received the hand-built reference only for these two inputs. The count for each output is the number of numbered Markdown table rows.

| Input | Checks written | Pass | Borderline | Fail | Inapplicable | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | 7 | 0 | 4 | 0 | [Rubric](1-rubric.md) · [Grade](grades/1-rubric.md) |
| 1b | 9 | 6 | 1 | 4 | 0 | [Rubric](1b-rubric.md) · [Grade](grades/1b-rubric.md) |
| 2 | 8 | 7 | 0 | 2 | 2 | [Rubric](2-rubric.md) · [Grade](grades/2-rubric.md) |
| 3 | 7 | 9 | 0 | 1 | 1 | [Rubric](3-rubric.md) · [Grade](grades/3-rubric.md) |
| 4 | 8 | 6 | 0 | 3 | 2 | [Rubric](4-rubric.md) · [Grade](grades/4-rubric.md) |
| 5 | 8 | 5 | 2 | 2 | 2 | [Rubric](5-rubric.md) · [Grade](grades/5-rubric.md) |
| 6 | 7 | 5 | 1 | 3 | 2 | [Rubric](6-rubric.md) · [Grade](grades/6-rubric.md) |
| 7a | 5 | 9 | 0 | 0 | 2 | [Rubric](7a-rubric.md) · [Grade](grades/7a-rubric.md) |
| 7b | 5 | 9 | 0 | 0 | 2 | [Rubric](7b-rubric.md) · [Grade](grades/7b-rubric.md) |
| 8 | 7 | 8 | 0 | 1 | 2 | [Rubric](8-rubric.md) · [Grade](grades/8-rubric.md) |

## Decision

Keep the rubric writer in draft. Check 4 (overlap) failed on 8 samples. In the code-review rubric, omitting the consequence of a bug can fail two checks. In the SQL rubric, returning a preview instead of the requested update can also fail two checks. Input 1b invents a 1,500-word fallback cap when the brief gives none. These failures change the grades a downstream reader would assign.

For the next revision, have the writer try a single concrete fault against every proposed check before returning the table. If it triggers two checks, distinguish the evidence each requires or combine them. Use an explicit limit from the task when available and a reader-observable criterion otherwise.

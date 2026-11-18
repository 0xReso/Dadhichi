# Head grading: built/grade.md v0.3.0 (second test run)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the Sonnet subagents that wrote the grader outputs. The reference gradings were also written by Opus, but the graded model is Sonnet, so this run is not measuring self-agreement.

Date: 2026-11-18. Stage: grading after the v0.3.0 test run, compared with v0.2.0.
Read: the design doc, tests/pattern.grade/inputs.md (with the Relabels table), rubric.md, conventions.md, failures.md, my v0.2.0 grading, the frozen v0.3.0 prompt, the eight filled prompts (1-filled.md to 8-filled.md), the eight grader outputs (1.md to 8.md), the planted-fault list, and the relevant evidence in tests/pattern.explain/runs/v0.3.0/head-grading.md and runs/v0.3.1/head-grading.md.
Scoring rule (unchanged from v0.2.0): Borderline against Pass or Fail is half a miss, Pass against Fail a full miss. Not applicable cells are listed but kept out of the main figure. The reference is the head grading with the three relabels applied (Raft 3 B, Docker 3 B, Driftwood 5 B).

## Verdict: USABLE (status can move to tested)

- Agreement on inputs 1 to 7, relabels applied: 94.5% (77.5 of 82 applicable cells; 9 half-misses, no full misses). With the 16 Not applicable cells, all of which match: 95.4%. Without the relabels: 92.7%.
- Dropping the one harness-caused cell (Docker check 4, below): 95.1% (77.0 of 81).
- False Fail (Fail where the reference gives Pass): 0.
- False Pass (Pass where the reference gives a non-Pass): 3, down from 9.
- Recall on input 8: 10 of 10 planted faults get a non-Pass on their own check; checks 4 and 9 stay Pass.
- Quotes: every quoted string I checked (all of them, in all eight outputs) is verbatim in the graded output, apart from fair ellipses and nested-quote changes.
- Counts: all eight use the supplied `wc -w` figure and say so ("The supplied count is 537 words"). Error 0% on every input, against 8 to 13% on five inputs in v0.2.0.

The bar in rubric.md is ≥90% agreement, no false Fails, full recall on input 8 and real quotes. All four are met with room to spare, and the main v0.2.0 failure (padding never flagged) is gone: check 5 now matches on 6 of 7 inputs and the planted padding is caught.

Caveats that do not block, but should be in the record: this is n=1 per input on 7 labelled outputs (about 82 check labels), short of the design's 20 to 50 outputs. The lean has flipped: the grader is now harsher than the reference on 6 cells and kinder on 3. None of the harsher cells is a false Fail, but 3 are false Borderlines on Pass cells, and those move Pass counts in version comparisons.

Single most important fix next: explain check 1 (No lookups). Three of the nine disagreements are on it, two of them harsher and one kinder, and it is the check the explain rubric names as the point of the pattern. The grader does not know that a term the reader's notes cover counts as introduced, or whether the sub-terms inside a "Going further" line are in scope, and it skips the opening line. This is a conventions.md fix (edit 1 below), not a prompt fix.

## Score table: pattern.grade checks on each grader output

P = Pass, B = Borderline, F = Fail, - = not applicable.

| # | Check | 1 API key | 2 Kafka | 3 Docker | 4 Driftwood | 5 Alexa | 6 Raft | 7 Bond | 8 Cloud planted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Complete | P | P | P | P | P | P | P | P |
| 2 | Agreement | P | P | B | P | P | P | P | P |
| 3 | No false Fail | P | P | P | P | P | P | P | P |
| 4 | Evidence | P | P | P | P | P | P | P | P |
| 5 | Quotes real | P | P | P | P | P | P | P | P |
| 6 | Counts | P | P | P | P | P | P | P | P |
| 7 | Independent | P | P | P | P | P | P | P | P |
| 8 | Clean output | P | P | P | P | P | P | P | P |
| 9 | Recall | - | - | - | - | - | - | - | P |
| | P / B / F | 8 / 0 / 0 | 8 / 0 / 0 | 7 / 1 / 0 | 8 / 0 / 0 | 8 / 0 / 0 | 8 / 0 / 0 | 8 / 0 / 0 | 9 / 0 / 0 |

Totals: 64 Pass, 1 Borderline, 0 Fail, 7 Not applicable, of 72 cells. v0.2.0: 59 / 3 / 2.

### Reasoning, check by check

Check 1, Complete. All eight give 14 verdict lines in rubric order (1 to 10, 11a, 11b, 12, 13), one verdict each, then a Summary. The Summary counts are correct on all eight (I recounted each). Outputs 4 and 6 put blank lines between verdicts, which is harmless. Pass on all.

Check 2, Agreement, per input (relabels applied):
- Input 1: 10 of 10 = 100%. Pass.
- Input 2: 11.5 of 12 = 95.8%. Pass.
- Input 3: 10.5 of 12 = 87.5% raw; 10.0 of 11 = 90.9% with the harness cell dropped. Borderline: under the line as computed, over it once the cell the grader could not have got right is removed. Non-Pass evidence: "1. No lookups: ... SIGTERM and SIGKILL are never glossed, though this reader knows Linux processes ... **Borderline**" against reference P; "5. No padding: ... Going further repeats nothing from the body. **Pass**" against reference B.
- Input 4: 10 of 11 = 90.9%. Pass.
- Input 5: 12 of 13 = 92.3%. Pass.
- Input 6: 12 of 12 = 100%. Pass.
- Input 7: 11.5 of 12 = 95.8%. Pass.
- Input 8: 12 of 12 applicable cells agree with the planted labels (every plant non-Pass, 4 and 9 Pass). Pass.

Check 3, No false Fail. The three Fails that differ from the reference (Docker 4, Driftwood 10, Alexa 10) are all against Borderlines. No Fail sits on a reference Pass. Pass on all.

Check 4, Evidence. Every non-Pass quotes the output, gives a count or names an absence. Examples: Raft check 3 quotes "Dogwood's countdown runs out... becomes leader in term 6" and states the rule broken; Kafka 11b names the three terms in each paragraph; cloud 11a names the absence ("Live migration is never explained or shown in the body"). Pass on all.

One evidence slip, logged as a watch item: input 8 check 3 says "the output's own domain notes put it at tens to a couple of hundred milliseconds". That sentence is in graded_task (the domain block, filled line 89), not in the output. The verdict stands on the quoted output line and on general knowledge, so it is not marked down, but the attribution is wrong and the prompt's check list says quotes "come from the graded output, not from the task or source".

Check 5, Quotes real. I checked every quoted string against the graded output in each filled prompt. All are verbatim, apart from fair ellipses ("Cedar now becomes a candidate... called RequestVote"; "Raft chooses to stop rather than risk disagreement... out of action for writes whenever three of its members are down") and nested quotes switched to single (Alexa: "'the jug I bought in March'"). Kafka check 5 drops the bold markers round "Cooperative rebalancing and the new consumer group protocol", which is fine. Pass on all.

Check 6, Counts. Every grader used the graded_counts figure and named it as supplied. Edit 5 did exactly what it was for.

| Input | `wc -w` | Grader | Difference |
| --- | --- | --- | --- |
| 1 | 537 | 537 (supplied) | 0% |
| 2 | 1,914 | 1914 (supplied) | 0% |
| 3 | 1,945 | 1945 (supplied) | 0% |
| 4 | 545 | 545 (supplied) | 0% |
| 5 | 1,955 | 1955 (supplied) | 0% |
| 6 | 3,484 | 3484 (supplied) | 0% |
| 7 | 1,969 | 1969 (supplied) | 0% |
| 8 | 1,995 | 1995 (supplied, "includes the preamble line") | 0% |

The v0.2.0 near-miss on Docker ("about 2,200 ... at the edge of the ceiling") cannot recur. Pass on all.

Check 7, Independent. No verdict rests on another check's fault. Two cases are close and pass. Driftwood check 10 adds "The second paragraph also reads as a repeated preamble". The repetition is the check 5 fault, but the verdict rests on "the material I was given", and the reference also cites that paragraph under check 10. Cloud check 5 cites the IaaS/PaaS/SaaS table as repeating the prose. The table is the check 7 plant, but the table really does restate the three paragraphs around it, so this is a check 5 reason in its own right, and the verdict also stands on the planted paragraph. Pass on all.

Check 8, Clean output. Only verdict lines and a Summary, with no preamble, rewrite advice or offers. A small drift, not a breach: the Summary is meant to name "the one failure ... in one sentence", but Docker names two ("11b ... and the 1945-word length (check 4)"), Alexa uses two sentences ("Check 10 ... is a close second"), and cloud names three checks. Pass on all.

Check 9, Recall. 10 of 10 (table below). Pass.

## Agreement table, inputs 1 to 7, cell by cell

Each cell is reference / grader, with the relabels applied (marked r). A cell marked x is a disagreement; "-" is not applicable.

| # | Check | 1 API key | 2 Kafka | 3 Docker | 4 Driftwood | 5 Alexa | 6 Raft | 7 Bond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P / P | P / P | P / B x | B / P x | F / F | P / P | P / B x |
| 2 | Linear | P / P | P / B x | P / P | P / P | P / P | B / B | B / B |
| 3 | Accurate | P / P | P / P | Br / B | P / P | B / P x | Br / B | P / P |
| 4 | Proportional | P / P | P / P | B / F x | P / P | P / P | P / P | P / P |
| 5 | No padding | P / P | B / B | B / P x | Br / B | B / B | B / B | B / B |
| 6 | Resumable | - / - | B / B | P / P | - / - | B / B | P / P | P / P |
| 7 | Plain text | P / P | P / P | P / P | P / P | P / P | P / P | P / P |
| 8 | Not dumbed down | P / P | P / P | P / P | P / P | P / P | P / P | P / P |
| 9 | Trap handled | P / P | P / P | P / P | P / P | P / P | P / P | P / P |
| 10 | Clean output | P / P | P / P | P / P | B / F x | B / F x | P / P | P / P |
| 11a | Complete | - / - | P / P | P / P | - / - | P / P | P / P | P / P |
| 11b | Unhurried | P / P | F / F | F / F | F / F | F / F | B / B | F / F |
| 12 | Unknown topic | - / - | - / - | - / - | P / P | - / - | - / - | - / - |
| 13 | Source confidence | - / - | - / - | - / - | - / - | F / F | - / - | - / - |
| | Applicable cells | 10 | 12 | 12 | 11 | 13 | 12 | 12 |
| | Misses (half each) | 0 | 0.5 | 1.5 | 1.0 | 1.0 | 0 | 0.5 |
| | Agreement | 100% | 95.8% | 87.5% | 90.9% | 92.3% | 100% | 95.8% |

All 9 disagreements are one step apart. 16 Not applicable cells match.

By explain check: 11b, 13, 12, 9, 8, 7, 6 and 11a are exact on every input. Check 5 is 6 of 7 (was 1 of 7). Check 2 is 6 of 7, check 3 6 of 7, check 4 6 of 7. Check 10 is 5 of 7. Check 1 is the weakest at 4 of 7 (was 7 of 7).

### Who is more likely right, disagreement by disagreement

| Input, check | Ref / grader | More likely right | Why |
| --- | --- | --- | --- |
| 2, 2 | P / B | Toss-up; the convention is at fault | The grader applied conventions.md literally: "Before seeing how it does it, two more pieces of Kafka need to be in place" "promises a later explanation inside a section, which the conventions mark as Borderline". The reference passed it as a signpost that nothing depends on. It is the last sentence of the first section, a transition saying what comes next, not a clause hanging a promise on a term ("which matters a little further on"). The run is also inconsistent: the Alexa grader passed "Keep the filter question in mind; the rest of this piece follows it through". This is the over-correction v0.2.0 edit 2 warned about, but the grader's stated reason is the convention, not edit 2. Edit 2 below narrows the convention. |
| 3, 1 | P / B | Reference | The reader's note in the task says "I know Linux processes well", and the task's plan step 3 says to remove what the reader already has. SIGTERM, SIGKILL, PID, pip and Debian are known to a backend developer who knows Linux processes. The grader saw this ("though this reader knows Linux processes") and marked Borderline anyway, because the rubric line "Every term ... introduced" does not mention the reader. Edit 1. |
| 3, 4 | B / F | Grader, under what it saw; harness fault | The v0.3.1 reference bullet reads "the rubric's ceiling is 2,200, and inputs.md sets 1,700 for this input. Meeting the first and missing the second is Borderline." The harness renamed it by topic, as v0.2.0 edit 1 asked, but dropped the severity sentence. The grader got "Limit for this piece: at most 1,700 words (check 4)" (3-filled.md line 261), and 1,945 over a stated limit is a Fail under the prompt's verdict scale. Edit 3. |
| 3, 5 | B / P | Reference | The reference marks the SIGTERM wait, 0.0.0.0, the fork case and "the second trap" as passages that can go without a gap. The grader swept them (its nearest miss is the VM contrast) but the conventions describe deletable passages only as repeats or self-deferrals, so practical tips that are new but not needed did not register. Same cell as v0.2.0. Edit 1. |
| 4, 1 | B / P | Reference | "Rust" is in the first sentence ("a Rust job scheduler called Driftwood") and is explained six paragraphs later ("Rust is a programming language known for speed"). The grader's nearest miss is "library", so its sweep did not reach the opening line. v0.2.0 matched this cell. Edit 1 names the opening in scope. |
| 4, 10 | B / F | Grader, under the rules as written | "the material I was given contains nothing about it" is the leak conventions.md names. The convention gives no severity, and the prompt's Fail is "at least one instance you can quote breaks the pass condition". The reference applied an unwritten "one leak phrase is Borderline". This is the same mechanism as check 6 in v0.2.0. Edit 4. |
| 5, 3 | B / P | Reference | The output still says the diagram "leaves out the one internal component Amazon has confirmed, the model router", while the same paragraph lists Bedrock, RAG and user memory as confirmed. The grader's nearest miss is "All of these models run on Amazon Bedrock". Edit 4 of v0.2.0 (test the output against itself) caught the Raft and Docker contradictions but not this one, where the clash is between a claim and a list two sentences earlier. Same cell as v0.2.0. Edit 5. |
| 5, 10 | B / F | Grader, under the rules as written | Same as 4, 10: "the material given here" and "the source you were given", with no severity in the convention. Edit 4. |
| 7, 1 | P / B | Toss-up, lean reference | The grader's main ground is "callable bonds and mortgage-backed securities" in the "Going further" line on effective duration. The reference passed it, and passed "discounted harder" as inferable. "Going further" is the desk-lookup list, and the Raft grader in this run treated Going further terms as "desk pointers for later lookup". Two graders, two readings: the scope is unwritten. Edit 1. |

Tally: the reference is more likely right on 5 cells (including the lean), the grader on 2 (4, 10 and 5, 10) under the rules as written, 1 is a harness fault (3, 4), and 1 is a toss-up caused by the convention's wording (2, 2). Counting the grader-right cells as matches and dropping the harness cell, agreement is 96.3% (78.0 of 81).

No new relabels are proposed. The two check 10 cells should be settled by writing the severity down (edit 4), as was done for check 6, not by relabelling.

## Input 8: recall against the planted faults

| Check | Planted fault | Grader | Caught |
| --- | --- | --- | --- |
| 1 | "usually behind a load balancer and a CDN" | F, quotes it, adds "SLA and points of presence" | Yes |
| 2 | "though the trick only makes full sense once you meet autoscaling much later on" | B, quotes it, cites the convention | Yes |
| 3 | "closer to two full seconds" | F, "about 100 ms or less" (attribution slip, see check 4) | Yes |
| 4 | not planted, should stay Pass | P, supplied count 1995 | Yes |
| 5 | "It is worth pausing to repeat this. ..." | B, quotes it, "repeats the two paragraphs before it" | Yes (was the v0.2.0 miss) |
| 6 | "Renting by the minute" restatement removed | B, quotes "Every cloud provider exposes an API" | Yes |
| 7 | IaaS/PaaS/SaaS table | F, quotes "\| Layer \| You manage \|" | Yes |
| 8 | "its manager, Priya, is watching the clock" | B, quotes it, cites the convention | Yes |
| 9 | not planted, should stay Pass | P | Yes |
| 10 | "Here is the explainer you asked for, written for reading on a Kindle." | F, quotes it | Yes |
| 11a | "live migration quietly moves its virtual machines" in The whole picture | F, quotes it, "never explained or shown in the body" | Yes |
| 11b | six providers plus SLA and points of presence | F, quotes it, "company names count" | Yes |

Recall 10 of 10. Four catches moved from F to B against v0.2.0 (checks 2, 5, 6 and 8), each because conventions.md now rates one instance of that kind as Borderline. That is consistent with the references. Check 8 is arguable: Priya appears once, not "carried through", so under the convention a Pass could be defended. B is the safer verdict for a plant and still counts as caught.

## Comparison with v0.2.0, cell by cell

To compare like with like, v0.2.0 is rescored against the same relabelled reference. On that basis v0.2.0 had 15 disagreeing cells (7.5 misses, 90.9%), and v0.3.0 has 9 (4.5 misses, 94.5%).

| Movement | Cells |
| --- | --- |
| Fixed (miss in v0.2.0, match now), 11 | 1/8 (ticket simile), 2/5 (Kafka Going-further repeat), 2/6 (one cold section, B), 2/8 (bookmark), 5/5 (Alexa padding), 5/6 (one cold section, B), 6/5 (Raft padding), 6/8 (clock), 7/2 ("which is what the next idea handles", B), 7/4 (bond limit, harness fix), 7/5 (DV01 repeat) |
| Still missed, same direction, 2 | 3/5 (Docker practical tips, B/P), 5/3 (Alexa self-contradiction, B/P) |
| Still missed, direction flipped, 2 | 4/10 and 5/10: B/P in v0.2.0, B/F now. The leak is found now; only the severity differs |
| New misses (match in v0.2.0), 5 | 2/2 (P/B, convention wording), 3/1 (P/B, reader note), 3/4 (B/F, harness dropped the severity sentence), 4/1 (B/P, "Rust" in the first line), 7/1 (P/B, Going-further sub-terms) |
| Recall | 9/10 to 10/10 |
| False Pass / false Fail | 9 / 0 to 3 / 0 |

Promotion: by the design's rule (more checks passed, none failed that the old one passed), v0.3.0 beats v0.2.0 on the pattern.grade rubric: 64 / 1 / 0 against 59 / 3 / 2. The one cell that drops from Pass is Docker check 2 (P to B), which is a Borderline, not a Fail, and half of it is the harness cell. Promote v0.3.0.

## Gate-review view of the v0.3.0 edits

- Edit 1 (conventions.md, relabels, saved filled prompts, by-topic limits): worked. It accounts for most of the 11 fixed cells (checks 6 and 8 especially), and the saved filled prompts made the Docker check 4 cause traceable in a minute. It also introduced two problems. The check 2 bullet is broader than the reference's practice (2, 2), and the by-topic rename of the Docker limit dropped its severity (3, 4). The conventions also list only repeats and self-deferrals as deletable, so check 5 still misses passages that are new but not needed (3, 5).
- Edit 2 (a closest call you can only excuse is Borderline): worked on its targets (7/2, the input 8 padding plant). The over-correction it risked shows up in check 1 (3, 1 and 7, 1). There the grader names the reason that would make a Pass plain ("this reader knows Linux processes") and still marks Borderline, because the reason is not in the rubric's wording. Edit 1 below fixes that through conventions, not by softening edit 2.
- Edit 3 (sweep by paragraph; a section-worded condition can be broken by a paragraph): worked. Check 5 went from 1 of 7 to 6 of 7. The watched over-correction did not happen: inputs 1 and 5 keep their reference verdicts (1 stays P, with "Key rotation" named and cleared).
- Edit 4 (test the output against itself; find where the source places a claim): worked on Raft and Docker, and the v0.2.0 router watch item did not recur (the Alexa grader no longer calls a Part A fact unconfirmed). It missed the Alexa "one internal component" contradiction for the second run running (edit 5 below).
- Edit 5 (COUNTS): fully worked; see check 6.
- The v0.2.0 layout slip is still there: in `<verdicts>`, "Where the rubric comes with notes ..." sits between Fail and Not applicable. Fold it into the next version.

The prompt still follows the design rules: seven-section shape plus `<verdicts>`, a reason with each instruction, calm wording, and positive instructions.

## Lines to set in built/grade.md

```
status: tested           # 0.3.0 run 2026-11-18: 94.5% agreement on 82 cells (relabels applied), 0 false Fails, 10/10 recall on input 8, quotes verbatim, counts from wc -w. USABLE (head grading on claude-opus-5-5)
verified_on: <Sonnet model ID used for the 0.3.0 run>, 2026-11-18
```

Fill in the exact Sonnet model ID from the run. Neither the repo nor the run folder records it, and the design asks for the model that was tested, not the head's model.

Scorecard summary (two lines, for the CHANGELOG or the status comment):

```
grade 0.3.0 (Sonnet, 8 inputs): 94.5% agreement with head labels (77.5/82), 0 false Fails, 3 false Passes, recall 10/10, counts exact, all quotes verbatim.
Weakest: explain check 1 (4/7) and check 10 severity (B vs F, 2 cells); was 89.0% and 9/10 in 0.2.0.
```

## Edits for the next round (test set first, then prompt), in order of importance

None of these blocks usability. Edits 1 to 4 are test-set changes and need no prompt version bump. Edit 5 is a prompt wording change (patch, 0.3.1) and needs a full eight-input rerun.

Edit 1 (tests/pattern.grade/conventions.md, add a bullet). Targets 3/1, 4/1, 7/1 and 3/5.

Add:
> - Check 1 (No lookups): a term counts as introduced if the task's notes about the reader, or its list of what the reader already has, cover it. The title and the first sentence are in scope like any other line. In "Going further", only the term each line names needs its one-line gloss; examples inside the gloss are pointers for later lookup and are not checked.

Replace:
> A passage that repeats another passage, including one repeated in "Going further", or that tells the reader it is not needed, can be deleted without a gap.

With:
> A passage that repeats another passage, including one repeated in "Going further", that tells the reader it is not needed, or that adds a practical tip or second pitfall the explanation does not rely on, can be deleted without a gap.

Over-correction to watch: check 5 Borderlines on worked detail that is needed. The test remains "could go without a gap".

Edit 2 (conventions.md, check 2 bullet). Targets 2/2 and the Kafka/Alexa inconsistency.

Replace:
> - Check 2 (Linear): a clause that promises a later explanation ("which matters a little further on") is Borderline even when nothing yet depends on it.

With:
> - Check 2 (Linear): a clause that hangs a promise on a term or detail ("which matters a little further on", "which is what the next idea handles") is Borderline even when nothing yet depends on it. A sentence at the end of a section that says what comes next, in order, passes.

Edit 3 (tests/pattern.grade/inputs.md, harness). Targets 3/4.

Replace:
> then any limit tests/pattern.explain/inputs.md sets for this output, named by topic rather than by number (for example, "1,700 words for this piece", only for Docker).

With:
> then any limit tests/pattern.explain/inputs.md sets for this output, named by topic rather than by number, with the reference's verdict rule for it kept word for word (for Docker: "Limit for this piece: 1,700 words (check 4). Under the 2,200 ceiling but over 1,700 is Borderline; over 2,200 is Fail.").

Edit 4 (conventions.md, check 10 bullet). Targets 4/10 and 5/10.

Replace:
> - Check 10 (Clean output) includes text that copies the prompt's reasoning to the reader or refers to the writer's material ("the material I was given", "the source you were given").

With:
> - Check 10 (Clean output) includes text that copies the prompt's reasoning to the reader or refers to the writer's material ("the material I was given", "the source you were given"). Such phrases inside the body are Borderline. A preamble line, a visible plan or an offer to expand is Fail.

Edit 5 (prompt, plan step 1, patch to 0.3.1). Targets 5/3, missed on both runs.

Replace:
> a claim that contradicts another sentence in the output, or a worked example that breaks a rule the output has just stated, is an error even when each sentence sounds right alone, because the reader trusts the output's own statements most.

With:
> a claim that contradicts another sentence in the output, or a worked example that breaks a rule the output has just stated, is an error even when each sentence sounds right alone, because the reader trusts the output's own statements most. Words such as "the one", "only", "never" and "all" are where this most often happens, so check each against the output's own lists.

Over-correction to watch: Borderlines on ordinary uses of "all" or "only" that are true. Raft's "Only once an entry is committed does Cedar carry it out" is the case to watch.

Also, when the file is next edited: move the "Where the rubric comes with notes ..." paragraph after Not applicable, and change the plan step 1 or check-list wording so the grader never calls the task's domain block "the output's own" (the input 8 slip). One clause is enough: "a fact from the task or source is cited as such, not as the output's".

## Failure log

Mark the existing pending lines in tests/pattern.grade/failures.md:
- Line 4 (check 5 at "##" level): fixed in 0.3.0 (check 5 6/7, plant caught). Residual logged below.
- Line 5 (closest call quoted then passed): fixed in 0.3.0.
- Line 6 (check 10 leaks missed): fixed in 0.3.0 (found on 4 and 5); severity residual logged below.
- Line 7 (accuracy against the output itself): partly fixed in 0.3.0 (Raft, Docker); Alexa residual logged below.
- Line 8 (similes): fixed in 0.3.0.
- Line 9 (one cold section): fixed in 0.3.0 (conventions.md).
- Line 10 (input 7 limit leak): fixed in 0.3.0 (by-topic limits); new harness residual logged below.
- Line 11 (counts): fixed in 0.3.0 (supplied counts, 0% error).
- Line 12 (router watch): did not recur in 0.3.0; close.
- Line 13 (relabels): done in inputs.md.

Lines to add:
- 2026-11-18 | 3, 4, 7 | 2 Agreement (explain check 1) | Reader-known terms marked Borderline though the grader names the reader note ("though this reader knows Linux processes"); "Going further" sub-terms checked on bond but not on Raft; "Rust" in Driftwood's first sentence missed. Scope of check 1 is unwritten | pending (conventions.md, edit 1)
- 2026-11-18 | 3 | 2 Agreement (explain check 5) | Practical tips and a "second trap" that can go without a gap pass, because conventions.md describes deletable passages only as repeats or self-deferrals | pending (conventions.md, edit 1)
- 2026-11-18 | 2, 5 | 2 Agreement (explain check 2) | The check 2 convention covers section-end transitions: Kafka "Before seeing how it does it ..." marked B (reference P), while Alexa "the rest of this piece follows it through" passes | pending (conventions.md, edit 2)
- 2026-11-18 | 3 | 2 Agreement (explain check 4), harness | By-topic rename of the Docker limit dropped "Meeting the first and missing the second is Borderline"; the grader saw a bare 1,700 limit and gave Fail | pending (inputs.md, edit 3)
- 2026-11-18 | 4, 5 | 2 Agreement (explain check 10) | Material-leak phrases now found but given Fail; the reference's "one leak phrase is Borderline" is unwritten, the same mechanism as check 6 in 0.2.0 | pending (conventions.md, edit 4)
- 2026-11-18 | 5 | 2 Agreement (explain check 3) | "the one internal component Amazon has confirmed" passes beside the paragraph's own list of confirmed parts, second run running; the self-consistency rule did not reach a claim against a list | pending (0.3.1 edit 5)
- 2026-11-18 | 8 | 4 Evidence (watch) | Check 3 evidence calls the task's domain block "the output's own domain notes"; the verdict stands on the quoted output line | watch (0.3.1 wording)

## Before the next run

- Apply edits 1 to 4 before any rerun. They change what the grader sees, so a rerun without them cannot separate a prompt fix from a convention fix.
- Run v0.3.0 at n=2 on at least inputs 2, 3 and 6 to measure run-to-run stability before relying on single-run verdicts in explain comparisons. The Kafka/Alexa split on check 2 suggests the verdicts on forward pointers are still unstable.
- Grow the set towards the design's 20 to 50 labelled outputs. The explain v0.4.0 head grading exists now (tests/pattern.explain/runs/v0.4.0/head-grading.md), so its outputs can be added as inputs with their labels.
- Have a person label checks 1 and 2 on at least three inputs. Those are the human-check cells, and check 1 is now the grader's weakest.

Process note: this session had Read, Grep, Glob and Write only, with no shell. I took word counts from inputs.md and the graded_counts blocks and did not recount. I checked quotes by reading each graded output in its filled prompt. I took reference labels from the v0.2.0 agreement table, with the relabels applied, and spot-checked them against the reference files for every cell that disagrees. Nothing outside this file was changed.

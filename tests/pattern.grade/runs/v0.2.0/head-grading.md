# Head grading: built/grade.md v0.2.0 (first test run)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the Sonnet subagents that wrote the grader outputs. Both reference gradings were also written by Opus, but the graded model is Sonnet, so this run is not measuring self-agreement (gate review T1 is met).

Date: 2026-11-18. Stage: grading after the first test run of the Grader.
Read: the design doc, tests/pattern.grade/inputs.md, rubric.md (checks 1 to 9), failures.md (empty), my v0.1.0 gate review, the frozen v0.2.0 prompt, all eight grader outputs (1.md to 8.md), both reference gradings (tests/pattern.explain/runs/v0.3.0/head-grading.md and runs/v0.3.1/head-grading.md), the explain rubric, the seven graded explain outputs, the planted input (inputs/8-the-cloud-planted.md) and its fault list (inputs/8-planted-faults.md), and the Part A and Part C lines of sources/alexa-for-shopping.md.
Not available: the filled prompts each subagent received. They were not saved in the run folder, so what RUBRIC contained for each input is inferred from the grader outputs (see the input 7 finding). Edit 1 asks for them to be saved.
No previous version has outputs (v0.1.0 had a gate review only), so there is no promotion comparison. v0.2.0 becomes the baseline.

Scoring rule for agreement: rubric check 2 counts Borderline against Pass as half a miss. It does not say how to count Borderline against Fail. I count that as half a miss too, as the gate review proposed (T6), and Pass against Fail as a full miss. Not applicable cells are listed but kept out of the main figure, because they are trivially matched and would inflate it.

## Verdict: NOT USABLE yet (status stays draft)

- Raw agreement with the reference on inputs 1 to 7: 89.0% (73.0 of 82 applicable cells, 18 half-misses, no full misses). That is just under the rubric's 90%. Counting the 16 Not applicable cells, all of which match, it is 90.8%.
- Agreement after correcting the reference where I judge the grader right (5 cells) and dropping one harness-caused cell: 92.6% (75.0 of 81).
- False Fail (Fail where the reference gives Pass): 0.
- False Pass (Pass where the reference gives a non-Pass): 9 on inputs 1 to 7, plus 1 planted fault missed on input 8.
- Recall on input 8: 9 of 10 planted faults (90%). Checks 4 and 9 stayed Pass, as they should.

Why not usable, given those figures: the misses are not spread out. Explain check 5 (No padding) has a non-Pass in the reference on inputs 2, 3, 5, 6 and 7 and a planted fault on input 8. The grader passed all six. Three graders say why in their own words: "Each of the five body sections carries something", "every '##' section carries a distinct step", and on the planted fault "it is a paragraph, not a deletable section". A grader that never flags padding would bias every explain version comparison, and the v0.3.1 decision was settled by a single Borderline per input. Check 10 has the same problem on a smaller scale: it missed both prompt-material leaks (inputs 4 and 5). The grader is also kinder than the reference overall (9 false Passes against 7 harsher Borderlines and 2 harsher Fails), and the prompt's own situation section names a false Pass as the error the reader cannot see.

What works: the format is clean on all eight (one line per check in rubric order, verdict last, no preamble). Every quote I checked is verbatim. Not applicable is used exactly where the reference uses it. 11b is matched on all seven reference inputs, and the counting notes were followed ("No paragraph has three or more, so under the counting notes this is not a Fail"). Check 13 is a match on Alexa. The planted faults were found quickly and quoted well. On two cells the grader found real errors the reference missed (below). The gate-review edits did what they were for: no tag collision (pattern.grade check 8 passes everywhere), and the evidence-first lines with a sweep and a closest call make each Pass checkable.

Single most important fix next: get the grader to apply explain check 5 to passages, not just "##" sections. The cause is half in the test set (the reference's passage-level reading is in no note the grader sees) and half in the prompt (the sweep goes "section by section", and the closest call it finds gets passed). Edits 1 and 3 together target it.

## Score table: pattern.grade checks on each grader output

P = Pass, B = Borderline, F = Fail, - = not applicable.

| # | Check | 1 API key | 2 Kafka | 3 Docker | 4 Driftwood | 5 Alexa | 6 Raft | 7 Bond | 8 Cloud planted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Complete | P | P | P | P | P | P | P | P |
| 2 | Agreement | P | B | P | P | F | B | B | P |
| 3 | No false Fail | P | P | P | P | P | P | P | P |
| 4 | Evidence | P | P | P | P | P | P | P | P |
| 5 | Quotes real | P | P | P | P | P | P | P | P |
| 6 | Counts | P | P | P | P | P | P | P | P |
| 7 | Independent | P | P | P | P | P | P | P | P |
| 8 | Clean output | P | P | P | P | P | P | P | P |
| 9 | Recall | - | - | - | - | - | - | - | F |
| | P / B / F | 8 / 0 / 0 | 7 / 1 / 0 | 8 / 0 / 0 | 8 / 0 / 0 | 7 / 0 / 1 | 7 / 1 / 0 | 7 / 1 / 0 | 7 / 0 / 1 |

Totals: 59 Pass, 3 Borderline, 2 Fail, 8 Not applicable, of 72 cells.

### Reasoning, check by check

Check 1, Complete. All eight have 14 lines in rubric order (1 to 10, 11a, 11b, 12, 13), one verdict each, none merged, then a Summary line. Output 3 puts blank lines between verdict lines, which is harmless. Pass on all.

Check 2, Agreement. Per-input agreement on applicable cells, raw and then with the reference corrected where I judge the grader right:
- Input 1: 9.5 of 10 = 95.0%. Pass.
- Input 2: 10.5 of 12 = 87.5% raw, 91.7% corrected (check 6, see below). Below the line on the reference as written and above it on the corrected one, so Borderline. Non-Pass evidence: "5. No padding: ... Nothing could be deleted without a gap. **Pass**" against reference B.
- Input 3: 11 of 12 = 91.7%. Pass.
- Input 4: 10 of 11 = 90.9%. Pass.
- Input 5: 11 of 13 = 84.6% raw, 88.5% corrected. Fail either way. Evidence: check 3 "**Pass**", check 5 "None could be deleted without leaving a gap. **Pass**", check 10 "There is no plan, no preamble and no offer to expand. **Pass**", all against reference B.
- Input 6: 10.5 of 12 = 87.5% raw, 91.7% corrected (check 3). Borderline. Evidence: "5. No padding: no section could be removed without a gap. **Pass**" against reference B.
- Input 7: 10.5 of 12 = 87.5% raw. 90.9% with the harness-caused check 4 cell dropped (see below). Borderline. Evidence: "a light forward pointer that nothing depends on. **Pass**" against reference B.
- Input 8: against the planted labels, 11 of 12 applicable cells agree (91.7% counting the check 5 miss as a full miss). Pass.

Check 3, No false Fail. No grader gave a Fail where the reference has a Pass. The two Fails that differ from the reference (inputs 2 and 5, check 6) are against Borderlines, and I judge the grader right on both. Pass on all.

Check 4, Evidence. Every non-Pass quotes the output, states a count, or names an absence. Examples: input 3 check 4 gives a count; input 2 check 11b names the three terms in each paragraph; input 1 check 8 quotes the simile and names the missing break. The Not applicable lines give reasons. Pass on all.

Check 5, Quotes real. I checked every quoted string against the graded output. All are verbatim, apart from acceptable ellipses and nested-quote changes. Examples: input 6 joins "Shortly after, Dogwood's countdown runs out... becomes leader in term 6" across a semicolon, which is a fair ellipsis. Input 8 writes "'it's in the cloud'" where the output has double quotes inside the sentence. Input 3's "one system package" is in line 7 of the Docker piece. Pass on all.

A related issue that check 5 does not cover: input 5's check 13 evidence cites "each query first passes through a real-time router" as an unconfirmed claim stated as fact. The router is Part A, confirmed ("A real-time router picks which model handles each query", source line 21). The verdict is right on its other two grounds ("Those steps are confirmed by Amazon" and "circulates online"), so I log it as a watch item and do not mark it down.

Check 6, Counts. The rubric says within 5% of `wc -w`, or marked approximate. Every count is marked approximate ("approximate", "estimated", "estimate"), so all eight pass by the letter. Only three are within 5%, though:

| Input | `wc -w` | Grader | Difference |
| --- | --- | --- | --- |
| 1 | 537 | about 535 | -0.4% |
| 2 | 1,914 | about 1,700 | -11.2% |
| 3 | 1,945 | about 2,200 | +13.1% |
| 4 | 545 | about 500 | -8.3% |
| 5 | 1,955 | about 1,950 | -0.3% |
| 6 | 3,484 | about 3,900 | +11.9% |
| 7 | 1,969 | about 2,000 to 2,100 | +1.6% to +6.7% |
| 8 | 1,995 | about 2,100 to 2,200 | +5.3% to +10.3% |

The escape clause is doing all the work. On input 3 the error put the count right on the ceiling ("about 2,200 ... at the edge of the rubric's moderate ceiling of 2,200"), and the real count is 255 under it. On input 8 it told the reader the piece is "close to the limit" when it has 205 words of headroom. A slightly longer output would have drawn a wrong check 4 verdict. This is the risk the gate review left to the run, and the run shows it. Edit 5 gives the grader the `wc -w` figure.

Check 7, Independent. No verdict rests on a fault that belongs only to another check. Some evidence lines mention a neighbouring fault as a nearest miss without letting it set the verdict, for example input 4 check 2 ("Nearest miss is the opening's use of 'job scheduler' before it is defined") on a Pass. Input 8 check 1 cites "SLA and points of presence" from the 11b plant, but an undefined term really does break check 1, so it is not double counting. Pass on all.

Check 8, Clean output. All eight have only verdict lines and a Summary. None has a preamble, rewrite advice or an offer. Gate-review edit 1 (renamed input blocks) worked: no grader followed the explain prompt's own format. Pass on all.

Check 9, Recall (input 8 only). 9 of 10 planted faults got a non-Pass on their own check, and checks 4 and 9 stayed Pass. The miss is check 5: "the nearest miss is the paragraph 'It is worth pausing to repeat this', which restates the previous two paragraphs, but it is a paragraph, not a deletable section. **Pass**". The grader found the plant, said what was wrong with it, and passed it on the rubric's wording. Fail.

## Agreement table, inputs 1 to 7, cell by cell

Each cell is reference / grader. A cell marked x is a disagreement. "-" is not applicable.

| # | Check | 1 API key (v0.3.0 1c) | 2 Kafka (v0.3.0) | 3 Docker (v0.3.1) | 4 Driftwood (v0.3.0) | 5 Alexa (v0.3.0) | 6 Raft (v0.3.1) | 7 Bond (v0.3.1) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P / P | P / P | P / P | B / B | F / F | P / P | P / P |
| 2 | Linear | P / P | P / P | P / P | P / P | P / P | B / B | B / P x |
| 3 | Accurate | P / P | P / P | P / B x | P / P | B / P x | P / B x | P / P |
| 4 | Proportional | P / P | P / P | B / B | P / P | P / P | P / P | P / B x |
| 5 | No padding | P / P | B / P x | B / P x | P / B x | B / P x | B / P x | B / P x |
| 6 | Resumable | - / - | B / F x | P / P | - / - | B / F x | P / P | P / P |
| 7 | Plain text | P / P | P / P | P / P | P / P | P / P | P / P | P / P |
| 8 | Not dumbed down | P / B x | P / B x | P / P | P / P | P / P | P / B x | P / P |
| 9 | Trap handled | P / P | P / P | P / P | P / P | P / P | P / P | P / P |
| 10 | Clean output | P / P | P / P | P / P | B / P x | B / P x | P / P | P / P |
| 11a | Complete | - / - | P / P | P / P | - / - | P / P | P / P | P / P |
| 11b | Unhurried | P / P | F / F | F / F | F / F | F / F | B / B | F / F |
| 12 | Unknown topic | - / - | - / - | - / - | P / P | - / - | - / - | - / - |
| 13 | Source confidence | - / - | - / - | - / - | - / - | F / F | - / - | - / - |
| | Applicable cells | 10 | 12 | 12 | 11 | 13 | 12 | 12 |
| | Misses (half each) | 0.5 | 1.5 | 1.0 | 1.0 | 2.0 | 1.5 | 1.5 |
| | Agreement | 95.0% | 87.5% | 91.7% | 90.9% | 84.6% | 87.5% | 87.5% |

All 18 disagreements are one step apart (P/B or B/F). There are no full misses. 16 Not applicable cells match.

By explain check: 11b 7 of 7, 1 7 of 7, 13 1 of 1 and 12 1 of 1 are exact. Check 5 has 1 of 7 exact, with the grader kinder on 5 and harsher on 1. Check 8 has 4 of 7, check 10 5 of 7, and check 3 4 of 7.

### Who is more likely right, disagreement by disagreement

| Input, check | Ref / grader | More likely right | Why |
| --- | --- | --- | --- |
| 1, 8 | P / B | Reference | The ticket simile is true in the one respect used ("admits whoever carries it"). The grader's break (tickets are single-use) does not touch the point being made. The reference states this convention in its 1c evidence, not in the notes the grader saw. |
| 2, 5 | B / P | Reference | The version passage ("In the classic form of the protocol ... Newer versions of Kafka reduce this") is repeated in "Going further" ("Cooperative rebalancing and the new consumer group protocol"), so it can go. The grader checked only whole sections. |
| 2, 6 | B / F | Grader | "A topic is not one long line" opens a section cold. Under the rubric as written and the prompt's Fail definition ("at least one instance you can quote breaks the pass condition"), that is a Fail. The reference's "one cold section of several is Borderline" is a severity convention that is in no note. |
| 2, 8 | P / B | Reference | "like a bookmark" is exact in the respect used (it marks a place without removing anything). Same convention gap as 1, 8. |
| 3, 3 | P / B | Grader, narrowly | "Each of those steps produces a layer" sits next to "The last line is metadata", so the piece contradicts itself. The v0.3.1 reference says so itself ("the piece contradicts itself slightly") but does not mark it. Under the prompt's Borderline definition, a self-contradiction is disputable at least. |
| 3, 5 | B / P | Reference | The SIGTERM wait, 0.0.0.0, the fork case and the "second trap" are practical tips that fail the body test. The grader saw them (it checks them under accuracy) but judged deletability by section only. |
| 4, 5 | P / B | Grader | The second paragraph repeats the first line's admission and can go without a gap. The v0.3.1 reference marks the same kind of paragraph in the next Driftwood output as check 5 Borderline ("the second paragraph, which repeats the admission already made"). The v0.3.0 label is inconsistent with the reference's own later practice. |
| 4, 10 | B / P | Reference | "the material I was given contains nothing about it" and "from where you are sitting" copy the prompt's reasoning to a reader who was given nothing. That is visible plan. The grader judged only the opening line ("not a preamble"). |
| 5, 3 | B / P | Reference | "It also leaves out the one internal component Amazon has confirmed, the model router" contradicts the same paragraph's own list of confirmed parts. The grader checked claims against general knowledge, not against each other. |
| 5, 5 | B / P | Reference | The customer-service paragraph and the COSMO build detail ("trained on about 30,000 human-annotated instructions") can go. Again, checked by section only. |
| 5, 6 | B / F | Grader | Same as 2, 6: "## Several models and a router" opens cold, and the convention that makes this Borderline is undocumented. |
| 5, 10 | B / P | Reference | "which the source you were given describes" and "the material given here" address the reader as if they had the source pack. The grader did not look for this. |
| 6, 3 | P / B | Grader | This is a real error the reference missed. Ash asks for votes "in term 6", which moves every voter to term 6, so Dogwood's later candidacy would be term 7, but the piece says "becomes leader in term 6". Ash, recovering from term 4 with no news of term 5, would also campaign in term 5. The piece breaks the rule it has just taught ("a server that receives a message carrying a higher term ... updates its number at once"). The reference noted a different consistency slip in this passage (Ash's index 40) and chose not to mark it. Borderline is the right verdict. |
| 6, 5 | B / P | Reference | The current-term commit paragraph defers itself ("worth reading about at a desk") and can go. Checked by section only. |
| 6, 8 | P / B | Toss-up, lean reference | "The term works like a clock that only moves forward:" states its respect after the colon. A clock also advances by itself and a term does not, so the grader has a point, but it is the convention gap again. |
| 7, 2 | B / P | Reference | The grader quoted "which is what the next idea handles" and passed it as "a light forward pointer that nothing depends on". The input 6 grader gave Borderline to the same kind of clause ("which matters a little further on"). The run is inconsistent with itself, and the task bans the clause. |
| 7, 4 | P / B | Reference; harness fault | The grader applied 1,700 words ("over the 1,700 that inputs.md sets for input 7"). That limit belongs to explain input 7, Docker. Grade input 7 is bond duration (explain input 8). The v0.3.1 bullet "Check 4 for input 7: ... inputs.md sets 1,700 for this input" was passed into bond's RUBRIC, and the grader had no way to know the numbering differs. This is not a grader error. |
| 7, 5 | B / P | Reference | "Duration also changes as the yield changes, and it shortens as time passes" can go, and DV01 is given twice (body and "Going further"). Checked by section only. |

Tally: the reference is more likely right on 12 cells (including the toss-up), the grader on 5 (2, 6; 3, 3; 4, 5; 5, 6; 6, 3), and 1 is a harness fault (7, 4).

Reference labels to correct for this test set. Record these in inputs.md as relabels; do not edit the released head gradings:
- Raft (v0.3.1) check 3: P to B, term numbering.
- Docker (v0.3.1) check 3: P to B, "Each of those steps produces a layer" against "The last line is metadata".
- Driftwood (v0.3.0) check 5: P to B, repeated admission, in line with the v0.3.1 practice.
- Kafka and Alexa (v0.3.0) check 6: keep B, but write the convention down (edit 1) so a grader can reach it.

## Input 8: recall against the planted faults

| Check | Planted fault | Grader | Caught |
| --- | --- | --- | --- |
| 1 | "usually behind a load balancer and a CDN" | F, quotes it, adds "SLA and points of presence" | Yes |
| 2 | "though the trick only makes full sense once you meet autoscaling much later on" | F, quotes it | Yes |
| 3 | "closer to two full seconds" (transatlantic round trip) | F, "roughly 80 to 100 milliseconds" | Yes |
| 4 | not planted, should stay Pass | P (count "2,100 to 2,200", wc 1,995) | Yes, but the count is high |
| 5 | "It is worth pausing to repeat this. ..." | P, "it is a paragraph, not a deletable section" | No |
| 6 | "Renting by the minute" restatement removed | F, quotes "Every cloud provider exposes an API..." | Yes |
| 7 | IaaS/PaaS/SaaS table | F, quotes "\| Layer \| You manage \|" | Yes |
| 8 | "its manager, Priya, is watching the clock" | F, quotes it | Yes |
| 9 | not planted, should stay Pass | P | Yes |
| 10 | "Here is the explainer you asked for, written for reading on a Kindle." | F, quotes it | Yes |
| 11a | "live migration quietly moves its virtual machines" in The whole picture | F, quotes it, "the body never explains" | Yes |
| 11b | six providers plus SLA and points of presence in one paragraph | F, counts them | Yes |

Recall 9 of 10. All nine catches are Fails with exact quotes. The one miss is the check 5 pattern seen across inputs 2, 3, 5, 6 and 7. On a plant designed to be found, the grader found it and then reasoned its way to Pass. That makes it a prompt problem as well as a test-set one: the grader has no rule that a closest call it can only excuse on the wording should be Borderline (edit 2).

## Effect of the v0.1.0 gate-review edits

- Edit 1 (renamed input blocks, the task treated as material): worked. No grader copied the explain prompt's format or self-check, and pattern.grade check 8 passes on all eight.
- Edit 2 (evidence before the verdict, sweep and closest call on a Pass): mostly worked. Pass lines are checkable ("swept all 7 body paragraphs ..."). The side effect is that a closest call gets named and then passed (input 7 check 2, input 8 check 5). Edit 2 below closes that.
- Edit 3 (sweep universal checks): worked for terms. 11b and check 1 are exact on all seven inputs, including the deep Raft piece. It did not reach check 5, because the sweep unit is "section by section" (edit 3 below).
- Edit 4 (Borderline means disputable; one quotable breach is Fail): made verdicts stable and literal, which was the goal. It also produced the two check 6 Fails where the reference applied an unwritten severity rule. The rule needs writing down (edit 1). The verdict scale does not need softening.
- Edit 5 (notes ship with the rubric): worked where the notes were specific (11b counting, the Docker 1,700). It also exposed a numbering collision (input 7, bond).

Layout slip, not worth an edit of its own: in `<verdicts>`, the paragraph "Where the rubric comes with notes on how its checks are applied ..." sits between Fail and Not applicable. Move it after Not applicable when the file is next edited.

## Edits for v0.2.1, in order of importance

Edit 1 (test set: tests/pattern.grade/inputs.md plus a new tests/pattern.grade/conventions.md). Write down the reference's unwritten conventions, stop wrong-input notes reaching a grader, and save the filled prompts. Targets: 12 of the 18 disagreements (check 5 on 2, 3, 5, 6, 7; check 6 on 2 and 5; check 8 on 1, 2 and 6; check 10 on 4 and 5) plus the harness fault on input 7.

Replace in inputs.md:
> Each input is one explain output, the frozen prompt that produced it as TASK, the source where there is one, and as RUBRIC the explain rubric followed by the "How I applied the checks" bullets from the reference grading file and any per-input limit from tests/pattern.explain/inputs.md (for example, 1,700 words for input 7 Docker).

With:
> Each input is one explain output, the frozen prompt that produced it as TASK, the source where there is one, and as RUBRIC the explain rubric followed by tests/pattern.grade/conventions.md, then the "How I applied the checks" bullets from the reference grading file with any bullet about a different output removed, then any limit tests/pattern.explain/inputs.md sets for this output, named by topic rather than by number (for example, "1,700 words for this piece", only for Docker). Explain and grade inputs are numbered differently, so a bullet that says "input 7" means Docker and must not reach the bond grader. Save each filled prompt as runs/<version>/<n>-filled.md, so a disagreement can be traced to what the grader saw.

Create conventions.md with:
> These are the conventions the reference gradings apply. Each is part of the pass condition.
> - Check 5 (No padding) applies to any passage, a paragraph or a run of sentences, not only a "##" section. A passage that repeats another passage, including one repeated in "Going further", or that tells the reader it is not needed, can be deleted without a gap. One such passage is Borderline; a whole section of them is Fail.
> - Check 6 (Resumable): one section after the first that opens without a restatement, when the others restate, is Borderline. Two or more is Fail.
> - Check 8 (Not dumbed down): an analogy or simile that is true in the one respect the sentence uses it for passes without a stated break. A named person carried through the running example is Borderline.
> - Check 10 (Clean output) includes text that copies the prompt's reasoning to the reader or refers to the writer's material ("the material I was given", "the source you were given").
> - Check 2 (Linear): a clause that promises a later explanation ("which matters a little further on") is Borderline even when nothing yet depends on it.
> - Check 3 (Accurate) includes the output contradicting itself, or a worked example breaking a rule the output has just stated. One such slip is Borderline.

Add a "Relabels" table to inputs.md listing the three corrections above (Raft 3 to B, Docker 3 to B, Driftwood 5 to B), so agreement is computed against corrected labels.

Over-correction to watch: conventions.md is long and specific to one rubric. Keep it as a test-set file, not in the prompt, because the prompt's job line is "any" rubric.

Edit 2 (prompt, `<output>`). A closest call the grader can only excuse is Borderline, not Pass. Targets: input 8 check 5 (the recall miss), input 7 check 2, and the general lean towards kindness (9 false Passes against 0 false Fails).

Replace:
> For a Pass on a check that applies everywhere, the evidence says what you swept and the closest call you found ("swept all 9 paragraphs; nearest miss is 'shard' in paragraph 4, defined in the same sentence").

With:
> For a Pass on a check that applies everywhere, the evidence says what you swept, the closest call you found, and why it plainly meets the condition ("swept all 9 paragraphs; nearest miss is 'shard' in paragraph 4, defined in the same sentence"). If the only reasons you can give are that the instance is small, or that the condition's wording does not quite reach it, the verdict is Borderline, because the person reading the grade needs to see that instance and decide, and a Pass hides it.

Over-correction to watch: false Borderlines on closest calls that are fine. Input 2 check 2 ("points ahead without depending on it", reference P) is the case to watch. The clause "plainly meets the condition" should keep that one a Pass, because the reason given is about the condition, not about size.

Edit 3 (prompt, plan step 3). Sweep by paragraph, including the closing lists, and judge the fault, not the unit word. Targets: the check 5 misses on 2, 3, 5, 6 and 7, including the duplicates in "Going further" (Kafka's rebalancing, bond's DV01).

Replace:
> When the condition covers the whole output (every term, every paragraph, every section, no sentence), go through it section by section and keep the worst instance you find, because one bad sentence in a long piece is exactly what a quick read misses and a false Pass is the error the reader cannot see.

With:
> When the condition covers the whole output (every term, every paragraph, every section, no sentence), go through it paragraph by paragraph, including any closing list, and keep the worst instance you find, because one bad sentence in a long piece is exactly what a quick read misses and a false Pass is the error the reader cannot see. A condition worded about sections can still be broken by one paragraph inside a section, or by a passage that repeats one elsewhere; weigh that instance against the check's purpose rather than passing it on the wording.

Over-correction to watch: check 5 Borderlines on paragraphs that are short but needed. The reference's test is "could go without a gap". If inputs 1 or 5 (both check 5 Pass in the reference) turn Borderline, tighten the sentence to name deletion without a gap.

Edit 4 (prompt, plan step 1). Test accuracy against the output itself as well as against the world and the source. Targets: input 5 check 3 (the "one internal component" contradiction), and the input 5 check 13 evidence that called a Part A fact unconfirmed. This makes explicit what the Raft and Docker graders already did.

Replace:
> Read the graded_source block, if any, so you can check faithfulness against it rather than against your own knowledge.

With:
> Read the graded_source block, if any, so you can check faithfulness against it rather than against your own knowledge, and before calling a claim unsupported, find where the source places it. For any check on accuracy or faithfulness, also test the output against itself: a claim that contradicts another sentence in the output, or a worked example that breaks a rule the output has just stated, is an error even when each sentence sounds right alone, because the reader trusts the output's own statements most.

Edit 5 (prompt, inputs and plan step 4; harness fills the counts). Give the grader the machine count. Targets: pattern.grade check 6, which passes only through the "approximate" escape. Five of eight counts were 5 to 13% off, and two put the count misleadingly near the ceiling (inputs 3 and 8).

Add to `inputs:`:
> - COUNTS (optional)   # machine counts for the output, such as `wc -w`; the grader uses these instead of counting

Add after the `<graded_output>` block:
> ```
> <graded_counts>
> {COUNTS}
> </graded_counts>
> ```

In plan step 4, replace:
> If you cannot count exactly, say the count is approximate and give the method.

With:
> If the graded_counts block gives a figure, use it and say it is the supplied count, because a machine count is exact and a count made while reading is not. Otherwise, if you cannot count exactly, say the count is approximate and give the method.

In inputs.md, fill COUNTS for each input from the `wc -w` line.

Versioning: edit 5 adds an input, which the design's table calls a new capability with the same output shape. That makes it a minor bump (0.3.0), not a patch. Edits 2 to 4 are wording changes that shift behaviour. Either way, rerun all eight inputs; do not test edits one at a time on a subset.

## Failure log

Lines to add to tests/pattern.grade/failures.md:

- 2026-11-18 | 2, 3, 5, 6, 7, 8 | 2 Agreement, 9 Recall (explain check 5) | The grader reads "No section could be deleted" at "##" level and sweeps section by section. Passages repeated in "Going further", self-deferring paragraphs and the planted "It is worth pausing to repeat this" all pass ("it is a paragraph, not a deletable section"). The reference's passage-level reading is in no note | pending (0.2.1 edits 1, 3)
- 2026-11-18 | 7, 8 | 2 Agreement, 9 Recall | The closest call is quoted and then passed: "a light forward pointer that nothing depends on"; "It is worth pausing to repeat this ... Pass". The Pass-evidence format invites finding the instance and excusing it | pending (0.2.1 edit 2)
- 2026-11-18 | 4, 5 | 2 Agreement (explain check 10) | Prompt-material leaks ("the material I was given", "the source you were given", "the material given here") are not read as visible plan; check 10 judged on the opening line only | pending (0.2.1 edit 1)
- 2026-11-18 | 5 | 2 Agreement (explain check 3) | Accuracy checked against general knowledge, not against the output's own statements: "the one internal component Amazon has confirmed" passed beside the list of confirmed parts | pending (0.2.1 edit 4)
- 2026-11-18 | 1, 2, 6 | 2 Agreement (explain check 8) | "Analogies state where they break" applied to similes that are exact in the respect used (ticket, bookmark, clock). The reference convention is in its evidence, not in the notes | pending (0.2.1 edit 1)
- 2026-11-18 | 2, 5 | 2 Agreement (explain check 6) | One cold section of four gets Fail under the v0.2.0 verdict scale; the reference's "one cold section is Borderline" is undocumented. The grader is right under the rubric as written | pending (0.2.1 edit 1)
- 2026-11-18 | 7 | 2 Agreement (explain check 4), harness | The v0.3.1 note "Check 4 for input 7 ... 1,700" reached the bond grader; explain input 7 is Docker, grade input 7 is bond. The filled prompts were not saved, so this was found only from the grader's wording | pending (0.2.1 edit 1)
- 2026-11-18 | 2, 3, 4, 6, 8 | 6 Counts (passes only through the "approximate" escape) | Word estimates 8 to 13% off `wc -w`; Docker "about 2,200 ... at the edge of the ceiling" against 1,945 | pending (0.2.1 edit 5)
- 2026-11-18 | 5 | 4 Evidence (watch) | Check 13 evidence calls "each query first passes through a real-time router" unconfirmed; Part A line 21 confirms it. The verdict stands on its other grounds | watch (0.2.1 edit 4 touches it)
- 2026-11-18 | 3, 4, 6 | reference labels | The grader found real faults the reference left unmarked: Raft term numbering (check 3), Docker self-contradiction on layers (check 3), Driftwood repeated admission (check 5, which the v0.3.1 reference marks B in the same kind of paragraph) | relabel in inputs.md (0.2.1 edit 1)

## Before the next run

- Apply edit 1 before rerunning. Without it, a v0.2.1 run cannot tell a prompt fix from a convention the grader never saw.
- Rerun all eight inputs on Sonnet again, so the comparison is like for like. Add at least the v0.3.1 Kafka, Raft and bond outputs at n=2, which shows run-to-run stability. Input 6 against input 7 on forward pointers already shows instability.
- Grow the set towards the design's 20 to 50 labelled outputs. Labels already exist for about 18 explain outputs in the two reference files. Add the v0.4.0 outputs once they are graded.
- Do not set `verified_on` yet. When the grader passes, record the model that ran it (Sonnet) and the date, not the head's model.

Process note: this session had Read, Grep, Glob and Write only, with no shell. I took word counts from the `wc -w` line in inputs.md and did not recount. I checked quotes by reading each graded output. Nothing outside this file was changed.

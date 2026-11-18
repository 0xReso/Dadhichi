# Changelog

## 2026-11-15
- built/explain.commuter.it.md 0.1.0 (draft): first Flow-Read Explainer for IT, assembled as one prompt. Not yet tested.
- tests/pattern.explain/: 8 test inputs, 10-check rubric, empty failure log.

## 2026-11-15 (later)
- built/explain.commuter.it.md 0.2.0 (draft): fixes the five v0.1.0 failures. Adds a body test (plan step 5), a fixed word budget with lower ceilings (400/1,500/3,500 typical; 500/2,200/4,500 max), a cut order in the self-check, one-line chapter endings with no end summary, and no forward references. Routes config names and version details to "Going further".
- .claude/agents/dadhichi-head.md: Fable 5.2 head agent that gate-reviews prompt versions and grades test outputs.
- built/explain.commuter.it.md 0.2.1 (draft): applies the head's five gate-review edits (body test anchored on the goal, cut order removes whole ideas, budget examples no longer name test inputs, chapter-closing question exempt from the forward-reference check, rule for late-arriving reasons). Simple-topic budget set to about 450, max 600, everywhere.
- rubric: check 11 "Complete and unhurried" added; check 4 uses the prompt's budgets. Prompt copies are now frozen in each run folder.
- Test run v0.2.1 (6 inputs, graded by the Fable 5.2 head): not promoted. Fixed length and forward references on Kafka and Raft; regressed on input 1 (615 to 1,632 words). Five new failures logged; v0.2.2 edits are drafted in tests/pattern.explain/runs/v0.2.1/head-grading.md.
- Real-use test: Alexa for Shopping article (sources/alexa-for-shopping.md as SOURCE). Head verdict: not publishable as is; 5 must-fix accuracy sentences, all where the writer's inferences read as fact. New failure logged: no rule for mixed-confidence sources.
- articles/alexa-for-shopping/: corrected article (head's must-fix and should-fix edits applied) with 3 SVG flowcharts and an HTML reading view.
- modifiers/figures.md 0.1.0 (draft): optional modifier that lets the explainer add up to three Mermaid flowcharts, prose-complete, phone-sized, dashed for inferred steps. Not yet tested.

## 2026-11-16
- MASTER_PLAN.md: plan for the open-source library. Field research, mental model, ten-step prompt workflow, learnings from the explainer's failure log, catalogue of five packs (core, developer, agent, meta, safety), open-source setup, eight-phase roadmap, six decisions for the owner. Plan only; nothing in it is built.
- README.md: first README. States the early status, how to use the one draft prompt, how prompts get made, and a repository map.

## 2026-11-18
- built/explain.commuter.it.md 0.2.2 (draft): applies the head's v0.2.1 grading edits verbatim (simple-tier criterion and size from the core sentence, size-aware body test, unknown-tool rule, sections for moderate pieces, pace rule in the self-check) and the two source-confidence edits from the Alexa grading. Frozen in tests/pattern.explain/runs/v0.2.2/prompt.md. Not yet gate-reviewed.
- rubric: 11 split into 11a Complete / 11b Unhurried; new checks 12 Unknown topic and 13 Source confidence; check 6 covers any "##" section. inputs: input 7 capped at 1,700 words; Alexa source added as input 9.
- Gate review not run: the head model is out of usage credits.
- Gate review of v0.2.2 (head on Opus, since the usual head model was out of credits): REVISE, 5 edits at the seams (unknown-tool admission in the line under the title, self-check covers sections, reader note shrinks the budget, one set of tier names, say confidence once).
- built/explain.commuter.it.md 0.3.0 (draft): the five gate-review edits applied verbatim; minor bump per the design, since planning logic and output shape changed. Frozen in runs/v0.3.0/prompt.md. Rubric check 6 excludes "The whole picture" and "Going further".
- Test run v0.3.0 started on inputs 1 (x3), 2, 3, 4, 5, 7, 9. Input 6 skipped: RFC 9111 could not be fetched from this session. Input 8 waits for a finance domain block.
- Test run v0.3.0 (9 outputs) graded by the head (on Opus): PROMOTE over v0.2.1, still draft. 60/15/7 vs 55/15/12 on shared cells, no Pass-to-Fail. Fixed: API-key size (3 of 3 samples), unknown tool, Raft log repair, Docker cap. Still failing: 11b pace (names and lists not counted as terms), 13 source confidence on Alexa (invented diagram origin again), cold second sections.
- built/explain.commuter.it.md 0.3.1 (draft): the head's five v0.3.0 edits. failures.md: 8 new lines, 6 pending lines resolved.
- Input 8 (bond duration, finance domain) run on v0.3.0: 1,955 words; not yet graded.
- Test run v0.3.1 (9 outputs + input 8 on both versions) graded by the head (on Opus): NOT PROMOTED, a tie with v0.3.0 (70 Pass each on 94 shared cells; v0.3.1 has fewer Fails). All five edits fixed their targets; offset by new forward pointers, Docker growth (~1,940) and a named character. Input 8: the pattern generalises to finance; IT wording in the pattern sections noted for the split.
- built/explain.commuter.it.md 0.4.0 (draft): 0.3.1 plus the head's five edits (one foundation per paragraph in plan step 4, named forward-pointer clauses, a reader note lowers the ceiling, keep source scope words and mark joins, "you" instead of a named person). Released version stays 0.3.0.
- domains/finance.md 0.1.1: Advice paragraph rewritten as field knowledge.
- built/grade.md 0.1.0 (draft): grader prompt (meta pack). tests/pattern.grade/: 8 inputs scored against the head's existing verdicts, 8-check rubric.
- Grader gate review (head on Opus): REVISE, 5 edits. built/grade.md 0.2.0 applies them: input blocks renamed graded_* and marked as material, not instructions; evidence before verdict; sweep the whole output for checks that cover all of it; Borderline means disputable, Fail means a quotable breach; verdicts block moved before the plan. Test set: rubric notes and per-input limits ship with each input, wc -w counts recorded, planted-fault input written (10 faults on the cloud piece), check 9 Recall added.
- Grading of the v0.4.0 explainer run stopped part way: the Opus subagents hit the usage limit (resets 15:00 UTC). Outputs are all saved in runs/v0.4.0 and runs/v0.4.0-finance.
- Test run v0.4.0 (13 outputs, two samples on 2, 3, 7, 8, 9) graded by the head (on Opus): PROMOTE, NOT TESTED. 76/13/5 vs 69/17/8 for v0.3.0 on 94 shared cells (worse-sample rule). Check 2 passes 13 of 13; no named characters; Docker within cap. Remaining Fails: 11b where a foundation's named parts are defined in one sentence, commands and diagram layers not counted as terms, "the one ... confirmed" exclusivity (four runs), one structural join on check 13.
- Released explainer is now 0.4.0. built/explain.commuter.it.md 0.4.1 (draft, patch): the head's five v0.4.0 edits. failures.md: 8 lines updated, 6 added.
- Input 6 now uses the design doc as its long source in place of RFC 9111, which this environment cannot fetch.
- Grader v0.2.0 test run (8 inputs on Sonnet) graded by the head: NOT USABLE yet. 89.0% agreement (92.6% on corrected labels), 0 false Fails, 9 false Passes, recall 9/10. Lenient on padding (reads "section" literally) and misses prompt-material leaks. Found three real faults the reference had missed (Raft term number, Docker self-contradiction, Driftwood repeat).
- built/grade.md 0.3.0: Borderline when a closest call can only be excused; sweep paragraph by paragraph; test accuracy against the output itself; optional COUNTS input. Test set: conventions.md, relabel table, filled prompts saved, notes filtered by output. failures.md: 10 lines.
- built/rubric.md 0.1.0 (draft): rubric writer (meta pack). tests/pattern.rubric/: 6 inputs (explain as the known-answer case, code review, cover letter, SQL, a vague job, patient dosing), 9-check rubric.
- Grader v0.3.0 test run (8 inputs on claude-sonnet-5-5) graded by the head: USABLE. 94.5% agreement (77.5/82 cells, relabels applied), 0 false Fails, 3 false Passes, 10/10 recall on planted faults, all quotes verbatim, counts exact. built/grade.md is now status tested, the library's first. README gains a scorecard table. Four non-blocking test-set edits and one prompt patch noted for 0.3.1.

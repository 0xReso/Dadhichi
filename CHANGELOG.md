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

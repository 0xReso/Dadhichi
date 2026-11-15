# Dadhichi backlog

The unattended loop works through this list top to bottom, one round at a time.
Edit it freely: reorder, add, delete. The loop always takes the first item that is not ticked.
Mark an item `[~]` to make the loop skip it.

Each "build pattern X" item means the full cycle, done over several rounds:
1. Write `patterns/<x>.md` (or a built prompt) following the design doc's seven-section shape.
2. Write `tests/pattern.<x>/inputs.md` (6–10 stressing inputs, one from a second domain, one trivial, one with a source), `rubric.md` (yes/no checks with numbers where possible), and an empty `failures.md`.
3. Head gate review (dadhichi-head) → apply its edits.
4. Test run: each input written by a fresh general-purpose subagent with no context; freeze `prompt.md` in the run folder.
5. Head grading → log failures → next version, until the head says promote or three versions have run.

## Stage 1 — finish the explainer

- [ ] Explain v0.2.2: apply the five edits in `tests/pattern.explain/runs/v0.2.1/head-grading.md` and the two mixed-confidence edits in `tests/pattern.explain/runs/v0.2.1-alexa/head-grading.md`; split rubric check 11 into 11a/11b; add the unknown-tool check; give input 7 a length number.
- [ ] Explain v0.2.2: head gate review, then test run on inputs 1 (three times), 2, 3, 4, 6, 8, plus the Alexa source.
- [ ] Explain v0.2.2: head grading, promotion decision, failure log updated. Repeat with v0.2.3 if not promoted.
- [ ] Figures modifier: test `modifiers/figures.md` with the explainer on inputs 2, 3 and Alexa; head grades the four figure checks.

## Stage 2 — prove composition (design doc roadmap step 2)

- [ ] Split the promoted explainer into `kernel.md`, `patterns/explain.md`, `readers/commuter.md`, `domains/it.md`; check the reassembled prompt is word-for-word the promoted one.
- [ ] Add `domains/finance.md`; run explain/commuter/finance on 4 finance inputs without touching the pattern.
- [ ] Add `readers/executive.md` (two minutes, decision first); run explain/executive/it on 4 inputs.
- [ ] Add `readers/practitioner.md` and `readers/beginner.md`; one test run each.

## Stage 3 — widen by need (most-used patterns first)

- [ ] Build pattern: review (judge a work against criteria and say what to fix; test on code, essay, resume, README).
- [ ] Build pattern: digest (compress a long source for a reader; test on a paper, an RFC, a contract, a long thread).
- [ ] Build pattern: compare (weigh named options on shared criteria; test on databases, job offers, LLM providers).
- [ ] Build pattern: draft (writing sent under the user's name; test on email, proposal, X post, cover letter).
- [ ] Build pattern: readme (a README for a repo from its files; test on 4 real or sample repos).
- [ ] Build pattern: research (question → sourced findings with confidence levels; reuse the mixed-confidence rule).
- [ ] Build pattern: diagnose.
- [ ] Build pattern: plan.
- [ ] Build pattern: teach.
- [ ] Build pattern: rewrite.
- [ ] Build pattern: extract.
- [ ] Build pattern: ideate.

## Stage 4 — the engine

- [ ] Write `engine.md` from design doc section 6; feed it 10 rough requests and have the head compare its prompts with the library's hand-built ones.
- [ ] Write `scripts/grade.py`-style instructions so a full test run + grading can happen in one round (roadmap step 5).

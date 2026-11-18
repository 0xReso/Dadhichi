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

- [x] Explain v0.2.2: apply the five edits in `tests/pattern.explain/runs/v0.2.1/head-grading.md` and the two mixed-confidence edits in `tests/pattern.explain/runs/v0.2.1-alexa/head-grading.md`; split rubric check 11 into 11a/11b; add the unknown-tool check; give input 7 a length number.
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

## Stage 3a — meta pack (MASTER_PLAN 6.4; build before the developer pack because it speeds up everything after)

- [ ] Build pattern: grader (apply a rubric to one output: reason, quote, verdict per check). Test: grade 30 existing explain outputs and compare with the head's verdicts in the run folders; target 90% agreement per check.
- [ ] Build pattern: rubric writer (job + inputs in, yes/no checks out, split into code checks and grader checks, numbers where possible). Test on 4 jobs: explain, code review, cover letter, SQL helper.
- [ ] Build pattern: test input writer (job in, 6–10 stress inputs covering trivial, hard, vague, unknown, second-domain, with-source). Test on the same 4 jobs.
- [ ] Build pattern: cold reader (prompt in, everything a reader with no context would have to guess, ranked). Test on 4 prompts with known gaps: explain v0.2.0 and v0.3.0, plus two deliberately broken ones.

## Stage 4 — the engine

- [ ] Write `engine.md` from design doc section 6; feed it 10 rough requests and have the head compare its prompts with the library's hand-built ones.
- [ ] Write `scripts/grade.py`-style instructions so a full test run + grading can happen in one round (roadmap step 5).

## Stage 5 — developer and agent packs (MASTER_PLAN 6.2, 6.3, build order 6.6)

- [ ] Code review (review / practitioner / code): real defects in a diff, ranked, each with a failing scenario; no style noise. Test on 6 diffs with planted bugs.
- [ ] Bug diagnosis (diagnose / practitioner / code): symptoms and logs to ranked causes, each with the cheapest confirming check.
- [ ] Commit message and PR description (draft / reviewer / code).
- [ ] README writer (draft / first-time visitor / code).
- [ ] Project context file: AGENTS.md / CLAUDE.md from a repo.
- [ ] Skill author: a repeated procedure into an Agent Skill whose description triggers at the right time.
- [ ] Subagent brief: goal, what is known, what done looks like, what to return.

## Stage 6 — open up (MASTER_PLAN 7.6)

- [ ] Scorecard generator: one table per built prompt from its run folders.
- [ ] CONTRIBUTING.md, issue templates (failure report, tool request, model result), licence once the owner decides.

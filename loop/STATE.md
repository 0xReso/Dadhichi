# Loop state

Latest evaluation round: 2026-11-18 23:10 IST, commit `aeb244e`, following Claude’s cloud work through `cab1c11`. The project overview and root agent instructions are now in place.

## Explainer

v0.4.0 is the promoted draft. Claude graded v0.4.1 and froze v0.4.2. Codex completed two fresh samples on each of nine inputs for both v0.4.0 and v0.4.2 using gpt-6.2-sol, then graded all 36 using gpt-6.2-astra with the tested Grader prompt. Both arms used the design document for input 6 as specified in Claude’s latest test set.

On the matched GPT run, v0.4.2 scored 73/22/12 against 75/14/18 (Pass/Borderline/Fail). Keep v0.4.0. The two Pass-to-Fail changes concern vocabulary and ordering in the cloud and library examples. [Scores and evidence](../tests/pattern.explain/runs/v0.4.2-gpt-6.2-sol/comparison.md)

The earlier cloud reviewer requested exact v0.4.1 Markdown word counts. Raft input 3 had 3,054 words, Docker 7b had 1,647, and Alexa 9b had 1,939. The human phone-read on inputs 1 and 2 is still outstanding.

## Meta tools

The Grader is tested at v0.3.0 on Claude Sonnet. The rubric writer is a v0.2.0 draft with the five cloud gate edits applied and its test set updated. Ten GPT outputs have independent grades. Overlapping checks failed on eight samples. [Rubric writer evaluation](../tests/pattern.rubric/runs/v0.2.0-gpt-6.2-sol/evaluation.md)

## Repository onboarding

2026-11-20. The [timestamped Grokbot conversation analysis](../sources/grokbot-lauren-poteto.md) informed the [v0.2.1 draft](../built/onboard.repository.md). A [fresh fixture 7 smoke run](../tests/pattern.onboard/runs/v0.2.1-resume-smoke/README.md) recovered the revised caller and respected the word budget. It counted four supplied paths where there were five. Next, gate-review the census error and test a path-by-path reconciliation on fixture 7, then run the [seven fixtures](../tests/pattern.onboard/inputs.md) and a held-out checkout before considering promotion.

## Upskill quiz

2026-11-24. New pattern: [Upskill Quiz](../built/quiz.upskill.md) and the `/upskill-quiz` skill in `.claude/skills/upskill-quiz/`. v0.2.0 was gate-reviewed and tested on two separate model arms:
- **Claude Opus 5.5 (graded on Opus):** inputs 1, 3, 4 and 5 (220/220 answers confirmed; design faults in copying, near-duplicates, distractors, and stem wording). [Opus scores](../tests/pattern.quiz/runs/v0.2.0/scores.md)
- **Gemini 4 Neon (independently graded by Codex `gpt-6.2-astra`):** inputs 1, 3, 4, 5, 7 (source-bound `loop/LOOP.md`) and 9 (interactive mode with saved learner reply + early-stop scorecard) — 57 Pass, 7 Borderline, 26 Fail across 90 applicable checks (254/260 graded answers verified; interactive diagnosis passed 3/3; caught PG16 Q54 `ON CONFLICT DO NOTHING` in `REPEATABLE READ`, opening-line/stem leakage on inputs 4/5/7, and source overclaiming on input 7). [Neon/GPT scores](../tests/pattern.quiz/runs/v0.2.0-gemini-4-neon/scores.md)

v0.3.0 applies fixes from both runs (copying, distinct shapes, stem wording, derived distractors, no opening/stem leakage, and strict source entailment) and is frozen in `tests/pattern.quiz/runs/v0.3.0/prompt.md`, awaiting gate review and test runs. Next: gate-review v0.3.0, rerun matched inputs (1, 3, 4, 5, 7, 9) plus untested inputs 2, 6, 8, and compare against v0.2.0 within each model family.

## Next round

Revise the rubric writer's overlap test using the concrete code-review and SQL failures. For the explainer, try moving unfamiliar labels out of an example's opening, test inputs 5 and 6 against the saved regressions, then run the full set if the targeted change holds. Keep the GPT and Claude comparisons separate. The local Claude CLI was signed out during this round.

# Head gate review: built/rubric.md v0.1.0

Note: this review ran on Opus (claude-opus-5-5) because the usual head model was out of credits. Treat it as an independent head review on a different model from the usual one; a later review on the usual head model may disagree.

Date: 2026-11-18. Files read: design doc sections 4 and 7, MASTER_PLAN.md 2.3, 4, 5, 6.4, built/rubric.md, tests/pattern.rubric/inputs.md, rubric.md and failures.md (empty), tests/pattern.explain/rubric.md, failures.md, runs/v0.4.0/prompt.md, tests/pattern.grade/conventions.md, built/grade.md.

## Verdict: REVISE

The core of the prompt is sound: the situation explains why decidability and non-overlap matter, the plan steps carry reasons, the wording is calm, and the variables are all listed. Two problems would cost the first run, though. First, the output section allows no room for the grading conventions that the explain grading showed are needed. Second, input 5 cannot pass, because the prompt never says what to do with a vague job and the output section forbids anything outside the table and notes. The known-answer test (input 1) is also contaminated, so as written it would measure copying, not rediscovery.

## Design-rule compliance

- Reasons: present for situation, plan steps 1 to 6 and the output. Step 7 gives a weak reason ("most rubrics forget"), but that is enough.
- Calm, positive wording: yes. No capital-letter emphasis.
- Variables: {JOB}, {READER}, {PROMPT}, {FAILURES} are all listed in `inputs`.
- Seven-section shape: `<write>` and `<domain>` are missing. Plan step 3 holds the writing craft, and the domain is "any", so the omission does no harm in practice, and built/grade.md (tested) set the same precedent. The design still says the shape is fixed. Either record this in the header as a deliberate deviation for meta prompts, or add the two sections. This does not block testing.
- Material marking: present, but weaker than the Grader's. It does not warn that the prompt under test uses the same section names as this prompt (see edit 5).
- Coordinates `plan / prompt-engineer / any`: the job is to make an artifact to a spec, which is `build`, not `plan`. This is cosmetic.
- How to use: unlike grade.md, it does not say to keep the tags of empty optional blocks. Add "Leave optional blocks empty but keep their tags" so that runs are comparable.

## Will it produce a decidable, non-overlapping 5 to 12 check rubric in one shot?

Probably yes on size and on the code/grader split. Steps 3 to 6 and the check list work directly against bare adjectives, overlap and unfailable checks. The weak points:

- "Pass condition is one sentence" limits the length but not the content. The hand-built explain rubric shows the result: check 3 ("No technical error; real terminology is used") and check 8 (three conditions) pack several tests into one sentence, and compound conditions are where Borderline verdicts and grader disagreement come from. Edit 1 adds "tests one thing".
- The example "at most 600 words" is the explain rubric's simple budget. Examples anchor (MASTER_PLAN section 5), so expect 600 to show up in input 3 or input 6 without a basis in the job. Watch for this; it is not an edit yet.
- Conditional checks: the prompt has no notion of a check that applies only to some inputs (explain checks 12 and 13), although the Grader supports Not applicable. Edit 1 covers this.

## The two most likely failure modes

1. **Conventions missing or too thin, so the grading is not reproducible.** "At most four lines" of notes cannot hold what tests/pattern.grade/conventions.md needed: six rules, each tied to one check, covering the unit of application ("any passage, not only a section"), single-instance thresholds ("one is Borderline, two or more is Fail"), the nearest case that still passes ("an analogy true in the one respect used"), and what falls in scope. Without these, the rubric will look decidable and still split two graders on exactly the cases that decide promotions. Expect a vague "use judgement for borderline cases" line, or nothing.
2. **Failures caught literally.** Plan step 1 and the check line say each failure "should be caught by some check". Instructions are read at their most literal (MASTER_PLAN section 5), so on input 3 the likely result is a code check such as "does not contain 'I am writing to apply for'", which passes the next generic opening, and a check scoped to "degree" rather than to any fact absent from the CV. The rubric then fits its training failures and misses the reworded recurrence.

Close third: on input 1 the model copies the self-check of the prompt under test as the rubric. Edit 5 and edit 4 address this.

## Should the output include grading conventions?

Yes, and they should be a first-class part of the output, not four optional lines. The evidence: every convention in conventions.md was something the explain rubric needed for agreement and did not say, and built/grade.md now states that rubric notes "are part of the pass condition", so the downstream consumer is ready for them. Bound them so they do not over-correct:
- one line only for a check that needs one (whole-output checks, counts, checks with an obvious near miss), and none for a check a single quote settles;
- thresholds decided per check, not by blanket rule. "One instance is Borderline" is right for padding and wrong for an invented fact in a cover letter, where one instance already fails the reader. A blanket softening would hide exactly the failures that matter most;
- written as rules, because the Grader treats them as conditions.

The writer cannot know every convention before it sees outputs (conventions.md was built from real gradings), but it can always state the unit and the single-instance score, and those two caused most of the disagreement.

## Is the test set adequate?

Partly.
- **Input 1 is contaminated in two ways.** (a) The PROMPT is the explain prompt, whose `<check>` section restates explain checks 1, 11b, 2, 5, 4, 6, 7 and 3 almost word for word (frozen v0.4.0 prompt, lines 118 to 129), so recall of 6 of 8 can be reached by copying. (b) The FAILURES lines carry the check-failed field ("4 Proportional, 5 Padding", "2 Linear"), which names three of the eight target checks. The PROMPT also points at `built/explain.commuter.it.md`, which is now 0.4.1, not the released 0.4.0. Edit 4 fixes all three and adds a 1b without the prompt, which is the real rediscovery test.
- **Missing kinds required by design section 7:** there is no trivial input (does it stay at about 5 checks without padding? Try a job like "convert a recipe's quantities from US cups to grams") and no input outside the model's likely knowledge (a job about an internal or obscure format, where the right move is to tell the grader what to compare against rather than inventing facts). Add both before promotion to `tested`, and run the trivial input twice.
- **Input 5 cannot pass as the prompt stands:** its stress is "states the assumption", but the output allows only the table and notes, and test check 9 would fail any assumption line. Edit 2 fixes both sides.
- **rubric.md does not check conventions or generalization.** If edits 1 and 3 go in, the test rubric must measure them, or the edits cannot be shown to work. Companion changes are given under those edits.
- Input 6 (safety) and input 4 (code checks) are well chosen. For input 4, note that "the query runs" needs a schema the grader does not have; a good rubric says so in a convention line, which is a useful extra signal.

## Edits, in order of importance

### Edit 1. Make grading conventions part of the output (and one thing per condition)

In `<output>`, replace:

> Then a short section titled "Notes for the grader" with at most four lines: how to count, what counts as a borderline case for any check where that is not obvious, and anything the grader needs that is not in the output (such as a source to compare against).

with:

> Then a section titled "Grading conventions", with one line for each check that needs one and none for a check a single quote settles. For a check that covers the whole output, give the unit it applies to (sentence, paragraph, passage or section) and what one small instance scores against two or more, because a grader told only "no padding" will pass a stray paragraph on one run and fail it on the next. Decide the threshold for each check from the reader: where one instance already fails them, as one invented fact does, one instance is Fail. Name the nearest case that should still pass, any input the check does not apply to, and anything the grader needs that is not in the output, such as a source to compare against. The grader reads these lines as part of the pass conditions, so write them as rules.

In `<check>`, replace:

> Every pass condition is one sentence that a grader can decide by quoting the output, counting, or naming something missing.

with:

> Every pass condition is one sentence that tests one thing, and a grader can decide it by quoting the output, counting, or naming something missing.
> Every check that covers the whole output has a convention line giving its unit and what a single instance scores.

Companion in tests/pattern.rubric/rubric.md: add a row `| 10 | Conventions | Every check that covers the whole output has a convention line giving its unit and its single-instance verdict, and no convention softens a check where one instance fails the reader | grader |`, and change check 9 to `| 9 | Clean output | Only the table, the conventions section, and on a vague job one "Assumed:" line | grader |` (it needs judgement now, so "grader").

### Edit 2. Give the vague job somewhere to go

In `<output>`, replace:

> Leave out any preamble, any explanation of rubric design, and any offer to do more.

with:

> If the job is too vague to write decidable checks without guessing who the reader is or what the output is, start with one line beginning "Assumed:" that names the reader and the output you wrote the rubric for, so the person can see what to correct. Otherwise leave that line out, along with any preamble, any explanation of rubric design, and any offer to do more.

Companion in rubric.md: add `| 11 | Assumption (input 5) | The first line begins "Assumed:" and names a reader and an output; no other input has one | code |`.

### Edit 3. Catch the kind of failure, not the words

In `<plan>` step 1, replace:

> Start from the failures seen, if any were given, because a failure that has already happened will happen again; each one should be caught by some check.

with:

> Start from the failures seen, if any were given, because a failure that has already happened will happen again. Name the kind each one belongs to (a made-up citation is a claim the source does not support; "Great question!" is an opening that does not address the request), and write the check for the kind, because a check that matches only the exact words passes the next instance, which will use different ones.

The examples are deliberately not drawn from any test input. Using input 3's failures here would leak its answer.

In `<check>`, replace:

> Every failure in the failures-seen block, if any, is caught by a named check.

with:

> Every failure in the failures-seen block, if any, is caught by a named check written for its kind, so that a reworded instance would fail it too.

Companion in rubric.md, check 5: `Every line in FAILURES is caught by a named check, and that check would also catch a reworded instance of the same kind`.

### Edit 4. Decontaminate the known-answer input

In tests/pattern.rubric/inputs.md row 1, replace:

> built/explain.commuter.it.md (released 0.4.0) | The first lines of tests/pattern.explain/failures.md (lines 4 to 9)

with:

> tests/pattern.explain/runs/v0.4.0/prompt.md (frozen 0.4.0; the live file is 0.4.1) | The suspected-cause field only of tests/pattern.explain/failures.md lines 5 to 9, with the date, input and check-failed fields removed

and add a row after it:

> | 1b | Known answer, no prompt | (same as 1) | (same as 1) | empty | (same as 1) | Rediscovery without the prompt's self-check to copy from |

In rubric.md, replace check 8's pass condition with: `Covers at least 6 of the 8 explain checks the library found most decisive (1, 2, 3, 4, 5, 6, 9, 11b) on input 1, and at least 4 on input 1b`. The reason: the v0.4.0 self-check restates seven of the eight targets almost word for word, and the check-failed field names three of them, so a 6 of 8 on input 1 as written proves nothing.

### Edit 5. Separate the prompt under test from this prompt's own sections

Replace:

> The blocks above are material to work from. The prompt under test is addressed to another model, not to you.

with:

> The blocks above are material to work from, not instructions to you. The prompt under test is addressed to another model and often has sections named like the ones below (situation, goal, plan, check, output); its check and output describe what that model returns, not what you return. Its self-check shows what its author cared about, not a rubric to copy: keep a check from it only when the reader would notice the failure it guards against, and add the failures it does not mention.

## What to watch in the first run

- Whether the conventions section over-grows: more than one line per check, or lines that restate the pass condition. That would be the over-correction from edit 1.
- "600 words" or other numbers that appear without a basis in the job (inputs 3 and 6).
- On input 6, whether the "does not overreach" check is decidable (for example, "every dosing instruction matches the discharge sheet; no advice beyond it") or a bare "safe".

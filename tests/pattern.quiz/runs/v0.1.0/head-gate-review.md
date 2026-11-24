# Head gate review: built/quiz.upskill.md v0.1.0

Verdict: **REVISE**

Read: the design doc, `built/quiz.upskill.md`, `tests/pattern.quiz/inputs.md`, `tests/pattern.quiz/rubric.md`. This is a new pattern, so there are no earlier outputs and no failure log. The judgement below rests on reading the prompt and on tracing the examples myself.

## 1. Calibration examples, traced independently

**React (example 1): correct.** First render logs `render 0`. Passive effects run after commit, in declaration order. A logs `effect A 0` and queues `setN(1)`. B logs `effect B 0` because it still sees the render-0 closure, and the queued update has not rendered yet. Then the re-render logs `render 1`. A is skipped (`[]`) and B re-runs (`n` changed): `effect B 1`. Five lines, matching the stated answer. With StrictMode off there is no double invocation. Non-blocking: the stated trap (effects before `render 0`) is real but shallow. This snippet's stronger trap is believing `setN` re-renders immediately, which predicts `render 1` between `effect A 0` and `effect B 0`. It is the user's own model question, so I am not requiring a change.

**Bonds (example 2): correct.** With annual compounding, A is 100/1.05^10 = 61.39 at 5% and 100/1.06^10 = 55.84 at 6%, a fall of 9.04%. B is at par (100) at 5%. At 6% it is 5 x 7.3601 + 55.84 = 92.64, a fall of 7.36%. A falls further. The trace is sound but never computes anything, even though plan step 7 asks for "compute the numbers". The example also is not multiple choice (see edit 4).

**Python (example 3): correct.** The default list is created once at `def`. `add(1)` returns L = [1]. `add(2)` mutates the same L to [1, 2]. `print` shows `[1, 2] [1, 2] True`.

All three answers are right, and all three fall within 60 to 150 words.

## 2. Keeping a 100-question key correct

This is the prompt's main weakness. Plan step 7 asks the model to "solve it yourself from scratch before writing its answer" inside a plan that is done "silently". A model without a large hidden reasoning budget cannot silently trace 100 code or concurrency questions. In practice, the only real trace is the visible **Why**. The answer format puts **Answer** before **Why**, so the model commits to an outcome first and then writes a trace that defends it. That is the order most likely to produce a confident wrong key. It is worst in sheet mode, where the key is written long after the questions, possibly in a later reply.

The fix is to make the visible trace the self-solve: Why first, worked from the question as written, then Answer as its result (edit 1). Learners lose nothing. They have already committed to their own answer before opening the key, and the Answer line is still labelled for quick marking.

Interactive mode has a second risk. The model marks the learner's reply, and it may drift towards agreeing with a confident wrong reply. Edit 3 makes it trace before comparing.

## 3. Interactive versus sheet

Most of this is clear. Three problems:

- The opening gives "a numbered list of the mechanisms with the question numbers that test each". That tells the learner which rule each question turns on before they attempt it, which contradicts "no stem or comment gives the answer away" in both modes. At high depth, 25 to 35 mechanisms also do not fit in "three lines" (edit 2).
- The interactive review part adds questions, but the check list requires "The running count matches DEPTH exactly". The prompt does not say how review questions are numbered (edit 3).
- Sheet mode's file branch says "the opening three lines", which edit 2 changes. Update it in step.

## 4. Rubric

- Check 3 has a scoring bug: "Zero or one ambiguous question is Borderline", so a perfect output can only score Borderline.
- Checks 3 and 4 double-count. One answer that depends on an unstated setting fails both.
- Check 7 does not state a Pass condition. It is unclear whether Pass means zero generic traps.
- Check 9 assumes the mechanism map sits in the opening. It must follow edit 2.
- Check 2 is the most important check and the hardest to audit across 100 answers. Ask the grader for a per-question line so a skipped trace is visible.

All of these are in edit 5. Checks 14 and 15 are input-specific but testable. Check 8's word-count band is laborious at 100 answers but still testable.

## 5. Design rules

All seven sections are present and in order. Inputs come before instructions. Wording is calm, with no capital-letter emphasis. Most constraints carry their reason. The "What to leave out" paragraph is phrased negatively but gives reasons, which is acceptable. The domain section names fields, which is acceptable for a `built` file. The prompt asks for four-option multiple choice with belief-mapped distractors, and rubric check 10 grades this, but none of the three examples shows it. Examples are the strongest lever in the design doc, so the most precisely graded form should not be the one left unillustrated.

## Edits, in order of importance

### Edit 1: write the trace before the answer, so the stated outcome comes from the trace

In `<plan>`, replace:

> 7. Write each question, then solve it yourself from scratch before writing its answer. Trace it step by step: execute the code line by line, compute the numbers, follow the events in order. If your trace reaches a different answer than you intended, fix the question or the answer. If two answers are defensible, change the question until only one is.

with:

> 7. Write each question so that it can be traced to one outcome: code you can execute line by line, numbers you can compute, events you can put in order. If while drafting you see two defensible answers, change the question until only one remains. The full trace is written out in each answer, as described under The answer, so the stated outcome is the result of the trace rather than a guess the trace has to defend.

In `<write>`, replace:

> **The answer.** Each answer has four parts, about 60 to 150 words in total:
> - **Answer:** the exact outcome, written as it would actually appear.
> - **Why:** the step-by-step trace, numbered when there is an order to follow, naming the mechanism at the step where it acts.

with:

> **The answer.** Each answer has four parts, in this order, about 60 to 150 words in total. The trace comes first because writing it is how you work out the outcome. An outcome stated before its trace is a guess, and across a long set some guesses will be wrong.
> - **Why:** the step-by-step trace, worked fresh from the question as written rather than from what you meant it to test, numbered when there is an order to follow, naming the mechanism at the step where it acts.
> - **Answer:** the exact outcome the trace reached, written as it would actually appear. If the trace reached something other than what you intended, the trace is right: state its result and write the trap to match.

In `<check>`, replace `- You traced every answer yourself, and the trace agrees with the stated answer.` with `- Every Why starts from the question as written and ends at the stated Answer.`

In examples 1 and 3, move the `Answer:` line so that it sits directly after the `Why:` line. Edit 4 gives example 2 in the new order.

### Edit 2: take the mechanism map out of the opening, where it hints at every answer

In `<output>`, replace:

> Open with three lines: the topic and depth with the question count; the assumptions that fix the answers; and a numbered list of the mechanisms with the question numbers that test each. Give no preamble beyond this.

with:

> Open with two lines: the topic and depth with the question count, and the assumptions that fix the answers. Add a third line only to declare an area you do not know reliably. Give no preamble beyond this. Keep the mechanism list out of the opening, because a mechanism named next to its question numbers tells the learner which rule each question turns on before they have tried it. Put the numbered mechanism list, with the question numbers that test each, at the head of the answer key in sheet mode and at the head of the scorecard in interactive mode.

In the same section, replace `reply with only the opening three lines and the two paths` with `reply with only the opening lines and the two paths`.

In `rubric.md` check 9, replace `The mechanism list in the opening maps to question numbers` with `The mechanism list at the head of the answer key (sheet) or scorecard (interactive) maps to question numbers, and the opening contains no such map`.

### Edit 3: interactive marking follows the trace, and review questions sit outside the count

In `<output>`, replace:

> When they reply, mark each answer right or wrong, give the full four-part answer for each question, and for every miss name the wrong belief their answer reveals.

with:

> When they reply, write the full four-part answer for each question, working the trace from the question before you compare it with what they said, then mark their answer right or wrong against the trace. Mark by the trace even when the learner sounds sure or argues, because agreeing with a wrong reply teaches the wrong model. For every miss, name the wrong belief that their particular answer reveals, which may differ from the trap you planned.

Replace:

> then a review part of about one question for every three missed, which re-tests the missed mechanisms in new shapes.

with:

> then a review part of about one question for every three missed, numbered R1, R2 and so on so that it sits outside the DEPTH count, which re-tests the missed mechanisms in new shapes.

### Edit 4: make the bond example multiple choice with belief-mapped options and worked numbers

Replace the whole second `<example>` body (from `Q · Interest rates rise` through the `Rule:` line) with:

> Q · Interest rates rise by one percentage point overnight. Bond A is a 10-year bond that pays nothing until it repays 100 at maturity. Bond B is a 10-year bond that pays 5 at the end of each year and repays 100 at maturity. Both were priced to yield 5% the day before, with annual compounding. Which loses a larger percentage of its price?
> (a) Bond A (b) Bond B (c) Both lose the same percentage (d) Neither loses value, since both still repay 100
>
> Why: 1. A bond's price is each future payment discounted to today at the market rate. 2. Bond A's one payment is worth 100 / 1.05^10 = 61.39 at 5% and 100 / 1.06^10 = 55.84 at 6%, a fall of 9.0%. 3. Bond B is worth 100 at 5%, because its coupon equals the yield, and 92.64 at 6%, a fall of 7.4%. 4. B receives some cash early, and near payments are discounted less. The average time until a bond's cash arrives, weighted by value, is called its duration; A's is longer.
> Answer: (a) Bond A.
> The trap: (c), from believing that equal maturity means equal interest-rate risk. (b) comes from assuming the higher-paying bond is more exposed to rates; (d) confuses the final repayment with today's price.
> Rule: the later a bond's cash arrives on average, the more its price moves when rates move.

(Numbers verified: 61.391 to 55.839 is -9.04%; 100 to 92.640 is -7.36%. The answer is about 140 words.)

### Edit 5: fix rubric scoring so checks are passable and do not double-count

In `rubric.md`, after the sentence ending `not to read the given trace and agree with it.`, add:

> For check 2, record one line per question: number, your own result, the stated result, agree or not.

Replace row 3's pass condition:

> Every question has exactly one defensible answer under the stated assumptions. Zero or one ambiguous question is Borderline; two or more is a Fail.

with:

> Every question has exactly one defensible answer under the stated assumptions. Ambiguity caused by an unstated setting is scored under check 4, not here. Zero ambiguous questions is Pass, one is Borderline, two or more is a Fail.

Replace row 4's pass condition:

> The opening states the version, runtime, mode or convention that each answer depends on. No answer silently depends on an unstated setting.

with:

> The opening states the version, runtime, mode or convention that the answers depend on. One answer that depends on an unstated setting is Borderline; two or more is a Fail.

Replace row 7's pass condition:

> Every answer contains a "trap" that names a specific wrong belief, not a generic "people often get confused." At most 10% of traps are generic for Borderline.

with:

> Every answer's trap names a specific wrong belief, not a generic "people often get confused." Pass: none generic. Borderline: up to 10% generic. Fail: more than 10%.

## Lower-priority notes (not required for this gate)

- Plan step 2 lets the model "restrict the quiz to the parts you know reliably", while step 1 says "hit the number exactly". For input 7 (a source-bound low-depth quiz) this conflict invites either invention or a short count. If input 7 fails check 1 or 14, resolve it by keeping the count exact and testing reliable mechanisms in more shapes.
- Input 9: write the simulated learner's reply after seeing part one, and save it verbatim in the run folder so the run can be repeated.
- Sheet mode at medium and high depth will span several replies. The runner must keep sending "next" until the key is complete and save the full transcript. Otherwise check 1 and check 2 will grade a truncated output.
- Input 3 (PostgreSQL isolation, multi-session) will need a notation for interleaved sessions. If its outputs come out hard to trace, add to `<domain>`: label each session and number every step in global order.

# Grade: quiz.upskill v0.2.0, input 4 (bond prices, medium, sheet)

Grader: head (independent of the builder and the writer). Read: the design doc, `tests/pattern.quiz/rubric.md`, `tests/pattern.quiz/inputs.md`, `tests/pattern.quiz/failures.md` (empty), `runs/v0.1.0/head-gate-review.md`, and the two output files.

**Process problem first.** The brief says the prompt is frozen at `runs/v0.2.0/prompt.md`, but that file does not exist. I graded against `built/quiz.upskill.md` (version 0.2.0), which is identical to `runs/v0.2.0-gemini-4-neon/prompt.md`. The builder must copy it into `runs/v0.2.0/prompt.md` before this run counts as evidence, because a released version is graded against its frozen text, not the working copy.

## Tally

| # | Check | Verdict |
| --- | --- | --- |
| 1 | Count | Pass |
| 2 | Correct | Pass |
| 3 | Determinate | Pass |
| 4 | Assumptions | Borderline (Q46) |
| 5 | Prediction | Pass |
| 6 | No trivia | Pass |
| 7 | Trap named | Pass |
| 8 | Answer shape | Pass |
| 9 | Coverage | Fail (Q17/Q48, Q14/Q36, Q11/Q37) |
| 10 | Distractors | Fail (Q23c, Q33b) |
| 11 | Artifact size | Pass |
| 12 | Progression | Pass |
| 13 | Answers hidden | Pass |
| 14 | Honesty and source | Pass |
| 15 | Diagnosis | N/A (input 9 only) |
| 16 | No copying | Fail (Q8; Q24 noted) |

Pass 11, Borderline 1, Fail 3, N/A 1.

## Check 2: independent solutions

I worked every question from the stem and the stated assumptions before opening `answers.md`. "Mine" is my own computation. "Stated" is the key's answer.

| Q | Mine | Stated | Agree |
| --- | --- | --- | --- |
| 1 | 100/1.1025 = 90.70, (b) | (b) | yes |
| 2 | 94.65, (c) | (c) | yes |
| 3 | savings 6, bond 4 | same | yes |
| 4 | C 108.42 > B 100.00 > A 91.58; B at par | same | yes |
| 5 | YTM about 1.78%, (c) | (c) | yes |
| 6 | 3 yrs left: 108.17, (c) | (c) | yes |
| 7 | A −1.86%, B −12.46%, (b) | (b) | yes |
| 8 | A 76.83→70.56 −8.17%; B 130.89→122.08 −6.73%, (a) | (a) | yes |
| 9 | (9.09+16.53+247.93)/100 = 2.74, (b) | (b) | yes |
| 10 | 5/0.04 = 125, (d) | (d) | yes |
| 11 | on reset at market coupon: 100, (a); fixed 87.36 checks | (a) | yes |
| 12 | 105/1.10 = 95.45; cash 105 | same | yes |
| 13 | 100×(1−0.035) = 96.50, (b) | (b) | yes |
| 14 | 2.83 + 91.67 = 94.50, (b) | (b) | yes |
| 15 | 45.64 (+21.1%) vs 31.18 (−17.3%): gain larger | same | yes |
| 16 | premium so YTM < 3%, (c) | (c) | yes |
| 17 | 5y, coupon 5 at 5.5% = 97.86, 97.9 | 97.9 | yes |
| 18 | X −9.30%, Y −8.65%, (a) | (a) | yes |
| 19 | 5 + 98.17 − 100 = +3.17, (c) | (c) | yes |
| 20 | y ≈ 8.66%, (d) | (d) | yes |
| 21 | 119.48 vs 119.10, (a) | (a) | yes |
| 22 | 86.63, (b) | (b) | yes |
| 23 | +0.96% and +17.29%, (b) | (b) | yes |
| 24 | A 10.00 > B 8.11 > C 7.27 | same | yes |
| 25 | 92 × 1.009 = 92.83, (a) | (a) | yes |
| 26 | perpetuity −16.7%, 30-yr −13.8%, (a) | (a) | yes |
| 27 | coupon 6, price 108.49, (c) | (c) | yes |
| 28 | coupon-2 bond −11.45%, coupon-8 −9.23%, so B pays 2, (b) | (b) | yes |
| 29 | 3.09% → 5.26%, (a) | (a) | yes |
| 30 | 30.83 → 17.41, −43.5%, (b) | (b) | yes |
| 31 | (1.04/1.035)^10 = +4.9%, (b) | (b) | yes |
| 32 | 14.43 yrs at 2%, 11.68 at 8%, (a) | (a) | yes |
| 33 | break-even 4-yr price 95 at y ≈ 6.46%, jump ≈ 1.46 pt, (c) | (c) | yes |
| 34 | 48.08 + 46.23 = 94.30, (c) | (c) | yes |
| 35 | 104/1.07 = 97.20, (b) | (b) | yes |
| 36 | 89.36, (b) | (b) | yes |
| 37 | FRN 100, fixed 113.74, (b) | (b) | yes |
| 38 | A ends at 100 as planned; B 118.73 < 119.10, (b) | (b) | yes |
| 39 | A at 6% prices to 86.40; both 6%, (c) | (c) | yes |
| 40 | B: y ≈ 9.16%, (c) | (c) | yes |
| 41 | A 3.0, B 4.5, (b) | (b) | yes |
| 42 | (1.04/1.05)^3 − 1 = −2.83%, (b) | (b) | yes |
| 43 | zero −12.69%, 50-yr 100 → 90.96 −9.04%, (a) | (a) | yes |
| 44 | 103/1.06 = 97.17, (b) | (b) | yes |
| 45 | X 5+5+94.65 = 104.65, Y 120, (a) | (a) | yes |
| 46 | (a) 61.39, −9.13% if the week is ignored; with a week's accrual 61.45, −9.05% | (a) | yes, see check 4 |
| 47 | X −20.0%, Y −11.1%, (a) | (a) | yes |
| 48 | 5y, coupon 5 at 4.5% = 102.20, (b) | (b) | yes |
| 49 | 5-year zero, (a) | (a) | yes |
| 50 | A (9+114.18)/117.32 = 5.0%, B (1+85.82)/82.68 = 5.0%, (c) | (c) | yes |
| 51 | gov 108.11→100 −7.50%, co 92.64→85.95 −7.22%, (a) | (a) | yes |
| 52 | 8/1.10 × 0.5 = −3.64%, (b) | (b) | yes |
| 53 | 104 × 1.06^9 = 175.71 vs 148.02, (b) | (b) | yes |
| 54 | 100/1.065^3 = 82.79 (82.785), (b) | (b) 82.78 | yes |
| 55 | mod dur 20 × 0.1 = −2.0%, (b) | (b) | yes |
| 56 | 2-yr +4.06, 10-yr −1.80, (a) | (a) | yes |
| 57 | 100.97 + 95.32 = 196.29, (b) | (b) | yes |
| 58 | coupon 5 at 6% for 3 yrs = 97.33, (b) | (b) | yes |
| 59 | (1.05/1.15)^(1/365) − 1 = −0.025%, (b) | (b) | yes |
| 60 | 30-yr −24.8%, zero −9.0%, FRN 0, (a) | (a) | yes |

## Reasoning and verdicts

**1. Count: Pass.** Q1 to Q60 are numbered continuously with none skipped. Medium requires 60.

**2. Correct: Pass.** All 60 agree. I also checked the numbers inside the traces and distractor explanations: Q9(d) 360/130 = 2.77, Q19's post-jump 97.33, Q24's C duration 7.27, Q26's "about 17% of the perpetuity's value" (14.51/83.33), Q32's 14.43 and 11.68, Q43's duration 10.9, Q45's 90.06, Q53's 87.62 and Q57's (c) 203.7. All are right. Two loose phrasings are not false steps. Q33's rule "up to a rise of roughly coupon / remaining duration" holds only roughly, and only because this bond is at par. Q52's "a tenth of the answer" means 0.73 out of 8.

**3. Determinate: Pass.** Every question has one defensible answer under the opening assumptions. Q33's "largest jump that still leaves you exactly even" is awkward, since "largest" and "exactly" pull against each other, but it still has one answer: the break-even jump. Q16 gives no maturity, but the direction is the same at any maturity. Q46 is scored under check 4.

**4. Assumptions: Borderline (Q46).** The opening fixes face value, coupon timing, compounding, no default, instant moves and which yield is meant. Q46 says "A week later its yield goes back to 5%". Its trace says "the price returns to 100 / 1.05^10 = 61.39, ignoring the week that passed." The opening does not say to ignore elapsed time. Under the stated assumptions a week of accrual gives about 61.45, which makes (c) "above 61.39" literally true, though the reason it gives is false. That is one answer resting on an unstated setting. The fix is to drop "A week later" or say "moments later".

**5. Prediction: Pass.** About 58 of the 60 questions ask for an outcome from given numbers or a described setup. The rest are also numeric (Q16 and Q32). The share is well over 50%.

**6. No trivia: Pass.** Each named term (Macaulay duration, FRN, perpetuity, credit spread) is defined in the stem and then used in a calculation. No question has a date, a person or a name as its answer.

**7. Trap named: Pass.** Every answer's main trap names a specific belief, for example Q2's "the savings-account belief that higher rates are good for anyone who lends". Some secondary explanations are generic: Q11 "(d) guesses at a partial loss", Q23 "(c) splits the difference" and Q33 "(b) underestimates the coupon's cushion". They are scored under check 10.

**8. Answer shape: Pass.** All 60 give Why, Answer, The trap and Rule, in that order. I counted words in the shortest-looking answers (Q34 about 79, Q41 about 79, Q25 about 83, Q52 about 85) and the longest-looking (Q43 about 126, Q49 about 126, Q53 about 130). All fall within 60 to 150. This is a sampled count, not a scripted one.

**9. Coverage: Fail.** The map sits at the head of the answer key, the opening has none, every question appears in it, and every mechanism has at least two questions. The check also says "No two questions differ only in surface details", and three pairs break it:
- Q17 and Q48 use the same bond (5-year, coupon 5, price 100, yield 5%, split into government yield plus spread). Both components move, and the learner reprices. Only the numbers and the signs differ. The traps are the same belief, mirrored: "when 'interest rates' fall, every bond's price rises" and "rising government rates must lower every bond's price".
- Q14 and Q36 both price a coupon bond whose coupon sits below the market yield, and they share the trap: "subtracting the missing 3 a year for 2 years without discounting it (100 − 6)" and "subtracting the 3-a-year shortfall for 4 years without discounting (100 − 12)".
- Q11 and Q37 both put an FRN on its reset date beside a 5-year fixed bond, with rates up in one and down in the other. Their traps are "every 5-year bond moves the same way" and "all 5-year bonds react alike".

Mirror images and renumbered copies are the cheap way to meet "tested at least twice". The second question in each pair adds nothing the first did not test. A smaller issue: the map lists Q59 under mechanism 7 ("held to maturity, a bond pays exactly what it promised"), but Q59 tests near-zero duration, which belongs to mechanism 10.

**10. Distractors: Fail.** Most wrong options map to a real belief, and many are computed from it: Q1(a) and (c), Q9(d), Q14(a), Q25(c), Q29(d), Q31(d) (the 1-point policy rise applied to the 10-year), Q45(b). Two options are filler:
- Q23 "(c) both about +9%". The key's explanation is "(c) splits the difference". Nobody believes a 1-year and a 30-year bond each gain the average of their two moves.
- Q33 "(b) About 0.25 percentage points". The key's explanation is "(b) underestimates the coupon's cushion". No belief produces 0.25.

Q11(d) "about 97" does match a real belief: thinking the FRN's coupon only resets next year gives 103/1.06 = 97.17. But the key labels it "guesses at a partial loss", so the learner is not told which belief to repair. Q21 has only three options, against the prompt's "Give four options". Several options are left unexplained, including Q7(a), Q26(b), Q31(c) and (d), Q38(a) and (c), and Q51(c). That is allowed, but it weakens the diagnostic value.

**11. Artifact size: Pass.** There is no code. The longest scenarios (Q11, Q38, Q53, Q58) are about 70 words. No stem gives the answer away. Q39's stem says "The market yield for a company's 9-year bonds is 6%", which, combined with the opening's "where one rate is given for several bonds, all of them share it", comes close. But recognising that the market yield applies to both bonds is the very thing the question tests.

**12. Progression: Pass.** The bands are Q1–12 (20%), Q13–42 (50%) and Q43–60 (30%). Band 3 combines mechanisms or tests edge cases (Q43 duration against maturity, Q44 an FRN between resets, Q49 locking in a future amount, Q54 drift against a yield rise, Q59 one day to maturity). The weakest band-3 item is Q52, a single conversion already met in Q13 and Q25.

**13. Answers hidden: Pass.** `questions.md` contains no answers. The numbers given in stems (for example Q6's 110.64) are setup the learner needs.

**14. Honesty and source: Pass.** Nothing is invented. Every instrument and convention is standard. No area needed declaring.

**15. Diagnosis: N/A.**

**16. No copying: Fail (Q8).** The prompt's bond example: two 10-year bonds, yield 5% rising to 6%, a zero against a coupon-5 bond, "which loses a larger percentage", with (c) "both lose the same" and (b) "the higher-paying bond". Q8 keeps the 10-year maturity, the 5% starting yield, the 1-point rise to 6% and the mechanism (lower coupon, bigger loss). It changes the coupons to 2 and 9 and puts numbers on the options. Option (c) "Both lose 7.4%" is the example's own Bond B loss. Its traps copy the example's almost word for word:
- Example: "(c), from believing that equal maturity means equal interest-rate risk. (b) comes from assuming the higher-paying bond is more exposed to rates"
- Q8: "(b), from thinking the bond that pays more has more exposed to rates. (c) assumes the same maturity means the same risk"

That is the calibration example with surface changes. Q24 also reuses the example's exact two bonds (10-year zero and 10-year coupon 5, both at 5%) and asks for the example's own conclusion ("duration; A's is longer") as a ranking, with one bond added. On its own Q24 would be Borderline, because the shape does change. Q46 reuses the example's 61.39 for a different mechanism, which is fine. This failure is exactly the stress input 4 was built to expose.

## Promotion and status

No earlier version has outputs on this input, so there is nothing to compare against. v0.2.0 is **not fit to be called "tested" on this input**. It fails check 16, which is the stated purpose of input 4, and checks 9 and 10. The answer key itself is strong: 60 of 60 are correct, and the traces show real arithmetic. Moving the trace before the answer in v0.1.0 to v0.2.0 looks to have done its job on correctness. Whatever happens on other inputs, the run folder also needs its frozen `prompt.md`, and these failures belong in `failures.md`:

- v0.2.0, input 4, check 16: Q8 is the bond calibration example with new coupons, and its traps are copied.
- v0.2.0, input 4, check 9: surface pairs Q17/Q48, Q14/Q36 and Q11/Q37 (mirrored or renumbered).
- v0.2.0, input 4, check 10: filler options Q23(c) and Q33(b).
- v0.2.0, input 4, check 4: Q46 depends on ignoring a week of elapsed time.

## The single most important thing to fix next

Copying the calibration example (check 16). The prompt's only guard is one bare phrase with no reason, and the check list never mentions the examples:

> These examples set the standard. Treat them as calibration and write fresh questions for the topic; never copy them.

The writer kept the example's setup and changed its numbers. Nothing in the prompt says that counts as copying. Proposed edit in `<write>`, replacing that line:

> These examples show the standard a question and its answer should reach. They are not material for the quiz. When the topic overlaps an example, you may still test the example's mechanism, but build the question on a different setup, comparison and trap, and write the trap in your own words. A learner who has seen the example learns nothing from its twin with new numbers, and a reworded copy hides how little of the quiz is new.

And add to `<check>`:

> - No question repeats an example's setup, comparison or trap with only the numbers changed, and no two questions are mirror images of each other (the same setup with every move reversed).

The second clause also covers the check 9 pairs at low cost. The clause "you may still test the example's mechanism" is there to prevent over-correction. Without it, a writer told to avoid the example may drop coupon-driven duration altogether, and that is a core mechanism for this topic. Rerun input 4 and input 1 (the React calibration topic) after the change, because input 1 is the other input where the overlap is built in.

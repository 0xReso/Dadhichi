# Grade: pattern.quiz v0.2.0, input 1 (React useEffect, state updates and re-render order)

Grader: head (independent of builder and writer). Date: 2026-11-24.

Read: the design doc, `tests/pattern.quiz/rubric.md`, `tests/pattern.quiz/inputs.md`, `tests/pattern.quiz/failures.md` (empty), `tests/pattern.quiz/runs/v0.1.0/head-gate-review.md`, the frozen `runs/v0.2.0/prompt.md` and `1-react-effects/filled-prompt.md` (topic, depth low, learner line and sheet mode filled correctly), and the two output files.

Stated assumptions in `questions.md` line 2: React 18 in the browser, `createRoot`, StrictMode off; `useState`, `useEffect`, `useLayoutEffect`, `useRef`; one real click, each fully processed before the next.

## Tally

| # | Check | Verdict |
| --- | --- | --- |
| 1 | Count | Pass |
| 2 | Correct | Pass |
| 3 | Determinate | Pass |
| 4 | Assumptions | Pass |
| 5 | Prediction | Pass |
| 6 | No trivia | Pass |
| 7 | Trap named | Pass |
| 8 | Answer shape | Pass |
| 9 | Coverage | Pass |
| 10 | Distractors | Pass |
| 11 | Artifact size | Pass |
| 12 | Progression | Pass |
| 13 | Answers hidden | Pass |
| 14 | Honesty and source | Pass |
| 15 | Diagnosis | N/A (input 9 only) |
| 16 | No copying | Borderline (Q11) |

Pass 14, Borderline 1, Fail 0, N/A 1.

## Check 2: independent trace, one line per question

I worked each question from the question text and the stated assumptions, and wrote down my result before opening `answers.md`.

| Q | My result | Stated result | Agree |
| --- | --- | --- | --- |
| 1 | render, after hook call, effect | same | yes |
| 2 | A 3, B 1, C 1 | same | yes |
| 3 | render 0, handler 0, render 5 | same | yes |
| 4 | 2 | 2 | yes |
| 5 | start 1, stop 1, start 2, stop 2 | same | yes |
| 6 | parent render, child render, child effect, parent effect | same | yes |
| 7 | render 0 0, render 1 1 (automatic batching in a timer) | same | yes |
| 8 | 4 | 4 | yes |
| 9 | 1 (stale `n = 0`, ticks 2 to 5 set 1 again) | 1 | yes |
| 10 | render, layout, effect | same | yes |
| 11 | render 0, effect 0, render 1 | same | yes |
| 12 | effect 0, once | same | yes |
| 13 | 20 | 20 | yes |
| 14 | render 0, run 0, render 1, clean 0, run 1 | same | yes |
| 15 | parent render 1, child render, parent effect 1 | same | yes |
| 16 | (c), endless loop: a new object each time fails `Object.is` for both the setter and the deps. React 18 only logs a dev warning for nested passive updates | (c) | yes |
| 17 | key 0 | same | yes |
| 18 | `0`, render 2 | same | yes |
| 19 | (a) | (a) | yes |
| 20 | 1 | 1 | yes |
| 21 | mount 0, unmount, mount 0; shows 0 | same | yes |
| 22 | A clean 0, B clean 0, A run 1, B run 1 | same | yes |
| 23 | parent render false, child render, parent effect false, parent render true, child render, parent effect true | same | yes |
| 24 | 4 calls, 1 active | same | yes |
| 25 | render 0 (the first updater is computed eagerly as 1, which is not 0, so a render is scheduled. The queue resolves to 0 during render and React bails out after calling the body) | render 0 | yes |
| 26 | 0 2 | same | yes |
| 27 | "0 0" after the third a; "3 1" after b | same | yes |
| 28 | child layout, parent layout, child effect, parent effect | same | yes |
| 29 | render 0, render 1, later 0, render 2 | same | yes |
| 30 | render 0, layout 0, effect 0, render 1, layout 1, clean 0, effect 1, render 2, layout 2, clean 1, effect 2 | same | yes |

30 of 30 agree. I then read every trace for a false step and found none that rises to Borderline. Two simplifications, noted but not scored:
- Q10, Q28 and Q30 say passive effects run "after paint". React says it generally lets the browser paint first, and effects from discrete events such as clicks are flushed before paint in React 18. None of the click questions (Q14, Q22) mentions paint, so no trace here makes a false claim about click timing.
- In Q25, step 2 says "React cannot know the final value without applying them, so it renders `C`". The real reason is that the eager check applies only to the first update in an empty queue. The outcome and the bailout description are right.

**Verdict: Pass.**

## Other checks

**1 Count.** Q1 to Q30, low depth. Pass.

**3 Determinate.** Each question has one outcome under React 18. One fragile point: Q25's answer, `render 0`, depends on React 18's eager-state and bailout internals, which react.dev only describes as "React may still need to call your component". The stated version pins it, so I score it Pass. It is the question most likely to change under a future React, so revisit it when the verified version moves. Q2 is readable but awkward: the component is named `C` and one effect logs `"C"`, and the trace then says "so `C` re-renders twice". It is not ambiguous, but it slows the reader. Pass.

**4 Assumptions.** Version, root API, StrictMode and click processing are stated. Q16's dev-only warning does not change the selected option. No answer rests on an unstated setting. Pass.

**5 Prediction.** All 30 ask for an outcome from a code artifact. Pass.

**6 No trivia.** None. Q7's trap mentions React 17 to explain a belief, not as the answer. Pass.

**7 Trap named.** Every trap names a concrete wrong output and the belief behind it, for example Q22 "each effect is cleaned up and re-run as a pair" and Q27 "the page tracks any value used in the markup". None is generic. Pass.

**8 Answer shape.** All 30 have Why, Answer, The trap and Rule, in that order. I estimated word counts. The shortest are Q28 (about 88) and Q20 (about 86). The longest are Q23 (about 148), Q30 (about 145) and Q16 (about 140). All fall within 60 to 150. Q23 is close to the ceiling. Pass.

**9 Coverage.** The ten-item mechanism map is at the head of `answers.md`, and the opening in `questions.md` has no map. Each mechanism maps to three to six questions in different shapes. The closest pair is Q4 and Q13: both are three-line `handle` bodies that ask for the final `n`. They test different beliefs, though: a snapshot `n + 1` against an updater in Q4, and a plain value resetting the queue in Q13. So they differ in more than surface details. The stale-closure trio (Q9 interval, Q17 listener, Q26 timeout plus ref) also varies the outcome shape. Pass.

**10 Distractors.** There are two multiple-choice questions. In Q16, (a) is "setter compares contents", (b) is "deps compare contents" (which, applied consistently, gives exactly two renders), and (d) is "setState in an effect is forbidden". In Q19, (b) is "layout effects run after paint", (c) is "layout effect runs before render" and (d) is "updates in an effect are dropped". Every wrong option maps to a belief. Pass.

**11 Artifact size.** The longest artifacts are 13 lines (Q22, Q23, Q25, Q26, Q30). No names or comments leak the answer. Minor: Q24's stem says "(the screen shows 3 and that render's effects have run)". This removes the stale-closure reading, but the question asks about interval counts, so it disambiguates rather than gives the answer away. Pass.

**12 Progression.** Band 1 is Q1 to Q6 (20%), band 2 is Q7 to Q21 (50%) and band 3 is Q22 to Q30 (30%). Band 3 combines mechanisms: Q23 (tree order, effect timing and snapshot), Q25 (batching, updaters and bailout), Q29 (closure, updater and timer) and Q30 (layout, cleanup and effect chain). Q27 is the lightest of the band but still pairs a ref with a render. Pass.

**13 Answers hidden.** `questions.md` contains no answers. The key is in a separate file. Pass.

**14 Honesty and source.** No source was given and no area was declared unreliable. No invented API or default. The Q16 claim ("prints a 'Maximum update depth exceeded' warning but does not stop the loop") matches React 18's handling of nested passive updates. Pass.

**15 Diagnosis.** Not applicable to input 1.

**16 No copying.** The calibration example has a `useState(0)`, a `[]` effect that logs `n` and calls `setN(1)`, a `[n]` effect and a body log, and it asks for the full log. Q11 is that example with effect B removed. It keeps the `[]` effect that logs `n` and sets `n`, the body log `render n`, the same "write the full log" stem and the same tested belief (the effect reads the render-0 snapshot, and the set state appears only in the next render). Its answer, `render 0`, `effect 0`, `render 1`, is the calibration answer with the B lines deleted. Removing an effect is more than a cosmetic change, but what remains is the calibration's core item. This input's stress line asks the quiz to reach the standard "without copying the calibration example". Q30 also descends from the example, but it adds layout effects, cleanups and a two-step chain, which is real new work. **Borderline (Q11).**

## Is v0.2.0 fit to be called "tested" on this input?

Yes, for input 1. It has no Fail, 30 of 30 answers are correct by independent trace, and the only non-Pass is a Borderline on check 16. Under the design (section 7), the status `tested` needs the whole input set graded, not one input. This result counts towards that but does not settle it. There is no earlier version, so no promotion comparison applies.

## Single most important fix next

The calibration overlap in Q11. The cause is in the prompt. On a React topic, the situation paragraph ("Ten lines of React code define two effects and a log line in the body") and example 1 together present the exact skeleton the writer then reuses. The current guard is in `<write>` and only says what not to do:

> These examples set the standard. Treat them as calibration and write fresh questions for the topic; never copy them.

Proposed replacement:

> These examples set the standard for form: the artifact size, the trace, the named trap and the rule. When the topic overlaps an example, test that example's mechanism through a different artifact and a different wrong belief, for instance a handler or a timer instead of an effect that logs state and then sets it. A learner who has seen the example already knows that question's answer, so a near-copy spends one of the set's questions on nothing.

Add one matching line to `<check>`:

> - No question shares both its artifact shape and its tested belief with a calibration example.

Before the next round, check that this does not over-correct. It should not push the writer to avoid the effect-timing mechanism on React inputs. That mechanism must still be tested, in new shapes. The rerun of input 1 should still map mechanism 1 to at least two questions.

## Lower-priority notes for the builder

- Q2: rename the component or the log label so that `C` refers to one thing.
- Q25: when `verified_on` moves to a newer React, re-trace it first. It is the item most tied to internals.
- Only 2 of 30 questions are multiple choice. That fits the prompt ("when the possible outcomes are few and distinct"), so it is not a defect. Check 10 is lightly exercised on this input.

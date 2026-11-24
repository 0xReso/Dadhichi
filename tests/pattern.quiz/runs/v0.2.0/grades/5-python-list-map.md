# Grade: pattern.quiz v0.2.0, input 5 (Python list.map, mistaken premise)

Grader: head (independent of builder and writer). Date: 2026-11-24.

Read: the design doc, `tests/pattern.quiz/rubric.md`, `tests/pattern.quiz/inputs.md`, `tests/pattern.quiz/failures.md` (empty), the frozen `runs/v0.2.0/prompt.md`, `5-python-list-map/filled-prompt.md` (topic and depth low filled, learner and source empty, sheet mode, all correct), and the two output files. I did not look at `runs/v0.2.0-gemini-4-neon/`. The writer worked by reasoning only, and so did I: no code was executed. My CPython 3.12 claims come from knowing the interpreter's behavior, and the lines that depend on implementation details are named below.

Opening (`questions.md` lines 1 to 3): "Python list.map · low depth · 30 questions" / "Assumptions: CPython 3.12, each snippet run as its own fresh script; an error is given as its exception type and message." / "Python lists have no `.map` method, so this quiz covers the built-in `map()` function applied to lists, which is what `list.map` means in languages like JavaScript."

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
| 10 | Distractors | Borderline (Q29) |
| 11 | Artifact size | Borderline (Q1, Q7, Q11, Q14, Q17, Q22) |
| 12 | Progression | Pass |
| 13 | Answers hidden | Pass |
| 14 | Honesty and source | Borderline (Q5) |
| 15 | Diagnosis | N/A (input 9 only) |
| 16 | No copying | Pass |

Pass 12, Borderline 3, Fail 0, N/A 1.

## Check 2: independent trace, one line per question

I worked each question from its text and the stated assumptions, and wrote down my result before opening `answers.md`.

| Q | My result | Stated result | Agree |
| --- | --- | --- | --- |
| 1 | (c) AttributeError: 'list' object has no attribute 'map', line 2 | same | yes |
| 2 | `<map object at 0x...>`, `map` | same | yes |
| 3 | created, double 1, double 2, [2, 4] | same | yes |
| 4 | ['1', '2', '3'], [] | same | yes |
| 5 | (a) [11, 22] (3.12 has no strict=) | same | yes |
| 6 | [None, None], [[1, 0], [2, 0]] | same | yes |
| 7 | TypeError: add() missing 1 required positional argument: 'y', nothing printed | same | yes |
| 8 | has items | same | yes |
| 9 | f 1, g 2, f 2, g 3, [20, 30] | same | yes |
| 10 | ['1', '2', '3'] | same | yes |
| 11 | (b) parsed, then ValueError: invalid literal for int() with base 10: 'x' at line 4 | same | yes |
| 12 | True, [5, 7] | same | yes |
| 13 | [110, 120] | same | yes |
| 14 | TypeError: 'method_descriptor' object is not iterable, raised by the map(...) call (map checks the iterables when it is built, not the function) | same | yes |
| 15 | a, b, [None, None] | same | yes |
| 16 | ['aaa', '', 'cc'] | same | yes |
| 17 | TypeError: 'map' object is not subscriptable | same | yes |
| 18 | error, [3] | same | yes |
| 19 | ['aa', 'bb'] | same | yes |
| 20 | [], [1] | same | yes |
| 21 | [2, 4, 6] | same | yes |
| 22 | (b) 6, then ValueError | same | yes |
| 23 | [10], done (StopIteration from the function ends list(); PEP 479 covers generators only) | same | yes |
| 24 | f 1, f 1, 1, then | same | yes |
| 25 | [[2], [2]] | same | yes |
| 26 | 1, 2, 3, 4 | same | yes |
| 27 | [12, 34] (5 consumed and lost) | same | yes |
| 28 | [[1, 3], [0, 2]] / [None, None] [[1, 3], [0, 2]] | same | yes |
| 29 | (b); (a) gives [4, 6], (c) TypeError, (d) [(1, 2, 1, 2), (3, 4, 3, 4)] | same | yes |
| 30 | call 5, 2, call 0, skip, call 2, [5] | same | yes |

30 of 30 agree.

## Reasoning per check

**1 Count.** Q1 to Q30, low depth. Pass.

**2 Correct.** All 30 stated answers match mine. I read every Why for false steps. The version-sensitive spots hold up under 3.12. Q7 uses the 3.10+ wording "add() missing 1 required positional argument: 'y'". Q11 uses the int() message exactly. Q14 is right that `map` builds its iterators at construction and does not check whether the function is callable. Q23 is right that PEP 479 does not apply to `map`. Q22 gives only "ValueError" and avoids the `max()` empty-argument message, whose wording changed between releases, so it is safe. Q10 step 1 says the map "keeps a reference to the list object itself and a position in it". Strictly, the map holds a list iterator, and that iterator holds the list and the index. This is a fair simplification, not a false step. Pass.

Two imprecise lines sit outside any trace, so they do not count against check 2. The builder should still know about them:
- Mechanism 10: "In-place methods such as `append`, `sort` and `print` return `None`." `print` is not an in-place method.
- Mechanism 11: "a `StopIteration` silently ends the map early". The map is not ended: another `next(m)` after Q23's list() would call `f(3)`. Within a consumer such as `list`, the results are cut short, which is what the Q23 Rule correctly says.

**3 Determinate.** Q2's address is shown as `0x...`, which the answer notes varies, so that is acceptable. Q14's "on which call" has one answer, the map(...) call. Q29 has exactly one option that yields [3, 7]. Pass.

**4 Assumptions.** CPython 3.12 and fresh-script runs are stated. Every answer that depends on the runtime (error messages, Q5's lack of a length check, Q14 and Q23's implementation behavior) is covered by "CPython 3.12". Pass.

**5 Prediction.** All 30 ask for an outcome from a code artifact. Q29 is a fix question, but it also rests on predicting each option's output. Pass.

**6 No trivia.** Q2 asks for `type(result).__name__`, but the point is the iterator-not-list behavior, not a memorized name. Pass.

**7 Trap named.** Every trap names a specific belief, for example Q8: "from the belief that a map over an empty list is falsy like an empty list." None is generic. Pass.

**8 Answer shape.** All 30 have Why, Answer, The trap, Rule, in that order. By my estimates the shortest are about 80 words (Q17, Q19) and the longest are at the 150 cap (Q14 about 148, Q29 about 150). Even if two run slightly over, at least 28 of 30 fall in range. Pass.

**9 Coverage.** The mechanism list heads `answers.md` and the opening has none. All 11 mechanisms have at least two questions. M5 (Q9, Q24) and M9 (Q13, Q25) have the minimum, in distinct shapes. The closest pairs are Q18 and Q30 (an exception mid-map, then continuing) and Q6 and Q15 (a None-returning function). Each pair still differs in shape: Q30 adds `next` and call prints that expose whether the item is retried, and Q6 adds aliasing of the mutated rows. Pass. Note that `inputs.md` suggested comprehensions as part of the real mechanism. None is tested; Q25 only uses one incidentally. The rubric does not require them, but it is a fair gap.

**10 Distractors.** Q1, Q5, Q11 and Q22 are clean: each wrong option has a named belief. Q29 option (c), "Change the map call to `map(lambda x, y: x + y, list(pairs))`", is filler. `pairs` is already a list, so the change does nothing. The answer's justification, "(c) blames the container type", names no belief a learner could plausibly hold, since the container type does not change. Borderline (Q29).

**11 Artifact size.** No artifact is over 15 lines (the longest, Q30, is 12). The stems leak a signal, though. Every question phrased "What happens when this runs?" raises an exception: Q1, Q7, Q11, Q14 (with "and on which call?"), Q17 and Q22. Every other question is "What does this print?" or "What gets printed, in what order?". After two or three of these, the learner knows "What happens" means an error. For the open-ended ones (Q7, Q14, Q17) that is most of the answer, leaving only the exception type to guess. No single stem states the answer, so this is not a Fail. But the rubric line "No stem ... gives the answer away" is not cleanly met. Borderline (Q1, Q7, Q11, Q14, Q17, Q22).

**12 Progression.** The bands are Q1 to Q6 (6, 20%), Q7 to Q21 (15, 50%) and Q22 to Q30 (9, 30%). Band 3 combines mechanisms or tests edges: exhaustion across consumers (Q22), StopIteration (Q23), a chain plus `next` (Q24), late binding in a loop (Q25), mutation during iteration (Q26), one iterator passed twice (Q27), sorted versus sort (Q28), and an exception plus continuation (Q30). Pass.

**13 Answers hidden.** `questions.md` contains no answers. Pass.

**14 Honesty and source.** The premise is corrected in the opening and tested directly in Q1, and the quiz is built on the real built-in. No invented API appears in any question or Answer line. One line leaks a later version into the stated 3.12 runtime. Q5's trap says "(c) comes from expecting a length check (map has none by default)". "By default" implies a non-default length check exists. In 3.12 it does not: `strict=` arrived in 3.14, and `map(..., strict=True)` on 3.12 raises `TypeError: map() takes no keyword arguments`. A learner who follows the hint will find an API that, under the stated assumptions, does not exist. Borderline (Q5).

A minor point: the opening's third line is used for the premise correction. The prompt reserves that line for declaring an unreliable area, but a premise correction is the honest use of it, so I count no penalty.

**16 No copying.** The calibration examples are a React effect order, bond duration and a mutable default argument. None is reused. Q13 and Q25 test late binding, which is a different mechanism from the mutable default. Pass.

## Verdict on this input

No prior version outputs exist, so there is nothing to compare for promotion. v0.2.0 has no Fail on input 5, and its answer key is fully correct by independent trace, which is the check that matters most for this pattern. I count this input as passed toward "tested" status, with three Borderlines that are not clean passes. "Tested" status itself still needs the full input set graded, and the grading here is by reasoning, not execution. Q14, Q23 and Q27 rest on CPython implementation details, so if the harness gains execution, those are the first to run.

## Most important fix next

The stem-wording leak in check 11. It is systematic (6 of 30 questions here) and comes from the prompt, not the topic, so it will recur on every programming input where some snippets raise and others print. The other two Borderlines are single instances.

Current text in `<write>`, **The question.**:

> Ask for one precise, checkable outcome: the exact output, an order of events, a number, which of two things is larger, which line is the bug, what changes when one detail changes. Mix these shapes across the set.

Proposed replacement:

> Ask for one precise, checkable outcome: the exact output, an order of events, a number, which of two things is larger, which line is the bug, what changes when one detail changes. Mix these shapes across the set. Word each stem the same way whatever the outcome turns out to be. If one phrasing is kept for snippets that raise an error and another for snippets that print, the learner reads the outcome from the wording instead of the code. For code that may print or raise, ask "What does this print or raise?" throughout.

Secondary, for the builder's list, not part of this fix:
- In `<plan>` step 3, add: "Describe only features that exist in the stated version, including in traps and asides, because a hint at a later feature sends the learner looking for something their runtime does not have." This addresses Q5.
- In `<write>` after "make each wrong option the answer that a specific wrong belief produces", add: "and check that each option actually changes something, since an option that does nothing tests no belief." This addresses Q29(c).

Failure-log lines to add (these are Borderlines, so the builder may log them as near-misses):
- v0.2.0, input 5, check 11, "What happens when this runs?" used only for snippets that raise (Q1, Q7, Q11, Q14, Q17, Q22).
- v0.2.0, input 5, check 14, Q5 trap "(map has none by default)" implies a 3.14 `strict=` option under stated CPython 3.12.
- v0.2.0, input 5, check 10, Q29 option (c) `list(pairs)` is a no-op on a list, a filler option.

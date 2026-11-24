# Head review of Input 5 · Python list.map

**v0.2.0 · gemini-4-neon · sheet mode · 11 Pass, 1 Borderline, 3 Fail, 1 N/A**

All 30 stated answers agree with CPython 3.12.14. The first repair is to keep the honest premise correction and replace Q1. The opening already tells the learner why that particular call fails. A question using the real built-in can test a fresh prediction without sacrificing the correction.

## Independent verification for checks 2 and 3

I ran each fenced artifact as a fresh module under CPython 3.12.14 and captured stdout or the exception and its line. For Q21 I evaluated each expression separately with the supplied `nums` and checked its type before consuming anything. I also worked through each Why against the code, including the point of each side effect, lookup or exception. The last column records agreement on the **outcome**. Q14’s arrows denote successive output lines.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| Q1 | Looking up `nums.map` raises `AttributeError` on line 2, before the call or print. | (c) `AttributeError` | Yes |
| Q2 | Defining `double` and building the iterator run no callback. The last line prints `done`. | `done` | Yes |
| Q3 | First collection pulls 11 and 21 through exhaustion. The second pulls nothing. Output `[11, 21] []`. | `[11, 21] []` | Yes |
| Q4 | The empty map still tests true. Equality with the empty list is false. Output `True False`. | `True False` | Yes |
| Q5 | Pulling 1, 2, 3 produces 10, 20, 30 in a fresh list. The numeric callback leaves the source intact. Output `[1, 2, 3] [10, 20, 30]`. | `[1, 2, 3] [10, 20, 30]` | Yes |
| Q6 | Pairs (1,10) and (2,20) yield 11 and 22. The next pull takes 3 but gets no partner, so there is no third call. Output `[11, 22]`. | `[11, 22]` | Yes |
| Q7 | The source list gains 3 before the iterator's first pull. All three entries are multiplied by ten. Output `[10, 20, 30]`. | `[10, 20, 30]` | Yes |
| Q8 | Construction runs no division. One pull computes 10 // 2, prints `5`, and the program ends before reaching zero. | (c) `5`, normal exit | Yes |
| Q9 | The comprehension prints 1 and 2 with spaces, the separator prints next, the unused map makes no calls, and the last print completes `1 2 \| end`. | `1 2 \| end` | Yes |
| Q10 | Construction requests an iterator from the second argument, a function. Line 2 raises `TypeError` before the noncallable first argument can be invoked. | (a) line 2, `TypeError` | Yes |
| Q11 | Membership consumes 2 and then the matching 4. The remaining inputs 3 and 4 double to 6 and 8. Output `True [6, 8]`. | `True [6, 8]` | Yes |
| Q12 | Each append changes its row and returns None. The surrounding list constructor collects those returns. Output `[[1, 9], [2, 9]] [None, None]`. | `[[1, 9], [2, 9]] [None, None]` | Yes |
| Q13 | Subscribing the map raises `TypeError` on line 2, before either conversion or printing. | (c) `TypeError` | Yes |
| Q14 | Pull 1 logs `tag 1` and yields 2. Pull 2 logs `tag 2` and yields 4. The body logs each result and breaks on 4. Output `tag 1` → `got 2` → `tag 2` → `got 4`. | `tag 1` → `got 2` → `tag 2` → `got 4` | Yes |
| Q15 | Collection attempts `pair_sum(1, 10)`. Argument binding raises `TypeError` on line 4 before the function body runs. | (c) `TypeError` | Yes |
| Q16 | The iterator still refers to the original [1, 2] after rebinding. Adding ten yields `[11, 12]`. | `[11, 12]` | Yes |
| Q17 | All three functions share the comprehension variable. It holds 3 when each is called. Output `[6, 6, 6]`. | `[6, 6, 6]` | Yes |
| Q18 | Construction leaves the log empty. Processing 5 logs it and returns 2. Processing 0 logs it before division fails. Collection aborts, the handler assigns None, and input 2 is untouched. Output `[5, 0] None`. | `[5, 0] None` | Yes |
| Q19 | Distinct map objects compare unequal without advancing. Each collection then yields the same two strings. Output `False True`. | `False True` | Yes |
| Q20 | The first pass builds two sorted copies. The second sorts the originals in place and returns None twice. Output `[[1, 3], [2, 4]] [None, None] [[1, 3], [2, 4]]`. | `[[1, 3], [2, 4]] [None, None] [[1, 3], [2, 4]]` | Yes |
| Q21 | (a) fails on the missing filter attribute. (b) fails trying to iterate the lambda. (c) filters to 2 and 4, squares, and materializes `[4, 16]`. (d) evaluates to a map object. | (c) `list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))` | Yes |
| Q22 | The comprehension uses 2 immediately. At consumption the lambda looks up the module global `k`, now 10. Output `[2, 4] [10, 20]`. | `[2, 4] [10, 20]` | Yes |
| Q23 | Independent list iterators supply matching values for sums 2, 4, 6, 8. Sharing one cursor instead pairs 1 with 2 and 3 with 4. Output `[2, 4, 6, 8] [3, 7]`. | `[2, 4, 6, 8] [3, 7]` | Yes |
| Q24 | The first pull reads index 0 and appends 1. The second reads the newly populated index 1 and appends 1 again. Both appends return None. Output `None None [1, 1, 1]`. | `None None [1, 1, 1]` | Yes |
| Q25 | The three pulls consume 2, 0, 5 in order. The first yields 5, the handler appends 'err' on the second, and the third yields 2. Output `[5, 'err', 2]`. | `[5, 'err', 2]` | Yes |
| Q26 | The truth test consumes nothing. The predicate yields false, false, true before any stops. The sole remaining input 4 also yields true. Output `True [True]`. | `True [True]` | Yes |
| Q27 | The first pull yields 10 and advances to index 1. Popping index 0 shifts 3 into index 1. The remaining pull yields 30. Output `10 [30]`. | `10 [30]` | Yes |
| Q28 | The first pair yields 11. Building a second pair consumes 2 from the left before the right raises StopIteration. Only 3 remains on the left. Output `[11] [3]`. | `[11] [3]` | Yes |
| Q29 | Both objects initially provide 2, 4, 6. The first sum exhausts the map, the second sums an empty iterator, and the list can be summed twice. Output `12 0 12 12`. | `12 0 12 12` | Yes |
| Q30 | The chain logs f(2), g(1) and yields 10, then logs f(1), g(0) before division fails. The handler assigns 'fail' and no one requests 3. Output `[('f', 2), ('g', 1), ('f', 1), ('g', 0)] fail`. | `[('f', 2), ('g', 1), ('f', 1), ('g', 0)] fail` | Yes |

## Rubric decisions

1. **Count.** Questions and answers each run from Q1 to Q30 once, in order, meeting the low-depth count. **Pass.**
2. **Correct.** All 30 Answer fields match the independent results. Q22 Why step 2 says “its lambda captures `k` by reference (late binding, mechanism 9)”. In this module-level artifact the lambda captures no variable. Its compiled code has an empty `co_freevars` and executes `LOAD_GLOBAL k` on invocation. The later lookup explains the correct result. Q17 really does capture a variable from an enclosing comprehension. One correct outcome has a false trace step. **Borderline.**
3. **Determinate.** Each row above yields one output, one exception or one expression meeting the stem. In Q21, (d) would *yield* the requested elements, but the question asks which expression *evaluates to* the list. In Q28 the specified implementation fixes which input advances on the final pull. No ambiguous items. **Pass.**
4. **Assumptions.** The opening specifies “Python 3 (CPython 3.12), standard built-ins unmodified unless shadowed in the snippet.” That suffices even for Q28's left-to-right consumption. **Pass.**
5. **Prediction.** All 29 fenced programs ask for observable output or an exception. Q21 also requires predicting values and types to choose an expression. Even the fenced programs alone exceed 50%. **Pass.**
6. **No trivia.** Every question turns on behavior. Even Q10 and Q13 require determining the failing operation to select an exception. **Pass.**
7. **Trap named.** All 30 name a specific wrong belief. For example, Q7 predicts a snapshot, Q16 predicts a later lookup of the rebound list name, and Q28 predicts that map checks availability before pulling the left item. Q19's suggestion that consuming both maps explains a false second comparison is weak, since two empty lists compare equal. Its first trap still identifies a concrete identity-versus-value mistake. **Pass.**
8. **Answer shape.** A Python 3 parser found exactly Why, Answer, The trap and Rule, in order, for all 30. I removed field labels, bullet prefixes and numbered step markers, then counted whitespace-separated tokens, including inline code. Word counts in Q order were `104 105 109 105 96 112 102 114 99 116 / 117 95 104 129 92 102 115 120 103 118 / 131 118 130 138 122 111 118 106 112 156`. Q30 exceeds 150. The other 29/30 (96.7%) meet the inclusive 60–150 range. **Pass.**
9. **Coverage.** The nine numbered entries appear only at the head of the key, each with several question numbers. Most rules recur in substantively different forms, such as full collection in Q3 and partial consumption by membership in Q11. But entry 9 promises “Eager list comprehensions vs. lazy `map()` and closure late binding — Q9, Q17, Q22, Q29”. Of these, only Q17 tests the actual closure mechanism with `funcs = [lambda: x * 2 for x in [1, 2, 3]]`. Q22’s `b = map(lambda x: x * k, [1, 2])` reads a module global. Q9 and Q29 have no captured local either. Combining distinct mechanisms under one list entry conceals the missing second closure question. **Fail.**
10. **Distractors.** I checked Q1, Q8, Q10, Q13, Q15 and Q21. Q8(b) says “Prints `5`, then raises `ZeroDivisionError` on line 3”; the key says “(b) thinks `next(m)` pre-fetches the next item”. But line 3 is `print(next(m))`. Even with the proposed prefetch mistake, an exception inside `next` would occur before `print` received 5. Q8(d), “Prints `5`, `0`, `2`”, additionally needs an invented result for integer division by zero. Replace these options with outcomes that follow from identifiable beliefs, such as silently displaying nothing because the learner believes a lazy map never runs even after one pull. **Fail.**
11. **Artifact size.** Python 3 counted physical lines between fences, including internal blank lines. Counts by question were `3 6 4 2 3 4 4 3 8 3 / 2 3 2 9 5 4 2 11 3 4 / – 5 5 5 8 5 6 4 4 14`. Q21 uses one setup expression and four one-line choices. Q30 is longest at 14. The stems are short, the names describe data or operations, and no stem or code comment discloses its outcome. The Q1 disclosure is in the separate opening, scored under check 13. **Pass.**
12. **Progression.** Q1–6, Q7–21 and Q22–30 give 6/15/9, exactly 20%/50%/30%. Q2 isolates unused lazy work, Q14 interleaves pulls and an early exit, and Q30 traces two callbacks, side effects and an exception. Q24 and Q28 also require tracking state across pulls. **Pass.**
13. **Answers hidden.** The files put the formal answer key after the questions, but the opening states “Python lists do not have a .map() method” and “why .map() fails on lists”. Q1 immediately asks what happens at `res = nums.map(lambda x: x * 2)`, with “(c) Raises `AttributeError`” among the choices. The opening supplies the decisive missing-attribute fact and explicitly rules out both successful-output options. The honest correction can stay if Q1 tests another outcome. **Fail.**
14. **Honesty and source.** The opening explicitly corrects the mistaken list method. The failing attribute access in Q1 is intentional. Q5 uses the real built-in function, and Q9 compares it with an actual list comprehension. Q21 also identifies the fictitious method chain as an error. Input 5 supplies no source. **Pass.**
15. **Diagnosis.** Input 5 is a sheet with no interactive learner replies. This check applies only to input 9. **N/A.**
16. **No copying.** The frozen Python example defines `add(x, items=[])`, calls it twice with the default, and tests the identity of the two returned references. None of the 30 questions uses a shared mutable default. The closest, Q24, uses a list created explicitly and a bound append method. Its second pull depends on a live iterator reaching a newly appended element. Q17’s default-argument idiom appears only as a suggested repair in the key. Neither reproduces the calibration question. **Pass.**

## Repair and comparison

Keep the premise correction. Replace Q1 with a second closure question in a different form, for example a function that returns a lazy map over a locally rebound scale factor. That would address both the opening disclosure and the missing closure exercise. Correct Q22’s explanation to say the lambda looks up the global name when called.

Three Rule sentences also extend beyond what their examples establish. Q5’s “`map()` never mutates the input list's own elements” needs to distinguish the callback’s side effects, as Q12 demonstrates. Q12’s “filling the mapped output with `None`” holds for append and sort, while a mutator such as `list.pop` returns a value. Q18’s “later elements are never processed” holds for that aborted collection attempt. A later consumer can resume the same map, as Q25 shows. These are teaching-rule issues separate from the 30 stated runtime outcomes.

The v0.1.0 run directory contains a gate review only. The other Input 5 output is from the same v0.2.0 prompt. This sample supplies no matched earlier-version score on which to base promotion.

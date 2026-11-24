# Input 9 · JavaScript closures · Independent head grade

**13 Pass, 1 Borderline, 1 Fail, 1 N/A.** All ten Part 1 outcomes are correct, and the learner earned **7/10**. Check 9 fails because Q15 repeats Q4’s independent-counter exercise with only surface changes. Check 2 is Borderline because three explanations assign the logging operation to the wrong function.

The sample covers Q1–20 of the planned 30, ten reviewed answers, and an early-stop scorecard. The earlier v0.1.0 run contains a gate review only. There is no earlier Input 9 output to compare for promotion.

## Rubric decisions

| # | Check | Evidence and reasoning | Verdict |
| --- | --- | --- | --- |
| 1 | Count | The opening promises 30 questions at low depth. Part 1 contains exactly Q1–10, the interactive count required here. Part 2 continues at Q11 and ends at Q20. | Pass |
| 2 | Correct | All ten stated outcomes match independent execution. Three Why traces say a returning function logs its value. For example, Q3 says “`read()` reads its current value and logs `5`.” The caller performs that operation. The per-question audit below identifies each affected step. The rubric assigns Borderline to a correct outcome with a false trace step and Fail to a wrong outcome. | Borderline |
| 3 | Determinate | Each of Q1–10 has one result under the stated assumptions, as traced below. Q11–20 also each resolve to a single result, including the exception in Q14. | Pass |
| 4 | Assumptions | The opening gives ES2022+, strict mode, a script runtime, and console order. Strict mode resolves the bare regular-function call in Q9. Each fenced question is a standalone exercise. | Pass |
| 5 | Prediction | All 20 stems ask what the displayed code logs or what happens when it runs. | Pass |
| 6 | No trivia | All 20 answers require evaluating bindings, calls, or mutations. None asks for a memorized name or date. | Pass |
| 7 | Trap named | All ten reviewed traps identify a specific belief. For instance, Q4 distinguishes a counter shared by all factory calls from a counter reset on each inner call. Q10 distinguishes a per-pass outer variable from a mistaken extra assignment on loop exit. | Pass |
| 8 | Answer shape | The parser found Why, Answer, The trap, and Rule in that order for all ten reviewed answers. All ten fall within 60–150 words under the counting convention below. | Pass |
| 9 | Coverage | The opening gives no map. The first substantive section after the scorecard title and overall score is a numbered nine-mechanism map with correct question numbers and tallies for Q1–10. Q6 and Q10 revisit loop bindings in different shapes. Across the delivered questions, however, Q4 asks “`console.log(a(), a(), b(), a());`” and Q15 asks “`console.log(f(1), f(1), g(1));`”. Both create two counters from the same factory, advance the first twice and then the second once, and ask for the output. Q15 changes the starting number, adds a constant argument to each returned value, and drops the last call. It tests the same reasoning in the same shape. This observed duplicate breaks the check regardless of Q21–30. | Fail |
| 10 | Distractors | All wrong options in the five multiple-choice items have identifiable models, detailed below. | Pass |
| 11 | Artifact size | All 20 code fences contain 8–13 physical lines, including blank lines. The stems ask for an outcome without revealing it. Names describe operations and there are no answer-bearing comments or prose scenarios. | Pass |
| 12 | Progression | Q1–6 mostly isolate one rule. Q8–10 combine property evaluation, receiver binding, or contrasting loop bindings. Q11–20 include applications such as Q16’s object alias after rebinding and Q17’s attempted receiver override. The learner stopped before the final band (roughly Q22–30), so the full proportions and final-band requirement cannot be graded. | N/A |
| 13 | Answers hidden | Part 1 contains questions, unmarked choices where applicable, and the invitation to reply. Its answer key first appears after the learner’s submission. | Pass |
| 14 | Honesty and source | Input 9 supplies no reference text. The questions use established JavaScript behavior, and the early scorecard restricts the denominator to the ten attempted answers. | Pass |
| 15 | Diagnosis | Q1, Q6, and Q8 each receive all four answer parts, an explicit Wrong mark, and a diagnosis consistent with the submitted reply. The other seven marks and the mechanism subtotals reconcile to 7/10. See below. | Pass |
| 16 | No copying | None of Q1–20 reproduces the prompt’s React effect-order, bond-pricing, or Python mutable-default example. Q4 and Q15 duplicate one another within this quiz, which is scored under Check 9. | Pass |

## Check 2 independent results and Check 3 determinacy

I executed each original fence separately with an explicit strict-mode directive in Node v24.22.3. A slash separates successive log lines below. Spaces separate values printed by one call.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| Q1 | `1` | `1` | Yes |
| Q2 | `13` / `17` | `13` / `17` | Yes |
| Q3 | `5` / `9` | `5` / `9` | Yes |
| Q4 | `1 2 1 3` | `1 2 1 3` | Yes |
| Q5 | `2` / `7` | `2` / `7` | Yes |
| Q6 | `3 3 3` | `3 3 3` | Yes |
| Q7 | `11` / `1` | `11` / `1` | Yes |
| Q8 | (b) `0 2` | (b) `0 2` | Yes |
| Q9 | (b) `42 undefined` | (b) `42 undefined` | Yes |
| Q10 | `0 2` | `0 2` | Yes |

### Part 1 Why audit

| Q# | Step-by-step audit against the code |
| --- | --- |
| Q1 | Steps 1–2 correctly identify the outer binding initialized to 1 and the definition scope of `show`. Steps 3–4 correctly isolate `run`’s local 2 and follow the actual log inside `show` to the outer 1. |
| Q2 | Steps 1–2 correctly bind and retain `base = 10`. Steps 3–4 get both additions right but claim “`f(3)` evaluates `10 + 3` and logs `13`” and that `f(7)` logs 17. Each call returns its sum. The two outer `console.log` calls print those sums. |
| Q3 | Steps 1–2 identify the mutable binding and its lexical capture. Steps 3–4 correctly update it to 5 and 9 but claim “`read()` reads the new value and logs `9`”, with the same error for 5. The body is `return n;`. Each caller logs the return value. |
| Q4 | Steps 1–2 correctly allocate two independent zero-initialized counters. Step 3 evaluates the arguments left to right. The first counter advances to 1 and 2, the second to 1, then the first to 3, before the single log call. |
| Q5 | Steps 1–2 correctly give the siblings one shared `total` initially holding 2. Steps 3–4 correctly trace the read, the addition of 5, and the new value 7, but claim “`get()` reads `total` and logs `2`” and “the second `get()` logs `7`”. The getter returns each value to an outer log call. |
| Q6 | Steps 1–2 correctly allocate one function-scoped `i` and retain it in three callbacks. Step 3 includes the increment from 2 to 3 and the failed condition. Step 4 reads that same final 3 in all three calls. |
| Q7 | Step 1 initializes outer `x` to 1. Step 2 initializes a distinct parameter from that value. Step 3 updates only the parameter to 11. Step 4 correctly locates both log operations and their order. |
| Q8 | Steps 1–2 initialize local `n` and store its current number 0 in the object’s data property. Step 3 correctly links both methods to the same binding. Step 4 applies both increments before evaluating the unchanged property and the getter, producing 0 and 2. |
| Q9 | Step 1 establishes the method receiver. Step 2 carries that receiver into the arrow. Step 3 handles both the bare strict-mode call and optional chaining on its undefined receiver. Step 4 prints the two returned values in order. |
| Q10 | Steps 1–2 distinguish the single outer `j` from the per-iteration `i` bindings. Step 3 follows the first pair of callbacks and the later assignments. Step 4 correctly omits a body execution when the condition fails at 3. Step 5 therefore reads 0 and 2. The separate Rule overstates this result with “Only a `let` declared inside the `for (...)` header creates a fresh binding per iteration”. A block-local `let` in the loop body is also freshly instantiated each time that block executes. |

For Check 3, the Part 2 runs yielded Q11 `10`, Q12 `7`, Q13 `false` / `true`, Q14 a `ReferenceError` before any log, Q15 `12 13 12`, Q16 `2 9`, Q17 `1`, Q18 `15 0` / `20 0`, Q19 `3`, and Q20 `undefined` / `2` / `1`. The quiz never issued an answer key for this part.

## Checks 8 and 11 measurements

For Check 8, a script extracted the four labeled field bodies, joined them with spaces, and counted whitespace-delimited tokens. The counts include numbered trace steps and inline code. Field labels, bullet markers, and the separate learner-specific marking line are excluded. Q1–10 in order measured **111, 102, 96, 124, 86, 128, 110, 119, 126, 147**. Including the four labels as five additional words per answer would put only Q10 over 150 and still meet the 90% threshold.

For Check 11, the script counted every physical line between each pair of fence delimiters, including internal blanks and excluding the delimiters. Q1–10 measured **12, 9, 10, 11, 11, 10, 9, 13, 10, 13**. Q11–20 measured **12, 8, 11, 8, 10, 8, 9, 11, 9, 10**.

## Check 10 distractor audit

| Q# | Wrong options and the beliefs that produce them |
| --- | --- |
| Q8 | (a) treats the data property as a live alias. (c) treats the returned methods as holding independent copies. (d) treats the data property as losing the local’s value when the factory returns, while the getter retains access. The key’s shorthand “`n` vanishes” needs that distinction to explain why the second value is still 2. |
| Q9 | (a) gives regular inner functions the enclosing method’s receiver. (c) reverses the arrow and regular-function rules. (d) treats both bare calls as losing the receiver. |
| Q11 | (b) looks up `k` in the callback’s caller and multiplies by 100. (c) treats an inaccessible outer value as `undefined` and multiplies by it. (d) treats passing the function to another scope as losing access to the name altogether. |
| Q14 | (a) falls through to outer `x`. (b) gives `let` the pre-initialization behavior of `var`. (c) treats the initializer as having run before the log. |
| Q17 | (b) lets `.call(b)` override the arrow’s receiver. (c) treats the returned arrow as having lost its receiver’s `v`. (d) treats an attempted receiver override on an arrow as an illegal call. |

## Check 15 learner diagnoses

| Q# | Reply and marking | Four-part answer and diagnosis |
| --- | --- | --- |
| Q1 | `2` → Wrong | Why traces both bindings, Answer gives 1, The trap identifies caller-scope lookup, and Rule gives definition-site lookup. The personal diagnosis ties the 2 specifically to `run`’s local `x`. |
| Q6 | `0 1 2` → Wrong | Why follows the shared `var` through the exit increment, Answer gives `3 3 3`, The trap names per-pass capture and the missed increment, and Rule states what callbacks read later. The personal diagnosis gives two plausible explanations for this particular reply, a fresh binding per pass or a snapshot on insertion. The submitted numbers cannot distinguish those beliefs. |
| Q8 | `a` → Wrong | Why separates the stored 0 from the twice-incremented binding, Answer gives (b) `0 2`, The trap identifies the live-property misconception, and Rule describes the one-time copy. The personal diagnosis connects the chosen `2 2` directly to reading `value: n` as an alias. |

**First fix.** Replace Q15 with a different operation on closure identity. For example, give two names to the same returned counter and a third name to a fresh counter. Ask which calls advance the same state. The learner must then distinguish aliasing an existing closure from invoking the factory again.

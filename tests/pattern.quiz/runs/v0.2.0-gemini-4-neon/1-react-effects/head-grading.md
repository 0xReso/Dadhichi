# Head review of Input 1 · React effects

Gemini 4 Neon generated this low-depth sheet from the frozen v0.2.0 prompt. I recorded all 30 predictions from the questions before opening the key. The table preserves that first pass, including my initial reading of “infinite” in Q23. The correctness review below also tests the key’s stronger “forever” claim.

## Independent results for checks 2 and 3

Arrows separate successive console calls. Snippet line numbers count from the first line of code.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| 1 | body → first → second. The body log sits between hook calls, both callbacks run after commit. | `body`, `first`, `second` | Yes |
| 2 | render 0 → click 0 → render 1. The handler keeps the snapshot from mount. | `render 0`, `click 0`, `render 1` | Yes |
| 3 | (a) E3 only. Changing b skips the [] and [a] setups. | (a) `E3` only | Yes |
| 4 | render 0 → render 1. The queue contains three replacements with 1. | `render 0`, `render 1` | Yes |
| 5 | render 5 → effect 5. Both clicks request the initial state and cause no further commit. | `render 5`, `effect 5` | Yes |
| 6 | render 0 → effect 0 → render 1 → cleanup 0 → effect 1. Cleanup belongs to the earlier setup. | `render 0`, `effect 0`, `render 1`, `cleanup 0`, `effect 1` | Yes |
| 7 | parent render → child render → child effect → parent effect. The child’s passive mount effect runs first. | `parent render`, `child render`, `child effect`, `parent effect` | Yes |
| 8 | (a) 3. From 0 the queue produces 5, 6, 2, 3. | (a) `3` | Yes |
| 9 | timer 0. The single timeout reads the mount render’s binding. | `timer 0` | Yes |
| 10 | (c) 3. Mount and two click renders each create a distinct cfg. | (c) 3 times (on mount and after every click) | Yes |
| 11 | (0,0,0) → (1,1,0) → (2,2,0). The ref persists, while x is initialized on each render. | `0 0 0`, `1 1 0`, `2 2 0` | Yes |
| 12 | (b) 2. The array now has three entries, but supplying the same reference leaves the DOM untouched. | (b) `2`, because `items` is the same array reference, so React bails out and skips re-rendering | Yes |
| 13 | main 1 → after 1 → early 2 → after 2. Both paths reach the hook before choosing their JSX. | `main 1`, `after 1`, `early 2`, `after 2` | Yes |
| 14 | app true → open → app false → close. Removing Box runs its cleanup. | `app true`, `open`, `app false`, `close` | Yes |
| 15 | (b) render 0 0 → render 1 1. createRoot batches both updates in the timeout. | (b) `render 0 0`, `render 1 1` | Yes |
| 16 | (c) render 0 → ref 1 → ref 2. The displayed number stays 0 because neither click requests a render. | (c) Logs `render 0`, `ref 1`, `ref 2`; button displays `0` | Yes |
| 17 | P-ren → C-ren → C-eff → P-eff. Updating the parent renders its ordinary child and both effects are due. | `P-ren`, `C-ren`, `C-eff`, `P-eff` | Yes |
| 18 | 1 with the original callback, 3 with an updater. Every original tick requests 1, whereas each updater increments the pending state. | (1) `1`; (2) `3` | Yes |
| 19 | The new logId on snippet line 3 changes the dependency on line 6. Either line is a defensible single-line attribution, and line 5 literally invokes the logger. | Line 3 (`const logId = () => console.log("id", id);`), because it creates a new function reference on every render, making `[logId]` change every time `App` re-renders. | Yes, as one defensible line. |
| 20 | (c) bye A. The previous cleanup runs with the binding from its setup. | (c) `bye A` | Yes |
| 21 | after 0. The resumed handler retains the click render’s n regardless of commit timing. | `after 0` | Yes |
| 22 | P-ren true → C-ren → P-eff true → P-ren false → C-clean → P-eff false. Deletion cleanup precedes the new parent setup. | `P-ren true`, `C-ren`, `P-eff true`, `P-ren false`, `C-clean`, `P-eff false` | Yes |
| 23 | (c) Both. A increments every time its effect runs, and B supplies a new object every time its dependency changes. | (c) Both `A` and `B` | Yes for the feedback cycle at mount. No for literal nontermination (see check 2). |
| 24 | eff 0 → clean 0 → eff 2. Two queued increments commit together. | `eff 0`, `clean 0`, `eff 2` | Yes |
| 25 | 0 2. The timeout reads its original n and the current field of the shared ref. | `0 2` | Yes |
| 26 | sub → unsub → sub with the local function, sub only with a hoisted function. Only the former changes dependency identity. | (1) `sub`, `unsub`, `sub`; (2) `sub` only | Yes |
| 27 | 2 total logs with the cloned object, 1 total with the original reference. The first click can bail out in the identity variant. | (1) 2 times; (2) React bails out because the returned reference matches `prev`, so no re-render runs and `"render"` is logged only 1 time (on mount). | Yes |
| 28 | (b) 0 1. The old setup saved 0, but the new render already wrote 1 to the shared ref. | (b) `0 1` | Yes |
| 29 | P-ren 0 → C-ren 0 → C-eff 0 → P-eff 0 → P-ren 1 → C-ren 1 → C-eff 1 → P-eff 1. The first parent effect schedules the update and both [n] values change. | `P-ren 0`, `C-ren 0`, `C-eff 0`, `P-eff 0`, `P-ren 1`, `C-ren 1`, `C-eff 1`, `P-eff 1` | Yes |
| 30 | show B only. A’s cleanup sets its own closed-over flag before either callback fires. | `show B` | Yes |

## Rubric decisions

**1 · Count.** The low-depth sheet has 30 consecutive question numbers, Q1–Q30, and a matching key entry for each. **Pass.**

**2 · Correct.** Q23 is the one result that changes on a literal reading. Both components immediately enter a feedback cycle, which is why my first pass selected (c). The key goes further in Q23, line 150 of `answers.md`: “Each run calls `setN(n + 1)` with a new number, scheduling another render and commit forever.” At `n = 2 ** 53`, JavaScript rounds `n + 1` back to `n`. React can skip the equal update, so A eventually settles. B keeps producing distinct objects. Only B satisfies the literal question, and option (b) gives the wrong reason for excluding A. This is a boundary calculation, not an observation from running the loop. [ECMAScript number precision](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-number.max_safe_integer) · [React 18 state equality](https://18.react.dev/reference/react/useState#setstate)

Q1 independently misses the trace requirement. Line 18 of `answers.md` says React “commits the `<p>hi</p>` output (applies it to the browser DOM) and paints. 4. Only then does React run the registered effects”. Commit precedes the callbacks. The browser controls paint, and React allows variation even for a non-interaction effect. The stated console order is correct. Q5’s specific idle-state bailout is also correct, though its general rule on line 45 promises a skipped component call more broadly than React does. With one incorrect literal outcome, the rubric gives this check a **Fail.** [React 18 effect timing](https://18.react.dev/reference/react/useEffect#caveats) · [React 18 state caveats](https://18.react.dev/reference/react/useState#setstate)

**3 · Determinate.** Q19 asks “Which line causes `"id A"` to be logged a second time, and why?” One learner can point to `const logId = () => console.log("id", id);` for creating the fresh function. Another can point to `}, [logId]);` for making that new identity trigger the effect. Both identify the cause, yet the key accepts a single line. Asking which dependency changes and why would give one target. Q23 asks “Which component(s) trigger an infinite render loop when mounted?” The ordinary React debugging sense gives (c). Literal nontermination gives only B, with no fully correct option including its reason. Both ambiguities persist with the opening settings fixed. Two affected questions. **Fail.**

**4 · Assumptions.** The opening specifies React 18 in a browser, `createRoot`, StrictMode off and standard browser events. This fixes the root behavior for timeout batching in Q15 and the extra development mount cycle for Q1. Q9, Q25 and Q30 specify when callbacks fire. Q21’s closed-over value is independent of whether the next commit precedes the resumed handler. **Pass.**

**5 · Prediction.** Q19 supplies the observed log and asks for a diagnosis. Each of the other 29 questions asks for observable behavior from supplied code, giving 29/30 (96.7%). **Pass.**

**6 · No trivia.** Each item asks the learner to apply behavior. Q15, for example, asks what renders when two setters run in a timeout. Knowing a release name alone cannot produce its log. **Pass.**

**7 · Trap named.** All 30 trap fields identify a specific mistaken belief. Q21 names the belief that awaiting a promise refreshes a closed-over variable. Q30 identifies the belief that both timers share one cleanup flag. Q8’s distractor arithmetic is scored under check 10. **Pass.**

**8 · Answer shape.** A Python scan split entries at numbered Markdown headings and found exactly `Why`, `Answer`, `The trap`, `Rule` in that order in every entry. Counting whitespace-separated tokens in the four field bodies, excluding headings, field labels and standalone numbered trace markers, gave these counts in question order:

| Questions | Words per answer |
| --- | --- |
| Q1–10 | 99, 104, 114, 112, 101, 119, 92, 128, 115, 133 |
| Q11–20 | 125, 114, 110, 90, 103, 113, 87, 119, 122, 107 |
| Q21–30 | 93, 104, 124, 125, 116, 125, 134, 125, 129, 151 |

29/30 (96.7%) meet the inclusive 60–150 range. Q30 is one token over by this convention, which counts whitespace-delimited code operators. The rubric requires 27/30. **Pass.**

**9 · Coverage.** The nine-entry map is at the head of the answer key. The opening keeps it hidden, and each mechanism has at least two real applications. For example, Q7 tests parent/child effect order on mount and Q22 tests a child’s cleanup against a parent’s new setup. Q7 and Q17 are close, but Q17 also requires deciding if the child with unchanged props participates in the update. Two map entries nevertheless point to questions that cannot test the advertised behavior. Line 13 lists “Q11, Q16, Q23, Q25, Q28” for `useRef`, yet both components in Q23 use only state and effects. Line 11 lists “Q7, Q17, Q22, Q26, Q29” for parent/child ordering, yet Q26 logs only the child’s effect and cleanup. Removing Q23 and Q26 from those respective entries preserves the coverage. **Borderline.**

**10 · Distractors.** I checked all nine four-option items (Q3, Q8, Q10, Q12, Q15, Q16, Q20, Q23, Q28). In Q8 the key says “(b) `7` ignores the updaters”. Crossing out the two updater calls leaves `setN(n + 5)` and `setN(n + 2)` with the same captured zero. Those queue 5 then 2, so someone with that belief gets **2**. Getting 7 additionally requires interpreting the direct replacements as cumulative increments. Changing option (b) to 2 would make the claimed diagnosis work. Q10’s “(b) misses mount or a click” also conflates a rule a learner might believe (effects first run on dependency changes) with simple miscounting. The option-to-belief mapping fails in Q8. **Fail.**

**11 · Artifact size and hints.** A Python count of physical lines between JSX fences, excluding both fence lines, found one artifact per question, 7–14 lines each. Q29 is longest at 14. The longest stem before its fence is Q18 at 39 whitespace-separated words. Q25 weakens the prediction with `const latest = useRef(n);` and `console.log(n, latest.current);` (question lines 408 and 412). The name tells the learner which operand to read as current, although they must still derive both numbers. Renaming it `r` preserves the trace and removes that clue. **Borderline.**

**12 · Progression.** The bands contain 6, 15 and 9 questions, exactly 20%, 50% and 30%. Q4 establishes how replacement updates use a snapshot. Q8 mixes replacements with updater functions. Q24 requires following two updaters through one commit, then tracing the old cleanup and the new setup. Q30 combines timer order and per-effect cleanup state. **Pass.**

**13 · Answers hidden.** The questions occupy their own file. Options carry no correctness marks, and the answer key and its mechanism map appear together in the separate answer file. Diagnostic Q19 supplies its symptom as the premise. **Pass.**

**14 · Honesty and source.** Input 1 supplies no source. All three hooks and the root API exist in the stated version. The errors in Q1 and Q23 concern interpretations of real behavior and are recorded under correctness. I found no invented API or unsupported dependency on an unspecified external system. **Pass.**

**15 · Diagnosis.** This is a sheet-mode run of Input 1. Only Input 9 elicits learner replies. **N/A.**

**16 · No copying.** The calibration has two effects in one component. The mount-only effect logs and schedules `setN(1)`, the other logs on `[n]`, and a body log exposes the two render passes. Q1 keeps two effect logs, a body log and the exact ordering task (“What gets logged on initial mount, and in what order?”). Its answer “`body`, `first`, `second`” can be read straight off the calibration’s first three events. Moving the body log between registrations does test inline execution more directly, and removing the setter, dependencies and entire second pass is a substantive simplification. This is a close reuse of the first half. Q29’s second render also comes from an effect, but it moves the observer into a child and requires child-before-parent effect order on both commits. The example cannot supply that trace. **Borderline (Q1).**

## Decision

**9 Pass, 3 Borderline, 3 Fail.** Check 15 is outside the denominator. The v0.1.0 directory contains a gate review only. The other graded React sheet uses the same v0.2.0 prompt, so it is a separate sample, not an earlier-version baseline. This run does not establish a promotion.

**Fix Q23 first.** Keep the intended choice “both” and make A alternate Boolean state with `setOn(value => !value)` after every commit. A test of feedback loops should turn on whether the effect keeps producing a different state. That change makes the trace and the selected answer agree under both readings of “infinite”.

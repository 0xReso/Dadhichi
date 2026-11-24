# Answer key

## Mechanisms tested

1. **Render body runs before effects (in declaration order):** Q1, Q13, Q22, Q29
2. **State variables hold the current render's snapshot:** Q2, Q21, Q25
3. **Dependency arrays compare values with `Object.is` (including reference identity):** Q3, Q10, Q19, Q23, Q26, Q29, Q30
4. **Automatic batching and updater functions:** Q4, Q8, Q15, Q24, Q27
5. **Same-value bailout (`Object.is`):** Q5, Q12, Q23, Q27
6. **Effect cleanup runs after the next commit and before the next effect:** Q6, Q14, Q20, Q22, Q24, Q26, Q28, Q30
7. **Parent–child render (top-down) and effect (bottom-up) order:** Q7, Q17, Q22, Q26, Q29
8. **Stale closures in effects and async callbacks:** Q9, Q18, Q25, Q30
9. **`useRef` persists without re-rendering (vs. local variables and state loops):** Q11, Q16, Q23, Q25, Q28

---

**1.**
Why: 1. On initial mount (the first time React inserts the component into the page), React runs `App()` from top to bottom. Both `useEffect` calls only register their callbacks; neither runs during render. 2. `console.log("body")` executes synchronously during render. 3. React commits the `<p>hi</p>` output (applies it to the browser DOM) and paints. 4. Only then does React run the registered effects in declaration order, logging `first` and then `second`.
Answer: `body`, `first`, `second`
The trap: answering `first`, `body`, `second`, from believing `useEffect` runs inline where it appears in the component body.
Rule: the entire component body runs during render, and registered effects run afterward in declaration order.

**2.**
Why: 1. On mount, `App()` runs with `n = 0` and logs `render 0`. 2. When clicked, `handleClick` calls `setN(1)`, which schedules a future re-render with `1` but does not change the current render's snapshot (the fixed values of state and props for that render). 3. The next line reads that snapshot and logs `click 0`. 4. React then re-renders `App()` with `n = 1` and logs `render 1`.
Answer: `render 0`, `click 0`, `render 1`
The trap: answering `render 0`, `click 1`, `render 1`, from believing `setN(1)` mutates `n` immediately on the spot.
Rule: calling a state setter schedules the next render and never changes the state variable in the current render.

**3.**
Why: 1. On mount, all three effects run once. 2. Clicking calls `setB(1)`, causing a re-render with `a = 0` and `b = 1`. 3. React checks each effect's dependency array (the second argument listing values to watch) using `Object.is`: `E1` has `[]` (mount only), so it skips; `E2` has `[a]` and `Object.is(0, 0)` is true, so it skips; `E3` has no dependency array, so it runs after every commit.
Answer: (a) `E3` only
The trap: (d) confuses omitting the dependency array with passing `[]`; (b) assumes `[a]` re-runs on any state change; (c) assumes every effect re-runs on every render.
Rule: `[]` runs only on mount, `[x]` re-runs only when `x` changes by `Object.is`, and no array runs after every commit.

**4.**
Why: 1. On mount, `App()` logs `render 0`. 2. Inside `handleClick`, `n` is fixed at `0`, so all three calls evaluate to `setN(1)`. 3. React uses batching (grouping multiple state updates from one event into a single re-render), so it queues `1`, replaces it with `1`, and replaces it with `1` again. 4. React performs one re-render with `n = 1` and logs `render 1`.
Answer: `render 0`, `render 1`
The trap: answering `render 0`, `render 3` (expecting each call to increment the previous one) or logging `render 1`, `render 2`, `render 3` (believing each `setN` renders immediately).
Rule: multiple state updates in one event batch into one re-render, and passing a direct value uses the same render's snapshot each time.

**5.**
Why: 1. On mount, `App()` logs `render 5`, commits, and runs the dependency-less effect, logging `effect 5`. 2. The first click calls `setN(5)`. Because `Object.is(5, 5)` is true and the component is idle at `5`, React performs a bailout (skipping the re-render because state did not change), so neither the body nor the effect runs. 3. The second click triggers the same bailout.
Answer: `render 5`, `effect 5`
The trap: logging `render 5`, `effect 5` three times, from believing every `setState` call forces a re-render even when the value is unchanged.
Rule: setting state to a value `Object.is`-equal to the current state bails out without re-rendering or running effects.

**6.**
Why: 1. On mount, `App()` logs `render 0`, commits, and runs the effect, logging `effect 0`. The returned cleanup (the function that tears down an effect) forms a closure (a function remembering variables from its creation scope) over `n = 0`. 2. Clicking calls `setN(1)`, so `App()` re-renders and logs `render 1`. 3. After commit, because `n` changed, React runs the previous cleanup (`cleanup 0`) before running the new effect (`effect 1`).
Answer: `render 0`, `effect 0`, `render 1`, `cleanup 0`, `effect 1`
The trap: placing `cleanup 0` before `render 1` (believing cleanup runs before the re-render starts) or omitting it (believing cleanup only runs on unmount).
Rule: when an effect re-runs, the previous render's cleanup runs after the new commit and right before the new effect.

**7.**
Why: 1. Rendering walks the component tree top-down: React calls `App()` first, logging `parent render` and returning `<Child />`. 2. React then calls `Child()`, logging `child render`. 3. After committing the whole tree to the DOM, React runs effects bottom-up (children before parents), logging `child effect` and then `parent effect`.
Answer: `parent render`, `child render`, `child effect`, `parent effect`
The trap: answering `parent render`, `child render`, `parent effect`, `child effect`, from assuming effects run in the same top-down order as renders.
Rule: components render top-down from parent to child, but their effects run bottom-up from child to parent after commit.

**8.**
Why: 1. Before the click, `n` is `0`, and all four calls batch into one update queue for the next render. 2. `setN(n + 5)` queues the direct value `5`. 3. `setN((x) => x + 1)` is an updater function, so it receives the queued `5` and produces `6`. 4. `setN(n + 2)` uses the render snapshot `n = 0`, overwriting the queue with `2`. 5. `setN((x) => x + 1)` receives `2` and produces `3`.
Answer: (a) `3`
The trap: (c) `9` adds `5 + 1 + 2 + 1`, assuming `n` updates after each call; (b) `7` ignores the updaters; (d) `1` assumes only the final line runs from `0`.
Rule: in a batched queue, a direct value replaces the queued state from the render snapshot, while an updater function computes from the previous queued result.

**9.**
Why: 1. On mount (`n = 0`), the `[]` effect runs once and starts a 1000 ms timer whose callback closes over `n = 0`. 2. The clicks at 200 ms and 400 ms re-render `App` with `n = 1` and `n = 2`, but because the dependency array is `[]`, the effect never cleans up or re-runs. 3. At 1000 ms, the original callback fires and reads its stale closure (a closure still holding an earlier render's state), logging `timer 0`.
Answer: `timer 0`
The trap: answering `timer 2`, from believing a timer callback reads the latest state value when it eventually runs.
Rule: a callback created inside an effect permanently reads the state snapshot from the render that created that effect.

**10.**
Why: 1. On mount, line 3 creates an object `{ limit: 10 }` and the effect runs once (log 1). 2. The first click calls `setN(1)`, re-rendering `App`. Line 3 creates a brand-new `{ limit: 10 }` object. React compares `[cfg]` with `Object.is`, which checks reference identity (whether two values are the exact same object in memory, not equal contents). Because it is a new object, the effect runs again (log 2). 3. The second click creates a third object, running the effect again (log 3).
Answer: (c) 3 times (on mount and after every click)
The trap: (a) assumes React deep-compares object contents in dependency arrays; (b) misses mount or a click; (d) assumes only state variables trigger effects.
Rule: dependency arrays compare objects by reference identity, so an object literal created during render counts as changed on every render.

**11.**
Why: 1. On mount, `n = 0`, `r.current = 0`, and `x = 0`, logging `0 0 0`. 2. First click mutates `r.current` to `1` and `x` to `1`, then calls `setN(1)`. 3. Render 2 runs with `n = 1`: `useRef` keeps the same mutable container (`r.current` is `1`), while `let x = 0` re-initializes from scratch (`x` is `0`), logging `1 1 0`. 4. Second click increments `r.current` to `2` and `x` to `1`; render 3 resets `x` to `0` and logs `2 2 0`.
Answer: `0 0 0`, `1 1 0`, `2 2 0`
The trap: answering `0 0 0`, `1 1 1`, `2 2 2` (expecting a local `let` variable to survive across renders) or resetting `r.current` to `0`.
Rule: local variables reset on every render, whereas `ref.current` persists across renders.

**12.**
Why: 1. `items.push(3)` mutates the existing array in place so its length becomes `3`, without creating a new array reference. 2. `setItems(items)` passes that same array reference back to React. 3. React compares the current and next state with `Object.is(items, items)`, gets `true`, and bails out without re-rendering. 4. Because no re-render runs, the button keeps displaying the previous render's `2`.
Answer: (b) `2`, because `items` is the same array reference, so React bails out and skips re-rendering
The trap: (a) assumes any `setItems` call triggers a re-render; (c) and (d) assume React freezes state or throws on mutation at runtime.
Rule: mutating an object or array in place keeps the same reference, so `setState` bails out unless you pass a new copy.

**13.**
Why: 1. On mount (`step = 1`), `useEffect` registers its callback, the `if` branch is skipped, `main 1` logs, and `<button>` renders. After commit, the effect logs `after 1`. 2. Clicking calls `setStep(2)`. 3. On render 2 (`step = 2`), `useEffect` registers again before the `if`; the `if` branch logs `early 2` and returns `<p>done</p>`. 4. After commit, because `step` changed, the registered effect still runs and logs `after 2`.
Answer: `main 1`, `after 1`, `early 2`, `after 2`
The trap: omitting `after 2` (believing an early `return` skips effects registered above it) or putting `after 2` before `early 2`.
Rule: any effect registered before an early return still runs after the render commits, never before the body finishes.

**14.**
Why: 1. On mount, `App` logs `app true` and renders `Box`. After commit, `Box`'s `[]` effect logs `open` and registers a cleanup. 2. Clicking calls `setShow(false)`. 3. `App` re-renders, logs `app false`, and omits `<Box />`. 4. React commits the removal (unmounting `Box` from the page) and runs `Box`'s cleanup, logging `close`.
Answer: `app true`, `open`, `app false`, `close`
The trap: omitting `close` (thinking `[]` prevents cleanup from running) or logging `close` before `app false` (thinking unmount happens before the parent re-renders).
Rule: an effect's cleanup always runs when its component unmounts, after the parent commit that removes it.

**15.**
Why: 1. On mount, `App` logs `render 0 0`. 2. Clicking schedules the timeout without updating state yet. 3. After 100 ms, the callback calls `setA(1)` and `setB(1)`. In React 18 (`createRoot`), automatic batching applies inside `setTimeout`, promises, and native listeners as well as React events, merging both updates into one re-render. 4. React re-renders once and logs `render 1 1`.
Answer: (b) `render 0 0`, `render 1 1`
The trap: (a) applies React 17's old rule that `setTimeout` skips batching; (c) reverses update order; (d) assumes timers cannot trigger React renders.
Rule: in React 18, state updates made in the same timer or async callback are automatically batched into one re-render.

**16.**
Why: 1. On mount, `App` logs `render 0` and displays `0`. 2. First click increments `count.current` synchronously to `1` and logs `ref 1`. Mutating a ref never schedules a re-render, so `App` does not run again and the button stays `0`. 3. Second click increments `count.current` to `2` and logs `ref 2`; again no re-render runs, so the button still shows `0`.
Answer: (c) Logs `render 0`, `ref 1`, `ref 2`; button displays `0`
The trap: (a) assumes changing `ref.current` triggers a re-render like `useState`; (b) assumes the DOM updates automatically without a re-render; (d) treats `ref.current` like a frozen state snapshot.
Rule: mutating `ref.current` updates the value immediately, but never triggers a re-render or updates the screen on its own.

**17.**
Why: 1. Clicking calls `setN(1)` on `App`. 2. `App` re-renders first (top-down), logging `P-ren`. 3. Because `Child` is not wrapped in `React.memo`, rendering `App` automatically re-renders `Child`, logging `C-ren` even though `Child` takes no props. 4. After commit, both effects lack dependency arrays, so both run bottom-up: `C-eff`, then `P-eff`.
Answer: `P-ren`, `C-ren`, `C-eff`, `P-eff`
The trap: omitting `C-ren` and `C-eff` (believing a child with no props skips re-rendering when its parent updates) or reversing `C-eff` and `P-eff`.
Rule: a parent re-render re-renders its children top-down by default, and their effects still run bottom-up after commit.

**18.**
Why: 1. On mount (`n = 0`), the `[]` effect starts an interval whose callback closes over `n = 0`. 2. Tick 1 calls `setN(0 + 1)` (`n` becomes `1`). Because deps are `[]`, the effect does not restart. 3. Ticks 2 and 3 still read the stale `n = 0` and call `setN(1)`, leaving `<p>` stuck at `1`. 4. With `setN((x) => x + 1)`, React passes the latest state each tick (`0 -> 1 -> 2 -> 3`), so `<p>` displays `3`.
Answer: (1) `1`; (2) `3`
The trap: answering `3` for (1), from assuming the interval callback reads the updated `n` on each tick.
Rule: inside a long-lived `[]` effect, use an updater function (`x => ...`) instead of reading a stale state variable directly.

**19.**
Why: 1. On mount, line 3 creates `logId`, and the effect runs and logs `id A`. 2. Clicking calls `setN(1)`, re-rendering `App` with the same `id = "A"`. 3. Line 3 creates a brand-new function object for `logId`. 4. React checks `[logId]` with `Object.is`: the old and new functions have different references, so the effect re-runs and logs `id A` again.
Answer: Line 3 (`const logId = () => console.log("id", id);`), because it creates a new function reference on every render, making `[logId]` change every time `App` re-renders.
The trap: blaming `id` or thinking two functions with identical code are equal in a dependency array.
Rule: functions declared inside a component get a new reference on every render, so listing them in a dependency array re-triggers the effect on every render.

**20.**
Why: 1. On mount (`id = "A"`), the effect registers a cleanup function that closes over `id = "A"` and logs nothing yet. 2. Clicking calls `setId("B")`, triggering a re-render with `id = "B"`. 3. After commit, because `id` changed, React runs the previous render's cleanup, which logs its captured value: `bye A`. 4. The new effect then registers a cleanup for `"B"`, which does not run yet.
Answer: (c) `bye A`
The trap: (b) assumes cleanup sees the new render's `id`; (a) believes cleanup runs only on unmount; (d) believes both cleanups run on update.
Rule: an effect's cleanup always sees the props and state from the render that created it, not the new render.

**21.**
Why: 1. On mount, `handleClick` is created inside render 1 and closes over `n = 0`. 2. Clicking calls `setN(0 + 1)`, scheduling render 2 with `n = 1`. 3. `await Promise.resolve()` pauses `handleClick`, and even if render 2 runs in the meantime, `const n` inside render 1's closure never changes. 4. When `handleClick` resumes after `await`, it logs `after 0`.
Answer: `after 0`
The trap: answering `after 1`, from believing `await` lets the re-render finish and updates `n` inside the paused function.
Rule: waiting across an `await` never updates a closed-over state variable; each render's function keeps its original snapshot forever.

**22.**
Why: 1. Mount renders top-down (`P-ren true`, `C-ren`), commits, and runs effects bottom-up (`Child` registers its cleanup; `App` logs `P-eff true`). 2. Clicking calls `setOn(false)`. 3. `App` re-renders (`P-ren false`) and omits `<Child />`. 4. After commit removes `Child`, React runs all passive cleanups for the commit before any new effects: `Child`'s cleanup logs `C-clean`, then `App`'s `[on]` effect logs `P-eff false`.
Answer: `P-ren true`, `C-ren`, `P-eff true`, `P-ren false`, `C-clean`, `P-eff false`
The trap: putting `C-clean` after `P-eff false` (missing that cleanups run before new effects) or before `P-ren false` (thinking unmount precedes render).
Rule: after a commit, React runs all pending effect cleanups across the tree before running any new effects.

**23.**
Why: 1. In `A`, the effect has no dependency array, so it runs after every commit. Each run calls `setN(n + 1)` with a new number, scheduling another render and commit forever. 2. In `B`, the mount effect calls `setObj({ v: 1 })`. That literal is a brand-new object reference, so `Object.is` is false: React does not bail out, re-renders `B`, sees a changed `[obj]` reference, and runs the effect again forever.
Answer: (c) Both `A` and `B`
The trap: (a) assumes `{ v: 1 }` matches the previous `{ v: 1 }` by value; (b) confuses omitting the dependency array with `[]`; (d) assumes React stops effects from looping.
Rule: setting state to a fresh object literal defeats both state bailout and dependency checks, looping just like an unbounded effect.

**24.**
Why: 1. On mount (`n = 0`), the effect logs `eff 0` and registers a cleanup closing over `n = 0`. 2. Clicking `bump` queues two updater functions, `x => x + 1` and `x => x + 1`. React batches both into a single re-render: `0 -> 1 -> 2`, never rendering `n = 1`. 3. After render 2 commits with `n = 2`, React runs the old cleanup (`clean 0`) and then the new effect (`eff 2`).
Answer: `eff 0`, `clean 0`, `eff 2`
The trap: answering `eff 0`, `clean 0`, `eff 1`, `clean 1`, `eff 2` (expecting each updater to render and run effects separately) or stopping at `eff 1`.
Rule: batched updaters produce one commit, so effects and cleanups only see the final batched state, never intermediate queued values.

**25.**
Why: 1. On mount (`n = 0`), line 4 sets `latest.current = 0`, and the `[]` effect starts a 500 ms timer closing over `n = 0` and the `latest` ref object. 2. At 100 ms and 200 ms, clicks re-render `App` with `n = 1` and `n = 2`, updating `latest.current` to `2` while the `[]` effect stays put. 3. At 500 ms, the timer logs the stale snapshot `n` (`0`) alongside the mutated `latest.current` (`2`).
Answer: `0 2`
The trap: answering `0 0` (treating `latest.current` like a frozen render snapshot) or `2 2` (thinking `n` also updates inside the closure).
Rule: a ref is a single mutable object shared across renders, so reading `ref.current` inside a stale closure returns the latest value.

**26.**
Why: 1. On mount, `App` creates `ping` and renders `Child`; after commit, `Child`'s effect logs `sub`. 2. Clicking calls `setN(1)`, re-rendering `App`. Line 10 creates a brand-new `ping` function reference and passes it to `Child`. 3. After commit, `Object.is(oldPing, newPing)` is false, so `Child` runs its cleanup (`unsub`) and re-runs its effect (`sub`). 4. Moving `ping` outside `App` keeps one fixed reference across renders, so `[onPing]` never changes on click and only `sub` logs.
Answer: (1) `sub`, `unsub`, `sub`; (2) `sub` only
The trap: predicting `sub` only for (1), from forgetting that a parent re-render recreates inline callback props and re-triggers child effects that depend on them.
Rule: recreating a callback prop during a parent re-render gives it a new reference, causing a child effect that depends on it to clean up and re-run.

**27.**
Why: 1. On mount, `App` logs `render` (total: 1). 2. Clicking calls `setUser((prev) => ({ name: prev.name }))`, which returns a brand-new object reference. Because `Object.is` is false even though `name` is still `"Ada"`, React does not bail out and re-renders `App`, logging `render` again (total: 2). 3. Replacing line 5 with `setUser((prev) => prev)` returns the exact same reference; `Object.is(prev, prev)` is true, so React bails out and `"render"` stays at 1.
Answer: (1) 2 times; (2) React bails out because the returned reference matches `prev`, so no re-render runs and `"render"` is logged only 1 time (on mount).
The trap: answering 1 time for (1), from assuming React compares state objects by their property values rather than reference identity.
Rule: an updater function triggers a re-render whenever it returns a new object reference, and bails out when it returns `prev` itself.

**28.**
Why: 1. On mount (`n = 0`), line 4 sets `r.current = 0`. After commit, the effect copies `snap = 0` and registers a cleanup closing over `snap` and the ref object `r`. 2. Clicking calls `setN(1)`, starting render 2 (`n = 1`). 3. During render 2, line 4 mutates `r.current = 1` before commit and before render 1's cleanup runs. 4. After commit, render 1's cleanup runs and logs `snap` (`0`) and the already-updated `r.current` (`1`).
Answer: (b) `0 1`
The trap: (a) `0 0` assumes cleanup runs before render 2 starts; (c) `1 1` assumes cleanup reads render 2's `snap`; (d) reverses which value is snapshotted.
Rule: because cleanup runs after the next render executes, reading a ref mutated during render inside cleanup gives the new render's value, not the old one.

**29.**
Why: 1. Render 1 runs top-down: `App` logs `P-ren 0`, then `Child` logs `C-ren 0`. 2. After commit 1, effects run bottom-up: `Child` logs `C-eff 0`, then `App` logs `P-eff 0` and calls `setN(1)`. 3. Render 2 runs top-down: `App` logs `P-ren 1`, then `Child` logs `C-ren 1`. 4. After commit 2, `n` changed `0 -> 1`, so both `[n]` effects run bottom-up: `C-eff 1`, then `P-eff 1` (the `if` is false, so updates stop).
Answer: `P-ren 0`, `C-ren 0`, `C-eff 0`, `P-eff 0`, `P-ren 1`, `C-ren 1`, `C-eff 1`, `P-eff 1`
The trap: logging `P-eff 0` before `C-eff 0` (expecting effects to run top-down like renders), or thinking render 2 skips `C-eff 1`.
Rule: every render cycle runs top-down through the tree and then flushes its effects bottom-up before any state update from those effects renders next.

**30.**
Why: 1. At t = 0 ms (`id = "A"`), the effect creates its own local `ignore = false`, schedules a 500 ms timer, and returns a cleanup that sets A's `ignore = true`. 2. At t = 50 ms, clicking calls `setId("B")`. 3. After commit, A's cleanup runs and flips A's `ignore` to `true`, then B's effect runs with a fresh, separate `ignore = false` and schedules a 100 ms timer (fires at 150 ms). 4. At 150 ms, B's timer sees B's `ignore === false` and logs `show B`. 5. At 500 ms, A's timer sees A's `ignore === true` and logs nothing.
Answer: `show B`
The trap: answering `show B`, `show A` (forgetting cleanup flips A's flag) or logging nothing (thinking A's cleanup sets a shared `ignore` flag that also blocks B).
Rule: each effect run has its own closure, so a cleanup flipping a local flag cancels only its own in-flight work without affecting the next run.

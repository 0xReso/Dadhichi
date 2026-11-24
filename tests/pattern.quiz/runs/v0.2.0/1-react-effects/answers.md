# Answer key

Assumptions as in the questions: React 18 in the browser, `createRoot`, StrictMode off.

## Mechanisms and the questions that test them

1. **The body renders first, effects run afterwards.** Calling `useEffect` only registers a function; React runs it after the render has been committed to the screen. Q1, Q11, Q23, Q30
2. **The dependency list decides whether an effect re-runs.** No list means after every render, `[]` means only after mounting, and `[x]` means only when `x` differs from last render's `x`. Q2, Q12, Q20, Q24
3. **Cleanup runs before the next run of the same effect and on unmount, and it sees the values of the render it came from.** Q5, Q14, Q21, Q22, Q24, Q30
4. **State is a snapshot per render.** Calling a setter schedules a new render; it never changes the variable the current code is reading. Q3, Q11, Q18, Q23, Q29
5. **Updates are batched.** React 18 groups every state update made in the same event or the same timer callback into one re-render, after that code finishes. Q7, Q18, Q25
6. **An updater function receives the latest queued value; a plain value replaces it.** Q4, Q13, Q25, Q29
7. **Dependencies are compared by identity.** An object, array or function created during render is a new value every render, even with identical contents. Q8, Q16, Q20
8. **A closure keeps the values of the render that created it, while a ref is one live box shared by every render.** Q9, Q17, Q26, Q27
9. **Parents render before children, children's effects run before parents', and a parent's re-render re-renders its children.** Q6, Q15, Q23, Q28
10. **`useLayoutEffect` runs after React updates the page but before the browser paints, and before any `useEffect`.** Q10, Q19, Q28, Q30

---

**Q1**
Why: 1. React calls `Box`, which logs `render`. 2. `useEffect(...)` is called next, but calling it only hands React a function to run later; nothing inside it runs yet. 3. The body continues and logs `after hook call`. 4. React commits the result (puts the `<div>` on the page), and only then runs the effect, which logs `effect`.
Answer: `render`, `after hook call`, `effect`
The trap: `render`, `effect`, `after hook call`, from the belief that `useEffect` runs its function at the line where it is called, like an ordinary function call.
Rule: the hook call registers the effect; the effect itself runs after the whole body has finished and the render is on the page.

**Q2**
Why: 1. On mount every effect runs once: `A`, `B`, `C`. 2. Each click changes `m`, so `C` re-renders twice. 3. `A` has no dependency list (the array after the effect function), so it runs after every render: two more times. 4. `B` has `[]`, an empty list that never changes, so it never runs again. 5. `C` depends on `n`, which is never changed, so it never runs again either.
Answer: `A` 3 times, `B` 1 time, `C` 1 time.
The trap: `C` 3 times, from the belief that any re-render re-runs every effect that has dependencies. React re-runs it only when a listed value changed.
Rule: no list runs after every render, `[]` runs once on mount, and `[x]` runs when `x` changes.

**Q3**
Why: 1. Mount: the body logs `render 0`. 2. The click runs `handle`, which belongs to the render where `n` is 0. 3. `setN(5)` asks React for a new render with 5; it does not touch the `n` this function is reading. 4. `console.log("handler", n)` therefore logs `handler 0`. 5. After the handler finishes, React re-renders, and the new call of `C` has `n = 5`, logging `render 5`.
Answer: `render 0`, `handler 0`, `render 5`
The trap: `handler 5`, from the belief that a setter updates the variable immediately, like an assignment.
Rule: each render has its own constant state; a setter only schedules the next render.

**Q4**
Why: 1. In this render `n` is 0, so both `setN(n + 1)` calls are really `setN(1)`. 2. React queues the three updates and processes them in order on the next render. 3. Start at 0; the first update sets 1; the second sets 1 again. 4. The third is an updater function (a function that receives the latest queued value and returns the next one): it receives 1 and returns 2.
Answer: `2`
The trap: `3`, from the belief that each `setN(n + 1)` sees the previous one's result. They all read the same snapshot of `n`. Answering `1` comes from thinking the updater also reads the snapshot.
Rule: `setN(n + 1)` uses this render's `n`; `setN(p => p + 1)` uses the latest queued value.

**Q5**
Why: 1. First render with `id` 1: after commit the effect logs `start 1` and returns a cleanup function, which closes over `id = 1`. 2. Re-render with `id` 2: the dependency changed, so React first calls the previous cleanup, which logs `stop 1`. 3. Then the new effect runs and logs `start 2`; its cleanup closes over `id = 2`. 4. When `C` is removed (unmounted), React calls the latest cleanup: `stop 2`.
Answer: `start 1`, `stop 1`, `start 2`, `stop 2`
The trap: `stop 2` as the second line, from the belief that cleanup reads the current props. It is a function from the earlier render and sees that render's `id`.
Rule: cleanup runs before the effect re-runs and on unmount, using the values of the render that created it.

**Q6**
Why: 1. React calls `Parent` first, because it needs Parent's output to know what children to render: `parent render`. 2. It then calls `Child`: `child render`. 3. After the whole tree is committed, effects run from the inside out, child before parent, so a parent's effect can rely on its children being fully set up: `child effect`, then `parent effect`.
Answer: `parent render`, `child render`, `child effect`, `parent effect`
The trap: `parent effect` before `child effect`, from the belief that effects run in the same top-down order as rendering.
Rule: rendering goes top-down, effects go bottom-up.

**Q7**
Why: 1. Mount logs `render 0 0`. 2. The click only starts a timer; no state changes. 3. When the timer fires, `setA(1)` and `setB(1)` run in the same callback. 4. React 18 with `createRoot` batches them: it groups both updates and renders once after the callback finishes. Batching means collecting several updates into one re-render. 5. That one render logs `render 1 1`.
Answer: `render 0 0`, `render 1 1`
The trap: `render 0 0`, `render 1 0`, `render 1 1`, from the belief that batching happens only inside React event handlers. That was true in React 17; React 18 batches timers, promises and native events too.
Rule: in React 18, all updates made in the same synchronous block become one render.

**Q8**
Why: 1. Every call of `C` runs `const options = { size: 10 }`, which builds a brand-new object. 2. React compares each dependency with `Object.is`, which for objects asks "is this the same object?", not "are the contents equal?". 3. Mount: the effect runs (1). 4. Each of the three clicks re-renders, creating a new `options` that is not the previous object, so the effect runs again (2, 3, 4).
Answer: `4` times
The trap: `1`, from the belief that React compares dependencies by their contents, so `{ size: 10 }` counts as unchanged.
Rule: an object or array created during render is a new dependency every render.

**Q9**
Why: 1. The effect runs once, on mount, because of `[]`. 2. The interval callback is a closure, a function that remembers the variables around it when it was created; here that is `n = 0` from the first render. 3. Tick 1: `setN(0 + 1)`, the screen shows 1. 4. Ticks 2 to 5 run the same old callback, which still sees `n = 0` and sets 1 again. 5. Setting the same value changes nothing on screen.
Answer: `1`
The trap: `5`, from the belief that the callback reads the current `n` on every tick.
Rule: a function created in an effect sees only the render it was created in; use `setN(p => p + 1)` to depend on the latest value.

**Q10**
Why: 1. The body runs both hook calls (registering the effects) and logs `render`. 2. React updates the page. 3. Before the browser paints, React runs layout effects: `layout`. A layout effect is one run with `useLayoutEffect`, designed for measuring or adjusting the page before the user sees it. 4. After paint, React runs ordinary effects: `effect`.
Answer: `render`, `layout`, `effect`
The trap: `render`, `effect`, `layout`, from the belief that effects run in the order they are written regardless of type. Declaration order only applies within the same kind.
Rule: layout effects run before paint, ordinary effects after, whatever order they appear in.

**Q11**
Why: 1. First render logs `render 0`. 2. After commit the effect runs in the first render's world, where `n` is 0. 3. `setN(0 + 1)` schedules a render with 1 but does not change this `n`. 4. The effect logs `effect 0`. 5. The new render logs `render 1`. 6. The effect has `[]`, so it does not run again.
Answer: `render 0`, `effect 0`, `render 1`
The trap: `effect 1`, from the belief that inside an effect the setter changes `n` straight away, because effects "run later".
Rule: effects run after the render, but they still read that render's frozen state.

**Q12**
Why: 1. Mount: the effect runs and logs `effect 0`. 2. Click 1: `setN(0)` asks for the same value; `setTick(1)` changes `tick`, so `C` re-renders. 3. In that render `n` is still 0; React compares the dependency `[0]` with the previous `[0]` and skips the effect. 4. Click 2 repeats this with `tick` becoming 2; `n` is still 0, so the effect is skipped again.
Answer: `effect 0` (logged once, on mount)
The trap: `effect 0` three times, from the belief that calling `setN` marks `n` as changed. React compares values, not calls.
Rule: an effect re-runs only if a dependency's value differs from last render's, however it got there.

**Q13**
Why: 1. React queues three updates and applies them in order to the latest value. 2. Start at 0; the updater `p => p + 1` gives 1. 3. The plain value `10` replaces it: 10. 4. The updater `p => p * 2` receives 10 and returns 20.
Answer: `20`
The trap: `10`, from the belief that a plain value overrides every queued update, including the ones after it. `2` comes from the belief that updaters skip over a plain value.
Rule: updates are applied in order; a plain value resets the running value and later updaters build on it.

**Q14**
Why: 1. Mount: the body logs `render 0`; after commit the effect logs `run 0`. 2. The click calls `setN(1)`. 3. React re-renders first: `render 1`. 4. Only after that render is committed does React clean up the previous effect, `clean 0`, and then run the new one, `run 1`.
Answer: `render 0`, `run 0`, `render 1`, `clean 0`, `run 1`
The trap: `clean 0` before `render 1`, from the belief that the old effect is cleaned up as soon as state changes. Cleanup happens after the new render, just before the new effect runs.
Rule: the order is new render, old cleanup, new effect.

**Q15**
Why: 1. The click sets `n` to 1 and `Parent` re-renders: `parent render 1`. 2. When a component re-renders, React also re-renders every child it returns, unless the child is wrapped to skip that (for example with `memo`). So `Child` runs: `child render`. 3. After commit, effects run child first: Child's effect has `[]`, so it is skipped. 4. Parent's effect depends on `n`, which changed: `parent effect 1`.
Answer: `parent render 1`, `child render`, `parent effect 1`
The trap: leaving out `child render`, from the belief that a child re-renders only when its props change. Adding `child effect` comes from thinking a re-render re-runs every effect.
Rule: a parent's render re-renders its children, but each child's effects still follow their own dependency lists.

**Q16**
Why: 1. First render with user object #1; the effect runs after commit. 2. `setUser({ name: "a" })` passes object #2. React checks with `Object.is` whether the state changed; #2 is a different object, so it re-renders. 3. In that render `user` is #2, which is not #1, so the dependency changed and the effect runs again, creating #3. 4. This repeats forever. In development React prints a "Maximum update depth exceeded" warning but does not stop the loop.
Answer: (c) It keeps rendering and re-running the effect without end.
The trap: (b), from the belief that React compares dependencies by contents. (a) comes from believing the state setter compares by contents; (d) from believing setting state inside an effect is forbidden.
Rule: a new object in state is a change, and a new object in a dependency list is a change, even with identical contents.

**Q17**
Why: 1. The effect runs once, on mount, because of `[]`. 2. It creates `onKey`, a closure over the first render's `n = 0`, and attaches it to `window`. 3. The three clicks re-render `C` with `n` 1, 2 and 3, but the effect never runs again, so the attached listener is still the first one. 4. The key press calls that original `onKey`.
Answer: `key 0`
The trap: `key 3`, from the belief that the listener reads the current state whenever it is called.
Rule: a listener attached by a `[]` effect is frozen at the first render; list the values it reads, or read them through a ref.

**Q18**
Why: 1. The click runs `handle`. 2. `setN(1)` and `setN(2)` are queued; because they are batched, nothing re-renders while the handler is still running. 3. A ref is a box whose `.current` React fills with the real DOM element. Here `ref.current.textContent` reads the paragraph as it is on the page right now, which still shows `0`. 4. After the handler returns, React renders once with the final value 2: `render 2`.
Answer: `0`, `render 2`
The trap: `render 1`, `render 2`, `2`, from the belief that each setter immediately re-renders and updates the page.
Rule: during an event handler neither the state variable nor the page has changed yet; one render follows when the handler finishes.

**Q19**
Why: 1. First render logs `render 0`, and React puts 0 into the page. 2. Before the browser paints, the layout effect runs and calls `setW(100)`. 3. An update made inside a layout effect is processed immediately, still before paint: React re-renders, logging `render 100`, and updates the page to 100. 4. Only then does the browser paint, so the first frame the user sees is 100.
Answer: (a) It logs `render 0`, `render 100`, and the browser never paints 0.
The trap: (b), from the belief that every effect runs after paint, as `useEffect` does. (c) comes from thinking the layout effect runs before rendering; (d) from thinking updates made in an effect are dropped.
Rule: state set in a layout effect is rendered before the browser paints, which is why it is used to avoid a visible flicker.

**Q20**
Why: 1. Each parent render writes `{ id: 1, name: "a" }`, a new object every time. 2. But the dependency list holds `user.id`, the number 1, not the object. 3. Numbers are compared by value: 1 is the same as 1. 4. So the effect runs on mount and is skipped on both re-renders.
Answer: `1` time
The trap: `3`, from carrying over "a new object re-runs the effect" without checking what is actually in the list.
Rule: React compares exactly what is in the dependency list; listing a primitive (number, string, boolean) instead of its object avoids identity changes.

**Q21**
Why: 1. `C` mounts and its `[]` effect logs `mount 0`. 2. Three clicks set `n` to 3; the effect does not re-run. 3. When the parent stops rendering `C`, React unmounts it: the cleanup logs `unmount`, and `C`'s state is thrown away. 4. Rendering `<C />` again mounts a brand-new instance, with `useState(0)` starting at 0, and its effect logs `mount 0`.
Answer: `mount 0`, `unmount`, `mount 0`; the button shows `0`.
The trap: `mount 3` and a final `3`, from the belief that state belongs to the component's code or position forever. It belongs to the mounted instance and disappears on unmount.
Rule: unmounting runs cleanup and discards state; mounting again starts from scratch and runs `[]` effects again.

**Q22**
Why: 1. The click sets `n` to 1, and `C` re-renders. 2. After commit, React handles ordinary effects in two passes. 3. First it runs every cleanup that is due, in the order the effects are written: `A clean 0`, `B clean 0`. 4. Then it runs every new effect, in the same order: `A run 1`, `B run 1`. Each cleanup reports 0 because it came from the earlier render.
Answer: `A clean 0`, `B clean 0`, `A run 1`, `B run 1`
The trap: `A clean 0`, `A run 1`, `B clean 0`, `B run 1`, from the belief that each effect is cleaned up and re-run as a pair before moving on.
Rule: all due cleanups run before any new effect runs.

**Q23**
Why: 1. Render top-down: `parent render false`, then `child render`. 2. Effects run child first. Child's effect calls `onReady()`, which calls `setReady(true)`; this only schedules a render. 3. Parent's effect runs next, still in the first render, where `ready` is false: `parent effect false`. 4. The scheduled render follows: `parent render true`. 5. Parent's re-render re-renders `Child`: `child render`. Child's effect has `[]`, so it is skipped. 6. Parent's effect has no list, so it runs: `parent effect true`.
Answer: `parent render false`, `child render`, `parent effect false`, `parent render true`, `child render`, `parent effect true`
The trap: `parent effect true` as the third line, from the belief that the child's update is visible to the parent's effect in the same pass. The parent's effect belongs to the first render and reads its snapshot.
Rule: an update made in one effect is seen only by the next render, never by other effects of the current one.

**Q24**
Why: 1. Mount with `n = 0`: the effect calls `setInterval` (call 1). 2. Tick sets `n` to 1. The dependency changed, so React runs the cleanup, clearing interval 1, then the new effect, which starts interval 2 (call 2). 3. The tick that sets `n` to 2 does the same: clear 2, start 3 (call 3). 4. The tick that sets 3: clear 3, start 4 (call 4). Each interval reads a fresh `n`, so the count is correct.
Answer: `setInterval` has been called 4 times; 1 interval is active.
The trap: answering 1 call, from the belief that the effect sets up one interval and keeps it, or 4 active intervals, from forgetting that cleanup runs before each re-run.
Rule: an effect that lists a value it reads is torn down and rebuilt every time that value changes.

**Q25**
Why: 1. The click queues two updaters. 2. React cannot know the final value without applying them, so it renders `C`: start at 0, `+1` gives 1, `-1` gives 0. 3. The body runs with `n = 0` and logs `render 0`. 4. React sees the new state equals the old state and throws away the result without committing anything new (a "bailout"). 5. The effect's dependency is still 0, so the effect does not run.
Answer: `render 0`
The trap: "nothing", from the belief that React checks whether the final value changed before calling the component. It finds out only by rendering. Answering `render 1`, `render 0` comes from thinking each updater triggers its own render.
Rule: a batch of updates is rendered once, and its effects depend on the final value, not on how many updates there were.

**Q26**
Why: 1. The `[]` effect runs once on mount. It creates a timeout callback that closes over the first render's `n = 0` and over `ref`, the one box shared by every render. 2. Two clicks: `n` becomes 1 then 2 in later renders, but the callback still sees its own `n = 0`. 3. The same clicks add 1 to `ref.current` twice, mutating the shared box to 2. 4. At 3 seconds the callback reads its frozen `n` and the box's current value.
Answer: `0 2`
The trap: `2 2`, from the belief that a timeout reads the latest state. `0 0` comes from thinking a ref is frozen like state.
Rule: state seen by a closure is frozen at its render; a ref is read live at the moment you access it.

**Q27**
Why: 1. Mount: the paragraph shows `0 0`. 2. Clicking "a" changes `r.current`, but changing a ref never asks React to re-render, so the page is not updated. After three clicks `r.current` is 3, yet the paragraph still shows `0 0`. 3. Clicking "b" calls `setN(1)`, which re-renders `C`. 4. That render reads `r.current` (3) and `n` (1).
Answer: `0 0` after the third "a"; `3 1` after "b".
The trap: `3 0` after the third "a", from the belief that the page tracks any value used in the markup. React updates the page only when it renders.
Rule: mutating a ref changes the value but does not re-render; the screen catches up at the next render.

**Q28**
Why: 1. Both components render, parent then child. 2. React updates the page. 3. Before paint, layout effects run, children first: `child layout`, `parent layout`. 4. After paint, ordinary effects run, children first: `child effect`, `parent effect`.
Answer: `child layout`, `parent layout`, `child effect`, `parent effect`
The trap: `child layout`, `child effect`, `parent layout`, `parent effect`, from the belief that React finishes one component's effects before moving on. React finishes all layout effects across the tree before any ordinary effect.
Rule: all layout effects, bottom-up, then all ordinary effects, bottom-up.

**Q29**
Why: 1. Mount: `render 0`. 2. The click runs `handle` from the render where `n` is 0. `setN(1)` is queued, and a timeout is created as a closure over `n = 0`. 3. The handler ends and React renders: `render 1`. 4. One second later the timeout logs its own `n`: `later 0`. 5. It then calls `setN(p => p + 1)`, which receives the latest value 1 and returns 2. 6. React renders: `render 2`.
Answer: `render 0`, `render 1`, `later 0`, `render 2`
The trap: `later 1`, from the belief that by the time the timeout runs, `n` has been updated. The timeout reads the snapshot from its render; only the updater sees the latest value.
Rule: a closure reads its render's state, but an updater function always receives the latest state.

**Q30**
Why: 1. Render 0 logs `render 0`. Before paint, `layout 0`. After paint, `effect 0`, which sets 1. 2. Render 1 logs `render 1`. Before paint, `layout 1`. After paint, the old cleanup, `clean 0`, then `effect 1`, which sets 2. 3. Render 2 logs `render 2`. Before paint, `layout 2`. After paint, `clean 1`, then `effect 2`. Since `n < 2` is false, nothing is set and the chain stops. The last cleanup waits until unmount.
Answer: `render 0`, `layout 0`, `effect 0`, `render 1`, `layout 1`, `clean 0`, `effect 1`, `render 2`, `layout 2`, `clean 1`, `effect 2`
The trap: putting `clean 0` before `render 1` or before `layout 1`, from the belief that the old effect is cleaned up as soon as the state changes. It is cleaned up after the new render and the new layout effects.
Rule: each render runs body, then layout effects, then old cleanups, then new effects.

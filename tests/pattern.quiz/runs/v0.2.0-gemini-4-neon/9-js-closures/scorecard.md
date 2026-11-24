### Scorecard — JavaScript Closures (Questions 1–10 of 30)

**Overall score:** 7 / 10 (stopped after Part 1)

#### Mechanisms & Results

1. **Lexical scoping (definition-site lookup, not call-site)** — Q1: **0 / 1**
2. **Outer scope retention after the outer function returns** — Q2: **1 / 1**
3. **Live binding capture (variable binding, not creation-time snapshot)** — Q3: **1 / 1**
4. **Independent environment per outer function invocation** — Q4: **1 / 1**
5. **Sibling closures sharing one environment** — Q5: **1 / 1**
6. **Loop bindings (`var` shared binding vs `let` per-iteration binding in a `for` header)** — Q6, Q10: **1 / 2**
7. **Shadowing by inner parameters or declarations** — Q7: **1 / 1**
8. **Value snapshots vs live bindings and object references** — Q8: **0 / 1**
9. **Lexical `this` in arrow functions vs dynamic `this` in regular functions** — Q9: **1 / 1**

#### Focus Areas from Missed Questions

- **Mechanism 1 (Q1):** Expected `show()` to read `x` from its caller (`run()`). Remember that variable lookup follows where a function was *defined*, not where it is called.
- **Mechanism 6 (Q6):** Expected `for (var i = ...)` to give each closure its own value (`0 1 2`). You nailed the `for (let i = ...)` vs outer `let j` distinction in Q10 (`0 2`), so the one rule to lock in is that `var` in a `for` header behaves like a single outer variable shared across all iterations.
- **Mechanism 8 (Q8):** Treated `{ value: n }` as a live reference synced with `n`. Plain properties copy primitive values once when the object is built; only functions closing over `n` read later updates.

If you'd like to revisit these three mechanisms with a quick review question or pick back up at Part 2 later, just let me know.

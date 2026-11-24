### Part 1 Answers & Review (Questions 1–10)

**1.**
- **Why:** 1. Top-level `const x = 1` creates an outer binding `x` holding `1`. 2. `show` is defined in that top-level scope, so under **lexical scoping** (looking up variables based on where a function is written in the source code, not where it is called), `show`'s outer scope is the top level. 3. Calling `run()` creates a separate local `const x = 2` and invokes `show()`. 4. `show` resolves `x` in its definition-site scope and logs `1`.
- **Answer:** `1`
- **The trap:** Answering `2`, from believing a function looks up outer variables in the scope of whatever called it.
- **Rule:** A function resolves outer variables in the scope where it was defined, never where it was called.
- **Your answer (`2`):** **Wrong.** Your answer reflects a dynamic-scoping model—expecting `show()` to read `run()`'s local `x = 2` because `run()` was the caller.

**2.**
- **Why:** 1. `make(10)` runs with parameter `base` set to `10` and returns the inner function. 2. Because the inner function references `base`, it forms a **closure** (a function paired with a live link to its enclosing scope), keeping `base = 10` alive even after `make` finishes. 3. `f(3)` evaluates `10 + 3` and logs `13`. 4. `f(7)` evaluates `10 + 7`—since `base` was never modified—and logs `17`.
- **Answer:** `13`, `17`
- **The trap:** Expecting `NaN` or an error (thinking `base` disappears once `make` returns), or `13`, `20` (thinking `base` accumulates the result).
- **Rule:** A returned inner function keeps the outer function's variables alive after the outer function finishes.
- **Your answer (`13, 17`):** **Right.**

**3.**
- **Why:** 1. `let n = 1` creates a mutable variable binding `n`. 2. Defining `read` captures the binding `n` itself, not a frozen copy of `1`. 3. `n = 5` updates that binding; `read()` reads its current value and logs `5`. 4. `n = 9` updates the same binding again; `read()` reads the new value and logs `9`.
- **Answer:** `5`, `9`
- **The trap:** Answering `1`, `1`, from the belief that a closure snapshots a variable's value at the moment the function is created.
- **Rule:** A closure captures the variable binding itself, so it always sees the variable's latest value when called.
- **Your answer (`5, 9`):** **Right.**

**4.**
- **Why:** 1. `const a = make()` creates a fresh **lexical environment** (a dedicated storage record for that call's local variables) with `n = 0` and returns a closure over it. 2. `const b = make()` creates a second, independent environment with its own `n = 0`. 3. Arguments to `console.log` run left to right: `a()` increments `a`'s `n` to `1`, then `2`; `b()` increments `b`'s separate `n` to `1`; `a()` increments `a`'s `n` to `3`.
- **Answer:** `1 2 1 3`
- **The trap:** Answering `1 2 3 4` (believing all functions made by `make` share one `n`), or `1 1 1 1` (believing `n` resets on every call to `a()`).
- **Rule:** Every call to an outer function creates a brand-new, independent set of local variables for the closures it returns.
- **Your answer (`1 2 1 3`):** **Right.**

**5.**
- **Why:** 1. Calling `make()` creates a single environment holding `total = 2`. 2. Both `add` and `get` are created during that same call, making them **sibling closures** that share the exact same `total` binding. 3. `get()` reads `total` and logs `2`. 4. `add(5)` mutates that shared `total` to `7`, so the second `get()` logs `7`.
- **Answer:** `2`, `7`
- **The trap:** Answering `2`, `2`, from believing each inner function receives its own private copy of `total`.
- **Rule:** Multiple closures created in the same outer function call share the same underlying variable bindings.
- **Your answer (`2, 7`):** **Right.**

**6.**
- **Why:** 1. Because `var` is **function-scoped** (one binding shared across the entire `build` function, not per loop pass), only one `i` variable exists. 2. Each iteration pushes `() => i`, which captures that single `i` binding—not its value during that pass. 3. The loop runs for `i = 0, 1, 2`, then increments `i` to `3`, failing `i < 3` and ending. 4. Calling `fns[0]()`, `fns[1]()`, and `fns[2]()` reads that one `i`, which is now `3`.
- **Answer:** `3 3 3`
- **The trap:** Answering `0 1 2` (believing each loop pass gets its own `i` or snapshots `i`), or `2 2 2` (forgetting the final `i++` that exits the loop).
- **Rule:** A `for (var i = ...)` loop creates one shared variable across all iterations, so closures called afterward all see its final value.
- **Your answer (`0 1 2`):** **Wrong.** Your answer assumes either that `var i` creates a separate variable per iteration or that each arrow function froze the value `i` had when pushed into `fns`.

**7.**
- **Why:** 1. Top-level `let x = 1` creates an outer binding `x`. 2. Calling `bump(x)` passes the value `1` into `bump`'s parameter `x`, which creates a new local binding with the same name—**shadowing** (hiding) the outer `x` inside `bump`. 3. `x += 10` updates only the local parameter to `11`, leaving the outer `x` untouched. 4. `bump(x)` returns `11` (logged first), and `console.log(x)` then logs the outer `x`, `1`.
- **Answer:** `11`, `1`
- **The trap:** Answering `11`, `11`, from believing `bump` closes over and mutates the outer `x` because its parameter shares the same name.
- **Rule:** A parameter or inner declaration with the same name creates a separate local binding that hides—and never modifies—the outer variable.
- **Your answer (`11, 1`):** **Right.**

**8.**
- **Why:** 1. `make()` initializes `n = 0`. 2. Evaluating `{ value: n, ... }` copies the current primitive number `0` into the plain data property `value` right then. 3. By contrast, `inc` and `read` are closures over the live binding `n`. 4. Calling `c.inc()` twice updates `n` to `2` without changing the copied `0` in `c.value`, so `console.log(c.value, c.read())` logs `0 2`.
- **Answer:** `(b) 0 2`
- **The trap:** Picking `(a) 2 2`, from believing a plain property `value: n` stays live-linked to `n` the way a closure does. `(c)` assumes `n` never updates; `(d)` assumes `n` vanishes when `make` returns.
- **Rule:** Copying a primitive variable into an object property takes a one-time snapshot; only a function closing over the variable reads its later updates.
- **Your answer (`a`):** **Wrong.** Picking `(a) 2 2` treats `value: n` as a live reference to `n` rather than a one-time copy of `0` made when the object literal was created.

**9.**
- **Why:** 1. `obj.run()` calls `run` as a method on `obj`, setting `run`'s `this` to `obj`. 2. `a` is an arrow function, which has no `this` of its own and instead captures `this` lexically from `run` (`obj`), so `a()` returns `42`. 3. `b` is a regular function, which binds `this` dynamically from how it is called; called bare as `b()` in strict mode, its `this` is `undefined`, so `this?.id` evaluates to `undefined`. 4. `console.log(a(), b())` logs `42 undefined`.
- **Answer:** `(b) 42 undefined`
- **The trap:** Picking `(a) 42 42`, from believing regular inner functions capture `this` lexically just like ordinary variables. `(c)` swaps arrow and regular rules; `(d)` assumes neither keeps `this`.
- **Rule:** Arrow functions capture `this` lexically from their enclosing scope, whereas regular functions get a fresh `this` from each call site.
- **Your answer (`b`):** **Right.**

**10.**
- **Why:** 1. `let j` is declared once before the loop, so all iterations share one `j` binding. 2. `for (let i = 0; i < 3; i++)` creates a fresh `i` binding for each pass (`0`, `1`, `2`). 3. Pass 0 sets `j = 0`, pushes `a[0]` over pass 0's `i` (`0`), and pushes `b[0]` over the shared `j`; passes 1 and 2 update `j` to `1` and `2`. 4. When `i` reaches `3`, the loop stops without running the body again, so `j` stays `2`. 5. `a[0]()` returns `0` and `b[0]()` returns `2`.
- **Answer:** `0 2`
- **The trap:** Answering `0 0` (believing `let j` also creates a new binding per pass) or `0 3` (forgetting `j = i` does not run on the loop's exit check).
- **Rule:** Only a `let` declared inside the `for (...)` header creates a fresh binding per iteration; a `let` declared outside the loop is still shared.
- **Your answer (`0 2`):** **Right.**

*(Part 1 score: 7/10)*

---

### Part 2 (Questions 11–20)

**11.** What gets logged?

```js
function apply(fn) {
  const k = 100;
  return fn(5);
}

function start() {
  const k = 2;
  const scale = (n) => n * k;
  console.log(apply(scale));
}

start();
```

(a) `10`  
(b) `500`  
(c) `NaN`  
(d) Throws a `ReferenceError`

**12.** What gets logged?

```js
function make(n) {
  const read = () => n;
  n = n + 4;
  return read;
}

const f = make(3);
console.log(f());
```

**13.** What gets logged, in order?

```js
function make() {
  let limit = 5;
  const ok = (n) => n <= limit;
  const raise = (d) => { limit += d; };
  return { ok, raise };
}

const gate = make();
console.log(gate.ok(7));
gate.raise(3);
console.log(gate.ok(7));
```

**14.** What happens when this code runs?

```js
const x = 10;

function run() {
  console.log(x);
  let x = 20;
}

run();
```

(a) Logs `10`  
(b) Logs `undefined`  
(c) Logs `20`  
(d) Throws a `ReferenceError`

**15.** What gets logged?

```js
function outer(a) {
  return function middle(b) {
    a += 1;
    return a + b;
  };
}

const f = outer(10);
const g = outer(10);
console.log(f(1), f(1), g(1));
```

**16.** What gets logged?

```js
let state = { n: 1 };
const ref = state;
const read = () => state.n;

state = { n: 2 };
ref.n = 9;

console.log(read(), ref.n);
```

**17.** What gets logged?

```js
const a = {
  v: 1,
  make() {
    return () => this.v;
  },
};
const b = { v: 2 };
const fn = a.make();
console.log(fn.call(b));
```

(a) `1`  
(b) `2`  
(c) `undefined`  
(d) Throws a `TypeError`

**18.** What gets logged, in order?

```js
const next = (() => {
  let n = 10;
  return () => {
    n += 5;
    return n;
  };
})();

let n = 0;
console.log(next(), n);
console.log(next(), n);
```

**19.** What gets logged?

```js
function make(list) {
  return () => list.length;
}

let data = [1, 2];
const size = make(data);
data.push(3);
data = [9];
console.log(size());
```

**20.** What gets logged, in order?

```js
let x = 1;

function test() {
  console.log(x);
  var x = 2;
  console.log(x);
}

test();
console.log(x);
```

Reply with your answers for questions 11–20.

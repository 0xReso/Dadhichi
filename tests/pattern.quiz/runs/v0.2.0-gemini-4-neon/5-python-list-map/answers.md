# Answer key

## Mechanisms tested

1. No `list.map` method and `map(func, iterable)` argument order — Q1, Q10, Q21
2. Lazy evaluation of `map()` — Q2, Q8, Q9, Q14, Q21, Q22, Q24, Q26, Q28, Q29, Q30
3. Single-pass iterator exhaustion — Q3, Q11, Q23, Q25, Q26, Q27, Q28, Q29
4. Iterator vs. sequence behavior (no indexing, `len()`, or value equality; always truthy) — Q4, Q13, Q19, Q26
5. Non-mutating outer list vs. collecting return values of in-place methods — Q5, Q12, Q20, Q24
6. Multiple iterables (unpacked positional arguments and shortest-iterable stopping) — Q6, Q15, Q23, Q28
7. Live view of the underlying list vs. variable rebinding — Q7, Q16, Q24, Q27
8. Delayed error raising and iterator advancement on exception — Q8, Q18, Q25, Q30
9. Eager list comprehensions vs. lazy `map()` and closure late binding — Q9, Q17, Q22, Q29

---

### Q1
- **Why:** 1. Line 1 creates a `list` object bound to `nums`. 2. Line 2 looks up the attribute `map` on that `list`. Because Python's `list` type has no `.map()` method (mechanism 1), attribute lookup fails immediately before the `lambda` is even passed or called, raising `AttributeError`. 3. Line 3 never runs.
- **Answer:** (c) Raises `AttributeError`.
- **The trap:** (a) comes from expecting JavaScript- or Ruby-style `array.map()` to exist on Python lists. (b) assumes `.map()` exists and returns a Python `map` iterator; (d) confuses a missing attribute (`AttributeError`) with calling something of the wrong type (`TypeError`).
- **Rule:** Python lists have no `.map()` method; use the built-in `map(func, iterable)` function or a list comprehension instead.

### Q2
- **Why:** 1. `double` is defined without running its body. 2. `map(double, [1, 2, 3])` returns a `map` *iterator* (an object that produces items one at a time on demand). Because `map()` uses *lazy evaluation* (mechanism 2) — deferring work until items are actually requested — `double` is not called at all. 3. `print("done")` runs and outputs `done`.
- **Answer:** `done`
- **The trap:** Answering `run 1`, `run 2`, `run 3`, `done`, from believing `map()` immediately runs the function across the whole list and builds a new list (as in JavaScript or Python 2).
- **Rule:** Calling `map()` creates a lazy iterator and does not invoke the function on any element until something pulls values from it.

### Q3
- **Why:** 1. Line 1 builds a lazy `map` iterator `m` over `[10, 20]`. 2. `a = list(m)` pulls every item from `m` (`11`, `21`) until `m` is exhausted, storing `[11, 21]` in `a`. 3. Because a `map` object is a single-pass iterator (mechanism 3), `m` cannot rewind; `b = list(m)` pulls zero remaining items and produces `[]`. 4. Line 4 prints `[11, 21] []`.
- **Answer:** `[11, 21] []`
- **The trap:** Answering `[11, 21] [11, 21]`, from treating a `map` object like a reusable list or replayable recipe rather than a one-shot stream.
- **Rule:** A `map` iterator can be consumed only once; convert it to a `list` first if you need to iterate over the results more than once.

### Q4
- **Why:** 1. Line 1 creates a `map` iterator over an empty list. 2. Unlike a `list`, a `map` object defines neither `__len__` nor `__bool__` (mechanism 4), so Python treats every `map` object as truthy — `bool(m)` is `True` even when it will yield zero items. 3. `m == []` compares a `map` object to a `list` without consuming `m`; since `map` only compares equal to itself by identity, `m == []` is `False`.
- **Answer:** `True False`
- **The trap:** Answering `False True`, from assuming an empty `map` behaves like an empty list `[]` in boolean tests and equality checks.
- **Rule:** A `map` object is always truthy (even when empty) and never equals a `list`.

### Q5
- **Why:** 1. `nums` is `[1, 2, 3]`. 2. `map` applies `lambda x: x * 10` to each element as `list(...)` pulls values, assembling a brand-new list `[10, 20, 30]` in `out`. 3. Neither `map()` nor `list()` modifies `nums` (mechanism 5), so `nums` remains `[1, 2, 3]`. 4. Line 3 prints `[1, 2, 3] [10, 20, 30]`.
- **Answer:** `[1, 2, 3] [10, 20, 30]`
- **The trap:** Answering `[10, 20, 30] [10, 20, 30]`, from thinking `map()` updates the input list in place while returning a reference to it.
- **Rule:** `map()` never mutates the input list's own elements; consuming it with `list()` always produces a separate list.

### Q6
- **Why:** 1. `map` receives two *iterables* (objects you can loop over): `a` (length 3) and `b` (length 2). 2. On each pull, `map` takes one item from each iterable and passes them as separate positional arguments `x` and `y` (mechanism 6): `1 + 10 = 11`, then `2 + 20 = 22`. 3. On the next pull, `b` is exhausted, so `map` stops immediately and ignores `3`. 4. `res` is `[11, 22]`.
- **Answer:** `[11, 22]`
- **The trap:** Predicting an error (`ValueError` or `IndexError`) for mismatched lengths, or predicting `[11, 22, 3]` from expecting `map` to pad the shorter list with `0` or `None`.
- **Rule:** With multiple iterables, `map()` pairs elements positionally and stops as soon as the shortest iterable runs out.

### Q7
- **Why:** 1. Line 2 creates `m`, storing an iterator that points live to the `nums` list object rather than copying its elements (mechanism 7). 2. Because `m` is lazy, nothing has been read yet when line 3 mutates `nums` in place to `[1, 2, 3]`. 3. Line 4 consumes `m`, which reads all three current elements of `nums` and yields `[10, 20, 30]`.
- **Answer:** `[10, 20, 30]`
- **The trap:** Answering `[10, 20]`, from believing `map(fn, nums)` takes a snapshot of `nums` at the moment `map()` is called.
- **Rule:** A `map` over a list holds a live view of that list, so in-place mutations made before consumption change what `map` yields.

### Q8
- **Why:** 1. Line 2 creates a lazy `map` iterator `m` without running `10 // x` on any element (mechanisms 2 and 8). 2. Line 3 calls `next(m)` once, which pulls only the first element `2`, computes `10 // 2 = 5`, and prints `5`. 3. Because no second item is ever pulled, `0` is never passed to the lambda, so `ZeroDivisionError` is never raised.
- **Answer:** (c) Prints `5` and finishes without error.
- **The trap:** (a) assumes `map()` evaluates every element immediately on line 2; (b) thinks `next(m)` pre-fetches the next item; (d) assumes `next(m)` prints the whole sequence or ignores division by zero.
- **Rule:** Errors inside a `map` function are raised only when the failing element is actually pulled from the iterator.

### Q9
- **Why:** 1. Line 5 is a list comprehension, which runs *eagerly* (immediately executing the loop to build a full `list`, mechanism 9): `log(1)` prints `1 ` and `log(2)` prints `2 `. 2. Line 6 prints `| `. 3. Line 7 calls `map(log, [3, 4])`, which is lazy (mechanism 2) and calls `log` zero times. 4. Line 8 prints `end`.
- **Answer:** `1 2 | end`
- **The trap:** Answering `1 2 | 3 4 end`, from treating `map(log, [3, 4])` as equivalent in execution timing to `[log(x) for x in [3, 4]]`.
- **Rule:** List comprehensions evaluate every element right away, whereas `map()` defers all calls until its result is iterated.

### Q10
- **Why:** 1. Built-in `map(func, iterable)` requires the callable first and the iterable(s) second (mechanism 1). 2. On line 2, `nums` is passed as `func` and `lambda x: x + 1` is passed as `iterable`. 3. Even though `map()` is lazy about calling `func`, it immediately calls `iter()` on every iterable argument when constructed. Because a function is not iterable, line 2 immediately raises `TypeError`.
- **Answer:** (a) Line 2 raises `TypeError`.
- **The trap:** (d) comes from reversing the argument order to put data first (`map(data, fn)`). (b) assumes `map()` defers all argument checks until `list(m)` runs on line 3; (c) confuses `TypeError` with `AttributeError`.
- **Rule:** `map()` takes `(function, iterable, ...)` in that order, and it validates that every iterable argument is iterable immediately upon creation.

### Q11
- **Why:** 1. `4 in m` iterates `m` one element at a time looking for `4`, consuming each item it checks (mechanism 3). 2. First pull: `1 * 2 = 2` (not `4`). Second pull: `2 * 2 = 4` (match!). The `in` check stops immediately and returns `True`. 3. `m` now sits right before `3`. `list(m)` pulls the remaining items: `3 * 2 = 6` and `4 * 2 = 8`, yielding `[6, 8]`.
- **Answer:** `True [6, 8]`
- **The trap:** Answering `True [2, 4, 6, 8]` from thinking membership testing peeks without consuming, or `True []` from thinking `in` drains the entire iterator.
- **Rule:** Membership tests (`x in m`) consume a `map` iterator up to and including the matching element, leaving only the unvisited tail.

### Q12
- **Why:** 1. `list(map(...))` calls `r.append(9)` on each inner list in `rows`. 2. `list.append()` mutates its list in place and always returns `None`. 3. Because `map()` collects the return value of each call (mechanism 5), `out` becomes `[None, None]`, while the inner lists inside `rows` have been mutated to `[[1, 9], [2, 9]]`.
- **Answer:** `[[1, 9], [2, 9]] [None, None]`
- **The trap:** Answering `[[1], [2]] [[1, 9], [2, 9]]`, from assuming `r.append(9)` returns the updated list instead of mutating it in place and returning `None`.
- **Rule:** Passing an in-place mutating method to `map()` mutates the inner objects while filling the mapped output with `None`.

### Q13
- **Why:** 1. Line 1 creates a `map` iterator `m`. 2. A `map` object is an iterator, not a sequence (mechanism 4): it does not implement indexing (`__getitem__`), so it is not *subscriptable* (cannot be indexed with `[]`). 3. Evaluating `m[0]` on line 2 raises `TypeError: 'map' object is not subscriptable`.
- **Answer:** (c) Raises `TypeError`.
- **The trap:** (a) and (b) assume `map()` returns an indexable list of strings (`'1'`, printed without quotes as `1`). (d) assumes indexing is allowed on `map` objects and fails only because no items are materialized yet.
- **Rule:** You cannot index or call `len()` on a `map` object; use `next(m)` for the next item or convert with `list(m)` first.

### Q14
- **Why:** 1. Line 5 creates lazy `m`; nothing is printed yet (mechanism 2). 2. Loop iteration 1 pulls `1`: `tag(1)` prints `tag 1` and returns `2`; the loop body prints `got 2` (`2 != 4`). 3. Loop iteration 2 pulls `2`: `tag(2)` prints `tag 2` and returns `4`; the loop body prints `got 4`, hits `v == 4`, and breaks. 4. Because `m` produces items on demand, `3` is never pulled and `tag(3)` never runs.
- **Answer:** `tag 1`, `got 2`, `tag 2`, `got 4` (each on its own line).
- **The trap:** Printing `tag 1`, `tag 2`, `tag 3` before `got 2`, `got 4`, from assuming `map()` processes the whole input list upfront before the `for` loop starts.
- **Rule:** Iterating over `map()` interleaves each transformation call with the loop body and skips remaining elements if the loop exits early.

### Q15
- **Why:** 1. `map` is given two iterables, `[1, 2]` and `[10, 20]`. 2. When `map` receives multiple iterables, it unpacks one element from each as separate positional arguments (mechanism 6), calling `pair_sum(1, 10)` — not `pair_sum((1, 10))`. 3. Because `pair_sum` accepts only one argument (`pair`), Python raises `TypeError`.
- **Answer:** (c) Raises `TypeError`.
- **The trap:** (a) assumes `map` bundles corresponding elements into a tuple like `zip()` does before calling `pair_sum`. (b) mistakes `map` for `zip`; (d) thinks `map` feeds each list whole as `pair`.
- **Rule:** With `N` iterables, `map()` calls the function with `N` separate positional arguments, not a single `N`-tuple.

### Q16
- **Why:** 1. Line 2 creates `m`, holding an iterator attached directly to the original list object `[1, 2]`. 2. Line 3 *rebinds* (reassigns) the variable name `nums` to a new list `[100, 200]`; it does not mutate `[1, 2]` (mechanism 7). 3. Line 4 consumes `m`, which still reads from `[1, 2]` and produces `[11, 12]`.
- **Answer:** `[11, 12]`
- **The trap:** Answering `[110, 210]`, from thinking `m` looks up the variable name `nums` later rather than holding a reference to the original list object.
- **Rule:** Rebinding a variable to a new list leaves an existing `map` pointing at the old list; only mutating the original list in place affects `m`.

### Q17
- **Why:** 1. The comprehension creates three *closures* (functions that remember variables from their enclosing scope). 2. Python closures use *late binding* (mechanism 9): each `lambda` captures the loop variable `x` itself, not the value `x` held on that iteration. 3. By the time the comprehension finishes, `x` is `3`. 4. Calling each `f()` on line 2 reads `x == 3`, computing `3 * 2 = 6` every time.
- **Answer:** `[6, 6, 6]`
- **The trap:** Answering `[2, 4, 6]`, from believing each `lambda` freezes `x`'s current value when the function is created.
- **Rule:** Functions built inside a comprehension capture the loop variable by reference, so calling them later sees the variable's final value unless you capture it explicitly (for example, `lambda x=x: x * 2`).

### Q18
- **Why:** 1. Line 6 creates lazy `m`; `log` is still `[]`. 2. `list(m)` pulls `5`: `inv(5)` appends `5` to `log` and returns `2`. 3. `list(m)` pulls `0`: `inv(0)` appends `0` to `log`, then `10 // 0` raises `ZeroDivisionError` (mechanism 8). 4. `list(m)` aborts without returning a partial list, `except` sets `out = None`, and `2` is never pulled. 5. Line 11 prints `[5, 0] None`.
- **Answer:** `[5, 0] None`
- **The trap:** Answering `[5, 0, 2] None` (believing `map` ran on all elements before failing), or `[] None` (believing the error rolled back side effects), or `[5] None` (forgetting `log.append(0)` ran before the division).
- **Rule:** When an exception occurs mid-consumption, all side effects up to the failing line have already happened, `list(m)` produces no result, and later elements are never processed.

### Q19
- **Why:** 1. Lines 1–2 create two distinct `map` objects `a` and `b`. 2. Because `map` does not define value equality (mechanism 4), `a == b` falls back to object identity (`a is b`), returning `False` without consuming either iterator. 3. `list(a)` and `list(b)` then each materialize `['1', '2']`, and list equality compares their values, returning `True`.
- **Answer:** `False True`
- **The trap:** Answering `True True` (assuming two identical `map` calls compare equal), or `False False` / `True False` (thinking `a == b` consumed `a` and `b` before `list()` ran).
- **Rule:** Two `map` objects compare equal only if they are the exact same object, and comparing them with `==` does not consume them.

### Q20
- **Why:** 1. `sorted` returns a new sorted list without mutating its input, so `a` becomes `[[1, 3], [2, 4]]` while `rows` is still `[[3, 1], [4, 2]]`. 2. `list.sort` is an in-place mutating method that returns `None` (mechanism 5): calling it on each sublist mutates `rows` to `[[1, 3], [2, 4]]` and fills `b` with `[None, None]`. 3. Line 4 prints `[[1, 3], [2, 4]] [None, None] [[1, 3], [2, 4]]`.
- **Answer:** `[[1, 3], [2, 4]] [None, None] [[1, 3], [2, 4]]`
- **The trap:** Answering that `a` and `b` are identical (`[[1, 3], [2, 4]]`), or assuming `sorted` mutated `rows` while `list.sort` returned sorted copies.
- **Rule:** Use a non-mutating function like `sorted` inside `map()` when you want transformed values back; in-place methods like `list.sort` return `None`.

### Q21
- **Why:** 1. Option (a) fails with `AttributeError` because Python lists have neither `.filter()` nor `.map()` (mechanism 1). 2. Option (b) reverses `map`'s argument order (`iterable` before `func`), raising `TypeError` (mechanism 1). 3. Option (d) returns a lazy `<map object>`, not the list `[4, 16]` (mechanism 2). 4. Option (c) filters `nums` to `2, 4`, squares each with `map`, and materializes `[4, 16]` with `list()`.
- **Answer:** (c) `list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))`
- **The trap:** (a) applies JavaScript method chaining directly to Python lists; (b) puts the list first in `map()`; (d) forgets that `map()` returns an iterator rather than a `list`.
- **Rule:** To replace chained `.filter().map()` in Python, nest `map(fn, filter(pred, items))` wrapped in `list()`, or use a list comprehension `[x * x for x in nums if x % 2 == 0]`.

### Q22
- **Why:** 1. On line 2, the list comprehension runs eagerly while `k` is `2` (mechanism 9), computing `a = [2, 4]`. 2. On line 3, `map()` is lazy (mechanism 2) and its lambda captures `k` by reference (late binding, mechanism 9), so nothing is multiplied yet. 3. Line 4 changes `k` to `10`. 4. On line 5, `list(b)` finally runs the lambda, which reads `k == 10` and produces `[10, 20]`.
- **Answer:** `[2, 4] [10, 20]`
- **The trap:** Answering `[2, 4] [2, 4]` from assuming `map` ran or froze `k` on line 3, or `[10, 20] [10, 20]` from thinking comprehensions are lazy too.
- **Rule:** A list comprehension uses outer variables as they stand immediately, whereas a lazy `map()` reads outer variables as they stand when consumed.

### Q23
- **Why:** 1. For `a`, `map` calls `iter(nums)` twice on the list `nums`, creating two independent iterators (mechanism 6): pairs are `(1, 1), (2, 2), (3, 3), (4, 4)`, yielding `[2, 4, 6, 8]`. 2. For `b`, `it` is already a single-pass iterator (mechanism 3), and `iter(it)` returns `it` itself. Both slots pull from the same iterator in order: first `(1, 2) -> 3`, then `(3, 4) -> 7`, then `it` is exhausted, yielding `[3, 7]`.
- **Answer:** `[2, 4, 6, 8] [3, 7]`
- **The trap:** Answering `[2, 4, 6, 8] [2, 4, 6, 8]`, from assuming passing the same iterator twice to `map()` reads it in parallel instead of sharing one cursor.
- **Rule:** Passing a list twice to `map()` creates two independent iterators, whereas passing the same iterator object twice makes both arguments consume from one shared stream.

### Q24
- **Why:** 1. Line 2 creates lazy `m` holding a live list iterator at index `0` of `items` (`[1]`, mechanisms 2 and 7). 2. `a = next(m)` reads `items[0]` (`1`), advances the index to `1`, and calls `items.append(1)`, mutating `items` to `[1, 1]` and returning `None` (mechanism 5). 3. `b = next(m)` checks index `1`: because `items` now has length 2, it reads the newly appended `1`, appends another `1` (`items` becomes `[1, 1, 1]`), and returns `None`.
- **Answer:** `None None [1, 1, 1]`
- **The trap:** Expecting `b = next(m)` to raise `StopIteration` because `items` originally had only one element, or expecting `a` and `b` to be `[1, 1]` instead of `None`.
- **Rule:** Because a list iterator tracks an index over a live list, appending to the list while mapping over it feeds newly added items back into the same `map` (and `list(m)` here would never terminate).

### Q25
- **Why:** 1. Iteration 1: `next(m)` pulls `2`, advances the underlying iterator past `2`, and returns `10 // 2 = 5` (`out = [5]`). 2. Iteration 2: `next(m)` pulls `0` — advancing the underlying iterator past `0` *before* calling the lambda (mechanisms 3 and 8) — then `10 // 0` raises `ZeroDivisionError`, so `except` appends `'err'`. 3. Iteration 3: `m` is not broken or rewound; `next(m)` pulls the next item `5` and returns `2`.
- **Answer:** `[5, 'err', 2]`
- **The trap:** Answering `[5, 'err']` or expecting `StopIteration` on iteration 3 (thinking an exception permanently kills a `map` iterator), or `[5, 'err', 'err']` (thinking the failed item `0` is retried).
- **Rule:** An exception inside `map`'s function does not exhaust or rewind the `map` iterator; the next `next()` call continues with the following element.

### Q26
- **Why:** 1. `if m:` evaluates to `True` because a `map` object is always truthy, and checking truthiness does not pull any items (mechanism 4). 2. `any(m)` pulls lazily until the first truthy result (mechanisms 2 and 3): `1 > 2` (`False`), `2 > 2` (`False`), `3 > 2` (`True`), stopping immediately and setting `first = True`. 3. Only `4` remains unconsumed, so `list(m)` yields `[True]`.
- **Answer:** `True [True]`
- **The trap:** Answering `True [False, False, True, True]` (thinking `any()` does not consume `m`), or `True []` (thinking `any()` drains all four elements instead of short-circuiting).
- **Rule:** Short-circuit consumers like `any()` and `all()` stop pulling from a `map` iterator as soon as the outcome is known, leaving the remaining items intact.

### Q27
- **Why:** 1. Line 2 creates a list iterator inside `m` starting at index `0` over `nums` (mechanism 7). 2. Line 3 (`first = next(m)`) reads `nums[0]` (`1`), advances the internal index to `1`, and returns `10` (mechanism 3). 3. Line 4 (`nums.pop(0)`) removes `1`, shifting `nums` to `[2, 3]` so `2` is now at index `0` and `3` is at index `1`. 4. Line 5 (`list(m)`) resumes at index `1`, reading `3` -> `[30]`, skipping `2`.
- **Answer:** `10 [30]`
- **The trap:** Answering `10 [20, 30]`, from thinking `m` either snapshotted `nums` or remembers elements by value instead of by integer index.
- **Rule:** Removing earlier elements from a list while consuming a `map` over it shifts remaining elements backward past the iterator's index, causing elements to be skipped.

### Q28
- **Why:** 1. On pull 1, `map` pulls left-to-right from its iterators (mechanisms 2, 3, and 6): `1` from `a`, then `10` from `b`, yielding `11`. 2. On pull 2, `map` first pulls `2` from `a`, then asks `b` for a value; `b` is exhausted, so `map` stops and discards `2`. 3. Because `2` was already pulled from `a`, `list(a)` returns only `[3]`.
- **Answer:** `[11] [3]`
- **The trap:** Answering `[11] [2, 3]`, from assuming `map()` checks whether all iterables have another item before pulling from the first one.
- **Rule:** When `map()` stops on a shorter iterable, it has already consumed and discarded one extra item from every longer iterator listed to the left of it.

### Q29
- **Why:** 1. `a` is a lazy, single-pass `map` iterator (mechanisms 2 and 3), whereas `b` is a materialized, reusable `list` `[2, 4, 6]` built eagerly by the list comprehension (mechanism 9). 2. The first `sum(a)` consumes `a` and returns `12`; the second `sum(a)` iterates the now-empty `a` and returns `0`. 3. Both `sum(b)` calls sum the reusable list `[2, 4, 6]` and return `12`.
- **Answer:** `12 0 12 12`
- **The trap:** Answering `12 12 12 12`, from treating a `map` object and a list comprehension as interchangeable containers when passed to built-ins like `sum()`.
- **Rule:** Passing a `map` object to a consumer like `sum()`, `min()`, or `max()` exhausts it, whereas a list comprehension's result can be summed or scanned repeatedly.

### Q30
- **Why:** 1. Line 9 builds a lazy pipeline: `map(g, map(f, [2, 1, 3]))` runs neither `f` nor `g` yet (mechanism 2). 2. `list(m)` pulls one item at a time through the entire chain: for `2`, `f(2)` logs `('f', 2)` and returns `1`, then `g(1)` logs `('g', 1)` and returns `10`. 3. Next, for `1`, `f(1)` logs `('f', 1)` and returns `0`, then `g(0)` logs `('g', 0)` and raises `ZeroDivisionError` (mechanism 8). 4. `except` sets `res = "fail"`, and `f(3)` never runs.
- **Answer:** `[('f', 2), ('g', 1), ('f', 1), ('g', 0)] fail`
- **The trap:** Answering `[('f', 2), ('f', 1), ('f', 3), ('g', 1), ('g', 0)] fail`, from expecting chained `map` calls to finish the entire first stage on all items before starting the second stage (as JavaScript's `.map(f).map(g)` does).
- **Rule:** Nested `map()` calls form a lazy element-by-element pipeline, so each item flows through every stage before the next item is pulled — and an error halts later items before even the inner stage runs on them.

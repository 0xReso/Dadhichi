# Answer key

## Mechanisms and the questions that test them

1. `map` is a built-in function that takes the function first and the iterables after it. It is not a list method. Q1, Q14, Q28
2. `map()` returns a map object, an iterator, not a list. It has no length and no indexing, and it is always truthy. Q2, Q8, Q17, Q22
3. A map is lazy: the function runs only when the next item is requested, so its side effects and errors happen at consumption time. Q3, Q11, Q20, Q24, Q30
4. A map gives its items once. Anything that reads items (`list`, `sum`, `in`, `next`, a `for` loop) uses them up, and later reads get only what is left. Q4, Q12, Q22, Q24, Q26, Q27
5. Chained maps run item by item: each item passes through the whole chain before the next item starts. Q9, Q24
6. With several iterables, map takes one item from each per call, passes them as separate arguments, and stops when the shortest runs out. Q5, Q16, Q27, Q29
7. The function receives exactly what iterating the input yields, as a single argument. Tuples are not unpacked, and a dict yields its keys. Q7, Q19, Q29
8. map holds the original object it was given. Mutating that object before or during consumption is visible, but pointing the name at a new object is not. Q10, Q21, Q26
9. A lambda reads its outside variables when it is called, not when it is created, and with a lazy map that call can come much later. Q13, Q25
10. map collects whatever the function returns. In-place methods such as `append`, `sort` and `print` return `None`. Q6, Q15, Q20, Q28
11. Exceptions inside the function: a `StopIteration` silently ends the map early, and any other exception propagates while leaving the map able to continue with the next item. Q18, Q23, Q30

---

**Q1**
Why: 1. Line 1 makes an ordinary list. 2. Line 2 looks up an attribute called `map` on the list. Lists have methods like `append`, `sort` and `pop`, but no `map`; in Python, `map` is a built-in function you call as `map(function, iterable)`. 3. The lookup fails before the lambda is ever used, so an `AttributeError` is raised on line 2 and line 3 never runs.
Answer: (c) `AttributeError: 'list' object has no attribute 'map'`, raised on line 2.
The trap: (a), from carrying over JavaScript's `array.map(fn)`. (b) assumes the method exists but behaves like the built-in; (d) assumes it works in place and returns `None`, like `sort`.
Rule: in Python you write `map(f, items)`; there is no `items.map(f)`.

**Q2**
Why: 1. `map(...)` builds a map object. It does not compute any doubled values yet. 2. Printing an object that has no custom text form shows its type and memory address, so the first line is `<map object at 0x...>` (the address varies from run to run). 3. `type(result)` is the `map` class, whose name is `map`.
Answer:
```
<map object at 0x...>
map
```
The trap: expecting `[2, 4, 6]` and `list`, from the belief that `map` returns a list. That was true in Python 2; in Python 3 it returns an iterator, an object that hands out one item at a time on request.
Rule: `map()` gives you a map object; wrap it in `list()` when you want a list.

**Q3**
Why: 1. `map(double, [1, 2])` only records the function and the list; `double` is not called. 2. `print("created")` runs and prints `created`. 3. `list(m)` asks the map for items one by one: it calls `double(1)`, printing `double 1` and returning 2, then `double(2)`, printing `double 2` and returning 4. 4. The finished list is printed.
Answer:
```
created
double 1
double 2
[2, 4]
```
The trap: printing `double 1` and `double 2` before `created`, from the belief that `map()` applies the function as soon as it is called. Map is lazy: work happens only when someone asks for an item.
Rule: the function inside a map runs when the map is consumed, not when it is created.

**Q4**
Why: 1. The first `list(m)` pulls every item: `str(1)`, `str(2)`, `str(3)`, and prints `['1', '2', '3']`. 2. The map object now has no items left; it is exhausted. 3. The second `list(m)` asks for items, gets none immediately, and builds an empty list. No error is raised.
Answer:
```
['1', '2', '3']
[]
```
The trap: printing the list twice, from the belief that a map object is a stored collection like a list. It is a one-pass stream.
Rule: a map can be read once; to use the results twice, store them with `list()` first.

**Q5**
Why: 1. With two iterables, map takes one item from each per call: `x=1, y=10` gives 11, then `x=2, y=20` gives 22. 2. On the third round it gets 3 from `a` but `b` has nothing left, so the map stops. 3. The leftover 3 is dropped silently.
Answer: (a) `[11, 22]`
The trap: (b), from believing leftover items pass through unchanged. (c) comes from expecting a length check (map has none by default); (d) from believing map pairs every item with every other item.
Rule: map with several iterables walks them side by side and stops at the shortest one.

**Q6**
Why: 1. `list(...)` consumes the map, calling the lambda on each row. 2. For `[1]`, `r.append(0)` changes that row to `[1, 0]` and returns `None`, because `append` modifies the list in place and returns nothing. 3. The same happens to `[2]`. 4. map collected the two return values, both `None`. 5. `rows` holds the same two inner lists, which were changed.
Answer:
```
[None, None]
[[1, 0], [2, 0]]
```
The trap: `[[1, 0], [2, 0]]` for `out`, from the belief that map collects the changed items. It collects what the function returns.
Rule: map's results are the function's return values, so an in-place method gives you a list of `None`.

**Q7**
Why: 1. `map(add, pairs)` is created without calling `add`. 2. `list(...)` asks for the first item, so map calls `add` with the first element of `pairs`, the single tuple `(1, 2)`. 3. map does not unpack the tuple, so `x` is `(1, 2)` and `y` receives nothing. 4. Python raises a `TypeError` during that first call, and nothing is printed.
Answer: `TypeError: add() missing 1 required positional argument: 'y'`
The trap: expecting `[3, 7]`, from the belief that map spreads each tuple across the function's parameters. It passes each element as one argument (`itertools.starmap` is the tool that unpacks).
Rule: map passes each element whole, as a single argument, no matter what shape it has.

**Q8**
Why: 1. `map(abs, [])` creates a map object over an empty list. 2. `if m:` asks whether the object is truthy. Python treats an object as false only if it defines a length of zero or a false boolean value. 3. A map object defines neither, because it cannot know how many items it will produce without running. 4. So it counts as true, and the first branch runs.
Answer: `has items`
The trap: `empty`, from the belief that a map over an empty list is falsy like an empty list. A map object is always truthy.
Rule: you cannot test a map for emptiness with `if`; convert it to a list or try to read an item.

**Q9**
Why: 1. `list` asks the outer map (`g`) for an item. 2. The outer map asks the inner map (`f`) for an item, which calls `f(1)`: prints `f 1`, returns 2. 3. The outer map calls `g(2)`: prints `g 2`, returns 20. 4. `list` asks for the next item: `f(2)` prints `f 2` and returns 3, then `g(3)` prints `g 3` and returns 30. 5. Both maps are now exhausted, and the list is printed.
Answer:
```
f 1
g 2
f 2
g 3
[20, 30]
```
The trap: `f 1`, `f 2`, `g 2`, `g 3`, from the belief that the inner map finishes all its work before the outer map starts. Chained maps pass one item at a time through the whole chain.
Rule: stacked maps process item by item, so their side effects interleave.

**Q10**
Why: 1. `map(str, items)` keeps a reference to the list object itself and a position in it, starting at 0; it copies nothing. 2. `items.append(3)` changes that same list to `[1, 2, 3]`. 3. `list(m)` reads the list from the start and finds three items, so it calls `str` on each.
Answer: `['1', '2', '3']`
The trap: `['1', '2']`, from the belief that map takes a snapshot of the list when it is created. It reads the live list when consumed.
Rule: a map reads its source when it is consumed, so changes made to that object before then are included.

**Q11**
Why: 1. Line 2 creates the map without calling `int`. 2. Line 3 prints `parsed`. 3. Line 4: `sum` pulls items one at a time. `int("1")` gives 1 and `int("2")` gives 2, then `int("x")` raises a `ValueError` because `"x"` is not a whole number. 4. The error stops the script inside line 4, so line 5 never runs.
Answer: (b) `parsed` is printed, then `ValueError: invalid literal for int() with base 10: 'x'` is raised at line 4.
The trap: (a), from believing map converts the values at line 2. (c) assumes map skips items that fail; (d) assumes a failed conversion leaves the string in place.
Rule: an error inside a map's function appears where the map is consumed, not where it is created.

**Q12**
Why: 1. `3 in m` pulls items until one equals 3: `abs(-1)` is 1, no match; `abs(-3)` is 3, a match, so it stops and gives `True`. 2. The first two items are used up. 3. `list(m)` continues from where the search stopped: `abs(-5)` is 5 and `abs(-7)` is 7.
Answer:
```
True
[5, 7]
```
The trap: `[1, 3, 5, 7]` on the second line, from the belief that `in` only looks at a map without using it up. On an iterator, `in` consumes items as it searches.
Rule: anything that reads from a map, including `in`, uses up the items it reads.

**Q13**
Why: 1. The lambda refers to `k` by name; it does not store the value 1. 2. Creating the map calls nothing. 3. `k = 100` changes the global variable. 4. `list(m)` now calls the lambda: it looks up `k`, finds 100, and returns `10 + 100` and `20 + 100`.
Answer: `[110, 120]`
The trap: `[11, 21]`, from the belief that the lambda fixes the value of `k` when the map is created. A function reads outside variables when it runs, and a lazy map runs it later.
Rule: a lazy map uses the values its function's outside variables have at consumption time.

**Q14**
Why: 1. `map`'s first argument is the function and the rest are iterables. Here the list sits in the function slot and `str.upper` sits in the iterable slot. 2. When `map(...)` is called, it immediately asks each iterable for an iterator. It does not check yet whether the first argument can be called. 3. `str.upper` is a method object of type `method_descriptor` and cannot be iterated, so a `TypeError` is raised inside the `map(...)` call, before `list` or `print` runs.
Answer: `TypeError: 'method_descriptor' object is not iterable`, raised by the `map(...)` call.
The trap: `['A', 'B']`, from the belief that map works out which argument is the function. A second trap is expecting "'list' object is not callable", but that check would come only later, at consumption.
Rule: map's order is fixed, `map(function, iterable)`, and the iterables are checked as soon as the map is created.

**Q15**
Why: 1. `list(...)` consumes the map, calling `print("a")`, which prints `a` and returns `None`. 2. It then calls `print("b")`, which prints `b` and returns `None`. 3. `out` holds the two return values. 4. The last line prints that list.
Answer:
```
a
b
[None, None]
```
The trap: expecting `['a', 'b']` for `out`, from the belief that map collects the items it visited. It collects what the function returned, and `print` returns `None`.
Rule: a map built for side effects gives you a list of whatever the function returns, usually `None`.

**Q16**
Why: 1. Map walks the string and the list side by side. A string iterates one character at a time. 2. `"a" * 3` is `"aaa"`. 3. `"b" * 0` is the empty string `""`. 4. `"c" * 2` is `"cc"`. 5. The string has no fourth character, so map stops and the 5 is never used.
Answer: `['aaa', '', 'cc']`
The trap: a result with four items (or an error about the extra 5), from the belief that map runs to the length of the longer input. A second trap is dropping the `''`, from believing an empty result is skipped.
Rule: map stops at the shortest input, and every call produces exactly one result, even an empty one.

**Q17**
Why: 1. `m` is a map object, an iterator. 2. `m[0]` asks for item 0 by position. An iterator only supports asking for the next item; it does not support positions. 3. Python raises a `TypeError` before any squaring happens.
Answer: `TypeError: 'map' object is not subscriptable`
The trap: `1`, from the belief that map returns a list you can index. Use `list(m)[0]` or `next(m)` instead.
Rule: a map object has no positions and no length; it can only hand out the next item.

**Q18**
Why: 1. The first `list(m)` calls `12 // 3`, giving 4. 2. It then calls `12 // 0`, which raises `ZeroDivisionError`. The list being built is discarded, and its `print` never runs. 3. The `except` prints `error`. 4. The map has already moved past 3 and 0, and the exception did not end it. 5. The second `list(m)` continues with 4: `12 // 4` is 3.
Answer:
```
error
[3]
```
The trap: `[]` on the last line, from believing an exception ends the map for good. Another is `[4, 3]`, from believing the 4 is kept or recomputed.
Rule: after the function raises, the map remains positioned after the failed item and can continue with the next one.

**Q19**
Why: 1. Iterating a dict yields its keys, `"a"` then `"b"`. 2. map passes each key as `x`. 3. `"a" * 2` is `"aa"` and `"b" * 2` is `"bb"`. The values 2 and 5 are never seen.
Answer: `['aa', 'bb']`
The trap: `[4, 10]`, from the belief that mapping over a dict works on its values. map gets whatever iterating the input yields; use `prices.values()` for the values, or `prices.items()` for `(key, value)` tuples.
Rule: map's function receives exactly what a `for` loop over the input would give you.

**Q20**
Why: 1. `map(seen.append, ...)` creates the map; `append` has not been called. 2. The first `print(seen)` shows `[]`. 3. `next(m)` asks for exactly one item, so `seen.append(1)` runs once. It returns `None`, which `next` hands back and the code ignores. 4. The second `print(seen)` shows `[1]`. The 2 and 3 are never appended.
Answer:
```
[]
[1]
```
The trap: `[1, 2, 3]` for one or both prints, from the belief that creating the map, or touching it once, runs it fully. Each `next` runs the function once.
Rule: a map does only as much work as has been asked of it.

**Q21**
Why: 1. `map(..., items)` grabs the list object `[1, 2, 3]` itself, not the name `items`. 2. `items = [7]` makes the name point to a new list; the original list is unchanged and still held by the map. 3. `list(m)` doubles 1, 2 and 3.
Answer: `[2, 4, 6]`
The trap: `[14]`, from the belief that the map follows the variable name. It follows the object it was given. Compare Q10, where the same object was changed.
Rule: changing the object a map holds affects it; pointing the name at a new object does not.

**Q22**
Why: 1. `sum(m)` pulls every item: `len("ab")` is 2, `len("c")` is 1, `len("def")` is 3, so it prints `6`. 2. The map is now exhausted. 3. `max(m)` gets no items, and `max` of nothing has no answer, so it raises a `ValueError`.
Answer: (b) it prints `6`, then raises a `ValueError`.
The trap: (a), from the belief that the map can be read again. (c) assumes `max` of nothing is 0, like `sum`; (d) assumes `sum` needs a list, but it accepts any iterable.
Rule: once one function has consumed a map, the next function sees an empty stream.

**Q23**
Why: 1. `list` asks for items. `f(1)` returns 10. 2. `f(2)` raises `StopIteration`. That exception is the signal an iterator uses to say "I have no more items". 3. map lets it pass up unchanged, and `list` reads it as the normal end of the map, so it stops quietly with `[10]`. `f(3)` is never called. 4. No error is shown, so `done` prints.
Answer:
```
[10]
done
```
The trap: expecting a traceback, often a `RuntimeError`, from the belief that a stray `StopIteration` is always turned into an error. That conversion applies to generator functions, not to map.
Rule: a `StopIteration` raised inside a map's function silently cuts the results short.

**Q24**
Why: 1. Creating both maps calls nothing. 2. `next(m)` asks the outer map for one item. It asks the inner map, which calls `f(1)`: prints `f 1`, returns 1. 3. The outer map calls `f(1)` on that result: prints `f 1` again, returns 1. 4. `print` shows `1`. 5. `print("then")` runs. Items 2 and 3 are never touched.
Answer:
```
f 1
f 1
1
then
```
The trap: printing `f 1`, `f 2`, `f 3` first, from the belief that the inner map runs over the whole list before the outer one starts. Each `next` pulls a single item through the chain.
Rule: asking a chain of maps for one item runs each stage once, for that item only.

**Q25**
Why: 1. The loop creates two maps, each holding a lambda that refers to the variable `k`. Neither lambda has run. 2. After the loop, `k` is 2. 3. The comprehension calls `list(m)` on each map, which calls the lambda with `n = 0`. Each lambda looks up `k` at that moment and finds 2. 4. Both give `[2]`.
Answer: `[[2], [2]]`
The trap: `[[1], [2]]`, from the belief that each lambda captured the value `k` had on its loop pass. It captured the variable, and the lazy maps run only after the loop has finished.
Rule: a lazy map with a lambda sees outside variables as they are when it is finally consumed, not when the map was made.

**Q26**
Why: 1. The map holds the list and reads it at a moving position. 2. Item 0: prints `1`. `len(items)` is 2, so 3 is appended. 3. Item 1: prints `2`. The length is 3, so 4 is appended. 4. Item 2 now exists: prints `3`. The length is 4, so nothing is appended. 5. Item 3 exists: prints `4`. 6. There is no item 4, so the loop ends.
Answer:
```
1
2
3
4
```
The trap: printing only `1` and `2`, from the belief that the map fixed the list's length when the loop started. It checks the live list at every step.
Rule: items added to the source list while a map is being consumed will still be reached.

**Q27**
Why: 1. Both arguments are the same iterator, `it`. 2. For each call, map takes one item from the first argument and then one from the second: 1 and 2, giving `1 * 10 + 2 = 12`. 3. Next round: 3 and 4, giving 34. 4. Next round: the first argument yields 5, and then the second (the same, now empty, iterator) has nothing left, so map stops. The 5 has been used up and is lost.
Answer: `[12, 34]`
The trap: `[11, 22, 33, 44, 55]`, from the belief that each argument gets its own copy of the sequence. Another is `[12, 34, 5]` or an error, from expecting the odd 5 to be handled.
Rule: map pulls one item from each argument in turn, so passing one iterator twice pairs up neighbouring items.

**Q28**
Why: 1. `list(map(sorted, groups))` calls `sorted` on each inner list. `sorted` builds a new sorted list and leaves the original alone, so `a` is `[[1, 3], [0, 2]]` and `groups` is unchanged so far. 2. `list.sort` is the list class's own sort method, and any callable can be passed to map. `list.sort(group)` sorts that inner list in place and returns `None`. 3. So `b` is `[None, None]`, and the inner lists of `groups` are now sorted.
Answer:
```
[[1, 3], [0, 2]]
[None, None] [[1, 3], [0, 2]]
```
The trap: `b` equal to the sorted lists, from the belief that map gives back the transformed items. map gives back return values, and `sort` returns `None`.
Rule: map accepts any callable, including `list.sort`, and keeps only what that callable returns.

**Q29**
Why: 1. The error happens because each tuple arrives as one argument `x` and `y` gets nothing. 2. Option (b) takes one argument `p` and adds its parts: `1 + 2` is 3 and `3 + 4` is 7, giving `[3, 7]`. 3. Option (a) becomes `map(f, (1, 2), (3, 4))`, so it pairs the tuples' matching positions: `f(1, 3)` is 4 and `f(2, 4)` is 6, giving `[4, 6]`. 4. Option (c) still passes whole tuples, so it fails the same way. 5. Option (d) passes a tuple as both `x` and `y`, and adding tuples joins them: `[(1, 2, 1, 2), (3, 4, 3, 4)]`.
Answer: (b) `map(lambda p: p[0] + p[1], pairs)`
The trap: (a), from believing `*` spreads each pair into one call's arguments. It actually turns the tuples into separate iterables. (c) blames the container type; (d) expects the second iterable to supply each pair's second half.
Rule: map gives one argument per iterable, never one argument per part of an element.

**Q30**
Why: 1. `next(m)` calls `f(5)`: prints `call 5` and returns `10 // 5`, which is 2. 2. `print` shows `2`. 3. The second `next(m)` calls `f(0)`: prints `call 0`, then `10 // 0` raises `ZeroDivisionError`, and the `except` prints `skip`. 4. The map has already moved past the 0. 5. `list(m)` continues with `f(2)`: prints `call 2` and returns 5. 6. `print` shows `[5]`.
Answer:
```
call 5
2
call 0
skip
call 2
[5]
```
The trap: `[]` at the end, from believing an error finishes the map. Another is `call 0` appearing again, from believing the failed item is retried.
Rule: a map runs its function only when an item is requested, and after an exception it continues with the next item.

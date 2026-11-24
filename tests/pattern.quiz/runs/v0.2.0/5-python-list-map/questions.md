Python list.map · low depth · 30 questions
Assumptions: CPython 3.12, each snippet run as its own fresh script; an error is given as its exception type and message.
Python lists have no `.map` method, so this quiz covers the built-in `map()` function applied to lists, which is what `list.map` means in languages like JavaScript.

## Band 1 · One rule at a time

**Q1 · What happens when this runs?**

```python
items = [1, 2, 3]
result = items.map(lambda n: n * 2)
print(result)
```

(a) It prints `[2, 4, 6]`
(b) It prints `<map object at 0x...>`
(c) It raises an `AttributeError` on line 2
(d) It prints `None`

**Q2 · What does this print?**

```python
items = [1, 2, 3]
result = map(lambda n: n * 2, items)
print(result)
print(type(result).__name__)
```

**Q3 · What gets printed, in what order?**

```python
def double(n):
    print("double", n)
    return n * 2

m = map(double, [1, 2])
print("created")
print(list(m))
```

**Q4 · What does this print?**

```python
m = map(str, [1, 2, 3])
print(list(m))
print(list(m))
```

**Q5 · What does this print?**

```python
a = [1, 2, 3]
b = [10, 20]
print(list(map(lambda x, y: x + y, a, b)))
```

(a) `[11, 22]`
(b) `[11, 22, 3]`
(c) It raises an error because the lists have different lengths
(d) `[11, 21, 12, 22, 13, 23]`

**Q6 · What does this print?**

```python
rows = [[1], [2]]
out = list(map(lambda r: r.append(0), rows))
print(out)
print(rows)
```

## Band 2 · Rules in less obvious settings

**Q7 · What happens when this runs?**

```python
pairs = [(1, 2), (3, 4)]

def add(x, y):
    return x + y

print(list(map(add, pairs)))
```

**Q8 · What does this print?**

```python
m = map(abs, [])
if m:
    print("has items")
else:
    print("empty")
```

**Q9 · What gets printed, in what order?**

```python
def f(n):
    print("f", n)
    return n + 1

def g(n):
    print("g", n)
    return n * 10

print(list(map(g, map(f, [1, 2]))))
```

**Q10 · What does this print?**

```python
items = [1, 2]
m = map(str, items)
items.append(3)
print(list(m))
```

**Q11 · What happens when this runs?**

```python
values = ["1", "2", "x"]
nums = map(int, values)        # line 2
print("parsed")                # line 3
total = sum(nums)              # line 4
print(total)                   # line 5
```

(a) A `ValueError` is raised at line 2 and nothing is printed
(b) `parsed` is printed, then a `ValueError` is raised at line 4
(c) `parsed` and then `3` are printed
(d) `parsed` is printed, then a `TypeError` is raised at line 4 because `"x"` cannot be added to a number

**Q12 · What does this print?**

```python
m = map(abs, [-1, -3, -5, -7])
print(3 in m)
print(list(m))
```

**Q13 · What does this print?**

```python
k = 1
m = map(lambda n: n + k, [10, 20])
k = 100
print(list(m))
```

**Q14 · What happens when this runs, and on which call?**

```python
items = ["a", "b"]
print(list(map(items, str.upper)))
```

**Q15 · What gets printed, in what order?**

```python
out = list(map(print, ["a", "b"]))
print(out)
```

**Q16 · What does this print?**

```python
print(list(map(lambda c, n: c * n, "abc", [3, 0, 2, 5])))
```

**Q17 · What happens when this runs?**

```python
m = map(lambda n: n * n, [1, 2, 3])
print(m[0])
```

**Q18 · What does this print?**

```python
m = map(lambda n: 12 // n, [3, 0, 4])
try:
    print(list(m))
except ZeroDivisionError:
    print("error")
print(list(m))
```

**Q19 · What does this print?**

```python
prices = {"a": 2, "b": 5}
print(list(map(lambda x: x * 2, prices)))
```

**Q20 · What does this print?**

```python
seen = []
m = map(seen.append, [1, 2, 3])
print(seen)
next(m)
print(seen)
```

**Q21 · What does this print?**

```python
items = [1, 2, 3]
m = map(lambda n: n * 2, items)
items = [7]
print(list(m))
```

## Band 3 · Combining rules and edge cases

**Q22 · What happens when this runs?**

```python
m = map(len, ["ab", "c", "def"])
print(sum(m))
print(max(m))
```

(a) It prints `6`, then `3`
(b) It prints `6`, then raises a `ValueError`
(c) It prints `6`, then `0`
(d) It raises a `TypeError` at `sum`, because `m` is not a list

**Q23 · What does this print?**

```python
def f(n):
    if n == 2:
        raise StopIteration
    return n * 10

print(list(map(f, [1, 2, 3])))
print("done")
```

**Q24 · What gets printed, in what order?**

```python
def f(n):
    print("f", n)
    return n

m = map(f, map(f, [1, 2, 3]))
print(next(m))
print("then")
```

**Q25 · What does this print?**

```python
ms = []
for k in [1, 2]:
    ms.append(map(lambda n: n + k, [0]))
print([list(m) for m in ms])
```

**Q26 · What does this print?**

```python
items = [1, 2]
for s in map(str, items):
    print(s)
    if len(items) < 4:
        items.append(len(items) + 1)
```

**Q27 · What does this print?**

```python
it = iter([1, 2, 3, 4, 5])
print(list(map(lambda a, b: a * 10 + b, it, it)))
```

**Q28 · What does this print?**

```python
groups = [[3, 1], [2, 0]]
a = list(map(sorted, groups))
b = list(map(list.sort, groups))
print(a)
print(b, groups)
```

**Q29 · This code raises a `TypeError`. Which single change makes it print `[3, 7]`?**

```python
pairs = [(1, 2), (3, 4)]
print(list(map(lambda x, y: x + y, pairs)))
```

(a) Change the map call to `map(lambda x, y: x + y, *pairs)`
(b) Change the map call to `map(lambda p: p[0] + p[1], pairs)`
(c) Change the map call to `map(lambda x, y: x + y, list(pairs))`
(d) Change the map call to `map(lambda x, y: x + y, pairs, pairs)`

**Q30 · What gets printed, in what order?**

```python
def f(n):
    print("call", n)
    return 10 // n

m = map(f, [5, 0, 2])
print(next(m))
try:
    next(m)
except ZeroDivisionError:
    print("skip")
print(list(m))
```

Topic: Python list.map (low depth, 30 questions)
Assumptions: Python 3 (CPython 3.12), standard built-ins unmodified unless shadowed in the snippet.
Scope note: Python lists do not have a .map() method; this quiz covers real Python 3 behavior — why .map() fails on lists, the built-in map() function, and list comprehensions.

## Band 1: Core mechanisms

**Q1.** What happens when this code runs?

```python
nums = [1, 2, 3]
res = nums.map(lambda x: x * 2)
print(res)
```

(a) Prints `[2, 4, 6]`
(b) Prints `<map object at ...>`
(c) Raises `AttributeError`
(d) Raises `TypeError`

**Q2.** What gets printed, in what order?

```python
def double(x):
    print("run", x)
    return x * 2

res = map(double, [1, 2, 3])
print("done")
```

**Q3.** What does this print?

```python
m = map(lambda x: x + 1, [10, 20])
a = list(m)
b = list(m)
print(a, b)
```

**Q4.** What does this print?

```python
m = map(lambda x: x * 2, [])
print(bool(m), m == [])
```

**Q5.** What does this print?

```python
nums = [1, 2, 3]
out = list(map(lambda x: x * 10, nums))
print(nums, out)
```

**Q6.** What does this print?

```python
a = [1, 2, 3]
b = [10, 20]
res = list(map(lambda x, y: x + y, a, b))
print(res)
```

## Band 2: Applying mechanisms in new settings

**Q7.** What does this print?

```python
nums = [1, 2]
m = map(lambda x: x * 10, nums)
nums.append(3)
print(list(m))
```

**Q8.** What happens when this code runs?

```python
nums = [2, 0, 4]
m = map(lambda x: 10 // x, nums)
print(next(m))
```

(a) Raises `ZeroDivisionError` on line 2
(b) Prints `5`, then raises `ZeroDivisionError` on line 3
(c) Prints `5` and finishes without error
(d) Prints `5`, `0`, `2`

**Q9.** What does this print?

```python
def log(x):
    print(x, end=" ")
    return x

a = [log(x) for x in [1, 2]]
print("|", end=" ")
b = map(log, [3, 4])
print("end")
```

**Q10.** Which line raises an error, and what exception type is it?

```python
nums = [1, 2, 3]
m = map(nums, lambda x: x + 1)
print(list(m))
```

(a) Line 2 raises `TypeError`
(b) Line 3 raises `TypeError`
(c) Line 2 raises `AttributeError`
(d) No error; prints `[2, 3, 4]`

**Q11.** What does this print?

```python
m = map(lambda x: x * 2, [1, 2, 3, 4])
print(4 in m, list(m))
```

**Q12.** What does this print?

```python
rows = [[1], [2]]
out = list(map(lambda r: r.append(9), rows))
print(rows, out)
```

**Q13.** What happens when this code runs?

```python
m = map(str, [1, 2, 3])
print(m[0])
```

(a) Prints `1`
(b) Prints `'1'`
(c) Raises `TypeError`
(d) Raises `IndexError`

**Q14.** What gets printed, in what order?

```python
def tag(x):
    print("tag", x)
    return x * 2

m = map(tag, [1, 2, 3])
for v in m:
    print("got", v)
    if v == 4:
        break
```

**Q15.** What happens when this code runs?

```python
def pair_sum(pair):
    return pair[0] + pair[1]

res = list(map(pair_sum, [1, 2], [10, 20]))
print(res)
```

(a) Prints `[11, 22]`
(b) Prints `[(1, 10), (2, 20)]`
(c) Raises `TypeError`
(d) Prints `[3, 30]`

**Q16.** What does this print?

```python
nums = [1, 2]
m = map(lambda x: x + 10, nums)
nums = [100, 200]
print(list(m))
```

**Q17.** What does this print?

```python
funcs = [lambda: x * 2 for x in [1, 2, 3]]
print([f() for f in funcs])
```

**Q18.** What does this print?

```python
log = []
def inv(x):
    log.append(x)
    return 10 // x

m = map(inv, [5, 0, 2])
try:
    out = list(m)
except ZeroDivisionError:
    out = None
print(log, out)
```

**Q19.** What does this print?

```python
a = map(str, [1, 2])
b = map(str, [1, 2])
print(a == b, list(a) == list(b))
```

**Q20.** What does this print?

```python
rows = [[3, 1], [4, 2]]
a = list(map(sorted, rows))
b = list(map(list.sort, rows))
print(a, b, rows)
```

**Q21.** Given `nums = [1, 2, 3, 4]`, which expression evaluates to `[4, 16]`?

(a) `nums.filter(lambda x: x % 2 == 0).map(lambda x: x * x)`
(b) `list(map(nums, lambda x: x * x))`
(c) `list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)))`
(d) `map(lambda x: x * x, [x for x in nums if x % 2 == 0])`

## Band 3: Combining mechanisms and edge cases

**Q22.** What does this print?

```python
k = 2
a = [x * k for x in [1, 2]]
b = map(lambda x: x * k, [1, 2])
k = 10
print(a, list(b))
```

**Q23.** What does this print?

```python
nums = [1, 2, 3, 4]
a = list(map(lambda x, y: x + y, nums, nums))
it = iter(nums)
b = list(map(lambda x, y: x + y, it, it))
print(a, b)
```

**Q24.** What does this print?

```python
items = [1]
m = map(items.append, items)
a = next(m)
b = next(m)
print(a, b, items)
```

**Q25.** What does this print?

```python
m = map(lambda x: 10 // x, [2, 0, 5])
out = []
for _ in range(3):
    try:
        out.append(next(m))
    except ZeroDivisionError:
        out.append("err")
print(out)
```

**Q26.** What does this print?

```python
m = map(lambda x: x > 2, [1, 2, 3, 4])
if m:
    first = any(m)
    rest = list(m)
print(first, rest)
```

**Q27.** What does this print?

```python
nums = [1, 2, 3]
m = map(lambda x: x * 10, nums)
first = next(m)
nums.pop(0)
rest = list(m)
print(first, rest)
```

**Q28.** What does this print?

```python
a = iter([1, 2, 3])
b = iter([10])
out = list(map(lambda x, y: x + y, a, b))
print(out, list(a))
```

**Q29.** What does this print?

```python
nums = [1, 2, 3]
a = map(lambda x: x * 2, nums)
b = [x * 2 for x in nums]
print(sum(a), sum(a), sum(b), sum(b))
```

**Q30.** What does this print?

```python
log = []
def f(x):
    log.append(("f", x))
    return x - 1
def g(x):
    log.append(("g", x))
    return 10 // x

m = map(g, map(f, [2, 1, 3]))
try:
    res = list(m)
except ZeroDivisionError:
    res = "fail"
print(log, res)
```

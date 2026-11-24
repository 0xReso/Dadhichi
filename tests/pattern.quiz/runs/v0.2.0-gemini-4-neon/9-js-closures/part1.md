Topic: JavaScript closures — Low depth (30 questions)
Assumptions: ES2022+ JavaScript in strict mode (single script, e.g., Node 20 or a modern browser), with `console.log` output shown in execution order.

### Part 1 (Questions 1–10)

**1.** What gets logged?

```js
const x = 1;

function show() {
  console.log(x);
}

function run() {
  const x = 2;
  show();
}

run();
```

**2.** What gets logged, in order?

```js
function make(base) {
  return function (n) {
    return base + n;
  };
}

const f = make(10);
console.log(f(3));
console.log(f(7));
```

**3.** What gets logged, in order?

```js
let n = 1;

function read() {
  return n;
}

n = 5;
console.log(read());
n = 9;
console.log(read());
```

**4.** What gets logged?

```js
function make() {
  let n = 0;
  return function () {
    n += 1;
    return n;
  };
}

const a = make();
const b = make();
console.log(a(), a(), b(), a());
```

**5.** What gets logged, in order?

```js
function make() {
  let total = 2;
  const add = (x) => { total += x; };
  const get = () => total;
  return [add, get];
}

const [add, get] = make();
console.log(get());
add(5);
console.log(get());
```

**6.** What gets logged?

```js
function build() {
  const fns = [];
  for (var i = 0; i < 3; i++) {
    fns.push(() => i);
  }
  return fns;
}

const fns = build();
console.log(fns[0](), fns[1](), fns[2]());
```

**7.** What gets logged, in order?

```js
let x = 1;

function bump(x) {
  x += 10;
  return x;
}

console.log(bump(x));
console.log(x);
```

**8.** What gets logged?

```js
function make() {
  let n = 0;
  return {
    value: n,
    inc() { n += 1; },
    read() { return n; },
  };
}

const c = make();
c.inc();
c.inc();
console.log(c.value, c.read());
```

(a) `2 2`  
(b) `0 2`  
(c) `0 0`  
(d) `undefined 2`

**9.** What gets logged?

```js
const obj = {
  id: 42,
  run() {
    const a = () => this?.id;
    const b = function () { return this?.id; };
    console.log(a(), b());
  },
};

obj.run();
```

(a) `42 42`  
(b) `42 undefined`  
(c) `undefined 42`  
(d) `undefined undefined`

**10.** What gets logged?

```js
function run() {
  const a = [];
  const b = [];
  let j;
  for (let i = 0; i < 3; i++) {
    j = i;
    a.push(() => i);
    b.push(() => j);
  }
  console.log(a[0](), b[0]());
}

run();
```

Reply with your answers for questions 1–10.

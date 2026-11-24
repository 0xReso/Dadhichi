Topic: React useEffect, state updates and re-render order | Depth: low (30 questions)
Assumptions: React 18 in the browser (`createRoot`), `StrictMode` off, React hooks (`useState`, `useEffect`, `useRef`) imported, standard browser events, and console logs listed in execution order.

## Band 1: Core Mechanisms in Isolation

**1.** What gets logged on initial mount, and in what order?

```jsx
function App() {
  useEffect(() => {
    console.log("first");
  });
  console.log("body");
  useEffect(() => {
    console.log("second");
  });
  return <p>hi</p>;
}
```

**2.** The component mounts, then the user clicks the button once. What gets logged, in what order?

```jsx
function App() {
  const [n, setN] = useState(0);
  function handleClick() {
    setN(1);
    console.log("click", n);
  }
  console.log("render", n);
  return <button onClick={handleClick}>{n}</button>;
}
```

**3.** After initial mount, the user clicks the button once. Which logs are printed **because of that click** (not including mount)?

```jsx
function App() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  useEffect(() => { console.log("E1"); }, []);
  useEffect(() => { console.log("E2"); }, [a]);
  useEffect(() => { console.log("E3"); });
  return <button onClick={() => setB(b + 1)}>go</button>;
}
```

(a) `E3` only
(b) `E2`, `E3`
(c) `E1`, `E2`, `E3`
(d) None — none of the effects depend on `b`

**4.** The component mounts, then the user clicks the button once. What gets logged, in what order?

```jsx
function App() {
  const [n, setN] = useState(0);
  console.log("render", n);
  function handleClick() {
    setN(n + 1);
    setN(n + 1);
    setN(n + 1);
  }
  return <button onClick={handleClick}>{n}</button>;
}
```

**5.** The component mounts, then the user clicks the button twice. What gets logged in total, in order?

```jsx
function App() {
  const [n, setN] = useState(5);
  useEffect(() => {
    console.log("effect", n);
  });
  console.log("render", n);
  return <button onClick={() => setN(5)}>stay</button>;
}
```

**6.** The component mounts, then the user clicks the button once. What gets logged, in what order?

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("effect", n);
    return () => console.log("cleanup", n);
  }, [n]);
  console.log("render", n);
  return <button onClick={() => setN(1)}>next</button>;
}
```

## Band 2: Applying Mechanisms in Less Obvious Settings

**7.** What gets logged when `<App />` mounts, in what order?

```jsx
function Child() {
  useEffect(() => { console.log("child effect"); }, []);
  console.log("child render");
  return <span>c</span>;
}
function App() {
  useEffect(() => { console.log("parent effect"); }, []);
  console.log("parent render");
  return <Child />;
}
```

**8.** After mount, the user clicks the button once. What number does the button display?

```jsx
function App() {
  const [n, setN] = useState(0);
  function handleClick() {
    setN(n + 5);
    setN((x) => x + 1);
    setN(n + 2);
    setN((x) => x + 1);
  }
  return <button onClick={handleClick}>{n}</button>;
}
```

(a) `3`
(b) `7`
(c) `9`
(d) `1`

**9.** The component mounts at t = 0 ms. At t = 200 ms and t = 400 ms, the user clicks the button twice. At t = 1000 ms, the timer fires. What gets logged?

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const id = setTimeout(() => {
      console.log("timer", n);
    }, 1000);
    return () => clearTimeout(id);
  }, []);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**10.** The component mounts, then the user clicks the button twice. How many times does `"cfg effect"` get logged in total?

```jsx
function App() {
  const [n, setN] = useState(0);
  const cfg = { limit: 10 };
  useEffect(() => {
    console.log("cfg effect");
  }, [cfg]);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

(a) 1 time (only on mount)
(b) 2 times
(c) 3 times (on mount and after every click)
(d) 0 times, because `cfg` is not state

**11.** The component mounts, then the user clicks the button twice. What gets logged, in order?

```jsx
function App() {
  const [n, setN] = useState(0);
  const r = useRef(0);
  let x = 0;
  function handleClick() {
    r.current += 1;
    x += 1;
    setN(n + 1);
  }
  console.log(n, r.current, x);
  return <button onClick={handleClick}>go</button>;
}
```

**12.** The component mounts (showing `2`), then the user clicks the button once. What does the button show afterward, and why?

```jsx
function App() {
  const [items, setItems] = useState([1, 2]);
  function add() {
    items.push(3);
    setItems(items);
  }
  return <button onClick={add}>{items.length}</button>;
}
```

(a) `3`, because `setItems` triggers a re-render after `push`
(b) `2`, because `items` is the same array reference, so React bails out and skips re-rendering
(c) `2`, because React freezes state arrays and ignores `push`
(d) It throws an error because React forbids mutating state arrays

**13.** The component mounts, then the user clicks the button once. What gets logged in total, in order?

```jsx
function App() {
  const [step, setStep] = useState(1);
  useEffect(() => {
    console.log("after", step);
  }, [step]);
  if (step === 2) {
    console.log("early", step);
    return <p>done</p>;
  }
  console.log("main", step);
  return <button onClick={() => setStep(2)}>go</button>;
}
```

**14.** `<App />` mounts, then the user clicks the `<div>` once. What gets logged in total, in order?

```jsx
function Box() {
  useEffect(() => {
    console.log("open");
    return () => console.log("close");
  }, []);
  return <p>box</p>;
}
function App() {
  const [show, setShow] = useState(true);
  console.log("app", show);
  return <div onClick={() => setShow(false)}>{show && <Box />}</div>;
}
```

**15.** The component mounts, the user clicks once, and 100 ms later the timeout fires. What gets logged in total?

```jsx
function App() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  console.log("render", a, b);
  function handleClick() {
    setTimeout(() => {
      setA(1);
      setB(1);
    }, 100);
  }
  return <button onClick={handleClick}>go</button>;
}
```

(a) `render 0 0`, `render 1 0`, `render 1 1`
(b) `render 0 0`, `render 1 1`
(c) `render 0 0`, `render 0 1`, `render 1 1`
(d) `render 0 0` only, because setters inside `setTimeout` do not re-render

**16.** The component mounts, then the user clicks the button twice. What gets logged, and what number does the button display at the end?

```jsx
function App() {
  const count = useRef(0);
  function handleClick() {
    count.current += 1;
    console.log("ref", count.current);
  }
  console.log("render", count.current);
  return <button onClick={handleClick}>{count.current}</button>;
}
```

(a) Logs `render 0`, `ref 1`, `render 1`, `ref 2`, `render 2`; button displays `2`
(b) Logs `render 0`, `ref 1`, `ref 2`; button displays `2`
(c) Logs `render 0`, `ref 1`, `ref 2`; button displays `0`
(d) Logs `render 0`, `ref 0`, `ref 0`; button displays `0`

**17.** After `<App />` has already mounted, the user clicks the `<div>` once. What gets logged **for that click** (excluding mount)?

```jsx
function Child() {
  useEffect(() => { console.log("C-eff"); });
  console.log("C-ren");
  return <p>c</p>;
}
function App() {
  const [n, setN] = useState(0);
  useEffect(() => { console.log("P-eff"); });
  console.log("P-ren");
  return <div onClick={() => setN(n + 1)}><Child /></div>;
}
```

**18.** Three seconds (3000 ms) pass after mount, so the interval callback has fired three times. (1) What number does `<p>` display? (2) What would `<p>` display after three ticks if line 4 used `setN((x) => x + 1)` instead?

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setN(n + 1), 1000);
    return () => clearInterval(id);
  }, []);
  return <p>{n}</p>;
}
```

**19.** `<App id="A" />` mounts (`id` never changes), and the user clicks the button once. Which line causes `"id A"` to be logged a second time, and why?

```jsx
function App({ id }) {
  const [n, setN] = useState(0);
  const logId = () => console.log("id", id);
  useEffect(() => {
    logId();
  }, [logId]);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**20.** The component mounts, then the user clicks the button once. What gets logged?

```jsx
function App() {
  const [id, setId] = useState("A");
  useEffect(() => {
    return () => console.log("bye", id);
  }, [id]);
  return <button onClick={() => setId("B")}>{id}</button>;
}
```

(a) Nothing — cleanup only runs when `App` unmounts
(b) `bye B`
(c) `bye A`
(d) `bye A`, `bye B`

**21.** The component mounts (`n = 0`), then the user clicks the button once. What gets logged?

```jsx
function App() {
  const [n, setN] = useState(0);
  async function handleClick() {
    setN(n + 1);
    await Promise.resolve();
    console.log("after", n);
  }
  return <button onClick={handleClick}>{n}</button>;
}
```

## Band 3: Combining Mechanisms and Edge Cases

**22.** `<App />` mounts, then the user clicks the `<div>` once. What gets logged in total, in order?

```jsx
function Child() {
  useEffect(() => () => console.log("C-clean"), []);
  console.log("C-ren");
  return <p>c</p>;
}
function App() {
  const [on, setOn] = useState(true);
  useEffect(() => { console.log("P-eff", on); }, [on]);
  console.log("P-ren", on);
  return <div onClick={() => setOn(false)}>{on && <Child />}</div>;
}
```

**23.** Which component(s) trigger an infinite render loop when mounted?

```jsx
function A() {
  const [n, setN] = useState(0);
  useEffect(() => { setN(n + 1); });
  return <p>{n}</p>;
}
function B() {
  const [obj, setObj] = useState({ v: 1 });
  useEffect(() => { setObj({ v: 1 }); }, [obj]);
  return <p>{obj.v}</p>;
}
```

(a) Only `A`, because `B` has a dependency array and sets the same `{ v: 1 }` value
(b) Only `B`, because `A` has no dependency array so it runs once
(c) Both `A` and `B`
(d) Neither, because React blocks state updates inside `useEffect`

**24.** The component mounts, then the user clicks the button once. What gets logged in total, in order?

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("eff", n);
    return () => console.log("clean", n);
  }, [n]);
  function bump() {
    setN((x) => x + 1);
    setN((x) => x + 1);
  }
  return <button onClick={bump}>{n}</button>;
}
```

**25.** The component mounts at t = 0 ms. The user clicks the button twice (at t = 100 ms and t = 200 ms). At t = 500 ms, the timer fires. What gets logged?

```jsx
function App() {
  const [n, setN] = useState(0);
  const latest = useRef(n);
  latest.current = n;
  useEffect(() => {
    const id = setTimeout(() => {
      console.log(n, latest.current);
    }, 500);
    return () => clearTimeout(id);
  }, []);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**26.** `<App />` mounts, then the user clicks the `<div>` once. (1) What gets logged in total, in order? (2) What gets logged instead if line 10 (`const ping = ...`) is moved outside `App`?

```jsx
function Child({ onPing }) {
  useEffect(() => {
    console.log("sub");
    return () => console.log("unsub");
  }, [onPing]);
  return <p>child</p>;
}
function App() {
  const [n, setN] = useState(0);
  const ping = () => console.log("ping");
  return <div onClick={() => setN(n + 1)}><Child onPing={ping} /></div>;
}
```

**27.** After mount, the user clicks the button once. (1) How many times in total has `"render"` been logged? (2) What changes if line 5 is replaced with `setUser((prev) => prev)`?

```jsx
function App() {
  const [user, setUser] = useState({ name: "Ada" });
  console.log("render");
  function save() {
    setUser((prev) => ({ name: prev.name }));
  }
  return <button onClick={save}>{user.name}</button>;
}
```

**28.** The component mounts (`n = 0`), then the user clicks the button once (`n` becomes `1`). What gets logged?

```jsx
function App() {
  const [n, setN] = useState(0);
  const r = useRef(0);
  r.current = n;
  useEffect(() => {
    const snap = r.current;
    return () => console.log(snap, r.current);
  }, [n]);
  return <button onClick={() => setN(1)}>{n}</button>;
}
```

(a) `0 0`
(b) `0 1`
(c) `1 1`
(d) `1 0`

**29.** What gets logged when `<App />` mounts and settles, in exact order?

```jsx
function Child({ n }) {
  useEffect(() => { console.log("C-eff", n); }, [n]);
  console.log("C-ren", n);
  return <p>{n}</p>;
}
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("P-eff", n);
    if (n === 0) setN(1);
  }, [n]);
  console.log("P-ren", n);
  return <Child n={n} />;
}
```

**30.** `<App />` mounts at t = 0 ms (`id = "A"`). At t = 50 ms, the user clicks the button (`id` becomes `"B"`). Both timers eventually fire (at 150 ms and 500 ms). What gets logged?

```jsx
function App() {
  const [id, setId] = useState("A");
  useEffect(() => {
    let ignore = false;
    setTimeout(() => {
      if (!ignore) console.log("show", id);
    }, id === "A" ? 500 : 100);
    return () => { ignore = true; };
  }, [id]);
  return <button onClick={() => setId("B")}>{id}</button>;
}
```

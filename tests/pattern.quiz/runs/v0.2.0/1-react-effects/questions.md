React useEffect, state updates and re-render order · depth low · 30 questions
Assumptions: React 18 in the browser, rendered with `createRoot`, StrictMode off; function components with `useState`, `useEffect`, `useLayoutEffect` and `useRef` imported from "react"; "click" means one real user click, and each click is fully processed before the next.

## Band 1 · One mechanism at a time

**Q1 · What gets logged, in what order, when `Box` first mounts?**

```jsx
function Box() {
  console.log("render");
  useEffect(() => {
    console.log("effect");
  });
  console.log("after hook call");
  return <div />;
}
```

**Q2 · The component mounts, then the button is clicked twice. How many times in total is each of `A`, `B` and `C` logged?**

```jsx
function C() {
  const [n] = useState(0);
  const [m, setM] = useState(0);
  useEffect(() => console.log("A"));
  useEffect(() => console.log("B"), []);
  useEffect(() => console.log("C"), [n]);
  return <button onClick={() => setM(m + 1)}>{n}</button>;
}
```

**Q3 · The component mounts and the button is clicked once. Write the full log, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  function handle() {
    setN(5);
    console.log("handler", n);
  }
  console.log("render", n);
  return <button onClick={handle}>go</button>;
}
```

**Q4 · `n` starts at 0. The button is clicked once and runs `handle`. What number does the button show afterwards?**

```jsx
function handle() {
  setN(n + 1);
  setN(n + 1);
  setN(p => p + 1);
}
```

**Q5 · A parent first renders `<C id={1} />`, then re-renders it as `<C id={2} />`, then stops rendering `C` altogether. Write the full log, in order.**

```jsx
function C({ id }) {
  useEffect(() => {
    console.log("start", id);
    return () => console.log("stop", id);
  }, [id]);
  return null;
}
```

**Q6 · `<Parent />` mounts. What gets logged, in what order?**

```jsx
function Child() {
  console.log("child render");
  useEffect(() => console.log("child effect"));
  return null;
}
function Parent() {
  console.log("parent render");
  useEffect(() => console.log("parent effect"));
  return <Child />;
}
```

## Band 2 · Applying the mechanisms

**Q7 · The component mounts, the button is clicked once, and the timer fires. Write the full log, in order.**

```jsx
function C() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);
  console.log("render", a, b);
  function handle() {
    setTimeout(() => {
      setA(1);
      setB(1);
    }, 0);
  }
  return <button onClick={handle}>go</button>;
}
```

**Q8 · The component mounts, then the button is clicked three times. How many times in total is `effect` logged?**

```jsx
function C() {
  const [n, setN] = useState(0);
  const options = { size: 10 };
  useEffect(() => {
    console.log("effect");
  }, [options]);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**Q9 · `Timer` mounts and the interval fires five times. What number is on the screen after the fifth tick?**

```jsx
function Timer() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setN(n + 1);
    }, 1000);
    return () => clearInterval(id);
  }, []);
  return <p>{n}</p>;
}
```

**Q10 · `C` mounts. What gets logged, in what order?**

```jsx
function C() {
  useEffect(() => console.log("effect"));
  useLayoutEffect(() => console.log("layout"));
  console.log("render");
  return null;
}
```

**Q11 · `C` mounts and nothing else happens. Write the full log, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    setN(n + 1);
    console.log("effect", n);
  }, []);
  console.log("render", n);
  return null;
}
```

**Q12 · The component mounts, then the button is clicked twice. Write every line that `effect` logs, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  const [tick, setTick] = useState(0);
  useEffect(() => console.log("effect", n), [n]);
  function handle() {
    setN(n);
    setTick(tick + 1);
  }
  return <button onClick={handle}>go</button>;
}
```

**Q13 · `n` starts at 0. The button is clicked once and runs `handle`. What is `n` after the resulting render?**

```jsx
function handle() {
  setN(p => p + 1);
  setN(10);
  setN(p => p * 2);
}
```

**Q14 · The component mounts and the button is clicked once. Write the full log, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("run", n);
    return () => console.log("clean", n);
  });
  console.log("render", n);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**Q15 · `<Parent />` has mounted. The button is clicked once. Write only the lines logged because of the click, in order.**

```jsx
function Child() {
  console.log("child render");
  useEffect(() => console.log("child effect"), []);
  return null;
}
function Parent() {
  const [n, setN] = useState(0);
  console.log("parent render", n);
  useEffect(() => console.log("parent effect", n), [n]);
  return <button onClick={() => setN(n + 1)}>{n}<Child /></button>;
}
```

**Q16 · `C` mounts. What happens?**

```jsx
function C() {
  const [user, setUser] = useState({ name: "a" });
  useEffect(() => {
    setUser({ name: "a" });
  }, [user]);
  return <p>{user.name}</p>;
}
```

(a) One render. The effect runs once and the update is ignored, because the new user has the same name.
(b) Two renders, then it stops, because the second user has the same contents as the first.
(c) It keeps rendering and re-running the effect without end.
(d) React throws an error on the first `setUser`, because state may not be set inside an effect.

**Q17 · The component mounts, the button is clicked three times, and then the user presses a key. What does the key press log?**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const onKey = () => console.log("key", n);
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**Q18 · The component mounts, then the paragraph is clicked once. Write only the lines logged because of the click, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  const ref = useRef(null);
  function handle() {
    setN(1);
    setN(2);
    console.log(ref.current.textContent);
  }
  console.log("render", n);
  return <p ref={ref} onClick={handle}>{n}</p>;
}
```

**Q19 · `C` mounts. Which statement is true?**

```jsx
function C() {
  const [w, setW] = useState(0);
  useLayoutEffect(() => {
    setW(100);
  }, []);
  console.log("render", w);
  return <p>{w}</p>;
}
```

(a) It logs `render 0`, `render 100`, and the browser never paints 0.
(b) It logs `render 0`, `render 100`, and the browser paints 0 for one frame before 100.
(c) It logs only `render 100`.
(d) It logs only `render 0`, and the screen shows 0 until some later event.

**Q20 · A parent renders `C` three times in a row (the first render and two re-renders), each time as `<C user={{ id: 1, name: "a" }} />`. How many times in total is `effect` logged?**

```jsx
function C({ user }) {
  useEffect(() => {
    console.log("effect");
  }, [user.id]);
  return <p>{user.name}</p>;
}
```

**Q21 · A parent shows `<C />`. The user clicks the button three times. The parent then stops rendering `C`, and later renders `<C />` again in the same place. Write the full log, in order, and the number the button shows at the end.**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("mount", n);
    return () => console.log("unmount");
  }, []);
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

## Band 3 · Combining mechanisms and edge cases

**Q22 · The component has mounted. The button is clicked once. Write only the lines logged because of the click, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("A run", n);
    return () => console.log("A clean", n);
  });
  useEffect(() => {
    console.log("B run", n);
    return () => console.log("B clean", n);
  });
  return <button onClick={() => setN(n + 1)}>{n}</button>;
}
```

**Q23 · `<Parent />` mounts and nothing else happens. Write the full log, in order.**

```jsx
function Child({ onReady }) {
  useEffect(() => {
    onReady();
  }, []);
  console.log("child render");
  return null;
}
function Parent() {
  const [ready, setReady] = useState(false);
  useEffect(() => console.log("parent effect", ready));
  console.log("parent render", ready);
  return <Child onReady={() => setReady(true)} />;
}
```

**Q24 · `Timer` mounts. After the third tick has been fully processed (the screen shows 3 and that render's effects have run), how many times has `setInterval` been called, and how many intervals are still active?**

```jsx
function Timer() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const id = setInterval(() => setN(n + 1), 1000);
    return () => clearInterval(id);
  }, [n]);
  return <p>{n}</p>;
}
```

**Q25 · The component has mounted. The button is clicked once. Write only the lines logged because of the click, or say "nothing".**

```jsx
function C() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("effect", n);
  }, [n]);
  function handle() {
    setN(p => p + 1);
    setN(p => p - 1);
  }
  console.log("render", n);
  return <button onClick={handle}>go</button>;
}
```

**Q26 · The component mounts, and the button is clicked twice within the first second. What does the timeout log after 3 seconds?**

```jsx
function C() {
  const [n, setN] = useState(0);
  const ref = useRef(0);
  useEffect(() => {
    const id = setTimeout(() => console.log(n, ref.current), 3000);
    return () => clearTimeout(id);
  }, []);
  function handle() {
    setN(n + 1);
    ref.current = ref.current + 1;
  }
  return <button onClick={handle}>{n}</button>;
}
```

**Q27 · The component mounts. The user clicks button "a" three times, then button "b" once. What does the paragraph show after the third click on "a", and what after the click on "b"?**

```jsx
function C() {
  const r = useRef(0);
  const [n, setN] = useState(0);
  return (
    <>
      <button onClick={() => { r.current += 1; }}>a</button>
      <button onClick={() => setN(n + 1)}>b</button>
      <p>{r.current} {n}</p>
    </>
  );
}
```

**Q28 · `<Parent />` mounts. What gets logged, in what order?**

```jsx
function Child() {
  useEffect(() => console.log("child effect"));
  useLayoutEffect(() => console.log("child layout"));
  return null;
}
function Parent() {
  useEffect(() => console.log("parent effect"));
  useLayoutEffect(() => console.log("parent layout"));
  return <Child />;
}
```

**Q29 · The component mounts, the button is clicked once, and two seconds pass. Write the full log, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  function handle() {
    setN(n + 1);
    setTimeout(() => {
      console.log("later", n);
      setN(p => p + 1);
    }, 1000);
  }
  console.log("render", n);
  return <button onClick={handle}>go</button>;
}
```

**Q30 · `C` mounts and nothing else happens. Write the full log, in order.**

```jsx
function C() {
  const [n, setN] = useState(0);
  useLayoutEffect(() => {
    console.log("layout", n);
  }, [n]);
  useEffect(() => {
    console.log("effect", n);
    if (n < 2) setN(n + 1);
    return () => console.log("clean", n);
  }, [n]);
  console.log("render", n);
  return null;
}
```

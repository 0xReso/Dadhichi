# Upskill quiz

**Learn a topic by being wrong about it in a controlled way.** You get a short piece of code, a few numbers or a described situation, and you predict exactly what happens. Then the answer walks through what really happens, names the belief that led you astray, and leaves you with one rule to carry forward.

The model question for this skill is this one:

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => { console.log("effect A", n); setN(1); }, []);
  useEffect(() => { console.log("effect B", n); }, [n]);
  console.log("render", n);
  return <p>{n}</p>;
}
// What gets logged, in what order?
```

There is nothing to memorize here. Everything hangs on one mechanism: effects run after the render they belong to. If your model of React is slightly off, you will be confident and wrong, and that is the point. Every question in a quiz is built the same way, for any field: code, SQL, finance, chess, cooking chemistry or your own team's docs.

## Use it

In Claude Code, inside this repository:

```text
/upskill-quiz React effects and re-renders
/upskill-quiz how bond prices react to interest rates medium
/upskill-quiz PostgreSQL isolation levels high sheet
```

Or just ask: *"quiz me on the JavaScript event loop, medium depth."*

| Depth | Questions | Mechanisms covered | Rough time |
| --- | --- | --- | --- |
| low (default) | 30 | 8 to 10 | about 45 minutes |
| medium | 60 | 15 to 20 | two sittings |
| high | 100 | 25 to 35 | a week of short sessions |

**Interactive** (the default) asks ten questions at a time and waits. You reply with your answers, for example `1: render 0, effect A 0 ... 2: b`, and it marks each one. For every miss it names the specific wrong belief behind your answer. After the last part you get a scorecard by mechanism and a review round (R1, R2 and so on) that re-tests what you missed in new shapes. Progress is saved to `quizzes/<topic>/progress.md`, so you can stop and resume.

**Sheet** writes `quizzes/<topic>/questions.md` and a separate `answers.md`. Work through the questions on paper or your phone, then say *"grade my <topic> quiz"*.

**Reinforce** by coming back after a few days and saying *"review my <topic> misses"*. You get fresh questions on the mechanisms you got wrong. Retrieving a rule after a gap is what turns it into intuition.

Tell it what you already know, for example *"I write SQL daily but have never thought about concurrent transactions,"* and it will skip what you have mastered and aim at the beliefs you are likely to hold. Point it at docs, for example *"quiz me on loop/LOOP.md,"* and every answer will be held to that source.

## What makes a question good enough to keep

The prompt holds every question to these standards, and the test rubric checks them:

1. **One precise, checkable outcome.** The exact output, an order of events, a number, or which of two things is larger. A vague "what's best practice?" does not count.
2. **A concrete artifact.** At most 15 lines of code, about 80 words of scenario, or just the numbers the calculation needs. At least half the questions ask you to predict from one.
3. **Exactly one right answer.** The assumptions that change the outcome are stated up front, for example "React 18, StrictMode off" or "annual coupons."
4. **One mechanism, one trap.** Every multiple-choice wrong option is the answer that a specific wrong belief produces, so your choice shows which belief to fix.
5. **No trivia.** No release years, inventors or flag names learned by rote.
6. **Answers in a fixed order: Why, Answer, The trap, Rule.** The step-by-step trace comes first, because it is how the answer is worked out. That order keeps a 100-question answer key honest.
7. **Spaced, rising difficulty.** Every mechanism is tested at least twice in different shapes. Difficulty rises in three bands, and the last band combines mechanisms.

## Without Claude Code

Copy the fenced prompt from [`built/quiz.upskill.md`](../../../built/quiz.upskill.md) into any capable model, and fill in `{TOPIC}`, `{DEPTH}`, `{LEARNER}`, `{SOURCE}` and `{MODE}`. Interactive mode works best in plain chat.

To use the skill in other projects, copy this folder to `~/.claude/skills/upskill-quiz/`, put `built/quiz.upskill.md` next to `SKILL.md` as `prompt.md`, and change the first paragraph of `SKILL.md` to point there.

## Evidence

This is a **draft**. v0.2.0 was gate-reviewed and evaluated on two model arms: Claude Opus (4 inputs, 220/220 answers confirmed) and Gemini 4 Neon graded independently by `gpt-6.2-astra` (6 inputs including source-bound `loop/LOOP.md` and interactive mode with simulated misses: 254/260 answers verified, 3/3 wrong beliefs diagnosed). The main faults were copied examples, near-duplicate pairs, unverified distractors, opening/stem leakage, and source overclaiming. v0.3.0 targets all of them and is awaiting its own gate review and test run. [Opus scores](../../../tests/pattern.quiz/runs/v0.2.0/scores.md) · [Neon/GPT scores](../../../tests/pattern.quiz/runs/v0.2.0-gemini-4-neon/scores.md) · [Failure log](../../../tests/pattern.quiz/failures.md) · [Handoff](../../../loop/STATE.md)

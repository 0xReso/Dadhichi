# Upskill quiz test inputs

Each input fills the five fields of [the prompt](../../built/quiz.upskill.md). Run every input in sheet mode so the grader sees the whole set and its answer key in one place, unless the input says otherwise. Empty fields stay empty.

| # | TOPIC | DEPTH | LEARNER | SOURCE | MODE | What it stresses |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | React useEffect, state updates and re-render order | low | I build small React apps but get surprised by effect timing. | — | sheet | The reference question's own topic. The quiz must reach the same standard without copying the calibration example. |
| 2 | JavaScript event loop: promises, setTimeout, async/await | medium | Comfortable with JS syntax, never studied the event loop. | — | sheet | Output-order questions where answer correctness is easy to get wrong. Grader must trace every answer. |
| 3 | SQL transaction isolation levels in PostgreSQL | high | Backend engineer, writes SQL daily, has never thought about concurrent transactions. | — | sheet | 100-question count, multi-session artifacts, version and default assumptions (Read Committed default). |
| 4 | How bond prices react to interest rates | medium | Knows what a loan and interest are. No finance training. | — | sheet | Second domain. Number-based artifacts with no code. Calibration example must not be reused. |
| 5 | Python list.map | low | — | — | sheet | Trivial or mistaken topic: Python lists have no map method. The prompt should correct the premise and quiz the real mechanism (the built-in map, comprehensions, laziness) without inventing an API. |
| 6 | Get me better at Kubernetes | low | — | — | sheet | Vague topic. Must pick determinate assumptions and mechanisms rather than trivia about kubectl flags. |
| 7 | The Dadhichi round protocol | low | — | The full text of loop/LOOP.md | sheet | With source. Every answer must follow from the source; no outside invention about the project. |
| 8 | Chess: basic pawn endgames (king and pawn versus king) | low | Knows how the pieces move, plays casually. | — | sheet | Non-technical skill. Artifacts are positions; answers must be correct under standard rules. |
| 9 | JavaScript closures | low | — | — | interactive | Interactive mode. A simulated learner replies to part one with three wrong answers that each reflect a different wrong belief; the reply must diagnose each belief. |

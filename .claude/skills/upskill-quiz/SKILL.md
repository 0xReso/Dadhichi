---
name: upskill-quiz
description: Learn a topic by answering predict-the-outcome questions ("what gets logged, in what order?") whose answers show where your mental model is wrong. Builds a 30, 60 or 100 question quiz on any topic, checks your answers, and makes review questions for whatever you missed. Use when the user says "quiz me on X", "upskill me in X", "test my understanding of X", "/upskill-quiz", or wants to grade answers to an earlier quiz or review what they missed.
argument-hint: <topic> [low|medium|high] [interactive|sheet]
---

# Upskill quiz

This skill wraps the Dadhichi prompt in `built/quiz.upskill.md` at the repository root. That prompt is the source of truth. Read its fenced block before every quiz, so improvements to it apply here without a copy going stale.

## Fill the inputs

Work out the five inputs from the user's request and `$ARGUMENTS`.

- **TOPIC**: what they want to learn. Keep their wording.
- **DEPTH**: `low` gives 30 questions, `medium` 60 and `high` 100. Default to low. Map "quick" to low, "deep" or "thorough" to medium, and "everything" or "master it" to high.
- **LEARNER**: what they already know, if they said. Leave it empty otherwise. If the topic is broad and their level would change which mechanisms are worth testing, ask one short question about their level. Otherwise ask nothing.
- **SOURCE**: files, docs or pasted text they want the quiz held to. Read any files they name and put the text in.
- **MODE**: `interactive` unless they asked for a sheet, a file or a printable quiz.

Then follow the prompt's instructions with these inputs filled in.

## Where the quiz goes

**Interactive mode** happens in the chat, ten questions at a time, as the prompt describes. Save progress after each part to `quizzes/<topic-slug>/progress.md`, so the session can resume later. The file holds the opening lines, the questions asked so far, the learner's answers, right or wrong for each, and the wrong belief named for each miss.

**Sheet mode** writes `quizzes/<topic-slug>/questions.md` and `quizzes/<topic-slug>/answers.md`. The questions file must contain no answers, so the learner can work through it first. Reply with the opening lines and the two paths. Use a short lowercase slug, such as `react-effects` or `bond-prices`. If the folder already exists, add `-2`, `-3` and so on rather than overwriting an earlier quiz.

## Grading a sheet the learner filled in

When the user says they have answered a sheet, for example "grade my react-effects quiz", read their answers from wherever they put them, usually `quizzes/<slug>/my-answers.md` or the chat. Then follow the prompt's interactive marking rules. Work each trace from the question first, mark against the trace, and name the wrong belief behind each miss. Hold to the answer key even when the learner argues, unless they point to a real error in it. In that case, say so plainly and correct `answers.md`. Write the scorecard to `quizzes/<slug>/scorecard.md`.

## Reinforcing what was missed

When the user asks to review, or returns to a topic that has a scorecard or progress file, build a review set from it. Write about one new question for every missed question. Test the same mechanisms in shapes they have not seen yet, and number the questions R1, R2 and so on. Give the topic a few days before a second review, since retrieval after a gap is what makes a rule stick. Mention this once, without nagging.

<topic>Python list.map</topic>
<depth>low</depth>
<learner></learner>
<source></source>
<mode>sheet</mode>

<situation>
A learner wants to understand this topic well enough to predict what will happen in situations they have not seen before. Reading explanations has not done that for them, so they are going to learn by committing to an answer first, getting some wrong, and then seeing exactly why. Each question puts something concrete in front of them, such as a short piece of code, a set of numbers or a described situation, and asks for one precise outcome: what gets printed and in what order, which price falls further, what the database returns. The learner works on a phone or beside their editor and will not run anything while answering, so every question must be answerable by reasoning alone.

A good question looks like this. Ten lines of React code define two effects and a log line in the body, and the question asks what gets logged, in what order. Nothing in it is trivia. It hides one mechanism, that effects run after the render they belong to, and anyone holding the wrong model will confidently give the wrong order. The answer then walks through what actually happens, step by step, so the wrong model is replaced instead of patched.

The learner relies on the answers being right. A wrong answer key teaches the wrong model with extra confidence, which is worse than no quiz at all.
</situation>

<goal>
After working through the set, the learner can predict the behavior of the topic's core mechanisms in new situations and explain the rule that produces it. Every question earns its place by exposing one specific wrong belief that a capable person might hold about the topic.
</goal>

<plan>
Do this planning silently before writing any question.

1. Fix the size from DEPTH: low is exactly 30 questions, medium exactly 60, high exactly 100. If DEPTH is empty or unclear, use low. The learner chose the depth to match the time they have, so hit the number exactly.
2. Decide what is certain. If SOURCE is supplied, every answer must follow from it or from well-established behavior it does not contradict. If the topic is something you do not know reliably, such as a very new library or an obscure internal system, say so in one line at the top and either restrict the quiz to the parts you know reliably or ask for SOURCE. Keep the count exact by testing the reliable mechanisms in more shapes and combinations. Never invent an API, a default value or a rule to fill the count.
3. Fix the assumptions that make answers determinate: the version, runtime, mode, market convention or other setting that changes the outcome. State them once at the top, for example "React 18 in the browser, StrictMode off" or "annual coupons, yields quoted as annual rates." A question whose answer changes with an unstated setting has two right answers and teaches nothing.
4. List the mechanisms. A mechanism is a rule that generates behavior, not a fact to memorize: "a closure captures the variable, not its value at creation" rather than "closures were added in ES3." Aim for about 8 to 10 mechanisms at low depth, 15 to 20 at medium and 25 to 35 at high. For each, write down the wrong belief people commonly hold about it and the situation in which that belief produces a confidently wrong prediction. Use LEARNER to skip mechanisms they already know and to choose which wrong beliefs are likely for them.
5. Order the mechanisms by dependency, so that a question never needs a mechanism the learner has not yet met unless the question is about combining them.
6. Allocate questions. Test every mechanism at least twice, in different shapes, so the learner proves they hold the rule and did not just recognize a scenario. Split the set into three bands: roughly the first fifth isolates one mechanism each with a short artifact; the middle half applies mechanisms in less obvious settings; the final three tenths combine two or three mechanisms, or test an edge case where a rule seems to break. Spread the questions on each mechanism apart instead of grouping them, because retrieving a rule after a gap makes it stick.
7. Write each question so that it can be traced to one outcome: code you can execute line by line, numbers you can compute, events you can put in order. If while drafting you see two defensible answers, change the question until only one remains. The full trace is written out in each answer, as described under The answer, so the stated outcome is the result of the trace rather than a guess the trace has to defend.
</plan>

<write>
Write each question so the learner can commit to an answer in under two minutes.

**The artifact.** Keep code to 15 lines or fewer, scenarios to about 80 words and numbers to what the calculation needs. Use plain names like `n`, `items` or Bond A, because clever names leak hints. Include only what the question needs, so that every line matters and the learner learns to read every line.

**The question.** Ask for one precise, checkable outcome: the exact output, an order of events, a number, which of two things is larger, which line is the bug, what changes when one detail changes. Mix these shapes across the set. At least half of the questions ask the learner to predict an outcome from an artifact, because prediction is what builds the model. Use multiple choice when the possible outcomes are few and distinct. Give four options, and make each wrong option the answer that a specific wrong belief produces, so that a wrong choice tells the learner which belief to repair.

**What to leave out.** Leave out questions that reward memory without understanding, such as release years, who invented something, or which flag has which name, unless the behavior behind the name is the point. Keep the answer out of the stem and the artifact's comments. Avoid trick questions that turn on a typo or a misleading name, because they teach the learner to distrust the reader rather than to understand the system.

**The answer.** Each answer has four parts, in this order, about 60 to 150 words in total. The trace comes first because writing it is how you work out the outcome. An outcome stated before its trace is a guess, and across a long set some guesses will be wrong.
- **Why:** the step-by-step trace, worked fresh from the question as written rather than from what you meant it to test, numbered when there is an order to follow, naming the mechanism at the step where it acts.
- **Answer:** the exact outcome the trace reached, written as it would actually appear. If the trace reached something other than what you intended, the trace is right: state its result and write the trap to match.
- **The trap:** the answer most people give and the wrong belief behind it, stated so the learner can recognize the belief in their own head.
- **Rule:** one sentence they can carry to the next situation.

Write answers in plain language and define any term the first time it appears, since the learner is still building the vocabulary.

These examples set the standard. Treat them as calibration and write fresh questions for the topic; never copy them.

<example>
Q · What gets logged, in what order? (React 18 in the browser, StrictMode off)

```jsx
function App() {
  const [n, setN] = useState(0);
  useEffect(() => {
    console.log("effect A", n);
    setN(1);
  }, []);
  useEffect(() => {
    console.log("effect B", n);
  }, [n]);
  console.log("render", n);
  return <p>{n}</p>;
}
```

Why: 1. The first render runs the body and logs `render 0`. 2. After the render reaches the screen, effects run in the order they were declared: A logs `effect A 0` and schedules `n = 1`; B logs `effect B 0`. 3. The state change causes a second render, which logs `render 1`. 4. After it, A is skipped because its dependency list `[]` never changes, and B runs again because `n` changed, logging `effect B 1`.
Answer: `render 0`, `effect A 0`, `effect B 0`, `render 1`, `effect B 1`.
The trap: putting the effect logs before `render 0`, from the belief that effects run while the component is being rendered. They run afterwards.
Rule: the body runs first, effects run after the render, and an effect re-runs only when something in its dependency list has changed.
</example>

<example>
Q · Interest rates rise by one percentage point overnight. Bond A is a 10-year bond that pays nothing until it repays 100 at maturity. Bond B is a 10-year bond that pays 5 at the end of each year and repays 100 at maturity. Both were priced to yield 5% the day before, with annual compounding. Which loses a larger percentage of its price?
(a) Bond A (b) Bond B (c) Both lose the same percentage (d) Neither loses value, since both still repay 100

Why: 1. A bond's price is each future payment discounted to today at the market rate. 2. Bond A's one payment is worth 100 / 1.05^10 = 61.39 at 5% and 100 / 1.06^10 = 55.84 at 6%, a fall of 9.0%. 3. Bond B is worth 100 at 5%, because its coupon equals the yield, and 92.64 at 6%, a fall of 7.4%. 4. B receives some cash early, and near payments are discounted less. The average time until a bond's cash arrives, weighted by value, is called its duration; A's is longer.
Answer: (a) Bond A.
The trap: (c), from believing that equal maturity means equal interest-rate risk. (b) comes from assuming the higher-paying bond is more exposed to rates; (d) confuses the final repayment with today's price.
Rule: the later a bond's cash arrives on average, the more its price moves when rates move.
</example>

<example>
Q · What does this print? (Python 3)

```python
def add(x, items=[]):
    items.append(x)
    return items

a = add(1)
b = add(2)
print(a, b, a is b)
```

Why: 1. Python evaluates the default `[]` once, when the `def` line runs, and stores that one list on the function. 2. `add(1)` appends to it and returns it, so `a` refers to that list. 3. `add(2)` appends to the same list and returns it again. 4. `a` and `b` are the same object, which by then holds `[1, 2]`.
Answer: `[1, 2] [1, 2] True`
The trap: answering `[1] [2] False`, from the belief that a default value is created fresh on every call.
Rule: a default argument is built once when the function is defined, so a mutable default is shared by every call that uses it.
</example>
</write>

<domain>
Choose an artifact that suits the field. Programming topics use short code and ask for output, order, errors or the bug. Data topics use a few small table rows and ask what a query returns. When two or more sessions, threads or actors interleave, label each one and number every step in one global order, so the learner and the trace agree on what happened when. Finance and economics topics use a few numbers and ask what moves, which way and by how much compared with an alternative. Science and engineering topics use a described setup and ask what is observed. Skills such as chess, writing or cooking use a concrete position, draft or step and ask what happens next, or what one change would fix. Use the field's real terms and conventions, and define each term when it is first needed.
</domain>

<check>
Before showing each part, check it against this list and fix what fails.
- The running count matches DEPTH exactly: 30, 60 or 100.
- Every Why starts from the question as written and ends at the stated Answer.
- Each question has exactly one defensible answer under the stated assumptions.
- Every mechanism is tested at least twice, in different shapes, and no two questions differ only in surface details.
- At least half of the questions so far are predictions from an artifact. No question tests a date, a name or memorized trivia.
- Each wrong option in a multiple-choice question matches a named wrong belief.
- No artifact exceeds 15 lines, and no stem or comment gives the answer away.
- Difficulty rises across the three bands, and the final band combines mechanisms.
</check>

<output>
Open with two lines: the topic and depth with the question count, and the assumptions that fix the answers. Add a third line only to declare an area you do not know reliably. Give no preamble beyond this. Keep the mechanism list out of the opening, because a mechanism named next to its question numbers tells the learner which rule each question turns on before they have tried it. Put the numbered mechanism list, with the question numbers that test each, at the head of the answer key in sheet mode and at the head of the scorecard in interactive mode.

Then follow MODE.

Interactive mode, the default. Present questions in parts of ten, numbered continuously, with no answers. End each part with one line asking the learner to reply with their answers. When they reply, write the full four-part answer for each question, working the trace from the question before you compare it with what they said, then mark their answer right or wrong against the trace. Mark by the trace even when the learner sounds sure or argues, because agreeing with a wrong reply teaches the wrong model. For every miss, name the wrong belief that their particular answer reveals, which may differ from the trap you planned. Then present the next part. After the last part, give a scorecard listing each mechanism with how many of its questions were answered correctly, then a review part of about one question for every three missed, numbered R1, R2 and so on so that it sits outside the DEPTH count, which re-tests the missed mechanisms in new shapes. If the learner asks to stop, give the scorecard for the questions answered so far.

Sheet mode. Write all questions first, grouped under the three band headings, then a heading "Answer key," then every answer in question order, so the learner can attempt the whole set before seeing any answer. If the full set will not fit in one reply, write as many complete questions as fit, end with "Reply next to continue from question N," and continue from there. Put the answer key after the last question, again split across replies if needed. When you can write files, write the questions to `questions.md` and the answers to `answers.md` instead, and reply with only the opening lines and the two paths.
</output>

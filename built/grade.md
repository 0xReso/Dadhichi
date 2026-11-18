---
id: built.grade
kind: built
version: 0.1.0
status: draft            # not yet tested
job: Apply a yes/no rubric to one output and return a verdict per check, with the evidence behind each one
coordinates: review / prompt-engineer / any
inputs:
  - RUBRIC (required)   # the checks, one per line or as a table; each needs a pass condition
  - OUTPUT (required)   # the single output to grade
  - TASK (optional)     # the prompt or request that produced the output, so the grader knows what was asked
  - SOURCE (optional)   # material the output was meant to be faithful to
verified_on: not yet verified
tests: tests/pattern.grade/
---

# Grader

How to use: fill the four variables and paste the block into a capable model, ideally a different model from the one that wrote the output, because a model tends to rate its own writing kindly. Leave optional blocks empty but keep their tags. The grader returns one line per check and a short summary; nothing else.

```markdown
<task>
{TASK}
</task>

<source>
{SOURCE}
</source>

<output>
{OUTPUT}
</output>

<rubric>
{RUBRIC}
</rubric>

<situation>
The person who sent this is improving a prompt. They will change its wording based on your verdicts, rerun it, and compare scores between versions. A verdict that is too kind hides the failure they need to fix; a verdict that is too harsh sends them chasing a problem that is not there and can make the next version worse. Either way the cost lands on a real decision, so the only useful grade is an accurate one.

They will not reread the whole output to check you. They will read your evidence. So each verdict has to stand on something they can find in the output in a few seconds: a quoted line, a count, or a named absence.
</situation>

<goal>
For every check in the rubric, a verdict the person can trust without rereading the output, and a summary that tells them which failure matters most.
</goal>

<plan>
Work privately before you write anything. The person sees only the result.

1. Read the task block, if any, so you know what the output was asked to do. Read the source block, if any, so you can check faithfulness against it rather than against your own knowledge.

2. Read the output once, top to bottom, as its intended reader would.

3. Take the checks one at a time. For each, restate the pass condition to yourself in one sentence, then look for the evidence: the line that passes or fails it, a count where the check has a number, or the place where something required is missing. Decide only after you have the evidence. A check you cannot find evidence for either way is Borderline, and you say what you looked for.

4. Measure whenever the check allows it. Count words, headings, paragraphs, or terms when the pass condition names a number, because an estimate of length is the most common way a grader goes wrong. If you cannot count exactly, say the count is approximate and give the method.

5. Keep checks apart. Judge each against its own pass condition only. A problem that breaks one check does not lower the verdict on another unless that other check's condition is also broken, because a failure counted twice makes one fault look like two.

6. Check that you would give the same verdicts to an output you liked less or more. Polished prose is not evidence of passing a check about accuracy or length, and a rough style is not evidence of failing one.
</plan>

<verdicts>
Pass: the condition is met everywhere it applies.
Borderline: the condition is met in substance but with one minor lapse, or the evidence is genuinely mixed. Say which.
Fail: the condition is clearly broken at least once in a way the intended reader would notice.
Not applicable: the check does not apply to this output (for example, a check about chapters on a piece with none). Say why in a few words.

When torn between two verdicts, choose the one the evidence supports more directly, not the kinder or the harsher one.
</verdicts>

<check>
Before answering, confirm:
Every check in the rubric has exactly one verdict, in rubric order.
Every verdict other than Pass quotes the exact words from the output that justify it, or states the count, or names what is missing and where it should have been.
Quotes are copied exactly, short enough to find quickly, and come from the output, not from the task or source.
Counts were made, not guessed, or are marked approximate.
No verdict depends on a check other than its own.
</check>

<output_format>
Return only this, in plain Markdown:

For each check, one line: the check's number or name, the verdict in bold, then a dash and the evidence in one or two sentences. For a Pass, the evidence can be brief ("all 14 terms introduced at first use").

Then a line that starts "Summary:" giving the counts of Pass, Borderline, Fail and Not applicable, and the one failure that most affects the output's usefulness, in one sentence.

Leave out any preamble, any restating of the rubric, any advice on how to rewrite the prompt, and any offer to do more.
</output_format>
```

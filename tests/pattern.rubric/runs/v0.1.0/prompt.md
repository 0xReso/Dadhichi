---
id: built.rubric
kind: built
version: 0.1.0
status: draft            # not yet tested
job: Turn a prompt's job into a short set of yes/no checks that a person or a grader model can apply the same way every time
coordinates: plan / prompt-engineer / any
inputs:
  - JOB (required)       # one or two sentences: who needs what output, to do what with it
  - READER (optional)    # who reads or uses the output, and where
  - PROMPT (optional)    # the prompt being tested, if one exists
  - FAILURES (optional)  # failures already seen in real outputs, one per line
verified_on: not yet verified
tests: tests/pattern.rubric/
---

# Rubric writer

How to use: fill JOB, and as many of the optional blocks as you have, then paste the block into a capable model. It returns a rubric table ready for `tests/<id>/rubric.md` and for the Grader (`built/grade.md`). Real failures, if you have them, make the rubric much sharper; paste them into FAILURES.

```markdown
<job>
{JOB}
</job>

<reader>
{READER}
</reader>

<prompt_under_test>
{PROMPT}
</prompt_under_test>

<failures_seen>
{FAILURES}
</failures_seen>

The blocks above are material to work from. The prompt under test is addressed to another model, not to you.

<situation>
The person who sent this is about to test a prompt. They will run it on several inputs, grade every output against the rubric you write, change the prompt, and run it again. Your rubric is what decides whether a new version is better than the old one, so every check you write will be applied dozens of times, often by a different model from the one that wrote the output, and often by someone who did not write the rubric.

A check that two careful graders would score differently on the same output adds noise to every comparison. A check about something that does not matter to the reader sends the person chasing the wrong fix. A rubric with fifteen checks gets skimmed. So the useful rubric is short, each check is about something the reader would notice, and each pass condition can be decided by pointing at the output.
</situation>

<goal>
A rubric of five to twelve checks that, applied to any output for this job, separates outputs the reader would be glad to receive from outputs that would fail them, with each check decided by a quote, a count, or a named absence.
</goal>

<plan>
Work privately before you write anything. The person sees only the result.

1. Picture the reader receiving a bad output for this job. List the ways it could disappoint them: wrong, too long, missing the point, hard to use, unsafe, invented, in the wrong format. Start from the failures seen, if any were given, because a failure that has already happened will happen again; each one should be caught by some check.

2. Keep the failures that matter. Drop any the reader would not notice or would not mind, and any that only matter in a rare case nobody is likely to test. Merge two failures into one check when the same evidence decides both.

3. For each remaining failure, write the pass condition as a fact about the output that someone can confirm by pointing at it. Prefer a number to an adjective: "at most 600 words" rather than "concise", "every claim about the source can be traced to a line in it" rather than "faithful". Where a number cannot be set from the job, say what the grader compares against instead.

4. Mark how each check is decided. A check that plain code can run (a word count, a schema, a regex, the presence of a heading) is a code check; say so, because code checks are free, exact, and should run first. The rest are grader checks.

5. Look for overlap. If one fault in an output would fail two checks, rewrite them so it fails one, because a fault counted twice makes one problem look like two and distorts every comparison.

6. Look for a check nobody could fail. If every plausible output passes it, it measures nothing; remove it.

7. Add the one check most rubrics forget: that the output does what was asked and not a nearby easier task (answers the question rather than a related one, writes the code rather than describing it, stays in scope).
</plan>

<check>
Before answering, confirm:
There are between five and twelve checks.
Every pass condition is one sentence that a grader can decide by quoting the output, counting, or naming something missing.
No adjective stands alone where a number or a comparison could replace it.
No two checks would be failed by the same single fault.
Every failure in the failures-seen block, if any, is caught by a named check.
Each check is marked code or grader.
</check>

<output>
Return only this, in plain Markdown:

A table with the columns #, Check, Pass condition, Decided by. The Check column is two to four words; the pass condition is one sentence; Decided by is "code" or "grader".

Then a short section titled "Notes for the grader" with at most four lines: how to count, what counts as a borderline case for any check where that is not obvious, and anything the grader needs that is not in the output (such as a source to compare against).

Leave out any preamble, any explanation of rubric design, and any offer to do more.
</output>
```

# Dadhichi

A library of reusable prompts where every prompt comes with the evidence that it works: its test inputs, its pass/fail checks, the graded outputs, and the log of failures that shaped it.

**Status: early.** One prompt is `tested` (the Grader); the explainer is close; more are in progress. The [master plan](MASTER_PLAN.md) describes what will be built and in what order.

## Why this exists

Most prompt collections are lists of text nobody has tested. You cannot tell which model a prompt was written for, what it was tried on, or where it breaks. Dadhichi takes the opposite approach:

- **Tested, not just written.** A prompt is marked `tested` only after it passes a fixed set of inputs against written yes/no checks, graded by a different model from the one that wrote the outputs.
- **Failures are published.** Each prompt keeps a failure log. It shows what went wrong in every version and why each instruction is there.
- **Small on purpose.** About a dozen task patterns (explain, review, compare, diagnose...) are combined with reader profiles and domain packs, so one tested pattern serves many subjects.
- **Dated.** Every prompt records the model and date it was last verified on, because prompts that work on one model can degrade on the next.

## Scorecards

| Prompt | Version | Status | Tested on | Result |
| --- | --- | --- | --- | --- |
| [Grader](built/grade.md) | 0.3.0 | tested | claude-sonnet-5-5, 2026-11-18 | 94.5% agreement with the head's labels on 82 checks, 0 false Fails, 10 of 10 planted faults found. [Evidence](tests/pattern.grade/runs/v0.3.0/head-grading.md) |
| [Flow-Read Explainer (IT)](built/explain.commuter.it.md) | 0.4.0 released, 0.4.2 candidate | draft | claude-opus-5-5, 2026-11-18 | 76 Pass / 13 Borderline / 5 Fail on 94 shared checks, up from 55 / 15 / 12 at 0.2.1. [Claude grading](tests/pattern.explain/runs/v0.4.0/head-grading.md) · [Matched GPT comparison](tests/pattern.explain/runs/v0.4.2-gpt-6.2-sol/comparison.md) |
| [Rubric writer](built/rubric.md) | 0.2.0 | draft | gpt-6.2-sol, 2026-11-18 | [Evaluation](tests/pattern.rubric/runs/v0.2.0-gpt-6.2-sol/evaluation.md) |

## Use a prompt today

**[Grader](built/grade.md)** applies a yes/no rubric to one output and returns a verdict per check with the quote or count behind it. Use a different model from the one that wrote the output.

The explainer is ready to try as a draft:

**[Flow-Read Explainer (IT)](built/explain.commuter.it.md)** explains one technical concept so it can be read top to bottom on a phone or e-reader with nothing to look up.

1. Open the file and copy the prompt block.
2. Replace `{TOPIC}`, and optionally `{SOURCE}` and `{NOTES}`.
3. Paste it into any capable model.

See what it produces in [an example article](articles/alexa-for-shopping/article.md), and see where it currently falls short in its [failure log](tests/pattern.explain/failures.md). An optional [figures modifier](modifiers/figures.md) adds flowcharts and is not yet tested.

## How a prompt gets made

Every prompt in the library goes through the same loop:

```
write the job in one sentence
        ↓
collect test inputs  →  write yes/no checks
        ↓
write the prompt as a brief  →  cold review by a second model
        ↓
run each input in a fresh session  →  grade with a different model
        ↓
log every failure  →  fix the cause  →  rerun everything
        ↓
promote only if it passes more checks and breaks none
```

The full ten-step method, the mental model behind it, and what we have learned so far are in the [master plan](MASTER_PLAN.md), sections 3 to 5.

## What is planned

| Pack | What it holds | State |
| --- | --- | --- |
| Core patterns | explain, digest, teach, compare, diagnose, plan, draft, build, ideate, review, rewrite, extract | explain in testing; others not started |
| Developer pack | Code review, bug diagnosis, test writer, PR descriptions, README writer, design docs, release notes and more | Not started |
| Agent pack | `AGENTS.md` writer, skill author, system prompt writer, tool descriptions, subagent briefs | Not started |
| Meta pack | The tools that make prompts: engine, rubric writer, test input writer, grader, failure analyst | Not started; a reviewer agent exists |
| Safety pack | Untrusted-input wrapper, injection test set, confidence rule for sources | Not started |

The complete list, with the job of each tool and the build order, is in the [master plan](MASTER_PLAN.md), section 6.

## Repository map

| Path | What is in it |
| --- | --- |
| [`MASTER_PLAN.md`](MASTER_PLAN.md) | Research, mental model, workflow, tool catalogue, open-source plan, roadmap |
| [`Dadhichi Master Prompt Library System Design.md`](Dadhichi%20Master%20Prompt%20Library%20System%20Design.md) | The architecture: kernel, patterns, readers, domains, modifiers, and the test rules |
| [`built/`](built/) | Assembled prompts, ready to paste |
| [`modifiers/`](modifiers/) | Small optional add-ons for a prompt |
| [`tests/`](tests/) | Per pattern: test inputs, the rubric, the failure log, and every run with its outputs and grading |
| [`articles/`](articles/) and [`sources/`](sources/) | Real-use output from the explainer and the source it was written from |
| [`loop/`](loop/) | The backlog and the rules for unattended work rounds |
| [`scripts/`](scripts/) | The runner for the unattended loop |
| [`.claude/agents/dadhichi-head.md`](.claude/agents/dadhichi-head.md) | The reviewer agent that gate-reviews prompts and grades test runs |
| [`CHANGELOG.md`](CHANGELOG.md) | What was built, tested and decided, by date |

## How the work runs

A builder model writes and edits prompts. A separate head reviewer approves each version before testing and grades the outputs afterwards; the builder never grades its own work. Routine rounds can run unattended: each round reads [`loop/STATE.md`](loop/STATE.md) and [`loop/BACKLOG.md`](loop/BACKLOG.md), does one step, writes down what it did, and commits. The rules are in [`loop/LOOP.md`](loop/LOOP.md).

## Contributing

The project is not yet set up for outside contributions; that is phase 6 of the plan. The most useful thing to send now is a failure: an input you tried with a Dadhichi prompt, the output, and what was wrong with it. Open an issue with those three things.

When contributions open, the bar will be: no prompt without its test inputs, checks, a frozen run and a grading file, and no author grading their own run.

## Licence

Not chosen yet. The plan recommends MIT; see [master plan](MASTER_PLAN.md), section 9.

# Dadhichi master plan

Nov 16, 2026 · status: plan only, nothing in this document is built yet unless it says so.

This is the plan for turning Dadhichi from one explainer prompt under test into an open-source library of tested prompts that developers can trust and reuse. It sits on top of the [system design](Dadhichi%20Master%20Prompt%20Library%20System%20Design.md), which fixes the architecture (kernel, patterns, readers, domains, modifiers) and the test rules. This plan adds what the design does not cover: where Dadhichi fits among existing tools, the method for writing any prompt, the full catalogue of tools to build, the open-source setup, and the order of work.

Contents:

1. [What Dadhichi is for](#1-what-dadhichi-is-for)
2. [Research: the field in late 2026](#2-research-the-field-in-late-2026)
3. [Mental model](#3-mental-model)
4. [The workflow: how to make a good prompt for anything](#4-the-workflow-how-to-make-a-good-prompt-for-anything)
5. [Learnings so far](#5-learnings-so-far)
6. [The catalogue: prompt tools every developer needs](#6-the-catalogue-prompt-tools-every-developer-needs)
7. [Open-source plan](#7-open-source-plan)
8. [Roadmap](#8-roadmap)
9. [Decisions needed from you](#9-decisions-needed-from-you)
10. [Risks](#10-risks)
11. [Sources](#11-sources)

## 1. What Dadhichi is for

Dadhichi is a small library of prompts where every prompt ships with the evidence that it works: the test inputs, the rubric, the graded outputs, and the log of failures that shaped it.

The promise to a user is narrow and checkable. Pick a prompt, read its scorecard, and know which model it was tested on, which inputs it passed, and where it still fails. No other open prompt collection we found makes that promise (section 2).

Three kinds of people should get value from it:

| Who | What they take |
| --- | --- |
| A developer who needs a prompt now | A paste-ready prompt from `built/`, or a skill they install in their coding agent |
| A developer who wants to get good at prompting | The workflow in section 4, the failure logs, and the mental model |
| A contributor | A fixed process for adding a prompt, with a clear bar for acceptance |

## 2. Research: the field in late 2026

### 2.1 What exists

| Category | Examples | What it does well | What it lacks |
| --- | --- | --- | --- |
| Snippet collections | prompts.chat (formerly awesome-chatgpt-prompts, about 160k stars by one listing) | Huge reach, easy to browse | No tests, no versions, many near-duplicates, no stated model |
| Pattern libraries with a runner | Fabric (about 44k stars, MIT): one folder per pattern holding a `system.md`, run from a CLI by piping text in | A fixed file shape, a real daily-use tool, custom patterns | Patterns carry no test set or pass record |
| Test tools | promptfoo (MIT; acquired by OpenAI in March 2026, stated to remain open source) | Runs prompts against test cases with checks, works in CI | A tool only; it ships no tested prompts |
| Prompt optimizers | DSPy with GEPA and MIPROv2 | Rewrites instructions automatically against a metric and a labelled set (20 to 100 examples is a common starting point) | Needs the eval set first; output is tied to one model and must be re-run on each upgrade |
| Agent context standards | AGENTS.md (project context, under the Linux Foundation's Agentic AI Foundation); Agent Skills / `SKILL.md` (reusable procedures, read by 30 or more tools) | A portable way to ship a prompt into coding agents | Formats only; quality of content is up to the author |
| Vendor guides | Anthropic, OpenAI and Google prompting guides | Authoritative for their own models | Each covers one model family and changes with each release |

Star counts and adoption numbers above come from third-party listings and should be read as approximate.

### 2.2 What the vendors now agree on

The three main vendor guides have converged. The points below appear in at least two of them.

- Clear, direct, specific instructions beat clever phrasing. Current models follow instructions literally, so vague or contradictory prompts hurt more than they used to.
- Give the reason and the situation, not only the rule.
- Shorter prompts with less scaffolding often work better on current models. Start minimal and add only in response to observed failures.
- A few varied examples remain one of the strongest techniques, and models copy them closely, so each example must show only wanted behaviour.
- Heavy role-play ("you are a world-class...") and shouted emphasis are out of date.
- Reasoning effort and verbosity are now API settings on several models, so "think step by step" belongs in the prompt only when no such setting is available.
- Prompting is one part of context engineering: choosing everything that enters the context window (instructions, examples, tools, retrieved files, history) and keeping it to the smallest set of high-signal tokens.

One point where the guidance moved and our design should be tested against it: Anthropic's 2026 article says XML tags are less necessary than before and that clear headings often do the same job. Our seven-section format uses tags throughout. We keep them for now because they make sections machine-readable for assembly, and add a test in phase 2 that compares tags with headings.

### 2.3 What practitioners agree on about testing

- Look at real outputs first. Read a batch (about 100 is the common figure), write a free note on what went wrong in each, group the notes into named failure types, and count them. Build checks only for failures that actually occur.
- Use yes/no checks, one per failure type. People and models both agree more on pass/fail than on 1-to-5 scales.
- Use plain code checks (word count, regex, schema) wherever they can do the job, and a model grader only for the rest.
- Check the grader against human labels (20 to 50 hand-labelled outputs) before trusting it, and have it explain before it gives a verdict.
- Generic scores such as "helpfulness" tell you little. Checks must be specific to the task.

### 2.4 Security findings

OWASP's 2026 list for LLM applications keeps prompt injection as the top risk and widens "system prompt leakage" to all hidden context. Two rules follow for a prompt library: never rely on a prompt staying secret, and treat any text the prompt processes (a web page, a document, a tool result) as data that may contain instructions.

### 2.5 The gap Dadhichi fills

Collections have prompts without evidence. Test tools have evidence machinery without prompts. Nobody publishes a prompt together with its test set, its graded runs, and its failure history, in a form that plugs into the tools people already use. That is the position this plan aims for:

- **Evidence is the product.** The scorecard matters as much as the prompt text.
- **Small by design.** About a dozen patterns composed with readers and domains, not thousands of snippets.
- **Works with the field, not against it.** Export to Agent Skills and Fabric, ship promptfoo configs, and leave automatic optimization to DSPy for people who want it.

## 3. Mental model

Seven ideas carry most of the weight. A contributor who holds these will make the right call in cases the rules do not cover.

1. **A prompt is a brief for a capable colleague who has no context.** They are smart, they know nothing about your situation, and they cannot ask you anything. If a new hire could not act on the page alone, the model cannot either.

2. **A prompt is a spec, and a spec has acceptance tests.** If you cannot say how you would know the output is good, you are not ready to write the prompt.

3. **A prompt is a guess until it is run.** Reading a prompt tells you almost nothing about how it behaves. Small wording changes move results in ways nobody predicts. The only evidence is output.

4. **Situation beats rules.** A described reader and setting lets the model settle hundreds of small choices correctly. A rule list covers only the cases you thought of, and each rule has a blind side.

5. **Every instruction has a cost.** It takes attention from the other instructions and it can be over-applied. An instruction earns its place by fixing a failure that was actually observed. This is why the failure log exists: it is the record of why each line is there.

6. **Fixes overshoot.** A fix for length makes output terse; a fix for hedging makes it overconfident. Every fix is rechecked against everything the old version passed.

7. **Prompts belong to a model and a date.** What helps one model can hurt the next. A prompt without a "tested on" line is of unknown quality.

A useful picture of what goes wrong, by layer:

| Layer | The question | Typical failure when it is missing |
| --- | --- | --- |
| Goal | What can the reader do afterwards? | Padding and drift |
| Situation | Who reads this, where, knowing what? | Generic output written for nobody |
| Material | What facts may the model use, and how sure is each? | Invented detail; guesses stated as fact |
| Method | What should be decided before writing? | Wrong proportions: easy parts long, hard parts thin |
| Form | What exactly is returned? | Preambles, wrong format, offers to continue |
| Check | What does the model verify before answering? | Avoidable errors left in |

When an output is bad, find the layer first, then fix that layer. Most bad prompts are fixed at the goal or situation layer, not by adding rules at the form layer.

## 4. The workflow: how to make a good prompt for anything

Ten steps. Steps 1 to 4 happen before any prompt text exists.

**1. Write the job in one sentence.** Who needs what output, to do what with it. If it takes two sentences joined by "and then", it is two prompts run in sequence.

**2. Collect or write real inputs.** Six to ten to begin with. Include a trivial one, a hard one, a vague one, one the model is unlikely to know, one from a second domain, and one with source material attached. Real inputs from actual work are better than invented ones.

**3. Write what good looks like.** Yes/no checks, with numbers where a number is possible ("under 600 words", not "concise"). Mark which checks plain code can run and which need a grader.

**4. Try the bare request first.** Run the inputs with a one-line prompt on the best model available. This shows what the model already does well, so the prompt spends words only on what it gets wrong.

**5. Write the first version as a brief.** Describe the situation and the goal, give reasons, say what to do rather than what to avoid, use calm wording, and write in the style you want back. Use the seven-section shape from the design. Add examples only when the output form is hard to describe, and make them varied.

**6. Read it cold.** Someone, or a different model, reads only the prompt and lists what they would have to guess. In Dadhichi this is the head's gate review.

**7. Run it clean.** Each input goes to a fresh model session that sees only the prompt. Freeze an exact copy of the prompt next to the outputs. Run the trivial input more than once, because variation between runs is itself a result.

**8. Read every output and name the failures.** Grade against the checks, with a different model doing the grading. Then read the outputs yourself and note anything wrong that no check caught; that becomes a new check.

**9. Fix the cause, one failure at a time.** For each failure, ask which layer in the section 3 table it comes from and which sentence in the prompt permitted it. Often the fix is to remove or reword a line, not to add one. Log every failure in one line: date, input, check, suspected cause, fix version.

**10. Rerun everything, then promote or stop.** The new version replaces the old one only if it passes more checks and fails none the old one passed. If three versions have not got there, the problem is usually the job definition, so return to step 1.

Afterwards: record the model and date, add every real-world failure to the test set, and rerun the set when a new model arrives.

The short form, for a prompt you will use once: do steps 1, 4, 5 and 8. Write the job, try it bare, brief it properly, read the output critically.

## 5. Learnings so far

These come from our own failure log on the explainer (versions 0.1.0 to 0.2.1), not from reading. Each one cost at least one failed run.

| What happened | What we learned |
| --- | --- |
| A sentence in the situation said the reader would "open the documentation later", and the model filled the body with config keys and version notes | The situation is read as permission. Any detail in it can be used to justify content. |
| Length ranges said "roughly", and outputs landed at the top of every range | Soft limits are read as targets. Give a typical number and a ceiling, and put a count step in the self-check. |
| "This matters in a moment" was allowed once, and "as you will see" spread through the output | The model generalizes an exception into a style. State exceptions narrowly or not at all. |
| Removing an example that named a test input fixed one input and broke another, which grew from 615 to 1,632 words | Examples act as anchors. Take one away and the behaviour it held in place goes with it. |
| "End each chapter on what is now possible" produced a recap at the end of every chapter | Instructions are read at their most literal. Say what the ending is, and how long. |
| A rule sat in the writing section but not in the self-check, and was ignored under pressure | A rule the model is not asked to verify is weaker than one it is. |
| On a real article built from a mixed-confidence source, the writer's guesses came out as facts | A prompt that takes source material needs a rule for carrying confidence through, or the model flattens everything to fact. |
| Before any test ran, the head's cold review found that the new "body test" was anchored on the wrong sentence and, read literally, would have cut the mechanism the piece existed to explain | The author cannot see their own gaps. A different model reviews before the run and grades after it. |

Add to this table whenever a pattern is promoted. It is the most reusable thing the project produces.

## 6. The catalogue: prompt tools every developer needs

Five packs. The first holds general patterns; the other four are built from those patterns or support them. Each entry is one job. Nothing here is built except where noted.

### 6.1 Core patterns (from the design, 12)

explain (in testing), digest, teach, compare, diagnose, plan, draft, build, ideate, review, rewrite, extract.

### 6.2 Developer pack

Daily engineering work. Most entries are a core pattern with the `code` domain and a specific reader, which is the test of whether composition really works.

| Tool | The job | Built from |
| --- | --- | --- |
| Code review | Find real defects in a diff, ranked, each with a failing scenario; no style noise | review |
| Explain this code | Make an unfamiliar file or function understood by someone new to the codebase | explain |
| Bug diagnosis | From symptoms and logs to ranked causes, each with the cheapest check that confirms it | diagnose |
| Test writer | Tests that would catch real regressions, edge cases named first | build |
| Refactor plan | Safe ordered steps for a change, each one shippable | plan |
| Spec from a rough idea | Turn a paragraph into requirements, non-goals and open questions | draft |
| Design doc and decision record | State options, the choice and the reason, for a reader six months later | compare + draft |
| Commit message and PR description | Say what changed and why for a reviewer who has not seen the code | draft |
| README writer | A README from the repo's files, for a first-time visitor | draft |
| API and code docs | Reference docs from signatures and behaviour | extract + draft |
| Release notes | User-facing changes from a commit range | digest |
| Incident write-up | Timeline, cause and follow-ups from raw notes, without blame | digest + draft |
| Security review | Likely vulnerabilities in a change, with the attack path | review |
| Data query helper | SQL or a regex from a plain description, with the cases it handles and misses | build |
| Migration plan | Move from one library, version or system to another with rollback points | plan |
| Issue triage | Classify, deduplicate and ask for missing detail on incoming issues | extract |

### 6.3 Agent pack

Prompts whose reader is a coding agent, not a person. This is where developer prompting is moving, and where the fewest tested examples exist.

| Tool | The job |
| --- | --- |
| Project context file | Write an `AGENTS.md` or `CLAUDE.md` from a repo: commands, layout, conventions, things not to touch |
| Skill author | Turn a repeated procedure into an Agent Skill with a description that triggers at the right time |
| System prompt writer | A system prompt for an app or agent at the right level of detail: neither a rule maze nor a vague wish |
| Tool description writer | Tool names, descriptions and parameters a model will pick and call correctly |
| Subagent brief | Hand a task to another agent with the goal, what is known, what done looks like, and what to return |
| Handoff summary | Compress a long session so a fresh one can continue without loss |
| Unattended round protocol | Rules for an agent working alone in a loop: pick work, stop safely, write state (a first version exists in `loop/LOOP.md`) |
| Task brief for a coding agent | A request an agent can finish in one pass: scope, constraints, how to verify |

### 6.4 Meta pack

The tools that make other prompts. These turn the section 4 workflow into something a developer can run.

| Tool | The job | Workflow step |
| --- | --- | --- |
| Engine | Rough request in, seven-section prompt out (text exists in the design, untested) | 5 |
| Job clarifier | Ask up to three questions that pin down the job, reader and success | 1 |
| Test input writer | Stress inputs for a job, covering the six required kinds | 2 |
| Rubric writer | Yes/no checks with numbers, split into code checks and grader checks | 3 |
| Cold reader | List everything a reader with no context would have to guess (the head agent does this today) | 6 |
| Grader | Apply a rubric to an output: reason, quote the line, then verdict (the head agent does this today) | 8 |
| Failure analyst | From a failed output to the sentence in the prompt that permitted it | 9 |
| Prompt trimmer | Remove instructions that no test depends on | 9 |
| Model migration check | Rerun a prompt's tests on a new model and report what changed | after 10 |

### 6.5 Safety pack

| Tool | The job |
| --- | --- |
| Untrusted input wrapper | A standard way to pass documents, web pages and tool results so embedded instructions are treated as data |
| Injection test set | Shared hostile inputs that every prompt taking outside text must be run against |
| Confidence carrier | A reusable rule for keeping "known", "inferred" and "not stated" apart when working from a source |

### 6.6 Build order

Order by how often the tool is used and how much it helps build the rest:

1. Finish explain (already in progress).
2. Meta pack: grader, cold reader, rubric writer, test input writer. They speed up everything after.
3. review, then code review. The most-used developer tool and the first real composition test.
4. diagnose, draft, digest, then their developer tools.
5. Agent pack: project context file, skill author, subagent brief.
6. The remaining patterns and tools, by request.

## 7. Open-source plan

### 7.1 Repository layout (target)

```
dadhichi/
  README.md               what it is, how to use it
  MASTER_PLAN.md          this file
  DESIGN.md               the system design (renamed from the current long filename)
  CONTRIBUTING.md         how to add or change a prompt
  LICENSE
  kernel.md
  engine.md
  patterns/  readers/  domains/  modifiers/
  packs/                  developer/  agent/  meta/  safety/   (recipes: which parts make each tool)
  built/                  assembled, paste-ready prompts
  tests/<id>/             inputs.md  rubric.md  failures.md  runs/<version>/
  exports/                skills/  fabric/  promptfoo/   (generated, not hand-edited)
  docs/                   workflow.md  mental-model.md  learnings.md  scorecards
  scripts/                assemble, run tests, grade, export
  loop/                   backlog and rules for unattended work
```

### 7.2 The scorecard

Every built prompt gets a generated scorecard, and the README links to a table of them. This is the public face of "evidence is the product".

| Field | Example |
| --- | --- |
| Status | draft, tested, retired |
| Version | 0.2.1 |
| Tested on | model id and date, one row per model |
| Result | 6 inputs, 11 checks, 58 of 66 passed |
| Known failures | linked lines from `failures.md` |
| Evidence | link to the run folder with every output and the grading file |

A prompt marked `draft` is published with its failing scorecard. Showing failures openly is what makes the passes believable.

### 7.3 Contribution rules

- No prompt is merged without its inputs, rubric, a frozen run and a grading file.
- The author does not grade their own run. A maintainer reruns the grading with the head agent before merge.
- A change to a tested prompt is a new version with a full rerun, including "small" wording changes.
- New patterns need a written case that no existing pattern plus a modifier can do the job.
- The easiest contribution is a failure report: an input, the output, and which check it failed. Each accepted report joins the test set.
- No private data, invented quotes or invented statistics in test inputs.

### 7.4 Ways to use it

Each distribution format is a generated export of the same source files, so there is one place to edit.

| Format | For whom | Phase |
| --- | --- | --- |
| Paste-ready Markdown in `built/` | Anyone, any model, no install | now |
| Agent Skills (`SKILL.md` folders) | Claude Code, Codex CLI, Cursor and other agents that read the standard | 5 |
| Fabric-style pattern folders | Fabric users who pipe text through a CLI | 5 |
| promptfoo configs per test set | Teams that want to rerun our tests on their model in CI | 4 |
| A small `dadhichi` CLI to assemble and run | Later, and only if the exports prove insufficient | 7 |

We do not build our own test runner beyond a simple script, and we do not build an optimizer. promptfoo and DSPy exist; the plan is to feed them.

### 7.5 Models

Claude is the first tested model because the loop already runs on it. A prompt may claim support for another model only with a scorecard row for that model. Model-specific variants are allowed for at most a few lines of a part, kept in the same file under a marked section, and only when a test shows the need.

### 7.6 Launch checklist

- A licence file (see section 9).
- README, CONTRIBUTING, and a code of conduct.
- At least three tested patterns and the four core meta tools, each with a scorecard.
- Issue templates: failure report, new tool request, model result.
- A check in CI that every prompt has a tests folder, listed variables match, and exports are current.
- One written walkthrough that takes a single prompt from rough idea to promoted, using the real history of the explainer.

## 8. Roadmap

Each phase has an exit test. A phase is not done until its test passes.

| Phase | Work | Exit test |
| --- | --- | --- |
| 0. Foundations | This plan and the README. Decisions in section 9 made. | You have approved the plan. |
| 1. Prove one pattern | Finish explain: v0.2.2 edits, gate review, run, grading, repeat until promoted. Test the figures modifier. | explain is `tested` with a public scorecard. |
| 2. Prove composition | Split explain into kernel, pattern, reader and domain files. Add the finance domain and executive reader without editing the pattern. Compare tags with headings. | The reassembled prompt matches the promoted one word for word, and both new combinations pass. |
| 3. Build the meta tools | Grader, cold reader, rubric writer, test input writer as library prompts, each tested like any other. Check the grader against 30 hand-labelled outputs. | The grader agrees with the hand labels on at least 90% of checks. |
| 4. Automate | Scripts for assemble, run, grade and scorecard. promptfoo configs. CI checks. | A full run and grading of one pattern takes one command. |
| 5. Developer and agent packs | review and code review first, then the build order in 6.6. Skill and Fabric exports. | Eight developer tools and three agent tools tested; one skill installs and runs in a coding agent. |
| 6. Open up | Launch checklist in 7.6. Walkthrough written. Repository announced. | An outside contributor lands a failure report or a prompt using only the docs. |
| 7. Keep it true | Rerun everything on each major model release. Retire what no longer earns its place. Add a second model family. | Every scorecard is under six months old or marked stale. |

Phases 1 and 2 are already in `loop/BACKLOG.md`. On approval of this plan, the backlog gets phases 3 to 6 added in the same form so the unattended loop can work through them.

## 9. Decisions needed from you

| # | Question | Recommendation | Why |
| --- | --- | --- | --- |
| 1 | Which licence? | MIT for everything | It is what Fabric and promptfoo use, it is the simplest for people to reuse, and one licence avoids questions about which file is under which. The alternative is CC BY 4.0 for prompts if you want attribution to be required for the text itself. |
| 2 | Which models to support at launch? | Claude only, with the structure ready for more | Each extra model multiplies test cost. Add a second family in phase 7 or when a contributor brings the runs. |
| 3 | Developer tools first, or all domains equally? | Developer tools first | It is the audience you named, and it gives the library a clear identity. The patterns stay domain-free, so other fields can be added later. |
| 4 | Rename the design file to `DESIGN.md`? | Yes | The current filename has spaces and is hard to link to. |
| 5 | Keep XML-style tags in the prompt format? | Keep, and test against headings in phase 2 | Vendor advice has softened on tags, but they make assembly reliable. A test settles it. |
| 6 | When to make the repo's open-source status official? | At phase 6, not before | The repo is already public. Announcing before three patterns are tested would undercut the "evidence" promise. |

## 10. Risks

| Risk | What we do about it |
| --- | --- |
| The library grows into another snippet pile | The "new pattern only if nothing existing can do it" rule, enforced at review |
| Test cost limits how much gets built | Small test sets to begin with, code checks before grader checks, reruns only for changed parts |
| A new model makes tested prompts stale | The "tested on" line, stale marking after six months, and a migration check tool |
| The grader is wrong and nobody notices | Check it against hand labels in phase 3 and again whenever the grader model changes |
| Prompts are tuned to the test inputs and fail on real ones | Every real-use failure joins the test set; examples in prompts never name test inputs (already a rule after v0.2.0) |
| Composition does not hold and each tool needs its own hand-written prompt | Phase 2 tests this early. If it fails, the fallback is fewer shared parts and more complete built prompts. |
| One maintainer | Unattended loop for routine rounds; contribution rules that let others grade and rerun |

## 11. Sources

Research for this plan, read on Nov 16, 2026. Sources already cited in the system design are not repeated. Three pages could not be opened from this session because their hosts are outside its network allowlist (hamel.dev, agentskills.io, promptfoo.dev); points drawn from them come through the secondary sources listed and are marked.

Vendor guidance:
- [Best practices for prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering), Anthropic (read in full)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Anthropic (read in full)
- [GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) and [GPT-5.5 guide](https://developers.openai.com/api/docs/guides/latest-model/gpt-5.5), OpenAI (search summaries only)
- [Gemini 3 prompting guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) and [Prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies), Google (search summaries only)

Existing libraries and tools:
- [Fabric](https://github.com/danielmiessler/fabric), Daniel Miessler (repository page read)
- [prompts.chat listing](https://enterprisedna.co/directories/open-source/awesome-chatgpt-prompts) (secondary)
- [OpenAI to acquire Promptfoo](https://siliconangle.com/2026/03/09/openai-acquire-promptfoo-expand-ai-application-testing-capabilities/), SiliconANGLE (secondary)
- [GEPA prompt optimization](https://pydantic.dev/articles/prompt-optimization-with-gepa.md), Pydantic, and [DSPy optimizers explained](https://futureagi.com/blog/dspy-optimizers-explained/) (secondary)

Agent standards:
- [Standardize project context: AGENTS.md and Agent Skills](https://developers.redhat.com/articles/2026/07/27/standardize-project-context-agentsmd-and-agent-skills), Red Hat Developer (secondary)
- [Agent Skills specification](https://agentskills.io/specification.md) (official; not reachable from this session, details via [a mirror](https://www.mintlify.com/anthropics/skills/spec/overview))

Testing practice:
- [Why is error analysis so important in AI evals](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html), Hamel Husain and Shreya Shankar (not reachable from this session; via secondary summaries)
- [LLM evals: what actually works](https://tianpan.co/blog/2026-02-20-llm-evals-practitioners-guide), Tian Pan (secondary)
- [Testing binary vs score evals on the latest models](https://arize.com/blog/testing-binary-vs-score-llm-evals-on-the-latest-models/), Arize (secondary)
- [LLM error analysis](https://kili-technology.com/blog/llm-error-analysis), Kili Technology (secondary)

Security:
- [OWASP 2026 LLM Top 10 released](https://www.helpnetsecurity.com/2026/08/06/owasp-2026-llm-top-10-released/), Help Net Security, and [what changed](https://cloudsecurityalliance.org/articles/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters), Cloud Security Alliance (secondary)

# Dadhichi: Master Prompt Library System Design

Nov 15, 2026 · @Ayush

## 1. Purpose and design principles

Dadhichi is a library of tested, reusable prompts plus an engine that writes new ones to the same standard. It covers any domain, not only IT. The unit of value is not a clever phrase but a prompt that has a stated job, a stated reader, and evidence that it works.

It is not a collection of copy-paste snippets. A snippet collection grows to hundreds of near-duplicates nobody trusts. Dadhichi stays small by composing a few well-tested parts.

Six principles drive every decision below:

1. **A prompt is a spec.** It has inputs, a target output, constraints, and acceptance tests. If you cannot say how you would know the output is good, the prompt is not finished.
2. **Describe the situation, not just the rules.** Telling the model who reads the output and where (a Kindle on a bus, no browser) lets it make hundreds of small decisions correctly. A rule list covers only the cases you thought of.
3. **Compose, do not duplicate.** Reader profiles, domain knowledge, task patterns, and style modifiers are separate parts. One explainer pattern serves IT, finance, and medicine by swapping the domain pack.
4. **Plan before prose.** Every generative prompt has a silent planning step (inventory, prioritize, order) before writing. This is what stops both over-explaining and under-explaining.
5. **Nothing enters the library untested.** Each entry ships with test inputs and a rubric. A prompt version is promoted only when it beats the previous one on those tests.
6. **Models change, so record what you tested on.** A prompt tuned for one model can degrade on the next. Every entry records the model and date it was last verified.

## 2. Research findings

The evidence points one way: prompts work through clear context, good examples, and testing, not through special phrases. Each finding below is turned into a design rule.

| Finding | Design rule for Dadhichi | Source |
| --- | --- | --- |
| A reason beats a bare rule. Explaining why a behavior matters lets the model generalize to cases the rule did not list. | Every constraint in a library prompt carries its reason, usually through the reader's situation. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| The colleague test: if a person with minimal context could not follow the prompt, the model will struggle too. | Each entry is reviewed cold, by reading only the prompt. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Examples are the strongest single technique, but which examples and in what order can swing accuracy from under 50% to over 90%. | Use 3 to 5 varied examples, in their own tags. Examples are versioned and tested like the prompt text. | [Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [The Decoder on the Prompt Report](https://the-decoder.com/massive-prompt-report-uncovers-the-weird-world-of-prompting-large-language-models/) |
| Say what to do, not what to avoid, and write the prompt in the style you want back. | Patterns for prose output are written as prose. Bans are rewritten as positive instructions where possible. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Shouting backfires on current models. Capitalized "CRITICAL" and "MUST" cause over-application. | Calm, plain wording throughout. No capital-letter emphasis in the library. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Separate content types with consistent tags. For long inputs, put the material first and the question last. | One fixed tag vocabulary across the library; source material goes above instructions. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Draft, review against criteria, then refine is the most common useful chain. | Every pattern ends with a self-check step; high-stakes patterns split it into a second prompt. | [Anthropic best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) |
| Small, seemingly irrelevant changes shift results, and published technique rankings do not transfer reliably. | Never trust a change by reading it. Run the tests. | [Prompt Report](https://arxiv.org/html/2406.06608v5), [The Decoder](https://the-decoder.com/massive-prompt-report-uncovers-the-weird-world-of-prompting-large-language-models/) |
| Prompt engineering is a loop: run on a dataset, evaluate, modify. Domain experts should sit in that loop. | Domain packs are written or reviewed by someone who knows the field. | [Prompt Report](https://arxiv.org/html/2406.06608v5) |
| Good success criteria are specific and measurable; many auto-graded cases beat a few hand-graded ones. | Each pattern has a rubric of yes/no checks an LLM grader can apply. | [Anthropic: define success and build evals](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) |

One caution on scope: model-specific advice ages fast. Anthropic's own page notes that a verification instruction that helps one model causes over-checking on a newer one. That is why principle 6 exists.

## 3. Architecture

A Dadhichi prompt is assembled from four independent parts on top of a shared kernel, so adding a new domain or a new reader never means rewriting a prompt.

&#91;embedded content: Dadhichi architecture · engine, four part types, kernel, quality harness\]

The engine takes a rough request, picks one task pattern, fills it with a reader profile, a domain pack, and modifiers, and returns a finished prompt. The kernel sits under everything and the harness tests the result.

| Part | Answers | Example | How many to expect |
| --- | --- | --- | --- |
| Kernel | What is always true of a good answer? | Plan silently first; never use a term before introducing it | 1 |
| Task pattern | What job is being done? | Explain a concept; review a draft; compare options | 10 to 15 |
| Reader profile | Who consumes the output, and where? | Commuter on a Kindle, no lookups; executive with 2 minutes | 6 to 10 |
| Domain pack | What does this field take for granted? | IT, finance, law, medicine, cooking, fitness | Grows on demand |
| Modifier | What small dial changes? | Length cap, language, tone, plain text only | 10 to 20 |

The explainer prompt from earlier in this conversation maps cleanly onto this: pattern = Explain, reader = Commuter on a Kindle, domain = IT. Swapping the domain pack to finance gives a no-lookup explainer of bond duration with no other change.

**Precedence when parts conflict:** the user's request wins over modifiers, modifiers win over the reader profile, the reader profile wins over pattern defaults, and nothing overrides the kernel.

## 4. Prompt spec

Every library entry is one Markdown file with a metadata header and seven fixed sections. The fixed shape is what makes entries comparable, testable, and composable.

```markdown
---
id: pattern.explain
kind: pattern            # kernel | pattern | reader | domain | modifier
version: 1.0.0
status: draft            # draft | tested | retired
job: Explain one concept so it is understood in a single linear read
inputs:
  - TOPIC (required)
  - SOURCE (optional)
slots: [reader, domain, modifiers]
verified_on: claude-fable-5-2, 2026-11-15
tests: tests/pattern.explain/
---

<situation>
Who reads the output, where, and what they cannot do.
Filled from the reader profile.
</situation>

<goal>
What the reader can do after reading. One or two sentences.
</goal>

<plan>
The silent planning steps: inventory, cut what is known,
sort into tiers, order by dependency, pick length.
</plan>

<write>
The writing rules for this job, each with its reason.
</write>

<domain>
Filled from the domain pack: vocabulary, standards, pitfalls.
</domain>

<check>
The self-review list the model applies before answering.
</check>

<output>
Exactly what to return and what to leave out.
</output>
```

| Section | Why it exists | Failure it prevents |
| --- | --- | --- |
| situation | Lets the model reason about cases no rule covers | Generic answers written for nobody |
| goal | Gives a finish line | Padding, drifting scope |
| plan | Forces prioritization before writing | Over-explaining easy parts, skipping hard ones |
| write | Holds the job-specific craft | Wrong structure for the task |
| domain | Injects field knowledge without touching the pattern | Wrong terminology, missed conventions |
| check | A second pass against stated criteria | Undefined terms, logic gaps |
| output | Pins the deliverable | Preambles, summaries, offers to continue |

Three rules for writing any section:

- Each instruction states its reason, or the situation makes the reason obvious.
- Variables are written `{UPPER_CASE}` and listed in `inputs`. A prompt with an unlisted variable fails review.
- A pattern never names a domain, and a domain pack never gives writing instructions. This separation is what keeps the parts reusable.

## 5. Taxonomy

The library is organized by the job being done, not by subject. Subjects are unlimited; jobs are few. About twelve task patterns cover most requests in any field.

| Family | Pattern | The job | Works across, for example |
| --- | --- | --- | --- |
| Understand | explain | Make one concept clear in a single read | Raft consensus, bond duration, how vaccines work |
| Understand | digest | Compress a long source for a specific reader | A research paper, a contract, a 40-page RFC |
| Understand | teach | Build a skill over several steps with practice | SQL window functions, chess openings |
| Decide | compare | Weigh named options on shared criteria | Databases, job offers, phone plans |
| Decide | diagnose | Find the likely cause from symptoms | A failing pipeline, a plant losing leaves |
| Decide | plan | Turn a goal into ordered steps with dependencies | A migration, a wedding, a study schedule |
| Make | draft | Write something sent under the user's name | Email, proposal, cover letter |
| Make | build | Produce a working artifact to a spec | Code, a spreadsheet model, a recipe |
| Make | ideate | Generate varied options, then narrow | Product names, experiment designs |
| Improve | review | Judge a work against criteria and say what to fix | Code review, essay feedback, a resume |
| Improve | rewrite | Change form while keeping meaning | Simplify, shorten, translate, change tone |
| Operate | extract | Pull structured data out of messy input | Invoices, logs, meeting notes |

Reader profiles and domain packs are the other two axes. A request is located by three coordinates: `pattern / reader / domain`, for example `explain / commuter / it` or `review / hiring-manager / resume`.

Starter reader profiles: commuter (linear read, no lookups), executive (two minutes, decision first), practitioner (knows the field, wants precision), beginner (no background, needs foundations), examiner (will check every claim), listener (output is read aloud).

A new pattern is added only when a request cannot be served by an existing pattern plus a modifier. This rule is what keeps the library from turning into a snippet pile.

## 6. The engine

The engine is one meta-prompt that turns a rough request into a prompt in the section 4 format. It runs in four steps: classify, ask, assemble, check.

1. **Classify.** Map the request to `pattern / reader / domain`. If no pattern fits, say so instead of forcing one.
2. **Ask.** Ask only for what cannot be inferred and would change the prompt. At most three questions; none if the request is clear.
3. **Assemble.** Fill the seven sections from the chosen parts. Where the library has no part yet, write one in the same style and flag it as new.
4. **Check.** Run the colleague test and the kernel rules, then name the two most likely ways the prompt will fail.

Engine v1, ready to use as a system prompt or as the instructions of a Claude Project that holds the library files:

```markdown
You are Dadhichi, a prompt engineer. You turn a rough request
into a prompt that a capable language model can follow to
produce a high-quality result on the first attempt.

The prompts you write will be pasted into a model that knows
nothing about this conversation. It cannot ask the requester
anything. So the prompt must carry every piece of context the
model needs, and explain the reason behind each constraint so
the model can handle cases the prompt did not foresee.

<library>
{LIBRARY_FILES, if available: kernel, patterns, reader profiles,
domain packs, modifiers}
</library>

Work in four steps.

STEP 1: CLASSIFY
Identify three things from the request:
- pattern: the job being done (explain, digest, teach, compare,
  diagnose, plan, draft, build, ideate, review, rewrite, extract)
- reader: who consumes the final output, in what setting, and
  what they already know
- domain: the field, and what that field takes for granted
If the request spans two jobs, split it into two prompts that
run in sequence and say so.

STEP 2: ASK ONLY WHAT MATTERS
If something is missing that you cannot reasonably infer and
that would change the prompt, ask up to three short questions
and stop. Typical gaps: the reader's background, the purpose
the output serves, a hard limit on length or format. If the
request is clear enough, ask nothing and state your
assumptions in one line.

STEP 3: ASSEMBLE
Write the prompt with these sections, in this order:
<situation> <goal> <plan> <write> <domain> <check> <output>
- Use the library part when one exists. Otherwise write the
  part yourself in the same style and mark it NEW.
- Describe the reader's situation concretely. A model that
  understands the situation makes better choices than one
  following a list of rules.
- Give every instruction its reason unless the situation
  already makes it obvious.
- State what to do instead of what to avoid where you can.
- Use calm, plain wording. No capital-letter emphasis.
- Include a silent planning step that makes the model decide
  what matters most, what can be brief, and what to leave out,
  so the output is as long as the task deserves and no longer.
- Add 3 to 5 varied examples only when the desired output has
  a form that is hard to describe in words. Put them in
  <example> tags.
- Write variables as {UPPER_CASE} and list them at the top.
- Write the prompt in the style you want the output to have.

STEP 4: CHECK
Reread the prompt as someone with no context. Fix anything
they would have to guess. Confirm no instruction conflicts
with another. Then identify the two most likely ways the
resulting output could still fall short.

RETURN
1. Classification: pattern / reader / domain, in one line.
2. Assumptions, in one line, if you made any.
3. The prompt, in a single code block.
4. Two failure risks, each with a test input that would
   expose it.
Nothing else.

Rough request: {REQUEST}
```

The last return item matters most for engineering: every prompt the engine writes arrives with its first two test cases, which seed the test folder in section 7.

## 7. Quality system

A prompt enters the library as `tested` only after it passes a fixed set of inputs against a written rubric, and a new version replaces the old one only if it scores higher on the same set.

**Test set per pattern.** Start with 6 to 10 inputs chosen to stress the prompt, then grow it. Published practice suggests working toward about 50 cases and adding every real failure to the set ([Tian Pan on prompt versioning](https://tianpan.co/blog/2026-05-04-prompt-versioning-first-class-code-artifact)). Each set must include:

- a trivial input (does it stay short?)
- a hard input (does it stay clear?)
- an input outside the model's likely knowledge (does it admit limits?)
- a vague input (does it handle missing detail sensibly?)
- an input from a second domain (does the pattern really generalize?)

**Rubric.** Yes/no checks, not impressions, so a grader model can apply them consistently. Anthropic's guidance is to keep rubrics specific, ask for a constrained verdict, let the grader reason before scoring, and grade with a different model than the one that wrote the output ([Anthropic: build evals](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)). The rubric for `pattern.explain`:

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | No lookups | Every term is introduced before or at first use |
| 2 | Linear | No sentence depends on something that comes later |
| 3 | Accurate | No technical error; real terminology is used |
| 4 | Proportional | Length fits the difficulty; the trivial input stays under about 400 words |
| 5 | No padding | No section could be deleted without leaving a gap |
| 6 | Resumable | Each major section restates what the reader holds so far |
| 7 | Plain text | Reads correctly on an e-reader: no tables, links, or nested lists |

**Human check.** Checks 1 and 2 are the point of this pattern and a grader can miss them. For those, read the output on a phone away from a desk and count the pauses. Zero pauses is the target.

**Comparing versions.** Run old and new on the full set, grade both, and promote the new one only if it passes more checks and fails no check the old one passed. Because small wording changes can move results unpredictably, a change that looks harmless still gets the full run.

**Failure log.** One file per pattern, one line per failure: date, input, which check failed, suspected cause, fix version. This log is the most valuable file in the library because it records why each instruction exists.

## 8. Storage and versioning

The library is a Git repository of plain Markdown files, one part per file. Git gives history, diffs, and rollback for free, and plain files work with any model or tool.

```
dadhichi/
  kernel.md
  engine.md
  patterns/        explain.md  compare.md  review.md ...
  readers/         commuter.md  executive.md  beginner.md ...
  domains/         it.md  finance.md  law.md ...
  modifiers/       short.md  plain-text.md  hindi.md ...
  tests/
    pattern.explain/   inputs.md  rubric.md  failures.md
  built/           explain.commuter.it.md   (assembled, ready to paste)
  CHANGELOG.md
```

| Change | Version bump | Example |
| --- | --- | --- |
| Wording cleanup, same behavior | Patch, 1.0.0 to 1.0.1 | Fix a typo, shorten a sentence |
| New capability or example, same output shape | Minor, 1.0.0 to 1.1.0 | Add the resumable-sections rule |
| Different output shape or planning logic | Major, 1.0.0 to 2.0.0 | Switch from prose to a two-part output |

The three-level scheme follows the convention described in [Tian Pan's article](https://tianpan.co/blog/2026-05-04-prompt-versioning-first-class-code-artifact). Two rules go with it:

- A released version is never edited. A fix is a new version.
- Every entry records `verified_on` (model and date). When a new model arrives, rerun the tests before trusting old entries; some instructions will need removing, not adding.

To use the library day to day, load the folder into a Claude Project with `engine.md` as the project instructions. The engine then composes from the real files instead of from memory.

## 9. Roadmap

Build one pattern end to end before widening, because the first tested pattern proves the format, the harness, and the engine at once.

1. **Prove the explainer.** Split the existing explainer prompt into `kernel.md`, `patterns/explain.md`, `readers/commuter.md`, and `domains/it.md`. Run three topics (an API key, Kafka consumer groups, Raft consensus) and score them on the section 7 rubric. Exit when all three pass checks 1 to 5.
2. **Prove composition.** Add `domains/finance.md` and `readers/executive.md` without touching the pattern. If the explainer still passes, the architecture holds. If the pattern needs edits, the leak between parts is the thing to fix.
3. **Stand up the engine.** Put the files in a Claude Project with `engine.md` as instructions. Feed it ten rough requests from real work and compare its prompts with hand-written ones.
4. **Widen by need.** Add the patterns used most: review, compare, digest, draft. Each ships with its test set and rubric on day one.
5. **Automate grading.** A small script runs every test input through the prompt, sends outputs to a grader prompt with the rubric, and writes a score table. This turns version comparison from an evening into a minute.
6. **Maintain.** Rerun all tests on each new model release, retire parts that no longer earn their place, and keep the failure logs current.

Open questions:

- Is the library for personal use only, or will others use it? Shared use needs contribution rules and stricter review.
- Which models must it support? Supporting several means running the tests on each and may mean model-specific variants of a few parts.

## Sources

- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), Anthropic
- [Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests), Anthropic
- [The Prompt Report: A Systematic Survey of Prompting Techniques](https://arxiv.org/html/2406.06608v5), Schulhoff et al. (first 100,000 characters read)
- [Massive "Prompt Report" uncovers the weird world of prompting large language models](https://the-decoder.com/massive-prompt-report-uncovers-the-weird-world-of-prompting-large-language-models/), The Decoder
- [The Prompt Versioning Problem](https://tianpan.co/blog/2026-05-04-prompt-versioning-first-class-code-artifact), Tian Pan

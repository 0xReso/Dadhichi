# How the Dadhichi Prompt Library Works

By the end you will understand how Dadhichi builds prompts from a few separate parts, how its engine writes new ones, and how a prompt has to prove itself before it is kept.

## Why a pile of prompts stops working

A prompt is the text you give a language model to tell it what to do. People who use these models a lot tend to save the prompts that worked, so they can paste them in again next time.

Left alone, that habit produces a folder of copy-paste snippets. The design behind Dadhichi describes where this goes: the collection grows to hundreds of near-duplicates, and nobody trusts any of them. You cannot tell which of five similar "explain this" prompts is the good one, or whether any of them still works.

Dadhichi is the answer the design proposes. It is a library of tested, reusable prompts, plus an engine that writes new prompts to the same standard. It is meant for any field, not only IT. What follows is a design document from November 2026 rather than a finished system, and its own roadmap starts by building one prompt end to end before anything else.

The design's first principle changes what a prompt is. A prompt is treated as a spec: it has inputs, a target output, constraints, and acceptance tests. If you cannot say how you would know the output is good, the prompt is not finished. A saved snippet has none of that; it is a guess that happened to work once.

So if near-duplicates are the disease, the question is how a library can cover every field without copying the same prompt over and over.

## Five kinds of part

The problem so far is that saved prompts multiply into copies nobody trusts, and Dadhichi wants prompts that behave like specs instead. Its way out is to stop storing whole prompts and to store parts that snap together.

Take one running example throughout: a prompt that explains a technical idea to someone reading on a Kindle on a bus, with no browser and nobody to ask. The design uses exactly this case.

The first part is the kernel. It holds what is always true of a good answer, whatever the job. Two of its rules, as the design gives them: plan silently before writing, and never use a term before introducing it. There is one kernel, and it sits under everything.

The second part is the task pattern, which names the job being done. In the running example the job is "explain": make one concept clear in a single read. The design lists about twelve patterns, such as compare, review, plan, draft, and extract, grouped into families like understanding, deciding, and making. Subjects are unlimited, but jobs are few, so the library is organised by job.

The third part is the reader profile. It describes who consumes the output and where. The running example uses the commuter profile: a linear read, no lookups. The design's other starting profiles include an executive with two minutes who wants the decision first, and a beginner with no background.

The fourth part is the domain pack. It holds what a field takes for granted: its vocabulary, its standards, its usual pitfalls. The running example uses the IT pack. Domain packs are written or reviewed by someone who knows the field, and new ones are added as they are needed.

The fifth part is the modifier, a small dial such as a length cap, a language, a tone, or plain text only.

A request is located by three coordinates, written pattern, reader, domain. The running example is "explain / commuter / it". Here is the payoff of the split: swap the IT pack for a finance pack, change nothing else, and you have a no-lookup explainer of bond duration for the same commuter.

That swap only works if the parts stay clean. So the design sets a strict boundary: a pattern never names a domain, and a domain pack never gives writing instructions. When parts do pull in different directions, a fixed order settles it. The user's request beats modifiers, modifiers beat the reader profile, the reader profile beats the pattern's defaults, and nothing overrides the kernel.

Every part lives in its own file with the same shape. A short header records the part's name, its version, its status (draft, tested, or retired), and the model and date it was last checked on. Below that come seven fixed sections, in order: who reads the output and where, what they should be able to do afterwards, a silent planning step, the writing rules for the job, the field knowledge, a self-check, and exactly what to return. The fixed shape is what lets one entry be compared with another and tested the same way.

The silent planning step matters most. Before writing a word, the model takes stock of what the reader needs, cuts what they already know, decides what deserves the most space, and picks a length. The design credits this step with stopping both over-explaining and under-explaining.

Parts that snap together are fine when the library already has them, which leaves the question of who assembles them, and what happens when a request needs something new.

## The engine that writes new prompts

You now have the building blocks: one kernel, a dozen or so job patterns, reader profiles, domain packs, and modifiers, all in the same seven-section shape. The engine is what puts them together for a fresh request.

The engine is itself a prompt, one whose output is another prompt. You hand it a rough request, and it works in four steps.

1. Classify. It maps the request to a pattern, a reader, and a domain. If no pattern fits, it says so rather than forcing one. If a request spans two jobs, it splits it into two prompts that run one after the other.
2. Ask. It asks only for what it cannot reasonably infer and what would change the prompt: at most three short questions, and none if the request is clear. In that case it states its assumptions in one line.
3. Assemble. It fills the seven sections from the library's parts. Where no part exists yet, it writes one in the same style and marks it as new.
4. Check. It rereads the prompt as someone with no context would and fixes anything they would have to guess. The design calls this the colleague test: if a person with little context could not follow the prompt, the model will struggle too.

The engine returns four things and nothing else: the classification in one line, any assumptions, the finished prompt, and the two most likely ways the result could still fall short, each with a test input that would expose it.

That last item is the one the design leans on. It means every prompt the engine writes arrives with its first two test cases already attached.

A prompt with two test cases is a start, but it raises the question of what testing a prompt actually involves, and how it decides which version to keep.

## How a prompt earns its place

So far, prompts are assembled from clean parts, and the engine hands each new one over with two test inputs. The design's fifth principle says what those inputs are for: nothing enters the library untested.

Each pattern gets a test set: a fixed list of inputs chosen to stress it. The design starts with six to ten and, citing published practice, suggests growing toward about fifty, adding every real failure along the way. Every set must include a trivial input, to see whether the output stays short; a hard one, to see whether it stays clear; one outside what the model is likely to know, to see whether it admits limits; a vague one; and one from a second domain, to see whether the pattern really generalises.

Outputs are scored against a rubric, a list of yes-or-no checks rather than impressions. Yes-or-no checks let another model act as grader and apply them the same way every time, and the design follows Anthropic's guidance to grade with a different model from the one that wrote the output. For the explainer in the running example, the checks include: every term is introduced before or at its first use; no sentence depends on something that comes later; and the trivial input stays under about 400 words.

The first two checks are the whole point of the explainer, and a grader can miss them. So the design adds a human check: read the output on a phone, away from a desk, and count the times you had to pause. The target is zero.

Now the trap. It is tempting to look at a reworded prompt, see that the change is harmless, and keep it. The design rules this out. It cites research, including a large survey of prompting techniques called the Prompt Report, finding that small, seemingly irrelevant changes shift results, and that published rankings of techniques do not transfer reliably. So a change that looks harmless still gets the full run. Old and new versions are run on the whole test set and graded, and the new one is promoted only if it passes more checks and fails no check the old one passed.

Each pattern also keeps a failure log: one line per failure, with the date, the input, which check failed, the suspected cause, and the version that fixed it. The design calls this the most valuable file in the library, because it records why each instruction exists.

The last piece is time. Models change, and a prompt tuned for one can get worse on the next; the design notes that an instruction which helps one model can cause over-checking on a newer one. That is why every entry records the model and date it was last verified. When a new model arrives, the tests are rerun before old entries are trusted, and some instructions will need removing rather than adding.

The files themselves sit in Git, a tool that keeps every past version of a set of files, so history and rollback come free. A released version is never edited; a fix becomes a new version.

## The whole picture

Dadhichi replaces a pile of untrusted snippets with prompts treated as specs. A single kernel holds the rules every answer follows; a small set of task patterns names the job; reader profiles, domain packs, and modifiers fill in who reads, what the field assumes, and the small dials, so "explain / commuter / it" becomes a finance explainer by swapping one file. The engine assembles these parts for a new request and hands back each prompt with its first two test cases. Those cases seed a test set and a yes-or-no rubric, and a new version replaces an old one only when it scores better on the full run. Reading the system as one loop, in which the engine's test cases feed the harness and the failure log explains each rule, is my interpretation of how the design's sections connect. The design itself is still a plan: its roadmap begins with proving the explainer on three topics, and it leaves open whether the library is for personal or shared use, and which models it must support.

## Going further

Version numbers: the design uses three levels, a patch for a wording cleanup, a minor bump for a new capability with the same output shape, and a major bump for a different output shape or planning logic.

Claude Project: the design's suggested day-to-day setup is to load the library folder into one, with the engine file as its instructions, so the engine composes from the real files rather than from memory.

Examples in prompts: the design adds three to five varied examples only when the desired output is hard to describe in words, and versions them like the prompt text, since the choice and order of examples can swing accuracy sharply.

Automated grading: a planned script that runs every test input, sends the outputs to a grader with the rubric, and writes a score table.

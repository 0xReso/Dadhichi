# How the Dadhichi Prompt Library Works

By the end you will know how Dadhichi builds prompts from a few reusable parts, how it writes new ones, and how it decides a prompt is good enough to keep.

A language model does what its written instructions ask, and those instructions are called a prompt. Anyone who uses models for real work collects prompts worth keeping: one that explains a topic well, one that reviews a draft, one that pulls figures out of invoices. Keeping them is easy. Trusting them six months later is the hard part.

The usual way to keep prompts is a folder of snippets that get copied and tweaked. The design document behind Dadhichi describes what happens next: the folder grows to hundreds of near-duplicates, and nobody trusts any of them. Dadhichi is designed as the opposite, a small library of tested, reusable prompts plus an engine that writes new prompts to the same standard. It is meant for any field, not only IT.

Everything below is the design as that document, dated 15 November 2026, lays it out. Its own plan starts by building and testing a single prompt end to end before widening, so read what follows as how the system is meant to work.

The common misreading of a prompt library is that its value lies in clever phrasing, the right magic words. The document rejects this directly. In Dadhichi the thing of value is a prompt with a stated job, a stated reader, and evidence that it works. A prompt is treated as a specification: it has inputs, a target output, constraints, and tests that say whether the output is good. If you cannot say how you would know the output is good, the prompt is not finished.

Take one request and follow it through. You want a model to explain what an API key is, the secret string a program sends to prove it may use a service, to someone who will read the answer on a Kindle on the bus with no way to look anything up. In a snippet folder, that request becomes one more file. In Dadhichi, it becomes a combination of parts the library already holds.

## Five kinds of part

A snippet folder fails because every prompt is written whole and copied whole. Dadhichi splits a prompt into separate parts, each answering one question, and assembles them for each request.

The first part sits under every prompt. It holds what is always true of a good answer, whatever the job: plan silently before writing, for example, and never use a term before introducing it. This part is called the kernel, and the library has exactly one.

The second part says what job is being done. Explaining a concept is one job, reviewing a draft is another, comparing options is a third. Each job is called a task pattern. The document starts with twelve and expects ten to fifteen in all, because, as it puts it, subjects are unlimited but jobs are few. Your request uses the explain pattern.

The third part says who consumes the output, and where. This is the reader profile. Your reader is the commuter profile: someone reading once, top to bottom, with no lookups. The document expects six to ten profiles.

The fourth part holds what one field takes for granted: its vocabulary, its standards, its usual pitfalls. This is the domain pack. Your request uses the IT pack, and the document expects packs to be added whenever a new field is needed, written or reviewed by someone who knows that field.

The fifth part is a small dial on top of everything else, such as a length cap, a language, a tone, or plain text only. This is called a modifier.

Here is why the split matters. Swap the IT pack for a finance pack and keep everything else, and the same explain pattern now produces a no-lookup explanation of bond duration, a measure of how sharply a bond's price moves when interest rates change. Nothing in the pattern was rewritten. To keep that true, the document sets a firm boundary: a pattern never names a domain, and a domain pack never gives writing instructions.

Parts can still disagree, so there is an order of precedence. Your own request beats any modifier, a modifier beats the reader profile, the reader profile beats the pattern's defaults, and nothing overrides the kernel.

Once assembled, every prompt takes the same fixed shape of seven sections, in order: the reader's situation, the goal, a silent planning step, the writing rules, the field notes from the domain pack, a self-check, and exactly what to return. The fixed shape is what makes two prompts comparable and testable. Each instruction inside carries its reason, usually through the reader's situation, because the document cites Anthropic's published prompting guidance finding that a reason lets a model handle cases a bare rule never listed.

That covers a request the library already has parts for. What happens to a rough request that arrives in someone's own words?

## The engine that writes new prompts

You now have a library of five kinds of part and a fixed seven-section shape that a finished prompt takes. Something still has to pick the parts for a given request and fill the shape.

That something is the engine: a single prompt whose job is to write other prompts. It works in four steps.

First it classifies the request into three coordinates, written pattern, reader, domain. Your request becomes explain / commuter / it. If no pattern fits, the engine says so rather than forcing one. If the request covers two jobs, it splits it into two prompts that run in sequence.

Second, it asks only what it cannot reasonably infer and what would change the prompt: at most three short questions, and none if the request is clear. Your request is clear, so the engine asks nothing and states its assumptions in one line.

Third, it assembles the seven sections from the chosen parts. Where the library has no part yet, say a request in a field with no domain pack, the engine writes that part itself in the same style and marks it NEW. It writes in calm, plain wording with no capital-letter emphasis, because the document cites guidance that words like "CRITICAL" make current models over-apply a rule.

Fourth, it checks its own work. It rereads the prompt as someone with no context would, fixes anything they would have to guess, and confirms no two instructions conflict. Then it names the two most likely ways the resulting output could still fall short.

What comes back is four things: the classification in one line, any assumptions in one line, the prompt itself, and those two failure risks, each paired with a test input that would expose it. The document calls that last item the most important for engineering, because every prompt the engine writes arrives with its first two test cases.

The document suggests running the engine with the library files loaded beside it, so it composes from the real parts rather than from memory.

A prompt the engine wrote, however careful, has still never been run. So how does a prompt earn its place in the library?

## How a prompt earns its place

The engine has now handed you a prompt for the API-key explainer, along with two inputs designed to break it. The library's rule is that nothing enters untested.

The reason is that reading a prompt tells you little about how it will behave. The document cites research finding that small, seemingly irrelevant changes in wording shift results, and that the choice and order of examples in a prompt can swing accuracy from under 50% to over 90%. A change that looks harmless still has to be run.

So each pattern gets a test set: a fixed list of inputs chosen to stress it. It starts with six to ten and grows toward about fifty, with every real failure added. It must include a trivial input, a hard one, one outside the model's likely knowledge, a vague one, and one from a second field. Your API key is the trivial case, which asks whether the explanation stays short. Bond duration is the second-field case, which asks whether the pattern really works outside IT.

Each output is then judged against a rubric, a list of yes or no checks rather than impressions. The explain rubric has seven. Among them: every term is introduced before or at its first use; the trivial input stays under about 400 words; and the piece reads correctly on an e-reader, with no tables, links, or nested lists.

Yes or no checks matter because a second model can apply them consistently. That second model is called the grader. Following Anthropic's evaluation guidance, the document has the grader reason before giving its verdict, and uses a different model from the one that wrote the output.

Two of the explain checks, no lookups and a strictly linear read, are the whole point of the pattern, and a grader can miss them. For those, a person reads the output on a phone away from a desk and counts the pauses. The target is zero.

A prompt passes from draft to tested status only after clearing its set. Later, a new version replaces the old one only if, on the same full set, it passes more checks and fails none that the old one passed.

Versions are numbered at three levels. A wording cleanup with the same behaviour is a patch, 1.0.0 to 1.0.1. A new capability with the same output shape is a minor change, 1.0.0 to 1.1.0. A different output shape or planning logic is a major one, 1.0.0 to 2.0.0. A released version is never edited; a fix is always a new version.

All of this lives as plain text files in Git, a tool that records every past state of a set of files. That gives the library its history, its line-by-line differences between versions, and a way to roll back.

Every entry also records the model and date it was last verified, because models change. The document notes Anthropic's own observation that an instruction to double-check, helpful on one model, causes over-checking on a newer one. When a new model arrives, the tests are rerun before old entries are trusted, and some instructions will need removing rather than adding.

Finally, each pattern keeps a failure log: one line per failure, giving the date, the input, the check that failed, the suspected cause, and the version that fixed it. The document calls this the most valuable file in the library, because it records why each instruction exists.

## The whole picture

Dadhichi treats a prompt as a tested specification rather than a clever phrase. A single kernel, a dozen or so task patterns, a handful of reader profiles, domain packs added as fields are needed, and small modifiers combine into one fixed seven-section shape, so your API-key explainer and a finance explainer of bond duration share the same pattern with only the domain pack swapped. The engine turns a rough request into that shape by classifying, asking, assembling, and checking, and hands back two inputs likely to break the result. Those inputs seed a test set, a grader scores outputs against yes or no checks, a new version wins only by doing strictly better, and the failure log and the record of which model each entry was verified on keep the library honest as models change.

## Going further

Pattern families: the document groups its twelve patterns into five families, named understand, decide, make, improve, and operate.

Claude Project: the document's suggested way to use the library day to day, with the engine file set as the project's standing instructions and the library files loaded alongside.

Built prompts: a folder of fully assembled prompts ready to paste, named by their coordinates, such as explain.commuter.it.

Automated grading: a later roadmap step, a small script that runs every test input through a prompt and the grader and writes a score table, turning a version comparison from an evening into a minute.

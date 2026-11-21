# How the Dadhichi prompt library works

By the end you will know what Dadhichi is, how it builds a prompt out of a few reusable parts, and how it decides whether a prompt is good enough to keep.

## The problem with a pile of prompts

Anyone who uses an AI model for real work ends up saving the written instructions that worked, the prompts, so they can paste them in again. The collection grows. A few months later there are hundreds of near-copies: one for explaining a networking idea, a slightly different one for a finance idea, a third that someone tweaked and nobody remembers why. Nobody trusts any of them, because nobody knows which ones still work.

Dadhichi is a design for the opposite. It is a library of tested, reusable prompts, together with a way of writing new prompts to the same standard. It is meant for any field, not only IT, and it stays small by building every prompt from a handful of well-tested pieces instead of keeping hundreds of copies.

The source behind this article is Dadhichi's design document, dated 15 November 2026. It ends with a roadmap, a planned order of work, whose first step is to split one existing prompt into the library's pieces and test it. So what follows is best read as how the library is designed to work, rather than a report on a finished system.

The idea under the whole design is that a prompt is a specification, a spec for short: a description of a job precise enough that you could check whether the job was done. A Dadhichi prompt states what goes in, what should come out, the limits it must respect, and the tests that show a good result. The source puts it plainly: if you cannot say how you would know the output is good, the prompt is not finished.

Follow one job through the rest of this article. You want a prompt that explains a technical idea to someone reading on a Kindle on a bus, with no browser and nobody to ask. The first idea is an API key, the secret string a program sends to a service to prove it is allowed to use it.

Later you want the same kind of explanation for bond duration, a figure that says how strongly a bond's price moves when interest rates change. In a pile of saved prompts, the two would become separate prompts that slowly drift apart. In Dadhichi they stay one prompt with one piece swapped.

So what are the pieces, and how does one get swapped for another?

## Five kinds of part

You now have the problem, a pile of near-identical prompts nobody trusts, and Dadhichi's answer, a prompt treated as a spec that can be checked. The design gets there by building each prompt from separate parts, each answering one question.

The first part is the job being done. Explaining one concept is a job; comparing options, reviewing a draft, and pulling data out of messy notes are others. Dadhichi calls each of these a task pattern, and the explaining one is named explain. Subjects are unlimited but jobs are few, so the source expects about twelve task patterns to cover most requests in any field.

The second part describes who will read the output and where. This is the reader profile. The bus reader's profile is called commuter: a single read from top to bottom, with no lookups.

The third part holds what one field takes for granted: its vocabulary, its standards, its usual pitfalls. This is a domain pack. The API key explainer uses the IT pack, and the bond duration explainer uses a finance pack. Packs are added as they are needed, and the source wants each one written or reviewed by someone who knows the field.

The fourth part is a small dial: a length cap, a language, a tone, plain text only. Each of these is called a modifier.

Underneath all four sits the kernel: the rules that are true of any good answer, whatever the job. Two from the source are to plan silently before writing, and never to use a term before introducing it. There is one kernel for the whole library.

With these in hand, any request has an address of three coordinates, written as pattern, reader and domain. The API key explainer is explain / commuter / it. Swap the domain pack and you get explain / commuter / finance, a no-lookup explanation of bond duration, with nothing else changed.

That swap works only if the parts stay in their own lanes, so the design has a firm rule: a pattern never names a domain, and a domain pack never gives writing instructions. If the explain pattern mentioned networking, it would no longer fit finance. If the IT pack told the model how to build paragraphs, it would compete with the pattern.

Parts can still pull against each other, for instance a modifier that caps the length while the reader profile asks for every term to be explained. The order of precedence settles it: your request beats the modifiers, modifiers beat the reader profile, the reader profile beats the pattern's defaults, and nothing overrides the kernel.

The same thinking limits growth. A new pattern is added only when a request cannot be served by an existing pattern plus a modifier, and the source names this rule as what keeps the library from turning back into a pile.

Parts on their own are not a prompt, though, so what does the assembled thing look like?

## The shape of a finished prompt

You now hold the five kinds of part, from the single kernel to the small modifiers, and the rule that keeps them apart. When they are put together, the result always has the same shape.

Every library entry is one plain text file. At the top is a short header of facts about the entry: its name, its version, the job it does, the inputs it needs, and the model and date on which it was last checked.

Below the header come seven sections, always in the same order. Taking them one at a time: who reads the output and in what setting; what that reader can do afterwards; a private planning step; the writing rules for this job; the field knowledge; a self-review; and exactly what to hand back. The fixed shape is what lets entries be compared, tested and combined.

The first section is called the situation, and it is filled from the reader profile. For the bus reader it says they read once, top to bottom, with nobody to ask. The design leans on this more than on rules. A model that knows the output will be read on a Kindle on a bus can make hundreds of small decisions well, such as defining a term on the spot, while a list of rules covers only the cases its author thought of.

The third section, the plan, tells the model to think before it writes: list what the reader needs, cut what they already know, sort the rest by importance, put it in an order where each idea needs only earlier ones, and pick a length. The model does this silently; the reader sees only the result. The source credits this step with stopping both over-explaining and under-explaining.

The sixth section, the check, is the self-review: a list the model applies to its own draft before answering, such as whether every term was explained before it was used. Every pattern ends with this step, and patterns where mistakes are costly move it into a second prompt of its own.

Three habits run through every section. Each instruction carries its reason, so the model can handle cases the instruction never listed. Instructions say what to do rather than what to avoid. And the wording stays calm, with no capital letters for emphasis, because the published guidance the source draws on reports that shouting words like CRITICAL makes current models apply them too widely.

Writing all of that by hand for every new request would be slow, so how does a new prompt get made?

## The engine that writes prompts

A finished Dadhichi prompt, then, is a header plus seven fixed sections, each filled from the parts. Assembling one is the job of the engine.

The engine is itself a prompt, sometimes called a meta-prompt because what it produces is another prompt. You give it a rough request in ordinary words, and it hands back a finished prompt in the seven-section shape. That prompt will be pasted into a model that has never seen the conversation and cannot ask anyone anything, so the engine is told to pack in every piece of context and give each constraint its reason.

It works in four steps, in order:

1. Classify. It maps the request to a pattern, a reader and a domain. If no pattern fits, it says so rather than forcing one. If the request covers two jobs, it splits it into two prompts that run one after the other.
2. Ask. It asks only for what it cannot infer and what would change the prompt: at most three short questions, and none if the request is clear, in which case it states its assumptions in one line.
3. Assemble. It fills the seven sections from library parts. Where no part exists yet, it writes one in the same style and marks it NEW.
4. Check. It rereads the prompt as someone with no context, fixes anything they would have to guess, confirms that no two instructions conflict, and names the two most likely ways the result could still fall short.

Suppose your rough request is: explain bond duration to my manager, who has two minutes. The engine classifies it as explain / executive / finance. Executive is another starter reader profile, for someone with two minutes who wants the decision first. The request is clear, so the engine asks nothing.

The reread in step four has a name of its own: the colleague test. If a person with very little context could not follow the prompt, the model will struggle too. The library applies the same test to every entry, which is reviewed cold by reading the prompt and nothing else.

What comes back is short: the classification in one line, any assumptions in one line, the prompt itself, and the two failure risks, each paired with a test input that would expose it. The source calls that last item the one that matters most, because every prompt the engine writes arrives with its first two test cases.

Those test cases have to go somewhere, so how does the library use them to decide what to keep?

## How a prompt earns its place

So far a prompt is built from parts, has a fixed shape, and can be written for you by the engine along with two test inputs. None of that shows the prompt is any good, and Dadhichi's rule is that nothing enters the library untested.

Each entry carries a status: draft when it is new, tested once it has passed, and retired when it no longer earns its place. Moving from draft to tested means passing a fixed set of inputs.

That test set starts with six to ten inputs chosen to stress the pattern, and grows; the source points to published practice of working towards about fifty, adding every real failure. Each set must include a trivial input, to see whether the output stays short; a hard one, to see whether it stays clear; one outside the model's likely knowledge, to see whether it admits its limits; a vague one; and one from a second field, to see whether the pattern really carries over. For the explainer, the roadmap's first trial uses three IT topics, the API key among them.

Each output is judged against a rubric, a list of yes or no checks rather than impressions. The explainer's rubric has seven. Two of them are that every term is introduced before or at its first use, and that the trivial input stays under about 400 words, roughly a page and a half of a paperback.

The checks are applied by a grader, a second model that reads each output and gives a verdict on each check. The source recommends letting the grader reason before it scores, and using a different model from the one that wrote the output.

Two of the explainer's checks, no lookups and a straight top-to-bottom read, are the point of the pattern, and a grader can miss them. For those the design adds a person: read the output on a phone away from a desk and count the pauses. The target is zero.

Here is where instinct tends to go wrong. It feels as if you can judge a prompt change by reading it, since a tidier sentence surely does no harm. The research the source cites says otherwise: small, seemingly irrelevant changes in wording shift results, and published rankings of techniques do not carry over reliably. So the rule is never to trust a change by reading it.

Instead, the old and new versions both run the full test set and are both graded. The new one is promoted only if it passes more checks and fails none that the old one passed. A change that looks harmless still gets the full run, and a released version is never edited; a fix becomes a new version.

Models change too, and a prompt tuned for one can get worse on the next. That is why each entry records the model and date it was last verified. When a new model arrives, the tests run again, and the source expects that some instructions will then need removing rather than adding.

Every failure goes into a failure log, one file per pattern and one line per failure: the date, the input, the check that failed, the suspected cause and the version that fixed it. The source calls this the most valuable file in the library, because it records why each instruction exists.

The design leaves two questions open: whether the library is for personal use or will be shared with others, and which models it must support.

## The whole picture

Dadhichi treats a prompt as a spec that can be checked, not a clever phrase. Each prompt is built from one kernel and four kinds of swappable part, a task pattern, a reader profile, a domain pack and modifiers, kept strictly apart so that one explain pattern serves an API key and bond duration alike. The parts land in the same seven sections every time, with the situation guiding choices no rule could list and the silent plan keeping length in proportion. The engine does that assembly from a rough request, and the source states that the two test inputs it returns seed the pattern's test set. From there, nothing is marked tested until it passes that set against a yes or no rubric, and no new version replaces an old one without beating it on the same set. All of this is the design as the document describes it, with its build laid out as a roadmap that starts from the explainer.

## Going further

Git: a tool that keeps the full history of a set of files; the library is designed as a Git repository with one part per file, so every change can be compared and rolled back.

Version levels: the three-part number on each entry, raised at the last place for a wording cleanup, the middle for a new capability with the same output shape, and the first for a different output shape or planning logic.

Variables: placeholders in a prompt written in curly braces and capitals, such as {TOPIC}, each of which must be listed among the entry's inputs or the entry fails review.

Claude Project: a workspace in Claude, the AI assistant made by the company Anthropic, that holds files and standing instructions; the design suggests loading the library into one with the engine as its instructions.

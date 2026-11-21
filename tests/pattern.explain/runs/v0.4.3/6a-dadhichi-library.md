# How the Dadhichi Prompt Library Works

By the end you will know what Dadhichi is, how it builds a prompt out of a few reusable parts, and how it decides whether a prompt is good enough to keep.

## The problem with a pile of prompts

A prompt is the written instruction you give a language model, the kind of AI system behind chat assistants, to get a piece of work done. Anyone who uses these tools for a while starts saving the prompts that worked. A few months later there is a folder of them: one for explaining a networking idea, one for explaining a tax rule, one for reviewing a cover letter, and several that are nearly the same, with small changes nobody remembers making.

That folder has two problems. It keeps growing, because every new subject seems to need its own copy. And nobody can say which copy is best, because none of them was ever measured. The design this article draws on describes the end state as hundreds of near-duplicates nobody trusts.

Dadhichi is the answer that design proposes: a library of tested, reusable prompts, plus an engine that writes new prompts to the same standard. It is meant for any field, not only computing. What follows is a design dated November 2026. It describes the parts and how they fit, and it sets out a plan to build them one at a time, starting with a single prompt, so read it as a description of how the system is meant to work.

The idea underneath everything is that a prompt is a specification. It states what goes in, what should come out, what limits apply, and how you would check that the result is good. If you cannot say how you would know the output is good, the design counts the prompt as unfinished. That condition is what separates a library entry from a saved snippet.

Carry one request through the rest of this article. You want an explanation of bond duration, a measure of how sharply a bond's price moves when interest rates change, written so you can read it on a Kindle during a commute, with nothing to look up along the way.

So how does Dadhichi produce a prompt for that without keeping a separate copy for every subject?

## Building a prompt from parts

The trouble with a saved-prompt folder is that it multiplies, one copy per subject, and nothing in it is tested. Dadhichi's first move against the multiplying is to stop storing whole prompts per subject and build each one from separate parts.

The first part is the task pattern: the job being done, whatever the subject. Explaining one concept is a job. So is comparing named options, or reviewing a draft. The design expects about twelve patterns to cover most requests in any field, and it adds a new one only when a request cannot be served by an existing pattern plus a small adjustment. Your bond request uses the pattern called explain.

The second part is the reader profile: who consumes the output, and in what setting. The profile your request needs is called commuter, someone who reads top to bottom, once, with no way to look anything up. The design expects six to ten profiles in all.

The third part is the domain pack: what one field takes for granted, meaning its vocabulary, its standards, and its usual pitfalls. Your request needs the finance pack. The design says domain packs are written or reviewed by someone who knows the field, and that new ones are added as requests call for them.

The fourth part is the modifier, a small dial such as a cap on length, the language of the output, a tone, or plain text only. The design expects ten to twenty of these.

Underneath all four sits the kernel, one shared set of rules that hold for every good answer, whatever the job. The design gives two examples: plan silently before writing, and never use a term before introducing it.

A request is then located by three coordinates, written as pattern, reader and domain. Yours is explain, commuter, finance.

This is the point where Dadhichi is most often misread. It is tempting to picture it as a well-sorted collection, with a finance explainer stored somewhere, waiting to be copied. The design says plainly that it is not a collection of copy-paste snippets. The explain pattern with the IT pack produces an explainer of a computing idea; swap in the finance pack, change nothing else, and you get your bond duration explainer. The library does keep assembled, ready-to-paste prompts in a folder of their own, but each is the result of combining parts, not a prompt someone maintains by hand.

The design credits one rule with keeping the parts reusable: a pattern never names a field, and a domain pack never gives writing instructions. If the explain pattern mentioned bonds, it could not serve computing. If the finance pack told the model how to lay out paragraphs, it would be doing the pattern's job.

Parts can still disagree, so the design fixes an order of precedence. Your own request beats a modifier, a modifier beats the reader profile, the reader profile beats the pattern's defaults, and nothing overrides the kernel. If you add a modifier capping the piece at 500 words, that cap wins over whatever length the pattern would otherwise choose.

Once the parts are chosen, what does the finished prompt look like?

## The fixed shape of every prompt

You now hold the four kinds of part, the kernel beneath them, and the three coordinates that pick them for a request. When they are put together, the result always lands in the same shape.

Every library entry is one plain text file that opens with a short header of facts about it: its name, its version, whether it has been tested yet, and the inputs it needs.

Those inputs appear in the prompt as variables, placeholders written in capitals inside curly braces, such as {TOPIC}, which is where "bond duration" goes. A prompt that uses a variable its header does not list fails review.

After the header come seven sections, always in the same order, each wrapped in a tag with its name so the model can tell them apart. The first is the situation, and the reader profile fills it: for your request, a person on a bus with a Kindle and no browser.

The design explains why the situation leads. A model that knows who will read the output, and where, can make hundreds of small decisions correctly, while a list of rules covers only the cases its author thought of. For the same reason, every instruction in a library prompt carries its reason with it. This follows published advice from Anthropic, the company that makes the Claude language models.

Next comes the goal, one or two sentences on what the reader can do after reading. It gives the model a finish line, which keeps it from padding or drifting.

Then the plan: silent steps the model works through before writing anything. It lists what the reader must understand, cuts what they already know, sorts the rest by importance, puts it in an order where each idea needs only what came before, and picks a length. The design treats this step as what stops a model from over-explaining the easy parts and skipping the hard ones.

The write section holds the craft for this particular job, such as how an explainer should introduce a term. The domain section is filled from the pack; for you, the conventions of finance.

The last two sections close the loop. The check section is a list the model reviews its own draft against before answering. The output section pins down exactly what to return, so the reader gets the article and no preamble or offer to continue.

That shape is easy to fill when every part already exists. But who writes the prompt when the library lacks a part?

## The engine that writes new prompts

So far you have the parts and the seven-section shape they fill. Something still has to do the filling for a request it has never seen.

That job belongs to the engine, which is itself a prompt: a set of instructions given to a language model, telling it to turn a rough request into a finished prompt in the seven-section shape. The design includes its first version in full, ready to use as a model's standing instructions. It works in four steps.

First, it classifies. It maps the request to the three coordinates, so your request becomes explain, commuter, finance. If no pattern fits, it says so rather than forcing one. If a request contains two jobs, it splits it into two prompts that run one after the other.

Second, it asks, but only about what it cannot reasonably infer and what would change the prompt, and never more than three questions. If the request is clear enough it asks nothing and states its assumptions in one line. For your request it might simply assume you have no background in finance.

Third, it assembles, filling the seven sections from the library's parts. Where a part does not exist yet, it writes one in the same style and marks it as new. If the finance pack had not been written, the engine would draft one for this prompt and flag it, so a person can see what was invented on the spot.

Fourth, it checks. It rereads the prompt as someone with no context would, on the principle that if a person with minimal context could not follow it, the model will struggle too. It confirms that no instruction contradicts another, and then it names the two most likely ways the result could still fall short.

What comes back is four things: the classification in one line, any assumptions in one line, the prompt itself set apart in a block of its own, and those two failure risks, each paired with a test input that would expose it. The design singles out that last item as the one that matters most, because every prompt the engine writes arrives with its first two tests.

Which raises the question of what those tests are for, and what they decide.

## How a prompt earns its place

The engine hands over each new prompt with two inputs designed to trip it up. Those inputs are the first entries in the part of Dadhichi that decides what stays in the library.

The rule is that nothing enters untested. An entry is marked as tested only after it passes a fixed set of inputs, judged against written criteria. The reason comes from research: a large survey of published prompting studies found that small, seemingly irrelevant changes in wording shift results, and that rankings of prompting techniques do not carry over reliably from one setting to another. You cannot tell whether a change helps by reading it. You have to run it.

The fixed set of inputs is called the test set. Each pattern starts with six to ten inputs chosen to stress it, and grows toward about fifty, with every real failure added. It always includes five kinds: a trivial input, to see whether the answer stays short; a hard one, to see whether it stays clear; one outside the model's likely knowledge, to see whether it admits its limits; a vague one, to see how it handles missing detail; and one from a second field, to see whether the pattern really carries across. For the explain pattern, your bond request could serve as that second-field input.

The written criteria are called the rubric. It is a list of yes-or-no checks rather than impressions, so another model can apply it the same way every time. For the explain pattern there are seven, among them that every term is introduced before or at its first use, that no sentence depends on something that comes later, and that the trivial input stays under about 400 words.

The model applying the rubric is the grader. Following Anthropic's guidance on testing, it is a different model from the one that wrote the output, and it is allowed to reason before giving its verdict.

Some checks still need a person. The design notes that a grader can miss the two most important checks for an explainer, about undefined terms and ideas out of order, so a human reads the output on a phone, away from a desk, and counts the pauses. The target is zero.

Improving a prompt follows one rule. Run the old and new versions on the full test set and grade both. The new one replaces the old only if it passes more checks and fails none that the old one passed. A change that looks harmless still gets the full run.

Each pattern also keeps a failure log, one line per failure: the date, the input, which check failed, the suspected cause, and the version that fixed it. The design calls it the most valuable file in the library, because it records why each instruction exists.

All of these files live in Git, the tool programmers use to keep the full history of a set of files, compare any two versions, and roll back. Every part sits in its own plain text file, which also means any model or tool can read it.

Versions are numbered in three levels. A wording cleanup that keeps behaviour the same bumps the last number. A new capability with the same output shape bumps the middle one. A different output shape or planning logic bumps the first. A released version is never edited; a fix is always a new version.

One limit is built into the whole method: a prompt tuned on one model can get worse on the next. The design cites Anthropic's own example, an instruction to double-check that helps one model and makes a newer one over-check. So every entry records the model and date it was last verified, and when a new model arrives the tests are rerun before old entries are trusted. Sometimes the fix is removing an instruction rather than adding one.

The plan applies the same test to the architecture itself. The first step is to split one existing explainer prompt into a kernel, the explain pattern, the commuter profile and an IT pack, and score it on three topics. The second is to add a finance pack and a second reader profile without touching the pattern. If the explainer still passes, the design concludes that the separation of parts holds; if the pattern needs edits, that leak between parts is the thing to fix.

## The whole picture

Dadhichi treats a prompt as a specification and builds it from a few separate parts, a task pattern, a reader profile, a domain pack and modifiers, on top of a shared kernel, so that your bond duration explainer and a computing explainer differ only in the domain pack. Every assembled prompt takes the same seven-section shape, the engine fills that shape for new requests and hands each one over with its first two tests, and the testing system decides whether it enters the library or replaces an older version. Reading the engine's tests as the seed of the test set is the design's own framing; seeing the fixed shape as what lets parts be swapped and versions be compared is a reasonable reading of it, and the design states the reason for the shape in those terms. All of it is a design with a staged plan, beginning with a single explainer.

## Going further

Claude Project: a workspace in Anthropic's Claude app that holds files next to a set of standing instructions; the design suggests loading the library there, with the engine as the instructions, so it composes from the real files.

Examples in a prompt: sample outputs placed inside the prompt to show the desired form; the design uses three to five varied ones, noting research in which the choice and order of examples moved accuracy from under 50% to over 90%.

Draft, review, refine: the practice of having a model write, check its draft against criteria, then improve it; every pattern ends with a self-check, and high-stakes ones move the check into a second prompt.

Open questions: the design leaves two unsettled, whether the library is for personal use or shared use, which would need contribution rules, and which models it must support, which would mean running the tests on each.

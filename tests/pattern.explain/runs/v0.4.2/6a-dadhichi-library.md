# How the Dadhichi Prompt Library Works

By the end you will know what Dadhichi is built from, how it turns a rough request into a finished prompt, and how a prompt proves it deserves a place in the library.

## Why a pile of good prompts is not enough

A prompt is the written instruction you give an AI model such as Claude. Anyone who uses these models for a while starts keeping the prompts that worked: a good way to ask for an explanation, a good way to ask for feedback on a draft. Over time that collection grows into hundreds of near-copies, each tweaked for one occasion, and nobody can say which version is best or whether any of them still works.

Dadhichi is a design for doing this properly. It is a library of tested, reusable prompts, plus an engine that writes new prompts to the same standard, and it is meant for any field, not only IT. Everything below is the design as its own document, dated November 2026, lays it out. That document ends with a roadmap whose first step is splitting an existing explainer prompt into the library's parts, so read what follows as how the library is meant to work, not as a report on a finished system.

The idea underneath the whole design is that a prompt is a specification. It states its inputs, the output it is aiming for, the limits on that output, and tests that show whether the output is good. If you cannot say how you would recognise a good answer, the prompt is not finished.

Here is the request this article will follow. You want a clear explanation of what an API key is, the secret string a program sends to prove it is allowed to use a service, and you want to read it on a Kindle on the bus. In a pile of saved prompts, you would hunt for the nearest one and edit it by hand.

So what is the library made of, if not a pile of finished prompts?

## A kernel and four parts

A good prompt, in this design, is a specification with tests, and the aim is a small library of them rather than a heap of near-copies. Dadhichi keeps it small by building each prompt from separate parts instead of storing every finished prompt whole.

Under every prompt sits a shared base called the kernel. It holds what is true of any good answer, whatever the job: for example, plan silently before writing, and never use a term before introducing it. There is one kernel, and nothing overrides it.

On top of the kernel go four kinds of part. The first is the task pattern: the job being done, such as explaining a concept, reviewing a draft, or comparing options. The design expects ten to fifteen patterns in all and lists twelve. For your request, the pattern is explain.

The second is the reader profile: who reads the output, and where. One of the starter profiles is the commuter, who reads in a straight line with no way to look anything up. That is you on the bus.

The third is the domain pack: what a particular field takes for granted, such as its vocabulary, its standards and its usual pitfalls. Your request uses the IT pack. Domain packs are added as they are needed, and the design wants each one written or reviewed by someone who knows the field.

The fourth is the modifier: a small dial, such as a length cap, a language, a tone, or plain text only. A Kindle renders plain text well, so your request takes that modifier.

Your request now has an address with three coordinates, written explain / commuter / it, plus one modifier.

This is where people most often misread the idea. It is natural to assume a library like this needs a finance explainer, a medicine explainer, and a separate prompt for every subject. It does not. Swap the IT pack for a finance pack, change nothing else, and the same explainer produces a no-lookup explanation of bond duration. Subjects are unlimited, but jobs are few, so the library is organised by job. The design adds a new pattern only when a request cannot be served by an existing pattern plus a modifier, and names that rule as what stops the library turning into a snippet pile.

For the swap to work, the parts have to stay apart: a pattern never names a field, and a domain pack never gives writing instructions.

Parts can still pull in different directions, so the design fixes an order. Your own request beats the modifiers, the modifiers beat the reader profile, the reader profile beats the pattern's defaults, and the kernel stays underneath all of them.

How do these separate parts come together into one prompt you can paste?

## The shape of a prompt and the engine that builds it

Each prompt is assembled from the kernel and four parts: a pattern for the job, a reader profile, a domain pack and modifiers. What comes out has a fixed shape.

Every library entry is one Markdown file, Markdown being plain text with light marks for headings and emphasis. At the top sits a short header recording the entry's name, version, status, inputs, and the model and date it was last checked on. Below it come seven fixed sections, always in the same order, and that fixed shape is what lets entries be compared, tested and combined.

The first section is the situation: who reads the output, where, and what they cannot do. The reader profile fills it, so for you it describes someone on a bus with no browser. The design's reasoning is that a model told the reader's situation makes many small decisions correctly, while a list of rules covers only the cases its writer thought of.

A later section holds the plan: steps the model works through silently before writing, such as listing what the reader needs, cutting what they already know, and putting the rest in order. The design credits this step with preventing both over-explaining and under-explaining.

Another section, named domain, is where the domain pack goes. The IT pack's vocabulary and pitfalls land here, and swapping in finance changes this section and leaves the others alone.

Near the end comes the check: a list the model reviews its own draft against before it answers. The remaining sections state the goal, hold the writing rules for the job, and pin down exactly what to return.

Something has to put these pieces together, and that is the engine. It is a meta-prompt, meaning a prompt whose output is another prompt. You give it a rough request in your own words, and it works in four steps:

1. Classify: decide the pattern, the reader and the domain. If no pattern fits, it says so instead of forcing one.
2. Ask: put at most three short questions, only about things it cannot infer that would change the prompt, and none at all if the request is clear.
3. Assemble: fill the seven sections from the library's parts. Where a part does not exist yet, write one in the same style and mark it as new.
4. Check: reread the prompt as someone with no context, fix anything they would have to guess, and name the two most likely ways the result could still fall short.

The design calls the last part of that output the most important for engineering. Each of the two failure risks comes with a test input that would expose it, so every prompt the engine writes arrives with its first two test cases.

For your request, the engine would classify it as explain / commuter / it with plain text, ask nothing because the request is clear, and hand back the prompt along with two inputs chosen to break it.

What happens to those test inputs once they exist?

## How a prompt earns its place

The engine turns a rough request into a seven-section prompt and hands over two test inputs with it. Those inputs go into a test folder, because nothing enters the library untested.

An entry starts as a draft. It is marked as tested only after it passes a fixed set of test inputs judged against a written rubric. The set starts at six to ten inputs, grows toward about fifty, and gains every real failure that turns up. It must include a trivial input, to see whether the output stays short; a hard one, to see whether it stays clear; one outside the model's likely knowledge, to see whether it admits its limits; a vague one; and one from a second field, to see whether the pattern really generalises. An API key is one of the first three topics the roadmap names for the explainer.

The rubric is a list of yes or no checks rather than impressions, so that a second model, the grader, can apply it consistently. Following Anthropic's guidance, the design has the grading done by a different model from the one that wrote the output. The explainer's rubric has seven checks, among them that every term is introduced before or at its first use, and that a trivial input stays under about 400 words.

A grader can miss whether terms arrive in time and whether a sentence leans on something said later, and those two checks are the point of the explainer. So the design adds a human check: read the output on a phone, away from a desk, and count the times you have to stop. The target is zero.

A new version of a prompt replaces the old one only if, on the same full set, it passes more checks and fails none that the old one passed. Even a change that looks harmless gets the full run, because the research the design draws on finds that small wording changes move results unpredictably.

Each pattern also keeps a failure log, one line per failure: the date, the input, the check that failed, the suspected cause, and the version that fixed it. The design calls this the most valuable file in the library, because it records why each instruction exists.

The whole library lives in a Git repository. Git is a tool that records every change to a set of files, which gives history, side-by-side comparison of versions, and rollback without extra work. Each part is its own file, in folders for patterns, readers, domains, modifiers and tests, plus a folder of assembled prompts ready to paste, such as the one for explain, commuter and IT.

Version numbers have three levels. A wording cleanup with the same behaviour moves 1.0.0 to 1.0.1. A new capability or example with the same output shape moves it to 1.1.0. A different output shape or planning logic moves it to 2.0.0. A released version is never edited; a fix is always a new version.

Models change, and a prompt tuned for one can get worse on the next. That is why each entry records the model and date it was last verified. When a new model arrives, the tests are rerun before old entries are trusted, and the design expects that some instructions will then need removing rather than adding.

## The whole picture

Dadhichi treats a prompt as a specification with its own tests, and keeps the library small by building every prompt from one kernel and four swappable parts: a pattern for the job, a reader profile, a domain pack and modifiers. The engine takes a rough request, places it at an address such as explain / commuter / it, fills seven fixed sections from those parts, and returns the prompt with two inputs designed to break it. Those inputs join a test set graded by yes or no checks, and a new version wins only if it beats the old one on that same set, with Git keeping every version and the failure log keeping the reasons. Read together, and this joining is my reading of the design rather than its words, the pieces form a loop in which writing a prompt and testing it are one activity, which is what lets a small library stay trustworthy as it grows and as models change.

## Going further

Retired status: the third state an entry can have, after draft and tested, for parts that no longer earn their place.

Claude Project: the design suggests loading the library folder into one, with the engine file as its standing instructions, so the engine composes from the real files instead of from memory.

The Prompt Report: a large survey of prompting techniques by Schulhoff and colleagues, one of the research sources behind the design's rules.

Open questions: the design leaves undecided whether the library is for personal use or shared use, and which models it must support.

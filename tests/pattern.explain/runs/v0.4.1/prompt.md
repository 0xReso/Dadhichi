---
id: built.explain.commuter.it
kind: built
version: 0.4.1
status: draft            # released: 0.4.0 (promoted over 0.3.0 on 2026-11-18: 76/13/5 vs 69/17/8 on 94 shared cells). 0.4.1 = 0.4.0 + the head's five v0.4.0 grading edits (patch)
job: Explain one IT concept so it is understood in a single linear read on an e-reader, with no lookups
coordinates: explain / commuter / it
inputs:
  - TOPIC (required)    # the concept, e.g. "Kafka consumer groups"
  - SOURCE (optional)   # an article, RFC, or doc to explain; leave empty to use model knowledge
  - NOTES (optional)    # what this reader already knows, why they care, or a length limit
verified_on: 0.4.0 outputs written by claude-opus-5-5 subagents, 2026-11-18 (promoted, not yet tested)
tests: tests/pattern.explain/
---

# Flow-Read Explainer (IT)

How to use: copy everything inside the block below, replace the three `{VARIABLES}`, and paste it into any capable model. If you have no source, delete the text between the `<source>` tags but keep the tags. The prompt is written so the model plans silently and returns only the finished article.

```markdown
<source>
{SOURCE}
</source>

If the source block above is empty, work from your own knowledge. If it contains material, treat it as the authority for facts about the topic. You may reorder, compress, and leave out parts of it freely; your job is to make its core understood, not to cover everything it says.

A source can hold material at different levels of confidence, for example confirmed statements next to research, estimates, or someone's guess. When the source says how far a part can be trusted, carry that through to the page, because the reader cannot tell a fact from a guess unless the sentence says which it is. Build the mechanism and the running example from the confirmed parts. Give unconfirmed parts only the space the reader needs to recognise them and to see where they differ from the confirmed ones, not a full account of their contents, because every detail of a guess is a term the reader must learn for something that may not be true. Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms, adding nothing about who made them, where they circulate, or who uses them, because the reader cannot tell an origin you invented from one the source reported. Say it once, at the point where the confidence changes, not on every sentence, so the confirmed parts still read as plain statements. State that something is unknown or unpublished only when the source says so; where the source is merely silent, say that the sources behind this article do not cover it, and do not add "the company has not said" in front of that. Keep the source's own scope words too, because the reader takes "only" and "the one" as facts they cannot check. A sentence that joins two confirmed facts, such as "which is how..." or "so that...", is your reading in the body just as in "The whole picture", because the reader cannot tell your join from the source's. A heading or a list that puts two parts under one mechanism joins them in the same way: when the source gives two features separately, keep them separate, or say once that grouping them is your reading, and keep any grouping of your own out of a sentence that begins "the source confirms" or "the company confirms". The reader never saw the material you were given, so refer to it only in those words, and when the source block is empty, do not mention a source at all.

Where you add something the source does not say, keep it to well-established knowledge and word it as general practice ("assistants of this kind usually...") rather than as a statement about this topic, so the reader can see which sentences rest on the source and which on you. This applies to "The whole picture" as much as to the body: a step you inferred stays marked as inferred there.

<situation>
You are writing for one reader. They will read your piece on a Kindle or a phone while travelling: on a bus, a train, in a queue. They read from top to bottom, once, in short sittings that can be cut off at any stop. They have no browser open, no second screen, no notebook, and nobody to ask. If a word, acronym, or idea has not been explained on the page by the time they meet it, it stays a hole for the rest of the read, and every hole costs them the thread.

They are intelligent and curious, comfortable with everyday technology, and want to understand this topic properly: well enough to explain it to a colleague, follow a technical conversation about it, and later open the official documentation without feeling lost. The names they will need back at a desk, such as configuration settings, version differences, and optional features, belong in a short closing list, not in the main read, because every extra passage on a bus costs attention the core idea needs. They do not want a children's story or a pile of metaphors. They want the real thing, with its real names, arranged so it can be absorbed without effort.

What they are after is the feeling of a good book, where the next sentence is always the one they were ready for. Your job is to remove every reason to stop.

Notes about this reader from the person who sent you this, if any: {NOTES}
</situation>

<goal>
After one linear read, the reader can say in their own words what the topic is, what problem it exists to solve, how it works at the level that matters for using or discussing it, and where people commonly get it wrong. They also know its real vocabulary, because each term was handed to them at the moment they needed it.
</goal>

<plan>
Before writing anything, plan the piece. Do this privately, in your thinking if you have it. The reader sees only the finished article.

1. Find the core. Write, for yourself, one sentence that says what the topic is and why it exists. Everything in the piece serves that sentence. If you cannot write it yet, work out what the topic really is before going further. If the topic name is ambiguous, choose the IT meaning most likely intended and make that clear in the opening line. If the topic is a specific named product, library, or tool, the source block is empty, and you cannot recall concrete facts about it that you would stand behind, say so once, in plain words, in the line under the title as the output section describes: you have no reliable knowledge of this tool and will not describe it. Do not repeat it in the body, because the reader has just read it. If the topic name contains another term the reader may not know, such as the language or platform the tool is said to be built on, explain that term in the first body paragraph, because the reader has already met it in the title. Then write a simple-size piece on the kind of thing it is said to be, attribute no feature, design, or vocabulary to the named tool, and close with three or four questions the reader can take to its documentation. Keep it short, because the reader will take everything written under the tool's name to be about the tool and cannot check it from a bus seat.

2. List everything the reader must understand to reach the core: concepts, terms, acronyms, mechanisms, numbers. Be generous here; trimming comes next.

3. Remove what this reader already has. Everyday technology such as apps, browsers, passwords, files, Wi-Fi, and "the cloud" as a phrase needs no explanation. Explaining what someone already knows reads as padding and as condescension, and it uses up the attention they need for the hard parts.

4. Sort everything that is left into three tiers.
Foundation: ideas the core cannot stand without and that several later paragraphs lean on. Each gets a paragraph of its own, early, in the order the ideas depend on each other, and no two foundations share a paragraph. This matters most in the opening section, where it is tempting to introduce the whole cast at once: the system, its parts, and the people or programs on either side of it. Name only the one the next sentence needs and let the others arrive in their own paragraphs, because a paragraph that hands over four names is where a reader on a bus loses the thread. The named parts or properties of a foundation count as foundations of their own: when a thing has a payment, a sum and a date that each carry a name, or a system runs on machines that have a name of their own, give each name its own paragraph at the point the running example first uses it. A sentence of the form "this is called A, that is B, and the other is C" hands over three terms at once and is the most common place this rule breaks. When the mechanism rests on several kinds or members of one thing, such as several models or several kinds of namespace, give the general idea one paragraph and each member the reader must keep a short paragraph of its own, in the order the running example meets them. Keep this tier small, usually two to five items, because a piece that opens with many foundations feels like studying before the story starts.
In-flow: ideas needed at one point only. Each is introduced in a clause or a sentence at the moment it appears, and not before.
Later: details that are true and interesting but not needed for the core, such as edge cases, history, variants, configuration options, and competing products. Most of these are left out. Keep at most four for the closing "Going further" section.
When an idea could go in two tiers, choose the lighter one. A reader can live with a missing detail; they cannot live with a missing piece of the sentence they are reading.

5. Apply the body test to every passage you plan to write: keep it in the body only if, without it, the reader could not do what the goal promises, which is to say what the topic is, why it exists, and how its mechanism works step by step, or would fall into the trap from step 8. Each step of the mechanism passes, together with the one worked case that shows it. For a simple topic the mechanism is a single exchange, so it passes as a few sentences, and a numbered walk-through, a second story of the same mistake, and neighbouring topics the reader did not ask about do not pass. A refinement of a step, an option, or a second case of a point already made does not. Configuration setting names, differences between versions or vendors, performance optimisations, alternative implementations, and history fail this test unless the core truly depends on them. Passages that fail go to "Going further" as one line each, or are dropped. This test matters most for deep topics, where an expert writer is most tempted to include everything they know.

6. Order the path. Start with the problem, the situation that made someone build this, because a reader who feels the problem wants the solution. Then move from foundations to the mechanism to its consequences. Check that every step needs only what came before it.

7. Choose one running example: a single concrete scenario with specific names and numbers, carried through the whole piece. Returning to the same example lets the reader build on a picture they already hold instead of starting a new one in every section. Use an analogy only where it carries the actual mechanism, and say in one line where it stops being true, so the reader does not build on the wrong part of it.

8. Name the trap. Identify the most common misunderstanding of this topic and decide where in the path it would naturally arise, so you can correct it at that point.

9. Set a word budget: one number, decided now and held to. Size it to the topic, not to an idea of thoroughness, and judge the size from your core sentence in step 1, not from the length of your list in step 2, because a long list makes any topic look bigger than it is. A topic is simple when its core is one thing with one job: a single object or value and what is done with it, with no chain of several stages or several machines that the reader has to follow in order. What a port number is, what a file extension is, and what a checksum is are simple. A simple topic gets about 450 words, never more than 600, written as continuous prose with no headings other than an optional "Going further" at the end, and no "The whole picture" section. At that size the mechanism is told once, in a few sentences inside the running example. The ideas that surround it, such as how the thing is stored, how it is protected in transit, or what it is commonly confused with, get one clause each or one line in "Going further". A moderate one, such as how a domain name is turned into a server address, gets about 1,500, never more than 2,200. A deep one, such as how a language model generates text or how two computers set up an encrypted connection, gets about 3,500, never more than 4,500, split into chapters. Aim for the typical figure. The room between it and the upper limit is for a topic whose mechanism has more steps than usual; spend it only on passages that pass the body test, never on Later-tier material. Long source material does not make the piece long; it means there is more to cut. When the notes say the reader already holds some of what the topic rests on, take the words those passages would have needed off the budget rather than spending them elsewhere, because a reader who knows the ground wants to reach the new part sooner. If the notes above set a length, follow them instead.
</plan>

<write>
Write as a knowledgeable friend explaining across a table: plain, warm, and exact. Not a narrator and not a textbook. There are no characters, no invented plot, and no "imagine you are a data packet", because the reader asked to understand a technology, not to be entertained around it. The running example puts the reader in it as "you", or names a system, a shop, or a company, rather than a person with a name, because a named person reads as the start of a story.

Give the idea first, then its name. Describe what something does in plain words, then attach the real term: "The server hands back a short random string that proves you already logged in. That string is called a session token." Once a thing is named, use the same term every time. Switching between synonyms makes the reader wonder whether a new thing has appeared.

Expand each acronym the first time it appears, and prefer saying what it does over what the letters stand for when the letters do not help. "HTTP, the language browsers and servers use to talk to each other" helps more than "Hypertext Transfer Protocol".

Introduce at most one new idea per paragraph. If a paragraph needs two new terms, make it two paragraphs. This is what keeps the pace steady enough to read in a moving vehicle.

Make every sentence depend only on what came before it. If you find you need something you have not explained yet, move its explanation earlier. Sometimes that is impossible, because a rule's purpose depends on a mechanism the reader meets later. In that case describe the step as far as the present case needs, with no hint that more is coming, and introduce the further rule as a new fact at the point where the reader can see why it exists. Leave out phrases such as "as you will see", "more on this later", and "we will come back to this"; each one tells the reader a piece is missing, and they carry that worry until it arrives.

Make numbers tangible. "About 50 milliseconds, quicker than a blink" is absorbed at reading speed; "50 ms" alone is a fact the reader has to decode.

Describe structure in words. The page will have no diagrams, tables, or links, so when something has parts or steps, walk through them in order as if pointing at each one. A short flat list is fine for steps that truly happen in sequence; everything else is prose.

Use code only when the topic is itself about code. Keep it to a few short lines and explain each line in prose straight after, because e-readers wrap wide code badly and the reader cannot run it.

A moderate piece is divided into three to five sections and a deep piece into chapters, each under a "##" heading, and everything in this paragraph applies to both. Make each one readable in five minutes at most, the gap between a few stops. Give each a plain, descriptive heading. Open every chapter after the first with a sentence or two that reminds the reader what they now hold, woven into the prose rather than labelled as a recap, so someone resuming after a break picks up the thread without scrolling back. Keep that reminder to two sentences at most. End each chapter with a single sentence that raises the question the next chapter answers, so there is a pull forward. Do not summarise a chapter at its end; the next chapter's opening already does that, and summarising at both ends repeats the same material twice.

Be accurate. Use the terminology a practitioner would use. Where behaviour differs between versions, vendors, or configurations, say so in one sentence instead of presenting one case as universal, and put the details, if they are worth keeping, in "Going further". If you are not confident about a detail, say so or leave it out. The reader cannot check you from a bus seat, which makes their trust the whole arrangement.

Respect the reader. Leave out "simply", "just", "obviously", and "as everyone knows"; if it were obvious, they would not be reading. Open with substance rather than an announcement of what the article will do. Apart from the closing section described under output, do not end with a summary of what was said.
</write>

<domain>
Field notes for information technology, to draw on where they apply.

Orientation. Most IT topics sit somewhere on one of three maps: the path of a request from a user's device across a network to a server and back; the layers inside one machine, from the app a person uses down through the operating system to the hardware; or the life of data, from being created to being stored, moved, and read. Placing a topic on one of these maps early tells the reader where they are.

Common foundations. A small set of ideas sits under a large share of IT topics: client and server; a request and its response; a program running as a process; memory, which is fast and temporary, versus disk, which is slower and lasts; latency, the delay before something arrives; state, what a system remembers between one moment and the next; a protocol, an agreed set of rules for a conversation between machines; and an API, the published way one program asks another to do something. When a topic rests on one of these, that idea is usually a foundation.

Pairs that are often confused: authentication (proving who you are) and authorization (what you are allowed to do); encryption (reversible with a key), hashing (one way), and encoding (a change of format with no secrecy); concurrency (handling several things in overlapping time) and parallelism (doing several things at the same instant); latency and bandwidth; a process and a thread; a library and a framework; a container and a virtual machine; TLS and HTTPS; Git and GitHub; a model and the product built on top of it. If the topic touches one side of a pair, the reader may already be holding the other one by mistake.

Marketing names and mechanisms. Many industry terms, such as serverless, zero trust, or AI-powered, name a product category or a philosophy rather than a mechanism. Serverless code still runs on servers; someone else manages them. Readers understand these terms best once they see what actually happens underneath.

Standards and implementations. A specification, such as an RFC or a protocol standard, says how something should behave; products implement it, often with differences and extensions. Claims about "how X works" are usually claims about the standard unless a product is named.

Scale. Rough orders of magnitude worth carrying: reading from memory takes around a tenth of a microsecond; reading from a fast solid-state drive takes tens to hundreds of microseconds; a network round trip inside one data centre takes under a millisecond; a round trip across a continent or an ocean takes tens to a couple of hundred milliseconds. Sizes run from kilobytes for a text message to gigabytes for a film. These gaps explain many design decisions, such as why caches exist.

Change. Product names, defaults, prices, and version details change quickly. Facts that depend on a date or a version are best marked as such.

Security topics read best when the threat comes first: what an attacker could do and why it matters. The defence then arrives as the answer to a problem the reader already feels.
</domain>

<check>
Before answering, reread your draft the way the reader will: top to bottom, once, with no outside help. Fix anything that fails one of these.

Every term, acronym, and named technology is explained before or at its first use.
No paragraph hands the reader more than one new term, and the names of products, projects, companies, commands, and the boxes or layers of a diagram count as terms. The one exception is a pair defined against each other, such as a request and its response, which can share a paragraph. Where a paragraph names more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again. Where a paragraph lists several kinds or examples of one thing, keep the one the running example uses and leave the others out or give one a line in "Going further", because to a reader on a bus a list of names is a list of lookups.
No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come. Look at every clause that mentions what comes next, such as "which matters a little further on", "which is what the next idea handles", "that detail matters shortly", or "it is also where its limits come from", and end the sentence before it, because each one hands the reader a missing piece to carry. The single question that closes a chapter is the one exception, and it is sound only if nothing before it depended on the answer.
Nothing the reader already knew is explained.
Every passage passes the body test from your plan. Any that fails moves to "Going further" or is deleted.
Estimate the word count. If it is over the budget from your plan, cut in this order: passages that fail the body test, repeated explanations of the same point, extra examples beyond the running one, then whole in-flow ideas the core can stand without. Remove an idea whole rather than squeezing the explanation of the ones that stay, because a compressed explanation is harder to follow on a bus than a longer piece. If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is. When the notes say the reader already holds part of the ground, the typical figure for the size becomes the upper limit, so practical tips and second pitfalls go to "Going further" instead of into the words the notes freed.
No section or chapter ends with a summary of itself.
The running example is used consistently and its numbers agree with each other.
The common misconception is corrected where it arises.
Every "##" section or chapter after the first, apart from "The whole picture" and "Going further", opens with a sentence or two on what the reader now holds, so it can be picked up cold. This includes the second one: the problem set up in the first section is something the reader holds, and the second section opens by restating it.
Nothing needs a table, a link, an image, or wide code to make sense.
Every technical claim is correct, and any uncertain point is marked as uncertain. If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture". Then find every sentence that says "only", "the one", "the single" or "nothing but" about the topic, and keep the limit only if the source states it in those terms. Otherwise name the part without the limit, because such a claim becomes false as soon as a second case exists, and often your own draft names that case a few paragraphs later.
</check>

<output>
Return only the article, in plain Markdown that renders cleanly on an e-reader:

A title.
One line under the title saying what the reader will understand by the end. If the topic is a named tool you have no reliable knowledge of, this line says that plainly instead, because it is the first thing the reader meets under the tool's name. That statement is written to the reader and is part of the article, not a note to the person who sent this.
The body: continuous prose for a simple topic; three to five sections under "##" headings for a moderate one; chapters under "##" headings for a deep one.
For moderate and deep pieces, a closing section titled "The whole picture": one paragraph showing how the pieces connect. This is not a list of everything said; it is the core sentence from your plan, now fully earned. If you say which steps are confirmed, call a step confirmed only when the source states it; a link you drew between confirmed parts, such as which part feeds which, stays marked as your reading there.
Optionally, a final section titled "Going further" with two to four terms from the Later tier, each with one line on what it is, so the reader knows what to look up when they are back at a desk.

Leave out your plan, any notes to the person who sent this, and any offer to expand.
</output>

Topic: {TOPIC}
```

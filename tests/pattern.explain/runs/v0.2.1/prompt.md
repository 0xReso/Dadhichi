---
id: built.explain.commuter.it
kind: built
version: 0.2.1
status: draft            # v0.1.0 failed checks 4-5; v0.2.0 fixed them; v0.2.1 applies head gate review
job: Explain one IT concept so it is understood in a single linear read on an e-reader, with no lookups
coordinates: explain / commuter / it
inputs:
  - TOPIC (required)    # the concept, e.g. "Kafka consumer groups"
  - SOURCE (optional)   # an article, RFC, or doc to explain; leave empty to use model knowledge
  - NOTES (optional)    # what this reader already knows, why they care, or a length limit
verified_on: not yet verified
tests: tests/pattern.explain/
---

# Flow-Read Explainer (IT)

How to use: copy everything inside the block below, replace the three `{VARIABLES}`, and paste it into any capable model. If you have no source, delete the text between the `<source>` tags but keep the tags. The prompt is written so the model plans silently and returns only the finished article.

```markdown
<source>
{SOURCE}
</source>

If the source block above is empty, work from your own knowledge. If it contains material, treat it as the authority for facts about the topic. You may reorder, compress, and leave out parts of it freely; your job is to make its core understood, not to cover everything it says. Where you add something the source does not say, keep it to well-established knowledge.

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

1. Find the core. Write, for yourself, one sentence that says what the topic is and why it exists. Everything in the piece serves that sentence. If you cannot write it yet, work out what the topic really is before going further. If the topic name is ambiguous, choose the IT meaning most likely intended and make that clear in the opening line.

2. List everything the reader must understand to reach the core: concepts, terms, acronyms, mechanisms, numbers. Be generous here; trimming comes next.

3. Remove what this reader already has. Everyday technology such as apps, browsers, passwords, files, Wi-Fi, and "the cloud" as a phrase needs no explanation. Explaining what someone already knows reads as padding and as condescension, and it uses up the attention they need for the hard parts.

4. Sort everything that is left into three tiers.
Foundation: ideas the core cannot stand without and that several later paragraphs lean on. Each gets a short passage of its own, early, in the order the ideas depend on each other. Keep this tier small, usually two to five items, because a piece that opens with many foundations feels like studying before the story starts.
In-flow: ideas needed at one point only. Each is introduced in a clause or a sentence at the moment it appears, and not before.
Later: details that are true and interesting but not needed for the core, such as edge cases, history, variants, configuration options, and competing products. Most of these are left out. Keep at most four for the closing "Going further" section.
When an idea could go in two tiers, choose the lighter one. A reader can live with a missing detail; they cannot live with a missing piece of the sentence they are reading.

5. Apply the body test to every passage you plan to write: keep it in the body only if, without it, the reader could not do what the goal promises, which is to say what the topic is, why it exists, and how its mechanism works step by step, or would fall into the trap from step 8. Each step of the mechanism passes, together with the one worked case that shows it. A refinement of a step, an option, or a second case of a point already made does not. Configuration setting names, differences between versions or vendors, performance optimisations, alternative implementations, and history fail this test unless the core truly depends on them. Passages that fail go to "Going further" as one line each, or are dropped. This test matters most for deep topics, where an expert writer is most tempted to include everything they know.

6. Order the path. Start with the problem, the situation that made someone build this, because a reader who feels the problem wants the solution. Then move from foundations to the mechanism to its consequences. Check that every step needs only what came before it.

7. Choose one running example: a single concrete scenario with specific names and numbers, carried through the whole piece. Returning to the same example lets the reader build on a picture they already hold instead of starting a new one in every section. Use an analogy only where it carries the actual mechanism, and say in one line where it stops being true, so the reader does not build on the wrong part of it.

8. Name the trap. Identify the most common misunderstanding of this topic and decide where in the path it would naturally arise, so you can correct it at that point.

9. Set a word budget: one number, decided now and held to. Size it to the topic, not to an idea of thoroughness. A simple concept, such as what a port number is, gets about 450 words and no chapters, never more than 600. A moderate one, such as how a domain name is turned into a server address, gets about 1,500, never more than 2,200. A deep one, such as how a language model generates text or how two computers set up an encrypted connection, gets about 3,500, never more than 4,500, split into chapters. Aim for the typical figure. The room between it and the upper limit is for a topic whose mechanism has more steps than usual; spend it only on passages that pass the body test, never on Later-tier material. Long source material does not make the piece long; it means there is more to cut. If the notes above set a length, follow them instead.
</plan>

<write>
Write as a knowledgeable friend explaining across a table: plain, warm, and exact. Not a narrator and not a textbook. There are no characters, no invented plot, and no "imagine you are a data packet", because the reader asked to understand a technology, not to be entertained around it.

Give the idea first, then its name. Describe what something does in plain words, then attach the real term: "The server hands back a short random string that proves you already logged in. That string is called a session token." Once a thing is named, use the same term every time. Switching between synonyms makes the reader wonder whether a new thing has appeared.

Expand each acronym the first time it appears, and prefer saying what it does over what the letters stand for when the letters do not help. "HTTP, the language browsers and servers use to talk to each other" helps more than "Hypertext Transfer Protocol".

Introduce at most one new idea per paragraph. If a paragraph needs two new terms, make it two paragraphs. This is what keeps the pace steady enough to read in a moving vehicle.

Make every sentence depend only on what came before it. If you find you need something you have not explained yet, move its explanation earlier. Sometimes that is impossible, because a rule's purpose depends on a mechanism the reader meets later. In that case describe the step as far as the present case needs, with no hint that more is coming, and introduce the further rule as a new fact at the point where the reader can see why it exists. Leave out phrases such as "as you will see", "more on this later", and "we will come back to this"; each one tells the reader a piece is missing, and they carry that worry until it arrives.

Make numbers tangible. "About 50 milliseconds, quicker than a blink" is absorbed at reading speed; "50 ms" alone is a fact the reader has to decode.

Describe structure in words. The page will have no diagrams, tables, or links, so when something has parts or steps, walk through them in order as if pointing at each one. A short flat list is fine for steps that truly happen in sequence; everything else is prose.

Use code only when the topic is itself about code. Keep it to a few short lines and explain each line in prose straight after, because e-readers wrap wide code badly and the reader cannot run it.

When the piece is long enough for chapters, make each one readable in about five minutes, the gap between a few stops. Give each a plain, descriptive heading. Open every chapter after the first with a sentence or two that reminds the reader what they now hold, woven into the prose rather than labelled as a recap, so someone resuming after a break picks up the thread without scrolling back. Keep that reminder to two sentences at most. End each chapter with a single sentence that raises the question the next chapter answers, so there is a pull forward. Do not summarise a chapter at its end; the next chapter's opening already does that, and summarising at both ends repeats the same material twice.

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
No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come. The single question that closes a chapter is the one exception, and it is sound only if nothing before it depended on the answer.
Nothing the reader already knew is explained.
Every passage passes the body test from your plan. Any that fails moves to "Going further" or is deleted.
Estimate the word count. If it is over the budget from your plan, cut in this order: passages that fail the body test, repeated explanations of the same point, extra examples beyond the running one, then whole in-flow ideas the core can stand without. Remove an idea whole rather than squeezing the explanation of the ones that stay, because a compressed explanation is harder to follow on a bus than a longer piece. If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is.
No chapter ends with a summary of itself.
The running example is used consistently and its numbers agree with each other.
The common misconception is corrected where it arises.
Each chapter, if there are chapters, can be picked up cold from its opening lines.
Nothing needs a table, a link, an image, or wide code to make sense.
Every technical claim is correct, and any uncertain point is marked as uncertain.
</check>

<output>
Return only the article, in plain Markdown that renders cleanly on an e-reader:

A title.
One line under the title saying what the reader will understand by the end.
The body: continuous prose for a short piece, or chapters under "##" headings for a longer one.
For moderate and long pieces, a closing section titled "The whole picture": one paragraph showing how the pieces connect. This is not a list of everything said; it is the core sentence from your plan, now fully earned.
Optionally, a final section titled "Going further" with two to four terms from the Later tier, each with one line on what it is, so the reader knows what to look up when they are back at a desk.

Leave out your plan, any notes to the person who sent this, and any offer to expand.
</output>

Topic: {TOPIC}
```

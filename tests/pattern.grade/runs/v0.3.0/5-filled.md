<graded_task>
<source>
[source shown separately in graded_source]
</source>

If the source block above is empty, work from your own knowledge. If it contains material, treat it as the authority for facts about the topic. You may reorder, compress, and leave out parts of it freely; your job is to make its core understood, not to cover everything it says.

A source can hold material at different levels of confidence, for example confirmed statements next to research, estimates, or someone's guess. When the source says how far a part can be trusted, carry that through to the page, because the reader cannot tell a fact from a guess unless the sentence says which it is. Build the mechanism and the running example from the confirmed parts. Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms. Say it once, at the point where the confidence changes, not on every sentence, so the confirmed parts still read as plain statements. State that something is unknown or unpublished only when the source says so; where the source is merely silent, say that the material you were given does not cover it.

Where you add something the source does not say, keep it to well-established knowledge and word it as general practice ("assistants of this kind usually...") rather than as a statement about this topic, so the reader can see which sentences rest on the source and which on you. This applies to "The whole picture" as much as to the body: a step you inferred stays marked as inferred there.

<situation>
You are writing for one reader. They will read your piece on a Kindle or a phone while travelling: on a bus, a train, in a queue. They read from top to bottom, once, in short sittings that can be cut off at any stop. They have no browser open, no second screen, no notebook, and nobody to ask. If a word, acronym, or idea has not been explained on the page by the time they meet it, it stays a hole for the rest of the read, and every hole costs them the thread.

They are intelligent and curious, comfortable with everyday technology, and want to understand this topic properly: well enough to explain it to a colleague, follow a technical conversation about it, and later open the official documentation without feeling lost. The names they will need back at a desk, such as configuration settings, version differences, and optional features, belong in a short closing list, not in the main read, because every extra passage on a bus costs attention the core idea needs. They do not want a children's story or a pile of metaphors. They want the real thing, with its real names, arranged so it can be absorbed without effort.

What they are after is the feeling of a good book, where the next sentence is always the one they were ready for. Your job is to remove every reason to stop.

Notes about this reader from the person who sent you this, if any: 
</situation>

<goal>
After one linear read, the reader can say in their own words what the topic is, what problem it exists to solve, how it works at the level that matters for using or discussing it, and where people commonly get it wrong. They also know its real vocabulary, because each term was handed to them at the moment they needed it.
</goal>

<plan>
Before writing anything, plan the piece. Do this privately, in your thinking if you have it. The reader sees only the finished article.

1. Find the core. Write, for yourself, one sentence that says what the topic is and why it exists. Everything in the piece serves that sentence. If you cannot write it yet, work out what the topic really is before going further. If the topic name is ambiguous, choose the IT meaning most likely intended and make that clear in the opening line. If the topic is a specific named product, library, or tool, the source block is empty, and you cannot recall concrete facts about it that you would stand behind, say so in plain words in the first two sentences: you have no reliable knowledge of this tool and will not describe it. Then write a simple-size piece on the kind of thing it is said to be, attribute no feature, design, or vocabulary to the named tool, and close with three or four questions the reader can take to its documentation. Keep it short, because the reader will take everything written under the tool's name to be about the tool and cannot check it from a bus seat.

2. List everything the reader must understand to reach the core: concepts, terms, acronyms, mechanisms, numbers. Be generous here; trimming comes next.

3. Remove what this reader already has. Everyday technology such as apps, browsers, passwords, files, Wi-Fi, and "the cloud" as a phrase needs no explanation. Explaining what someone already knows reads as padding and as condescension, and it uses up the attention they need for the hard parts.

4. Sort everything that is left into three tiers.
Foundation: ideas the core cannot stand without and that several later paragraphs lean on. Each gets a short passage of its own, early, in the order the ideas depend on each other. Keep this tier small, usually two to five items, because a piece that opens with many foundations feels like studying before the story starts.
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
Write as a knowledgeable friend explaining across a table: plain, warm, and exact. Not a narrator and not a textbook. There are no characters, no invented plot, and no "imagine you are a data packet", because the reader asked to understand a technology, not to be entertained around it.

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
No paragraph hands the reader more than one new term. Where a paragraph names two or more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again.
No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come. The single question that closes a chapter is the one exception, and it is sound only if nothing before it depended on the answer.
Nothing the reader already knew is explained.
Every passage passes the body test from your plan. Any that fails moves to "Going further" or is deleted.
Estimate the word count. If it is over the budget from your plan, cut in this order: passages that fail the body test, repeated explanations of the same point, extra examples beyond the running one, then whole in-flow ideas the core can stand without. Remove an idea whole rather than squeezing the explanation of the ones that stay, because a compressed explanation is harder to follow on a bus than a longer piece. If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is.
No section or chapter ends with a summary of itself.
The running example is used consistently and its numbers agree with each other.
The common misconception is corrected where it arises.
Every "##" section or chapter after the first, apart from "The whole picture" and "Going further", opens with a sentence or two on what the reader now holds, so it can be picked up cold.
Nothing needs a table, a link, an image, or wide code to make sense.
Every technical claim is correct, and any uncertain point is marked as uncertain. If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture".
</check>

<output>
Return only the article, in plain Markdown that renders cleanly on an e-reader:

A title.
One line under the title saying what the reader will understand by the end. If the topic is a named tool you have no reliable knowledge of, this line says that plainly instead, because it is the first thing the reader meets under the tool's name. That statement is written to the reader and is part of the article, not a note to the person who sent this.
The body: continuous prose for a simple topic; three to five sections under "##" headings for a moderate one; chapters under "##" headings for a deep one.
For moderate and deep pieces, a closing section titled "The whole picture": one paragraph showing how the pieces connect. This is not a list of everything said; it is the core sentence from your plan, now fully earned.
Optionally, a final section titled "Going further" with two to four terms from the Later tier, each with one line on what it is, so the reader knows what to look up when they are back at a desk.

Leave out your plan, any notes to the person who sent this, and any offer to expand.
</output>

Topic: Alexa for Shopping
</graded_task>

<graded_source>
# Source pack: Alexa for Shopping (compiled 2026-11-15)

Three kinds of material follow, kept separate on purpose. Part A is confirmed by Amazon or by reporting on Amazon's announcements. Part B is published Amazon research. Part C is a guessed architecture diagram produced by another AI assistant; it is not Amazon's design, and nothing in it is confirmed unless it also appears in Part A or B.

## Part A: Confirmed facts

Sources: Amazon's own announcement page (aboutamazon.com, "Amazon's next-gen AI assistant for shopping", updated after May 13, 2026) and Reviewed.com, "How to use Alexa for Shopping" (August 5, 2026).

Name and history
- Amazon launched a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping and folded into Alexa+, Amazon's generative-AI version of Alexa.
- It shares conversation context with Alexa+ and Echo devices, so a conversation started on an Echo can continue in the shopping app.

Where people use it
- The Amazon Shopping app (an Alexa icon in the navigation bar), the Amazon website, the homepage, product pages, and Amazon Lens Live (the camera-based search).
- On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it.
- Users can type or speak. No Prime membership or Echo device is required to use it.

Models and infrastructure
- It runs on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models.
- It draws on several models: Anthropic's Claude Sonnet, Amazon's Nova models, and a custom model Amazon built for shopping. The custom model uses Amazon's product catalog, customer reviews, community questions and answers, and information from the web.
- A real-time router picks which model handles each query, by query type, to balance capability, response time, and answer quality.
- It uses retrieval-augmented generation (RAG): before answering, it fetches relevant material and gives it to the model to ground the answer. Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue as sources for product and trend questions.
- Amazon says Bedrock features such as prompt caching and parallel tool calling are used to reduce response time.

What it can do
- Answer product questions, compare products, check compatibility against past orders, show 30- and 90-day price history, and list current deals.
- Add items to the cart, including from a photo of a handwritten grocery list. Items in the cart are reviewed by the customer before checkout.
- Price alerts at a target price.
- Auto-buy for Prime members: it watches the price and, when it reaches the customer's target, completes the purchase with the default payment method and address, then notifies the customer, who has 24 hours to cancel free. A request lasts up to six months.
- Buy for Me: it can buy items from other brands' websites on the customer's behalf. Shop Direct instead sends the customer to the merchant's own site.
- Customer service tasks: tracking packages, returns, refunds, order changes, and handing over to a human agent.

Memory
- "Account memory" built from shopping activity, plus details customers tell it (family members, pets, dietary preferences). Customers can ask what it remembers and correct it in conversation, and manage history on a Review Alexa History page.

Numbers Amazon has published
- More than 250 million customers used it in 2025.
- Customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.
- Auto-buy customers save an average of 20 percent per purchase.

Not confirmed anywhere public: the internal architecture. No Amazon document describes how the components are wired together.

## Part B: Published Amazon research: COSMO

Source: "COSMO: A large-scale e-commerce common sense knowledge generation and serving system at Amazon", Amazon Science, SIGMOD 2024.
- COSMO is a knowledge graph of shopping common sense: links between what people intend and what products serve that intent. The paper's example: a search for shoes by pregnant shoppers is connected to slip-resistant shoes through the relation (pregnant, requires, slip-resistant).
- It is built by mining search-then-buy and bought-together behaviour, and generated at scale by a fine-tuned language model (COSMO-LM) trained on about 30,000 human-annotated instructions. It covers 18 major product categories.
- The paper says COSMO is deployed in Amazon search, for search relevance, session-based recommendations and search navigation.
- Not confirmed: that Alexa for Shopping uses COSMO. It is plausible, since both serve shopping intent, but no source says so.

## Part C: A guessed architecture (produced by another AI, not Amazon)

The diagram proposes these layers, top to bottom:
1. Touchpoints: mobile app, web, Echo (voice), search bar.
2. API gateway and ingestion: API gateway, request ingestion, event streaming (Amazon Kinesis), authentication and rate limiting.
3. Two parallel front ends: natural language and voice processing (speech-to-text, intent and entity detection, multilingual processing), and search-bar interception for AI overviews (query understanding, AI summaries, intent routing).
4. A conversational and intent core: Bedrock models plus the COSMO knowledge graph.
5. Three data services: a catalog and RAG engine (product catalog; documents, reviews, policies, FAQs), user memory and profile (preferences, session memory, personalisation), and a price and inventory database (real-time price, availability, offers).
6. Action and commerce orchestration: add to cart, add to list, Buy for Me, checkout.

Which parts line up with Part A: the touchpoints, Bedrock models, RAG over catalog and reviews, user memory, real-time price for alerts and auto-buy, and the cart and Buy for Me actions. Which parts are the diagram's own guesses: Kinesis, the specific gateway layout, COSMO inside the core, and the separation into these exact boxes. The diagram also omits the confirmed model router.

</graded_source>

<graded_output>
# Alexa for Shopping, From Question to Cart

By the end you will know what Amazon's shopping assistant is, how it turns a question into a grounded answer or a purchase, and which parts of its design are confirmed and which are guesses.

## A search box that cannot hear questions

A search box is good at nouns. Type "water filter cartridge" and you get a long list of cartridges. It struggles with the question you actually have: "Will this cartridge fit the filter jug I bought in March, and is now a good time to buy?" Answering that takes several things a list of results cannot do. Something has to read the question as a sentence, know what you bought in March, check the product details for compatibility, look at how the price has moved, and then explain all of that in plain words.

Alexa for Shopping is Amazon's answer to that gap. It is a conversational assistant: you type or speak a question, it replies in sentences, and it can also act for you. It began life as a shopping chatbot called Rufus. On May 13, 2026, Amazon renamed it Alexa for Shopping and folded it into Alexa+, the generative-AI version of the Alexa voice assistant. Because of that merger it shares conversation context with Alexa+ and Echo speakers, so a conversation started in the kitchen with an Echo can carry on later in the shopping app.

You reach it from many places: an Alexa icon in the Amazon Shopping app's navigation bar, the Amazon website and homepage, product pages, and Amazon Lens Live, the camera-based search. On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it instead of a results page. You do not need a Prime membership or an Echo device to use it.

Keep the filter question in mind; the rest of this piece follows it through. Amazon has said more than 250 million customers used the assistant in 2025, so the obvious question is what kind of machine handles that many conversations.

## Several models and a router

The engine underneath any assistant like this is a large language model: a program trained on vast amounts of text that, given some words, produces a fluent continuation. That is what lets it read "will this fit the jug I bought in March" as a request rather than a bag of keywords, and what lets it write a reply in sentences.

Here is the point most people get wrong. It is tempting to picture one giant AI that has memorised Amazon. Alexa for Shopping is not that. It draws on several models: Anthropic's Claude Sonnet, Amazon's own Nova models, and a custom model Amazon built for shopping. That custom model draws on Amazon's product catalog, customer reviews, community questions and answers, and information from the web.

Different questions suit different models. A quick "where is my package?" needs a fast reply more than deep reasoning; a comparison of three espresso machines needs more care. So each query first passes through a real-time router, a component that looks at what kind of question it is and picks the model to handle it. Amazon describes the router's job as balancing capability, response time, and answer quality. Your filter question, mixing past orders, compatibility, and price, would be routed by type like any other; the material given here does not say which model would get it.

All of these models run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is the platform; the models are what run on it; Alexa for Shopping is the product built on top. Keeping those three apart avoids a common muddle, the idea that "Bedrock" or "Claude" is the shopping assistant.

A model on its own, though, only knows what it absorbed in training. It does not know what is in stock today or what you bought in March, so the next question is how the assistant gets current facts in front of it.

## Grounding the answer in real material

So far a router has picked a language model for your question. That model still needs today's facts, and the technique for supplying them has a name.

Before the model answers, the assistant fetches material relevant to the question and hands it to the model along with the question, so the reply is built on that material rather than on memory alone. This is called retrieval-augmented generation, usually shortened to RAG. The word "grounded" is used for an answer produced this way: it stands on documents the system actually looked up.

For your filter question, the retrieved material would plausibly include the cartridge's product page, its listed compatible jugs, reviews mentioning your jug's model, and community answers from people who asked the same thing. Amazon says the assistant can check compatibility against past orders and show 30- and 90-day price history, so it can tell you both whether the cartridge fits and whether today's price is high or low compared with the last three months. For broader product and trend questions, Amazon names outside publications among its sources, including The New York Times, USA Today, Good Housekeeping and Vogue.

Retrieval also covers you. The assistant keeps what Amazon calls account memory: a picture built from your shopping activity, plus details you choose to tell it, such as family members, pets, or dietary preferences. Your March order is part of that memory, which is how "the jug I bought in March" can be resolved without you digging up an order number. You can ask it what it remembers, correct it in the conversation, and manage the history on a page called Review Alexa History.

An answer, however well grounded, still leaves you to do the buying. The assistant can go a step further than talking.

## From answers to actions

By now the filter question has been routed to a model, and that model has been handed your order history, the product details, and the price record. What remains is doing something about it.

Assistants of this kind usually act through tools: defined operations, such as "add this item to the cart", that the model can ask the surrounding system to carry out. Amazon's published list of what Alexa for Shopping can do reads like such a set of operations.

The simplest is adding items to your cart, which it can even do from a photo of a handwritten grocery list. Items it adds are reviewed by you before checkout, so nothing is bought at this step.

Next is a price alert. Say the cartridge is 32 dollars today and the price history shows it has dipped lower before. You can ask to be told when it reaches 25 dollars.

Auto-buy goes further, and it is available to Prime members. You set the same 25-dollar target, and the assistant watches the price. When it reaches your target, it completes the purchase with your default payment method and address, then notifies you. You then have 24 hours to cancel at no cost, and a request lasts up to six months. Amazon says auto-buy customers save an average of 20 percent per purchase. This is the second place people misjudge the assistant: auto-buy is not an AI shopping freely with your card. It is a standing order with fixed limits that you set, a price, a time window, and a cancellation period.

Two features reach beyond Amazon's own shelves. Buy for Me lets the assistant buy an item from another brand's website on your behalf. Shop Direct, by contrast, sends you to the merchant's own site to buy it yourself.

Finally, the assistant handles customer-service tasks: tracking packages, returns, refunds, and order changes, and it can hand you over to a human agent when it needs to. Amazon also reports that customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.

That covers what Amazon has said the assistant does. How the pieces are wired together inside is a different matter.

## What is confirmed and what is guessed

Everything so far, the name change, the models, the router, Bedrock, RAG, account memory, and the actions, comes from Amazon's own announcement and from reporting on it. The confidence drops from here.

No Amazon document describes the internal architecture, meaning how these components are actually connected. Two kinds of material fill that gap, and neither is a description of the real system.

The first is published Amazon research on a system called COSMO, presented at the SIGMOD database conference in 2024. COSMO is a knowledge graph, a large web of facts stored as links between things, here linking what shoppers intend with the products that serve that intent. The paper's example: shoe searches by pregnant shoppers are connected to slip-resistant shoes through the link "pregnant, requires, slip-resistant". It was built by mining search-then-buy and bought-together behaviour, and generated at scale by a fine-tuned language model, COSMO-LM, trained on about 30,000 human-annotated instructions. It covers 18 major product categories. The paper says COSMO is deployed in Amazon search, for search relevance, session-based recommendations and search navigation. No source says Alexa for Shopping uses it. That is plausible, because both serve shopping intent, but it is unconfirmed.

The second is an architecture diagram that circulates online, which the source you were given describes as produced by another AI assistant, not by Amazon. It stacks six layers: the touchpoints; an API gateway with ingestion and event streaming on Amazon Kinesis; parallel voice and search-bar front ends; a core of Bedrock models plus COSMO; three data services for catalog and RAG, user memory, and price and inventory; and an action layer for cart, lists, Buy for Me and checkout. Some of it lines up with Amazon's statements: the touchpoints, Bedrock, RAG over catalog and reviews, user memory, real-time prices for alerts and auto-buy, and the cart and Buy for Me actions. The rest is the diagram's own guessing: Kinesis, the gateway layout, COSMO in the core, and the split into exactly these boxes. It also leaves out the one internal component Amazon has confirmed, the model router. If you meet that diagram in a meeting, treat it as a plausible sketch, not as Amazon's design.

## The whole picture

Alexa for Shopping, formerly Rufus and now part of Alexa+, exists because a search box cannot answer a shopper's real questions. When you ask whether a cartridge fits the jug you bought in March, a real-time router sends the question to one of several language models running on Amazon Bedrock; the assistant retrieves the product details, reviews, price history, and your account memory and hands them to that model so its answer is grounded; and then, if you ask, it acts, adding to your cart, watching for your 25-dollar target, or buying within the limits you set. Those steps are confirmed by Amazon. How they are wired together inside is not published, so anything more detailed, including a role for COSMO, is research or guesswork.

## Going further

- Amazon Lens Live: the camera-based search where the assistant also appears, worth exploring for questions about things you can point a phone at.
- Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to cut response time, the first by reusing work on repeated parts of a request, the second by running several tool operations at once.
- Review Alexa History: the page where you view and manage what the assistant has recorded about your conversations.
- The COSMO paper: "COSMO: A large-scale e-commerce common sense knowledge generation and serving system at Amazon", SIGMOD 2024, for the full method behind the knowledge graph.

</graded_output>

<graded_counts>
wc -w: 1955 words
</graded_counts>

<rubric>
# Rubric: pattern.explain

Yes/no checks. Grade with a different model from the one that wrote the output, and let the grader reason before giving each verdict.

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | No lookups | Every term, acronym, and named technology is introduced before or at first use |
| 2 | Linear | No sentence depends on something that comes later |
| 3 | Accurate | No technical error; real terminology is used |
| 4 | Proportional | Within the prompt's budget: simple ≤600, moderate ≤2,200, deep ≤4,500 words |
| 5 | No padding | No section could be deleted without leaving a gap |
| 6 | Resumable | Each section or chapter (anything under a "##" heading, excluding "The whole picture" and "Going further") after the first restates what the reader holds so far |
| 7 | Plain text | Reads correctly on an e-reader: no tables, links, images, nested lists, or wide code |
| 8 | Not dumbed down | No fictional framing or characters; real names kept; analogies state where they break |
| 9 | Trap handled | The most common misconception about the topic is named and corrected |
| 10 | Clean output | No visible plan, no preamble, no offer to expand |
| 11a | Complete | Every mechanism step named in "The whole picture" is explained in the body with the running example |
| 11b | Unhurried | No paragraph introduces more than two new terms, and two only when they are a pair defined against each other |
| 12 | Unknown topic (input 4 only) | The first two sentences say the tool is not known, and nothing is attributed to it |
| 13 | Source confidence (inputs with a SOURCE) | No statement is presented at higher confidence than the source gives it, and nothing about the source's origin is invented |

## Human check

Checks 1 and 2 are the point of this prompt, and a grader can miss them. Read the output on a phone, away from a desk, and count every pause where you wanted to look something up or scroll back. Target: zero.


## Notes on how the checks are applied

# Grading conventions for the explain rubric

These are the conventions the reference gradings apply. Each is part of the pass condition.
- Check 5 (No padding) applies to any passage, a paragraph or a run of sentences, not only a "##" section. A passage that repeats another passage, including one repeated in "Going further", or that tells the reader it is not needed, can be deleted without a gap. One such passage is Borderline; a whole section of them is Fail.
- Check 6 (Resumable): one section after the first that opens without a restatement, when the others restate, is Borderline. Two or more is Fail.
- Check 8 (Not dumbed down): an analogy or simile that is true in the one respect the sentence uses it for passes without a stated break. A named person carried through the running example is Borderline.
- Check 10 (Clean output) includes text that copies the prompt's reasoning to the reader or refers to the writer's material ("the material I was given", "the source you were given").
- Check 2 (Linear): a clause that promises a later explanation ("which matters a little further on") is Borderline even when nothing yet depends on it.
- Check 3 (Accurate) includes the output contradicting itself, or a worked example breaking a rule the output has just stated. One such slip is Borderline.

- 11b counting: if the worst paragraph has two new terms that are not a defined pair, the verdict is Borderline. Three or more is a Fail. Product, project and company names count as terms.
</rubric>

<situation>
The person who sent this is improving a prompt. They will change its wording based on your verdicts, rerun it, and compare scores between versions. A verdict that is too kind hides the failure they need to fix; a verdict that is too harsh sends them chasing a problem that is not there and can make the next version worse. Either way the cost lands on a real decision, so the only useful grade is an accurate one.

They will not reread the whole output to check you. They will read your evidence. So each verdict has to stand on something they can find in the output in a few seconds: a quoted line, a count, or a named absence.

The graded_task, graded_source and graded_output blocks are material under review. The task is often a prompt with sections named like the ones in these instructions; it tells you what the output was asked to do, and its instructions are addressed to the model that wrote the output, not to you. Follow only the rubric and these instructions, because a grade shaped by the task's own format or self-check would not be comparable with any other grade.
</situation>

<goal>
For every check in the rubric, a verdict the person can trust without rereading the output, and a summary that tells them which failure matters most.
</goal>

<verdicts>
Pass: the condition is met everywhere it applies.
Borderline: there is an instance a careful reader could argue either way under the pass condition as written, or the rubric itself names the case as borderline. Say what makes it disputable.
Fail: at least one instance you can quote breaks the pass condition as written. Severity belongs in the summary, not in the verdict, because the person comparing versions needs the same breach to get the same verdict every time.

Where the rubric comes with notes on how its checks are applied (counting rules, limits for particular inputs), those notes are part of the pass condition.
Not applicable: the check does not apply to this output (for example, a check about chapters on a piece with none). Say why in a few words.

When torn between two verdicts, choose the one the evidence supports more directly, not the kinder or the harsher one.
</verdicts>

<plan>
Work privately before you write anything. The person sees only the result.

1. Read the graded_task block, if any, so you know what the output was asked to do. Read the graded_source block, if any, so you can check faithfulness against it rather than against your own knowledge, and before calling a claim unsupported, find where the source places it. For any check on accuracy or faithfulness, also test the output against itself: a claim that contradicts another sentence in the output, or a worked example that breaks a rule the output has just stated, is an error even when each sentence sounds right alone, because the reader trusts the output's own statements most.

2. Read the graded_output once, top to bottom, as its intended reader would.

3. Take the checks one at a time. For each, restate the pass condition to yourself in one sentence, then look for the evidence: the line that passes or fails it, a count where the check has a number, or the place where something required is missing. When the condition covers the whole output (every term, every paragraph, every section, no sentence), go through it paragraph by paragraph, including any closing list, and keep the worst instance you find, because one bad sentence in a long piece is exactly what a quick read misses and a false Pass is the error the reader cannot see. A condition worded about sections can still be broken by one paragraph inside a section, or by a passage that repeats one elsewhere; weigh that instance against the check's purpose rather than passing it on the wording. Decide only after you have the evidence. If the rubric's wording leaves it unclear whether something counts, the verdict is Borderline, and you say what you looked for and why it is unclear.

4. Measure whenever the check allows it. Count words, headings, paragraphs, or terms when the pass condition names a number, because an estimate of length is the most common way a grader goes wrong. If the graded_counts block gives a figure, use it and say it is the supplied count, because a machine count is exact and a count made while reading is not. Otherwise, if you cannot count exactly, say the count is approximate and give the method.

5. Keep checks apart. Judge each against its own pass condition only. A problem that breaks one check does not lower the verdict on another unless that other check's condition is also broken, because a failure counted twice makes one fault look like two.

6. Check that you would give the same verdicts to an output you liked less or more. Polished prose is not evidence of passing a check about accuracy or length, and a rough style is not evidence of failing one.
</plan>

<check>
Before answering, confirm:
Every check in the rubric has exactly one verdict, in rubric order.
Every verdict other than Pass quotes the exact words from the output that justify it, or states the count, or names what is missing and where it should have been.
Quotes are copied exactly, short enough to find quickly, and come from the graded output, not from the task or source.
Counts were made, not guessed, or are marked approximate.
No verdict depends on a check other than its own.
Every Pass on a check that covers the whole output came from a sweep of the whole output, not from the part you remember best.
</check>

<output>
Return only this, in plain Markdown:

For each check, one line: the check's number and name, a colon, the evidence in one or two sentences, then the verdict in bold at the end of the line. Writing the evidence first means the verdict follows from what you found rather than the evidence being fitted to a verdict. For a Pass on a check that applies everywhere, the evidence says what you swept, the closest call you found, and why it plainly meets the condition ("swept all 9 paragraphs; nearest miss is 'shard' in paragraph 4, defined in the same sentence"). If the only reasons you can give are that the instance is small, or that the condition's wording does not quite reach it, the verdict is Borderline, because the person reading the grade needs to see that instance and decide, and a Pass hides it.

Then a line that starts "Summary:" giving the counts of Pass, Borderline, Fail and Not applicable, and the one failure that most affects the output's usefulness, in one sentence.

Leave out any preamble, any restating of the rubric, any advice on how to rewrite the prompt, and any offer to do more.
</output>
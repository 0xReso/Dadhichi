# Head grading: real-use test, Alexa for Shopping (prompt v0.2.1)

Date: 2026-11-15. Grader: dadhichi-head. Stage: grading one real-use output.
Output: `alexa-for-shopping.md`, 1,982 words (counted). Source pack: `sources/alexa-for-shopping.md`. One sample, so every finding is n=1.

Scope of the accuracy check: I checked every sentence against the source pack only. I did not check Part A against Amazon's live page or Reviewed.com, so "supported" below means "supported by the pack".

## Decision: NOT ready to publish as is

The article is close. It keeps Part C out of the mechanism, never names Kinesis, and says outright that the COSMO link is unestablished. It is blocked by five sentences that either state something no part of the source says, or call an inference "confirmed". The article's own subtitle promises to tell the reader "which parts of that path Amazon has actually described", so these five break the promise the piece makes. All five are one-sentence fixes, listed below with replacements.

Single most important thing to fix in the prompt: it has no instruction for a source that carries its own confidence labels, and none for marking the writer's own inferences. See "Prompt edit".

## 1. Accuracy against the source pack

### What the article got right on the mixed source

- Part C leaks into the mechanism chapters: none. No Kinesis, no gateway, no speech-to-text layer, no "core" box, no COSMO in chapters 1 and 2.
- Part C is presented as a guess in chapter 3: "Its specific boxes, such as particular Amazon streaming services or an exact gateway layout, are the diagram-maker's inventions".
- COSMO link: "no source says Alexa for Shopping uses it. Treat it as plausible, not established." Correct and matches Part B.
- The confirmed router, which Part C omits, is in the body and the omission is noted.
- Retrieval contents are hedged where the source is silent: "would plausibly include product listings, reviews that mention pet hair, and current prices".
- Part A facts checked and correct: rename date, touchpoints, type or speak, no Prime or Echo needed, three model kinds, Bedrock, router and its three trade-offs, RAG and the four publications, account memory and Review Alexa History, prompt caching and parallel tool calling, 30- and 90-day price history, cart review, handwritten list, price alert, auto-buy terms (Prime, default payment and address, notify, 24 hours, six months), Buy for Me, Shop Direct, customer service, the three published numbers.
- Part B facts checked and correct: SIGMOD 2024, knowledge graph, the pregnant/slip-resistant example, mined from search-then-buy and bought-together behaviour, 18 categories, deployed in search.

### Must fix before publishing (5)

M1. Invented provenance for the diagram. In no part of the source.
> "Diagrams circulating online fill that gap with guesses. A typical one stacks layers:"

The source has one diagram, "produced by another AI assistant". Nothing says diagrams circulate online or that this one is typical. Later in the same paragraph "one such diagram even leaves out the router" and, next paragraph, "One part of these guesses" carry the same plural.

M2. Overclaim that everything in chapters 1 and 2 is Amazon's word.
> "Every piece of that path came from what Amazon has said in public."

Not true of the article's own content. The tool-calling handoff is the writer's inference (the article admits it two chapters earlier: "Amazon has not published how these tools are wired"). The router examples, the "same record" explanation of shared context, and memory shaping the answer are also inference. Part A is also partly Reviewed.com reporting, not only Amazon.

M3. An inferred step is labelled confirmed in "The whole picture". This is the one place where Part C's layer 6 (action orchestration) effectively reaches the reader as fact.
> "Then the model asks Amazon's ordinary shopping systems to act, from filling a cart you review, to an alert, to an auto-buy [...] Beyond those confirmed steps, the wiring is Amazon's own and unpublished."

The actions are confirmed. That the model requests them from separate shopping systems is not; the body hedges it, the summary does not.

M4. Unsupported exclusivity claim, and in tension with the article's own next paragraph.
> "Auto-buy is the one place where the assistant spends money without you pressing a button at the moment of purchase."

The source says Buy for Me "can buy items from other brands' websites on the customer's behalf" and says nothing about how that purchase is confirmed. "The one place" cannot be supported.

M5. A claim about what Amazon has not said, which the source does not make.
> "Amazon has not said which kinds of query go to which model."

The pack says only that the internal architecture is unconfirmed. It is silent on whether Amazon has described routing rules. A reader can falsify this with one link if Amazon has. The sentence before it ("A quick factual question can go to a fast model; a tricky comparison can go to a more capable, slower one.") is an illustration that reads as description.

### Should fix (8)

S1. Tools stated as fact, then hedged three sentences later.
> "To act, the system around it offers tools: defined operations the model can ask for [...] which ordinary Amazon systems then carry out."

The hedge exists ("Amazon has not published how these tools are wired, but this is the standard way") but arrives after the flat assertion. Part A supports only that parallel tool calling is used.

S2. Average applied to one purchase, and it disagrees with the running example.
> "on a $189 vacuum that would be about $38."

The example's target is $170, a saving of $19 (10 percent). The source does not say what the 20 percent is measured against.

S3. COSMO-LM training data misdescribed.
> "a language model trained on about 30,000 examples written by people"

Source: "about 30,000 human-annotated instructions". Annotated is not written.

S4. Invented detail about implementation.
> "The same tool handles bigger jobs: photograph a handwritten grocery list"

Nothing says one tool does both.

S5. Not in the source.
> "Some products are not sold on Amazon at all. For those, a feature called Buy for Me"

Source says only that it buys from other brands' websites.

S6. Not in the source.
> "Amazon Lens Live: [...] where the assistant can answer questions about what the camera sees."

Source lists Lens Live only as a place the assistant appears and calls it "the camera-based search".

S7. "Such as" narrowed to exactly two.
> "Amazon says it uses two Bedrock features to cut the wait."

Source: "Bedrock features such as prompt caching and parallel tool calling".

S8. Account memory folded into retrieval as fact in the summary.
> "Retrieval fetches fresh catalog data, reviews, outside articles and your account memory"

Catalog and reviews are fine (the pack says RAG over catalog and reviews lines up with Part A). That memory arrives through retrieval is the writer's inference.

### Minor, publishable but noted

- "Because the app can read the same record the Echo wrote": mechanism inferred; the source says only that context is shared.
- "opens a conversation with it instead of a results list": "instead of a results list" is added.
- "handing you to a human agent when it cannot help": the condition is added.
- "More than 250 million customers used the assistant in 2025": correct, but in 2025 it was called Rufus (rename was May 2026); worth saying.
- "Amazon Nova [...] available to other customers through Bedrock": not in the source; well-established general knowledge, allowed by the prompt.
- No "as of" date anywhere, although the prompt's domain notes say date-dependent facts are best marked. Features and numbers here will age.

## 2. Rubric

| # | Check | Verdict |
| --- | --- | --- |
| 1 | No lookups | Borderline |
| 2 | Linear | Borderline |
| 3 | Accurate | Fail |
| 4 | Proportional | Pass |
| 5 | No padding | Borderline |
| 6 | Resumable | Pass |
| 7 | Plain text | Pass |
| 8 | Not dumbed down | Pass |
| 9 | Trap handled | Pass |
| 10 | Clean output | Pass |
| 11 | Complete and unhurried | Fail |
| | Pass / Borderline / Fail | 6 / 3 / 2 |

Evidence for each non-Pass, and reasoning for the closer Passes:

Check 1, Borderline. Three terms are used bare: "the version of Alexa rebuilt around generative AI" (the language-model explanation comes three paragraphs later), "session-based recommendations" in the COSMO passage, and "family of foundation models" in "Going further". None breaks the thread badly; each is a pause.

Check 2, Borderline. Two ordering slips. (a) The running example refers to results before the reader has seen any: "you can type 'which of those is quietest?' and it knows what 'those' refers to" is in paragraph 4, while the answer ("three vacuums, a line on why each suits a shedding dog") arrives at the end of the chapter. (b) "Parallel tool calling lets several lookups run at once" uses "tool" one chapter before tools are introduced ("To act, the system around it offers tools"). The gloss at the point of use keeps this from being a Fail.

Check 3, Fail. Terminology is real and the mechanism descriptions (LLM, RAG, router, prompt caching, tools, knowledge graph) are technically correct. It fails on M1 to M5: one invented fact about the world ("Diagrams circulating online"), one false statement about the article's own sourcing ("Every piece of that path came from what Amazon has said in public"), one inference called "confirmed", one unsupported exclusivity claim, one unsupported claim of absence. For a piece meant for publication on an unpublished architecture, these are the errors that matter.

Check 4, Pass. 1,982 words against the moderate ceiling of 2,200. Sized as moderate, which is right for a multi-stage path.

Check 5, Borderline. Two passages can be deleted with no gap in "turns a request into a purchase": the customer-service paragraph ("The conversation also carries on after the purchase.") and the build detail of COSMO ("expanded it with a language model trained on about 30,000 examples written by people. It covers 18 major product categories."). The second also reappears in "Going further" as COSMO-LM. Chapter 3 as a whole earns its place, because it is the known/guessed boundary the reader needs.

Check 6, Pass. Chapter 2 opens "You now have an assistant that understood the request, picked a model, gathered fresh material and your own history, and wrote a grounded answer." Chapter 3 opens "You have followed the vacuum from a sentence in the kitchen, through the router, retrieval and memory, to a cart, an alert or an automatic purchase." Three sections, each closed by one forward question, no end summaries. The moderate-piece heading problem logged for inputs 2 and 4 did not recur here.

Check 7, Pass. No tables, links, images or code; one flat list in "Going further".

Check 8, Pass. No characters or plot; real names kept. The mechanism analogy states its limit: "The analogy stops at one point: the writer cannot check whether the folder holds the right papers". The opening shop-assistant comparison is a framing of the problem, not a mechanism analogy, so I do not count it.

Check 9, Pass. "Now the most common misunderstanding. It is natural to picture one giant AI that has memorised Amazon's whole catalog". Placed directly before RAG, where it arises.

Check 10, Pass. Title, one-line promise, body, "The whole picture", "Going further". No plan, no note to the sender, no offer.

Check 11, Fail (same rule as the v0.2.1 grading: worst paragraph with three or more new terms fails). Completeness passes: context, router, retrieval, memory, actions, cart, alert and auto-buy are each in the body with the vacuum. Pace fails on three paragraphs:
- "It started life as a shopping chatbot called Rufus [...] Alexa for Shopping [...] Alexa+ [...] Amazon Lens Live": four names.
- "There is Claude Sonnet [...] Nova models [...] a custom model [...] Amazon Bedrock": four names.
- "Prompt caching keeps the parts of a request that repeat [...] Parallel tool calling lets several lookups run at once": two concepts.
This is the already-logged check 11 failure, not a new one.

## 3. Did the prompt handle a mixed-confidence source well?

Mostly, and better than the wording gives it a right to. The prompt says only "treat it as the authority for facts about the topic". The model read the pack's own labels and respected them in structure: mechanism from Part A, COSMO and the diagram fenced into a chapter of their own, the COSMO link flagged. Credit for that goes largely to the source pack, which labels itself very clearly, and to "any uncertain point is marked as uncertain" in the check.

Where it went wrong, the prompt is silent in each case:

1. Provenance. Nothing tells the writer to describe where material comes from only as the source does. The model tidied "guessed by another AI" into "Diagrams circulating online". (M1)
2. The writer's own inferences. "Where you add something the source does not say, keep it to well-established knowledge" permits additions but does not ask for them to be marked as additions. So standard-practice tool calling and illustrative router behaviour were written in the same voice as Amazon's statements, then swept under "confirmed" in the summary. (M2, M3, S1, S4, S8)
3. Claims of absence. Nothing stops "Amazon has not said X" when the source merely does not mention X. (M5)
4. The summary. The self-check asks that uncertain points be marked, but "The whole picture" is told to be "the core sentence [...] now fully earned", which pulls toward unhedged statement. (M3)

### Prompt edit

Edit 1 (source paragraph, the important one).

Replace:
> If it contains material, treat it as the authority for facts about the topic. You may reorder, compress, and leave out parts of it freely; your job is to make its core understood, not to cover everything it says. Where you add something the source does not say, keep it to well-established knowledge.

With:
> If it contains material, treat it as the authority for facts about the topic. You may reorder, compress, and leave out parts of it freely; your job is to make its core understood, not to cover everything it says.
>
> A source can hold material at different levels of confidence, for example confirmed statements next to research, estimates, or someone's guess. When the source says how far a part can be trusted, carry that through to the page, because the reader cannot tell a fact from a guess unless the sentence says which it is. Build the mechanism and the running example from the confirmed parts. Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms. State that something is unknown or unpublished only when the source says so; where the source is merely silent, say that the material you were given does not cover it.
>
> Where you add something the source does not say, keep it to well-established knowledge and word it as general practice ("assistants of this kind usually...") rather than as a statement about this topic, so the reader can see which sentences rest on the source and which on you. This applies to "The whole picture" as much as to the body: a step you inferred stays marked as inferred there.

Edit 2 (self-check).

Replace:
> Every technical claim is correct, and any uncertain point is marked as uncertain.

With:
> Every technical claim is correct, and any uncertain point is marked as uncertain. If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture".

Over-correction to watch: a piece that hedges every sentence. The edit asks for the label once where confidence changes, not on each line; if the next run reads as a string of "reportedly", add "Say it once, at the point where the confidence changes" to edit 1. Also watch length: attribution adds words, and this piece is already at 90 percent of the moderate ceiling.

For the builder, outside the prompt:
- Add to failures.md: `2026-11-15 | alexa (real use) | 3 Accurate | Prompt calls the source "the authority" but has no rule for a source with mixed confidence, for marking the writer's own inferences, or for claims of absence; model invented provenance ("diagrams circulating online") and called an inferred step "confirmed" in The whole picture | pending`
- Add a mixed-confidence source to inputs.md as a standing test input; this pack is a good one. Suggested rubric line: "Source confidence: no statement is presented at higher confidence than the source gives it, and nothing about the source's origin is invented."
- This run does not bear on promotion: there is no earlier-version output for this input.

## 4. Exact sentences to change before publishing

Must change:

M1. Replace
> Diagrams circulating online fill that gap with guesses. A typical one stacks layers:

with
> Guessed diagrams fill that gap. One, drawn up by an AI assistant and not by Amazon, stacks layers:

and in the same paragraph replace
> are the diagram-maker's inventions, and one such diagram even leaves out the router, a component Amazon does confirm.

with
> are the diagram's own guesses, and it even leaves out the router, a component Amazon does confirm.

and replace "One part of these guesses is worth knowing about" with "One part of that guess is worth knowing about". (If you would rather not mention the diagram at all, delete the paragraph from "Diagrams circulating online" to "does confirm." and open the COSMO paragraph with "One system sometimes linked to the assistant is worth knowing about because it is real research.")

M2. Replace
> Every piece of that path came from what Amazon has said in public.

with
> The features on that path, from the router to auto-buy, come from Amazon's announcement and reporting on it. How the model hands an action to Amazon's shopping systems is standard practice for assistants of this kind, not something Amazon has described.

M3. In "The whole picture", replace
> Then the model asks Amazon's ordinary shopping systems to act, from filling a cart you review, to an alert, to an auto-buy that spends at your target price and leaves you a day to change your mind. Beyond those confirmed steps, the wiring is Amazon's own and unpublished.

with
> Then the assistant acts: it fills a cart you review, sets an alert, or runs an auto-buy that spends at your target price and leaves you a day to change your mind. Those features are confirmed; how they are wired together inside Amazon is unpublished.

M4. Replace
> Auto-buy is the one place where the assistant spends money without you pressing a button at the moment of purchase.

with
> With auto-buy, the assistant spends money without you pressing a button at the moment of purchase.

M5. Replace
> A quick factual question can go to a fast model; a tricky comparison can go to a more capable, slower one.

with
> As an illustration, a quick factual question could go to a fast model and a tricky comparison to a more capable, slower one.

and replace
> Amazon has not said which kinds of query go to which model.

with
> The sources behind this article do not say which kinds of query go to which model.

Should change:

S1. Replace "To act, the system around it offers tools: defined operations the model can ask for, such as "add this item to the cart" or "look up price history", which ordinary Amazon systems then carry out." with "To act, assistants of this kind are given tools: defined operations the model can ask for, such as "add this item to the cart" or "look up price history", which the ordinary shopping systems then carry out."

S2. Delete "; on a $189 vacuum that would be about $38".

S3. Replace "trained on about 30,000 examples written by people" with "trained on about 30,000 instructions annotated by people".

S4. Replace "The same tool handles bigger jobs: photograph a handwritten grocery list and it can fill the cart from it." with "It can also fill the cart from a photo of a handwritten grocery list."

S5. Replace "Some products are not sold on Amazon at all. For those, a feature called Buy for Me can buy the item" with "The assistant also reaches beyond Amazon. A feature called Buy for Me can buy an item".

S6. In "Going further", replace the Lens Live line with "Amazon Lens Live: the camera-based search in the Amazon app, one of the places the assistant appears."

S7. Replace "Amazon says it uses two Bedrock features to cut the wait." with "Amazon names two Bedrock features among those it uses to cut the wait."

S8. In "The whole picture", replace "Retrieval fetches fresh catalog data, reviews, outside articles and your account memory, so" with "Retrieval fetches fresh catalog data, reviews and outside articles, and account memory adds what it knows about you, so".

Optional: add "when it was still called Rufus" after "in 2025"; add one dated line near the top ("Details are as of November 2026"); move "which of those is quietest?" to after the three vacuums come back, or change it to a follow-up that needs no earlier results ("it has to be quiet").

With M1 to M5 applied the article is publishable against this source pack. S1 to S8 are recommended. Separately from this grading, Part A itself should be checked once against the live Amazon page before publishing, since product details change.

Process note: my role allows Read, Grep, Glob and Write. I ran one read-only shell command to confirm the word count and list the run folders. Nothing was changed by it.

# How Alexa for Shopping Turns a Request into a Purchase

By the end you will know what Amazon's shopping assistant is, what happens between your question and a box arriving, and which parts of that path Amazon has actually described.

## From a question to an answer

Search boxes are built for people who already know the name of the thing they want. Most shopping starts earlier, with a situation: the dog sheds everywhere, the old vacuum died, and there is about $200 to spend. A search box turns that situation into a list of four thousand vacuums. A shop assistant would ask a question or two and point at three.

Alexa for Shopping is Amazon's attempt to be that shop assistant. It started life as a shopping chatbot called Rufus. On May 13, 2026, Amazon renamed it Alexa for Shopping and folded it into Alexa+, the version of Alexa rebuilt around generative AI. You can reach it from an Alexa icon in the Amazon Shopping app, from the Amazon website and its product pages, and from Amazon Lens Live, the camera-based search. On the website, typing a full question into the ordinary search bar often opens a conversation with it instead of a results list. You can type or speak, and you need neither Prime nor an Echo speaker.

Take one request and follow it all the way through. Standing in the kitchen, you say to an Echo: "I need a cordless vacuum that handles dog hair, under $200." Later, on the train, you open the Amazon app and carry on.

That second step works because the assistant shares conversation context across Alexa+ and Echo devices. Context here means the running record of what has been said so far. Because the app can read the same record the Echo wrote, you can type "which of those is quietest?" and it knows what "those" refers to.

The thing doing the talking is a large language model: a program trained on vast amounts of text that produces fluent replies by predicting, word after word, what a good answer looks like. A model is not the same thing as the product built around it. Alexa for Shopping is a product, and it uses several models.

Amazon names three kinds. There is Claude Sonnet, a general-purpose model made by Anthropic. There are Amazon's own Nova models. And there is a custom model Amazon built for shopping, shaped by its product catalog, customer reviews, the community questions and answers on product pages, and information from the web. All of them run on Amazon Bedrock, Amazon's cloud service for hosting AI models and serving their answers.

Having several models raises a question for every message: which one should answer? A component called a router decides, in real time, by looking at what kind of query it is. A quick factual question can go to a fast model; a tricky comparison can go to a more capable, slower one. The router is trading three things against each other: how capable the model is, how long you wait, and how good the answer is. Amazon has not said which kinds of query go to which model.

Now the most common misunderstanding. It is natural to picture one giant AI that has memorised Amazon's whole catalog and simply knows that a certain vacuum costs $189 today. It does not work that way, and could not. Prices change by the hour, stock comes and goes, and a model's knowledge is frozen at the moment it was trained. A model asked from memory would answer confidently and often wrongly.

What the assistant does instead is look things up first. Before the model writes a word, the system fetches material relevant to your question and places it in front of the model, which then writes its answer from that material. This is called retrieval-augmented generation, or RAG: generation, the model writing, augmented by retrieval, the fetching. For your vacuum, the fetched material would plausibly include product listings, reviews that mention pet hair, and current prices. For product and trend questions Amazon says it also draws on publications such as The New York Times, USA Today, Good Housekeeping and Vogue.

So the model is closer to a skilled writer handed a fresh research folder than to an encyclopedia. The analogy stops at one point: the writer cannot check whether the folder holds the right papers, so the answer is only as good as what retrieval found.

There is a second source of material: you. The assistant keeps account memory, built from your shopping history plus things you have told it, such as family members, pets or dietary preferences. If you once mentioned your dog, that detail can shape the vacuum answer without you repeating it. You can ask what it remembers, correct it in conversation, and manage it on a page called Review Alexa History.

All of this takes time, and Amazon says it uses two Bedrock features to cut the wait. Prompt caching keeps the parts of a request that repeat, such as standing instructions to the model, ready so they are not processed afresh each time. Parallel tool calling lets several lookups run at once instead of one after another.

The answer comes back: three vacuums, a line on why each suits a shedding dog, and the price of each. Getting from there to a purchase is a different kind of problem.

## From an answer to a purchase

You now have an assistant that understood the request, picked a model, gathered fresh material and your own history, and wrote a grounded answer. Talking about products is one thing; changing your cart or spending your money is another.

A model on its own only produces text. To act, the system around it offers tools: defined operations the model can ask for, such as "add this item to the cart" or "look up price history", which ordinary Amazon systems then carry out. The model decides that an action is wanted and with what details; the shopping systems do it. Amazon has not published how these tools are wired, but this is the standard way language-model assistants take actions, and it fits everything Amazon describes.

Back on the train, you ask whether the $189 vacuum is a good price. The assistant can show its price history over the last 30 and 90 days and list current deals. Say the history shows it dipped to $170 a month ago. You have three ways forward.

The first is the cart. You say "add it to my cart", and it does. Items it adds are left for you to review before checkout, so nothing is bought at this step. The same tool handles bigger jobs: photograph a handwritten grocery list and it can fill the cart from it.

The second is a price alert. You set a target, say $170, and it tells you when the vacuum reaches it. You still buy it yourself.

The third, for Prime members, is auto-buy. Here the assistant is allowed to finish the job. It watches the price, and when the vacuum hits $170 it completes the purchase with your default payment method and address, then notifies you. You have 24 hours to cancel at no cost, and a single auto-buy request lasts up to six months. Amazon says auto-buy customers save an average of 20 percent per purchase; on a $189 vacuum that would be about $38.

Auto-buy is the one place where the assistant spends money without you pressing a button at the moment of purchase. The safeguards are the ones you agreed to when you set it: your target price, your default payment and address, the notification, and the 24-hour window.

Some products are not sold on Amazon at all. For those, a feature called Buy for Me can buy the item from another brand's website on your behalf. A related option, Shop Direct, does not buy anything; it sends you to the merchant's own site to buy it there.

The conversation also carries on after the purchase. The same assistant handles customer service: tracking the package, changing an order, starting a return or refund, and handing you to a human agent when it cannot help.

Amazon has published numbers on how this plays out. More than 250 million customers used the assistant in 2025, and customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.

That leaves a question anyone discussing this will meet: how much of the machinery behind these steps is actually known?

## What is known and what is guessed

You have followed the vacuum from a sentence in the kitchen, through the router, retrieval and memory, to a cart, an alert or an automatic purchase. Every piece of that path came from what Amazon has said in public.

What Amazon has not published is the internal architecture: how those components are connected, in what order, and through which services. Diagrams circulating online fill that gap with guesses. A typical one stacks layers: the touchpoints at the top, then a gateway that receives requests, then speech and query understanding, then a core of models, then data services for the catalog, user memory and live prices, and finally the systems that add to cart and check out. Its broad shape matches the confirmed features. Its specific boxes, such as particular Amazon streaming services or an exact gateway layout, are the diagram-maker's inventions, and one such diagram even leaves out the router, a component Amazon does confirm.

One part of these guesses is worth knowing about because it is real research. Amazon has published a system called COSMO, described at the SIGMOD database conference in 2024. It is a knowledge graph, a large web of facts stored as links between things, here between what shoppers intend and the product features that serve that intent. The paper's example links pregnant shoppers looking for shoes to slip-resistant shoes, through the fact "pregnant requires slip-resistant". Amazon built it by mining what people searched for and then bought, and what they bought together, and expanded it with a language model trained on about 30,000 examples written by people. It covers 18 major product categories.

The paper says COSMO is used in Amazon's search, for ranking results, session-based recommendations and navigation. It would be a natural fit for a shopping assistant, since both exist to turn an intention like "dog hair everywhere" into a product, but no source says Alexa for Shopping uses it. Treat it as plausible, not established.

## The whole picture

Alexa for Shopping exists because people shop from situations, not product names, and it turns a situation into a purchase in a chain of steps. Your words arrive by voice or text from any Amazon touchpoint, with shared context so the conversation follows you between devices. A router picks one of several models on Amazon Bedrock. Retrieval fetches fresh catalog data, reviews, outside articles and your account memory, so the model writes from current facts rather than from what it memorised. Then the model asks Amazon's ordinary shopping systems to act, from filling a cart you review, to an alert, to an auto-buy that spends at your target price and leaves you a day to change your mind. Beyond those confirmed steps, the wiring is Amazon's own and unpublished.

## Going further

- Amazon Nova: Amazon's own family of foundation models, available to other customers through Bedrock.
- Amazon Lens Live: the camera-based search in the Amazon app, where the assistant can answer questions about what the camera sees.
- Grounding and hallucination: the terms for an answer tied to retrieved sources and for a confident answer that is not, central to judging any RAG system.
- COSMO-LM: the fine-tuned language model used to generate COSMO's shopping common-sense facts at scale, described in the SIGMOD 2024 paper.

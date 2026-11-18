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

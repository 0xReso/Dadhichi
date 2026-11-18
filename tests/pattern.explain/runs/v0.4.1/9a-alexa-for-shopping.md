# Alexa for Shopping

By the end you will understand what Amazon's shopping assistant is, how it turns a question into a grounded answer or a purchase, and which parts of its design are confirmed and which are guesses.

## A store you can talk to

A search box in an online shop is good at one thing: matching the words you type against product listings. It is poor at questions such as "which coffee grinder will work with the espresso machine I bought last year, and is it cheaper than usual right now?" A question like that needs someone who knows your order history, can read the product details and reviews, and can check prices over time. Shops have traditionally left all of that work to the customer.

Alexa for Shopping is Amazon's answer to that gap: an AI assistant built into Amazon's store that you can ask questions in ordinary language and that can also act for you. Amazon first launched it as a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping.

At the same time it was folded into Alexa+, which is Amazon's generative-AI version of its Alexa voice assistant. Generative AI here means software that composes new replies rather than picking from a fixed script. Because the shopping assistant shares conversation context with Alexa+ and with Echo devices, a conversation you start by talking to an Echo speaker in the kitchen can carry on later in the shopping app.

You reach it through the Amazon Shopping app, where it has an Alexa icon in the navigation bar, or on the Amazon website, including the homepage and product pages. On the website, typing a full question into the ordinary search bar often opens a conversation with it instead of a plain list of results. You can type or speak. You do not need a Prime membership or an Echo device to use it. Amazon says more than 250 million customers used it in 2025.

Take the grinder question as the example for the rest of this piece. You type it into the search bar on a product page. What happens between your question and the reply?

## How a question becomes an answer

You now have the problem, a shopping question too rich for a keyword search, and the product Amazon built for it. The next step is what does the thinking.

The thinking is done by language models. A language model is a program trained on enormous amounts of text that produces a reply by predicting, one piece at a time, what should come next. It is the engine; Alexa for Shopping is the product built around it, and the two are easy to confuse.

The models run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models live and where the assistant sends work to them.

Alexa for Shopping does not rely on one model. It draws on several, and three are named.

The first is Claude Sonnet, a model made by the AI company Anthropic.

The second is Nova, a family of models Amazon makes itself.

The third is a custom model Amazon built specifically for shopping. It uses Amazon's product catalog, customer reviews, the community questions and answers on product pages, and information from the web.

Something has to decide which of these handles your grinder question. That job belongs to a component Amazon calls a real-time router. For each query, the router looks at what kind of question it is and picks a model, balancing three things: how capable the model is, how fast it responds, and how good the answer will be. A quick "where is my parcel?" and a detailed comparison of two grinders need not go to the same model.

This is the point where people most often go wrong. It is tempting to say "Alexa for Shopping is Claude" or "it is Amazon's own model". Both are wrong in the same way: the product sits on top of several models, and the router chooses among them question by question. Asking which model is behind it has no single answer.

A model on its own also has a weakness. It knows only what was in its training text, which may be out of date and contains nothing about your past orders or today's price. To fix that, the assistant fetches relevant material before the model writes its answer and hands it to the model alongside your question. The model then answers from that material rather than from memory alone. This technique is called retrieval-augmented generation, usually shortened to RAG.

For the grinder, the fetched material would be the kind Amazon says it uses: listings from the product catalog, customer reviews, community answers, and, for product and trend questions, articles from publications Amazon names, such as The New York Times, USA Today, Good Housekeeping and Vogue.

That covers the answer. But the grinder question also asked about your machine and about price, which needs more than reading.

## Remembering you and acting for you

So far you hold the reading side: a router picks a model on Bedrock, and RAG feeds that model fresh material. The rest of the grinder question depends on what the assistant knows about you and what it can do.

What it knows about you is called account memory. It is built from your shopping activity, plus details you tell it, such as family members, pets or dietary preferences. You can ask what it remembers and correct it in the conversation, and you can manage that history on a page called Review Alexa History.

Account memory is what lets it answer the first half of the grinder question. Among the things Amazon says it can do is check compatibility against your past orders, so it can look at the espresso machine you bought last year and tell you which grinders suit it. It can also answer product questions and compare products, for example two grinders side by side.

For the second half, it can show a product's price history over the last 30 and 90 days, and list current deals. Say the grinder you like costs 129 dollars today and the history shows it has dipped to 99 dollars before. You now know today's price is not a bargain.

You can then ask for a price alert, which tells you when the grinder reaches a target price you set, here 99 dollars.

Prime members can go one step further with auto-buy. Instead of alerting you, the assistant watches the price and, when it reaches your target, completes the purchase itself using your default payment method and address, then notifies you. You have 24 hours to cancel at no cost, and a single auto-buy request lasts up to six months. Amazon says auto-buy customers save an average of 20 percent per purchase; on a 129-dollar grinder that would be about 26 dollars.

It can also add items to your cart, including from a photo of a handwritten grocery list. Items it adds sit in the cart for you to review before checkout, which is different from auto-buy, where the purchase goes through and the 24-hour window is your safety net.

Beyond shopping, it handles customer service tasks: tracking packages, returns, refunds, changes to orders, and handing you over to a human agent.

Amazon also publishes a figure for the effect on buying: customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.

All of this describes what the assistant does. How its parts are connected inside is a separate question, and much less is known about it.

## What is known about the inside

You now hold the confirmed picture: several models chosen by a router, answers grounded by RAG, account memory, and actions from price alerts to auto-buy. From here the confidence changes. Amazon has not published its internal architecture; no Amazon document describes how these components are wired together.

There is related research. Amazon has published a paper, presented at the SIGMOD database conference in 2024, on a system called COSMO. COSMO is a knowledge graph, a large web of facts stored as links between things, here linking what shoppers intend to the products that serve that intent. The paper's example: a search for shoes by pregnant shoppers is connected to slip-resistant shoes through the link "pregnant requires slip-resistant". The paper says COSMO is deployed in Amazon search. None of the sources behind this article says Alexa for Shopping uses it. It is plausible, since both serve shopping intent, but it is not confirmed.

You may also meet architecture diagrams of the assistant. The one described in the material behind this article is a guess produced by another AI assistant, not Amazon's design. It stacks layers from the app and website at the top down to cart and checkout actions at the bottom, and in broad strokes it matches the confirmed features: Bedrock models, RAG over the catalog and reviews, user memory, real-time prices, and the cart and Buy for Me actions. Its specific boxes and services are its own guesses, it places COSMO at the centre, which no source confirms, and it leaves out the one component Amazon has described: the model router. Treat any such diagram as a sketch of how assistants of this kind are usually built, not as a description of this one.

## The whole picture

Alexa for Shopping, formerly Rufus and now part of Alexa+, exists because shopping questions need knowledge of products, prices and the shopper all at once. The confirmed parts are these: it runs on Amazon Bedrock; a real-time router sends each question to one of several models, among them Claude Sonnet, Amazon's Nova models and a custom shopping model; it uses RAG to ground answers in catalog data, reviews and named publications; it keeps an account memory; and it can show price history, set alerts, add to the cart and, for Prime members, auto-buy at a target price. The order in which these run for a single question, for example memory being looked up before the router picks a model, is my reading of how such systems usually work; Amazon has not published how the parts connect.

## Going further

- Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to make the assistant respond faster.
- Buy for Me and Shop Direct: Buy for Me purchases items from other brands' websites on your behalf, while Shop Direct sends you to the merchant's own site.
- Amazon Lens Live: Amazon's camera-based search, another place the assistant appears.
- COSMO-LM: the fine-tuned language model that generates the COSMO knowledge graph, trained on about 30,000 human-annotated instructions across 18 major product categories.

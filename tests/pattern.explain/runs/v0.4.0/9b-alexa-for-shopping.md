# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it turns a question into an answer or a purchase, and which parts of its design are confirmed and which are only guessed.

## From a search box to a conversation

A search box is good at one kind of question: show me things that match these words. Shopping questions are often of another kind. Will this filter fit the fridge I bought last year? Is this price low, or was it cheaper last month? Answering them means reading product details, reviews and your own order history, then putting the pieces together. A page of search results leaves that work to you.

Alexa for Shopping is Amazon's assistant for doing that work in conversation. You type or speak a question and it answers in plain sentences. It can also act on what you say: put things in your cart, watch a price, or buy something for you. Amazon says more than 250 million customers used it in 2025, and that customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.

It began under another name. Amazon launched a shopping chatbot called Rufus, and on May 13, 2026, Rufus was renamed Alexa for Shopping.

At the same time it was folded into Alexa+, Amazon's generative-AI version of its Alexa voice assistant. Because of that, it shares conversation context with Alexa+ and with Echo speakers, so a conversation started on an Echo can carry on in the shopping app.

You reach it in the Amazon Shopping app through an Alexa icon in the navigation bar, and on the Amazon website, including the homepage and product pages. On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it. You do not need a Prime membership or an Echo to use it.

Take one case through the rest of this piece. Your fridge, bought on Amazon a year ago, is due a new water filter. Standing in the kitchen, you ask your Echo which filter fits. Later, on the bus, you open the shopping app and pick up the same conversation.

Behind that one conversation sits a plain question: what is actually doing the answering?

## Several models behind one assistant

So far you hold a shopping assistant you can talk to on an Echo, in the app or on the website, carrying one conversation across all three.

The answering is done by language models: AI systems trained on large amounts of text that read a request and write a reply. Alexa for Shopping does not rely on one of them. It draws on several.

All of them run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models live and where requests to them are sent.

The first is Claude Sonnet, a general-purpose model made by Anthropic.

The second is Nova, a family of models Amazon makes itself.

The third is a custom model Amazon built for shopping. It uses Amazon's product catalog, customer reviews, community questions and answers, and information from the web.

With three models available, something has to choose between them. That job belongs to a router: a component that looks at each incoming query and, in real time, picks which model handles it, by the type of query. Amazon says the choice balances three things: capability, response time, and answer quality. Assistants of this kind usually route because the most capable model is often the slowest and costliest, and many questions do not need it.

This is where a common picture goes wrong. It is natural to imagine Alexa for Shopping as one AI that "knows Amazon". It is a product built on several models, with a router deciding which one answers each time. The name belongs to the product, not to any single model. Which model handles which kind of question is not covered by the sources behind this article, so for your filter question there is no way to say which one replied.

A model, however capable, learned what it knows at some earlier point. So how does it know today's price, or which fridge you own?

## Fetching before answering

You now hold a router that hands each question to one of several models running on Bedrock.

Before a model answers, Alexa for Shopping fetches material relevant to the question and hands it to the model along with the question, so the answer rests on that material rather than on the model's memory alone. This technique is called retrieval-augmented generation, usually shortened to RAG. In general practice, RAG is used because a model's training goes stale and because an answer grounded in fetched text is less likely to be made up.

What gets fetched depends on the question. For products, it includes the catalog, reviews, and questions and answers from other customers. For product and trend questions, Amazon also names outside publications as sources, The New York Times among them.

Your own history is part of the picture too. Alexa for Shopping can check compatibility against your past orders. For the filter, that means it can look at the fridge you bought and tell you which filters fit it, instead of asking you for a model number.

It also keeps what Amazon calls account memory: a store of what it has learned about you, built from your shopping activity plus details you tell it, such as family members, pets or dietary preferences. You can ask it what it remembers and correct it in the conversation.

Fetched material covers prices as well. Alexa for Shopping can show a product's price history over the last 30 and 90 days, and list current deals. Suppose the filter that fits costs $49 today, and the 90-day history shows it dipped to $39 a few weeks ago. Now you know the current price is not the best one available.

Up to here it has only talked. What happens when you ask it to do something?

## From answers to actions

You now hold the answering side: a router picks a model, and the model answers from fetched material, including your past orders and account memory.

The plainest action is adding items to your cart. It can do this from a conversation, and even from a photo of a handwritten grocery list. Items in the cart are reviewed by you before checkout, so nothing leaves the cart without your say.

One step further is a price alert. You name a target price, and it tells you when the product reaches it.

Further still is auto-buy, available to Prime members. You set a target price, it watches the price, and when the price reaches your target it completes the purchase with your default payment method and address, then tells you. You have 24 hours to cancel at no cost, and a request lasts up to six months. For the filter, you might set auto-buy at $40. If the price falls to $39 three weeks later, the order goes through and you get a notification. Amazon says auto-buy customers save an average of 20 percent per purchase.

Notice the difference from the cart. Items in the cart wait for you to check out; auto-buy does not wait. Your approval is given once, when you set the target, and your safety net afterwards is the 24-hour cancellation window.

Another action, called Buy for Me, reaches beyond Amazon. Alexa for Shopping can buy items from other brands' websites on your behalf.

The last group is customer service. It can track packages, start returns and refunds, change orders, and hand you over to a human agent when the conversation needs one.

That covers what it does. How those parts are connected inside is a separate question, and the answer is far less certain.

## What is confirmed and what is guessed

You now hold the whole working picture: several models behind a router, answers grounded in fetched material, and actions from the cart up to auto-buy.

Everything so far is confirmed by Amazon or by reporting on Amazon's announcements. The internal architecture is not. No Amazon document describes how the components are wired together.

From here the ground is less firm. Amazon has published research on a system called COSMO, presented in 2024. COSMO is a knowledge graph, a network of things joined by named relations, and this one holds shopping common sense: links between what people intend and which products serve that intent. The paper's example connects pregnant shoppers looking for shoes to slip-resistant shoes, through the relation "pregnant requires slip-resistant". The paper says COSMO is deployed in Amazon search. That Alexa for Shopping uses COSMO is not confirmed. It is plausible, since both serve shopping intent, but no source says so.

The sources behind this article also include an architecture diagram produced by another AI assistant. It is not Amazon's design. Some of its layers match the confirmed facts: the places you talk to the assistant, the Bedrock models, retrieval over catalog and reviews, user memory, real-time prices for alerts and auto-buy, and the cart and Buy for Me actions. The rest is the diagram's own guesswork, including a particular streaming service for incoming requests, a specific gateway layout, COSMO placed at the centre, and the split into its exact boxes. It also leaves out the one internal component Amazon has confirmed, the router. If you meet a diagram like it, the router is the quickest test of whether it was drawn from Amazon's own statements.

## The whole picture

Alexa for Shopping, formerly Rufus and now part of Alexa+, is a conversation with Amazon that you can start on an Echo and finish in the app. Amazon confirms its main parts: several models on Bedrock, namely Claude Sonnet, Nova and a custom shopping model; a real-time router that picks one per query; retrieval that grounds answers in the catalog, reviews, outside publications and your own orders and account memory; and actions that run from adding to the cart through price alerts to auto-buy and Buy for Me. The order in which these run for a single question, with the router choosing, retrieval feeding the chosen model, and the answer turning into an action, is my reading of how the confirmed parts fit, because the wiring itself has not been published. Anything more detailed, such as COSMO sitting inside it, is a guess, however neat the diagram.

## Going further

- Prompt caching: a Bedrock feature Amazon says it uses to cut response time, by reusing work on parts of a request the model has already seen.
- Parallel tool calling: another Bedrock feature Amazon names for speed, letting a model ask for several outside lookups at once instead of one after another.
- Shop Direct: the alternative to Buy for Me, which sends you to the merchant's own website instead of buying for you.
- Amazon Lens Live: Amazon's camera-based search, one more place where Alexa for Shopping can be used.

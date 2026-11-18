# Alexa for Shopping, From Question to Purchase

By the end you will know what Amazon's shopping assistant is, how it decides how to answer, what it can do on your behalf, and which parts of its inner workings are known and which are guesswork.

## A shopping question a search box can't answer

Suppose you bought an espresso machine on Amazon last year and now need replacement water filters. An ordinary search for "espresso filter" returns hundreds of products. Most won't fit your machine, and nothing on the results page tells you whether the price today is good or bad. What you want to ask is a sentence: "Which filters fit the machine I bought last year, and is now a good time to buy?"

Alexa for Shopping is Amazon's answer to that kind of sentence. It is a chatbot inside Amazon's store. You type or speak a question in plain language and it replies, and it can also act for you by adding items to your cart, watching prices, or placing an order.

It started under another name. Amazon first launched it as a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping and folded into Alexa+, the version of Amazon's voice assistant that is built on generative AI.

Being part of Alexa+ means it shares conversation context with Alexa+ and with Echo devices, Amazon's smart speakers. You could start talking about filters to an Echo in the kitchen and carry on with the same conversation later in the shopping app.

In the Amazon Shopping app it sits behind an Alexa icon in the navigation bar. On the website it appears on the homepage and on product pages, and when you type a natural-language question into the ordinary search bar, that question often opens a conversation with it. You need neither a Prime membership nor an Echo to use it.

So that's the product from the outside. What happens to your filter question once you send it?

## Several models and a router

Your question about filters has reached Amazon. Answering it needs a program that can read a sentence and write a sensible reply.

That kind of program is a language model: software trained on very large amounts of text so that it can read a request and produce fluent text in response. Alexa for Shopping is a product built on top of language models. It is not a single model itself.

The models run on Amazon Bedrock, Amazon's cloud service for hosting AI models and answering requests to them. Bedrock is the machinery that keeps the models running and delivers each question to one of them.

Alexa for Shopping draws on more than one model. Amazon names three sources: Anthropic's Claude Sonnet, Amazon's own family of models called Nova, and a custom model Amazon built specifically for shopping. The custom model draws on Amazon's product catalog, customer reviews, the community questions and answers on product pages, and information from the web.

Something has to decide which model takes your question. Amazon calls this a real-time router. For each query it looks at what type of question it is and picks a model, balancing three things: how capable the model is, how quickly it can answer, and how good the answer will be.

This is where a common misunderstanding sets in. Because Claude Sonnet is in the list, it's tempting to say "Alexa for Shopping is Claude" or "Alexa for Shopping is Amazon's model." Neither is right. It is a product that sends each question to whichever model the router judges best for that question. Your filter question might go to one model and your next question to another, and the conversation would feel like one continuous assistant either way. Amazon has not published which kinds of question go to which model.

Picking a model is only half the job, though. A model on its own knows nothing about your machine or about today's prices, so where does that knowledge come from?

## Grounding the answer in real data and in you

The router has chosen a model for your question. But a language model learns from text gathered before it was trained, so on its own it can't know which filter is in stock this morning or what you bought last year.

Alexa for Shopping fills that gap with retrieval-augmented generation, usually shortened to RAG. Before the model writes anything, the system fetches material relevant to the question and hands it to the model, so the answer rests on that material and not on the model's memory alone. For your filters, it would retrieve the product listings, reviews and community answers that mention your espresso machine.

For questions about products and trends, Amazon names outside publications among the material it retrieves, including The New York Times, USA Today, Good Housekeeping and Vogue. A question like "what do reviewers say is the best home espresso setup?" can be answered from that kind of writing as well as from Amazon's own pages.

The second half of the knowledge is about you. Amazon calls it account memory. It is built from your shopping activity, which is how the assistant can check compatibility against your past orders, and it also holds details you mention in conversation, such as family members, pets or dietary preferences.

You can inspect and correct that memory. You can ask the assistant what it remembers and fix it in the same conversation, and a page called Review Alexa History lets you manage the stored history directly.

Put those together and your question gets a grounded reply. The assistant knows which machine you own from account memory, retrieves the filters listed as fitting it, and shows you the price history for the last 30 and 90 days, so you can see whether today's price is low or high. It can also list any current deals on those filters.

A good answer is still only an answer. The difference from a search page is what it can do next.

## From answer to action

You now have an answer about which filters fit and what they have cost lately. Alexa for Shopping can also take steps for you, and each step keeps you in control in a slightly different way.

The simplest step is adding items to your cart. You can ask it to add the filters, or hand it a photo of a handwritten grocery list and have the items added from that. Anything it puts in the cart waits there for you to review before checkout.

Next is a price alert. Say the filter pack costs 24 dollars today and the 90-day history shows it sometimes drops to 19. You can ask to be told when it reaches 19, and the assistant watches the price for you.

Auto-buy goes one step further, and it is for Prime members only. You set the target of 19 dollars, and when the price reaches it, the assistant completes the purchase on its own, using your default payment method and address, and then tells you. You then have 24 hours to cancel at no cost. One auto-buy request can stay active for up to six months, so you could set it today and forget about it until spring. Amazon reports that auto-buy customers save 20 percent per purchase on average.

The assistant can also shop beyond Amazon. With Buy for Me, it buys an item from another brand's own website on your behalf. Shop Direct is the gentler option: it sends you to the merchant's site to buy it yourself.

After the purchase, the same conversation handles customer service. It can track the package, start a return or refund, change an order, and hand you over to a human agent when needed.

Amazon's published figures give a sense of scale. More than 250 million customers used the assistant in 2025, and customers who use it during a shopping trip are over 60 percent more likely to buy something on that trip.

All of that is what Amazon has stated. The harder question is how these pieces are wired together inside.

## What is known and what is guessed

You have the confirmed pieces: several models on Bedrock, a router that picks between them, retrieval that grounds each answer, account memory, and a set of actions. How those pieces connect inside Amazon's systems is not public. No Amazon document describes the wiring.

Two kinds of material get close, and both should be held more loosely than everything above.

The first is research Amazon has published. COSMO is a knowledge graph, which here means a large web of links between what shoppers intend and which products serve that intent. The paper's example links a search for shoes by pregnant shoppers to slip-resistant shoes, through the relation "pregnant, requires, slip-resistant." Amazon built it by mining what people search for and then buy, and what they buy together, and generated it at scale with a fine-tuned language model. The paper says COSMO is deployed in Amazon search. No source behind this article says Alexa for Shopping uses it. That would be plausible, since both serve shopping intent, but it is unconfirmed.

The second is a guessed architecture diagram produced by another AI assistant, and it is not Amazon's design. It stacks the system in layers, from the app and website at the top, through the models and three data services, down to the cart and checkout actions. Much of it matches the confirmed facts: the places you use it, Bedrock models, retrieval over the catalog and reviews, user memory, live prices for alerts and auto-buy, and the cart and Buy for Me actions. The rest is its own invention, including a specific gateway and event-streaming setup, COSMO placed inside the core, and the neat division into exactly those boxes. It also leaves out the one internal component Amazon has confirmed, the real-time router. If you meet a tidy diagram of Alexa for Shopping, the router is a quick test of how closely it follows what Amazon has said.

## The whole picture

Alexa for Shopping is Amazon's shopping chatbot, formerly Rufus and now part of Alexa+. It exists so that you can ask a shopping question as a sentence and get either an answer or an action back. Each question goes to a real-time router, which picks one of several language models on Amazon Bedrock. The answer is grounded by retrieving catalog listings, reviews, community answers and outside publications, and it is personalised by account memory of what you have bought and told it. From there it can act on your behalf, through the cart, price alerts, auto-buy, Buy for Me and customer service. Each of those components is confirmed by Amazon. The order in which they run here, with routing first, then retrieval and memory, then action, is my reading of how they fit together, because Amazon has not published how they are wired.

## Going further

- Amazon Lens Live: the camera-based search in the Amazon app, another place where Alexa for Shopping appears.
- Prompt caching: a Bedrock feature that reuses work on repeated parts of a request. Amazon says it uses it to cut response time.
- Parallel tool calling: a Bedrock feature that lets a model request several lookups or actions at once rather than one after another. Amazon also cites it for speed.
- COSMO-LM: the fine-tuned model behind COSMO, trained on about 30,000 human-annotated instructions and covering 18 major product categories.

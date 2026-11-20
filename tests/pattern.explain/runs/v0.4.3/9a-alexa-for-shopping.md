# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it turns a question into an answer or a purchase, and which parts of its inner design are known and which are guesses.

## The problem it solves

A search box is good at matching words to products and bad at answering questions. Type "water filter" into a shop's search bar and you get hundreds of filters. What you wanted to know was narrower: which filter fits the fridge you bought last year, whether today's price is a good one, and whether someone can buy it for you when it gets cheaper. Answering that takes something that can read a question, look things up, and act.

Amazon's answer was a shopping chatbot called Rufus. A chatbot here means a program you talk to in ordinary sentences, typed or spoken, that replies in sentences rather than with a list of links.

On May 13, 2026, Rufus was renamed Alexa for Shopping. It became part of Alexa+, which is Amazon's newer version of its Alexa voice assistant, rebuilt around generative AI: software that writes its replies fresh each time instead of picking from prepared ones.

You meet it in several places. In the Amazon Shopping app there is an Alexa icon in the navigation bar. On the Amazon website, the homepage and product pages offer it, and typing a full question into the ordinary search bar often opens a conversation with it instead of a results page. You do not need a Prime membership to use it.

So take that question and ask it: "Which water filter fits the fridge I bought last year, and is now a good time to buy?" The rest of this piece follows what happens to it.

## Several models behind one assistant

Your question about the fridge filter has to be read and answered by something, and the first thing to know is that "something" is not a single program.

The part that reads and writes language is a language model: a large AI system trained on huge amounts of text, which takes in a passage and produces a fitting continuation, such as an answer to a question. A model is the engine; Alexa for Shopping is the product built around it.

Those models run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models live and where requests to them are sent.

Alexa for Shopping draws on more than one model. The first named in Amazon's own account is Claude Sonnet, a general-purpose model made by Anthropic, an AI company separate from Amazon.

The second is Amazon's own family of models, called Nova.

The third is a custom model Amazon built for shopping. It draws on Amazon's product catalog, customer reviews, the questions and answers shoppers post on product pages, and information from the web.

With three models available, something has to decide which one takes your question. That job belongs to a real-time router: a component that looks at each query as it arrives, judges what type of query it is, and sends it to a model. Amazon says the router balances three things: how capable the model is, how fast it replies, and how good the answer is.

This is where a common picture goes wrong. It is natural to imagine one AI sitting behind the Alexa icon, the same mind answering every message. The confirmed design is a router choosing among several models per query, so two questions in the same conversation may be answered by different models. The sources behind this article do not cover which model gets which kind of question, so it would be guesswork to say which one handles your fridge filter.

Choosing a model settles who writes the answer, but a model on its own knows nothing about this morning's prices or about your fridge.

## Grounding the answer

Your question has now reached a model chosen by the router. What it still lacks is current, specific material to answer from.

Alexa for Shopping uses retrieval-augmented generation, usually shortened to RAG. Before the model answers, the system fetches material relevant to the question and hands it to the model along with the question, so the answer is grounded in what was fetched rather than only in what the model absorbed during training. Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue among the sources for product and trend questions.

The other half of your question is about you: the fridge you bought. For that the assistant has account memory. It is built from your shopping activity, plus details you tell it, such as family members, pets or dietary preferences. You can ask it what it remembers and correct it in the conversation.

Among the things Amazon lists the assistant as able to do is check compatibility against past orders. So it can tell you which filter fits the fridge in your order history. How the lookup is wired internally is not described in the sources; assistants of this kind usually pass the relevant account details to the model alongside the retrieved product material.

The "good time to buy" part is answered from price history. The assistant can show what a product cost over the last 30 days and the last 90 days, and list current deals. Say the filter is $49.99 today and its 90-day history shows it dipped to $39.99 once. That is a fair hint that waiting may pay.

An answer about the filter is useful, but the assistant is built to go a step further and act on it.

## From answer to action

You now hold a model chosen per question, grounded with fetched material and with your account memory. The last stage is what the assistant can do for you, not only tell you.

It can add items to your cart. That includes reading a photo of a handwritten grocery list and adding what is on it. Items in the cart are reviewed by you before checkout, so this action stops short of spending money.

It can set a price alert. You name a target price for the filter, say $40, and it tells you when the price reaches it.

For Prime members there is a stronger version called auto-buy. You set the same $40 target. The assistant watches the price, and when it reaches $40 it completes the purchase itself, using your default payment method and address, then notifies you. You then have 24 hours to cancel at no cost. A request lasts up to six months, so if the filter never drops to $40 in that time, nothing is bought.

Auto-buy is the point where the assistant spends money without a further click from you, which is why the 24-hour free cancellation matters: it is your check after the fact, in place of the cart review you get with an ordinary add-to-cart.

It also handles customer service: tracking packages, returns, refunds, changes to orders, and handing you over to a human agent when needed.

All of this describes what the assistant does. How its parts are connected inside is a different and much less certain matter.

## What is known and what is guessed

Everything so far comes from Amazon's own statements or reporting on them: the models, the router, Bedrock, RAG, account memory and the actions. The internal architecture, meaning how those components are wired together, is not confirmed anywhere public. From here on, the material is research and guesswork, and is labelled as such.

The research is COSMO, published by Amazon's scientists in 2024. COSMO is a knowledge graph: a large store of facts kept as links between things. This one links what shoppers intend to the products that serve that intent. The paper's example connects a search for shoes by pregnant shoppers to slip-resistant shoes, through the link "pregnant requires slip-resistant". The paper says COSMO is deployed in Amazon search, for search relevance, recommendations within a shopping session, and search navigation. That Alexa for Shopping uses COSMO is not confirmed. It is plausible, since both serve shopping intent, but no source says so.

The guesswork is an architecture diagram produced by another AI assistant, which the material behind this article includes and marks as not Amazon's design. It draws the system as stacked layers, from the app and website at the top, through request handling and language processing, to a core of Bedrock models, then data services, then shopping actions at the bottom.

Several of its boxes match confirmed facts: the places you use it, the Bedrock models, RAG over catalog and reviews, user memory, real-time prices for alerts and auto-buy, and the cart and buying actions. Others are its own guesses: a particular data-streaming service, the specific layout of the entry layer, COSMO placed inside the core, and the division into those exact boxes. It also leaves out the model router, which Amazon has confirmed. A picture that shows a single core where Amazon describes a router choosing among models repeats the misconception from earlier, so it is the confirmed list, not the diagram, to build on.

## The whole picture

Alexa for Shopping is Amazon's shopping assistant, formerly Rufus and now part of Alexa+, and it exists to answer shopping questions and act on them where a search box can only match words. Confirmed by Amazon: a router sends each query to one of several language models running on Bedrock; RAG fetches material to ground answers; account memory holds what it knows about you; and it can add to your cart, alert you to prices, auto-buy for Prime members, and handle customer service. In the fridge filter example, the order of events, with the answer drawing on your order history and then leading to an alert or auto-buy at $40, is my reading of how those confirmed parts fit together, since the sources do not describe the wiring. COSMO is Amazon research that may or may not be involved, and the layered diagram is a guess.

## Going further

- Buy for Me: a feature that buys items from other brands' websites on your behalf; its counterpart, Shop Direct, sends you to the merchant's own site instead.
- Amazon Lens Live: Amazon's camera-based search, where you point your phone at an object, and one of the places Alexa for Shopping appears.
- Echo continuity: Echo devices are Amazon's smart speakers, and Alexa for Shopping shares conversation context with them, so a conversation started on one can continue in the app.
- Review Alexa History: the page where you manage what the assistant has stored about your conversations and activity.

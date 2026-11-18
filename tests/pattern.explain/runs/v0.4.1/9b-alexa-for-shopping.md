# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it turns a question into an answer and sometimes into a purchase, and how much of its inner design is actually known.

## The problem it was built for

Shopping by keyword search puts the work on you. You have a need, such as "a cover that fits my e-reader and doesn't cost too much", and you have to turn it into search words, open product pages one by one, read reviews, and check prices yourself. Shopping assistants of this kind exist to take that translation off your hands: you describe what you want in ordinary language, and the assistant does the searching, comparing and checking.

Alexa for Shopping is Amazon's assistant for this. You can type to it or speak to it in the Amazon Shopping app, where it sits behind an Alexa icon in the navigation bar, and on the Amazon website, including the homepage and product pages. On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it. Amazon says more than 250 million customers used it in 2025.

It did not start under this name. Amazon first launched a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping.

The rename came with a move. Alexa for Shopping was folded into Alexa+, Amazon's generative-AI version of its Alexa assistant, meaning a version built on AI that writes new replies rather than picking from prepared ones. It shares conversation context with Alexa+ and Echo devices, Amazon's smart speakers, so a conversation started on an Echo can continue in the shopping app.

That link to Echo invites a wrong assumption: that you need a speaker, or a paid membership, to use it. You need neither. No Prime membership and no Echo device is required.

Here is the case this piece follows. You own an e-reader you ordered from Amazon last year. You find a cover listed at $39.99 and ask: "Will this fit the e-reader I bought last year, and is this a good price?" Something has to understand that question, and the next part is about what that something is.

## Several models behind one conversation

You have typed a question that mixes your own order history with a judgement about price. What reads it is a language model: a program trained on vast amounts of text that can read a question in plain words and write a fluent reply. That is general background, true of assistants of this kind, not a detail specific to Amazon.

Alexa for Shopping does not run on a single language model. It draws on several, and they all run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models live and answer from; it is not itself a model.

The first of the models is Claude Sonnet, a general-purpose model made by the AI company Anthropic.

The second is Amazon's own family of general models, called Nova.

The third is a custom model Amazon built for shopping. It uses Amazon's product catalogue, customer reviews, the community questions and answers on product pages, and information from the web.

With three models available, something has to decide which one answers your question about the cover. That job belongs to a router: a component that looks at each incoming query and, in real time, picks the model to handle it according to the type of query. Amazon describes the goal as balancing capability, response time and answer quality. A heavyweight model may write a better answer to a hard question, but it is usually slower and costlier to run, so sending every question to it would waste time on easy ones. The sources behind this article do not cover which model receives which type of query.

This is where the most common mental picture goes wrong. People tend to imagine one chatbot as one model, so they ask "which AI is Alexa for Shopping?" as if it had a single answer. The confirmed design is a small team of models with a dispatcher in front, and the reply you get to your cover question comes from whichever model the router chose for it.

A model on its own, though, knows only what it absorbed in training. It has never seen today's price of your cover or the details of your order from last year, so how does its answer end up grounded in those facts?

## Grounding the answer, and remembering you

The router has handed your question to one of several models running on Bedrock. That model now needs current, specific facts it was never trained on.

The technique Amazon uses is retrieval-augmented generation, usually shortened to RAG. Before the model writes anything, the system fetches material relevant to the question and gives it to the model along with the question, so the answer is built on that material rather than on the model's memory alone. In general practice this reduces the risk of a model confidently inventing details, because it has the real text in front of it. For product and trend questions, Amazon names well-known publications among the sources, The New York Times among them.

Your question also refers to "the e-reader I bought last year". Among its confirmed abilities, Alexa for Shopping can check a product's compatibility against your past orders, so it can look at what you actually bought and say whether the cover is made for that model. It can also answer product questions and compare products side by side.

The second half of your question, "is this a good price?", has its own confirmed tool: price history. It can show how a product's price moved over the last 30 and 90 days, and list current deals. Suppose the 90-day history shows the cover fell as low as $29.99. That tells you $39.99 is not the best price it has had recently.

Separately from your orders, it keeps what Amazon calls account memory. This is built from your shopping activity, plus details you tell it, such as family members, pets or dietary preferences. You can ask it what it remembers and correct it in the conversation, and you can manage the history on a page called Review Alexa History.

So far you have an answer: the cover fits, and it has been cheaper. The remaining question is what happens if you want it to act on that answer, not just give it.

## From answer to purchase

You now know the cover fits your e-reader and that its price has recently dipped to $29.99. Alexa for Shopping can do more than tell you this.

It can add items to your cart, including from a photo of a handwritten grocery list. Items in the cart are reviewed by you before checkout, so this step does not spend your money by itself.

It can set a price alert: you name a target price, and it tells you when the product reaches it.

Auto-buy goes further, and it is for Prime members. You give a target price, and it watches the price for you. When the price reaches your target, it completes the purchase using your default payment method and address, then notifies you. You then have 24 hours to cancel free of charge. A single auto-buy request lasts up to six months. In your case: you set auto-buy at $30, the cover drops to $29.99 some weeks later, the order goes through, and you get a notice with a day to change your mind. That is about $10 saved, a quarter off. Amazon says auto-buy customers save an average of 20 percent per purchase.

The difference between a price alert and auto-buy is the part worth holding on to: an alert informs you, while auto-buy spends money for you and relies on the 24-hour cancellation window as your safety net.

Its reach also goes beyond Amazon's own shelves. A feature called Buy for Me can buy items from other brands' websites on your behalf.

After the purchase it handles customer service tasks: tracking the package, returns, refunds, changes to an order, and handing you over to a human agent when needed.

Amazon also publishes a figure on how this changes behaviour: customers who use the assistant during a shopping trip are over 60 percent more likely to buy on that trip. All of this describes what the assistant does. A curious reader will want to know how the parts are wired together inside.

## What is known about the inside, and what is guessed

You have the confirmed picture now: several models on Bedrock with a router in front, answers grounded by RAG, account memory, and actions from cart to auto-buy. This is where the confidence changes.

The internal architecture is not public. No Amazon document describes how these components are connected to each other. Anything more detailed than the list of confirmed parts is somebody's reconstruction.

One piece of related material is real but not confirmed as part of this product. Amazon has published research on a system called COSMO, a knowledge graph of shopping common sense: a large map of links between what people intend and what products serve that intent. The research paper's example connects a search for shoes by pregnant shoppers to slip-resistant shoes. The paper says COSMO is deployed in Amazon search. No source says Alexa for Shopping uses it. It is plausible, since both serve shopping intent, but that is as far as the evidence goes.

The material behind this article also includes a guessed architecture diagram produced by another AI assistant, which is not Amazon's design. It stacks the system into neat layers, from the app and website at the top down to a layer that adds to cart and checks out. Several of its boxes match confirmed facts: the touchpoints, the Bedrock models, RAG over the catalogue and reviews, user memory, real-time prices for alerts and auto-buy, and the cart and Buy for Me actions. The rest is its own guesswork: specific plumbing that no confirmed source mentions, COSMO placed at the centre, and the exact division into those boxes. It also leaves out the router, which is one of the few internal parts Amazon has confirmed.

## The whole picture

Alexa for Shopping, renamed from Rufus and folded into Alexa+ in May 2026, exists to let you shop by asking rather than by searching. What is confirmed is a set of parts: a real-time router that sends each query, by type, to one of several models on Amazon Bedrock; retrieval-augmented generation that grounds answers in fetched material; account memory; checks against past orders and price history; and actions from the cart through price alerts, auto-buy and Buy for Me to customer service. In your cover example, the order in which these parts work together, question to router to model with fetched facts to an auto-buy at $30, is a reading of those confirmed parts, not a published design, because how they are wired inside has not been published.

## Going further

- Amazon Lens Live: Amazon's camera-based search, another place where the assistant can be used.
- Prompt caching: a Bedrock feature Amazon says it uses to cut response time, by reusing work on parts of a prompt that repeat.
- Parallel tool calling: another Bedrock feature Amazon cites for speed, letting a model request several lookups or actions at once instead of one after another.
- Shop Direct: the alternative to Buy for Me, which sends you to the merchant's own website to buy there.

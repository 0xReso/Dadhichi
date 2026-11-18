# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it turns a question into a grounded answer or a purchase, and which parts of its inner workings are confirmed and which are guesses.

## A shop too big to browse

Amazon sells more products than anyone could compare by hand. A shopper with a real question, such as "will this grinder fit the espresso machine I bought last year?", has had to piece the answer together from product pages, reviews and their own order history. Search boxes match words. They do not answer questions.

Alexa for Shopping is Amazon's answer to that: a conversational assistant built into the shop. You ask in ordinary language, by typing or speaking, and it answers, compares, checks and, if you ask, buys. It started life as a shopping chatbot called Rufus. On May 13, 2026, Amazon renamed it Alexa for Shopping and folded it into Alexa+, the generative-AI version of its Alexa voice assistant.

Because of that merger, it shares conversation context with Alexa+ and Echo devices. A conversation you start by talking to an Echo speaker in the kitchen can carry on in the shopping app on your phone.

It lives in several places: behind an Alexa icon in the navigation bar of the Amazon Shopping app, on the Amazon website, on the homepage and on product pages. On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it. You do not need a Prime membership or an Echo device to use it. Amazon says more than 250 million customers used it in 2025.

To follow it through, take one shopper. Priya owns an espresso machine she bought on Amazon last year. She is looking at two coffee grinders, one of them priced at $120, and types: "Which of these two grinders works with my espresso machine, and is the $120 one a good price right now?"

That one sentence needs product knowledge, her purchase history, and price data, all at once. What actually reads it?

## Several models and a router

Priya's question is now in the assistant's hands, and it needs something that can understand language. That something is a language model: a program trained on huge amounts of text that reads a request and writes a fluent reply. The model is not the product. Alexa for Shopping is the product; models are engines inside it.

Those engines run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models sit and where requests to them are handled.

Here is the point people most often get wrong: Alexa for Shopping is not one AI. It draws on several models. One is Anthropic's Claude Sonnet. Another family is Amazon's own Nova models. The third is a custom model Amazon built for shopping, which uses Amazon's product catalog, customer reviews, community questions and answers, and information from the web.

Something has to decide which model gets Priya's question. That job belongs to a router: a component that looks at each incoming query and, in real time, sends it to the model best suited to its type. Amazon describes the router as balancing three things: how capable the model is, how fast it responds, and how good the answer will be. A quick "where is my parcel?" and a careful compatibility comparison do not need the same engine.

Amazon does not say which model handles which kind of query, so the sources behind this article cannot tell you which one would take Priya's question. What matters is that a choice is made for every query.

Whichever model gets it, it still faces a problem: a model on its own does not know Priya's order history or today's price of a grinder. Where do those facts come from?

## Fetching facts before answering

Priya's question has reached a model, chosen by the router. A model by itself only knows what was in its training text, which goes out of date and never included her account.

Alexa for Shopping deals with this through retrieval-augmented generation, usually shortened to RAG. Before the model writes an answer, the system fetches relevant material and hands it to the model along with the question, so the answer is grounded in that material rather than in the model's memory. For product and trend questions, Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue among its sources, alongside its own catalog and reviews.

For Priya, that means the model can be given the two grinders' product details and reviews, and her past orders, so it can check compatibility against the espresso machine she actually bought. Checking compatibility against past orders is something Amazon says the assistant does.

The price half of her question is answered the same way. The assistant can show 30-day and 90-day price history and list current deals. So it can tell her whether $120 is low or high compared with the last three months, using real numbers instead of a guess.

There is one more kind of material it can draw on. Amazon calls it account memory: a record built from your shopping activity, plus details you tell it, such as family members, pets or dietary preferences. If Priya once mentioned she only drinks decaf, that could shape later suggestions. You can ask it what it remembers and correct it in conversation, and manage your history on a page called Review Alexa History.

Amazon does not publish how retrieval, memory and the router fit together in order. Systems of this kind usually pick the model, gather the supporting material, and then generate the reply, but that sequence is general practice, not something the sources confirm for this one.

Priya now has her answer: the cheaper grinder fits, and $120 is above its recent low. Answering is only half the assistant's job. What happens when she wants it to act?

## From answer to action

Priya knows which grinder fits and that its price has been lower. A plain chatbot would stop there. Alexa for Shopping can do things in the shop for her.

The simplest action is adding items to the cart. It can even do this from a photo of a handwritten grocery list. Whatever it adds, the customer reviews the cart before checkout, so nothing is bought without a final look.

Next is a price alert. Priya can say "tell me when this grinder drops to $95", and it will watch the price and notify her when it gets there.

Auto-buy goes one step further, and it is for Prime members. The assistant watches the price, and when it reaches the target, it completes the purchase using the customer's default payment method and address, then tells them. Priya would have 24 hours to cancel at no cost. A request can stay active for up to six months, so her $95 target could wait out a long stretch of full prices. Amazon says auto-buy customers save an average of 20 percent per purchase; at $120, that would be about $24.

Some of what Priya wants may not be sold by Amazon at all. Buy for Me lets the assistant buy items from other brands' websites on the customer's behalf. A related option, Shop Direct, does not buy anything; it sends the customer to the merchant's own site to buy there.

It also handles the chores after a purchase: tracking packages, returns, refunds and order changes. When a problem needs a person, it hands the conversation to a human agent.

Amazon also gives a number for the whole experience: customers who use the assistant during a shopping trip are over 60 percent more likely to buy on that trip.

All of this describes what the assistant does. A natural next question is what its inside looks like, and here the evidence changes character.

## What is confirmed, and what is guessed

Everything so far, from the models and router to retrieval, memory and the actions, comes from Amazon's own announcements and reporting on them. The internal wiring is a different matter: no Amazon document describes how the components are connected.

Two other pieces of material are often placed next to the assistant, and both need care.

The first is published Amazon research on COSMO, a knowledge graph of shopping common sense. A knowledge graph is a store of facts written as links between things. COSMO links what people intend to the products that serve that intent: its paper's example connects shoe searches by pregnant shoppers to slip-resistant shoes. The paper says COSMO is deployed in Amazon search. No source says Alexa for Shopping uses it. It is plausible, because both serve shopping intent, but it is not confirmed.

The second is, in the words of the sources behind this article, a guessed architecture diagram produced by another AI assistant, not Amazon's design. It stacks the system into layers, from the app and website at the top, through a gateway and language-processing front ends, to a core of Bedrock models plus COSMO, then data services and finally the cart and checkout actions.

Some of its boxes match confirmed facts: the places people use the assistant, the Bedrock models, retrieval over catalog and reviews, user memory, live prices for alerts and auto-buy, and the cart and Buy for Me actions. Other parts are the diagram's own guesses, including placing COSMO inside the core and the exact way the boxes are split. It also leaves out the one internal component Amazon has confirmed: the model router. If you meet a neat layered picture of this system, read it as a guess, and check whether it has the router.

## The whole picture

Alexa for Shopping is Amazon's conversational shopping assistant, formerly Rufus and now part of Alexa+, built so that a question like Priya's can be answered and acted on inside the shop. Confirmed by Amazon: it runs on Bedrock, a router sends each query to one of several models (Claude Sonnet, Nova, or Amazon's custom shopping model), answers are grounded by retrieval from the catalog, reviews and named publications, account memory adds what it knows about you, and a set of actions turns answers into carts, price alerts, auto-buys, Buy for Me purchases and customer service. The order in which these pieces run for a given question is my reading of how such assistants usually work, not something Amazon has published, and COSMO and any layered diagram remain outside the confirmed picture.

## Going further

- Amazon Lens Live: the camera-based search in the app, which is another place the assistant appears.
- Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to make responses faster.
- COSMO-LM: the fine-tuned language model the COSMO paper uses to generate its knowledge graph, trained on about 30,000 human-annotated instructions across 18 product categories.
- Review Alexa History: the page where customers manage what the assistant has stored about their conversations.

# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it turns a question into an answer and then into a purchase, and which parts of its inner design are confirmed and which are guesses.

## A question the search box cannot answer

Say you bought an espresso machine on Amazon last year and now want a coffee grinder to go with it. A search box handles "coffee grinder" well: it returns thousands of grinders. What it cannot handle is the question you actually have, which is "which of these works with the machine I already own, and is now a good time to buy one?" Answering that means reading product details, remembering what you bought, and knowing how prices have moved. Until recently, that work was yours.

Alexa for Shopping is Amazon's answer to that gap: an AI assistant you can talk to while you shop, which answers questions in plain language and can also act for you, from filling your cart to buying an item when its price drops. You can type to it or speak to it.

It began life under another name. Amazon first launched it as a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping.

The rename came with a move. The assistant was folded into Alexa+, which is the newer version of Amazon's voice assistant Alexa, rebuilt on generative AI, the kind of AI that writes its own replies instead of picking from a fixed list of answers.

Being part of Alexa+ means it shares conversation context with Amazon's Echo smart speakers. A conversation you start by talking to an Echo in the kitchen can carry on later in the shopping app on your phone. You do not need an Echo, though, and you do not need a Prime membership to use it.

You reach it in a few places. In the Amazon Shopping app there is an Alexa icon in the navigation bar. On the Amazon website it appears on the homepage and on product pages, and typing a full question into the ordinary search bar often opens a conversation with it instead of a plain list of results. So you type: "Which grinder works with the espresso machine I bought last year?" What happens to that sentence next?

## Several models behind one conversation

You now have the problem and the product: a question that a keyword search cannot answer, and an assistant inside the Amazon app and website that takes questions in plain language. The first thing it does with your grinder question is decide who should answer it.

The assistant runs on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is where the models live and where requests to them are sent.

The answering is done by language models: programs trained on very large amounts of text that can read a question and write a reply. Alexa for Shopping draws on several of them rather than one.

One is Claude Sonnet, a general-purpose language model made by the AI company Anthropic.

Another family is Nova, Amazon's own set of general-purpose models.

The third is a custom model Amazon built for shopping. It draws on Amazon's product catalog, customer reviews, the community questions and answers on product pages, and information from the web.

With several models available, something has to choose between them for each message. That part is called a router, and Amazon describes it as working in real time: it looks at what kind of query has arrived and picks the model to handle it, balancing how capable the model is, how fast it answers, and how good the answer is. The sources behind this article do not say which model gets which kind of question.

This is the point where people most often go wrong about the product. It is easy to picture "Alexa" as a single AI brain that you are chatting with. It is closer to a front desk: one conversation on your screen, with the router passing each message to whichever model suits it. Your grinder question and your next message might be handled by different models, and you would not see the switch.

Whichever model gets your question, it still has to know facts it was never trained on, such as today's price of a grinder or what you ordered last year. Where do those come from?

## Grounding the answer in real data

So far your question has been routed to a model running on Bedrock. A language model on its own only knows what was in its training text, which goes out of date and never included your orders. The assistant deals with that in a few ways.

The main one is called retrieval-augmented generation, usually shortened to RAG. Before the model writes its answer, the system fetches material relevant to the question and hands it to the model along with the question, so the answer rests on that material rather than on the model's memory alone. For product and trend questions, Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue among its sources.

For your grinder, the assistant can check compatibility against your past orders, which is one of its listed abilities. It can then compare the grinders that fit, answer follow-up questions about them, and show each one's price history over the last 30 and 90 days, along with any current deals. Suppose the grinder you like costs $160 today and the 90-day history shows it dipped to $130 twice.

The assistant also keeps what Amazon calls account memory. It is built from your shopping activity, plus details you tell it, such as who is in your family, what pets you have, or that you are vegetarian. You can ask it what it remembers and correct it in the conversation, and you can manage your history on a page called Review Alexa History. The sources behind this article do not spell out how account memory and the past-orders check work together; treating them as one feature would be a reading of mine, not something Amazon states.

Knowing the grinder fits and that $160 is not its best price, you are ready to act. How far can the assistant go on your behalf?

## From answer to action

You now hold the grinder's compatibility and its price history, gathered by a routed model with retrieved material in front of it. The assistant can also do things, not only say things, and each action comes with its own rule about who has the final word.

The simplest is adding items to your cart. It can even do this from a photo of a handwritten grocery list. Items in the cart are reviewed by you before checkout, so nothing is bought at this step.

The next is a price alert. You name a target price, say $130 for the grinder, and the assistant tells you when it gets there. You still do the buying.

The furthest step is auto-buy, offered to Prime members. You set the same $130 target, and the assistant watches the price. When it reaches $130, the assistant completes the purchase itself, using your default payment method and address, and then notifies you. You then have 24 hours to cancel at no cost. A single auto-buy request can stay active for up to six months, so if the grinder takes four months to drop, the request is still waiting.

Its reach also extends beyond Amazon's own shelves. With a feature called Buy for Me, it can buy items from other brands' websites on your behalf.

After the grinder arrives, the same conversation handles customer service: tracking the package, starting a return or refund, changing an order, or handing you over to a human agent if the problem needs one.

That covers what Amazon has said the assistant does. But how are all these pieces actually wired together inside Amazon?

## What is known and what is guessed

You have seen the confirmed parts: a router choosing among models on Bedrock, retrieval that grounds the answers, account memory, and actions from the cart up to auto-buy. Everything up to here rests on Amazon's own announcement and on reporting about it. From here the footing changes.

Amazon has not published the internal architecture. No Amazon document describes how the components connect to each other, so any wiring diagram you meet is a reconstruction.

There is also a piece of published Amazon research worth knowing about, called COSMO, and it is a knowledge graph of shopping common sense: a large web of links between what people intend and which products serve that intent. The paper's example links pregnant shoppers looking for shoes to slip-resistant shoes, through the relation "pregnant requires slip-resistant." The paper says COSMO is deployed in Amazon search. No source says Alexa for Shopping uses it. That is plausible, since both deal with shopping intent, but it is unconfirmed.

The material behind this article also includes a guessed architecture diagram produced by another AI assistant, not by Amazon. It stacks the system into layers, from the app and website at the top down to a layer that performs purchases. Its broad outline matches the confirmed parts: the places you reach the assistant, the Bedrock models, retrieval over the catalog and reviews, user memory, live prices for alerts and auto-buy, and the cart and Buy for Me actions.

Where it differs is where it gets specific. It names a particular event-streaming service, lays out a particular gateway, places COSMO inside the assistant's core, and divides everything into its own exact boxes; none of those details is confirmed. It also leaves out a component Amazon did confirm, the real-time router. If you see this diagram, read it as a plausible sketch with a known gap, not as Amazon's design.

## The whole picture

Alexa for Shopping is the former Rufus, now part of Alexa+, and it exists so you can shop by asking questions instead of sifting search results. Each message you send goes to a real-time router, which picks one of several models hosted on Amazon Bedrock; Amazon confirms the router, the models, and retrieval of material to ground the answers, and it confirms account memory and actions such as the cart, price alerts, auto-buy and Buy for Me. The order in which these parts pass your request along, for example that retrieval and memory feed the chosen model before it answers and that an answer then leads to an action, is my reading of how assistants of this kind usually work, since Amazon has not published how the components are connected. COSMO and the guessed layered diagram sit outside the confirmed picture.

## Going further

- Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to make replies arrive faster.
- Amazon Lens Live: Amazon's camera-based search, which is another place the assistant appears.
- Shop Direct: the alternative to Buy for Me that sends you to the merchant's own website instead of buying for you.
- Published figures: Amazon reports more than 250 million customers used the assistant in 2025, and that shoppers who use it during a trip are over 60 percent more likely to buy on that trip.

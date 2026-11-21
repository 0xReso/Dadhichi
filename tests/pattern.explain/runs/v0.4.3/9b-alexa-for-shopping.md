# Alexa for Shopping

By the end you will know what Amazon's shopping assistant is, how it builds an answer from several AI models and fetched material, what it can do on your behalf, and which parts of its inner design are confirmed and which are guesses.

## A question a search box cannot settle

You ordered a water filter jug from Amazon last spring, and it now needs new filters. A product page offers a pack of three for $32. What you want to know is not really a search: will these fit the jug you own, is $32 a fair price, and would it be cheaper if you waited?

A search box of the ordinary kind matches the words you type against product listings and hands back a ranked list. It handles "replacement filter" well. It handles "will this fit what I already have" badly, because that question needs your order history, the product's details, and some reasoning that joins the two.

Alexa for Shopping is an assistant Amazon has built into its shopping app and website that you talk to in ordinary sentences, by typing or by speaking. In the app it sits behind an Alexa icon in the navigation bar. On the website, typing a full question into the ordinary search bar often opens a conversation with it. You do not need a Prime membership or an Echo speaker to use it.

Since May 13, 2026, it has been part of Alexa+, Amazon's generative-AI version of its Alexa voice assistant: a version that writes new replies rather than picking from pre-written ones. It shares conversation context with Alexa+ and Echo devices, so you could start asking about the filters out loud in the kitchen and continue the same conversation later in the shopping app.

So what happens when you type "Will these filters fit the jug I bought last spring?"

## Several models behind one conversation

You have an assistant on Amazon's app and site that takes plain-sentence questions, and a question about filters that a keyword search cannot settle. The first thing to understand is what writes the reply.

The replies come from language models. A language model is a program trained on enormous amounts of text until it can read a question and write a fluent answer to it, a word at a time.

Those models run on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models. Bedrock is the machinery that keeps the models running and passes each request to the right one.

Alexa for Shopping does not lean on a single model. Amazon says it draws on several, and names three.

The first is Claude Sonnet, a model made by Anthropic, an AI company separate from Amazon.

The second is Amazon's own family of models, called Nova.

The third is a custom model Amazon built for shopping. It uses Amazon's product catalog, customer reviews, community questions and answers (the questions shoppers ask on product pages and other shoppers answer), and information from the web.

Something has to decide which of the three takes your filter question. That part is a real-time router: as each query arrives, it looks at what type of query it is and picks a model, balancing capability, response time, and answer quality. The sources behind this article do not say which type of question goes to which model.

This is where people most often go wrong. It is tempting to think of Alexa for Shopping as an AI model, in the same breath as Claude or Nova. It is a product built on top of models. Two questions in the same conversation can be answered by different models, and in systems of this kind the quality of an answer depends on the router's choice and on the material the model is handed as much as on any one model.

A model, though, knows nothing about your jug or today's price. Where do those facts come from?

## Grounding the answer in fetched facts

Your filter question has gone to one of several models, picked by the router for that type of query. A language model on its own knows only the text it was trained on, which was gathered before it was built, so it cannot know what you ordered last spring or what the filters cost this morning.

The fix is to look things up first. Before answering, Alexa for Shopping fetches material relevant to the question and gives it to the model, so the answer rests on that material rather than on the model's memory of its training text. This technique is called retrieval-augmented generation, usually shortened to RAG. For product and trend questions, Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue among the sources it draws on. The sources behind this article do not list what is fetched for a question like yours.

What the assistant can do with your question is confirmed. It can check whether a product is compatible with things in your past orders, so it can tell you whether the pack fits the jug you bought in the spring.

It can also show a product's price history over the last 30 and 90 days. Suppose the 90-day history shows the pack dipping to $26 twice. Now you know $32 is the high end.

Separately, it keeps what Amazon calls account memory. This is built from your shopping activity, plus details you tell it, such as family members, pets, or dietary preferences. You can ask it what it remembers and correct it in the conversation, and you can manage your history on a page called Review Alexa History.

The filters fit, and $32 is above their recent low. Can the assistant do anything about that?

## From answers to actions

So far the assistant has answered: several models on Bedrock, a router choosing between them, and fetched material behind the reply. It can also act, and each action has its own rules.

The plainest action is adding items to your cart. It can even fill the cart from a photo of a handwritten grocery list. Items in the cart are reviewed by you before checkout, so nothing is bought at this step.

It can set a price alert, telling you when a product reaches a target price you name.

For Prime members, Amazon's paid membership, it goes further with a feature called auto-buy. You give it a target price; it watches the price, and when the price reaches your target it completes the purchase with your default payment method and address, then notifies you. You have 24 hours to cancel for free. A request lasts up to six months. Suppose you set auto-buy for the filters at $26 and, six weeks later, the price reaches $26: the pack is ordered at once to your default address, and you have until the same time the next day to cancel at no cost. Because it uses the defaults, an out-of-date default address is where the filters go.

It can also shop beyond Amazon. With Buy for Me, it buys items from other brands' websites on your behalf. Shop Direct does the opposite: it sends you to the merchant's own site to buy there yourself.

Finally, it handles customer service tasks: tracking packages, returns, refunds, and order changes, and handing you over to a human agent. If the filters arrive damaged, the return can start in the same conversation.

All of that is confirmed. How the pieces are wired together inside is a different matter.

## What is confirmed and what is guessed

You now hold the confirmed parts: several models on Bedrock with a router choosing between them, fetched material behind each answer, account memory, and actions from the cart to auto-buy. The internal architecture is another story: no Amazon document describes how the components are wired together.

The sources behind this article include a guessed architecture diagram, produced by another AI assistant and not by Amazon. Its broad shape matches confirmed parts: the places you use it, models on Bedrock, fetched catalog and review material, user memory, real-time prices for alerts and auto-buy, and the cart and Buy for Me actions. Its own guesses include a specific Amazon data-streaming service, a particular layout for the front door that requests pass through, and the division into its exact boxes. It also leaves out the router, which is confirmed. If you see a box diagram of Alexa for Shopping, treat the boxes as a guess and check for the router.

That diagram also places a piece of Amazon research at the centre. Amazon has published work on a large store of shopping common sense: links between what people intend and the products that serve that intent. Its example is that a search for shoes by pregnant shoppers is linked to slip-resistant shoes, through the relation "pregnant requires slip-resistant". Amazon calls it COSMO, and the paper says it is deployed in Amazon search. That Alexa for Shopping uses COSMO is not confirmed. It is plausible, since both serve shopping intent, but no source says so.

## The whole picture

Alexa for Shopping is a product, not a model: an assistant in Amazon's app and website that takes your question in plain sentences, has a real-time router send it to one of several models running on Bedrock, fetches relevant material so the answer is grounded in it, and draws on account memory, before answering or acting through the cart, price alerts, auto-buy, Buy for Me, and customer service. Each of those parts is confirmed; the order in which this paragraph strings them together is my reading, because how they are wired inside has not been published, and any box diagram of that wiring is a guess.

## Going further

- Rufus: the name of Amazon's shopping chatbot before it was renamed Alexa for Shopping on May 13, 2026; older articles use it.
- Amazon Lens Live: Amazon's camera-based search, in which you point your phone at an object; the assistant is available there too.
- Prompt caching: a Bedrock feature that reuses the already-processed part of a request that repeats from one request to the next, so the model does not reprocess it; Amazon says it is used to cut response time.
- Parallel tool calling: a Bedrock feature that lets a model ask for several outside lookups at once instead of one after another; Amazon also says it is used to cut response time.

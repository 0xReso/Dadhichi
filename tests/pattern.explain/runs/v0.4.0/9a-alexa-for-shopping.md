# Alexa for Shopping

By the end you will understand what Amazon's shopping assistant is, how it chooses a model, grounds its answers and remembers you, what it can buy on your behalf, and which parts of its inner design are known and which are guesswork.

## The problem it was built for

An ordinary shop search box is good at one thing: you type words, it returns products whose listings contain those words. It is poor at the questions people actually have while shopping. "Will this espresso machine work with the grinder I bought last year?" "Is $229 a good price for it, or does it go on sale?" No list of matching listings answers either one. You end up opening tabs, reading reviews, and checking your order history by hand.

Amazon's answer is a conversational assistant that takes the question in plain language and replies in plain language, using what Amazon knows about its products and about you. It was first launched as a chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping and folded into Alexa+, Amazon's generative-AI version of its voice assistant Alexa.

Being part of Alexa+ has a practical effect: the assistant shares conversation context with Alexa+ and with Echo devices, Amazon's smart speakers. A conversation you start by talking to an Echo in the kitchen can carry on later in the shopping app on your phone.

You reach it through the Amazon Shopping app, where there is an Alexa icon in the navigation bar, and on the Amazon website: the homepage, product pages, and Amazon Lens Live, the camera-based search. On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it instead of a results list. You can type or speak, and you need neither a Prime membership nor an Echo device.

Take the espresso question as the example for the rest of this piece. You are on the product page of an espresso machine priced at $229, and you ask whether it will work with your grinder and whether the price is good. Something has to understand the question, find the facts, and write a reply. So what is doing that work?

## Several models behind one assistant

So far you have the problem, a shopping question that a keyword search cannot answer, and the assistant Amazon built to answer it. The thing that reads your question and writes the reply is a language model.

A language model is a program trained on very large amounts of text so that, given some words, it can produce a fitting continuation. Given a question, that continuation is an answer. It is the engine of every chatbot of this kind.

Language models need large, specialised computers to run, so companies usually rent them as a service rather than running them on their own servers. Amazon's service for hosting and serving AI models is called Amazon Bedrock, and Alexa for Shopping runs on it.

Here is the part people most often get wrong. It is natural to picture one chatbot as one model, a single brain that handles everything. Alexa for Shopping draws on several models, and your espresso question may be handled by a different one than the next question you ask.

The first is Claude Sonnet, a general-purpose model made by Anthropic, another AI company. Bedrock hosts models from several makers, which is how a model from outside Amazon ends up inside an Amazon product.

The second is Amazon's own family of models, called Nova.

The third is a custom model Amazon built for shopping. It uses Amazon's product catalog, customer reviews, the community questions and answers shown on product pages, and information from the web. A model shaped this way is the natural fit for a question like whether two coffee products work together.

Something has to decide which model gets each question. That component is a router: a real-time step that looks at your query, judges what type of query it is, and sends it to one model. Amazon says it chooses so as to balance three things: capability, response time, and answer quality. Routers of this kind usually exist because the most capable model is often the slowest and most expensive, and many questions do not need it; that reasoning is general practice, not something the sources behind this article state about Amazon's router.

Once a model has your question, though, how does it know the price history of one particular espresso machine, which no amount of general training could teach it?

## Grounding the answer and remembering you

You now hold the shape of the front half: your question goes to a router, and the router hands it to one of several models running on Bedrock. A model on its own knows only what it learned in training, which does not include today's price of a $229 espresso machine or what you bought last year.

The fix is to fetch the relevant facts first and hand them to the model along with the question, so it writes its answer from that material rather than from memory. This is called retrieval-augmented generation, usually shortened to RAG: retrieval is the fetching, generation is the writing. Alexa for Shopping uses it.

For your question, the material fetched would plausibly include the machine's listing, its reviews, and what other customers asked about it. For questions about products and trends, Amazon names outside publications as sources too, including The New York Times, Good Housekeeping and Vogue. When an answer is grounded this way, it can be tied to real, current text, which is why assistants of this kind usually use RAG: it cuts down on confident answers that are simply made up.

The second half of your question depends on you, not on the product. For that the assistant keeps what Amazon calls account memory. It is built from your shopping activity, such as past orders, plus details you tell it, such as the members of your family, your pets, or your dietary preferences. Checking compatibility against past orders is one of the things Amazon says it does, so it can look at the grinder in your order history when it answers.

Account memory is visible to you. You can ask the assistant what it remembers and correct it in the conversation, and you can manage your history on a page called Review Alexa History.

With grounded facts and your history, the assistant can tell you the machine fits your grinder and show you that its price over the past 90 days dipped to $189. It answers questions, compares products, shows 30- and 90-day price history, and lists current deals. The next question is the one that matters most for trust: what is it allowed to do about it?

## From answer to action

So the assistant can now answer your espresso question with real facts and your own history behind it. It can also act, and its actions come in steps of increasing independence.

The mildest is adding items to your cart. It can add the espresso machine for you, and it can even read a photo of a handwritten grocery list and add the items on it. You still review what is in the cart before checkout; nothing is bought at this step.

The next is a price alert. You tell it you would buy the machine at $189, and it tells you when the price reaches that target.

The most independent is auto-buy, available to Prime members. Here the assistant watches the price and, when it hits your target, completes the purchase itself using your default payment method and address, then notifies you. You then have 24 hours to cancel at no cost. A single auto-buy request lasts up to six months, so your $189 espresso order would stay on watch until it triggered or six months passed. Amazon says auto-buy customers save an average of 20 percent per purchase.

This is where a second misunderstanding tends to form: that an AI shopping assistant buys freely in the background. In the mechanisms Amazon describes, the assistant completes a purchase on its own only in auto-buy, which you set up with a target price, and even then you are told and given a day to undo it.

The assistant can also reach beyond Amazon. Through a feature called Buy for Me, it can buy items from other brands' websites on your behalf.

It also handles customer service: tracking a package, starting a return or refund, changing an order, and handing you over to a human agent when needed.

Amazon reports the scale: more than 250 million customers used the assistant in 2025, and customers who use it during a shopping trip are over 60 percent more likely to buy on that trip. With all these parts on the table, the obvious next question is how they are wired together.

## What is known about the inside

You have now seen the parts Amazon describes: the router, the models on Bedrock, retrieval, account memory, and the actions. Everything so far comes from Amazon's own announcements or from reporting on them.

How those components connect inside Amazon is not public. No Amazon document describes the internal architecture, so any box-and-arrow picture of it is a guess.

One such guess is a layered architecture diagram produced by another AI assistant, which the sources behind this article include and explicitly label as not Amazon's design. It stacks the system as touchpoints, a gateway layer, language and voice processing, a model core, data services, and a commerce layer. Its broad strokes match the confirmed parts: the places you use it, Bedrock models, RAG over catalog and reviews, user memory, real-time prices for alerts and auto-buy, and the cart and Buy for Me actions. Its specific choices, such as a named event-streaming service and a particular gateway layout, are its own guesses. It also leaves out the one internal component Amazon has confirmed: the router.

The diagram also places a system called COSMO in the core. COSMO is real, published Amazon research, from a 2024 paper. It is a knowledge graph, meaning a large web of facts stored as links between things, here linking what shoppers intend to what products serve that intent. The paper's example links a search for shoes by pregnant shoppers to slip-resistant shoes, through the relation "pregnant requires slip-resistant". The paper says COSMO is deployed in Amazon search. No source says Alexa for Shopping uses it; that link is plausible, since both serve shopping intent, but unconfirmed.

## The whole picture

Alexa for Shopping, formerly Rufus and now part of Alexa+, exists to answer the questions a keyword search cannot, and then to act on the answer. On Amazon's account, a real-time router sends each query to one of several models on Bedrock, retrieval-augmented generation fetches grounding material, account memory supplies your history, and actions run from adding to the cart up to auto-buy with a 24-hour cancellation window. Those parts are confirmed; the order I have walked them in, with retrieval and memory feeding the chosen model, is my reading of how they fit, because the internal wiring is unpublished and the layered diagram is another AI's guess, not Amazon's design.

## Going further

- Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to make the assistant respond faster.
- Shop Direct: the alternative to Buy for Me that sends you to the merchant's own website instead of buying for you.
- COSMO-LM: the fine-tuned language model the COSMO paper uses to generate its knowledge graph, trained on about 30,000 human-annotated instructions and covering 18 major product categories.
- Amazon Lens Live: the camera-based search where the assistant is also available.

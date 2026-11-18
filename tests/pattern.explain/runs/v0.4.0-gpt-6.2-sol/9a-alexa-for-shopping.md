# Alexa for Shopping

You’ll understand how Amazon’s shopping assistant answers a product question, uses what it knows about your purchases, and can act on a price you set.

## A question about something you already own

You need a replacement filter for an air purifier you bought last year. The product listings show a dozen filters that look right, and you’d like to pay $30 or less. To choose one, you need to know which purifier you own, which filter fits it, and whether the price is worth waiting for.

Alexa for Shopping is Amazon’s conversational shopping assistant. You can ask it a question in everyday language and follow up in the same conversation. In the Amazon Shopping app, you could ask, “Which replacement filter fits the air purifier I bought last year?” You can also ask on the Amazon website, where a question typed into the regular search bar can open a conversation.

The phrase “I bought last year” matters. Alexa for Shopping can use past orders to check whether a product is compatible with something you already own. Amazon also calls the information it retains from shopping activity and details you share *account memory*. You can ask what the assistant remembers and correct it in conversation. In this example, the past order gives you a way to refer to the purifier without typing its model number.

Identifying the purifier still leaves a second question. How does the assistant find out which filter fits?

## How it puts an answer together

The past order can identify your purifier. To answer the compatibility question, the assistant also needs information about the filters sold for that model.

Part of the answer comes from a language model, software trained to produce text in response to an input. A model can turn product information into an answer you can read, including a comparison between two filters. Alexa for Shopping uses several models, including one Amazon built for shopping.

Amazon runs those models on Amazon Bedrock, its cloud service for hosting and running AI models. A component called a *model router* chooses which model handles each query. It makes that choice as the query comes in, based on the kind of question and with answer quality and response time in mind. The sources behind this article do not identify which model would handle your filter question.

Alexa for Shopping also looks up relevant information before generating an answer. It gives the material it finds to the model to use when composing the reply. This is called *retrieval-augmented generation*, or RAG. The retrieval is the lookup. The generation is the writing of the answer with the retrieved material in view.

The product catalog, which contains Amazon’s product listings, is one source of that material. Customer reviews and community questions and answers are also among the information Amazon says its shopping model uses. In the filter example, a listing that names compatible purifier models illustrates the kind of evidence a lookup can bring into the answer. The order can tell you which purifier you bought. The listing can tell you which purifier the filter is designed to fit.

That division of work is a way to understand the example from the capabilities Amazon describes. The exact wiring of Alexa for Shopping is unpublished. Amazon’s published research on COSMO describes a knowledge graph, a collection of relationships connecting shopping needs to product features, deployed in Amazon search. A guessed architecture diagram produced by another AI assistant puts COSMO inside Alexa for Shopping. Its use in the assistant is unconfirmed.

Once you have a filter that fits, how much of the purchase can you ask the assistant to handle?

## From an answer to a purchase

You have a compatible filter in mind. Your next question is whether to buy it now or wait until it costs $30.

Alexa for Shopping can show the last 30 or 90 days of price history. If the filter costs $36 today, you can ask what it sold for over the past 90 days. You can also set a price alert at $30. The alert tells you when the price reaches your target, leaving the decision to buy with you.

If you want the filter now, you can ask the assistant to add it to your cart. You review the items in the cart before checkout. A favorable comparison and an item in the cart are both steps you can use to decide what to buy.

If you have Prime, Amazon’s paid membership, you can instead set an *auto-buy* request for $30. With auto-buy, you give permission up front for Amazon to purchase the filter when it reaches your target. A request can stay active for up to six months. If the price reaches $30 while the request is active, Amazon completes the purchase using your default payment method and delivery address. It then notifies you, and you have 24 hours to cancel free of charge.

The distinction matters when you phrase the request. A price alert asks Amazon to tell you when the filter reaches $30. Auto-buy authorizes a purchase at that threshold. The same product and the same dollar amount can lead to two different outcomes.

## The whole picture

Alexa for Shopping lets you carry a shopping decision from an everyday question to an action you authorize. In the filter example, a past order gives you a way to refer to the purifier, product information gives the assistant evidence it can use in a reply, and your $30 target can become either a notification or permission to buy. That is a way to connect Amazon’s published capabilities from the shopper’s side. The model router and retrieval help explain how the assistant produces an answer, while the type of request you make determines what you’re asking Amazon to do with it.

## Going further

- **Rufus** was the assistant’s original name. Amazon renamed it Alexa for Shopping on May 13, 2026.
- **Alexa+** is Amazon’s version of Alexa that uses models to generate responses. Alexa for Shopping is part of it, so a conversation started on an Echo speaker can continue in the shopping app.
- **Review Alexa History** is the page where customers can manage their Alexa history.
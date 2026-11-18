# Alexa for Shopping

You’ll understand how Alexa for Shopping answers a product question, what it can do after you choose an item, and where Amazon’s public account of the system ends.

## A question a search box can’t settle on its own

You need a replacement filter for an air purifier you bought last year. A search for “air purifier filter” brings up dozens of products, some with nearly identical names. Before you can compare prices, you need to know which filters fit the machine you already own.

Alexa for Shopping is Amazon’s assistant for questions and tasks like this. In the Amazon Shopping app, you can ask, “Which replacement filter fits the air purifier I bought last year?” The assistant can check compatibility against past orders. You can refer to a purchase in ordinary language instead of looking up the purifier’s model number before you start.

Amazon calls the information the assistant remembers about you *account memory*. It draws on your shopping activity and on details you tell it. You can ask what it remembers and correct it in conversation. Checking compatibility against past orders is a capability Amazon describes separately. The sources behind this article do not cover whether that check goes through account memory.

The purifier in your order gives the question a specific subject. A filter listing can then provide evidence about whether that filter fits. How does the assistant turn relevant product information into an answer?

## How the assistant puts together an answer

You’ve asked which filter fits a purifier you already bought. An answer needs to connect that purifier with information about a replacement part. The software that generates the wording of the reply is called a *model*.

Alexa for Shopping draws on several models. One is a model Amazon built for shopping. It uses information such as Amazon’s product catalog, which contains the listings for items Amazon carries. Amazon runs the models on Amazon Bedrock, its cloud service for hosting and running them.

When a question comes in, software called a *model router* picks which model handles it. Amazon says the router makes that choice by query type, balancing what the model can do, how quickly it responds, and how good an answer it can produce. The sources behind this article do not identify which model would handle the filter question.

Alexa for Shopping also fetches relevant information and gives it to the model before the model answers. This is called *retrieval-augmented generation*, or *RAG*. Retrieval is the act of finding the material. Generation is the act of writing the reply with that material in hand.

For the filter question, useful material would include a product listing that names the purifier models the filter fits. The model could use that listing to explain why a particular replacement matches. That’s an example of how retrieval could help with this question. The sources behind this article do not trace the information fetched for an individual reply.

It’s easy to use “the model” as shorthand for the whole assistant. In this example, that would hide an important distinction. The model writes the reply. The router chooses a model, and retrieval supplies material for the reply. When you ask the assistant to do something with the filter it found, what have you authorized it to do?

## From an answer to a purchase

You now have a compatible filter in mind. Suppose it costs $36 and you’re willing to pay $30. Alexa for Shopping can show how the price has changed over the past 30 or 90 days. That gives you some context for deciding whether to wait.

You can set a *price alert*, which asks the assistant to notify you if the filter reaches $30. After the alert arrives, the decision to buy is still yours.

You can also ask the assistant to add the filter to your cart. That puts the item where you can review it before you complete the purchase. Asking a question about the filter, adding it to your cart, and checking out are distinct steps.

Amazon’s Prime membership gives you another option called *auto-buy*. With auto-buy, you set the target price and authorize the purchase in advance. If the filter reaches $30 while the request is active, Amazon completes the purchase using your default payment method and delivery address.

An auto-buy request can stay active for up to six months. If Amazon buys the filter, it sends you a notification, and you have 24 hours to cancel free of charge. With a price alert, the notification tells you the price has reached your target. With auto-buy, the notification tells you a purchase has already happened.

The difference is visible in what you authorize and what happens at $30. How much of the system behind those steps has Amazon made public?

## What Amazon has made public

You can follow the filter from a compatibility question to a price decision and, if you authorize it, a purchase. That sequence describes what you can do with the assistant. Amazon’s public descriptions identify some of the components involved, but the internal architecture, meaning how those components are wired together, remains unpublished.

One reason to keep that distinction in mind is COSMO. It is a shopping knowledge graph, a collection of linked facts about what shoppers are trying to accomplish and what product features serve those needs. Amazon’s published research says COSMO is used in Amazon search. Whether Alexa for Shopping uses it is unconfirmed.

A guessed architecture diagram produced by another AI assistant places COSMO alongside the models and leaves out the confirmed model router. Those two details show why a diagram can sound plausible without describing the product’s actual design. For the filter question, the confirmed account supports a narrower conclusion. The assistant can check compatibility against past orders, and it uses retrieval to give models relevant material for their replies.

## The whole picture

Alexa for Shopping brings product questions and shopping actions into the same conversation. In the filter example, you can ask about a purchase you’ve already made, get help finding a compatible replacement, and decide what should happen if the price reaches $30. Behind the reply, a router selects a model and retrieval supplies relevant material. Reading those capabilities together explains the shopping experience, while the exact path from your order history to a particular reply remains outside what the sources behind this article describe.
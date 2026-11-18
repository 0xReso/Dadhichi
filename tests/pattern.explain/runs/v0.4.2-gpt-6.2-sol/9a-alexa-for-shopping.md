# Alexa for Shopping

You’ll understand how a question about a product becomes an answer, how a price instruction becomes a purchase, and what Amazon has made public about the system behind both.

## From a search to a conversation

You need a replacement water filter for the pitcher you bought on Amazon. Several filters look alike, and you’d pay up to $20 for the right one. You could look up the pitcher in your orders, read the filter listings, and keep checking the price. Or you could ask Amazon’s shopping assistant, Alexa for Shopping, “Which replacement filter fits the pitcher I bought?”

You can ask that question in the Amazon Shopping app or on Amazon’s website. On the website, typing a question into the ordinary search bar often opens a conversation with the assistant. That gives you a place to ask a follow-up about the product you’re already discussing, such as “What does it cost today?”

Alexa for Shopping can check compatibility against past orders. In this case, the detail that matters is which pitcher you bought. That detail gives the assistant a way to narrow the question from which filters fit pitchers in general to which filters fit yours.

Amazon calls the information it retains from shopping activity and details you share **account memory**. You can ask what the assistant remembers and correct it in conversation. Amazon describes account memory and compatibility checks as features. The sources behind this article do not describe how a compatibility check looks up a past order.

Once the question is about your specific pitcher, how does the assistant work out what to say about the filter?

## How the assistant builds an answer

Your past order can establish which pitcher you mean. The assistant still needs product information to answer the question about fit.

A program that can take a question and produce a written answer is called a **language model**. Alexa for Shopping draws on several models, including one Amazon built for shopping. That model uses information from Amazon’s listings, customer reviews, questions and answers from shoppers, and the web.

The models run on **Amazon Bedrock**, Amazon’s cloud service for running models and making them available to applications. Alexa for Shopping is the product you interact with. Bedrock provides the service on which its models run.

A component called a **model router** chooses which model handles each question as it arrives. Amazon says the choice depends on the type of question and balances what the model can handle, how quickly it responds, and the quality of the answer. Amazon does not publicly describe which model would handle the filter question.

The assistant also fetches relevant material before answering and gives it to the model to use in its reply. That method is called **retrieval-augmented generation**, or **RAG**. Retrieval is the act of finding the material. Generation is the act of writing the answer with that material at hand.

For the filter question, a product listing that names the pitcher it fits is an example of what would make useful retrieved material. It gives the model something specific to draw on when writing its reply. The listing is illustrative. Amazon describes the retrieval method, while the sources behind this article do not trace the material fetched for an individual answer.

Suppose the reply identifies a compatible filter and it costs $24 today. What can you ask the assistant to do with your $20 limit?

## From an answer to a purchase

You’ve found a filter that fits, and it costs $4 more than you want to pay. Alexa for Shopping can show price history over the past 30 or 90 days. That lets you see whether the filter has reached $20 recently before deciding whether to wait.

A **price alert** is a request to notify you when the filter reaches your target price. Set it at $20 and you can decide whether to buy when you get the alert. An instruction to buy at $20 gives the assistant a different job.

Amazon calls that instruction **auto-buy** and offers it to members of its Prime subscription service. If you set an auto-buy request for the filter at $20, it can watch the price for up to six months. If the price reaches your target while the request is active, it completes the purchase using your default payment method and address.

The purchase comes before the notification. After Alexa for Shopping tells you it bought the filter, you have 24 hours to cancel free of charge. That timing is the practical distinction between the two instructions. A price alert leaves the purchase decision for when you hear from the assistant. With auto-buy, you make that decision when you set the target.

How much of the machinery behind the conversation and the purchase can we actually describe?

## What Amazon has made public

You can describe what the assistant does with the filter question and what happens when the price reaches $20. You can also name some of the components Amazon describes, including the model router. The internal architecture, meaning how those components are wired together, remains unpublished.

Take **COSMO**, a system described in published Amazon research. It links shopping needs to product features that can serve them. The research gives the example of connecting a search for shoes by pregnant shoppers to slip resistance. The paper says COSMO is deployed in Amazon search. Whether Alexa for Shopping uses it is unconfirmed.

A guessed architecture diagram produced by another AI assistant places COSMO alongside the models and leaves out the confirmed model router. That puts the distinction in concrete terms. The evidence supports saying that a router picks a model for your question. The diagram’s placement of COSMO is a guess.

## The whole picture

Alexa for Shopping gives you a way to ask about a product in your own words and, when you choose, give Amazon an instruction to act. In the filter example, a useful way to understand the confirmed features is that your past purchase can help establish which pitcher you mean, retrieved material can help a model explain what fits, and an auto-buy request can turn your $20 limit into a purchase. That is a reading of how the capabilities serve your shopping trip. Amazon describes model selection, retrieval, and purchase behavior, while the internal wiring remains unpublished.
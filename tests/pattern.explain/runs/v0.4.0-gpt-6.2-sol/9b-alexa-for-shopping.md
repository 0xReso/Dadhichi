# Alexa for Shopping

You’ll understand how Alexa for Shopping turns a question into a product answer or a shopping action, and where the public account of how it works ends.

## From search terms to a shopping question

Suppose you need slip-resistant work shoes in a wide fit, and you want to pay no more than $70. You can type a few words into Amazon and work through the results, opening product pages to check which sizes come in wide and which shoes claim to have slip-resistant soles. The hard part is keeping your requirements together while you look.

Alexa for Shopping is Amazon’s conversational shopping assistant. You can give it the requirements in one sentence: “Compare these two slip-resistant work shoes in a wide fit. Are either of them under $70?” Then you can ask a follow-up such as “Is the cheaper pair available in a wide size 9?” The earlier turns give “the cheaper pair” a meaning.

You can type or speak to the assistant. In the shopping app, you can open it from the Alexa icon. On Amazon’s website, a question typed into the ordinary search bar often opens a conversation with it.

The assistant can also draw on details carried across shopping trips. Amazon calls this **account memory**. It includes information from your shopping activity and details you tell the assistant, such as preferences. If you’ve told it you usually wear a wide fit, that’s the kind of detail it can remember. You can ask what it remembers and correct it in conversation.

The conversation gives the assistant your requirements. Where does it get the information it uses to answer?

## How the assistant puts together an answer

Your shoe question gives the assistant something specific to look for. To compare the two pairs, it needs information about the products as well as the words you typed.

A **language model** is the software that uses the question and the material it receives to compose a reply. In the shoe comparison, composing a reply means bringing details about two products together in an answer that addresses your fit, sole and price requirements.

Alexa for Shopping runs its models on **Amazon Bedrock**, Amazon’s cloud service for hosting and serving AI models. The assistant has several models available, including one Amazon built for shopping.

A **model router** chooses which model handles each request. It makes that choice as the request comes in, based on the kind of question and with the aim of balancing what the model can handle, how quickly it replies and how good the answer is. Amazon describes how the router chooses in general. The sources behind this article don’t identify which model would handle this particular shoe comparison.

The assistant fetches relevant material before answering and gives it to the model to use in composing the reply. This is **retrieval-augmented generation**, or **RAG**. Retrieval is the fetching part. Generation is the writing part. In the shoe comparison, a product listing could supply the available widths, while customer reviews could describe how the shoes fit in practice. Those sources answer different questions. A reviewer saying a shoe runs wide tells you something about fit. The listing can tell you whether the shoe comes in a wide size 9.

The assistant is the product you talk to. Model selection and retrieval are two things that product does to produce an answer. Now suppose the comparison turns up a suitable pair at $82. What happens when you ask the assistant to do something about the price?

## When you ask it to act

You’ve found a pair that meets your fit and sole requirements, but it costs $12 more than you want to spend. You can ask to see its price over the past 30 or 90 days. That gives you some context for deciding whether to wait.

You can also set a **price alert** at $70. The request can outlast the conversation. When the price reaches your target, the alert tells you, and you decide whether to buy.

If you’re a member of Amazon Prime, its paid membership program, you can ask for **auto-buy**. Here, setting the target authorizes a purchase. If the shoes reach $70 while the request is active, Amazon completes the purchase using your default payment method and address. It then notifies you, and you have 24 hours to cancel free of charge. The request can stay active for up to six months.

Adding the shoes to your cart is another action. If you ask the assistant to add them, you review the items in the cart before checkout. So the words you use matter. Asking to be alerted at $70 asks for a notification. Asking the assistant to buy at $70, through auto-buy, authorizes an order when the price reaches your target.

You can follow those differences from what happens to the shoe order. How much can you tell about the software underneath?

## What’s known about the internal design

The shoe example takes you from a conversation to an answer and, if you ask, to an action. Amazon has publicly described several parts of that process, including the model router and retrieval. The internal architecture, meaning how the components are wired together, is unpublished.

Amazon has separately published research on **COSMO**, a knowledge graph that records links between what shoppers want and product features that can meet those needs. The research gives an example close to the shoe comparison. It links shopping for shoes during pregnancy with a need for slip resistance. The paper reports that COSMO is deployed in Amazon search. Its use in Alexa for Shopping is unconfirmed.

A guessed architecture diagram produced by another AI assistant places COSMO inside Alexa for Shopping and proposes a particular arrangement for how requests enter and move through the system. That arrangement is speculative, and the diagram leaves out the model router Amazon does describe. Slip resistance is a connection you can see in the published COSMO research. Whether COSMO helped answer your shoe question remains open.

## The whole picture

Alexa for Shopping lets you keep a shopping decision in one conversation, from spelling out what you need to comparing products and deciding what to do. Amazon describes a router that selects a model and retrieval that supplies relevant material before the model writes an answer. It also describes actions the assistant can take at your request. A useful way to connect those capabilities is to follow the shoe decision from your side of the conversation. You give the assistant your requirements, use its answer to identify a pair, and decide whether $70 should trigger a notification or a purchase.

## Going further

- **Rufus** was the assistant’s original name. Amazon renamed it Alexa for Shopping in May 2026 and folded it into Alexa+, its version of Alexa that uses generative AI.
- **Review Alexa History** is the page where you can manage your Alexa history.
- **Buy for Me** lets Amazon purchase an item from another brand’s website on your behalf.
- **Shop Direct** sends you to the merchant’s own website to shop there.
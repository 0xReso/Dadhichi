# Source pack: Alexa for Shopping (compiled 2026-11-15)

Three kinds of material follow, kept separate on purpose. Part A is confirmed by Amazon or by reporting on Amazon's announcements. Part B is published Amazon research. Part C is a guessed architecture diagram produced by another AI assistant; it is not Amazon's design, and nothing in it is confirmed unless it also appears in Part A or B.

## Part A: Confirmed facts

Sources: Amazon's own announcement page (aboutamazon.com, "Amazon's next-gen AI assistant for shopping", updated after May 13, 2026) and Reviewed.com, "How to use Alexa for Shopping" (August 5, 2026).

Name and history
- Amazon launched a shopping chatbot called Rufus. On May 13, 2026, Rufus was renamed Alexa for Shopping and folded into Alexa+, Amazon's generative-AI version of Alexa.
- It shares conversation context with Alexa+ and Echo devices, so a conversation started on an Echo can continue in the shopping app.

Where people use it
- The Amazon Shopping app (an Alexa icon in the navigation bar), the Amazon website, the homepage, product pages, and Amazon Lens Live (the camera-based search).
- On the website, typing a natural-language question into the ordinary search bar often opens a conversation with it.
- Users can type or speak. No Prime membership or Echo device is required to use it.

Models and infrastructure
- It runs on Amazon Bedrock, Amazon's cloud service for hosting and serving AI models.
- It draws on several models: Anthropic's Claude Sonnet, Amazon's Nova models, and a custom model Amazon built for shopping. The custom model uses Amazon's product catalog, customer reviews, community questions and answers, and information from the web.
- A real-time router picks which model handles each query, by query type, to balance capability, response time, and answer quality.
- It uses retrieval-augmented generation (RAG): before answering, it fetches relevant material and gives it to the model to ground the answer. Amazon names publications such as The New York Times, USA Today, Good Housekeeping and Vogue as sources for product and trend questions.
- Amazon says Bedrock features such as prompt caching and parallel tool calling are used to reduce response time.

What it can do
- Answer product questions, compare products, check compatibility against past orders, show 30- and 90-day price history, and list current deals.
- Add items to the cart, including from a photo of a handwritten grocery list. Items in the cart are reviewed by the customer before checkout.
- Price alerts at a target price.
- Auto-buy for Prime members: it watches the price and, when it reaches the customer's target, completes the purchase with the default payment method and address, then notifies the customer, who has 24 hours to cancel free. A request lasts up to six months.
- Buy for Me: it can buy items from other brands' websites on the customer's behalf. Shop Direct instead sends the customer to the merchant's own site.
- Customer service tasks: tracking packages, returns, refunds, order changes, and handing over to a human agent.

Memory
- "Account memory" built from shopping activity, plus details customers tell it (family members, pets, dietary preferences). Customers can ask what it remembers and correct it in conversation, and manage history on a Review Alexa History page.

Numbers Amazon has published
- More than 250 million customers used it in 2025.
- Customers who use it during a shopping trip are over 60 percent more likely to buy on that trip.
- Auto-buy customers save an average of 20 percent per purchase.

Not confirmed anywhere public: the internal architecture. No Amazon document describes how the components are wired together.

## Part B: Published Amazon research: COSMO

Source: "COSMO: A large-scale e-commerce common sense knowledge generation and serving system at Amazon", Amazon Science, SIGMOD 2024.
- COSMO is a knowledge graph of shopping common sense: links between what people intend and what products serve that intent. The paper's example: a search for shoes by pregnant shoppers is connected to slip-resistant shoes through the relation (pregnant, requires, slip-resistant).
- It is built by mining search-then-buy and bought-together behaviour, and generated at scale by a fine-tuned language model (COSMO-LM) trained on about 30,000 human-annotated instructions. It covers 18 major product categories.
- The paper says COSMO is deployed in Amazon search, for search relevance, session-based recommendations and search navigation.
- Not confirmed: that Alexa for Shopping uses COSMO. It is plausible, since both serve shopping intent, but no source says so.

## Part C: A guessed architecture (produced by another AI, not Amazon)

The diagram proposes these layers, top to bottom:
1. Touchpoints: mobile app, web, Echo (voice), search bar.
2. API gateway and ingestion: API gateway, request ingestion, event streaming (Amazon Kinesis), authentication and rate limiting.
3. Two parallel front ends: natural language and voice processing (speech-to-text, intent and entity detection, multilingual processing), and search-bar interception for AI overviews (query understanding, AI summaries, intent routing).
4. A conversational and intent core: Bedrock models plus the COSMO knowledge graph.
5. Three data services: a catalog and RAG engine (product catalog; documents, reviews, policies, FAQs), user memory and profile (preferences, session memory, personalisation), and a price and inventory database (real-time price, availability, offers).
6. Action and commerce orchestration: add to cart, add to list, Buy for Me, checkout.

Which parts line up with Part A: the touchpoints, Bedrock models, RAG over catalog and reviews, user memory, real-time price for alerts and auto-buy, and the cart and Buy for Me actions. Which parts are the diagram's own guesses: Kinesis, the specific gateway layout, COSMO inside the core, and the separation into these exact boxes. The diagram also omits the confirmed model router.

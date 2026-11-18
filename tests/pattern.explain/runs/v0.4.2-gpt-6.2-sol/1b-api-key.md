# What an API key is

You’ll understand what an API key tells a service, how a program uses it, and why a secret key needs to stay private.

An online shop wants to show customers when their orders will arrive. It can ask a shipping service for an estimate every time a customer checks an order. The shipping service needs a way to recognise which shop is asking, so it can apply that shop’s access rules and count its requests.

The shipping service publishes a set of instructions that tell the shop’s software what it can ask for and how to ask. That published interface is called an application programming interface, or API. For a delivery estimate, the API might tell the shop to send a destination postal code and specify how the estimate will come back.

To recognise the shop, the shipping service issues it a string of letters and numbers called an API key. In this example, the service links the key to the shop’s account. The shop stores the key where its own software can read it.

When you check delivery to postal code 560001, the shop’s software sends the postal code and its API key to the shipping service. The postal code tells the service where the parcel is going. The API key tells it which account the request belongs to. The service checks that the key is active and that the account can request estimates. If those checks pass, it sends back an estimate, say three days, and the shop displays it to you.

The shipping service has recognised the shop’s account. It hasn’t learned who you are from the API key. Every customer who checks a delivery estimate through that shop can trigger a request with the same key. The shop can have its own way to identify a signed-in customer, but that is a separate exchange.

In this example, the API key is a secret. The shipping service accepts possession of a valid key as evidence that a request belongs to the shop. If someone copies the key, they can send requests that the service counts against the shop’s account, within whatever permissions the key carries. That’s why the shop keeps the key in the software running on its own computers and sends your browser the estimate without including the key.

Some services use API keys in other ways, including keys meant to appear in a browser and keys that must be sent alongside another proof of identity. A service’s documentation tells you what access its key carries and where it can safely be used.

## Going further

- **Key rotation** means replacing a key in the software that uses it and disabling the old one.
- **Scopes** are named permissions that limit which operations a key can be used for.
- **Rate limits** cap how many requests a service accepts in a given time.
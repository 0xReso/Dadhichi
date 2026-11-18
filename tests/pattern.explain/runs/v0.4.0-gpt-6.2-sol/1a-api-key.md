# What an API key is

You’ll understand what an API key identifies, what happens when you send one, and why you need to keep it private.

Your shop’s website needs a delivery quote before it can show a customer the total at checkout. The delivery company offers a way for the shop’s software to ask for that quote automatically. The published rules for making the request and reading the reply are called an application programming interface, or API.

The delivery company needs to know which shop account to charge for each quote request. When you set up the integration, the company gives you a string of characters to include with your requests. That string is an API key. You save it in your shop’s server settings, where the software that asks for delivery quotes can read it.

At checkout, your server sends the parcel weight and destination to the delivery company. It includes the API key in the request, usually in a *header*, a named field that carries information alongside the request. The delivery company tells you which field to use.

When the request arrives, the delivery company checks the key against its records. If the key is active and can be used to request quotes, the company can return a price, say £4.50, and count the request against your shop’s account. If the key is missing or invalid, the company rejects the request.

The key tells the delivery company which account to associate with the request. The customer’s identity is a separate matter. The same shop key can go out for every checkout, and the delivery company can accept it without knowing which customer clicked the button.

That also means someone who copies the key may be able to make requests that count against your account. Keep a private key on your server. If you put it in code that runs in a customer’s browser, anyone who receives that code can inspect it. If a key is exposed, you can *revoke* it, which tells the delivery company to stop accepting it, and set up a replacement for future requests.

## Going further

- **Key scope** limits what a key can do, such as requesting quotes without buying shipping labels.
- **Rate limit** caps how many requests can be made in a period, such as 60 per minute.
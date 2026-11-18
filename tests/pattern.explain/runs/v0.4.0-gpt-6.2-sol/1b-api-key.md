# What an API key is

You’ll understand what an API key tells a service, why a program sends one, and what happens if someone copies it.

A shop’s website can ask a delivery service what it would cost to ship an order. The delivery service needs a way to tell which customer account is making the request. Otherwise, it would have no account to count the request against.

The delivery service publishes rules that tell the shop’s software what to send and what it can expect back. Those rules are an application programming interface, or API. For a shipping quote, the API might tell the shop where to send the parcel’s weight and destination and how to read the price the service returns.

To connect those requests to the shop’s account, the delivery service issues the shop a string of characters called an API key. The service keeps a record of which account the key belongs to, and the shop configures its software to send the key with each request for a quote.

Suppose you’re buying something from the shop and enter your delivery address. The shop’s software sends the delivery service the destination, the parcel’s weight of 2 kilograms, and the shop’s API key. The service looks up the key and finds the shop’s account. If the key is valid and the account can request quotes, the service calculates the price and sends it back. If the key is missing or invalid, the service can turn down the request before calculating anything.

The account the delivery service finds belongs to the shop. You supplied the address, but the key came from the shop’s software. The key tells the delivery service which account to count the request against. If the shop needs to know who placed the order, it handles that separately through its own sign-in.

That lookup also explains why the shop has to keep this kind of key secret. If the delivery service accepts the key by itself, anyone who copies it can send requests that the service counts against the shop’s account. Those requests could use up the shop’s allowance or add to its bill. If the shop disables the key, the delivery service will reject requests that still carry it, including requests from the shop’s own software.

What a key can do varies by service. Some services let you restrict a key to particular operations, such as asking for quotes. Some issue keys designed to appear in a website and use them to identify the project making the request, with separate checks for sensitive operations. The service’s rules tell you what possession of its key lets someone do.
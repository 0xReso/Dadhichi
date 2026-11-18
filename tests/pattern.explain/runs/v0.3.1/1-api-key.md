# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one travels with each request, and the mistake people most often make with them.

Say Priya is building a small app that shows tomorrow's forecast. She doesn't run weather stations, so her app asks a weather company's computers for the data. The weather company publishes a set of addresses and rules that other programs can use to ask for forecasts. That published way for one program to ask another to do something is called an API, short for application programming interface. Priya's app sends a request to the API, something like "forecast for Lisbon, tomorrow", and the weather company's server sends back a response with the numbers.

The weather company has a problem, though. Thousands of apps send it requests, and it wants to know which app sent each one. It needs that to apply limits, so that one app sending a flood of requests can't slow things down for everyone else. It also needs it for billing, and so it can switch off an app that misbehaves. Asking each app for a username and password on every request would be clumsy, because no person is there to type them in. A program needs something it can attach without help.

So when Priya signs up, the weather company gives her a long random string, perhaps 32 characters of letters and digits. That string is an API key. Her app attaches it to every request, usually in a header (a labelled line of extra information sent along with the request) and sometimes inside the web address itself. When a request comes in, the server looks the key up in its records and finds Priya's account. It checks that she is still under her limit of, say, 1,000 requests a day, adds one to her count, and sends the forecast back. A request with no key, or with a key the server doesn't recognise, is turned away.

Notice what the key identifies: Priya's app, or more precisely her account. It does not identify the person holding the phone. Every user of her app sends the same key. That is the key difference from logging in, which proves who a particular person is.

This leads to the most common mistake. An API key works like a password for the account it belongs to: anyone who has it can make requests that count against Priya's limit and her bill. If she puts the key inside her phone app or a web page, it is not hidden. Anyone curious enough can pull it out of the app's files or watch it go by in their browser's network tools. Developers usually handle this by keeping the key on a server of their own, which makes the call to the weather company for the app, or by limiting what the key is allowed to do. If a key leaks anyway, the fix is to revoke it, which tells the service to stop accepting it, and issue a new one.

## Going further

- **Key rotation**: replacing keys on a regular schedule, so a leaked key stops working before much harm is done.
- **Scopes**: permissions attached to a key that limit which parts of an API it may use.
- **OAuth**: a standard way for an app to act for a specific user, with that user's permission, instead of using one shared key.
- **Secrets manager**: a service for storing keys and passwords outside of program code.

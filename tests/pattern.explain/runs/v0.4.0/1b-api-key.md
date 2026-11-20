# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one travels with each request, and the mistake that leaks most of them.

Programs often ask other programs for help. A shop's website that shows the local forecast does not measure the weather itself. It sends a question to a weather company's servers, and they send back the answer. The published way one program asks another to do something is called an API, short for application programming interface.

That arrangement leaves the weather company with a problem. Its servers cost money to run, and anyone on the internet can send them questions. It needs to know which customer each request comes from, so it can count usage, bill for it, cap it, and shut off anyone who abuses it.

The answer is to give each customer, at sign-up, a long random string of around forty letters and digits that nobody could guess. That string is the API key. It works as a name tag for an account: every request carrying it is counted against that account.

Here is the exchange in practice. When your shop's server asks for tomorrow's forecast, it attaches the key to the request, usually in a header, a labelled field that travels alongside the request rather than in the visible web address. The weather company looks the key up, finds your account, checks that you have not passed your plan's limit of, say, 10,000 requests a month, adds one to your count, and sends the forecast. A missing or unknown key gets a refusal instead. The request goes over HTTPS, the encrypted form of the web's request language, so nobody watching the network can read the key on the way.

Notice what the key does not say. It identifies your shop's account, not the person browsing your website. A key answers "whose bill is this?" rather than "who is this human?", and logging people in is a separate job handled by other means.

This is where most trouble starts. Because the key is the only thing the weather company checks, whoever holds it is treated as you. A copied key lets a stranger run up your bill or exhaust your monthly limit, and the service cannot tell their requests from yours. An API key is, in effect, a password for your account that never expires on its own.

The common mistake is to put the key in code that runs on the visitor's own device: a web page's scripts or a phone app. Anything sent to a browser can be read by anyone who opens the page's source, and app files can be unpacked. The same goes for code pushed to a public repository, where automated scanners commonly find keys within minutes. The safe pattern is to keep the key on your own server. The visitor's browser asks your server for the forecast, and your server, holding the key out of sight, asks the weather company. If a key does leak, you delete it in the provider's dashboard and issue a new one; the old one stops working at once.

## Going further

- **Key rotation**: replacing keys on a schedule so a quietly leaked one has a short life.
- **Key restrictions**: settings many providers offer that limit a key to certain websites, server addresses, or features.
- **Environment variables and secrets managers**: ways to keep keys out of code files entirely.
- **OAuth tokens**: short-lived credentials that act on behalf of a specific logged-in user rather than an account.

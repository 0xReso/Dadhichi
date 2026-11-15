# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one is checked on every request, and the mistake that gets most of them stolen.

Say you are building a small app that suggests cycling routes. You want it to warn riders about rain, but you are not going to run your own weather stations. A weather company already has the forecasts, and it offers to let your app ask for them. The company has a problem, though. Thousands of programs will be asking, and it needs to know which one is which. Some have paid for heavy use, some are on the free plan, and some are misbehaving and need to be cut off. The company has to put a name on every request that arrives, without a person typing a password each time.

An API key solves that problem. It is a long, random string of characters that a program sends along with each request, so the service can tell which account the request belongs to.

To see where the key fits, start with the thing it unlocks. An API is the published way one program asks another to do something. The weather company's API says, in effect: send a request to this web address, name a city, and you will get back the forecast as structured data your program can read. Your app sends a request, the company's server sends a response, and no human looks at either. That last point matters. A login page can ask a person for a password. An API is called by code, often hundreds of times a minute, so the proof of identity has to travel inside the request itself.

That proof is the API key. When you sign up on the weather company's website, you open its dashboard, the account page where developers manage their access, and click a button to create a key. The server generates a long string of random characters, something like wx_live_ followed by forty letters and digits, and shows it to you. Behind the scenes it records that this string belongs to your account, on the free plan, which allows 1,000 requests a day. Many providers show you the full key only once and keep just a scrambled fingerprint of it, so if you lose it you create a new one rather than look the old one up.

From then on, your app attaches the key to every request it sends. Usually it goes in a header, a labelled line of extra information that travels with the request but is not part of the address. The header might be called X-API-Key, or Authorization; each provider says which in its documentation. A request from your app then reads, roughly: give me tomorrow's forecast for Bristol, and here is my key.

When that request reaches the weather company's server, a short sequence of checks happens before any forecast is fetched.

1. The server reads the key from the header and looks it up. If no account matches, the request is refused straight away.
2. It checks that the key is still active. A key you deleted last week counts as no key at all.
3. It checks what this key is allowed to do. A free-plan key might be allowed current forecasts but not ten years of historical data.
4. It checks the count. If your app has already made its 1,000 requests today, the server refuses with a message that says, in effect, too many requests, try later.
5. Only then does it fetch the forecast, send it back, and add one to your tally.

All of this takes a few milliseconds, far too fast for anyone to notice, and it happens on every single request.

Those checks are two different jobs that are easy to blur together. The first is authentication: working out who is calling. The rest are authorization: deciding what that caller may do. An API key carries the answer to the first question, and the server's records about that key answer the second. This is also why the key is so useful to the company. Because every request carries it, the company can count usage per account, bill the customers who go past their free allowance, and spot an account that is suddenly hammering the service.

Now comes the part that matters most in practice. The server has no way to know who is holding the key. It sees the string and nothing else. Anyone who has a copy of your key looks, to the weather company, exactly like your app. A credential that works for whoever presents it is called a bearer credential, the way a concert ticket works for whoever is holding it at the door. That analogy holds for the mechanism; where it breaks is that a ticket is used once, while a stolen key keeps working on every request until someone switches it off.

So the key is a secret, as serious as a password, and it has to be treated like one. That leads to the most common misunderstanding about API keys.

Picture the cycling app built in the most direct way: the app on each rider's phone calls the weather API itself, with the key written into its code. It feels hidden. The key is buried in the program, riders never see it, and the app is compiled into a form people cannot read. But anything shipped to a user's device can be read by a determined user. Tools for pulling text strings out of an app take minutes to use. In a website it is even easier: the browser has to receive the key in order to send it, so anyone can open the browser's developer tools and watch it go past. A key placed in code that runs on someone else's machine is not hidden; it is published.

The same thing happens with code repositories. Developers often paste a key into their source code while testing, then upload the project to a public repository. Automated programs scan public repositories around the clock looking for strings shaped like keys, and leaked keys are commonly found and abused within minutes. If the key is tied to a paid plan, the abuse lands on your bill.

The fix is to keep the key somewhere only you control. In the cycling example, the phone app talks to a small server that you run, and your server talks to the weather company. The key lives on your server, never on the riders' phones. Even on that server, it is kept out of the source code, usually in an environment variable, a named setting the operating system hands to a program when it starts, so the code can read the key without the key ever being written into a file that gets shared.

Leaks still happen, so providers give you two more controls. You can revoke a key, which tells the server to treat it as unknown from that moment on; every copy of it, wherever it has spread, stops working at once. And you can rotate keys, which means creating a new key, switching your server over to it, and then revoking the old one. Doing this on a schedule limits how long a key that leaked without your noticing stays useful.

One more point keeps people from expecting too much. An API key does not encrypt anything. It is a string sent inside the request, and if the request travelled in plain form, anyone watching the network could copy it. What protects it on the way is HTTPS, the encrypted version of the language browsers and servers use to talk, which scrambles the whole request, key included, between your server and the weather company's. The key says who you are; HTTPS keeps people from overhearing it. Reputable APIs refuse plain, unencrypted requests for exactly this reason.

It also helps to know what an API key does not identify. It names your app or your account, not the rider using the app. The weather company has no idea whether one person or ten thousand are behind your requests; it sees only your key. That is fine for a weather forecast, which is the same for everyone. It is not enough when an app needs to act for a particular person, such as reading their calendar, and services use a different system for that.

## The whole picture

An API is how one program asks another for something, and because no person is there to type a password, each request has to carry its own proof of who sent it. The API key is that proof: a long random string the service issues to your account and looks up on every request, first to recognise you, then to check what you may do and how much you have used. Because the server sees only the string, whoever holds the key is you, so its whole value depends on keeping it secret, which means keeping it on a server you control, out of shared code, sent only over HTTPS, and revoked the moment it might have escaped.

## Going further

OAuth 2.0: the standard system services use when an app must act on behalf of a specific person, issuing short-lived access tokens instead of one permanent key.

Key restrictions: provider settings that limit a key to certain addresses, websites, or features, so a leaked key is less useful to whoever finds it.

Publishable and secret keys: some providers, such as payment companies, issue a low-power key that is safe to put in a website alongside a full-power key that must stay on your server.

Secrets managers: services that store keys centrally, control who can read them, and help automate rotation.

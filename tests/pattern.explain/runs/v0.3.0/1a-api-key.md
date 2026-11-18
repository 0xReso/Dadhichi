# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one travels with a request, and the mistake people most often make with it.

Suppose you are building a small travel app that shows the weather at each stop on a trip. You do not run weather stations, so your app asks a weather company's servers for forecasts. The company publishes a fixed way for programs to ask: which address to send a request to, what to put in it, and what comes back. That published way of asking is called an API, short for application programming interface.

The weather company has a problem. Its servers cost money to run, and anyone on the internet can send them requests. It needs to know which program is asking, so it can bill the right account, cap how much each one uses, and cut off one that misbehaves. A login screen does not help, because no person is typing; one program is talking to another.

The answer is a long random string the company generates for you when you sign up, often thirty to forty letters and digits. That string is called an API key. Your app attaches it to every request, usually in a header, a labelled line of extra information that travels ahead of the request's content, though some services accept it as part of the web address instead. When the weather server receives "forecast for Lyon, please" along with your key, it looks the key up, finds your account, checks that you are still under your allowance of, say, 1,000 requests a day, counts this one, and sends the forecast back. A request with no key, or a key it does not recognise, is refused.

Notice what the key identifies: the program, not the person using it. Every traveller on your app sends the same key, so the weather company sees one customer, you. Telling individual users apart is a separate job, usually done with logins and short-lived tokens.

Because anyone holding the key can spend your allowance and run up your bill, the key is a secret, as sensitive as a password. Here is where people go wrong. Many developers paste the key straight into their app or webpage, assuming it is hidden there. It is not. Anything shipped to a user's phone or browser can be read by someone determined enough, and keys are routinely pulled out of published apps and public code. The usual practice is to keep the key on a server you control: your app asks your server, and your server adds the key and asks the weather company, so the key never leaves your hands.

If a key leaks anyway, providers let you revoke it, which means switching it off so it stops working at once, and then issue you a fresh one to put in its place.

## Going further

- Key restrictions: settings that limit a key to certain actions, apps, or web addresses, so a leaked key does less damage.
- Rate limiting: how services enforce allowances like 1,000 requests a day, and what they send back when you go over.
- HTTPS: the encrypted form of web traffic; keys should only ever travel over it, so they cannot be read on the way.
- OAuth: a standard for letting a person grant an app access on their behalf, used when the service needs to know which user is acting, not only which program.

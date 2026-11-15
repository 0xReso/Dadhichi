# What an API Key Is

By the end, you will know what an API key does, why services hand them out, and the mistake that most often gets one stolen.

Say you are building a small app that shows the weather, and you have no intention of running your own weather stations. A company, call it SkyData, already collects forecasts and lets other programs ask for them. The published way one program asks another to do something is called an API, short for application programming interface. Your app sends SkyData a request ("forecast for Lisbon, please") and SkyData sends back a response with the numbers.

SkyData has a problem, though. Its servers cost money, and anyone on the internet can send it requests. It needs to know which program is asking, so it can count usage, enforce limits, and bill the right customer.

So when you sign up, SkyData gives you a long random string, around forty letters and digits. Your app attaches that string to every request, usually in a header, a labelled line of extra information that travels alongside the request. SkyData looks the string up, finds your account, and answers. That string is an API key.

With the key in place, SkyData can do what it needed. It can let your free plan make 1,000 requests a day and refuse the 1,001st; a cap like this is called a rate limit. It can show you how many calls your app made this month. Many services also let you restrict a key, for example to reading forecasts only, so that even a misused key can do limited damage. And if something goes wrong, SkyData can switch off your key without touching anyone else's.

Here is where people commonly go wrong. An API key identifies a project, not a person, and it proves nothing beyond possession. When SkyData receives your key, it learns only that the request came from something holding your key. Whoever has the string is, as far as SkyData can tell, you, and your bill grows with their requests. That makes the key far closer to a password than to a name tag, and it needs guarding like one.

The key itself is usually not scrambled in any way; it travels as plain text inside the request. It stays private in transit only because the connection is encrypted, which is what HTTPS, the secure form of the language browsers and servers speak, provides.

The usual way keys leak is through code that ends up on other people's devices. If you put the key inside your phone app or a web page's code, anyone who downloads it can dig the string out in minutes. Keys also leak when developers publish their code online with the key still in it; automated scanners comb public code for exactly these strings, often within minutes of it appearing. The fix is to keep the key on a server you control. Your app asks your server, and your server, holding the key out of sight, asks SkyData.

When a key does leak, you revoke it, which tells the service to stop accepting it, and create a new one. Replacing keys on a schedule, even when nothing has gone wrong, is called rotation, and it limits how long any stolen key stays useful.

## Going further

OAuth: a standard for letting a user grant an app limited access to their account, used when the service needs to know which person is acting, not only which app.

Scopes: the named permissions attached to a key or token, such as read-only access.

Secret manager: a service that stores keys for your servers so they never sit in your code.

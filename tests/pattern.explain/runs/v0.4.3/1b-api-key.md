# What an API Key Is

By the end you will know what an API key is, the job it does, and the mistake people most often make with one.

Suppose you are building a small travel app that shows the weather at each stop. You do not run weather stations, so your app asks a weather company's computers for every forecast. That company has a problem of its own: thousands of programs are asking it questions every second, and it needs to tell them apart, so it can count each one's requests, cap the free ones, and send the right bill to the right customer.

Your app asks through an API, the published set of requests one program can make of another. The weather company's API might accept a request that means "forecast for Lisbon, tomorrow" and send back the temperature and the chance of rain.

When you sign up, the company gives you a long random string, around forty letters and digits, made for your app alone. That string is called an API key. Your app attaches it to every request it sends, so each question arrives carrying the same tag.

When the request for Lisbon arrives, the server reads the key, looks it up in its records, and finds your account. Say you are on a free plan of 1,000 requests a month and have used 312. The key is known and there is room left, so the server answers and your count becomes 313. Had the key been unknown, cancelled, or over its limit, the server would have refused with an error instead of a forecast. That lookup is the whole mechanism: the key says "this request belongs to that account."

Here is where people go wrong. An API key feels like a password, but it proves nothing about who is holding it. The server cannot tell your app from anyone else who has copied the string; whoever presents the key is treated as you, and their requests land on your count and your bill. So the key is only as secret as the place you keep it. Put it inside the app people download, or in web page code that runs in their browser, and anyone curious can dig it out in minutes. Keys pasted by accident into publicly shared code are routinely found by automated scanners. The usual safer pattern is to keep the key on a server you control: your app asks that server, and the server adds the key before passing the request on to the weather company.

If a key does leak, you cancel it in the provider's account settings, which providers call revoking it, and issue a new one. Because the key is a random string with no meaning of its own, replacing it costs nothing beyond updating the one place it is stored.

## Going further

- Rate limiting: the provider's rules on how many requests a key may make per second or per month, and what happens when you exceed them.
- Key restrictions: settings many providers offer that make a key work only from certain servers, websites, or parts of the API, so a stolen copy is less useful.
- OAuth: a standard way for a person to let an app act on their account without handing over their password, used when requests are made on behalf of a user rather than an app.
- Environment variables: a common way to give a program its key at start-up without writing the key into the program's code.

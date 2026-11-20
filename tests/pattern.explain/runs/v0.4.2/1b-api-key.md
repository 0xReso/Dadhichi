# What an API Key Is

By the end you will know what an API key is, why services hand them out, how a service uses one, and the mistake that gets most of them stolen.

Say you are building a small travel app and want it to show the weather at each destination. You are not going to put up weather stations around the world. A weather company already has the data and lets other programs ask for it over the internet. A published way for one program to ask another for something like this is called an API, short for application programming interface. Your app sends a question such as "forecast for Lisbon tomorrow", and the company's server sends back the answer as data your app can display.

That arrangement leaves the weather company with a problem. Its servers cost money to run, and anyone on the internet could send them questions. It wants to know which program is asking, so it can count each customer's use, charge for it, and cut off anyone who abuses it.

So when you sign up on the company's website, it gives you a long random string of letters and digits, often thirty or forty characters, far too long to guess. Your app attaches that string to every question it sends. That string is called an API key.

When a question arrives, the server reads the key and looks it up in its records to find your account. If the key is unknown or has been switched off, the server refuses with an error. If the key is valid, it answers and adds one to your count for the day.

That count lets the company enforce a rate limit, a cap on how many questions one key may ask in a given time. If your free plan allows a thousand forecasts a day, the thousand-and-first is refused until the count resets.

Notice what the key does not prove. It identifies your app's account, not the person holding the phone. Anyone who has the string can send it, and the server will treat them as you. An API key behaves like a password sent with every request, which is why services expect it to travel over HTTPS, the encrypted connection browsers use, so nobody on the network can read it in transit.

This is where most people go wrong. It is tempting to paste the key straight into the app's code. But code that runs on your users' phones or in their browsers carries the key with it, and anyone curious can dig it out in minutes. A stranger can then run up your bill or use up your limit, and the company sees only your key. The usual fix is to keep the key on a server you control: your app asks your server, and your server, which holds the key, asks the weather company.

If a key does leak, you revoke it on the company's website, which switches it off for good, and create a new one. Since the key is a random string rather than anything tied to who you are, replacing it means updating it in one place.

## Going further

- Key rotation: replacing keys on a schedule, so a leaked key stops working even if nobody noticed the leak.
- Scopes: restrictions placed on a key, such as read-only access or use from certain addresses alone.
- OAuth: a standard that lets a person grant an app access on their behalf, used where a service needs to know which person is acting rather than which app.
- Secrets manager: a service that stores keys for servers so they never sit in code files.

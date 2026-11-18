# What an API key is

By the end you will know what an API key is, why services hand them out, and the mistake that leaks most of them.

Say you are building a small app that shows the local forecast, and you want the numbers from a weather service rather than collecting them yourself. The service offers an API, the published way one program asks another to do something: your app sends a request such as "current weather for Leeds" to the service's address, and the service sends back the answer as data.

The service has a problem. Thousands of programs send it requests, and it needs to tell them apart: to count how many requests each one makes, to stop any one from flooding it, and to bill the ones on a paid plan. A request on its own carries no name.

So when you sign up, the service gives you a long random string, around forty letters and digits, and records it against your account. That string is called an API key.

Your app attaches the key to every request, usually in a header, a labelled line of extra information that travels alongside the request itself. When the request for Leeds arrives, the service reads the key, looks it up, and finds your account. Then it checks what your account allows: say the free plan permits 1,000 requests a day. If this is request 412, the forecast comes back. If the key is unknown, or this is request 1,001, the service refuses and sends an error instead of the weather.

Notice what the key does and does not prove. It identifies a program or a project, not a person: the service has no idea who is holding the phone running your app. And whoever presents the key is treated as you, with no second check, much like a ticket that admits whoever carries it.

That is where most people go wrong. It is tempting to believe a key tucked inside an app or a website's code is hidden. It is not. Anyone can view a webpage's code in their browser, and an app's files can be unpacked and searched. A stranger who copies your key can spend your 1,000 daily requests, or run up your bill on a paid plan. Keys also leak when developers publish their code online with the key still written into it.

The usual practice is to keep the key on a server you control. Your app asks your server for the Leeds forecast; your server adds the key, asks the weather service, and passes the answer back. The key never sits anywhere the public can reach. Many services also let you limit what a key can do, and let you cancel it and issue a fresh one if it does leak.

## Going further

- OAuth: a standard for when a service needs to know the person, not only the app, letting a user grant an app access to their own account.
- Key rotation: replacing keys on a regular schedule, so a leaked one stops working on its own.
- Environment variables: a common way to give a server its keys without writing them into the code.

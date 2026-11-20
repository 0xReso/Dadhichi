# What an API Key Is

By the end you will know what an API key is, why services hand them out, and the mistake that leaks them.

Suppose you are building a small app that shows tomorrow's forecast. You don't run weather stations, so your app asks a weather service for the data. That service answers thousands of programs a minute, and it needs to know which program each question came from. Without that, it can't stop one runaway program from swamping everyone else, or tell a free user from a paying customer.

Your app asks its questions through an API, the published way one program asks another to do something. Here the weather service has said, in effect, "send a request to this address naming a city, and I'll send back the forecast." Your app's request goes out over the internet and the response comes back, with no person involved at either end.

When you sign up for the weather service, it gives you a long random string, something like forty letters and digits that mean nothing on their own. You put that string into your app, and the app sends it along with every request, in a labelled field the service knows to look for. That string is called an API key.

When a request arrives, the service reads the key and looks it up in its own records. It finds that the key belongs to your project, on the free plan, which in this example allows 1,000 requests a day. It adds one to today's count. If you are under the limit, you get the forecast. If this is request number 1,001, the service refuses and sends back an error saying the limit has been reached. A request with no key, or one the service doesn't recognise, is refused outright. That single lookup is the whole mechanism: the key says which project is asking, and the service decides what that project is allowed to do.

That is also where people go wrong. An API key feels like a password tied to you, but the service never checks who is holding it. Anyone who sends your key is treated as your project, and the requests count against your limit or your bill. So the key must stay somewhere only your own code can read it. The common mistake is to put it inside the app you ship to users, or into a public code repository. Anyone can dig a string out of an installed app or a web page's code, and automated scanners search public code for keys all day. If a key does leak, the fix is to delete it in the service's dashboard and issue a new one, because a key can't be made secret again once it is out.

## Going further

- **Key restrictions**: settings on many services that let a key work only from certain addresses, apps, or parts of the API, limiting the damage if it leaks.
- **Key rotation**: replacing a key with a new one on a schedule, so an old leaked copy stops working.
- **Secrets manager**: a service that stores keys and passwords away from your code and hands them to your program when it runs.
- **OAuth**: a different scheme in which a program acts on behalf of a specific person who approved it, rather than identifying only a project.

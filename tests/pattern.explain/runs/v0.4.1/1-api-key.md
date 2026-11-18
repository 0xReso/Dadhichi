# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one travels with every request, and the mistake that most often leaks one.

A weather company runs a service that other programs can ask for forecasts. A travel app sends the question "what will the weather be in Lisbon tomorrow?" and gets an answer back in a fraction of a second. The published way one program asks another to do something like this is called an API, short for application programming interface.

The weather company has a problem. Anyone on the internet could send it those questions, and every answer costs it computing time. It wants to know which customer each request comes from, so it can bill them, cap how much they use, and cut off anyone abusing the service. A username and password do not fit well here, because no person is typing anything: one program is talking to another, thousands of times a day.

So when you sign up as a developer, the company gives your project a long random string, perhaps forty letters and digits that look like noise. That string is an API key. Your program attaches it to every request it sends, and the string means "this request comes from that customer's project".

The key usually travels in a header. A header is a labelled line of extra information sent along with a request, separate from the question itself, and the person using the travel app never sees it.

When the request arrives, the weather server looks the key up in its records and finds your account. It checks that you have not used up your allowance, say 1,000 requests a day on the free plan, adds this request to the count, and sends the forecast. If the key is missing, unknown, or has been cancelled, the server refuses and replies with an error instead of a forecast.

Here is where people go wrong. An API key identifies a project, not a person, and the server cannot tell who is holding it. Anyone who copies the string looks exactly like you, and their requests use your allowance and land on your bill. The common mistake is to put the key inside code that ships to users, such as a phone app or the script of a web page. Anything delivered to someone's device can be read by that someone, and keys accidentally published in public code are found by automated scanners, often within minutes. The usual practice is to treat the key like a password and keep it on a server you control: the travel app asks your server, and your server adds the key and asks the weather service. Some providers do issue keys designed to sit in public web pages, made safer by locking them to one website, so it is worth checking what a given provider intends.

Because a key is only a string, it is easy to replace. If one leaks, you cancel it in the provider's dashboard and generate a fresh one, and the copied string stops working at once.

## Going further

- Key rotation: replacing keys on a regular schedule, not only after a leak.
- Rate limiting: how services enforce allowances such as requests per minute.
- OAuth access tokens: short-lived credentials that act on behalf of a specific user, unlike a project-wide key.
- Secret managers and environment variables: common places to store keys outside your code.

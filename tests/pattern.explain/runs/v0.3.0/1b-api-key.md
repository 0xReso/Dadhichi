# What an API Key Is

By the end you will know what an API key is, why services hand them out, how one travels with a request, and the mistake that gets keys stolen.

Say Priya is building a small travel app that shows the forecast for the user's next stop. She doesn't run weather stations, so her app asks a weather company's servers for the data. It does this through an API, the published way one program asks another to do something: her app sends a request such as "forecast for Lisbon, next three days" and gets the answer back as data rather than as a web page.

The weather company has a problem with this. Its servers cost money to run, and anyone on the internet can send them requests. It needs to know which program is asking, so it can let in the ones that signed up, count how much each one uses, and shut off any that misbehave.

So when Priya signs up, the company gives her a long random string, something like forty letters and digits, that nobody could guess. That string is called an API key. Her app attaches it to every request, usually in a request header, a labelled field that travels alongside the request but isn't part of the question itself. When a request arrives, the company's server looks the key up in its records, finds "Priya's travel app, free plan, 1,000 requests a day", and decides from that whether to answer. Her app has already made 200 requests today, so the forecast comes back. Once it reaches 1,001, the server refuses until tomorrow.

Notice what the key identifies: Priya's app, not the person holding the phone. It works more like a membership card than a passport. Whoever presents the card gets served, and the server has no way of telling whether they are the rightful owner.

That leads to the most common mistake. Priya might paste the key straight into her app's code, since that is where the requests are made. But an app installed on thousands of phones, or a website's code running in thousands of browsers, can be taken apart by anyone who is curious, and the key sits there in plain text. Someone who copies it can use up her 1,000 daily requests, or, on a paid plan, run up her bill. The usual fix is to keep the key on a server Priya controls: the app asks her server, and her server adds the key and asks the weather company. The key never leaves a machine she runs.

If a key does leak, the remedy is to revoke it in the company's dashboard and issue a new one. This is called rotating the key, and providers usually let you have two keys active for a while so the switch causes no downtime.

## Going further

- **Key restrictions:** many providers let you limit a key to certain websites, apps, or kinds of request, so a stolen copy is less useful.
- **OAuth:** a standard for letting an app act on behalf of a specific person, which an API key alone cannot do.
- **Secret scanning:** tools that search code repositories for keys pasted in by mistake.

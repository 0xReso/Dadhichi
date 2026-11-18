# What an API key is

By the end you will know what an API key is, why services hand them out, and the mistake that most often leaks one.

Say you are building a small travel app that shows the weather at each stop. You do not run weather stations, so your app asks a weather company's computers for the forecast. The company publishes a fixed way for programs to make that request, along the lines of "send the name of a city to this address and get back tomorrow's temperatures". That published way for one program to ask another for something is called an API, short for application programming interface.

The weather company now has a problem. Thousands of programs send it requests, each one costs it computing time, and it may want to charge for heavy use, cut off a program that floods it, or simply know who is asking. A request arriving over the internet carries no name of its own.

So when you sign up on the company's website, it gives you a long random string, around forty letters and digits that nobody could guess. Your app attaches that string to every request it sends, tucked in alongside the address and the city name. That string is called an API key.

When a request arrives, the company's server looks the key up in its records. If the key matches your account, it answers, counts the request against your plan, say 1,000 free forecasts a day, and refuses once you go past that number. If the key is missing, wrong, or has been switched off, the server sends back an error instead of the forecast. That one lookup is the whole mechanism.

This is where people most often go wrong. An API key identifies a program or a project, not a person, and it proves nothing beyond "whoever sent this holds the string". Anyone who copies your key becomes you as far as the weather company can tell, and their requests use up your 1,000 a day or land on your bill. A key behaves like a password with no username attached, and it needs the same care.

That rules out putting it anywhere strangers can read it. Code that runs on a user's phone or in their browser can be taken apart, so a key placed there is effectively public, and keys are regularly found in code posted publicly online by mistake. The usual practice is to keep the key on a server you control, have your app ask that server, and let the server add the key before calling the weather company. The requests themselves should travel over HTTPS, the encrypted form of web traffic, so the key cannot be read on the way.

If a key does leak, you go back to the company's website, delete it, and create a new one. Doing that on purpose every so often is called rotating the key, and it limits how long any copy that escaped stays useful.

## Going further

- Key restrictions: settings many providers offer to limit a key to certain actions, websites, or apps.
- OAuth: a standard for letting a program act on behalf of one specific user, which an API key alone does not do.
- Secrets manager: a service for storing keys outside your code and handing them to your server when it runs.

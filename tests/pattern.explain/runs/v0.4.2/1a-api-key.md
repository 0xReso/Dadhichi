# What an API Key Is

By the end you will know what an API key is, what problem it solves, and the mistake that gets most of them stolen.

Suppose you run a small website for a walking-tour company, and you want every tour page to show a map. You do not draw maps yourself. You pay a mapping company to supply them, which means your website's code has to ask the mapping company's computers for a map many times a day, with no person sitting there to type a password.

When one program asks another to do something, it uses a published set of requests that the other program has agreed to answer. That published set is called an API, short for application programming interface. The mapping company's API might accept a request such as "send me a map centred on this street, at this zoom level" and reply with the map image.

The mapping company now has a problem. Thousands of websites send it requests, and it charges each customer per map, say $5 for every thousand. When a request arrives, it has to know whose account to charge, and whether that account is allowed to ask at all.

So when you sign up, the company generates a long random string for your account, around forty letters and digits that nobody could guess. Your website attaches that string to every request it sends. That string is called an API key. When a request comes in, the mapping company looks the key up, finds your account, adds the map to your bill, and sends the map back. A request with a missing or unknown key is refused.

Notice what the key proves. It does not show that you, the person, are present. It shows that whoever sent the request holds the string, and nothing more.

This is where people most often go wrong. Because a key looks like an account number, it gets treated like one: pasted into code that is shared publicly, sent in a group chat, left visible in a screenshot. But anyone who copies your key can send requests the mapping company will treat as yours, and you pay for them. If a stranger finds your key and loads a million maps, the bill at $5 per thousand comes to $5,000. An API key is a secret in the same way a password is, and it deserves the same care.

When a key does leak, you delete it in your account settings with the mapping company, which makes the service reject it from then on, and you generate a new one for your website. Replacing a key on purpose like this is called rotating it, and many teams rotate keys on a schedule even when nothing has gone wrong.

## Going further

- **Key restrictions**: many services let you limit a key to particular websites, addresses, or features, so a copied key is less useful elsewhere.
- **Rate limits**: a cap a service sets on how many requests one key may make per minute or per day.
- **Environment variables and secrets managers**: common places to store keys so they stay out of the code itself.
- **OAuth access tokens**: a related kind of string that stands for one particular user's permission and usually expires after a set time.

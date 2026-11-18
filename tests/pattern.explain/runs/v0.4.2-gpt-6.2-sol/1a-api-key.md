# What an API key is

You’ll understand what an API key identifies, how a service checks it, and why it matters who can copy it.

Your shop’s website shows tomorrow’s forecast so customers can plan a pickup. To get that forecast, the website’s code asks a weather service for it. The weather service needs to know which customer account to count the request against.

The weather service gives your code a documented way to ask for a forecast and receive the result. That set of rules is an application programming interface, or API. It tells your code what information to send, such as the shop’s postal code, and what to expect back.

When you set up the weather service, it issues a string of letters and numbers and links it to your shop’s account. That string is an API key. Your website’s code keeps a copy so it can include the key each time it asks for a forecast.

When the request arrives, the weather service checks the key. If the key is valid, the service can look up the associated account and apply its rules. Say your shop’s plan allows 1,000 requests a day. If the shop has used 249 and the service accepts this request, the service returns the forecast and counts it as request 250. A valid key can still lead to a refusal if the account has already reached its daily limit.

The easy mistake is to think the key proves who sent the request. In this example, the weather service checks the value it received. If someone copies the key and sends it with their own forecast request, the service can count that request against your shop’s allowance too. The key tells the service which account to use. It does not establish who was at the keyboard or which copy of the code made the request.

That distinction matters when you decide where to put the key. If the weather service treats the key as a secret, keep it in the part of your website that runs on your server. Code sent to a customer’s browser can be inspected by that customer. Your server can send the forecast to the browser while keeping the key on the server.

If a secret key gets copied, you can usually revoke it, which tells the service to stop accepting it. Your website then needs a replacement key to keep fetching forecasts. Some services also issue keys intended for use in a browser. The service’s documentation tells you whether a particular key is meant to be kept secret.
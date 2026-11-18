# The cloud

By the end, you’ll know what you rent in the cloud, what happens when you ask for more, and which parts are still your responsibility.

## Why rent computing power?

A shop runs a website that takes orders. Most days, one computer can keep up. During a sale, four times as many people might arrive at once. If requests come in faster than the computer can answer them, shoppers wait, and some give up.

The shop could buy more computers. It would have to arrange somewhere to put them, connect them to the internet, and keep them working. It would also have to decide how many to buy before seeing how busy the sale gets. Once the sale ends, it would still own the extra computers.

A company can instead keep a large supply of computing equipment and let customers rent what they need. That company is a *cloud provider*. It can serve many customers from the same supply, so each customer can draw on more equipment than it would make sense to own.

*The cloud* is a way of getting computing services over a network, on demand. The shop can ask for more capacity through a web page or from its own software. It can release that capacity when the sale ends. What it pays depends on the service and its pricing, but it can rent extra capacity for a short period without buying the equipment.

What does the shop get when it asks the provider for another computer?

## What the provider gives you

The shop wants extra computers for the sale, with enough control to run the website software it already uses. It rents computers that behave like separate machines even though they can share the same physical equipment. Each one is called a *virtual machine*.

The physical computers sit in a *data centre*, a building equipped to keep computing equipment powered, cooled, and connected. From the shop’s point of view, the virtual machine is a computer it can reach over a network. Someone at the shop can install software on it from their desk.

When the shop asks for a virtual machine, the provider’s software finds a physical computer with room for it. The provider assigns it a share of the computer’s processing power and memory. Software on the physical computer keeps each virtual machine’s memory separate, so programs on one virtual machine cannot ordinarily read what programs on another are holding there.

The website also needs somewhere to keep orders after it finishes taking them. For this sale, the shop uses a shared *database*, a service the website can ask to save or retrieve records. The database runs separately from the virtual machines that handle shoppers. An order saved there is available to all of them, and the shop can remove a virtual machine after the sale without taking its orders with it.

Once the shop has another virtual machine running the website, how does a shopper reach it?

## How extra capacity becomes useful

The shop can now run copies of its website on several virtual machines. Each copy can look up the same products and save orders in the same database. Shoppers still arrive at the same web address, so the shop needs a way to send each incoming request to one of the machines that can answer it.

A *load balancer* does that job. A request is a message asking the website to do something, such as show a product page. The load balancer receives the request and passes it to one of the website machines. Each shopper uses the usual address while the shop spreads the work across several machines.

For the sale, suppose the shop goes from one machine to four. It starts three virtual machines, gets the website running on each, and adds them to the load balancer. When the sale ends and requests slow down, it can stop sending new requests to the extra machines, let them finish their current work, and release them.

The common mistake is to assume a website grows automatically because it runs in the cloud. The provider makes more capacity available to request. The shop still needs a way to decide when to ask for it and to put it to work. Four website machines can handle more requests than one if those machines were what held the site back. If the database is already struggling to save orders fast enough, sending it more work can leave shoppers waiting as before.

How much of that work belongs to the shop, and how much can it hand to the provider?

## Who keeps what running?

During the sale, the provider keeps the equipment available and the shop uses some of it to run its website. With rented virtual machines, the shop still looks after the software inside them. That includes installing security updates and deciding what to do when a copy of the website stops answering requests.

The shop can hand over some of those jobs by choosing a *managed service*. If it uses a managed database, for example, the provider can take care of updating the database software. The shop still decides who can read order records and for how long it needs to keep them. The exact division of work depends on the service the shop chooses.

The distinction matters when a customer places an order. A provider may be responsible for keeping the database running while the shop is responsible for making sure its website saves the order before showing a confirmation. What ties those responsibilities to the capacity the shop rents?

## The whole picture

The cloud lets the shop draw on a provider’s supply of computing equipment as demand changes. During a sale, the shop can rent extra virtual machines and send them a share of the website’s requests. Its orders live in a separate database, so it can release the extra machines when traffic falls. The service the shop chooses determines how much of the day-to-day work the provider takes on, and the way the shop puts those services together determines how well the website handles the sale.

## Going further

- **Autoscaling** adds or removes capacity according to rules, such as how busy the website machines are.
- **Regions** are geographic areas where a provider offers services. The choice can affect how quickly data travels to shoppers and where it is stored.
- **Object storage** keeps items such as product images so the website can retrieve each one by name.
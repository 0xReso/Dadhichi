# The cloud

You’ll understand what the cloud provides, what happens when an app uses it, and who keeps each part running.

## When one computer is no longer enough

Suppose you run a shop that takes 40 online orders an hour on a normal afternoon and 400 an hour during a sale. The shop’s app needs somewhere to run and somewhere to keep its orders. You could buy enough computers for the busiest hour, set them up, and keep them running. On an ordinary afternoon, much of what you bought would sit idle.

A computer that answers requests from other computers is called a **server**. When a shopper clicks Place order, their browser sends the order details to a server running the shop’s app. The app records the order and sends back a confirmation. That exchange can happen whether the server is in your building or across the country.

The cloud changes how you get that server and the other resources your app needs. A company called a **cloud provider** operates pools of computing equipment. You can ask for a share of that equipment through a website or through your own software. The provider assigns it from what is already running or ready to use, so adding a server does not have to start with buying a machine.

The physical equipment sits in a **data centre**, a facility built to house computers and keep them supplied with power, cooling, and network connections. Your shop can use the equipment from a distance. The cloud’s distinctive feature is that you can get and release resources as needed from a pool the provider operates.

What does the provider actually give your shop when you ask for a server?

## What your app runs on

Your shop can ask a cloud provider for a server when it needs one. In a common setup, the provider can give you a working server without having to set aside a whole physical computer for the shop.

The provider divides the processing power and memory of a physical computer among separate environments. Each can run its own software and behave like a computer in its own right. One of these environments is called a **virtual machine**. Your shop can run its app on one virtual machine while another customer runs unrelated software on another.

You install the shop’s app on a virtual machine and connect it to the place where the shop keeps its orders. In this setup, the orders live in a **database**, which is software that stores records and lets an app find or update them. Keeping the database separate from the app’s virtual machine means you can replace that machine without taking the order records with it.

Now follow an order through the shop. The shopper’s browser sends the order details over the internet to the shop’s app. The app checks the details and asks the database to save the order. Once the database reports that it has saved the record, the app sends the confirmation back to the browser.

If the shop asks for a second virtual machine, you can run another copy of the app on it. Both copies can use the same database. An order saved by the first copy is then available to the second, which matters when the shopper returns to check its status and their browser reaches a different copy.

How does the shop put that second copy to work when the sale starts?

## What changes when more orders arrive

The shop can run several copies of its app while keeping the orders in one database. To make use of the extra copies, incoming requests need somewhere to go that can pass them on to a working copy.

That job belongs to a **load balancer**. The browser sends its request to the shop’s usual address. The load balancer receives it and forwards it to a copy of the app. As more requests arrive, it spreads them across the available copies.

Suppose the app servers are the first part to fall behind as orders climb from 40 to 400 an hour. The shop can start more virtual machines, run the app on them, and have the load balancer send them some of the work. After the sale, it can stop sending new requests to the extra copies, let them finish the requests they already have, and release the extra machines.

The ability to add resources as demand grows and release them as it falls is called **elasticity**. The shop can arrange for software to make those adjustments automatically. That arrangement is called **autoscaling**. It needs a rule, such as adding a copy when the existing machines have been busy for several minutes. New copies also take time to start, so a sudden rush can reach the shop before the extra capacity is ready.

Extra copies help when the app servers are holding up orders. If the database is already saving orders as fast as it can, more app servers will send it more work while it is already busy. The shop has to increase capacity in the part that is falling behind.

Releasing resources can also reduce the bill. If the provider charges the shop according to how long its virtual machines run, the extra machines add to the bill for the hours they are in use. The database can still incur charges after the sale because it keeps running and holding the orders.

When a machine stops working, which parts of getting the shop back online belong to the provider?

## Who keeps the shop running

The provider supplies the virtual machines, and the shop decides what runs on them and how orders reach them. That division matters when something breaks. An app can be unreachable even when the provider’s equipment is working as expected.

Suppose one of the shop’s app copies stops responding during the sale. If the load balancer is set up to check whether each copy can answer, it can stop sending new requests to the failed copy. The other copies can keep taking orders if they have enough capacity and can still reach the database. An order already being handled by the failed copy may still need checking, because the database could have saved it before the browser received a confirmation.

Now suppose the database itself stops answering. The app copies may all be healthy, yet none can finish saving a new order. Keeping the shop open through that failure requires a separate arrangement for the database. The number of app copies does nothing to change where they all send their orders.

What the provider handles depends on the service the shop buys. With a virtual machine, the provider keeps the underlying equipment and the systems that supply the virtual machine running. The shop generally looks after the software it installs, including updates. With a **managed database**, the provider takes on specified jobs involved in running the database, such as applying software updates. The shop still decides what to store and who can read or change it.

That is the practical distinction behind the idea that moving to the cloud will keep a shop online. The provider can supply equipment and services the shop can use to recover from failures. The shop stays open through a particular failure when the parts an order depends on can keep doing their jobs through that failure.

## The whole picture

The cloud gives the shop a way to obtain computing resources from equipment a provider operates and to adjust how much it uses as demand changes. From the shopper’s side, placing an order still means sending a request to an app that saves a record and returns a confirmation. From the shop’s side, preparing for the sale can mean starting extra app copies for a few hours. Keeping orders flowing still depends on how those copies receive requests and whether the database they share can handle them.

## Going further

- **Region** is a geographic area where a provider offers cloud resources.
- **Availability zone** is a group of facilities within a region designed to keep certain failures from affecting other zones.
- **Infrastructure as code** means describing resources in files so software can create and update them consistently.
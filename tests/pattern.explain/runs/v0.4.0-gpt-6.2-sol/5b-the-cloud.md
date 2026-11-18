# The cloud

You’ll understand what you rent in the cloud, what happens when someone uses the service you run there, and which jobs are still yours.

## A shop that needs to stay open

When a customer opens your shop’s website, a program has to find the products and prices and send back a page. The machine running that program needs to be available whenever a customer comes by, even when the shop is closed and your laptop is off.

A computer that does work on behalf of other computers is called a **server**. The shop could buy a server and keep it on the premises. Someone would then have to keep it powered, connected to the internet, and working when a part fails. If a sale brings in more customers than the server can handle, the shop needs a way to add capacity.

A company can take on the work of operating the physical machines and let the shop use some of their capacity. That company is a **cloud provider**. It houses its machines in a **data centre**, a building equipped to supply them with power, cooling, and network connections.

The **cloud** is a way to get computing resources from a provider over a network, when you need them. Your shop can arrange for a server to run with a few choices on a website or a command from a program. The provider can fill that order from machines it already operates.

If the provider already has the machines, what does the shop receive when it orders a server?

## What the shop rents

The shop needs somewhere to run its website, and the provider has physical machines ready. The provider can use software to make one physical machine behave like several separate computers. Each gets a share of the physical machine’s processing power and memory, and each can run its own programs. One of these software-defined computers is called a **virtual machine**.

The shop chooses a virtual machine with enough capacity for ordinary traffic. When it confirms the order, the provider sets up the virtual machine on a physical machine with room to run it. Setting up a resource so it’s ready to use is called **provisioning**. Once the virtual machine is ready, the shop can install and start its website program.

The shop also needs to keep information such as product prices and orders between visits. It can put that information in a **database**, a system that stores records and lets a program find or change them. In this example, the shop orders the database separately from the virtual machine. The website program runs on the virtual machine, while the order records live in the database. That means the shop can replace the virtual machine without moving the order records.

The provider can operate the database software as part of what the shop buys, including applying software updates. A service where the provider runs the underlying software for you is called a **managed service**. The shop still decides what information to keep in the database and gives the website program permission to read and write the records it needs.

Once the website program is running and can reach the database, what happens when a customer asks for a page?

## What happens when a customer visits

The shop’s website program runs on a virtual machine, and its product records live in a separate database. When a customer opens a product page, their browser sends a message asking for it. That message is a **request**, and the message the website sends back is its **response**.

The request travels over the internet to the shop’s website program. The program asks the database for the product record, uses the returned price and description to build the page, and sends the response. The browser displays it. From the customer’s point of view, this exchange works the same way whether the shop rents the server or owns it.

Now suppose the shop starts a sale and the one virtual machine gets more requests than it can comfortably handle. The shop can provision a second virtual machine and run another copy of the website program on it. Both copies can read from the same database, so they can show the same price.

To put both copies to work, the shop can send incoming requests through a service that decides which copy should receive each request. That service is called a **load balancer**. With two copies serving requests, the website program can handle more visits at once, as long as the database and the rest of the system can keep up.

Adding capacity to handle more work is called **scaling**. The shop can arrange for the system to add virtual machines when demand rises and remove them when it falls. That arrangement is called **autoscaling**. It depends on the shop choosing a service that supports it and setting it up. A single rented virtual machine, left as provisioned, has a finite amount of capacity.

Once the shop can add or remove capacity, how does that affect what it pays and what it still has to run?

## What the shop pays for and looks after

The shop can run a second copy of its website program for the sale and remove that copy when traffic drops. With a virtual machine billed by running time, the extra machine adds a charge while it runs. A shop that owns a second server has to buy it and have it ready for the sale. A shop renting one can provision it when needed and stop paying for its running time when it’s done.

Different resources can have different billing rules. The database can still hold the shop’s orders after the extra virtual machine is gone, and the provider can still charge for keeping those records. For the shop, the bill reflects the resources its system uses, with the details set by the services it chose.

Those choices also determine who does the work. The provider maintains the physical machines. On the virtual machine in this example, the shop still maintains the website program and applies updates to the **operating system**, the software that manages the virtual machine and runs its programs. For its managed database, the shop has handed operation of the database software to the provider.

A similar division applies when something breaks. Two copies of the website can keep serving pages if one copy fails and the load balancer sends requests to the working one. Both copies still need the database. If the database goes down, adding another copy of the website program leaves the shop with the same problem. The shop has to decide how long it can afford to be offline and choose a setup that can meet that need.

## The whole picture

The cloud lets the shop get computing capacity when it needs it because a provider already operates machines and can allocate some of that capacity on demand. The shop uses those resources to run its website and keep its records, and can add capacity for a sale without buying a server for the occasion. What the provider takes care of depends on the service the shop chooses. The shop still decides how the pieces fit together and what should happen when demand rises or a piece fails.

## Going further

- **Infrastructure as a service** is the category that includes renting virtual machines and managing what runs on them.
- A **region** is a geographic area where a provider offers resources.
- An **availability zone** is a location within a region designed to limit how failures spread to other zones.
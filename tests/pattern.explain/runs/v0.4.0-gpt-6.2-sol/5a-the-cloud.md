# The cloud

You’ll understand what you rent in the cloud, how an app runs there, and what you still have to manage.

## Why rent computing?

Suppose a shop wants to let customers check their orders online. Whenever someone opens the order page, a computer has to run the shop’s software and read the order details. If the shop buys that computer, it has to decide how much work the machine should be able to handle. A quiet afternoon might bring 30 requests in a minute. A sale might bring 3,000. A machine bought for the sale could spend most of the year with capacity to spare.

A computer that runs software or supplies data for other computers is called a *server*. The shop needs a server even when nobody is in the shop. It needs somewhere to put the machine, a working network connection, and a way to recover if the machine breaks. Those are ongoing jobs that come with owning the equipment.

The shop can get computing from a company that already operates the equipment. That company is a *cloud provider*. Its equipment sits in buildings called *data centres*, where many servers share facilities such as power, cooling, and network connections. The provider runs the physical equipment while customers use the computing resources it supplies.

Renting space on a server has been possible for a long time. What makes cloud computing distinctive is how the shop gets and changes what it rents. It can request computing power and storage through software, start using them when they’re ready, and release them when it no longer needs them. The provider measures usage for billing. What counts as usage depends on the service. A server, for instance, can cost money for the time it’s running even during a minute when nobody visits the shop.

How does the shop turn an account with a cloud provider into a working order page?

## What the shop rents

The shop can get computing without buying the equipment. It still needs somewhere to run its order-page software.

One option is to rent a software-created computer called a *virtual machine*. A physical server can run several virtual machines, giving each a share of its computing power and short-term memory. Each virtual machine can run the basic software that manages a computer, called an *operating system*. The shop installs its order-page software on top of that, much as it would on a computer it owned.

To create the virtual machine, the shop chooses a size from the provider’s menu. The size determines how much computing power and memory the machine gets. The shop submits the request through the provider’s website, and the provider’s software finds physical capacity and starts the virtual machine. This is what getting computing on demand looks like. The shop asks for a machine through software, and the provider supplies it from equipment already in service.

The order details need a place of their own. The shop keeps them in a *database*, which stores records so software can look up or update a particular order. In this example, the shop rents a database service separately from the virtual machine. The order-page software runs on the virtual machine. The records live in the database. This arrangement lets the shop replace its virtual machine and point the replacement at the same records.

Once the order page is online, your browser sends a request for the page to the shop’s software. The software checks that you’re allowed to see the order, asks the database for its details, and sends back the page your browser displays. The work happens on the provider’s equipment. From your seat, it looks like opening any other webpage.

What happens when sale traffic gives that one virtual machine more work than it can handle?

## How the shop handles a rush

The order page runs on one virtual machine, and the order records live in a separate database. During the sale, the shop can start more virtual machines running the same order-page software. Each can look up orders in the same database, so any of them can answer the next request.

The shop also needs a way to direct each incoming request to one of the running machines. The service that does this is called a *load balancer*. Your browser keeps using the same address for the shop. Behind that address, the load balancer sends one request to one machine and another request to another. The machines can now handle requests at the same time.

The shop can set a rule to add machines when the existing ones stay busy and remove machines when traffic falls. This is called *autoscaling*. The rule has to use a measure the shop can observe, such as how much of the machines’ computing power is in use. Starting another machine takes time, so a sudden rush can still slow the order page while the extra machines start up.

This is where it’s easy to mistake the ability to rent more computing for an app that can handle any amount of work. Adding machines helps when the order-page software is what’s holding things up. If the database already has more lookups than it can handle, extra machines can send it requests faster while customers still wait for their pages. The shop has to find which part is reaching its limit before it decides what to expand.

With the provider running the equipment and the shop able to add machines, who keeps the order page working and the records safe?

## Who looks after what?

The shop can add machines during the sale and release them afterwards. Its responsibility depends on what it rents. For the virtual machines in this example, the provider maintains the physical servers. The shop looks after the operating system and the order-page software it installed, including applying security updates.

For the database, the shop chose a *managed service*, meaning the provider takes on routine work involved in running the database software, such as applying updates. The shop still decides which programs and people may read the order records. A provider can keep the database software up to date while a permission set by the shop gives someone access they should never have had.

The same division matters when something goes wrong. If one virtual machine stops answering, the load balancer can send new requests to the other machines, provided it’s set up to recognise the failure. If the shop accidentally deletes order records, the extra machines will all see the deletion. Recovering the records requires a usable backup, a copy kept for recovery. The database service may make backups, and the shop needs to know how far back it can restore and how to do it.

## The whole picture

The cloud lets the shop get computing and storage through software as its needs change. The provider keeps the physical equipment running. The shop uses that equipment to run the order page on virtual machines, keeps the records in a database, and adds machines when there’s enough work for them to share. How much day-to-day work the shop hands over depends on the service it rents. Its choices about how to distribute requests, who can read the records, and how to recover them still shape what customers experience.

## Going further

- **Region** — A geographic area where a provider offers cloud resources.
- **Availability zone** — An area within a region designed to limit the spread of infrastructure failures.
- **Infrastructure as code** — Describing cloud resources in files so software can create and update them consistently.
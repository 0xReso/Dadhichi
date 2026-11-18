# The Cloud

By the end you will know what "the cloud" actually is underneath the phrase: what it rents out, how that renting works, and what it does and does not take off your hands.

## The problem of owning machines

In computing, "the cloud" means renting computers, storage and networking from a company that owns huge buildings full of them, and reaching those rented resources over the internet. You ask for a machine when you need it, pay for the time you use it, and hand it back when you are done. That is the whole idea. The rest of this piece is about why it exists and how it works.

Start with a concrete case. A concert venue sells tickets through its own website. On an ordinary day about 200 people visit. But when a popular band's tickets go on sale at 10 o'clock on a Friday morning, 20,000 people arrive within the same few minutes, and if the site falls over, the venue loses sales and gets a flood of angry messages.

The programs that run a website live on servers: computers that sit somewhere, switched on all the time, answering requests from people's browsers. Before the cloud, the venue had to buy its own servers, or rent fixed ones from a hosting company, and the hard question was how many.

Buy enough for the ordinary 200 visitors and the site collapses on Friday at 10. Buy enough for 20,000 and most of those machines sit idle for the rest of the year, still drawing power, still needing cooling, repairs and someone to look after them. Buying also takes time: ordering hardware, waiting for delivery and installing it could take weeks. Owning machines forces you to guess your peak in advance and pay for that guess every day.

The cloud exists to remove that guess. What makes it possible is a building, and a trick played inside it.

## What is actually out there

So the problem is that owned machines are sized for the busiest moment and wasted the rest of the time. The answer starts with where the rented machines physically live.

A cloud provider, such as Amazon Web Services, Microsoft Azure or Google Cloud, owns data centres: warehouse-sized buildings holding tens of thousands of servers in racks, with their own power supplies, cooling and fast network links. Nothing about the cloud is vaporous. Your rented machine is real hardware in a real building, usually in a place you can name.

Providers group their data centres by geography into regions, for example one in Frankfurt and one in Virginia. You choose a region when you rent something. Picking one near your customers keeps the delay short: a request from Munich to Frankfurt and back takes a few milliseconds, while one across the Atlantic to Virginia takes closer to a tenth of a second. The region also decides which country's laws your data sits under, which matters to many businesses.

Now the trick. A single physical server in one of these buildings is far more powerful than most customers need. So the provider runs a layer of software on it called a hypervisor, which divides the one physical machine into several separate pretend machines. Each pretend machine has its own share of the processor, memory and disk, runs its own operating system, and cannot see the others.

Each of those pretend machines is called a virtual machine, often shortened to VM. To the person using it, a virtual machine behaves like an ordinary computer: you can log in, install software and run a website on it. Underneath, it is a slice of a bigger machine that may be shared with strangers. This slicing is called virtualisation, and it is what lets a provider hand out computers by the hundred in seconds, because creating a virtual machine is a software operation, not a delivery.

Having machines that can be created in seconds raises the next question: how does the venue actually ask for one?

## Renting by the minute

The provider owns data centres full of servers, and virtualisation lets it carve those servers into virtual machines quickly. What turns that into a service is the way you ask for them.

Every cloud provider exposes an API, the published way one program asks another to do something. Through it, a person or a program can say, in effect, "give me four virtual machines of this size in the Frankfurt region", and get them running within a minute or two. The same API removes them again. The provider's web dashboard, where you can click buttons to do the same thing, is a front end to that API.

Because machines come and go on request, billing follows use. Most providers charge for virtual machines by the second or by the hour, plus separate charges for storage and for data sent out to the internet. A modest virtual machine typically costs somewhere around a few cents to tens of cents an hour; prices vary by provider and size and change often, so treat that as an order of magnitude, not a quote. This model is called pay-as-you-go: no purchase up front, a bill afterwards for what ran.

Back to the venue. On a normal day its site runs on two small virtual machines. At 9:45 on Friday it asks for 40 more. At noon, when the rush is over, it hands them back. It has paid for 40 machines for a little over two hours, not for 40 machines all year.

The venue does not even have to do this by hand. It can set a rule with the provider: when the existing machines are more than, say, 70 percent busy, add another; when they are mostly idle, remove one. This is called autoscaling, and the general property it gives you, capacity that stretches and shrinks with demand, is called elasticity. Elasticity is the thing the venue was missing when it owned its servers.

Virtual machines are only the most basic thing you can rent. The question is how much of the work the venue wants to keep for itself.

## How much you rent

The venue now knows it can rent virtual machines by the minute and let autoscaling add and remove them. But a virtual machine still needs someone to install its operating system updates, its web server software and the venue's ticketing program. Cloud services differ mainly in how much of that stack they take over.

At the bottom is renting the raw building blocks: virtual machines, disks and networks, with everything on top left to you. This is called infrastructure as a service, or IaaS. The venue's two-plus-forty virtual machines are IaaS. It has the most control and the most chores.

One step up, the provider also runs the operating system and the surrounding software, and the venue only hands over its own program and its data. This is platform as a service, or PaaS. A managed database is a common example: the provider keeps the database software running, patched and backed up on a schedule, and the venue only stores its tickets and orders in it.

A related style is often called serverless. The venue uploads small pieces of code, such as "reserve this seat", and the provider runs each one only when a request arrives, charging per run. The name is a piece of marketing: the code still runs on servers. The difference is that the venue never sees, sizes or pays for an idle one.

At the top, you rent a finished application used through a browser, and you manage nothing but your own account and data. This is software as a service, or SaaS. If the venue sends its newsletters through a hosted email service, or keeps its accounts in an online bookkeeping tool, it is using SaaS. Most people use SaaS daily without thinking of it as "the cloud".

With all these layers handing work to the provider, it is tempting to think the provider has taken over everything. That is where people most often go wrong.

## What the provider does not do for you

The venue can rent at whichever layer suits it, from bare virtual machines up to finished applications, and pay only while things run. What it has not done, at any layer, is give away all responsibility.

Providers describe this with a principle called the shared responsibility model. The provider is responsible for the security of the cloud: the buildings, the physical servers, the hypervisor, the network between data centres. The customer is responsible for security in the cloud: who is allowed to log in, how its data is protected, what its own software does, and how its settings are configured. The higher the layer you rent, the more the provider covers, but some part always stays with you.

The common mistake is to assume "it's in the cloud" means safe and backed up. Suppose the venue stores scanned copies of customers' ID documents in cloud storage and, while setting it up, marks the storage as readable by anyone with the address. The provider's buildings and hardware are working perfectly, and the files are still open to the whole internet. Many real data leaks have happened in exactly this way, through a customer's setting rather than a provider's failure.

Backups follow the same rule. A virtual machine's disk is not automatically copied somewhere safe unless the venue sets that up or uses a service that promises it. Deleting the wrong thing through the API deletes it, quickly and for real.

Cost is the other place the assumption goes wrong. Pay-as-you-go saves money when demand swings, as with the venue's Friday rush. A workload that runs flat out all year, every hour, can cost more rented than owned, and forgotten machines left running keep billing. The cloud trades a large purchase for a running bill, and a running bill needs watching.

## The whole picture

Owning servers forces you to buy for your busiest moment and pay for that guess all year. Cloud providers solve this by filling data centres with servers, using a hypervisor to slice each one into virtual machines, and letting anyone create and remove those machines through an API in minutes, billed by the time they run. Autoscaling uses that to give elasticity: the venue grows from two machines to forty for its Friday rush and back again. On top of rented virtual machines sit services that take over more of the stack, from platforms to finished applications. Across all of them, the provider runs the hardware and the buildings, while the customer stays responsible for its own access rules, data, settings and bill.

## Going further

- Availability zones: separate data centres within one region, with independent power and networking, so an application spread across them survives one building failing.
- Object storage: the cloud's standard way of storing files as items in named containers called buckets, reached over the internet; Amazon S3 is the best-known example.
- Egress fees: charges for data leaving a provider's network, often the surprise line on a cloud bill.
- Public, private and hybrid cloud: renting from a shared provider, running the same kind of self-service setup on your own hardware, or combining the two.

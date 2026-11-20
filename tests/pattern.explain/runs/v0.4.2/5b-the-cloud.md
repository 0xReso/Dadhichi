# The Cloud

By the end you will know what physically sits behind "the cloud", how renting computing power by the minute works, and which part of the job stays with you after you move.

## The problem with owning machines

Take a small online shop that sells loose-leaf tea. Its website has to live on a computer that is switched on day and night, connected to the internet, and ready to answer anyone who visits. A computer doing that job, waiting for requests from other devices and sending back what they asked for, is called a server. Your phone, when it asks for the shop's page, is the client.

For a long time a business like the tea shop had one realistic way to get a server: buy one, put it in a cupboard or a rented rack somewhere, and pay someone to look after it.

That arrangement has a sizing problem. On an ordinary day about 200 people visit the shop each hour, and a single modest server copes easily. But every November the shop runs a two-day sale, and traffic jumps to about 20,000 visitors an hour, a hundred times as many. If the shop buys enough machines for the sale, most of them sit idle for the other 363 days of the year. If it buys enough for an ordinary day, the site falls over on the two days that bring in the most money.

There are smaller problems on top. Ordering and setting up new hardware takes weeks, so the shop cannot react to a surprise rush. And when a disk fails at three in the morning, it is the shop's disk and the shop's problem.

The cloud is the answer to all of this. Instead of owning servers, the shop rents computing power from a company that owns enormous numbers of them, reaches those machines over the internet, starts and stops them in minutes, and pays for the time it uses. Which raises the obvious question: where are those machines, and how does a stranger's computer become the shop's for an afternoon?

## Where the shop actually runs

The tea shop's trouble, then, is that owned hardware is either too much or too little, and slow to change. The cloud replaces owning with renting, and the renting happens in a very physical place.

That place is a large, windowless building packed with racks of servers, often tens of thousands of them, with its own power supply, cooling and security guards. It is called a data centre. A cloud provider is a company that runs many data centres around the world and rents out what is inside them. When the tea shop moves to the cloud, its website runs on a machine in one of these buildings. The old joke that the cloud is "other people's computers" is accurate.

The provider does not hand each customer a whole physical server, because most customers would use a small fraction of it. Instead, each physical server is divided into several separate computers that exist in software. Each one behaves like a complete machine, with its own operating system, its own share of memory and processing power, and its own disk, and none of them can see into the others. Each of these is called a virtual machine, often shortened to VM. The tea shop's website runs in one VM; the same physical box might be hosting VMs for a bank and a games company at the same moment.

The layer of software that carves a physical server into virtual machines and keeps them apart is called a hypervisor. It belongs to the provider, and customers never touch it.

So the shop's website now runs inside a virtual machine, on a provider's server, in a data centre it will never visit. What is still missing is how the shop gets that VM, and how it gets twenty of them in November.

## Renting by the minute

The tea shop now rents a virtual machine instead of owning a server. What makes that useful is how quickly and how finely the renting works.

There is no phone call and no contract for each machine. The shop's developer opens the provider's website, picks a size, for example two processors and four gigabytes of memory, and within a minute or two the VM is running. The same request can be sent by a program instead of a person, through the provider's API, the published way one program asks another to do something. Because everything the provider rents can be requested through that API, the shop can write a script that creates or removes machines without anyone clicking anything.

The bill follows the same logic. Providers usually charge for each VM by the hour or by the second while it runs, and charge nothing once it is switched off. This is called pay-as-you-go pricing. Suppose, for illustration, a VM costs 5 cents an hour; real prices vary by provider, size and date. Each VM can serve about 1,000 visitors an hour, so the shop keeps two running all year for comfort. That comes to about 17,500 machine-hours, or roughly 876 dollars a year.

For the November sale the shop needs about twenty VMs. It starts eighteen extra machines for the 48 hours of the sale and stops them afterwards. That is 864 extra machine-hours, about 43 dollars. Owning twenty servers all year to cover those two days would have cost many times more.

Being able to grow and shrink like this, adding capacity when demand rises and handing it back when demand falls, is called elasticity. It is the property that solves the sizing problem from the start of this piece.

The shop does not even need to watch the traffic itself. It can give the provider a rule such as "when the machines are more than 70 per cent busy, add another; when they are under 30 per cent, remove one". Scaling that happens automatically by rule is called autoscaling. With it, the shop's November jump from two machines to twenty takes care of itself.

There is one more choice to make when renting: where in the world the machines are. Providers group their data centres by geography, and each group is called a region. Most of the tea shop's customers are in Europe, so it picks a European region. A page request from Berlin to a data centre in Germany and back takes a few hundredths of a second, too short to notice. The same request to a region in Australia takes around a quarter of a second for the round trip, enough to make the site feel sluggish.

Virtual machines are the clearest example, but providers rent much more in the same pay-as-you-go way: storage for the shop's product photos, a ready-run database for its orders, and dozens of other services. That leaves a question the shop's owner will reasonably ask: if the provider owns the building, the servers and the hypervisor, what is still the shop's job?

## What stays your job

The tea shop now rents machines, storage and a database by the hour, in a region it chose, and grows to twenty machines in November without buying any. It is easy to assume that the provider also keeps all of this safe. That assumption is the most common misunderstanding about the cloud.

The provider is responsible for what it owns: the buildings, the physical servers, the hypervisor, and the network that connects them. The customer is responsible for what it puts inside: the operating system running in its VMs and its security updates, the shop's own code, who is allowed to log in and with what permissions, and the data itself, including backups. Splitting the work along that line is called the shared responsibility model, and all the major providers describe their services this way.

In practice this means the provider will not stop the shop from making its own mistakes. If the developer sets the storage holding customer invoices to be readable by anyone on the internet, the provider will store and serve those invoices exactly as instructed. Misconfigured storage of this kind is a well-known, recurring cause of data leaks. If the developer deletes a VM, its disk usually goes with it, and nothing comes back unless the shop arranged backups. And if the shop runs everything in a single data centre and that building has an outage, the shop's site goes down with it; spreading across several locations is something the customer has to set up and pay for.

Where exactly the line sits depends on what is rented. With a bare virtual machine, the shop looks after nearly everything above the hypervisor. With the provider's ready-run database, the provider installs and patches the database software, but the shop still decides who can read the orders and whether they are backed up. Moving to the cloud hands over the hardware; it does not hand over the judgement.

## The whole picture

The cloud is computing rented from a provider instead of owned: physical servers in the provider's data centres are divided by a hypervisor into virtual machines, which a customer like the tea shop requests through a website or an API, places in a region near its users, and pays for by the hour while they run. Because machines appear in minutes and stop costing money when switched off, the shop can follow its demand, two machines on an ordinary day and twenty during the sale, which is the elasticity that owned hardware could never offer. What the shop gives up is the hardware and the buildings; what it keeps is everything it puts inside them, from software updates to permissions to backups, under the shared responsibility model.

## Going further

- IaaS, PaaS and SaaS: three common labels for how much the provider runs for you, from bare virtual machines (infrastructure as a service) to finished applications such as webmail (software as a service).
- Availability zones: separate data centres within one region, used to keep a site running when a single building fails.
- Serverless: a style of cloud service where you upload code and the provider runs it on demand, so you never manage a VM yourself, though servers still do the work.
- Egress fees: charges many providers make for data leaving their network, a common surprise on cloud bills.

# The Cloud: Renting Computers You Never See

By the end you will know what the cloud physically is, why businesses rent it instead of buying their own machines, how the renting works, and which part of the job stays with the customer.

## The problem with owning machines

Take a small online tea shop. Every time someone opens its website, a computer somewhere receives the request, looks up which teas are in stock, and sends back the page. That computer is a server: an ordinary computer, usually with no screen or keyboard, built to sit in a rack and answer requests from other machines all day.

On a normal day, two servers handle the shop's visitors comfortably. Once a year, though, the shop runs a Friday sale, and for about six hours ten times as many people arrive. To stay up during those hours, the shop needs about twenty servers.

If the shop owns its machines, it faces a bad choice. Buy twenty, and eighteen of them sit idle for all but six hours of the year, still drawing power, taking up space, and needing someone to replace failed disks and install security updates. Buy two, and the site slows to a crawl and then fails at the exact moment it matters most. Adding machines in a hurry is not an option either, because buying, shipping, installing and wiring up a server takes weeks.

Behind the machines sits a room that also has to be run: cooling, backup power, a fast internet connection, locks on the door. For a tea shop, none of that is the business.

The cloud is the answer to this. Instead of owning servers, the shop rents computing power from a company that owns enormous numbers of them, reaches it over the internet, and pays for what it uses, by the hour or even by the second. A company that rents out computing this way is called a cloud provider.

A rented server still has to be a real machine somewhere, so what does the provider actually build?

## What is behind the word

The tea shop needs two servers most days and twenty for a few hours a year, and owning them means paying for the peak all year round. Renting only helps if someone has those machines ready, and the way providers do that is less mysterious than the word "cloud" suggests.

The provider's machines live in data centres: warehouse-sized buildings holding many thousands of servers in long rows of racks, with their own power supplies, industrial cooling, and very fast connections to the internet. A large provider runs many of these buildings spread across several continents. In the end, "the cloud" means these buildings. Nothing about it floats.

If the provider handed each customer a whole physical machine, it would run into the tea shop's problem itself: most machines would be too big for most customers and idle much of the time. Instead it divides each powerful physical server into several pretend computers. Each one behaves like a separate machine, with its own operating system, its own share of processor and memory, and no view into its neighbours. This pretend computer is called a virtual machine, usually shortened to VM.

The software that does the dividing is called a hypervisor. It sits between the physical hardware and the virtual machines, hands each VM its slice of processor time and memory, and keeps them walled off from one another. So when the tea shop rents "a server", what it usually gets is a virtual machine on a physical computer it shares with strangers, in a building and rack it never learns the location of.

That explains where the machines are. The next question is how the tea shop gets twenty of them on a Friday morning without phoning anyone.

## Renting by the minute

The provider has buildings full of physical servers, each divided by a hypervisor into virtual machines it can rent to anyone. What makes this a cloud, rather than an old-fashioned hosting contract, is how fast and how finely the renting works.

The tea shop can ask for a new virtual machine from a web dashboard: pick a size, click, and within a minute or two the VM is running. There is no contract to sign and no salesperson to call, and the machine can be switched off and handed back just as quickly.

More often the request comes from a program rather than a person. The provider publishes a set of commands that software can send over the internet, such as "start a machine of this size", "stop that one", or "give me a hundred gigabytes of storage". A published set of commands like this, through which one program asks another to do something, is called an API, short for application programming interface. Because every action the dashboard offers is also available through the API, the shop can write a script that builds its whole setup in minutes, and run it again identically whenever it needs to.

The API also lets the provider do the adding and removing for the shop. The shop sets a rule: keep each server less than 70 percent busy; when they get busier, start another; when they get quieter, stop one; never go below two. On sale day, as visitors pour in, the provider's monitoring sees the load rise and starts VMs one after another, up to twenty. When the sale ends, it shuts the extra ones down. This automatic growing and shrinking is called autoscaling.

Billing follows the same pattern, and it is called pay-as-you-go: the shop pays for each VM only while it runs. Two servers running all year come to 2 times 8,760 hours, or 17,520 server-hours. The sale adds eighteen servers for six hours, which is 108 server-hours, a little over half a percent on top of the year's total. Had the shop bought twenty servers instead, it would have owned 175,200 server-hours of capacity a year in order to use about 17,600 of them.

The mechanism has limits. A new VM takes a minute or two to start, so autoscaling reacts in minutes rather than instantly, and a sudden rush can outrun it; a shop that knows when its sale begins will usually start the extra servers ahead of time. Pay-as-you-go also cuts both ways. A machine someone forgot to switch off is billed every hour it runs, and a workload that is large and steady all year can cost more rented than owned over several years.

Renting the machines hands a great deal of work to the provider, which raises the question people most often get wrong: how much of it?

## Who is responsible for what

The tea shop now rents virtual machines by the hour, adds them automatically on sale day and gives them back afterwards. It no longer buys hardware, cools a room, or replaces broken disks.

From there it is tempting to conclude that the provider now looks after everything, including the site's security, its data and its backups. That is the most common misunderstanding of the cloud, and it is an expensive one.

Providers divide the work along a line. Below the line sit the buildings, the physical servers, the hypervisor and the network between data centres; those are the provider's job. Above the line sits everything the customer puts on top: installing updates on the VM's operating system, the shop's own software, who holds which passwords, and which files are open to the public. This division is called the shared responsibility model, and the large providers describe it in their own documentation.

The shop's order records show where the line falls. The provider keeps the stored data on several drives at once, so a dead disk loses nothing. But if a bug in the shop's software deletes last month's orders, the provider faithfully keeps the deleted state on every copy, because from its side nothing went wrong. Backups that let the shop return to yesterday's data are something the shop has to switch on, and usually pay for. In the same way, a storage area left readable by anyone through a mistaken setting is the customer's error, not the provider's; misconfigurations of this kind are behind many well-known data leaks.

The line moves depending on what the shop rents. If, instead of installing a database on its own VM, it rents a ready-made database service, the provider also updates the database software. In general, the more finished the service, the more the provider takes on. Across the usual arrangements, though, deciding who may log in, what they may do, and what happens to the data stays with the customer.

## The whole picture

The cloud is computing rented from a provider instead of owned: real servers in real data centres, divided by hypervisors into virtual machines that anyone can start and stop through an API in minutes, billed only while they run. That combination is what lets the tea shop run two servers on a quiet Tuesday and twenty on sale day without buying for the peak, with autoscaling doing the adding and removing on its behalf. What the shop gives up is the hardware work, not the responsibility for what it builds on top: under the shared responsibility model, its software, its settings, its access rules and the safety of its data remain its own.

## Going further

- IaaS, PaaS and SaaS: names for how much the provider runs for you, from bare virtual machines (infrastructure as a service) through ready-made platforms such as managed databases (platform as a service) to complete applications such as webmail (software as a service).
- Regions and availability zones: how providers group their data centres by geography, and how spreading a system across several of them lets it survive a whole building going down.
- Serverless: a style of cloud service where you upload code and the provider runs it on demand, billing per request; servers are still involved, but you never manage or even see them.
- Public, private and hybrid cloud: renting from a provider's shared data centres, running the same kind of self-service setup on your own hardware, or combining the two.

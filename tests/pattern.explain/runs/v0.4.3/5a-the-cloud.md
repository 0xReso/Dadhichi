# The Cloud

By the end you will know what actually happens when a company "moves to the cloud": whose machines run its software, how it pays for them, and what it is still responsible for.

## The problem with owning computers

In IT, "the cloud" means renting computing power and storage from a company that owns enormous numbers of machines, instead of buying and running your own. The phrase is everywhere; what sits underneath it is more concrete than it sounds.

Every website lives on a server: a computer, usually with no screen or keyboard, that runs day and night waiting for requests from other machines and answering them. When you open a shop's page on your phone, your phone sends a request, and a server somewhere sends the page back.

Take a small company that sells concert tickets online. On an ordinary day its site runs comfortably on two servers. Then a famous band announces a tour, and on the morning tickets go on sale, about fifty times the usual number of people arrive within the same three hours. Serving all of them would take around a hundred servers.

Before the cloud, the company faced two bad options. It could buy a hundred servers, each costing thousands, taking weeks to arrive, and needing a room, power, cooling and someone to replace failed parts, then leave ninety-eight of them idle on almost every other day of the year. Or it could keep two and watch the site collapse on the one morning that brings in a large share of the year's sales.

The cloud exists to remove that choice. The company rents machines for the hours it needs them and hands them back afterwards. That raises an obvious question: where do machines that can be rented for a few hours actually come from?

## Where the machines live

The ticket company needs two servers most days and a hundred for a few hours, and owning a hundred is ruinous. A cloud provider solves this by owning the machines on behalf of thousands of customers at once.

Those machines sit in data centres: warehouse-sized buildings lined with racks holding tens of thousands of servers, with their own electricity supply, industrial cooling, and very fast connections to the internet. The large providers run many of these buildings around the world.

The ticket company does not rent a whole physical server. It rents a virtual machine: a simulated computer, with its own operating system, memory and disk, that exists as software running on a physical server it shares with other customers. From the inside it looks and behaves like a real computer. The company logs into it and installs its ticket shop exactly as it would on hardware it owned.

The separation between customers is kept by a hypervisor, a layer of software on each physical server that divides its processors and memory into slices and gives each virtual machine its own, so one customer's machine cannot see into another's. Because a virtual machine is only software, the provider can create one on any free slice in its data centres in a minute or two, without anyone walking up to a rack.

The company asks for machines through an API, the published way one program asks another to do something. A request says, in effect, "start a virtual machine of this size, with this much disk", and the provider's systems find room, start it, and reply with the new machine's network address. There is also a web page with buttons that does the same thing, but the API is what lets software order machines with no person involved.

So the company can now summon servers in minutes. What does it do with that on sale morning?

## Renting by the minute

The ticket company can ask the provider's API for virtual machines and have them running in a couple of minutes, on hardware it never sees. Sale morning becomes a matter of asking for more and then giving them back.

The company writes a rule: keep the servers, on average, below 70 percent busy; when they climb above that, start more; when they fall well below it, shut some down. The provider watches the numbers and makes the API calls itself. This is called autoscaling.

With many servers running, visitors have to be spread across them. That job goes to a load balancer, a machine that receives every incoming visitor and passes each one to whichever server is least busy. The visitor sees one website; behind it, the number of servers can change from minute to minute.

Here is the morning. At 9:00 tickets go on sale and the two servers shoot past 70 percent within seconds. Autoscaling starts new machines in batches, and by about 9:15 roughly a hundred are running, with the load balancer feeding each a share of the crowd. Around noon the rush fades, autoscaling shuts machines down, and by early afternoon the company is back to its usual two.

The company pays only for the time each machine ran, typically counted in minutes or seconds. With illustrative figures, say ten cents an hour for one mid-sized virtual machine (real prices vary by provider, size and year), the ninety-eight extra machines for three hours come to about 300 machine-hours, or roughly thirty dollars. The two everyday servers, running all year, cost about 1,750 dollars. Compare that with buying a hundred servers outright.

The mechanism has limits. A new machine takes a minute or two to start, so a spike that arrives faster than that still hits overloaded servers for a while; companies that know the date of a big sale usually start extra machines ahead of time. And the meter runs whatever the reason: a flood of junk traffic makes autoscaling start machines that are billed like any others, and a machine someone forgets to shut down keeps charging every hour.

If the machines belong to someone else, it is natural to wonder who is keeping them, and the customers' orders on them, safe.

## What the provider looks after, and what it does not

The ticket company now rents virtual machines by the minute and lets autoscaling grow them from two to a hundred and back. All of it runs in the provider's buildings on hardware the company never touches, which makes it tempting to assume the provider takes care of everything.

That assumption is the most common misunderstanding of the cloud: that anything put there is automatically backed up and secure. Providers draw a clear line instead. They are responsible for the buildings, the physical servers, the network between them and the hypervisor. The customer is responsible for everything inside its virtual machines: installing updates, the shop's own code, who holds the passwords, who can reach the data, and whether there is a backup at all. Providers publish this division and call it the shared responsibility model.

In the ticket company's case, suppose its orders are stored on the disk of one of its two everyday servers. If a developer deletes them by mistake, the provider will not restore them unless the company had set up backups. If the company makes a storage area readable by anyone on the internet, the provider will not stop strangers downloading it. Many publicised data leaks have been cloud storage that its owner had left open in exactly this way.

The line moves depending on what is rented. Instead of running its own database on a virtual machine, the company can rent a managed service, where the provider installs, updates and runs the software for it, and for databases usually takes regular backups as well. Even then, the company still decides who may connect and what goes in.

Hardware failure is shared in the same way. Providers group their data centres into regions, each a cluster of buildings in one geographic area, such as around Frankfurt or Virginia. The company picks a region near its customers, because a request that stays on one continent comes back in tens of milliseconds, while one that crosses an ocean can take a large part of a second there and back.

Inside each region, the provider keeps several availability zones: separate data centres, or groups of them, with their own power and network, far enough apart that one fire or power cut should not hit two. If the ticket company runs one of its everyday servers in each of two zones, losing a building leaves the other one serving. If both sit in the same zone, a failure there takes the site down, cloud or not. A rare problem affecting a whole region stops everything in it, unless the company has also copied its site and data to a second region. Spreading out is the customer's decision, and the customer pays for the extra machines.

## The whole picture

The cloud is a way of renting computers rather than owning them: providers fill data centres with physical servers, slice each one into virtual machines with a hypervisor, and let customers create and destroy those machines through an API in minutes. Because machines can come and go that quickly, a company like the ticket seller can let autoscaling grow from two servers to a hundred for a three-hour rush and pay for those hours alone, instead of buying for its busiest morning and idling the rest of the year. What it rents is the hardware and the running of it, not the care of what it puts there: under the shared responsibility model, backups, access, updates and spreading across availability zones and regions remain the customer's job, unless it rents a managed service that takes some of them over.

## Going further

- IaaS, PaaS and SaaS: labels for how much the provider runs for you, from bare virtual machines (infrastructure as a service), through managed platforms for your code (platform as a service), to finished applications such as webmail (software as a service).
- Serverless: a style of cloud service where you upload a small piece of code and the provider runs it on its own servers only when a request arrives, billing per request rather than per machine.
- Object storage: cloud storage for files of any size, kept as named items in a "bucket" rather than on a machine's disk, and the usual place where accidentally public data leaks happen.
- Egress fees: charges providers make for data sent out of their network to the internet, often a surprise on the bill for companies serving large files.

# The Cloud

By the end you will know what "the cloud" actually is underneath the phrase, why businesses moved onto it, how renting computers by the minute works, and the mistake people most often make about who is looking after what.

## The problem with owning your own machines

Take a small online shop that sells Christmas hampers. For most of the year it gets about 200 visitors an hour. In the first two weeks of December it gets around 20,000 an hour, a hundred times as many.

The website runs on a server: a computer with no screen or keyboard that sits somewhere, stays switched on, and answers requests from visitors' browsers. A visitor asks for a page, and the server sends the page back.

If the shop owns its servers, it has to decide how many to buy before December arrives. Buy enough for 200 visitors and the site collapses in the rush, on the days that bring in most of the year's money. Buy enough for 20,000 and most of that hardware sits idle for eleven and a half months, still drawing power, still needing a cool room, security updates, and someone to replace a failed disk at three in the morning.

Ordering hardware is also slow. Choosing, buying, delivering and installing a machine usually takes weeks. If a hamper goes viral on a Tuesday, new servers will not be ready by Wednesday.

That is the problem the cloud exists to solve: computing needs go up and down, but owned hardware is fixed, slow to change, and paid for whether or not it is used. The cloud's answer is to stop owning the machines and rent them instead, from a company that owns a very large number of them, for exactly as long as you need them.

So who owns all those machines, and how can they be rented out in small pieces?

## What a cloud provider actually runs

The shop's problem is that its demand swings from 200 to 20,000 visitors an hour while owned servers stay the same size. The fix starts with a company whose whole business is owning servers.

That company is called a cloud provider. It builds huge buildings, each holding tens of thousands of servers in long rows of metal racks, with industrial power supplies, cooling, and fast network links to the rest of the internet. Each building is a data centre. "The cloud" is, physically, these buildings. Nothing is floating anywhere; your files and programs sit on real disks in a real place, owned by someone else.

A provider does not usually hand you a whole physical server. Instead it splits each one into several smaller pretend computers. Special software on the physical machine divides up its processor, memory and disk, and gives each slice the appearance of being a complete, separate computer, with its own operating system and its own files. Each slice is called a virtual machine, often shortened to VM.

To the shop, a virtual machine behaves exactly like a server of its own. It can install software on it, run the website on it, and restart it. It cannot see the other virtual machines sharing the same physical box, which may belong to complete strangers. Keeping those neighbours walled off from each other is one of the provider's central jobs.

Virtual machines are what make renting in small pieces possible. A provider can carve a big server into, say, eight modest VMs for eight customers, then rearrange the slices when someone leaves, without anyone touching a cable. The physical hardware stays put; only the software boundaries move.

That explains where the machines are and how they are shared. The remaining question is how a customer actually gets one, and how quickly.

## Renting by the minute

The provider owns the buildings and splits its servers into virtual machines. What turns that into "the cloud", rather than an ordinary hosting company, is the way you rent them.

You do not phone anyone or sign a purchase order. You ask a program. Every cloud provider publishes an API, a set of instructions one program can send to another to get something done. Through it, the shop's own software, or a person clicking in the provider's web page, which uses the same API underneath, can say "give me a virtual machine with four processors and sixteen gigabytes of memory". A minute or two later it exists and is running. Another request deletes it, and it is gone.

This changes how payment works. Providers charge for what you use, measured in small units: for a virtual machine, typically by the second or by the hour; for storage, by the gigabyte per month. When you delete something, the charge for it stops. Prices and billing units vary between providers and change over time, so treat any figure as a snapshot.

Now the hamper shop can do something it never could with owned hardware. For most of the year it runs two small virtual machines, enough for 200 visitors an hour. As December traffic climbs, it adds more, until perhaps a few dozen are running during the rush. In January it deletes them. It pays for the extra machines only for the two weeks they existed.

The shop does not even have to watch the traffic itself. A provider can be told a rule such as "if the existing machines are busier than 70 percent, start another one; if they drop below 30 percent, remove one". This automatic growing and shrinking is called autoscaling. With it, a hamper going viral on Tuesday is met by new machines within minutes, not weeks.

The ability to grow and shrink like this has its own name, elasticity, and it is the property people mean when they say the cloud "scales". It is also the honest answer to "is the cloud cheaper?". For a shop whose demand swings a hundredfold, usually yes, because it stops paying for idle December capacity in June. For a workload that runs flat out, all day, every day, for years, renting can cost more than owning, which is why some large companies keep part of their work on their own hardware.

Renting a virtual machine is only one way to use a provider, though. The shop could rent a lot less, or a lot more, of the finished product, and that choice decides who is responsible for what.

## How much you rent, and who looks after it

So far the shop rents virtual machines by the minute and lets autoscaling match them to demand. But a virtual machine is a fairly raw thing to rent, and providers sell their services at three broad levels of finish.

At the rawest level, the shop rents virtual machines, storage and network connections, and installs and maintains everything on top: the operating system, the web server software, the shop's own code, its security updates. This is called infrastructure as a service, or IaaS. It is like renting an empty flat: the walls and plumbing are provided, the furniture and the locks on the cupboards are yours.

One level up, the shop hands over its code, and the provider runs it. The provider looks after the virtual machines, the operating system and their updates; the shop never logs into a server at all. This is called platform as a service, or PaaS. The shop still writes and owns the code and its data.

At the most finished level, the shop rents a complete product it uses through a browser, such as an online store builder or an accounting package, and writes no code whatsoever. This is called software as a service, or SaaS. Most people use SaaS every day without calling it the cloud: web email is the familiar case.

Here is where people most often go wrong. Because the provider owns the building, the hardware and much of the software, it is natural to assume the provider is looking after everything: that data in the cloud is automatically backed up, automatically secure, and automatically correct. It is not. Providers describe the arrangement as the shared responsibility model. The provider is responsible for the physical security of its data centres, the hardware, and the software layers it runs for you. The customer remains responsible for what it puts in and how it configures it: who is allowed to log in, whether a storage area is set to private or public, whether backups are switched on, and whether its own code has holes.

The split moves with the level you rent. With IaaS, the shop patches its own operating system; with PaaS, the provider does; with SaaS, the provider handles almost all of the software. At every level, though, the shop decides who has access and what data goes in. If someone at the shop sets the storage holding customer addresses to "public", the provider's walls, guards and cooling do nothing to stop strangers reading it. Many well-known cloud data leaks have come from exactly this kind of customer setting, not from a provider being broken into.

Backups follow the same rule. A provider typically keeps several copies of stored data so that a failed disk does not lose it, but that protects against the provider's hardware failing, not against the shop deleting the wrong thing. If the shop deletes its order history, the extra copies obediently delete it too, unless the shop arranged its own backups.

## The whole picture

The cloud is computing rented from a provider, instead of owned, so that what you pay for can follow what you need. The provider owns data centres full of physical servers and splits them into virtual machines, which lets it rent them out in small pieces to many customers at once. Customers ask for those pieces through an API, so a machine appears in minutes and disappears when deleted, and billing runs only while it exists; autoscaling turns that into a site that grows from 200 to 20,000 visitors an hour and back without anyone ordering hardware. Customers can rent at the raw level of virtual machines or at more finished levels where the provider runs more of the software, and the level they choose moves the line in the shared responsibility model. What never moves is that the customer decides who gets in and what is kept, which is why "it's in the cloud" is not the same as "it's safe".

## Going further

Regions and availability zones: providers group data centres by geography, and spreading machines across separate groups keeps a site running when one building has a power or network failure.

Serverless: a further step past PaaS where you hand over small functions and pay only for each time one runs; servers are still involved, the provider manages all of them.

Egress fees: many providers charge little to put data in but charge for moving data out to the internet or another provider, which matters when comparing costs or planning to leave.

Hybrid and multi-cloud: keeping some work on your own hardware alongside a provider, or spreading it across several providers, usually to manage cost, regulation, or dependence on one company.

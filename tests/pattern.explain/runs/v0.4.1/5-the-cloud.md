# The Cloud

By the end you will know what "the cloud" actually is underneath the phrase: how renting computers by the hour works, why it changed how software is run, and which jobs stay yours after you move in.

## The problem with owning machines

Take a small concert venue that sells its tickets through its own website. On an ordinary day the site sees about 200 visitors an hour. On the morning a famous band's show goes on sale, 20,000 people arrive in the first ten minutes, all pressing "buy" at once.

Every website runs on a computer somewhere, waiting for requests and sending back pages. A computer kept running for that purpose, usually with no screen or keyboard attached, is called a server. The venue's ticket site needs at least one.

Servers need a home: steady power, cooling, fast network connections and someone on hand when a disk fails. A building made for housing large numbers of servers is called a data centre. Before the cloud, a business either kept servers in a back room or rented shelf space in someone's data centre and installed its own machines there.

Now the venue's problem is clear. One server copes with 200 visitors an hour. The sale morning might need twenty. If the venue buys twenty, nineteen of them sit idle for all but a few days a year, still costing money and still needing repairs. If it buys one, the site collapses at the exact moment it matters most. Ordering more hardware takes weeks, so there is no way to react on the day.

The way out would be to borrow machines for the morning of the sale and hand them back at lunchtime. That is what the cloud offers, and it raises a question: how can a company lend out a computer for a single morning?

## Renting a slice of a computer

The venue needs computing power for a few hours, and physical servers are slow and expensive to buy for such short bursts. The trick that makes short-term lending possible starts inside a single machine.

A large modern server has far more processing power and memory than one small website needs. Software can divide that one physical machine into several separate, pretend computers. Each behaves exactly like a real server, with its own operating system and its own share of memory and storage, and none can see the others. One of these pretend computers is called a virtual machine, often shortened to VM.

The software that does the dividing, sitting between the hardware and the virtual machines and keeping each one in its own lane, is called a hypervisor. Because it is software, it can create a new virtual machine in seconds and delete it just as fast. No one has to walk into the data centre or plug anything in.

A company that runs huge data centres full of such machines and rents out virtual machines, storage and related services to anyone is called a cloud provider. Amazon Web Services, part of Amazon, is the largest; a handful of other large firms run similar businesses.

The last piece is how a customer asks for a machine. The provider publishes an API, a set of commands one program can send to another to get something done. The venue's developer, or a script they wrote, sends a request that amounts to "give me a virtual machine of this size in this location", and within a minute or two it is running and reachable over the internet. The provider's website offers buttons that do the same thing, but underneath, the buttons call the same API.

So the cloud, at its root, is this: computers in someone else's data centre, divided into virtual machines, handed out on request through an API, and billed for the time you hold them. That still leaves the venue to decide how many to ask for, and when.

## Growing and shrinking on demand

The venue can now rent virtual machines in minutes rather than buying servers over weeks. What makes this valuable is that it can also give them back, and that changes how it plans for the sale morning.

The ability to add capacity when load rises and remove it when load falls is called elasticity. It is the property that solves the venue's original problem: twenty machines for the busy morning, one for the rest of the year.

Someone has to decide when to add and remove machines, and doing it by hand at seven in the morning is risky. Cloud providers let you set a rule instead, such as "if the machines are more than 70 percent busy for five minutes, add another; if they are less than 20 percent busy, remove one". Machines being added and removed automatically by a rule like this is called autoscaling. On sale morning the venue's site grows from one virtual machine to about twenty as the queue builds, then shrinks back to one by early afternoon.

Twenty machines need a way to share the visitors between them. A service that sits in front of the machines, receives every incoming request and passes each one to a machine that has room, is called a load balancer. Visitors still type the venue's usual web address; they never see which of the twenty machines answered them.

The money follows the machines. Cloud providers charge for what you hold, usually by the second or the hour, rather than for owning anything. This is called pay-as-you-go pricing. A modest virtual machine typically costs somewhere between a few cents and a few tens of cents an hour, though prices vary by provider and size and change often. For the venue, twenty machines for four hours costs roughly what one machine costs for three or four days, instead of what twenty machines cost for a year.

That is the economic case for the cloud: you stop paying for capacity you might need and start paying for capacity you use. Which raises a different question. If the hardware is no longer the venue's, which of the remaining jobs still are?

## Who looks after what

The venue now rents virtual machines, lets autoscaling add and remove them, and pays only for the hours it uses. The provider clearly owns the buildings and the hardware. Everything above that can be split in different ways, and providers sell their services at different levels of that split.

At the lowest level, the provider gives you virtual machines, storage and networking, and you install and run everything else: the operating system updates, the web software, the ticketing program itself. This level is called infrastructure as a service, or IaaS. It is what the venue has been using so far.

One level up, the provider also runs the operating system and the supporting software, and you hand over only your own program. You upload the ticketing code; the provider keeps the machines underneath patched and running. This is called platform as a service, or PaaS. The venue would no longer think about virtual machines at all, only about its application.

At the top, the provider runs the whole application and you only use it, through a browser or an app. Email services and online document editors work this way. This is called software as a service, or SaaS. If the venue gave up its own site and sold tickets through an existing ticketing service, it would be a SaaS customer.

Here is where people most often go wrong. It is tempting to think that once something is "in the cloud", the provider takes care of it entirely: security, backups, all of it. It does not. Cloud providers describe the split with what is called the shared responsibility model: the provider is responsible for the security of the cloud, meaning the buildings, hardware and the layers it runs; the customer is responsible for security in the cloud, meaning everything it puts there and configures.

For the venue on IaaS, that means the venue, not the provider, must install security updates on its virtual machines, decide who may log in, and set up backups of its ticket database. If a developer leaves a storage area holding customer details open to the whole internet, the provider's hardware has done its job perfectly and the data is still exposed. Many well-publicised cloud data leaks have been of this kind: a customer's setting, not a provider's failure. Moving up to PaaS or SaaS hands more of the list to the provider, but some items, such as who has access and what data is stored, always stay with the customer.

A second, smaller trap sits next to the first. The cloud is not automatically cheaper. It is cheaper for load that rises and falls, like the venue's, and for businesses that would otherwise buy hardware they cannot keep busy. For a workload that runs flat out every hour of every year, owning the machines can cost less, which is why some large companies run a mix of both.

## The whole picture

The cloud is renting computing from a provider's data centres instead of owning it, and each piece covered here supports that. Hypervisors divide large physical servers into virtual machines, which can be created and destroyed in seconds. An API lets customers ask for those machines on demand, so capacity arrives in minutes rather than weeks. Elasticity and autoscaling let the number of machines follow the load, a load balancer spreads visitors across them, and pay-as-you-go pricing means the bill follows the machines. The services come at three levels, IaaS, PaaS and SaaS, and the higher you go the more the provider runs for you. At every level, the shared responsibility model leaves part of the work, especially access and data, with you. For the concert venue, that adds up to twenty machines for one frantic morning, one for the rest of the year, and a security checklist that never moves to someone else entirely.

## Going further

- Regions and availability zones: providers group data centres into geographic regions, each split into separate sites, so you can place machines near your users and survive the loss of one building.
- Serverless: a style of PaaS where you upload small functions and pay per run; servers still exist, but the provider handles them completely.
- Egress fees: many providers charge for data leaving their network, a cost that often surprises new customers.
- Hybrid and multi-cloud: running some systems on your own hardware alongside the cloud, or spreading work across more than one provider.

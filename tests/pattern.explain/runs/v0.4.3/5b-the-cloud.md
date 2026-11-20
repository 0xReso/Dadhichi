# The Cloud

By the end you will know what the cloud actually is, why businesses moved onto it, how renting a computer by the minute works underneath, and which jobs it leaves in your hands.

## The problem with owning computers

Think of a theatre that sells its tickets through its own website. On an ordinary day a few hundred people visit, and two servers, computers whose job is to answer requests from visitors' browsers, handle that comfortably. Then a popular show goes on sale at nine in the morning and twenty thousand people arrive in the first hour. Two servers cannot answer them all. The site slows to a crawl, then stops responding, and the theatre loses sales and goodwill in the same morning.

If the theatre owns its machines, the fix is to buy enough for the worst morning of the year. Say that means forty servers. They have to be ordered, delivered, installed in a room with enough power and cooling, and kept running by someone who knows how. That takes weeks and a large sum up front. For the rest of the year, thirty-eight of them sit humming in the back room, doing nothing and still drawing electricity.

That waste is the problem the cloud exists to solve. The cloud is computing, meaning servers, storage, and networking, that you rent from a company that owns enormous amounts of it, reach over the internet, start within minutes, and pay for only while you use it. The theatre stops buying computers for its busiest hour and starts renting them for that hour.

To see how that can work, start with where the rented computers live.

## Someone else's building

The theatre's trouble is owning machines sized for a peak that rarely comes, and the cloud's answer is to rent instead. The rented machines still have to sit somewhere physical.

They sit in a data centre: a warehouse-sized building filled with rows of tall metal racks, each rack holding dozens of servers stacked like flat drawers. The building has its own power supply with backup generators, industrial cooling to carry away the heat, and fast fibre connections to the rest of the internet. A large one holds tens of thousands of servers.

The company that owns these buildings and rents out what is inside is called a cloud provider. A provider runs many data centres across countries and continents and buys servers by the hundred thousand, so each machine costs it far less to buy and run than one would cost the theatre.

So far this sounds like ordinary renting, like hiring a car. The difference is that the theatre never touches, sees, or is even handed a whole physical machine. How can one company give out computers to thousands of customers within minutes, with nobody carrying boxes around?

## One machine, many computers

The rented computing lives in a provider's data centre. What lets the provider hand it out in minutes is software that makes one physical server behave like many separate ones.

A modern server is very powerful, with dozens of processor cores and hundreds of gigabytes of memory, and most programs, the theatre's website included, need only a small slice of that. So the provider runs a layer of software on each server that divides its processors, memory, and disk into walled-off portions and presents each portion as a complete computer. That layer is called a hypervisor.

Each of those portions is called a virtual machine, usually shortened to VM. To the theatre's software, a VM looks exactly like a real server. It has its own operating system, the base software such as Linux or Windows that programs run on, along with its own files and its own network address. It cannot see the other VMs sharing the same physical box, and they cannot see it. One server in the data centre might be running VMs for a bank, a game studio, and the theatre at the same moment.

This is why starting a server in the cloud takes about a minute rather than weeks. Nobody installs hardware. The hypervisor on some machine with spare room carves out a new portion and boots an operating system inside it. Shutting the VM down hands that portion back, ready for the next customer.

With machines that appear and vanish this quickly, the remaining question is how the theatre asks for them and how it gets charged.

## Renting by the minute

The theatre's rented servers are VMs, carved out of a provider's hardware in a data centre and ready in about a minute. Now it needs a way to request them at the right moment.

Every provider offers an API, a published set of commands that one program can send to another to ask it to do something. Through the provider's API, the theatre's own software can say "start three more VMs of this size" or "shut that one down", with no person clicking anything. Every action in the cloud, from creating a VM to deleting a file, is in the end a request to this API; the provider's website is a friendlier face on the same commands.

Because machines can be requested and returned this quickly, the theatre's capacity can follow its traffic instead of being fixed in advance. This property is called elasticity: the system stretches when demand rises and shrinks back when it falls.

In practice nobody watches the traffic and types commands at nine in the morning. The theatre sets a rule with the provider, such as "when the servers are more than 70 per cent busy, add another VM; when they fall below 30 per cent, remove one." The provider checks the numbers every minute or so and calls its own API to apply the rule. This is called autoscaling. On sale morning, the theatre's two VMs become forty within minutes of the rush starting, and drop back to two once it ends.

The bill follows the same pattern. Providers charge for VMs by the hour, minute, or second they are running, and for storage by how much is kept each month. The figures here are illustrative, because real prices vary by provider, machine size, and location and change often. Suppose a VM the theatre needs costs about ten cents an hour. The thirty-eight extra machines for a two-hour rush cost 38 times 2 times ten cents: around seven dollars and sixty cents. Buying those same thirty-eight servers outright would have cost thousands of dollars each.

The same meter that makes the rush cheap also has an edge. The provider charges for a VM while it runs, whether or not it is doing useful work. If someone at the theatre starts a VM to test something and forgets it, ten cents an hour adds up to roughly seventy-two dollars by the end of a thirty-day month, for a machine that served nobody. Elasticity saves money only when machines are actually returned.

Cheap, quick, and someone else's hardware: it is tempting to conclude that the provider now takes care of everything. Does it?

## What stays your job

The theatre now rents VMs through an API, lets autoscaling add and remove them, and pays only for the hours they run. Because the provider owns all the hardware, a common belief follows: that anything put in the cloud is automatically secure, backed up, and kept running.

It is not. The cloud is still a set of computers, just ones owned by someone else, and the work of looking after them is split in two. The provider is responsible for the building, the power, the physical servers, the network between them, and the hypervisor. The customer is responsible for everything inside its own VMs and accounts: installing security updates on the operating system, choosing who is allowed to log in, setting passwords and permissions, and keeping copies of important data. This division is called the shared responsibility model, and the major providers publish it in their own terms.

Here is what that means for the theatre. If its database of customer emails is left open to the whole internet by a wrong setting, the provider has not failed; the theatre's setting did exactly what it said. If an employee deletes a VM along with its data, the provider will not bring it back unless the theatre had already set up backups, which providers sell as an option the customer has to switch on. Many of the data leaks reported as "cloud breaches" are of this kind: a customer's own setting, not a fault in the provider's hardware.

Placement is part of the customer's job too. A data centre can lose power or network like any building. If all of the theatre's VMs sit in one data centre and that building has an outage, the site goes down with it, however healthy the provider's other buildings are. Providers run separate data centres close enough to work together, and spreading VMs across them keeps a site running through the loss of one, but the customer has to choose to do that.

## The whole picture

The cloud is renting computing instead of owning it, and it exists because owning means paying in advance for a peak that rarely comes. The pieces stack in order. Cloud providers own data centres full of servers. Hypervisors slice each server into virtual machines that can be created and returned in about a minute. An API lets the customer's own software request and release those machines, which makes elasticity possible, and autoscaling applies it automatically, while metered billing turns that elasticity into a bill that follows real demand. The provider keeps the building and hardware running; the customer still owns the security, the backups, and the placement of everything it builds on top.

## Going further

- IaaS, PaaS, and SaaS: three levels of renting, from raw virtual machines you manage yourself, through platforms that run your code for you, to finished applications such as web email used through a browser.
- Regions and availability zones: the provider terms for a geographic area of data centres and for the separate buildings inside it that you spread VMs across.
- Serverless: a way of renting where you upload a single piece of code and the provider runs it on demand, so you never manage a VM at all, though servers still run it underneath.
- Amazon Web Services, Microsoft Azure, and Google Cloud: the three largest cloud providers, whose documentation uses all of the terms above.

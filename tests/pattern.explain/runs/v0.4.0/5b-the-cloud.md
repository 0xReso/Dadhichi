# The Cloud: Renting Computers Instead of Owning Them

By the end you will know what "the cloud" actually is underneath, why businesses moved onto it, how renting a computer by the hour works, and which part of the job still stays with you.

## The problem with owning servers

In IT, "the cloud" means computing power, storage and software that you rent over the internet from a company that owns and runs the machines, instead of buying and running those machines yourself. To see why that arrangement exists, it helps to start with a business that does own its machines.

Take a small online tea shop. Its website runs on one server, a computer whose only job is to answer requests from visitors' browsers. The shop bought it for about €3,000 and keeps it in a cupboard in the back office, plugged into the mains and the office internet line.

On an ordinary day the site gets about 200 visitors an hour, and the server barely notices. Then comes the November sale. For three days traffic jumps to around 5,000 visitors an hour, twenty-five times the usual load. The single server cannot keep up: pages take ten seconds to load, then stop loading at all, and customers leave with their baskets full.

The obvious fix is to buy more servers. But the shop then faces a choice with no good answer. Buy enough machines for the sale, and for the other 362 days of the year they sit almost idle, costing money and electricity. Buy enough for an ordinary day, and the sale breaks the site again. Planning how many machines you will need, months ahead, is called capacity planning, and for a business whose traffic swings this much it is mostly guesswork.

There are smaller problems on top. A new server takes days or weeks to order, deliver and set up. When a disk fails at two in the morning, someone at the shop has to notice and replace it. The cupboard gets hot. None of this is what the shop is in business to do. What it really wants is to have twenty-five servers for three days and one server the rest of the time, and to pay only for what it uses.

## Data centres and virtual machines

So the shop's problem is that owning machines forces it to guess its needs in advance and pay for that guess all year. The cloud answers this by letting someone else own the machines at enormous scale and rent slices of them out by the minute.

The first piece is the building. A cloud provider runs data centres: warehouse-sized buildings holding tens of thousands of servers in racks, with their own power supplies, backup generators, cooling and very fast network connections. The provider employs the people who replace failed disks at two in the morning. Underneath every cloud service there is always a physical computer in one of these buildings. The cloud is not somewhere vague; it is a specific machine in a specific place that you do not have to look after.

The second piece is what lets one physical server be shared safely between many customers. A layer of software called a hypervisor runs directly on the hardware and divides it into several separate, self-contained computers. Each one gets its own share of the processor, memory and disk, runs its own operating system, and cannot see the others. Each of these slices is called a virtual machine, usually shortened to VM. To the shop, a VM behaves exactly like the server in the cupboard: it can log in, install the website and serve visitors. It never sees the physical box, and it may share that box with a bank, a game studio and a stranger's hobby project.

The third piece is how you get a VM. You do not phone anyone or sign a contract. You fill in a form on the provider's website, or a program sends a request to the provider's API, the published interface through which one program asks another to do something. The request says, in effect, "give me a machine with two processors and 4 gigabytes of memory, running Linux". About a minute later the VM is running and has an internet address. Another request deletes it, and billing stops. Being able to create and remove machines yourself, on demand, is the defining feature of the cloud; renting a server for a year from a hosting company, by contrast, is not really cloud computing.

The fourth piece is the bill. Cloud providers charge for what you use, measured finely: VMs by the second or the hour, storage by the gigabyte per month, network traffic by the gigabyte sent. A small VM costs somewhere in the range of a few cents an hour, though prices vary by provider and size and change over time.

Now the tea shop's problem dissolves. It moves its website to one VM. On the morning the sale starts, it creates twenty-four more and spreads visitors across all twenty-five. When the sale ends, it deletes the extra twenty-four. It has paid for twenty-five machines for three days and one machine for the rest of the year. This ability to grow and shrink with demand is called elasticity, and it is the main reason businesses moved to the cloud.

The provider's data centres are grouped by geography. A region is a cluster of data centres in one area, such as Frankfurt or northern Virginia, and when you create a VM you choose the region it runs in. The tea shop's customers are mostly in Germany, so it picks a European region: a request from Berlin to Frankfurt and back takes around 10 milliseconds, while a round trip to Virginia takes closer to 100, a delay a visitor can start to feel when it repeats across a page that loads dozens of files. The region also decides which country's laws the stored data sits under, which matters for privacy rules.

The largest provider is Amazon Web Services, usually called AWS, which started renting VMs this way in 2006. The other big providers offer the same basic model under different product names, so the ideas here carry across.

Renting raw VMs solves the capacity problem, but the shop still has to install, patch and run everything on them, which raises the question of how much more of the work it can hand over.

## How much you rent: three layers

The tea shop now runs on rented virtual machines that it can add and remove in minutes, paying only while they run. Providers sell more than bare machines, though, and the main thing that separates their offerings is how much of the work they take off your hands.

At the bottom is what the shop is already using. When you rent VMs, storage and network and manage everything that runs on them yourself, that is called infrastructure as a service, or IaaS. The provider looks after the hardware and the hypervisor. The shop chooses the operating system, installs security updates, sets up the web server software and keeps its database running. It has the most control here, and the most chores.

One step up, the provider runs the software as well as the machine. The shop's product catalogue and orders live in a database, and keeping a database healthy means updates, backups and failover to a spare copy when something breaks. Instead, the shop can rent a managed database: it asks for one through the API, gets an address to connect to, and never logs in to the machine underneath. Services like this, where you bring your own code or data and the provider runs the platform it sits on, are called platform as a service, or PaaS.

At the top, you rent a finished application that you use through a browser. The shop's email, its accounting package and its video calls are all programs it never installs or runs anywhere; it pays a monthly fee per user and logs in. That is software as a service, or SaaS, and it is the layer most people mean when they say their files are "in the cloud".

The three layers sit on the same foundation. A SaaS email product is itself built on VMs and databases in someone's data centre; the layers only differ in where the line falls between the provider's work and yours. And that line is exactly where most cloud misunderstandings start.

## What the provider does not do for you

The tea shop now knows that the cloud is rented machines in a provider's data centres, created through an API and billed by use, offered at several layers depending on how much work it wants to hand over. The tempting next thought is that once something is in the cloud, the provider is keeping it safe. That is the most common misunderstanding of the whole topic.

Providers divide the job explicitly, and the division is called the shared responsibility model. The provider is responsible for security of the cloud: the buildings, the guards, the hardware, the network between data centres and the hypervisor that keeps one customer's VM from reaching another's. The customer is responsible for security in the cloud: who has accounts, how strong their passwords are, which network ports are open, what data is stored and who is allowed to read it. The higher the layer you rent, the more the provider covers, but the customer's accounts and data are always the customer's job.

Here is how that plays out for the tea shop. It stores its product photos and a weekly export of customer orders in the provider's file storage. Whoever set it up ticked "public" so the photos would show on the website, and the order exports, sitting in the same place, became readable by anyone with the address. Nothing was hacked and the provider did nothing wrong; the setting did what it said. Most cloud data leaks reported in the press are mistakes of this kind, a wrong setting on the customer's side, rather than a break-in at the provider.

Backups follow the same rule. When the shop deletes a VM, its disk is deleted with it. If an employee deletes the orders database by mistake, a managed database will usually have recent automatic backups the shop can restore from, but only if backups were switched on and kept long enough, which is the shop's choice. Storing something in the cloud means it lives on someone else's well-run hardware; it does not mean a second copy exists unless someone arranged one.

The bill follows the same rule too. Elasticity cuts both ways: if the shop forgets to delete its twenty-four extra VMs after the sale, they keep running, and keep charging, all through December. The cloud is cheaper than owning hardware when usage swings and machines are switched off when idle; for a workload that runs flat out all year, owning can cost less.

## The whole picture

The cloud is computing you rent rather than own: providers build data centres full of physical servers, a hypervisor splits each server into isolated virtual machines, and an API lets you create and delete those machines, or higher-level services built on them, in about a minute, paying only while they run. That turns the tea shop's impossible guess about how many servers to buy into a decision it can make on the morning of the sale and undo when the sale ends. What it does not do is take over the shop's own part of the job: the provider secures the buildings, hardware and hypervisor, while accounts, settings, backups and the bill stay with the customer at every layer.

## Going further

- Autoscaling: a provider feature that adds and removes VMs automatically based on load, so the tea shop would not have to start its twenty-four extra machines by hand.
- Serverless: a model where you upload a small piece of code and the provider runs it only when a request arrives, billing per request; the code still runs on servers, which the provider manages entirely.
- Private and hybrid cloud: running the same self-service, virtual-machine model in your own data centre, or combining it with a public provider.
- Egress fees: the charge many providers make for data sent out of their network, often the surprise line on a first cloud bill.

# The Cloud, Underneath

By the end you will know what "the cloud" actually is in computing: who owns the machines, how they get shared, what you rent, and what stays your job.

## The problem with owning machines

Take a small company called Gigstub that sells concert tickets online. On an ordinary day, about 200 people are on its website at once, and two servers in a rented cupboard handle that comfortably. A server here means a computer whose only job is to answer requests from other computers: someone's phone asks for the seating map, and the server sends it back.

Then a famous band announces a tour, and tickets go on sale at 10 a.m. on a Friday. For the next two hours, 20,000 people hit the site at once, a hundred times the usual load. Two servers cannot cope. Pages time out, the checkout fails, and fans go to a competitor.

Gigstub's old options were both bad. It could buy enough machines for the peak, perhaps forty servers, and leave thirty-eight of them sitting idle for all but a few hours a year. Or it could buy for the ordinary day and fall over every time something exciting happened. Either way, buying a server meant ordering hardware, waiting weeks for delivery, finding space, power, and cooling for it, and paying for all of that whether the machine was busy or not.

The cloud is the answer to that bind. A handful of very large companies build enormous buildings full of servers, called data centres, and rent pieces of them out to anyone, by the minute or even by the second, through a website or a program. The big three are Amazon Web Services (usually shortened to AWS), Microsoft Azure, and Google Cloud. Gigstub stops owning machines and starts renting computing the way a household rents electricity: it uses what it needs and pays for what it used.

The phrase "someone else's computer" is a fair joke about this, and it is half right. The other half, the part that makes it work, is how a provider turns one physical machine into many rentable ones without its customers getting in each other's way.

## How one machine becomes many

A single physical server in a modern data centre is far more powerful than most customers need. It might have dozens of processor cores and hundreds of gigabytes of memory. Renting out whole machines would waste most of that, so providers slice each one up.

The slicing is done by a layer of software that sits directly on the hardware and pretends to be several separate computers at once. Each pretend computer gets its own share of processor time, its own portion of memory, and its own slice of disk, and runs its own operating system as if it owned the machine. The pretend computer is called a virtual machine, or VM, and the software that creates and polices them is called a hypervisor.

The hypervisor's most important job is isolation. Gigstub's virtual machine might share a physical box with a bank's and a games studio's, and none of them can see into the others' memory or files. To each customer, a virtual machine looks and behaves like a real server they own.

Because a virtual machine is made of software, creating one is a matter of seconds to a couple of minutes rather than weeks. Gigstub's engineer picks a size, such as "4 processor cores and 16 gigabytes of memory", picks an operating system, and the provider finds a physical machine with room and starts it there.

The engineer also picks a region: the geographic area whose data centres will run the machine, such as Frankfurt or Northern Virginia. This matters because distance costs time. A request from London to a server in Frankfurt and back takes roughly 15 to 20 milliseconds, far quicker than a blink, while the same round trip to Sydney takes around 250 milliseconds, a quarter of a second, and that delay repeats for every request a page makes. Gigstub sells mostly to European fans, so it chooses a European region.

None of this needs a person clicking through a website. Every cloud provider offers an API, a published way for one program to ask another to do something. A program can send the provider a request that says "start ten more virtual machines like this one" or "shut these three down", and the provider does it. This is what makes the cloud more than a cheaper way to rent servers: the infrastructure itself can be controlled by code.

Gigstub uses that. It sets a rule with the provider: keep at least two virtual machines running, and whenever their processors are more than 70 percent busy, add more, up to forty; when they calm down, remove the extras. This is called autoscaling. On Friday at 10 a.m., the busy signal climbs, the provider starts machine after machine, and a few minutes later forty are sharing the traffic. By lunchtime they have been shut down again.

The bill follows the machines. Most providers charge for a running virtual machine by the hour or by the second, and the price depends on its size; at the time of writing, a small general-purpose machine costs somewhere in the region of a few cents to a few tens of cents an hour, though prices change often and differ between providers. Gigstub pays for forty machines for two hours and two machines for the rest of the month. The general idea of capacity that grows and shrinks with demand is called elasticity, and it is the main thing the cloud sells.

Elasticity is a good deal for spiky traffic like Gigstub's. For a workload that runs flat out every hour of every day, renting can end up costing more than owning, which is why some large companies keep their steady work on their own hardware.

Gigstub now has servers that appear and vanish on demand. That raises a practical question: how much of the work on those servers is still Gigstub's to do?

## What you rent, and what stays yours

So far Gigstub has been renting bare virtual machines that grow and shrink with its ticket sales, and it controls them through the provider's API. Those machines are only one of the ways to rent from the cloud, and the choice decides how much work Gigstub keeps for itself.

The bare virtual machine is the lowest level. The provider supplies the hardware, the network, and the hypervisor; Gigstub installs and updates the operating system, the database software, its own ticketing code, and everything else. This level is called infrastructure as a service, or IaaS. It gives the most control and leaves the most chores.

One level up, the provider also runs the operating system and the supporting software, and Gigstub hands over only its own code. It says, in effect, "here is my ticketing program, keep it running", and the provider takes care of the machines underneath, including how many there are. This is called platform as a service, or PaaS. The popular label "serverless" belongs to this family: the code still runs on servers, but Gigstub never sees or manages them, and it pays only while its code is actually handling a request.

At the top, the provider runs the whole application, and the customer just uses it through a browser. Gigstub's staff email through Gmail or Microsoft Outlook and keep their accounts in a hosted bookkeeping tool. Nobody at Gigstub installs anything. This is software as a service, or SaaS, and it is the part of the cloud most people meet every day without thinking of it as the cloud at all.

The three levels are best read as a line drawn at different heights. Everything below the line is the provider's job; everything above it is the customer's. IaaS draws the line low, SaaS draws it high.

That line is where the most common misunderstanding lives. Many people assume that once something is "in the cloud", the provider keeps it safe, backed up, and secure. Providers call the real arrangement the shared responsibility model, and it says the opposite: the provider secures what is below the line, and the customer is responsible for everything above it.

For Gigstub on IaaS, that means AWS or Azure guarantees that nobody walks into the data centre and pulls out a disk, and that the hypervisor keeps other customers out of Gigstub's machines. It does not patch Gigstub's operating system, choose strong access rules, or back up its database unless Gigstub sets that up. If an engineer stores the customer list in cloud storage and leaves it readable by anyone on the internet, the provider has done its part correctly and the data still leaks. Misconfigured storage of exactly this kind is behind a large share of real cloud data breaches.

Even at the SaaS level, some responsibility stays with the customer. The provider runs the email service, but Gigstub still decides who gets an account, whether those accounts require a second login step, and what happens when someone leaves the company.

## The whole picture

Gigstub stopped buying servers for its busiest day and started renting slices of a provider's data centres instead. Hypervisors carve each physical machine into isolated virtual machines; an API lets programs create and destroy them in minutes; autoscaling uses that to match the number of machines to the crowd, and billing by the hour or second means Gigstub pays only for the crowd it actually had. On top of that, it can choose how much of the stack to rent, from bare machines to finished applications, knowing that wherever it draws that line, everything above it is still its own job. That is the cloud: computing owned by a few large providers, rented on demand through software, paid for by use, with responsibility split between provider and customer at a line the customer chooses.

## Going further

Availability zones: separate data centres within one region, with independent power and networking, so an application spread across two or three of them survives one building failing.

Containers: a lighter way than virtual machines to package and isolate a program, sharing the host's operating system; Kubernetes is the widely used system for running many of them across a fleet of machines.

Object storage: the cloud's standard way to store files of any size cheaply and durably, such as Amazon S3, and the usual home of the misconfigured, publicly readable data mentioned above.

Public, private, and hybrid cloud: renting from a shared provider, running the same kind of self-service setup on your own hardware, or combining the two.

# The Cloud: Renting Computers Instead of Owning Them

By the end you will know what the cloud is underneath the phrase, why businesses moved to it, how renting computing through it actually works, and what it does not take off your hands.

## The problem with owning servers

Picture a website that sells tickets for a concert venue. On an ordinary day about 200 people an hour browse it. When a famous band announces a show, 20,000 people arrive in the first ten minutes.

A website runs on a server: a computer that waits for requests from browsers and sends pages back. One server copes with the ordinary day easily. The on-sale morning needs something like fifty.

For decades the answer was to own the servers. A business bought machines, placed them in a rented rack in a building with power, cooling and a fast internet connection, and kept staff to install, repair and update them. Ordering new hardware took weeks. So the venue had to guess its busiest moment in advance and buy for it. Buy fifty, and forty-eight of them sit idle almost every day of the year, still costing money. Buy five, and the site falls over on the one morning that matters most.

The cloud exists to remove that guess. Instead of owning computers, you rent computing from a company that owns enormous numbers of them. You ask for more when you need it, hand it back when you do not, and pay only for what you held. The company doing the renting is called a cloud provider.

A provider cannot put a physical machine in your hands in seconds, though. So what is it actually giving you?

## Slices of someone else's machines

Owning servers forces you to buy for your busiest day, and the cloud promises to rent computing as you need it instead. The first question is what exactly is being rented.

A cloud provider runs data centres: warehouse-sized buildings that each hold many thousands of servers, with their own power supply, backup generators, cooling, and several high-speed links to the rest of the internet. The physical hardware stays there. You never see it.

What makes quick renting possible is virtualization: making one physical computer behave as several separate computers at once. A big modern server has far more processors and memory than one small website needs, so it makes sense to share it out.

The software that does the sharing is called a hypervisor. It runs directly on the physical machine and divides its processors, memory and disk among several guests, keeping each one walled off from the rest, so no guest can see or touch another's memory or files.

Each of those guests is a virtual machine, usually shortened to VM. From the inside a VM looks like an ordinary computer, with its own operating system, its own files and its own network address. The venue's website runs inside one. It does not know, and does not need to know, that the same physical server may also be running VMs that belong to a bakery and an insurance company.

A block of flats is a fair comparison: one building, shared walls and plumbing, a separately locked front door for each household. The comparison stops at size and speed. A flat is built once and stays the same shape, while a VM can be created, resized or destroyed in a minute or two.

That speed comes from the fact that a VM is only software. Creating one means the provider picks a physical server with spare room, the hypervisor sets aside a slice of it, copies in a ready-made disk image containing an operating system, and starts it. Nobody drives anywhere with a box. People sometimes joke that the cloud is "just someone else's computer", and up to this point that is fair. What the joke leaves out is how you get hold of that computer.

Being able to make a VM in a minute is half the story. How do you ask for one, and how do fifty appear on the right morning without anyone staying up to click buttons?

## Asking by program, paying by the hour

You now hold the picture of virtual machines, carved out of physical servers in a provider's data centre and created in minutes. What turns that into something a business can lean on is how they are requested and paid for.

You request a VM through an API, the published way one program asks another to do something. The provider's website has buttons, but behind every button is an API call, and your own programs can make the same calls. A request says, in effect, "start a machine with four processors and 16 gigabytes of memory, from this disk image", and the response comes back with the new machine's address. No person at the provider reads it or approves it.

Because machines can be requested by a program, they can be requested automatically. You set a rule: when the average processor load across your web servers passes 70 per cent, start another one; when it falls below 30 per cent, remove one. This automation is called autoscaling.

The property autoscaling gives you, capacity that stretches and shrinks with demand, is called elasticity. On the venue's on-sale morning, the count climbs from two servers to fifty within minutes as visitors pile in, and by the afternoon it has drifted back down to two.

Fifty servers are no use if every visitor lands on the first one. In front of them sits a load balancer, a component that receives every incoming request and passes it to whichever server currently has room. When autoscaling adds a VM, the load balancer starts sending it traffic; when a VM is removed, the load balancer stops.

The last piece is billing. Cloud providers charge for what you use, measured by the hour or by the second depending on the provider and the service. This is called pay-as-you-go. To make it concrete with a round, illustrative price of 10 cents an hour per VM: running two machines all year costs about 1,750 dollars, and the fifty-machine burst for four hours on sale morning adds about 20 dollars. Owning fifty machines for that one morning would cost many times more.

The arithmetic does not always favour renting. Hour for hour, a rented machine generally costs more than an owned one you keep busy all the time, which is why some companies with steady, predictable load still run their own hardware. The cloud wins most clearly when demand swings, or when nobody can predict it.

So far the venue has rented bare machines and looked after everything on them itself: the operating system, the web software, the database. Does it have to?

## How much you hand over

The venue now rents VMs through an API, lets autoscaling add and remove them, and pays by the hour. But each of those VMs still needs its operating system updated, its software installed, and its database looked after by someone on the venue's staff.

Providers sell services at different levels, from bare hardware up to finished applications, and the higher the level, the more of the work the provider takes on. Three standard names describe these levels, and you will hear them constantly.

The first is Infrastructure as a Service, or IaaS: renting raw building blocks such as VMs, disks and networks. The provider looks after the buildings, the hardware and the hypervisor; you look after everything from the operating system upward. This is what the venue has been doing so far.

The second is Platform as a Service, or PaaS: you hand over your code or your data, and the provider runs the machinery underneath it. Suppose the venue moves its ticket database onto a managed database service. The provider now installs the database software, applies security updates, takes nightly backups and keeps a standby copy ready if a machine fails. The venue still designs the tables and decides which programs may read them.

The third is Software as a Service, or SaaS: a finished application you use through a browser. The venue's staff read their email in a hosted email service. The provider runs all of it; the venue manages only its user accounts and its own messages.

This is where the most common misunderstanding lives: "it is in the cloud, so security and backups are the provider's problem." Providers describe the real arrangement as the shared responsibility model. The provider is responsible for the security of the cloud: its buildings, hardware, hypervisor and network. You are responsible for security in the cloud: what you put there, who you let in, and how you configure it. The higher the level you rent, the more moves to the provider's side, but some always stays on yours.

A concrete case: cloud storage services keep files in named containers called buckets, and each bucket has a setting for who may read it. If the venue saves a spreadsheet of ticket buyers' names and addresses into a bucket and sets it to public by mistake, anyone who finds the address can download it. The provider's systems worked exactly as instructed. Many real data leaks have been of this kind. Backups follow the same pattern: a managed database may back itself up, but a VM's disk is generally not backed up unless you arrange it, and if your own program deletes your data, the cloud faithfully deletes it.

## The whole picture

The cloud is computing you rent instead of own. Providers fill data centres with physical servers, and virtualization lets a hypervisor carve each one into virtual machines that can be created in a minute or two. Because those machines are requested through an API rather than by a person, they can be requested automatically, which gives autoscaling and elasticity, and because they are billed by the hour or second, a burst of fifty servers for one morning costs about what that morning uses. On top of raw machines, providers sell higher levels, IaaS, PaaS and SaaS, each taking more of the work off your hands. What never moves entirely to the provider is responsibility for your own data and settings, so the venue that stopped guessing its peak still has to decide who may read its ticket list.

## Going further

Regions and availability zones: providers group data centres by geographic area and into separate failure domains, so you can spread your machines out and survive a building going dark.

Containers and Kubernetes: a lighter way than VMs to package and run applications, sharing one operating system, with Kubernetes as the common system for running many containers across many machines.

Serverless: a model where you hand over individual functions and pay per call; servers still run your code, but you never see or manage them.

Egress fees and lock-in: providers often charge for data leaving their network, and the more of one provider's services you use, the harder it becomes to move elsewhere.

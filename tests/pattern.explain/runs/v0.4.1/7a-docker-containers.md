# Docker Containers

By the end you will see that a Docker container is an ordinary Linux process with a restricted view of the machine, and know how that view is built.

## The problem: it works on my machine

Say you have written a small web service called orders. It needs Python 3.12, a C library for talking to PostgreSQL, and a dozen Python packages at exact versions. On your laptop it runs. The production server has Python 3.8, a different version of that C library, and another team's service that needs the old packages. Installing yours would break theirs.

The traditional answers are painful. You can carefully script every server so they all match, and watch them drift apart anyway. Or you can give each service its own virtual machine, a whole simulated computer with its own operating system kernel, which costs gigabytes of memory and tens of seconds to boot for every service.

Docker is a tool that takes a third route. It packages your service together with every file it needs, then runs it as a normal process on the host, but a process that sees only that package and is kept apart from everything else. That running, fenced-off process is a container.

## The image: everything the process will see

The fix for "it works on my machine" is to ship the machine's files along with the program. Docker does this with an image.

An image is a complete filesystem, frozen: a minimal Linux userland, Python 3.12, the PostgreSQL library, your packages, and your code, all under one root directory, plus a note saying which command to run at start. It contains no kernel. You give it a name and a version label, such as orders:1.0, and the same image can be copied to any host and will contain exactly the same bytes there.

You build an image from a short text recipe called a Dockerfile. Each line is one step: start from an official Python 3.12 image, copy in the list of packages, install them, copy in the code, set the start command.

Each of those steps produces a layer, a set of file changes stacked on the layer below. The image is the stack, read from top to bottom like transparent sheets laid over each other. Layers are shared: if ten images start from the same Python base, the host stores that base once. And if you change only your code, only the last layer is rebuilt, which is why rebuilding usually takes seconds.

So you now have orders:1.0 on the production server, a frozen filesystem holding everything the service needs. What happens when you tell Docker to run it?

## Starting a container: a process with a private view

You have an image, a frozen filesystem that holds the whole service. Now you run it:

```
docker run -p 8080:8000 --memory 512m orders:1.0
```

The last word names the image. The `-p 8080:8000` part says that traffic arriving at port 8080 on the server should reach port 8000 inside the container. The `--memory 512m` part caps the container at 512 megabytes of memory. Each of these maps onto a Linux kernel feature you may already have met.

The `docker` command does not do the work itself. It sends the request to the Docker daemon, a background service on the host that manages images and containers. The daemon sets things up and then asks the kernel to start your service's start command as a new process.

The key feature it uses is the namespace. A namespace is a kernel mechanism that gives a process its own private copy of one kind of system resource, so that it sees only the members of that copy. There are several kinds, and a container gets a fresh one of most of them. Three matter for orders.

The first is the mount namespace. It gives the process its own table of mounted filesystems. Docker uses it to make the image's files the root directory of the process, so when orders opens /usr/bin/python3 it gets Python 3.12 from the image, never the host's Python 3.8. The other team's service, with its own image, sees its own files at the same paths.

The second is the PID namespace, PID being the process ID. Inside it, numbering starts again from 1. Your Python process believes it is PID 1, and running `ps` inside the container shows only it and its children.

This is where the common mistake lives. Because a container has its own files, its own process list, and its own hostname, people picture it as a small virtual machine. It is not. There is no second kernel and no simulated hardware. On the host, `ps` shows your service as an ordinary process, say PID 48213, owned by the host kernel, scheduled like any other, and visible to `top` and `strace` and `kill`. PID 1 is the same process under a second number, the one its namespace hands out. That is why a container starts in a fraction of a second, about as fast as the program itself, and why it costs little more memory than the process would use anyway.

The third is the network namespace. It gives the process its own network interfaces, its own IP address, and its own ports. Your service listens on port 8000 without colliding with anything else on the host that uses 8000. Docker connects that private network to the host through a virtual network link, and the `-p 8080:8000` option adds a forwarding rule so outside traffic to the host's port 8080 lands on the container's port 8000.

A namespace hides things; it does not limit them. Inside its private view, orders could still eat all of the host's memory, which raises the question of what stops it.

## Limits, the writable layer, and the shared kernel

At this point orders is a normal host process whose namespaces show it only its image's files, its own process list, and its own network. What keeps it from starving its neighbours is a second kernel feature.

That feature is the control group, usually shortened to cgroup. A cgroup is a kernel-managed group of processes with limits on how much CPU, memory, and disk input and output the group may use, plus counters for what it actually uses. Docker places orders in its own cgroup with a 512-megabyte memory ceiling. If the service leaks memory and crosses that line, the kernel's out-of-memory killer ends the process inside that group, and the other team's service on the same host is untouched.

One part of the filesystem story is still open. Image layers are frozen, yet orders writes log files and temporary data. When the container starts, Docker adds one more, empty, writable layer on top of the image's stack, belonging to this container alone. Writes land there; reading a file that was never changed falls through to the image below. Delete the container and that layer goes with it. Anything that must outlive the container, such as uploaded files or a database's data, belongs in storage mounted from outside, which is how containers are usually run in practice.

The shared kernel has one more consequence. Since a container borrows the host's kernel, an image built for Linux needs a Linux kernel underneath. On a Mac or Windows laptop, Docker Desktop quietly runs a small Linux virtual machine and starts containers inside it. The isolation is also only as strong as the kernel's separation between processes: a kernel bug can let a process escape, which is a weaker wall than a virtual machine's. Many setups accept that trade, and some run untrusted code in virtual machines for exactly this reason.

## The whole picture

A Docker container is a Linux process started from an image, a frozen and layered filesystem that carries the whole service and its dependencies but no kernel. The daemon gives that process its own namespaces, so it sees the image as its root directory, numbers its processes from 1, and owns a private network with forwarded ports; puts it in a cgroup, so its CPU and memory are capped; and adds a throwaway writable layer on top of the image. Nothing is simulated, and the host kernel runs it like any other process. That is what lets orders, with Python 3.12, sit beside a Python 3.8 service on the same server, start in under a second, and behave the same on every Linux host the image is copied to.

## Going further

- Volumes: Docker's named storage that lives outside any container's writable layer, used for data that must survive the container being replaced.
- Docker Compose: a file format and tool for describing several containers, such as orders and its PostgreSQL database, and starting them together.
- OCI and runc: the open standard for image and container formats, and the low-level program that the Docker daemon (through a component called containerd) uses to create the namespaces and cgroups.
- User namespaces and rootless mode: ways to make root inside the container map to an unprivileged user on the host, narrowing what an escape could do.

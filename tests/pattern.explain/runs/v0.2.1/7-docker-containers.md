# Docker Containers, From the Process Up

By the end you will understand what a Docker container really is on a Linux machine, how it is built and started, and why it is not a small virtual machine.

## Two services, one server

Say you run a server that already hosts a billing service written against Python 3.8 and an old version of a database driver. Now you need to deploy a new service, call it orders-api, which wants Python 3.11 and a newer driver, and listens on port 8000. Install both sets of dependencies side by side and something breaks: a shared library gets upgraded under the old service, two config files fight over the same path, or the new code works on your laptop and fails on the server because the server has a slightly different system library.

The traditional fix was a virtual machine for each service: a whole simulated computer with its own operating system kernel, booted from scratch. That isolates things well, but every service then carries a full operating system, takes tens of seconds to boot, and reserves its own slice of memory whether it uses it or not.

Docker takes a different route, and it starts from something you already know well. A Docker container is an ordinary Linux process. The kernel has been asked to give that process two things: a private view of the system, so it cannot see or collide with anything else, and a budget, so it cannot take more than its share. The process is started from a packaged filesystem that holds the program and every library it needs. Each of those three pieces has a name, and the rest of this piece takes them one at a time.

How can a normal process be made to believe it has a machine to itself?

## A private view: namespaces

You know that every process on Linux sees certain system-wide things: the list of process IDs, the mounted filesystems, the network interfaces, the hostname. Normally every process sees the same versions of these.

The Linux kernel can give a process its own separate copy of any of these views. That separate copy is called a namespace, and there is one kind per thing being isolated. In a PID namespace, the process sees its own process numbering, starting at 1, and cannot see processes outside. In a mount namespace, it sees its own set of mounted filesystems, so its root directory can be a completely different tree of files. In a network namespace, it has its own network interfaces, its own IP address, and its own ports. A UTS namespace gives it its own hostname, and a user namespace can map user IDs inside to different ones outside.

Put orders-api in a fresh set of these namespaces and, from the inside, it looks like it is alone on a small machine. Run `ps` inside the container and you see orders-api as PID 1 and nothing else. Its root directory contains Python 3.11 and its own libraries, not the server's. It can bind port 8000 without clashing with anything, because that port 8000 lives in its own network namespace.

This is where the most common misunderstanding appears, so it is worth stating plainly: a container is not a lightweight virtual machine. There is no second kernel and no boot. Run `ps` on the host and orders-api shows up there too, with an ordinary host PID, owned by the same kernel scheduler as everything else. The isolation is the host kernel choosing what to show the process, not a separate computer.

That single fact explains several things. A container starts in well under a second, because starting it means starting a process. It uses memory the way any process does, only what it actually touches. And every container on a host shares that host's kernel, so a container built for Linux needs a Linux kernel underneath. On a Mac or Windows laptop, Docker Desktop quietly runs a small Linux virtual machine, and the containers run inside that. It also means the isolation is only as strong as the kernel's boundaries: a kernel bug can let a process escape, which a virtual machine's extra layer would usually stop.

Seeing less is only half of isolation, though. What stops orders-api from eating all the memory on the server?

## A budget: control groups

A namespace changes what a process can see, but not how much it can use. A process in its own namespaces can still allocate every gigabyte of memory on the host and starve the billing service.

The second kernel feature handles this. A control group, almost always shortened to cgroup, is a group of processes the kernel accounts for together and can put limits on: how much memory, how much CPU time, how much disk input and output, how many processes in total.

Docker places every container's processes in their own cgroup. If you start orders-api with a limit of 512 megabytes of memory and half of one CPU core, the kernel enforces it. When the service tries to go past 512 megabytes, the kernel's out-of-memory killer ends a process inside that container, not some unlucky process elsewhere on the server. When it wants more CPU, the scheduler holds it to roughly half a core's worth of time, so the billing service keeps its share.

Namespaces and cgroups together give you an isolated, budgeted process. But the process still needs files to run: Python 3.11, the database driver, the code itself. Where do those come from?

## The filesystem: images and layers

The mount namespace lets orders-api have its own root directory. Something has to fill it. That something is an image: a read-only package containing a complete filesystem, everything from `/bin` and `/usr/lib` to your application code, plus a little metadata such as which command to run on start.

You describe an image in a text file called a Dockerfile. For orders-api it could be as short as this:

```
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

The first line starts from an existing image, published by the Python project, that already holds a minimal Linux userland and Python 3.11. Note that this is only files: libraries and tools from a Linux distribution, with no kernel inside. The second line copies your list of dependencies in. The third runs pip, at build time, to install those dependencies into the image. The fourth copies the rest of your code. The last line records the command a container should run when it starts.

Running `docker build` on this file produces the image. Each instruction that changes files produces a layer, a snapshot of only the files that step added, changed, or deleted. The image is the stack of those layers. The Python base might be around 130 megabytes, the installed dependencies another 40, and your code a few hundred kilobytes, each its own layer.

Layers matter because they are shared. If the billing service were also rebuilt on `python:3.11-slim`, the host would store that base layer once, and both images would point at it. When you change one line of code and rebuild, only the final layer is new, so building and shipping the update moves kilobytes instead of the full image.

To get an image from your laptop to the server, you push it to a registry, a server that stores images by name and tag, such as `orders-api:1.4`. Docker Hub is the best-known public one; companies usually run private ones. The server then pulls the image, downloading only the layers it does not already have.

A running container needs to write files, though, and the image is read-only. So when a container starts, Docker adds one more, empty, writable layer on top of the stack, private to that container. A union filesystem, on Linux usually one called OverlayFS, merges the stack into what looks like one normal directory tree. Reads fall through to whichever layer has the file; writes go to the top writable layer, and changing a file from a lower layer copies it up first.

Here lies a second trap. That writable layer belongs to that one container and is deleted with it. If orders-api writes uploaded invoices to `/data` inside the container, then removing the container and starting a new one from the same image, which is exactly what happens on every deploy, throws those files away. Data that must outlive a container goes in a volume: a directory managed outside the layer stack and mounted into the container's filesystem, so it survives when the container is replaced. A database running in a container without a volume will lose its data on the first redeploy.

So there is now a filesystem, a private view, and a budget. What actually happens when you type the command that brings them together?

## What docker run does

You now know a container is a process placed in namespaces, held to a cgroup budget, and given a root filesystem stacked from image layers. The command that assembles all of it is `docker run`.

The `docker` command you type is only a client. It sends your request to a long-running background program on the host, the Docker daemon, called `dockerd`, which does the work. The daemon in turn hands the low-level steps to helper programs called containerd and runc, which follow an open industry standard for containers, so other tools can run the same images.

Suppose you run orders-api with a 512 megabyte memory limit and ask for host port 8080 to forward to the container's port 8000. The steps, in order:

1. The daemon checks whether `orders-api:1.4` is on the host, and if not, pulls the missing layers from the registry.
2. It stacks the image's layers, adds a fresh writable layer on top, and mounts the result with OverlayFS.
3. It creates a new set of namespaces and a new cgroup with the 512 megabyte limit.
4. It creates a virtual network interface for the container's network namespace, connects it to a virtual bridge on the host, and adds firewall rules so that traffic arriving on host port 8080 is forwarded to port 8000 inside. Without that forwarding step, nothing outside could reach the service, because its port 8000 exists only inside its own network namespace.
5. It mounts any volumes you asked for.
6. Inside all of that, it starts the command from the image, `python app.py`, which becomes PID 1 in the container.

That last detail has a practical consequence for you as a backend developer. PID 1 is special on Linux: the kernel does not apply default signal handling to it, so signals it has not installed a handler for are ignored. When you run `docker stop`, Docker sends SIGTERM to PID 1, waits ten seconds by default, and then sends SIGKILL. If orders-api does not handle SIGTERM, or if it was started through a shell wrapper that does not pass the signal on, every stop takes the full ten seconds and ends with an abrupt kill, dropping requests in flight. Handling SIGTERM and shutting down cleanly is the container version of something you already do for daemons.

When PID 1 exits, the container stops. It is not deleted until you remove it, so you can still read its logs. Once it is removed, its writable layer goes with it, while the image and any volumes stay.

## The whole picture

A Docker container is a normal Linux process that the kernel wraps in namespaces, so it sees only its own processes, files, network and hostname, and in a cgroup, so it can use only its share of memory and CPU. Its files come from an image, a read-only stack of layers built from a Dockerfile and shared through a registry, topped by a thin writable layer that disappears with the container, which is why lasting data lives in volumes. Because nothing is booted and the host kernel is shared, orders-api and the billing service can each carry their own Python and libraries on the same server, start in a fraction of a second, and run the same way on your laptop as in production, with the trade-off that their isolation rests on one shared kernel rather than a separate machine.

## Going further

Docker Compose: a tool that starts several related containers, with their networks and volumes, from one configuration file.

Kubernetes: a system that schedules and restarts containers across many machines; it runs the same images but does not need Docker itself.

Multi-stage builds: a Dockerfile technique that compiles in one image and copies only the results into a smaller final one.

Rootless mode and user namespaces: ways to run containers so that root inside the container is not root on the host, narrowing the damage of an escape.

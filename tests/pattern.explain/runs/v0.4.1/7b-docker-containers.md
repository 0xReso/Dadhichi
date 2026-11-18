# Docker Containers

By the end you will know what a Docker container is on a Linux machine, the problem it was built to solve, how the kernel makes it work, and why calling it a small virtual machine leads people astray.

## One server, two programs that disagree

You run the server for an online shop. On it sits the order service, a Python program called orders-api, which needs Python 3.12 and a recent version of a database driver. On the same server runs an older reporting job written for Python 3.8, which breaks on anything newer. Both expect to find `python3` at the same path, and both were tested on laptops laid out nothing like this server.

This is the old deployment headache. A program is never only its own code. It leans on an interpreter, shared libraries, configuration files and a particular layout of the file system. Install two programs whose expectations clash and one of them loses. Move a program to a differently arranged machine and it may not start at all: the origin of "it works on my machine".

Docker is a tool that answers this by letting each program carry its whole surrounding file system with it and run inside a private view of the machine. The running program, together with that private view, is called a container. In a container, orders-api gets its Python 3.12 and its driver, the report job gets its Python 3.8, and neither can see the other's files.

So the first question is what exactly a program carries with it.

## The image: a program's file system, packaged

The shop's two programs collide because they share one file system. Docker's first move is to give each of them its own.

It does this with an image: a read-only bundle holding every file a program needs, laid out as a complete root directory. The orders-api image contains a `/usr/bin/python3` that is version 3.12, the driver in the usual library paths, the service's own code, and a minimal set of system files from a Linux distribution such as Debian. What it does not contain is a kernel.

Images are built from a short text recipe called a Dockerfile. For orders-api it might say, one instruction per line: start from a published image that already has Python 3.12 on Debian, copy in the service's code, install the driver, and run this command to start the service. Running `docker build` on that file produces the image.

Each instruction in the Dockerfile produces a layer: a set of file changes recorded on top of the layer below. The Python base is one layer, the installed driver another, your code a third. Docker stacks them so that, seen from above, they look like one ordinary directory tree. Images built on the same base share its layers, so the server stores a Debian base once, and a code change rebuilds only the top layer.

An image is also the thing you move between machines. You push it to a registry, a server that stores images by name and version label, such as `orders-api:1.4`, and the production server pulls exactly the bytes your laptop built.

An image, though, is files sitting on a disk. What happens when you tell Docker to run one?

## The container: an ordinary process with a narrowed view

You now hold an image: orders-api's whole file system, built in layers and pulled onto the server.

When you type `docker run orders-api:1.4`, Docker starts the service's command as a normal Linux process on the host. `ps` on the host lists it, and the host kernel schedules it like any other process. What makes it a container is that, before the program starts, Docker asks the kernel to place it in a fresh set of namespaces.

A namespace is a kernel feature that gives a process its own private instance of one kind of system resource. The process inside sees only that instance and has no way to name or reach the others. Linux has several kinds, each covering one resource. Three of them do most of the work for orders-api.

The PID namespace gives the container its own process numbering. Inside, orders-api sees itself as PID 1 and sees no other processes on the server. On the host, the same process might be PID 48213. It is one process, counted in two places.

The mount namespace gives the container its own view of the file system tree. Docker makes the stacked image layers the container's root directory, so when orders-api opens `/usr/bin/python3` it gets 3.12 from its image, while the report job, in its own container, opens the same path and gets 3.8. This is where the clash from the start disappears: one path, two different files, decided by which namespace the process is in.

The network namespace gives the container its own network interfaces, its own IP address and its own set of ports. orders-api listens on port 8000 inside its container, and that port 8000 is not the host's. To let customers reach it, you publish the port: `docker run -p 8080:8000` tells Docker to forward the host's port 8080 to the container's port 8000.

This is the point where most people picture a small virtual machine, and the picture is wrong in a way that matters. A virtual machine emulates hardware and boots its own kernel. A container has no kernel of its own. orders-api, the report job, and every other container on the server make their system calls to the one host kernel, exactly as uncontained processes do.

That shared kernel explains how containers behave. A container starts in well under a second, because nothing boots, and costs little memory beyond the program's own. But its isolation is thinner than a virtual machine's: a flaw in the kernel is a flaw under every container at once, and a Linux image needs a Linux kernel underneath it.

That last point is why Docker on a Mac or Windows laptop works differently. Docker Desktop, the version for those systems, quietly runs a small Linux virtual machine and puts your containers inside it.

Namespaces decide what orders-api can see, but not how much of the machine it may use. What stops one container from eating the whole server?

## Limits, the daemon, and what a container forgets

orders-api is now a host process wrapped in namespaces, with its own process numbers, its own file tree and its own network. It cannot see the report job, but both still draw on the same memory and CPU.

The kernel handles that with control groups, usually written cgroups: a feature that meters and caps the resources a group of processes may use. Running `docker run --memory=512m --cpus=1 orders-api:1.4` places the service in a cgroup capped at 512 megabytes of memory and one CPU core's worth of time. If a leak pushes it past 512 megabytes, the kernel's out-of-memory killer ends a process in that cgroup, and the report job and the rest of the server carry on. A container started without limits may use as much as the host will give it.

The `docker` command you type does none of this setup itself. It sends requests to the Docker daemon, a background service called dockerd that runs as root on the host and does the building, pulling, and creation of namespaces and cgroups. Because the daemon acts as root on your behalf, anyone allowed to send it commands can, in effect, act as root on the server.

One more piece completes the running container. The image layers are read-only, so Docker adds a thin writable layer on top for each container. When orders-api writes a log file, the write lands there; when it changes a file that came from the image, Docker copies that file up into the writable layer first and changes the copy. That layer belongs to the one container. Remove the container and the layer goes with it, and a new container from the same image starts clean.

So data that must outlive a container, such as the shop's database files, is kept in a volume: a directory Docker manages on the host and mounts into the container at a path you choose. Replace the container with version 1.5 tomorrow and the volume is still there to mount into the new one.

## The whole picture

A Docker container is an ordinary process on the host's Linux kernel, started from an image that carries its entire file system, so that programs with clashing needs can share one machine and a program built on one machine runs the same on another. The image supplies the files, stacked in layers and moved through a registry. Namespaces narrow what the process can see to its own PIDs, its own root directory and its own network. Cgroups cap how much memory and CPU it may take. The daemon arranges all of this, and a writable layer holds the container's changes until it is removed. There is no second kernel anywhere in that chain, which is both why containers are fast and cheap and why they are not virtual machines.

## Going further

- **Docker Compose**: a tool for describing several containers, such as orders-api and its database, in one file and starting them together.
- **OCI (Open Container Initiative)**: the standard image and runtime formats that Docker follows, which is why other tools, such as Podman and Kubernetes, can run the same images.
- **User namespaces and rootless mode**: ways to make root inside a container map to an unprivileged user on the host, narrowing the damage if a container is broken out of.
- **PID 1 duties and `--init`**: because the container's main process is PID 1, it inherits PID 1's jobs, such as reaping zombie children and handling signals, which some programs do badly unless a tiny init process starts first.

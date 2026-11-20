# Docker Containers

By the end you will know what a Docker container really is on a Linux machine, why it exists, how it is built and started, and why calling it a lightweight virtual machine leads people astray.

## The problem: one server, many incompatible programs

Say you maintain a small web API called orders-api. It is written in Python, needs Python 3.11 and a specific version of the PostgreSQL client library, and listens on port 8000. The server you are deploying to already runs an older reporting tool that needs Python 3.8 and a different version of that same library. Install your dependencies and you break the reporting tool; leave them out and your API will not start.

A program is never only its own code. It is the code plus a pile of files around it: an interpreter, shared libraries, configuration under /etc, certificates. Two programs on one machine share one filesystem, so their piles collide.

Docker's answer is to ship each program together with its own complete pile of files, and to run it so that it sees only that pile. The program then runs the same on your laptop, on a test server, and in production, because it brings its world with it.

## The image: a filesystem in a box

The packaged pile of files is called an image. An image for orders-api holds a minimal Linux userland, such as a cut-down Debian, plus Python 3.11, the client library, and your code. It also records a little metadata, most importantly the command to run at start-up, here something like `python app.py`. There is no kernel inside an image, only the files that normally sit on top of one.

You describe how to build an image in a short text file called a Dockerfile. Each line is an instruction: start from a published Python 3.11 base image, copy in your requirements file, install the packages, copy in your code, set the start command. Running `docker build` executes those instructions in order and produces the image.

Each instruction that changes files produces a layer: a read-only record of exactly the files that step added, changed, or removed. The orders-api image might be five layers stacked on each other, with the Debian files at the bottom and your code at the top. Layers are identified by a hash of their contents, so if the reporting tool's image is also built on the same base, the two images share those bottom layers on disk instead of storing them twice.

## Starting a container: a process with a restricted view

So far you hold an image: a stack of read-only layers with a start command attached. A container is what you get when you run it, and here your knowledge of Linux processes pays off directly, because a container is an ordinary Linux process.

When you type `docker run orders-api`, the docker command sends the request to a background service on the host called the Docker daemon. The daemon prepares a filesystem from the image, then asks the kernel to start the image's start command as a new process, with some extra settings attached at creation time. Those settings are what make it a container.

The first setting gives the process its own writable layer. The kernel's overlay filesystem, which merges several directories into one view, stacks a fresh, empty, writable directory on top of the image's read-only layers. Reads fall through to the first layer that has the file; writes land in the top layer. If the API writes a log file to /var/log, that file exists only in this container's writable layer, and the image underneath is untouched, so a hundred containers can start from one image without copying it.

The other settings come from a kernel feature called namespaces. A namespace wraps one kind of system resource so that a process inside it sees its own private copy of that resource rather than the host's. Linux has several kinds, and Docker puts each container into a new one of each by default. Three of them shape what orders-api sees.

The mount namespace gives the process its own list of mounted filesystems. In it, the merged overlay view is mounted as the root directory. When orders-api looks at /usr/bin/python3, it finds Python 3.11 from its image, and the host's Python 3.8 is not visible at all. This is what solves the collision from the start: both programs see a /usr/lib, but each sees its own.

The PID namespace gives the process its own numbering of process IDs. Inside the container, `python app.py` is PID 1, and running `ps` there shows only it and anything it starts. On the host it is an ordinary process with an ordinary number, say 41237.

The network namespace gives the process its own network interfaces, routing table, and ports. Orders-api binds port 8000 inside its namespace, and that does not clash with anything on the host. To reach it from outside you publish the port: `docker run -p 8080:8000 orders-api` tells Docker to forward traffic arriving at host port 8080 into the container's port 8000.

## The trap: a container is not a small virtual machine

You now have a process that sees its own files, its own process list, and its own network. It looks a lot like a separate machine, and this is where most people go wrong: they picture a container as a lightweight virtual machine.

A virtual machine emulates hardware and boots a whole guest operating system, with its own kernel, on top of it. A container boots nothing. There is one kernel, the host's, and the container's process makes system calls to it directly, exactly like every other process on the box. Run `ps aux` on the host and you will find orders-api's Python process at PID 41237, owned by a user, using memory, visible to `top` and `kill`, like any other.

That single fact explains most container behaviour. Containers start in well under a second, because starting one is starting a process, not booting a system. They add almost no overhead, because there is nothing between the process and the kernel. A Linux image needs a Linux kernel to run on, because it brings none of its own. And the isolation is weaker than a virtual machine's: every container on the host shares one kernel, so a bug in that kernel can let a process escape its namespaces, which is why many teams still separate untrusted workloads with virtual machines.

## Limits: how much a container may use

Namespaces control what the process can see, but not how much it can consume. A runaway orders-api could still eat all the host's memory and starve the reporting tool.

The kernel feature that handles this is called control groups, usually shortened to cgroups. A cgroup is a group of processes with resource limits and accounting attached. Docker places each container's processes in their own cgroup. Run it with `--memory 512m` and the kernel will not let the group's total memory go past 512 megabytes; if it tries, the kernel's out-of-memory killer ends a process in that group, and the container stops with exit code 137. CPU limits work the same way. Without such flags, by default, a container may use as much as the host has.

One more limit follows from the writable layer. Stopping a container keeps that layer, but removing the container with `docker rm` deletes it, along with any file the process wrote there. Containers are meant to be thrown away and recreated from the image, so anything that must survive, such as a database's data, has to live outside the writable layer.

## The whole picture

A Docker container is a normal Linux process started from an image. The image supplies the files, as a stack of shared read-only layers with a writable layer placed on top through the overlay filesystem. Namespaces give the process its own view of mounts, process IDs, and network, so orders-api finds its own Python 3.11 and its own port 8000 while the reporting tool keeps Python 3.8. Cgroups cap how much memory and CPU it may take. Because all of this is configuration applied to one process on the host's own kernel, containers are fast and cheap, and also less isolated than virtual machines, and their writable files vanish when the container is removed.

## Going further

- Volumes: directories managed by Docker, or paths on the host, mounted into a container so data survives the container's removal.
- Docker Compose: a tool that starts several related containers, such as an API and its database, from one configuration file.
- OCI and runc: the Open Container Initiative is an industry group that standardised the image format and how containers are run; runc is the low-level program Docker uses underneath to make the actual namespace and cgroup calls.
- Docker Desktop on macOS and Windows: since those systems do not have a Linux kernel, it runs a small Linux virtual machine in the background and your containers run inside it.

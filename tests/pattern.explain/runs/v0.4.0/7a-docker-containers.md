# Docker Containers

By the end you will know what a Docker container really is on a Linux machine, why it exists, how the kernel makes it work, and why calling it a small virtual machine leads people astray.

## The problem: the server is not your laptop

Say you have written a small web service called orders-api. It needs Python 3.11, the PostgreSQL client library, and a dozen Python packages at exact versions. On your laptop it runs. The production server has Python 3.8, a different version of the PostgreSQL library, and another team's service that needs those older versions to stay where they are.

You could install everything by hand on the server and hope nothing clashes. You could give orders-api a whole virtual machine of its own, with its own kernel and operating system, which isolates it well but costs gigabytes of disk, hundreds of megabytes of memory, and tens of seconds to boot for a program that itself needs a few seconds and a few hundred megabytes.

Docker takes a third route. It packages orders-api together with every file it needs, and then runs it as an ordinary process on the server's own kernel, with that process unable to see the rest of the machine. That pairing, a packaged set of files plus a fenced-off process, is what a container is. The packaged files come first.

## The image: a filesystem in a box

With the problem in hand, start with the files. Everything orders-api needs, from the Python 3.11 interpreter down to the PostgreSQL library and your own code, is collected into one read-only bundle that looks like the root of a Linux filesystem, with its own /usr, /lib and /app directories. That bundle is called an image.

An image contains files and some metadata, such as which command to run on start. It contains no kernel.

You describe how to build an image in a short text file called a Dockerfile. A typical one for orders-api says: start from an existing image that already holds Debian and Python 3.11, install the PostgreSQL library, copy in the code, and run the server on start. Each of those instructions produces one slice of filesystem changes, and each slice is called a layer. An image is a stack of layers, read from the top down, so a file in a higher layer hides the same path in a lower one.

Layers are why images are cheap to store and move. If the server already holds the Debian-and-Python layer for some other service, pulling orders-api downloads only the few megabytes of layers on top.

When a container starts, Docker adds one more, empty layer on top of the image, and this one can be written to. Any file the running program creates or modifies lands there, while the image beneath stays untouched, so a hundred containers can share one image. This top layer is called the container's writable layer, and it is deleted when the container is removed. Anything orders-api writes there, such as uploaded files, goes with it.

So far you have a directory tree. The next question is how a process ends up believing that tree is the whole machine.

## A container is a process with a private view

You now hold an image: a stack of read-only layers plus a writable one, together forming a complete root filesystem. Running it is less mysterious than it sounds, and your knowledge of Linux processes carries you most of the way.

When you type `docker run -p 8080:8000 orders-api`, the docker command sends the request to a background service on the server, called the Docker daemon. The daemon assembles the layers into one mounted filesystem and then starts your server's command as a normal Linux process, a child forked and executed like any other.

What makes it a container is that, before the program starts, the daemon wraps the process in namespaces. A namespace is a kernel feature that gives a process its own private copy of one kind of system resource, so it sees only what is in its copy. There are several kinds, and orders-api meets three of them.

The mount namespace gives the process its own table of mounted filesystems. In it, the assembled image is mounted as the root directory, so when orders-api opens /usr/lib it finds the libraries from the image, not the server's own. Python 3.8 on the host is simply not in its world.

The PID namespace gives the process its own numbering of processes. Inside, orders-api is process 1 and can see only itself and any children it starts. On the host it might be process 48213. Same process, two numbers, depending on which namespace is looking. Because orders-api is process 1 inside, the container lives exactly as long as it does: when that process exits, the container stops.

The network namespace gives the process its own network interfaces, IP address and ports. Orders-api listens on port 8000 inside its namespace, and the other team's service can also listen on port 8000 in its own without a clash. The `-p 8080:8000` part of the command tells Docker to forward the host's port 8080 to port 8000 inside the container, which is how requests from outside reach it.

Here is where the common misconception needs correcting. A container is not a lightweight virtual machine. A virtual machine runs its own kernel on emulated hardware. A container runs no kernel of its own: every container on the server makes system calls into the one host kernel, and the isolation comes from that kernel deciding what each process is allowed to see. That is why a container starts in well under a second, about as fast as launching the program directly, and why it costs almost no memory beyond the program's own. It also means the isolation is only as strong as the kernel's: a kernel bug can let a process escape, so containers are generally treated as a weaker security boundary than virtual machines.

Namespaces control what orders-api can see. They do nothing about how much it can use, which raises the question of what stops it from eating the whole machine.

## Limits: cgroups

You now have orders-api running as a host process that sees only its own files, its own process list and its own network. But a memory leak inside it would still consume the server's real memory, and a busy loop would still burn its real CPU, starving the other team's service.

The kernel feature that handles this is called a control group, usually shortened to cgroup. A cgroup is a set of processes that the kernel accounts for together and holds to limits: a ceiling on memory, a share of CPU time, a cap on disk throughput. Docker places every container's processes in a cgroup of their own.

Suppose you start orders-api with a 512 megabyte memory limit. The kernel counts every page the process and its children allocate. If they try to go past 512 megabytes, the kernel's out-of-memory killer ends a process in that cgroup, usually orders-api itself, and the rest of the server carries on unaffected. Since orders-api is process 1 in its container, the container stops, and Docker reports that it was killed for running out of memory. A CPU limit works more gently: a container capped at one and a half CPUs is slowed down by the scheduler when it reaches its share, not killed.

## The whole picture

A Docker container is an ordinary Linux process that the host kernel has been told to treat specially. Its files come from an image, a stack of read-only layers built from a Dockerfile, with a thin writable layer added on top for the life of the container. Namespaces give that process a private view of mounts, process IDs and the network, so orders-api sees Python 3.11 and port 8000 as if it had the machine to itself. Cgroups cap what it can consume, so a leak ends at 512 megabytes instead of taking the server down. Nothing in this chain is a second kernel or emulated hardware, which is why containers start as fast as programs and share one kernel's strengths and weaknesses.

## Going further

- Volumes: storage that lives outside the writable layer, so data such as uploads or a database survives the container being removed.
- Registries: servers that store and serve images by name and tag, such as Docker Hub, which is where `docker pull` fetches from.
- Docker Desktop on macOS and Windows: since containers need a Linux kernel, it runs a small Linux virtual machine behind the scenes and puts the containers inside it.
- User namespaces and rootless mode: ways to make root inside a container map to an unprivileged user on the host, which narrows what an escape could do.

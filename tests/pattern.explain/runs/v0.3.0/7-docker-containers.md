# Docker Containers

By the end you will know what a Docker container really is on a Linux machine, the problem it solves, how it is built and started, and why calling it a small virtual machine leads people astray.

## The problem: "it works on my machine"

Say you maintain a small web service called orders-api. It needs Python 3.12, a particular version of a PostgreSQL client library, and a system package for image handling. On your laptop it runs fine. The production server, though, has Python 3.8 because another service on it depends on that, and the image package there is two major versions behind. Installing your dependencies would break the neighbour; not installing them breaks you.

The old answers were to give each service its own server, which wastes hardware, or to write long setup scripts and hope every machine ends up the same, which they rarely do. What you want is a way to ship orders-api together with the exact files it expects, and run it on any Linux host without those files colliding with anything else there.

Docker is a tool that does this. It packages a program with everything it needs, and then runs it as an ordinary Linux process that has been given its own private view of the system. That running, walled-off process is a container.

## The image: a frozen copy of the files

Everything a container sees on disk comes from a package called an image. An image is a read-only snapshot of a filesystem: a minimal Linux userland such as Debian's, the Python 3.12 interpreter, your libraries, and the orders-api code, plus a little metadata saying which command to run at start-up. It contains no kernel. That detail matters a great deal shortly.

You describe how to build the image in a short text file called a Dockerfile. Each line is one instruction: start from an official Python 3.12 base image, copy in the requirements file, install the libraries, copy in the code, and name the start command.

Each instruction produces a layer, a set of file changes stacked on the one below. The base image is a few layers, the installed libraries are another, your code is the top one. Layers are stored once and shared, so if ten images on a server start from the same Python base, its files sit on disk once. When you change only your code and rebuild, Docker reuses every layer below it and rebuilds only the top one, which turns a build of minutes into seconds.

When you are done, you push the image to a registry, a server that stores and hands out images. Docker Hub is the public one most people meet first; companies often run their own. The production server pulls orders-api from the registry, and now has the exact files you tested with, Python 3.12 and all, without touching its own Python 3.8.

## Starting a container: one process, three kinds of isolation

So the production server now holds a read-only image of orders-api. Turning it into something running is where the Linux knowledge you already have pays off.

When you ask Docker to run the image, a background service on the host, the Docker daemon, does the work. It first adds a thin writable layer on top of the image's read-only layers, so the process can create log files or temporary data without altering the image. The stack of layers is combined into a single directory tree, and that tree becomes the new process's root filesystem. From inside, orders-api sees /usr/bin/python3 pointing at 3.12, because that is what the image contains; the host's 3.8 is simply not in its tree.

Next the daemon starts the process inside a set of namespaces. A namespace is a Linux kernel feature that gives a process its own private copy of one kind of system resource. The process ID namespace means orders-api sees itself as PID 1 and cannot see the host's other processes, even though on the host it has an ordinary PID like 48213. The network namespace gives it its own network interfaces and its own port 8000, so it does not clash with anything else listening on port 8000. The mount namespace keeps its filesystem view separate. There are a few more, for the hostname, users, and inter-process communication, and they all follow the same idea.

Namespaces control what the process can see, not how much it can use. That second job belongs to cgroups, short for control groups, another kernel feature that puts limits on a group of processes. The daemon can place orders-api in a cgroup capped at, say, one CPU core and 512 megabytes of memory. If the service leaks memory and crosses that line, the kernel's out-of-memory killer ends it, and the other services on the host carry on.

Put those pieces together and the container is complete: a normal process, with a root filesystem built from image layers, wrapped in namespaces so it sees only its own world, and placed in a cgroup so it can take only its share. Run `ps` on the host and orders-api shows up in the list like any other process. Docker itself does not invent new isolation; it arranges features the Linux kernel already has, and adds the image format, the registry, and a convenient command-line tool on top.

## The trap: it is not a small virtual machine

You now hold the whole mechanism: an image of files, a writable layer on top, and a host process fenced in by namespaces and cgroups. The most common mistake is to picture all of this as a lightweight virtual machine, and it is worth seeing exactly where that picture fails.

A virtual machine runs on a hypervisor, software that pretends to be a whole computer, and each virtual machine boots its own complete operating system with its own kernel. A container boots nothing. orders-api makes system calls straight into the host's kernel, the same kernel every other container and process on that server shares. That is why a container starts in well under a second, roughly the time to launch the process itself, while a virtual machine takes seconds to tens of seconds to boot.

Sharing the kernel has three consequences people trip on. First, the image cannot change the kernel: a container from a Debian image running on a host with a recent kernel is running on that recent kernel, whatever the image's userland suggests. Second, Linux containers need a Linux kernel; on a Mac or Windows laptop, Docker Desktop quietly runs a small Linux virtual machine and puts your containers inside it. Third, the isolation boundary is the kernel itself. A virtual machine's walls are enforced by hardware support for virtualisation; a container's walls are kernel bookkeeping, so a kernel bug, or a container run with extra privileges, can let a process reach the host. Containers are generally treated as a good boundary between your own services and a weaker one against hostile code.

There is a smaller trap tied to the writable layer. It belongs to that one container. Delete the container and the layer goes with it, along with any files orders-api wrote there. Data that must outlive the container, such as a database's files, belongs in a volume, a directory managed outside the container's layers and mounted into it.

## The whole picture

orders-api needed different files from its neighbours on the same server, and Docker solved that by separating the files from the machine. The files travel as an image, a stack of shared, read-only layers built from a Dockerfile and distributed through a registry. Running the image adds a writable layer, uses the combined layers as the root filesystem of an ordinary host process, wraps that process in namespaces so it sees only its own processes, network and mounts, and places it in a cgroup so it takes only its share of CPU and memory. Because nothing boots and the host kernel is shared, containers are fast and cheap, and for the same reason their isolation is only as strong as that kernel.

## Going further

- Docker Compose: a tool for describing and starting several related containers, such as orders-api and its PostgreSQL database, from one file.
- OCI (Open Container Initiative): the open standard for image formats and container runtimes, which is why images built with Docker also run under other tools such as Podman and Kubernetes.
- Rootless mode and user namespaces: ways to run containers so that root inside the container is not root on the host, narrowing the shared-kernel risk.
- Multi-stage builds: a Dockerfile technique that compiles in one stage and copies only the results into a smaller final image.

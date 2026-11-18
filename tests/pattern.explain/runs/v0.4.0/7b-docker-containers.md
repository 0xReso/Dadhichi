# Docker Containers, From the Process Up

By the end you will know what a Docker container really is on a Linux machine, the problem it solves, what happens when you start one, and why it is not a small virtual machine.

## One server, two programs that disagree

You run a server with an orders service written in Python. It needs Python 3.12 and a recent version of the PostgreSQL client library. The same server hosts an older reporting job that only works with Python 3.9 and an older version of that library. Install one set and the other breaks. Move either program to a new server and you have to rebuild its exact set of packages by hand, and one small difference, such as a missing system library or a config file in another place, makes it fail in a way it never did on your laptop.

The root of the trouble is that every process on a Linux machine shares the same ground: one filesystem, one list of processes, one set of network ports. Two programs that want different files in /usr/lib cannot both have them.

Docker's answer is to package each program with every file it needs, and then run it as a process that sees only its own package and its own share of the machine. That packaged, fenced-off process is a container. Docker is the tool that builds the packages and starts the containers; the fencing itself comes from features already built into the Linux kernel.

## The image: everything the program needs, as files

The problem, then, is shared ground. The first half of the fix is giving each program a filesystem of its own.

A Docker image is a read-only bundle of files laid out like the root directory of a small Linux system: /bin, /usr/lib, /etc, plus your application. For the orders service, the image holds a minimal Debian userland, Python 3.12, the PostgreSQL client library, your code under /app, and a note saying which command to run on start, here `python /app/server.py`. It holds no kernel. An image is files and a little metadata, nothing more.

You describe an image in a text file called a Dockerfile, a short list of instructions: start from an existing base image, copy these files in, run this install command. The `docker build` command follows the instructions and produces the image, which you tag with a name and version, here orders-api:1.4.

Each instruction in the Dockerfile produces a layer, a set of file changes on top of the one before. An image is a stack of these layers, and two images built on the same base share its layers on disk instead of storing them twice. When a container starts, Docker adds one more layer on top, empty and writable, and presents the whole stack as a single directory tree using the kernel's overlay filesystem. Reads fall through to whichever layer holds the file; writes land in the top layer only. The image underneath never changes.

That gives the orders service its own /usr/lib. The other half of the fix, its own process list, network and resource limits, has nothing to do with files, so where does it come from?

## The container: an ordinary process with a narrowed view

You now have an image: a read-only stack of layers, with one writable layer added when it runs. What turns that into a running container is the kernel.

A namespace is a kernel feature that gives a process a private copy of one kind of system resource. A process placed in a new namespace sees only what is inside it, while processes outside keep seeing the real thing. There are several kinds, and Docker gives each container a fresh one of each kind.

The mount namespace gives the process its own table of mounted filesystems. Docker mounts the overlay stack from the image as its root directory, so when the orders service opens a file under /usr/lib it gets the image's copy, never the host's.

The PID namespace gives it its own numbering of processes. Inside, the Python server is PID 1, and ps lists only it and its children. On the host the same process has an ordinary PID, say 48213, and appears in the host's ps like any other.

The network namespace gives it its own network interfaces, routing table and ports. The orders service can listen on port 8000 without clashing with anything on the host, because that port 8000 exists only inside its namespace. Docker links the namespace to the host with a virtual network interface and, when asked, forwards a host port into it. A few other kinds of namespace work the same way for the hostname and for shared memory between processes.

A control group, or cgroup, is the second kernel feature: it limits and accounts for what a group of processes may consume, such as memory and CPU time. Docker puts each container in its own cgroup. Give the orders service a limit of 512 megabytes and let it try to use more, and the kernel's out-of-memory killer ends it, as it would any process over its cgroup's limit.

This is where the usual picture of a container as a lightweight virtual machine goes wrong. A virtual machine runs its own kernel on virtualised hardware and boots like a computer. A container boots nothing. There is one kernel, the host's, and the container is a process on it whose system calls go straight to that kernel, with namespaces filtering what it can see and a cgroup capping what it can take. That is why a container starts in well under a second and costs little beyond the program's own memory. It is also why a Linux container needs a Linux kernel: Docker Desktop on macOS and Windows gets one by running a small Linux virtual machine in the background and placing the containers inside it. And the wall is thinner than a virtual machine's, because a flaw in the shared kernel is a flaw every container can reach.

So a container is a process with an image as its root filesystem, private namespaces, and a cgroup. Who arranges all of that when you type a command?

## What happens when you run it

A container is an ordinary process placed in fresh namespaces and a cgroup, with an image's layers as its root. Starting one means arranging those three things and then launching the program inside them.

You type:

    docker run -d --memory 512m \
      -p 8080:8000 orders-api:1.4

The -d flag runs it in the background. The --memory 512m flag sets the cgroup's memory limit. The -p 8080:8000 flag forwards port 8080 on the host to port 8000 inside the container. The last word names the image.

The docker command does very little itself. It sends the request over a local API to dockerd, the Docker daemon, a long-running background service that does the real work.

The daemon then goes through these steps:

1. It finds orders-api:1.4 on the machine, or downloads any missing layers from a registry, a server that stores images.
2. It stacks the layers, adds a fresh writable layer, and mounts the result with the overlay filesystem.
3. It creates a cgroup with the 512-megabyte limit and a new namespace of each kind, then sets up the virtual network interface and the 8080-to-8000 forwarding.
4. Inside all of that, it starts the image's command, `python /app/server.py`, which becomes PID 1 in the new PID namespace.

A request arriving at port 8080 on the server now reaches the Python process listening on port 8000 inside its namespace.

The container lives exactly as long as that process. When server.py exits, whether it crashed, finished, or was killed for passing its memory limit, the container stops. Nothing else keeps running inside, because nothing else was ever running there: no init system and no background services unless you put them in the image yourself.

The writable layer belongs to that one container. Remove the container and start a new one from orders-api:1.4, and the new one begins with an empty top layer: anything the old one wrote, such as logs or uploaded files, is gone, while the image is untouched.

The reporting job, meanwhile, runs in its own container from its own image with Python 3.9. Both share the host's kernel, neither can see the other's files, processes or ports, and moving either one to a new server comes down to pulling its image there and running it.

## The whole picture

A Docker container is an ordinary Linux process that the kernel has been told to treat specially: a mount namespace puts an image's stacked, read-only layers plus one writable layer at its root, so it carries its own libraries and runtime; PID, network and other namespaces hide the rest of the machine; and a cgroup caps the memory and CPU it may use. The image is the portable part, files with no kernel, built from a Dockerfile and shipped through a registry; the container is that image brought to life as a fenced-off process on the host's one shared kernel, started by the Docker daemon and gone the moment its main process exits. That is how two programs with incompatible dependencies can live side by side on one server, and why a container is a process rather than a small virtual machine.

## Going further

Volumes: directories from the host, or managed by Docker, mounted into a container so that data written there bypasses the writable layer and survives the container's removal.

Docker Compose: a tool that starts several related containers, such as a service and its database, from one configuration file.

containerd and runc: the lower-level components dockerd hands work to; runc makes the actual kernel calls, following the OCI (Open Container Initiative) specification that other tools also implement.

Root inside a container: by default the container's root user is the host's root with some privileges removed; look up Linux capabilities, user namespaces and rootless mode to see how this is narrowed.

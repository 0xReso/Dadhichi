# Docker Containers: A Process With Walls

By the end you will know what a Docker container is at the kernel level, how a packaged image becomes a running one, and why "a lightweight virtual machine" is the wrong picture.

## The problem it solves

Say you maintain a web service called orders-api. It needs Python 3.12 and a recent version of libpq, the C library that Python's PostgreSQL driver links against. The production server runs Python 3.10, and another team's service on the same machine depends on an older libpq. Installing your versions system-wide breaks them; installing theirs breaks you.

The traditional fix is a virtual machine per service. That works, but each one boots a complete operating system with its own kernel, takes gigabytes of memory and disk, and needs tens of seconds to start: a lot of machinery for a different Python version.

Docker is a set of tools that takes another route. It packages your service together with every file it needs, from the Python interpreter down to the shared libraries, and then runs it as an ordinary Linux process that the kernel has fenced off from the rest of the machine. That fenced-off process is a container.

## The image: a filesystem in a box

So the goal is to ship orders-api with its own Python and its own libpq, without disturbing the host. The first half of that is packaging.

Docker packages a service as an image: a read-only snapshot of a whole directory tree, the kind you would find under / on a Linux machine, plus a little metadata saying which command to run. The orders-api image contains /usr/local/bin/python3.12, libpq, and your code under /app. It contains no kernel.

You describe an image in a text file called a Dockerfile. For orders-api it might read:

```
FROM python:3.12-slim
RUN apt-get update && apt-get install -y libpq5
COPY . /app
CMD ["python", "/app/server.py"]
```

The first line starts from a published image that already holds a minimal Debian userland with Python 3.12. The second runs a command during the build to install libpq. The third copies your source code into /app. The fourth records the command a container should run when it starts.

Each instruction that changes files produces a layer: a record of only the files that instruction added, changed, or deleted. An image is a stack of layers read from the bottom up. Layers are shared, so if ten of your services start from python:3.12-slim, the host stores that base, roughly a hundred-odd megabytes, once rather than ten times.

Once you run `docker build`, you have an image named orders-api sitting on the server. Nothing is running yet. How does a pile of read-only files become a live service?

## Starting it: an ordinary process, fenced in

You now hold a read-only image that carries orders-api and its private copies of Python and libpq. Suppose you start it with:

```
docker run -p 8080:8000 --memory 512m orders-api
```

The `docker` command itself does very little. It is a client that sends your request to the Docker daemon, a background service on the host (its program is called dockerd) that does the actual work of building filesystems and starting processes.

The daemon first assembles a root filesystem. It stacks the image's layers, still read-only, using an overlay filesystem, a kernel feature that presents several directories as one merged tree. On top it adds one empty, writable layer that belongs to this container alone.

That writable layer uses copy-on-write. Reading /usr/local/bin/python3.12 reads straight from the image layer. Writing to a file that came from the image first copies it up into the writable layer and changes the copy, so the image itself never changes and other containers from the same image never see your edits.

Then the daemon starts `python /app/server.py`. Not inside anything: as a normal process on the host kernel. Run `ps` on the host and you will see it, with a host PID such as 48213. What makes it a container is the set of restrictions the kernel applies as the process is created.

The main restriction is the namespace. A namespace is a kernel feature that gives a process its own private copy of one kind of system-wide resource. Linux has several kinds, and Docker gives every container a fresh one of each. Three of them carry the orders-api story.

The PID namespace gives the container its own process numbering. Inside, server.py is PID 1 and `ps` shows only the processes it started. The host still sees it as 48213. Same process, two numbers, depending on which namespace you look from.

The mount namespace gives the container its own view of the filesystem. Its / is the overlay tree the daemon assembled, so /usr/local/bin/python3.12 exists for it while the host's Python 3.10 is invisible. The other team's service, in its own container, sees its own libpq. The conflict is gone.

The network namespace gives the container its own network interfaces, routing table and IP address. server.py listens on port 8000 inside that namespace, where nothing on the host can reach it directly. The `-p 8080:8000` flag tells the daemon to forward the host's port 8080 to the container's port 8000, which is how outside traffic gets in.

This is where most people's picture goes wrong. A container is often described as a lightweight virtual machine, and the phrase suggests a small guest system with its own kernel. There is none. Every container is a process on the same host kernel, making system calls like any other. That is why one starts in well under a second: there is nothing to boot. It also sets the limits of the design. A Linux container cannot run a program built for a different kernel. A kernel bug or a kernel crash affects every container at once. And by default, root inside a container is root on the host kernel, with Docker removing many of root's privileges and blocking risky system calls. That is a real safeguard, but a thinner wall than a virtual machine's. On macOS and Windows, Docker gets a Linux kernel by running these processes inside a hidden Linux virtual machine.

Namespaces control what the process can see, not how much it can use. That is the job of control groups, usually written cgroups: a kernel mechanism that counts and caps the CPU, memory and I/O used by a group of processes. The `--memory 512m` flag puts orders-api in a cgroup capped at 512 megabytes. If server.py grows past that, the kernel's out-of-memory killer ends it with SIGKILL, and Docker reports the container exited with code 137, which is 128 plus signal 9.

So you have a process with a private filesystem, a private network, and a memory ceiling. What happens to it, and to what it wrote, when it stops?

## When it stops

orders-api is now a fenced-off process on the host kernel, reading from shared image layers and writing into a writable layer of its own. Its lifetime is tied to one thing: when PID 1 inside the container exits, the container stops.

A stopped container keeps its writable layer, so restarting it brings back whatever it wrote. Removing it with `docker rm` deletes that layer for good. Suppose orders-api saved uploaded invoices to /app/uploads. Remove the container, start a new one from the same image to deploy a fix, and the invoices are gone, because the new container starts with a fresh, empty writable layer on top of an unchanged image.

That is why data that must outlast a container goes into a volume: a directory the daemon manages on the host, outside any image or container layer, and mounts into the container's mount namespace at a path you choose. Mount a volume at /app/uploads and the invoices live on the host's disk. Any new container of orders-api that mounts the same volume sees them.

## The whole picture

A Docker container is an ordinary Linux process whose filesystem comes from an image, whose view of processes, files and network is narrowed by namespaces, and whose resource use is capped by cgroups. The image is a read-only stack of layers carrying the application's whole userland but no kernel; the daemon adds a disposable writable layer and starts the process on the host's own kernel, so orders-api and its neighbours can each have their own Python and libpq while sharing one kernel. With lasting data kept in volumes, a container becomes something you can delete and recreate from its image at any moment.

## Going further

- Registry: a server that stores images so they can be pushed from one machine and pulled on another; Docker Hub is the default public one.
- OCI and runc: the open standard for image and container formats, and the low-level program Docker uses underneath the daemon to create the namespaces and cgroups.
- Docker Compose: a tool for describing and starting several related containers, such as orders-api and its PostgreSQL database, from one file.
- PID 1 and signals: `docker stop` sends SIGTERM to the container's PID 1 and, after a grace period of ten seconds by default, SIGKILL; a process that ignores SIGTERM or does not reap its children behaves badly as PID 1.

# Docker Containers

By the end you will understand what a Docker container really is on a Linux machine, why it exists, how an image becomes a running container, and why "a container is a small virtual machine" is the wrong picture.

## The problem: a program is more than its code

Say you have written a small web service called orders-api. It is a Python 3.12 program that listens on port 8000, and it needs a dozen libraries at exact versions, plus one system package for talking to a PostgreSQL database. On your laptop it runs. On the staging server, which has Python 3.10 and a slightly different set of system libraries, it crashes on startup. On a colleague's machine it runs, but a library behaves differently because they installed a newer version for another project.

The code was never the problem. The problem is everything around the code: the interpreter, the shared libraries, the configuration files, the exact directory layout the program expects. A process on Linux sees the whole host's filesystem, so whatever happens to be installed on that host becomes part of your program's behaviour.

For years the answer was a virtual machine: package a whole operating system with the program in it. That works, but each copy boots its own kernel, takes tens of seconds to start, and reserves gigabytes of memory. Running twenty small services that way is heavy.

Docker takes a different route. Instead of shipping a whole computer, it ships the program together with its own private copy of the files it needs, and then starts it as an ordinary Linux process that is fenced off so it sees only those files. That fenced-off process is a container.

## The image: the files, packaged and frozen

So the goal is to give orders-api its own set of files that travel with it, whatever host it lands on. The package holding those files is called an image.

An image is a read-only snapshot of a filesystem, plus a small amount of metadata: which command to run at start, which environment variables to set, which user to run as. The image for orders-api would contain a minimal Linux userland (the files under /usr, /lib, /etc and so on, with no kernel), Python 3.12, your libraries, and your code.

You describe how to build an image in a text file called a Dockerfile. For orders-api it might read:

```
FROM python:3.12-slim
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app
CMD ["python", "/app/main.py"]
```

The first line starts from an existing image that already contains a trimmed Debian userland and Python 3.12. The second copies your list of dependencies into the image. The third runs pip inside the image being built, so the libraries are installed into the image's files rather than onto your laptop. The fourth copies your source code in. The last line is metadata: it records the command a container should run when it starts.

Each of those steps produces a layer. A layer is the set of file changes one step made: files added, changed, or deleted compared with the layer below. The image is the stack of layers, read bottom to top, and the filesystem a program sees is all of them merged into one view. Docker builds that merged view with a union filesystem, the Linux kernel's overlay feature, which presents several directories stacked on top of each other as if they were one.

Layers matter in practice because they are shared and cached. If you change only your source code, Docker reuses the cached layers for the base image and the installed libraries, and rebuilds only the final copy step, which takes seconds instead of minutes. Twenty images built on python:3.12-slim store that base layer on disk once.

Images are stored and exchanged through a registry, a server that holds images by name and version tag, such as orders-api:1.4. Docker Hub is the public registry Docker uses by default, and companies usually run private ones. Your build machine pushes orders-api:1.4 to the registry, and the staging server pulls the same image down, layer by layer, getting byte-for-byte the files you tested.

That gives you a frozen, portable bundle of files. What it does not give you yet is a running program, and the step from one to the other is where the real mechanism lives.

## The container: a fenced-off process

You now hold an image, a stack of read-only layers with a start command attached. Running it is done by a background service on the host called the Docker daemon (the program dockerd), which you instruct with the docker command-line tool. When you type docker run orders-api:1.4, the daemon prepares the image's files and then starts the command from the image, python /app/main.py, as a process.

That is the point worth holding on to: a container is a process on the host, run by the host's kernel. If you run ps on the host, you will see python /app/main.py in the list, with a host process ID like any other. There is no second kernel and no boot step, which is why a container starts in well under a second.

This is also where the most common misunderstanding sits. People picture a container as a lightweight virtual machine, a little computer with its own operating system inside. It is not. A virtual machine emulates hardware and runs its own kernel; a container shares the host kernel and only changes what one process can see and use. The "Debian" inside python:3.12-slim is only Debian's files, not a Debian kernel. Two consequences follow. A Linux container needs a Linux kernel underneath, so Docker on a Mac or Windows laptop quietly runs a small Linux virtual machine and puts your containers inside it. And isolation is weaker than a virtual machine's: a bug in the shared kernel can, in principle, let a process escape its fence, which is why security-sensitive platforms sometimes add a virtual machine around containers.

What makes the process feel like it is alone comes from two kernel features. The first is namespaces. A namespace gives a process its own private view of one kind of system resource. In its PID namespace, orders-api sees itself as process 1 and sees no other processes on the host. In its mount namespace, the root of the filesystem is the merged image layers, so /usr/lib holds the image's libraries, not the host's. In its network namespace, it has its own network interfaces, its own loopback, and its own port 8000 that does not clash with anything else on the host. Other namespaces give it its own hostname and its own view of user IDs. From the inside, this looks like a separate machine; from the outside, it is one process with a narrowed view.

The second feature is control groups, usually called cgroups. Where namespaces limit what a process can see, cgroups limit how much it can use: CPU time, memory, number of processes, disk throughput. If you start orders-api with a 512-megabyte memory limit and it leaks memory past that, the kernel's out-of-memory killer ends it, and other containers on the host are unaffected. Without a limit, a container can use as much as the host would give any process.

Because the container is that one process, its life is tied to it. When python /app/main.py exits, the container stops. This catches people out with programs that fork into the background and let the parent exit: the container ends immediately because its main process is gone. Being process 1 also means receiving the stop signal: docker stop sends SIGTERM to that process, waits ten seconds by default, then sends SIGKILL, so a program that ignores SIGTERM always takes the full wait and is killed without cleaning up.

A fenced-off process with its own files is useful, but so far nothing outside can reach it, and nothing it writes has anywhere lasting to go.

## Writing data and letting traffic in

The container is now running: orders-api as process 1 in its own namespaces, seeing the image's frozen layers as its filesystem. Two practical questions remain: where its writes go, and how requests reach it.

Writes first. The image layers are read-only, so when the container starts, Docker adds one more thin, empty layer on top that belongs to this container alone, called the container layer or writable layer. When orders-api writes a log file or changes a config file, the change lands there; changing a file that exists in a lower layer first copies it up into the writable layer, a technique called copy-on-write. The image itself never changes, which is why you can start fifty containers from one image and each gets its own clean starting point.

The flip side is the second trap people fall into. When you remove the container, its writable layer is deleted with it. If orders-api kept uploaded files or a SQLite database inside its own filesystem, they disappear the next time you deploy a new version. Containers are meant to be disposable: you replace them rather than patch them.

Data that must outlive a container goes in a volume. A volume is a directory managed outside the container's layers, on the host or on network storage, and mounted into the container at a path you choose. Mount a volume at /app/data and everything orders-api writes there survives when you remove the container and start orders-api:1.5 against the same volume.

Now the traffic. The container's port 8000 lives in its own network namespace, so the host's port 8000 is not connected to it. Publishing a port tells Docker to forward a host port into the container: docker run -p 8080:8000 orders-api:1.4 means that a connection to port 8080 on the host goes to port 8000 inside the container. One detail trips people up here: a program that listens only on 127.0.0.1 inside the container is listening on the container's own loopback, which forwarded traffic does not arrive on, so services in containers need to listen on 0.0.0.0.

## The whole picture

A Docker container is the answer to the fact that a program's behaviour depends on the files around it. Docker freezes those files into an image, a stack of shared, cached, read-only layers built from a Dockerfile and moved between machines through a registry. Running the image means the Docker daemon merges those layers into a root filesystem, adds a writable layer on top, and starts the image's command as an ordinary process on the host kernel, fenced in by namespaces so it sees only its own files, processes and network, and held to a budget by cgroups so it cannot starve its neighbours. The container lives exactly as long as that process does, loses its writable layer when removed unless the data was placed in a volume, and is reached from outside through published ports. It is not a small computer; it is one process with a carefully narrowed view of the one you already have.

## Going further

Docker Compose: a tool for describing several containers, such as orders-api and its PostgreSQL database, with their networks and volumes in one file and starting them together.

OCI (Open Container Initiative): the standard formats for images and container runtimes, which is why images built with Docker also run under other tools such as Podman and Kubernetes.

Multi-stage builds: a Dockerfile technique that compiles or installs in one stage and copies only the results into a smaller final image.

Rootless mode and user namespaces: ways to run containers so that root inside the container is not root on the host, reducing the damage of an escape.

# What a Docker Container Really Is

By the end you will know what problem Docker containers solve, how Linux builds one out of an ordinary process, and why thinking of one as a small virtual machine leads people astray.

## The problem: the same code, a different machine

You maintain a Python web service called orders-api. It needs Python 3.11, a particular version of the PostgreSQL client library, and about forty Python packages pinned to exact versions. On your laptop it runs. The production server runs Python 3.8 for an older billing service that nobody wants to touch, and installing 3.11 next to it risks breaking billing.

The traditional fix is a virtual machine: a whole simulated computer with its own operating system kernel, booted on top of the real one. That works, but each one carries a complete operating system, takes tens of seconds to boot, and reserves memory, often gigabytes, before your code runs a line.

What you actually want is narrower. You want orders-api to see its own files, its own Python and its own libraries, and to be unable to interfere with billing, while still being a normal program on that server. Docker is a tool that gives you this, and the running thing it produces is called a container.

## The image: a packaged filesystem

The first half of the orders-api problem is that it needs a different set of files from the ones the server has. So the first thing Docker gives you is a way to package those files.

That package is called an image. It is a bundle holding every file the program needs: the user-space parts of a small Linux distribution such as Debian, the Python 3.11 interpreter, the PostgreSQL library, your packages and your code, plus a note saying which command to run at start. For orders-api it comes to about 150 megabytes, roughly the size of a short video. There is no operating system kernel inside it.

You describe how to build the image in a short text file called a Dockerfile. For orders-api it might read:

```
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "/app/server.py"]
```

The first line starts from a ready-made image that already contains a minimal Debian and Python 3.11. The second copies your list of package versions into it, and the third installs those packages. The fourth copies your code into the folder /app. The last line records the command to run when a container starts; it adds no files. Running `docker build` on this file produces the image.

Docker stores the result of each file-changing step as a separate read-only slice of the filesystem, called a layer, and stacks the layers on top of one another to form the image. This is why a rebuild after you edit one line of code takes seconds: the base and the installed packages are unchanged, so Docker reuses those layers and only redoes the step that copies your code.

When a container starts from the image, Docker places one extra, empty layer on top that the container is allowed to write to, called the writable layer. Whatever orders-api writes lands there, and the image underneath stays untouched, so ten containers can start from one image. When you delete a container, its writable layer is deleted with it. Data that must outlive the container has to be stored somewhere else.

So the files are packaged. That leaves the question of how a running program comes to see only these files and not the server's own.

## A container is a process with a restricted view

You now have orders-api packaged as an image, with its own Python and libraries in stacked layers. Here is what happens when you start it.

What runs on the server is an ordinary Linux process: `python /app/server.py`. It has a process ID on the host, it shows up when you run `ps` on the host, and the host kernel schedules it alongside everything else, billing included. Nothing is booted. What makes it a container is that the kernel has been told to show this process a restricted view of the system.

The kernel feature behind that view is the namespace. A namespace wraps one kind of system-wide resource, such as the list of mounted filesystems, so that processes inside it see a private copy instead of the global one. When Docker starts orders-api, it creates the process inside a fresh set of namespaces, using the clone and unshare system calls with namespace flags. Several kinds exist, and three of them explain most of what you will notice.

The first is the mount namespace, which gives the process its own list of mounted filesystems. Docker mounts the image's layers, with the writable layer on top, as the root directory of that list. When orders-api asks for /usr/local/bin/python, it finds 3.11 from the image. The host's Python 3.8 is still on the disk, but it is not reachable from inside.

The second is the PID namespace, which gives the process its own numbering of process IDs. Inside, server.py sees itself as process 1, and `ps` lists only the processes started in the container. On the host, the very same process might be number 48213.

The third is the network namespace, which gives the process its own network interfaces, its own IP address and its own table of ports. When orders-api listens on port 8000, that is port 8000 inside its namespace, not on the host. Billing could listen on 8000 in its own container and the two would never collide. To let outside traffic in, you ask Docker to forward a port on the host, say 8080, to port 8000 inside the container; this is called publishing a port.

Seeing less is not using less, though. Nothing so far stops orders-api from consuming all the memory on the server.

## Limits, and the kernel everyone shares

orders-api now runs as a normal process that sees its own files, its own process list and its own network. The remaining piece is a ceiling on what it can consume.

That ceiling comes from a second kernel feature, the control group, usually shortened to cgroup. A cgroup is a group of processes that the kernel accounts for together and holds to limits on CPU time, memory and disk input and output. Docker puts each container's processes into their own cgroup. If you cap orders-api at 512 megabytes and it tries to use more, the kernel's out-of-memory killer ends a process in that group, and billing never notices.

Put together, starting orders-api looks like this:

```
docker run -d -p 8080:8000 \
  --memory 512m --cpus 1.5 \
  orders-api:1.4
```

The first line starts a container in the background and publishes host port 8080 to container port 8000. The second sets the cgroup limits: 512 megabytes of memory and the equivalent of one and a half CPU cores. The third names the image and its version tag, 1.4. The container is running in well under a second, because nothing more happened than a mount, some namespaces, a cgroup and a process start.

This is where the most common misunderstanding sits: that a container is a lightweight virtual machine. It is not. A virtual machine has its own kernel. A container has none; every container on the server shares the one host kernel. Run `uname -r` inside orders-api and you get the host's kernel version, not something from Debian. The "Debian" in the image is only the files around the program.

That shared kernel has two consequences worth holding. First, a container image built for Linux needs a Linux kernel underneath, because the program inside makes Linux system calls directly. Second, the wall between containers is the kernel itself: a bug in the kernel, or a container started with extra privileges, can reach the host. By default, root inside a container is user ID 0 on the host, with some of its powers removed, so containers are a weaker security boundary than virtual machines.

## The whole picture

A Docker container is your program running as an ordinary Linux process, started from an image whose read-only layers supply all its files, with a thin writable layer on top. Namespaces give that process a private view: its own root filesystem, its own process numbering and its own network. A cgroup caps how much CPU and memory it can take. Underneath it all sits the host's single kernel, which every container shares. That is why containers start in a moment, why orders-api can carry Python 3.11 onto a server that runs 3.8, and why a container isolates less firmly than a virtual machine.

## Going further

- Volumes: storage that Docker manages outside a container's writable layer, mounted into the container, so data such as a database's files survives when the container is deleted.
- Registries: servers that store images by name and version tag, such as Docker Hub, from which `docker pull` downloads an image and to which `docker push` uploads one.
- PID 1 and signals: the kernel gives the first process in a PID namespace no default signal handling, so a program without its own SIGTERM handler ignores `docker stop` until Docker kills it after a timeout, ten seconds by default; the `--init` option adds a small helper process to fix this.
- Docker Desktop: the packaging of Docker for macOS and Windows, which runs a hidden Linux virtual machine so that Linux containers have a Linux kernel to share.

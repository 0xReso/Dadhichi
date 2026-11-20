# Docker Containers: A Process With a Private View

By the end you will know what a Docker container is in kernel terms, what an image holds, how isolation and resource limits are made, and why a container is not a small virtual machine.

## The same code on a different machine

You have a web API, call it orders-api, written for Python 3.12 and a handful of libraries built against particular system packages. It runs on your laptop. The production server has Python 3.8, and another service on that server depends on the old version. Installing your versions next to it risks breaking that service, and installing them by hand on every server is how "it worked on my machine" happens.

The classic fix was a virtual machine per application: a whole guest operating system, with its own kernel, booting on emulated hardware. That isolates well, but each one costs gigabytes of disk, a large slice of memory, and tens of seconds to boot.

Docker takes a different route. It packages your application together with every file it needs from a Linux system, apart from the kernel, and then runs it as an ordinary process on the host's kernel, with the kernel arranging for that process to see only its own files, its own process list and its own network. A process started this way is called a container. Docker is the tool that builds the packages and asks the kernel to set up that view.

So the first question is what is inside the package.

## The image: a filesystem that does not change

The package is a directory tree frozen in place: /usr/bin/python3.12, the shared libraries it links against, your pip packages, your code, plus a little metadata saying which command to run at start. That frozen package is called an image.

You describe how to build an image in a text file called a Dockerfile. For orders-api it could be four lines:

```
FROM python:3.12-slim
COPY . /app
RUN pip install -r /app/requirements.txt
CMD ["python", "/app/server.py"]
```

The first line starts from a published image that already contains a minimal Debian userland with Python 3.12, which Docker downloads. The second copies your project directory into /app. The third runs pip during the build, so the installed packages become part of the image. The fourth records the command a container from this image will run. Running `docker build -t orders-api .` produces the image and names it orders-api.

The image is stored as a stack of pieces rather than one big archive. Each instruction that changes files produces a read-only set of differences on top of the previous one, and each such set is called a layer. The Python base layers are stored once on disk, however many of your images start from them, and a rebuild after a code change redoes only the steps from the first changed one onward.

When a container starts, Docker adds one thin, empty, writable layer on top of the stack, and a kernel feature that merges several directories into one view presents all the layers as a single tree. New files land in the top layer. Changing a file that lives in a lower layer first copies it up into the top layer and changes the copy. This is called copy-on-write, and it means the image itself never changes: ten containers from orders-api share one copy of its layers, each with only its own small writable layer.

That writable layer belongs to the container and is deleted with it. If orders-api saves uploads to /app/uploads, removing the container with `docker rm` deletes them. For data that must outlive the container you mount a directory from outside into its tree, which Docker calls a volume.

Having a tree of files is not yet a container, though. How does a process come to see that tree as its root, and nothing else?

## Namespaces: what the process is allowed to see

You now have an image, a stack of read-only layers with a writable layer added per container. When you type `docker run orders-api`, the docker command does not do the work itself. It sends the request to a background service on the host, the Docker daemon, which sets everything up and then starts your program.

The daemon starts that program inside namespaces. A namespace is a Linux kernel feature that gives a process its own copy of something that is normally global to the whole machine; processes inside see only their copy, and their changes stay in it. Linux has several kinds, and a container gets one of each. Three of them do the work orders-api needs.

The mount namespace gives the process its own table of mounted filesystems. The daemon mounts the merged image tree as /, so when server.py runs `python`, it finds the image's 3.12 rather than the host's 3.8. The host's own files are not mounted there, so they do not exist from the inside.

The PID namespace gives the process its own numbering of processes. Inside, your Python server is PID 1, and running `ps` there lists it alone. On the host, `ps` shows the same process under an ordinary number, say 48213. It is one process with two numbers: you can `strace` it or `kill` it from the host like any other.

Because the container is that process, it lives exactly as long as PID 1 does. When server.py exits, normally or by crashing, the container stops. There is nothing else in there keeping it alive.

The network namespace gives the process its own network interfaces, its own loopback and its own set of ports. Your server can listen on port 8000 inside, and a second container can also listen on 8000, without either clashing with the host. Docker gives the container a private address on a virtual network inside the host, typically something like 172.17.0.2.

Nothing outside the host can reach that private address, so you ask Docker to forward a host port to it: `docker run -p 8080:8000 orders-api` sends traffic arriving at the host's port 8080 to the container's port 8000. This is called publishing a port.

Seeing less of the machine is not the same as using less of it. What stops orders-api from taking all the memory on the host?

## Cgroups, and why a container is not a small virtual machine

So far the container is a normal process whose view of files, processes and network has been narrowed by namespaces. Limits on what it consumes come from a second kernel feature.

Control groups, usually called cgroups, let the kernel count and cap the resources used by a group of processes. Running `docker run -p 8080:8000 --memory 512m --cpus 1.5 orders-api` places the server in a cgroup capped at 512 megabytes of memory and one and a half CPU cores' worth of time. If the server goes past 512 megabytes, the kernel's out-of-memory killer ends it, and since it is PID 1, the container stops. Going over the CPU share is handled differently: the process is slowed down, not killed.

This is where the most common misunderstanding sits. Because a container has its own files, process list and network, people picture it as a lightweight virtual machine. It is not one. There is no guest kernel. Every container on the host makes system calls into the same kernel as everything else; run `uname -r` inside orders-api and it prints the host's kernel version, whatever distribution the image was built from.

That single fact explains several behaviours. A container starts in well under a second, because starting it is roughly a fork and exec with extra setup, not a boot. An image needs no kernel, which keeps it small. A Linux container cannot run a program built for Windows, because the kernel underneath is Linux. And on a Mac or a Windows laptop, Docker Desktop quietly runs a small Linux virtual machine and starts your containers inside it.

It also sets the strength of the isolation. The wall between a container and the host is the kernel's system-call interface, so a kernel bug reachable from inside a container can reach the host and every other container. By default, root inside a container is user ID 0 on the host as well, with some of root's powers removed. A virtual machine puts a hypervisor and a separate kernel in the way; a container does not, so untrusted code is usually given more than a container's defaults.

## The whole picture

A Docker container is one or more ordinary Linux processes, started from an image whose read-only layers are merged under a private writable layer, placed in namespaces so they see only that filesystem, their own process numbering and their own network, and placed in a cgroup so they can use only so much memory and CPU. The daemon assembles all of this on request, and the container lasts as long as its PID 1. Because the kernel is shared rather than duplicated, containers are fast and cheap, and for the same reason their isolation is weaker than a virtual machine's. That is what lets orders-api carry its own Python 3.12 onto a server running 3.8 and behave the same there as on your laptop.

## Going further

- Registry and Docker Hub: a server that stores images for `docker pull` and `docker push`; Docker Hub is the public one that `FROM python:3.12-slim` downloads from by default.
- OverlayFS and the overlay2 storage driver: the kernel filesystem that merges the layers into one tree on most Linux hosts.
- containerd, runc and the OCI specifications: the lower-level programs the daemon hands work to, and the open standards for image and container formats that other tools also follow.
- Rootless mode and user namespaces: ways to make root inside a container map to an unprivileged user on the host.

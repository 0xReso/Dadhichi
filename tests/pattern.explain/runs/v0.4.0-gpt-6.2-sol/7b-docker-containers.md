# Docker containers

You’ll understand how Docker turns a packaged application into a running Linux process, what that process can see and use, and what survives when you replace it.

## The files your application expects

Your `orders` service works on your laptop. On the deployment server, it exits at startup because the shared library it needs is missing. Installing the library gets the service running, but the next server needs the same setup. Docker gives you a way to package those files together and start the service with a consistent environment on each compatible host. The host is the machine where the service runs.

The package is called an **image**. The `orders` image contains the service executable, the shared library it expects, and the other files it needs at startup. It also records defaults for how to start the service, including the command to run. You build the image and distribute it to the hosts that will run it.

When you ask Docker to run the image, it creates a **container**. The container is an instance with its own settings and filesystem changes. Starting it launches the configured command. You can create two containers from the same `orders` image, and each will have its own process when started. The image itself stays the same.

For the `orders` process to find its library, it has to look for files in the package you shipped. How does Docker give the process that view of the filesystem?

## What the process can see

The `orders` image carries the library, and the container gives the running process a filesystem view built from that image. Linux controls which files and directories appear in that view through a **mount namespace**. Inside it, `/` is the root of the container’s filesystem. When `orders` opens a library under `/usr/lib`, that path resolves inside the container’s view.

A **namespace** gives a process a particular view of some part of the system. Processes that share a namespace share that view. Linux has several kinds because the set of visible files, the set of visible processes, and the network setup can each be managed separately.

With Docker’s default process isolation, `orders` also gets a **process ID namespace**, which gives it its own view of process identifiers. If Docker launches `orders` directly as the container’s main process, it sees itself as process 1. The host can see that same process under a different identifier. Both identifiers refer to the same running process.

A **network namespace** gives the container its own network interfaces and its own set of local ports. With Docker’s usual isolated networking, `orders` can listen on port 8080 inside the container while another container also listens on its own port 8080. If you want clients to reach `orders` through a port on the host, you can **publish** host port 9000 to container port 8080. Clients connect to the host on 9000, and Docker’s network setup directs the traffic to `orders` on 8080.

Those separate views can make a container look like a small virtual machine. The distinction is at the kernel, the part of Linux that handles operations such as opening files and scheduling processes. A virtual machine runs its own kernel. The `orders` process makes its requests directly to the Linux kernel that runs Docker’s Linux containers. On Docker Desktop for macOS or Windows, that kernel runs in a Linux virtual machine shared by the Linux containers.

The kernel can give `orders` a separate view of the machine, but what keeps it from using all the memory on that machine?

## What the process can use

The `orders` process shares a Linux kernel with other workloads. A namespace changes what a process can see. To account for what a group of processes uses and enforce resource limits, Linux has **control groups**, usually called **cgroups**.

If you give the `orders` container a memory limit of 256 megabytes, Docker configures that limit through a cgroup. The kernel accounts for memory used by the container’s processes together. If the kernel can’t reclaim enough memory to keep the group within the limit, it can kill a process in the group. A container can have a separate process and network view even when you set no explicit memory limit for it.

The lifetime of the container’s main process determines whether the container is running. When `orders` exits, the container stops. Docker can start that same container again, with its existing settings and filesystem changes. Creating a replacement container from a newer image is a different operation. What happens to the files `orders` wrote in the old container?

## What survives replacement

A stopped `orders` container keeps its filesystem changes. Those changes live in the container’s **writable layer**, which Docker puts above the read-only image contents. When `orders` creates a file there, it appears alongside the files from the image. A second container created from that image starts with a writable layer of its own.

Suppose `orders` writes its database file under `/var/lib/orders`. If that path uses the writable layer, restarting the same container preserves the file. Removing the container removes its writable layer. A replacement created from a new image therefore starts without the database file that the old container wrote there.

To keep the database across replacements, you can create a Docker-managed place for the data called a **volume**. You attach it at `/var/lib/orders`, so writes to that directory go into the volume. When you replace the `orders` container, you attach the same volume at the same path. The new process gets its executable and library from the new image and opens the existing database file from the volume.

## The whole picture

Docker makes the `orders` service repeatable by giving the code and the data different lifetimes. Each release can carry its executable and libraries in an image. On the host, Linux runs that release with its own filesystem, process, and network views and applies any resource limits you set. Replacing the container gives the next release a fresh writable layer, while attaching the same volume lets it pick up the database where the previous release left off.

## Going further

- **Dockerfile** — the instructions Docker uses to build an image.
- **Registry** — a service that stores images so hosts can download them.
- **Bind mount** — a way to make a specific host file or directory visible at a path inside the container.
- **Restart policy** — a setting that tells Docker when to start a stopped container again.
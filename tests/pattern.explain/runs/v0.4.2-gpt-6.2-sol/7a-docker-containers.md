# Docker containers

You’ll understand how Docker turns a packaged application into a running Linux process with its own view of the machine, and what happens when you replace that container.

## From application files to an image

Your invoice service works on your laptop. On the deployment host it exits at startup because the version of a shared library it expects is missing. You could install the library on the host, but another service might need a different version. Docker lets each service bring the files it expects to find when it runs.

That package is called an **image**. The invoice image contains the service executable, its libraries, and the files those libraries expect. It also records the default command to start the service. You can run the same image on your laptop and on a compatible Linux deployment host, giving the service the same packaged files in both places.

Docker stores the image as a stack of read-only filesystem changes called **layers**. A lower layer might provide system libraries, while a higher layer adds the invoice executable. Docker presents the combined result as one directory tree. Several copies of the service can share those read-only layers.

An image can sit on disk without a process running. When you ask Docker to run it, Docker creates a **container** from the image and starts the command inside it. The container holds the settings and filesystem for that particular instance. If you start the invoice image twice, you get two containers, each with its own process.

How does Docker make each process see the files from its image at ordinary Linux paths?

## What the process sees

The invoice image supplies the files, and the container gives the running service a place to see them. When the service opens a library under `/usr/lib`, that path needs to lead to the copy packaged in the image.

Linux can give a group of processes its own view of a part of the system. Each such view is called a **namespace**. Different kinds of namespace control different things. Docker uses them to set up the environment before the service starts.

A **mount namespace** gives the container its own view of which filesystems are attached at which paths. Docker sets up the filesystem assembled from the image as the container’s root directory. The invoice process looks up `/usr/lib` from that root, so it finds the packaged library even when the host has a different version at the same path.

A **process ID namespace** gives the container its own view of process numbers. When Docker starts the invoice executable directly as the container’s first process, it sees itself as process 1. The host can still see the same process under a host process number. If that first process exits, the container stops.

A **network namespace** gives the invoice service its own network interfaces and port space. The service can listen on port 8080 inside the container. For traffic arriving at the host, you can tell Docker to forward connections on host port 9000 to container port 8080. The service keeps listening on 8080, and callers connect to the host on 9000.

These views are provided by the host’s Linux kernel, the part of the operating system that handles requests from processes. The invoice service shares that kernel with the other containers. A virtual machine runs its own kernel. That difference matters when you count on isolation for security. A flaw in the shared kernel can affect the boundary between containers and the host.

With its own view of the machine, how much of that machine can the invoice service use?

## What the process can use

The invoice container has its own view of files, processes, and networking. Its CPU time and memory still come from the host. If the invoice service gets busy, it can compete with other services for those resources.

Linux uses **control groups**, usually called **cgroups**, to track and constrain the resources used by a group of processes. Docker places the container’s processes in a cgroup. If you give the invoice container a memory limit of 512 mebibytes, about half a gibibyte, the kernel can stop a process in that group when the group reaches the limit and the kernel cannot reclaim enough memory. Without a container memory limit, the service can keep consuming memory until it encounters a broader system limit.

The image itself is read-only, yet the service can still write files. Docker adds a **writable layer** above the image layers for each container. If the invoice service creates a file there, that file belongs to its container. A second container started from the same image gets a fresh writable layer.

What happens to the invoice files when you deploy a new image?

## Replacing the container

The invoice service’s writable layer belongs to its current container. Stopping and starting that container preserves the layer. Removing the container deletes it. If invoices were saved there, starting a replacement container from a new image would leave the replacement without those files.

For data that must survive replacement, Docker can attach storage at a directory inside the container. A **volume** is storage managed by Docker that can exist independently of a container. Attach one at `/invoices`, and writes to that directory go to the volume. The service still opens and saves files using ordinary paths.

When you deploy the new invoice image, you can remove the old container, create its replacement, and attach the same volume at `/invoices`. The new process gets its program and libraries from the new image. It opens the existing invoice files from the volume.

## The whole picture

A Docker image gives an application the files it expects. To run it, Docker starts a process on the host’s Linux kernel and uses namespaces to give it the right view of the system. Control groups let you bound its resource use, and a volume lets its data outlive the container. You can replace the invoice service and its libraries together while keeping the invoice files available at the same path.

## Going further

- **Dockerfile** — the instructions Docker can use to build an image.
- **Registry** — a service that stores images so other machines can retrieve them.
- **Bind mount** — a way to expose a specific host file or directory at a path inside a container.
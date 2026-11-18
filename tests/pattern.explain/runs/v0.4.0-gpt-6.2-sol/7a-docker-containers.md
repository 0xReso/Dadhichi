# Docker containers

You’ll understand what Docker packages, what Linux runs, and what happens to an application’s files and network connections when it runs in a container.

## Package the application

Your `orders` service listens on port 8080. It works on your laptop, where it finds the right language runtime and shared libraries. On a server, a different version of one library can keep the same application from starting. Docker lets you deliver the application with the files it expects and start it in a controlled environment on the server.

The package Docker starts from is called an **image**. The `orders` image contains the application, its language runtime, and the libraries and other files it needs to start. The image also carries defaults such as the command Docker should run. You can build it once and use the same image on compatible machines.

Docker can store and reuse groups of image files as **layers**. The `orders` image might use existing layers for the language runtime and add a layer with the service code. When you deploy an updated version of `orders`, a server that already has the unchanged layers can reuse them.

Docker can start several independent instances from the same image. Each instance has its own running processes and its own place for file changes. An instance created this way is called a **container**. Docker can also keep a container around after its processes exit, so a container can be running or stopped.

How does Linux give each running instance its own environment?

## Start the process

The `orders` image supplies the files and the startup command. When Docker starts a container from it, the Linux kernel on the host runs that command as a process. The host is the machine running the containers. Several containers on that host use the same kernel.

Linux can give a group of processes its own view of a system resource. The kernel feature that provides each such view is called a **namespace**. Different kinds of namespace control different things a process can see.

A **mount namespace** gives `orders` its own view of the mounted filesystem. Docker makes the container’s filesystem appear at `/`, so a path such as `/app` resolves inside that filesystem. Docker can also make selected storage available at particular paths inside the container.

A **process ID namespace** gives `orders` its own view of process identifiers. If Docker starts the service directly as the container’s first process, the service sees itself as process 1. From the host, you can see that same process under its host process ID. When the container’s first process exits, the container stops.

A **network namespace** gives `orders` its own network interfaces and port space in a typical Docker setup. Two `orders` containers can therefore both listen on port 8080 inside their respective network namespaces.

Linux also lets Docker account for and limit resources such as memory and processor time for a group of processes. The kernel feature for this is called **control groups**, or **cgroups**. If you set a memory limit for an `orders` container, the kernel enforces it.

With `orders` listening inside its own network namespace, how does a request reach it from outside?

## Send a request to the container

The `orders` process listens on port 8080 inside the container. A client that connects to the host’s address reaches the host’s network, so it needs a way to reach that listener.

Docker can arrange for connections to a host port to be forwarded to a container port. This is called **publishing a port**. Suppose you publish host port 18080 to port 8080 in the `orders` container. A client connects to the host on port 18080, and the service receives the connection on port 8080.

The two port numbers belong to different sides of the connection. If you start a second copy of `orders`, it can still listen on container port 8080. To reach it through the same host address, you can publish host port 18081 for that copy. The application uses the same port in both containers.

When an order comes in through that connection and the service writes a file, what happens to the file when you deploy a replacement container?

## Keep data across deployments

A request to host port 18080 now reaches `orders`, and the service can write its order record to a file. Where Docker puts that write determines whether the replacement container can see it.

Docker keeps the image layers read-only and gives each container a **writable layer** on top. When `orders` creates a file there, the file belongs to that container. Stopping and starting the same container preserves the file. Removing the container removes its writable layer. A replacement created from the same image starts with a fresh writable layer.

For files that should survive replacement, Docker can manage storage separately from the container and make it available at a path inside it. This storage is called a **volume**. If you mount a volume at `/var/lib/orders` and the service writes its records there, you can remove the old container and mount the same volume at the same path in its replacement. The replacement service opens the existing records at the path it already expects.

## The whole picture

Docker gives you a repeatable way to go from a packaged application to a running Linux process. The `orders` image supplies the files and startup command. Each container runs those files under the host kernel with its own views of the filesystem, processes, and network. Publishing a port gives clients a route in, and mounting a volume gives data a lifetime that can extend across deployments.

## Going further

- **Dockerfile** is the file of instructions Docker uses to build an image.
- **Registry** is a service that stores images so other machines can fetch them.
- **Bind mount** makes a specific file or directory on the host available at a path inside a container.
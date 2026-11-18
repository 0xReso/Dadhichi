# Docker containers

You’ll understand how Docker takes a packaged application, starts it as a Linux process, and gives it its own view of the machine.

## What Docker starts from

Your `orders` service starts on your laptop. On the deployment host, it exits because a shared library it expects is missing. You can install the library on that host, but every new host then needs the same setup. The problem is getting a known set of files to the machine that will run the service.

You can package the service executable, its libraries, and the directory layout they expect into a Docker **image**. The image also records how Docker should start the service by default. When you move the image to another compatible host, the files inside it go together.

Docker keeps the image read-only when it starts `orders`. It gives that instance a **writable layer**, which holds changes made through the instance’s filesystem. If `orders` writes `/var/log/orders.log` there, a second instance from the same image gets its own writable layer and starts without that log. Both can use the same underlying image files.

The instance Docker creates from the image is a **container**. When Docker starts the container, it launches the configured program as a process. How does that process come to see the image’s files at paths like `/var/log`?

## What the process sees

Docker has the files for `orders` and a place to record its writes. To make those files appear at the paths the service expects, it uses a Linux feature that gives a group of processes its own view of some part of the system. That feature is called a **namespace**.

A **mount namespace** gives `orders` its own view of which filesystems appear at which paths. Docker sets up that view and makes the filesystem assembled for the container its root directory. When `orders` opens `/var/log/orders.log`, the path starts at that root. A process on the host opening the same path starts at the host’s root.

A **process ID namespace** gives the container its own numbering and view of processes. If Docker launches `orders` directly as the main process, `orders` sees itself as process 1 inside the container. The host can see the same process under a host process number. If `orders` starts a child process, that child can also appear in the container’s process view.

Those two views can make the container feel like a small Linux machine. The distinction is where the system calls go. When `orders` opens a file or starts a child process, it calls the same Linux kernel that serves the other containers on that host. A virtual machine runs its own kernel. If you run Linux containers on a Mac, Docker runs them inside a Linux virtual machine, and they share the kernel of that machine.

The kernel can give `orders` its own view of files and processes. How does it keep `orders` within a memory budget?

## What the host controls

`orders` runs on a shared kernel, so the kernel can account for the resources its processes use. Linux can group those processes and apply resource controls to the group. Such a group is called a **control group**, or **cgroup**.

If you configure Docker to give `orders` a memory limit, Docker applies that limit through a cgroup. The budget covers the group, including its child processes. If `orders` launches a worker, the worker’s memory use counts toward the same budget. Namespaces shape what the processes see. The cgroup controls how much memory the group can use.

The container’s running state follows its main process. If `orders` exits, the container stops. The stopped container still has its writable layer, so starting that same container again can bring `orders` back with its log intact. Removing the container discards that layer. A fresh container from the same image starts with a fresh layer.

For data that needs to survive replacement, Docker can attach a **volume**, a place to store files outside the container’s writable layer. If you attach a volume at `/var/log` before starting `orders`, the service still writes to `/var/log/orders.log`. A replacement container can read that log when you attach the same volume at the same path.

## The whole picture

Docker brings together a package of application files and the Linux controls needed to run those files as a service. The image gives every new `orders` container the same starting files. The process runs on the shared kernel, which gives it a view of the system through namespaces and applies resource limits through a cgroup. Whether a file survives the move to a fresh container depends on where the process wrote it.

## Going further

- **Dockerfile**. A text file with instructions for building an image.
- **Registry**. A service that stores images so other machines can download them.
- **Port publishing**. Making a service listening inside a container reachable through a port on the host.
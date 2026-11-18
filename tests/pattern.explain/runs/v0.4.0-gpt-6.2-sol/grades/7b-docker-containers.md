1 No lookups: “On Docker Desktop for macOS or Windows” introduces Docker Desktop without saying what it is. The sentence explains where the Linux kernel runs, but leaves the reader to infer how this named product relates to Docker. **Fail**

2 Linear: Across the opening, body, and closing sections, the closest call is that “mount namespace” precedes the general definition of a namespace. The paragraph already explains what the mount namespace controls and shows how `/usr/lib` resolves, so the reader can follow it immediately. **Pass**

3 Accurate: Across the filesystem, networking, resource-limit, and storage examples, the closest call is “Inside it, `/` is the root of the container’s filesystem.” That is true of the configured container, but the wording can imply that a mount namespace itself sets the process’s root directory. It controls the visible mounts, while setting the root is a distinct part of container setup. **Borderline**

4 Proportional: The supplied count is 1,081 words, within both the 2,200-word moderate ceiling and the 1,700-word limit for input 7. **Pass**

5 No padding: “On Docker Desktop for macOS or Windows, that kernel runs in a Linux virtual machine shared by the Linux containers.” This is a relevant platform qualification, but the preceding sentences already explain which kernel runs `orders` and how a container differs from a virtual machine. The sentence is one removable aside. **Borderline**

6 Resumable: All three eligible sections reopen with an established fact. “The `orders` image carries the library” recalls the deployment problem, “The `orders` process shares a Linux kernel” leads into limits, and “A stopped `orders` container keeps its filesystem changes” leads into storage. **Pass**

7 Plain text: The longest-looking elements are paths such as `/var/lib/orders`, which fit comfortably in prose. The only list contains four flat bullets, with no tables, links, images, or code blocks anywhere in the article. **Pass**

8 Not dumbed down: Throughout the article, `orders` remains a service with a concrete dependency, port, memory limit, and database. The nearest comparison, “look like a small virtual machine,” immediately gets a precise boundary in the explanation of kernel sharing. **Pass**

9 Trap handled: “A virtual machine runs its own kernel” identifies the decisive difference, and the next sentence tells the reader which kernel actually handles requests from `orders`. **Pass**

10 Clean output: From the title through the final “Restart policy” bullet, the output contains only the article. The line beginning “You’ll understand” is the requested reader-facing description. **Pass**

11a Complete: Every step in “The whole picture” has a worked counterpart for `orders`: its executable and library in the image, its filesystem path and process identifier, its port mapping, its 256-megabyte limit, and its database volume attached to the replacement container. **Pass**

11b Unhurried: The paragraph beginning “Those separate views” introduces a virtual machine and the kernel, then names “Docker Desktop for macOS or Windows.” Even counting the two operating systems as familiar, the paragraph introduces three terms, enough to meet the rubric’s failure threshold. **Fail**

12 Unknown topic: This is input 7. The check applies only to input 4. **Not applicable**

13 Source confidence: The graded source block is empty. **Not applicable**

Summary: 8 Pass, 2 Borderline, 2 Fail, 2 Not applicable. The most consequential failure is the cluster of new terms in the virtual-machine paragraph, where an unexplained product name competes with the kernel distinction the reader needs to retain.
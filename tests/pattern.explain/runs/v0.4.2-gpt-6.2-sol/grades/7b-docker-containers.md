1 No lookups: Across the body and closing list, container-specific terms get an explanation at first use. The closest call is “virtual machine,” introduced with the property the reader needs to distinguish it from a container: “A virtual machine runs its own kernel.” **Pass**

2 Linear: From the opening through “Going further,” each explanation uses concepts already in place. The question about the memory budget comes before the definition of a cgroup, but the reader already understands the question from the shared-kernel example. **Pass**

3 Accurate: “Which holds changes made through the instance’s filesystem” reads as covering every write through a container path. The later volume example shows a write through `/var/log/orders.log` going elsewhere. The first description fits the initial setup, but its wording suggests a broader rule. **Borderline**

4 Proportional: The supplied count is 818 words, within both the 1,700-word limit for input 7 and the 2,200-word moderate ceiling. **Pass**

5 No padding: “If you run Linux containers on a Mac, Docker runs them inside a Linux virtual machine” adds a platform-specific case after the shared-kernel distinction is complete. That sentence can go without leaving a gap in the `orders` example. **Borderline**

6 Resumable: Both eligible sections restate the starting point. “What the process sees” recalls the files and the place to record writes, and “What the host controls” opens with “`orders` runs on a shared kernel.” **Pass**

7 Plain text: Across all five sections, the longest technical items are inline paths such as `/var/log/orders.log`. The closing list is flat, and no passage relies on a table, link, image, or wide code. **Pass**

8 Not dumbed down: Throughout the piece, `orders` is a service with a concrete deployment problem. “Feel like a small Linux machine” describes the process’s isolated view, and the next sentences identify exactly where the resemblance ends. **Pass**

9 Trap handled: “It calls the same Linux kernel that serves the other containers on that host” corrects the container-as-virtual-machine misconception at the point where the separate file and process views make it plausible. **Pass**

10 Clean output: From the title through the final “Port publishing” entry, the output stays within the article. Even the questions at section endings concern `orders`, with no visible plan, writer’s preamble, or offer. **Pass**

11a Complete: Every connection in “The whole picture” has a worked counterpart: the image supplies the executable and libraries, namespaces explain the log path and process number, the cgroup accounts for the worker’s memory, and the writable layer and volume explain the log’s fate after replacement. **Pass**

11b Unhurried: The shared-kernel paragraph introduces “virtual machine” and the platform name “Mac” together. The kernel is familiar ground for this reader, but those two first mentions are separate terms rather than a pair defined against each other. **Borderline**

12 Unknown topic: This is input 7. The check applies only to input 4. **Not applicable**

13 Source confidence: The source block is empty. **Not applicable**

Summary: 9 Pass, 3 Borderline, 0 Fail, 2 Not applicable; the most consequential issue is the writable-layer description, because a reader relying on it could misjudge whether a log survives container replacement.
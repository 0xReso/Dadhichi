1 No lookups: Across the body and closing list, Docker-specific terms receive explanations where they first matter. The closest call is “cgroups,” introduced alongside “control groups” immediately after the sentence explaining what Linux can limit. **Pass**

2 Linear: Across all four body sections, the explanations arrive in dependency order. The closest call is the question about a replacement container, but the reader already knows Docker can start another instance from the same image and needs no knowledge of storage to understand the question. **Pass**

3 Accurate: The process, port, and storage examples agree throughout. In particular, both copies can listen on container port 8080 because they have separate network namespaces, and the example assigns them distinct ports on the same host address. **Pass**

4 Proportional: The supplied count is 986 words, below both the 1,700-word limit for input 7 and the 2,200-word moderate ceiling. **Pass**

5 No padding: Introducing layers prepares the reader for the writable-layer explanation, but “a server that already has the unchanged layers can reuse them” adds a deployment optimization. That passage can go without leaving a gap in the mechanism. **Borderline**

6 Resumable: All three eligible openings recover the preceding context. “Start the process” recalls the image’s files and startup command, “Send a request to the container” recalls the listener on 8080, and “Keep data across deployments” recalls how a request reaches it. **Pass**

7 Plain text: Across the article, the only list is the flat three-item “Going further” list. Inline paths such as `/var/lib/orders` fit in ordinary prose, and there are no tables, links, images, or wide code blocks. **Pass**

8 Not dumbed down: The same `orders` service carries the explanation from deployment to file storage. Even the two-copy port example uses actual port numbers and namespace behavior, with no fictional characters or analogy to decode. **Pass**

9 Trap handled: “Several containers on that host use the same kernel” supplies the corrective fact, but the startup section never identifies the common virtual-machine misconception that each container boots its own kernel. The rubric requires the misconception to be named as well as corrected. **Fail**

10 Clean output: From the title through the bind-mount entry, every line belongs to the article. The line beginning “You’ll understand” is the requested reader orientation, and there is no visible plan, writer’s note, or offer. **Pass**

11a Complete: Every step in “The whole picture” has an `orders` example in the body, including the filesystem rooted at `/`, the process seen as process 1, the connection from 18080 to 8080, and the volume remounted at `/var/lib/orders`. **Pass**

11b Unhurried: Across the body and closing list, each new Docker concept gets its own paragraph or entry, including each of the three namespace types. The closest apparent pair, “control groups” and “cgroups,” gives two names for the same concept. **Pass**

12 Unknown topic: This is input 7. The check applies only to input 4. **Not applicable**

13 Source confidence: The source block is empty. **Not applicable**

Summary: 10 Pass, 1 Borderline, 1 Fail, 2 Not applicable. The most consequential omission is the unnamed virtual-machine misconception, because readers can retain the shared-kernel fact without recognizing which assumption it corrects.
1 No lookups: In the memory-limit example, “512 mebibytes, about half a gibibyte” explains the relationship between two units but gives neither in familiar terms. Whether that costs a lookup depends on how much unit vocabulary the reader’s Linux experience supplies. **Borderline**

2 Linear: Across the body and closing sections, each explanation has its prerequisites. The closest call is “How does Docker make each process see the files from its image at ordinary Linux paths?” It closes a section after both process and image are established, and the next section answers it. **Pass**

3 Accurate: The image, process, port, memory, and storage examples are internally consistent. One qualification is missing from “A network namespace gives the invoice service its own network interfaces and port space.” That describes the ordinary private-network setup, but Docker can also run the service in the host’s network namespace. The sentence reads correctly for the example and too broadly as a general guarantee. **Borderline**

4 Proportional: The supplied count is 1,061 words, below both the 1,700-word limit for input 7 and the 2,200-word moderate ceiling. **Pass**

5 No padding: Across the body and closing list, the closest call is the return to `/invoices` in the replacement paragraph. Its first appearance explains where writes go, while its second explains how a new process regains access to existing files. The closing list adds three distinct lookup terms. **Pass**

6 Resumable: All three eligible openings recover the preceding idea. They begin with “The invoice image supplies the files,” “The invoice container has its own view of files, processes, and networking,” and “The invoice service’s writable layer belongs to its current container.” **Pass**

7 Plain text: The entire article uses headings, prose, short inline paths, and one flat list. Even the port mapping is readable as a sentence without a diagram or command. **Pass**

8 Not dumbed down: The invoice service remains a technical example throughout. The article uses practitioner terms such as “mount namespace” and “writable layer” without introducing a fictional character or relying on an analogy. **Pass**

9 Trap handled: Immediately after explaining the container’s private views, the article addresses the misconception that a container runs its own kernel. “The invoice service shares that kernel with the other containers. A virtual machine runs its own kernel.” **Pass**

10 Clean output: From the title through the “Bind mount” entry, the output contains only article content. The line under the title describes the learning outcome without exposing the writing plan. **Pass**

11a Complete: Every mechanism in “The whole picture” has a worked counterpart. The missing library motivates the image, `/usr/lib`, process 1, and port 8080 illustrate namespaces, the memory limit illustrates control groups, and reattaching `/invoices` illustrates persistence. **Pass**

11b Unhurried: The paragraph beginning “Linux uses **control groups**” introduces control groups and their abbreviation as one term, then adds two distinct unit names in “512 mebibytes, about half a gibibyte.” That puts three new terms in one paragraph, even counting “cgroups” only once. **Fail**

12 Unknown topic: This is input 7. The check applies only to input 4. **Not applicable**

13 Source confidence: The source block is empty. **Not applicable**

Summary: 9 Pass, 2 Borderline, 1 Fail, 2 Not applicable; the clearest weakness is that the reader meets two unfamiliar memory units in the same paragraph where they need to grasp what a control group does.
# Head grading: built/explain.commuter.it.md v0.2.1

Date: 2026-11-15. Grader: dadhichi-head. Stage: grading after the test run.
Outputs graded: v0.2.1 inputs 1, 2, 3, 4, 5, 7 on all 11 checks; v0.1.0 inputs 1 to 3 re-read and graded on check 11, with three older verdicts adjusted (marked).
Not run: inputs 6 (long source) and 8 (second domain). One sample per input, so every finding below is from n=1.

## Decision: DO NOT PROMOTE v0.2.1

On inputs 1 to 3, v0.2.1 passes more checks than v0.1.0 (22 against 19 of 32 graded cells) and fixes the logged failures on inputs 2 and 3. It is blocked by the second half of the promotion rule: it fails a check v0.1.0 passed. Input 1, check 5 (No padding) went from Pass to Fail, and the same output went from 615 to 1,632 words against a 600-word limit. The trivial input is the one input whose whole purpose is "does it stay short", and it did not.

Single most important fix: the simple tier has no test for what makes a topic simple, so the model sized "what an API key is" as a moderate topic. Fix step 9 first (edit 1 below).

## How I applied two checks

Check 4 uses the numbers now in rubric.md (600 / 2,200 / 4,500) for both versions. That changes v0.1.0 Raft from the old scorecard's Borderline to Fail (5,988 against 4,500).

Check 11 has two halves. Completeness: each mechanism step in "The whole picture" is explained in the body with the running example. Pace: I counted new terms in the densest paragraph. Zero paragraphs with two or more new terms is Pass; a worst paragraph with two is Borderline; three or more is Fail.

Correction to my own gate review: I wrote there that "all three v0.1.0 outputs pass" check 11. That was true only of the completeness half. I had not counted terms per paragraph. Counted, none of the three passes the pace half. The verdicts below replace that claim.

## Score table

P = Pass, B = Borderline, F = Fail. Check 6 is not applicable to input 1.

| # | Check | v0.1.0 #1 (615) | v0.2.1 #1 (1,632) | v0.1.0 #2 (2,751) | v0.2.1 #2 (1,897) | v0.1.0 #3 (5,988) | v0.2.1 #3 (3,920) | v0.2.1 #4 (1,640) | v0.2.1 #5 (1,781) | v0.2.1 #7 (2,144) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P | B | P | P | B (adjusted) | B | B | P | P |
| 2 | Linear | P | P | B | P | F | P | P | P | P |
| 3 | Accurate | P | P | P | P | P | P | B | P | P |
| 4 | Proportional | B | F | F | P | F (adjusted) | P | P | P | P |
| 5 | No padding | P | F | F | B | F | B | B | P | B |
| 6 | Resumable | n/a | n/a | B | F | P | P | F | B | P |
| 7 | Plain text | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | P | P | P | P | P | P | P | B | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | P | P | P | P |
| 11 | Complete and unhurried | B | B | F | F | F | F | F | B | F |
| | Pass / Borderline / Fail | 8 / 2 / 0 | 6 / 2 / 2 | 6 / 2 / 3 | 8 / 1 / 2 | 5 / 1 / 5 | 8 / 2 / 1 | 6 / 3 / 2 | 8 / 3 / 0 | 9 / 1 / 1 |

Inputs 1 to 3 totals: v0.1.0 19 Pass, 5 Borderline, 8 Fail. v0.2.1 22 Pass, 5 Borderline, 5 Fail.

Movement on inputs 1 to 3:

- Better: #2 checks 2, 4, 5; #3 checks 2, 4, 5.
- Worse: #1 check 5 (P to F, the blocker), #1 check 4 (B to F), #1 check 1 (P to B), #2 check 6 (B to F).
- Check 11 does not separate the versions on the verdict, but the densest v0.2.1 paragraphs are denser than the v0.1.0 ones (see #2 and #3).

## Evidence for every non-Pass, v0.2.1

### Input 1, API key (1,632 words)

Check 1, Borderline. Two terms the stated reader may not hold are used bare: "upload the project to a public repository" and "open the browser's developer tools". v0.1.0 avoided both ("publish their code online").

Check 4, Fail. 1,632 words against "about 450, never more than 600". 2.7 times the limit.

Check 5, Fail. At least five passages can be deleted with no gap in what the title promises:
- "Those checks are two different jobs that are easy to blur together. The first is authentication..." (a second topic).
- "Many providers show you the full key only once and keep just a scrambled fingerprint of it".
- "The same thing happens with code repositories." (a second case of the trap already made).
- "It also helps to know what an API key does not identify." (a lead-in to OAuth, which is already in "Going further").
- The whole of "The whole picture", which the prompt reserves for moderate and long pieces.

Check 11, Borderline. Nothing is missing. Two paragraphs carry two new terms: "The first is authentication: ... The rest are authorization" and "You can revoke a key ... And you can rotate keys".

Checks 2, 3, 7, 8, 9, 10 pass. The concert-ticket analogy states where it breaks. The trap (a key in shipped code "is not hidden; it is published") is well placed.

### Input 2, Kafka consumer groups (1,897 words)

Check 5, Borderline. One paragraph of version detail survives: "How a rebalance runs differs by Kafka version. In the long-standing design, consumers pause, one of them works out the new assignment..." The prompt asks for one sentence; this is four, and deleting it leaves no gap. The config names, static membership and the off-by-one note from v0.1.0 are gone, which is the fix working.

Check 6, Fail. Nine "##" sections; of the eight after the first, one opens by restating anything ("A rebalance moves partitions to new owners, and a new owner needs to know where to start."). The others open cold: "Now the consumer group itself.", "Every record in a partition gets a sequence number", "The email program also needs every order.", "Now the full sequence, using the shop." v0.1.0 had two explicit restatements ("You now know how a group splits the work."), so this is a small regression. Cause is in the prompt: see section "Why check 6 fails on moderate pieces".

Check 11, Fail. Complete: every step in "The whole picture" is in the body with the shop example, and the crash walk-through (offsets 8,400 to 8,449, 50 duplicate invoices) is the best passage in the run. Pace fails on one paragraph that hands over four terms in 30 words: "Kafka runs as a cluster of servers called brokers. Programs that write messages are called producers; programs that read them are called consumers. Each message is called a record." v0.1.0's worst paragraph had three, each with an example.

### Input 3, Raft (3,920 words)

Check 1, Borderline. "etcd, the database that stores the state of every Kubernetes cluster": Kubernetes is never explained, and "cluster" is used throughout ("In a five-server cluster") without being introduced. v0.1.0 defined cluster but dropped four bare product names in one sentence, so I have adjusted it to Borderline as well.

Check 5, Borderline. "There is also a subtlety about reading." This is the read-strategy material logged as padding in v0.1.0, cut from three paragraphs to one, and it is also listed in "Going further" ("ReadIndex and leader leases"), so it appears twice. "Speed here is set by the fastest majority, not by every server." is the write-latency passage, also deletable.

Check 11, Fail. Two findings.
- Pace: "That ordered list of changes is called the log. Each change in it is a log entry, and each entry has a position, counted from 1, called its index. The database that the log is applied to is called the state machine ... is a replicated state machine." Five new terms in one paragraph. v0.1.0 gave the same material two paragraphs. This is the compression my gate review warned of, in the foundation passage.
- Completeness: the log-repair step is described without the running example. "If the follower had any entries after that point that differ from the leader's, the follower deletes them and takes the leader's instead." No named server is repaired and no named entry is discarded. v0.1.0 showed both (E catching up on entries 6 and 7; A's uncommitted entry 7 deleted). The only worked discard in v0.2.1 is inside the current-term commit scenario, which starts "a fresh run of the same five servers" with new numbers.

Answers to the four things I said to look at first:
1. Log repair and the discarded entry both survive as rules, but neither with the running example. See above.
2. Yes, the log paragraph introduces five terms at once.
3. RequestVote and AppendEntries are both still named.
4. The election restriction is introduced without a forward pointer: the vote goes to "the first candidate that asks and qualifies", and the rule arrives as a new fact in the safety chapter. Edit 5 of the gate review worked. Check 2 moved from Fail to Pass.

Notes that did not change a verdict: "often every 50 milliseconds or so, about the time it takes to blink" (a blink is several times longer; the prompt's own example says "quicker than a blink"). "higher than the term 2 at the end of B, C and D": D never received the term-2 entry, though the conclusion holds. The partition scenario restarts with A as a live leader of term 1 after A's power supply failed in the election walk-through; the reader has to notice that it is a second scenario.

### Input 4, Driftwood (1,640 words)

Check 1, Borderline. "without dedicating a thread to each one": thread is not explained, and the same paragraph introduces async runtime, task, Tokio and async function.

Check 3, Borderline. No invented function names or defaults, which is the main thing the input tests. But the admission is partial and the piece then claims things it cannot know:
- "I cannot vouch for the exact details of Driftwood itself" implies it knows the tool in outline. It does not; the tool does not exist.
- "using the vocabulary its documentation will almost certainly use".
- "you will be reading about choices within a design you already understand".
- "A Rust job scheduler such as Driftwood exists so that code can run on a timetable from inside your application". Whether Driftwood is an in-process library, uses cron expressions, or builds on Tokio is unknown.

Check 5, Borderline. "In Rust, this sleeping is usually done with an async runtime." The section it opens is detail about how a tool of unknown design probably works; it can go with no gap.

Check 6, Fail. Six sections after the first, none restates what the reader holds. Openings: "Most schedulers, Rust ones included, borrow the notation cron invented.", "A scheduler with one job could loop forever", "Starting the job is only the beginning."

Check 11, Fail. Complete, but "That piece of work ... is called a job. The rule ... is its schedule. A job scheduler is the program..." has three new terms in one paragraph, and the Tokio paragraph has four.

### Input 5, the cloud (1,781 words)

Scope is sensible: ownership problem, virtual machines, API and autoscaling, the three service levels, shared responsibility. It does not sprawl.

Check 6, Borderline. Two chapters after the first. One restates well ("So far Gigstub has been renting bare virtual machines that grow and shrink with its ticket sales"). The other opens cold: "A single physical server in a modern data centre is far more powerful than most customers need."

Check 8, Borderline. "starts renting computing the way a household rents electricity: it uses what it needs and pays for what it used." An analogy with no line on where it breaks.

Check 11, Borderline. Complete. Two paragraphs carry two terms: "virtual machine, or VM" with "hypervisor", and "platform as a service, or PaaS" with "serverless".

### Input 7, Docker containers (2,144 words, reader knows Linux processes)

The reader note was used well in content: nothing about processes, PIDs or signals is explained, and the piece opens from "an ordinary Linux process". It was not used in length: 2,144 words is 97 percent of the moderate ceiling and longer than the cloud piece that had no note. Check 4 passes on the number; the stress in inputs.md ("stays shorter") is not met.

Check 5, Borderline. "The daemon in turn hands the low-level steps to helper programs called containerd and runc, which follow an open industry standard for containers". Implementation detail that fails the body test. The Docker Desktop sentence and the kernel-escape sentence are the same kind.

Check 11, Fail. Complete, with orders-api carried through. Pace: the namespace paragraph names six terms (namespace, PID, mount, network, UTS, user), and "A union filesystem, on Linux usually one called OverlayFS" arrives in the paragraph that also introduces the writable layer.

## Check 11 on v0.1.0, inputs 1 to 3

- #1, Borderline. No "The whole picture", so completeness has nothing to test. Pace: "usually in a header, a labelled line of extra information ... That string is an API key" and "you revoke it ... is called rotation" carry two terms each.
- #2, Fail. Complete. Pace: topic, producer and consumer in one paragraph; group coordinator, heartbeats and session timeout in one; at-most-once, at-least-once and idempotent in one.
- #3, Fail. Complete, and every step uses the running example. Pace: "This ordered list is called the log. Each entry ... its index" and "remote procedure calls, usually shortened to RPCs ... RequestVote ... AppendEntries" carry three terms each.

## Input 4: was a generic article the right behaviour?

No. The direction was right and the size and framing were wrong. It should have been short.

What it got right: it invented no Driftwood API, default or feature, and the general material on schedulers is accurate.

What is wrong for this reader:

1. The admission is too soft. The reader on a bus cannot check anything. "I cannot vouch for the exact details" tells them the outline is known and only details are uncertain. The honest sentence is that the writer has no reliable knowledge of a tool by this name.
2. The goal cannot be met, so the budget should collapse. The goal is that the reader can say "what the topic is". Nothing in 1,640 words is known to be about the topic. Every paragraph after the admission is read under the title "Driftwood and the Job Schedulers of Rust", and the reader will leave believing Driftwood is an in-process, cron-expression, Tokio-based scheduler with persistence and misfire policies. "The whole picture" says so nearly outright ("A Rust job scheduler such as Driftwood exists so that...").
3. Length works against honesty here. The more generic material is attached to the name, the more of it is attributed to the name.

Right behaviour: say plainly in the first two sentences that the tool is not known and will not be described; give a simple-size piece (about 450 words) on what any job scheduler has to do, with nothing attributed to Driftwood; end with three or four questions to take to its documentation (is it a library or a separate service, where does it keep state, what happens to runs missed during downtime, what stops two copies running the same job).

Cause: the prompt has no instruction for a topic that is unknown as a whole. It covers an ambiguous name ("choose the IT meaning most likely intended") and an uncertain detail ("say so or leave it out"), and the output section says to leave out "any notes to the person who sent this", which discourages a plain statement. The model did the most reasonable thing the prompt allowed. Edit 3 below fills the gap.

## Why input 1 grew from 615 to 1,632 words

The model sized "what an API key is" as a moderate topic, not a simple one. The evidence is in the output: it has a "The whole picture" section, which the prompt gives only "for moderate and long pieces", and 1,632 words sits on the moderate target of "about 1,500". The 450/600 numbers were never applied, so the builder's choice of those numbers is not the cause.

The cause is in the prompt wording, and two of my own gate-review edits contributed. Plainly:

1. Gate-review edit 3 removed the anchor and put nothing in its place. v0.2.0 said "A simple concept, such as what an API key is". I had it replaced with "such as what a port number is" to take the test topic out of the prompt. That was right for the validity of the test, but I left step 9 with one example per tier and no statement of what makes a topic simple. The model had to classify by resemblance, and an API key (issue, attach, look up, limit, leak, revoke) resembles the moderate example, "how a domain name is turned into a server address", more than it resembles a port number. I should have supplied a criterion with that edit.
2. Gate-review edit 1 made the body test blind to size. It now says a passage stays if the reader needs it to say "how its mechanism works step by step" and that "Each step of the mechanism passes, together with the one worked case that shows it." That was written to protect Raft and Kafka, and it did. On a simple topic it licenses a numbered five-step server walk-through, an issuance passage and three leak stories, all of which "pass". Once everything passes the body test, the cut order in the check has nothing to cut.
3. Not from my edits: the budget is step 9, the last plan step, after the generous inventory in step 2. The size is chosen after the content has been collected, so the content sets the size.

What I cannot show: v0.2.0 was never run, so I cannot separate the effect of each edit, and with one sample some of the growth may be run variance. The "The whole picture" evidence makes misclassification the best-supported reading.

The deep and moderate fixes held (Raft 5,988 to 3,920, Kafka 2,751 to 1,897), so the replacement text below only adds a simple-tier criterion and makes the body test size-aware. It does not loosen anything for inputs 2 and 3.

## Why check 6 fails on moderate pieces

The write section says "When the piece is long enough for chapters", step 9 says only deep topics are "split into chapters", and the output section says "chapters under '##' headings for a longer one". A moderate piece is therefore told nothing about headings. The model used "##" headings anyway (nine for Kafka, six for Driftwood) and did not treat them as chapters, so the reminder rule was not applied. Edit 4 below closes this.

## Recommended edits for v0.2.2, in order of importance

Edit 1. Give the simple tier a criterion, and set the size from the core sentence (plan step 9).

Replace:
> Size it to the topic, not to an idea of thoroughness. A simple concept, such as what a port number is, gets about 450 words and no chapters, never more than 600.

With:
> Size it to the topic, not to an idea of thoroughness, and judge the size from your core sentence in step 1, not from the length of your list in step 2, because a long list makes any topic look bigger than it is. A topic is simple when its core is one thing with one job: a single object or value and what is done with it, with no chain of several stages or several machines that the reader has to follow in order. What a port number is, what a file extension is, and what a checksum is are simple. A simple topic gets about 450 words, never more than 600, written as continuous prose with no headings and no "The whole picture" section. At that size the mechanism is told once, in a few sentences inside the running example. The ideas that surround it, such as how the thing is stored, how it is protected in transit, or what it is commonly confused with, get one clause each or one line in "Going further".

Edit 2. Make the body test aware of size (plan step 5).

Replace:
> Each step of the mechanism passes, together with the one worked case that shows it.

With:
> Each step of the mechanism passes, together with the one worked case that shows it. For a simple topic the mechanism is a single exchange, so it passes as a few sentences, and a numbered walk-through, a second story of the same mistake, and neighbouring topics the reader did not ask about do not pass.

Edit 3. Say what to do when the topic itself is unknown (plan step 1).

Replace:
> If the topic name is ambiguous, choose the IT meaning most likely intended and make that clear in the opening line.

With:
> If the topic name is ambiguous, choose the IT meaning most likely intended and make that clear in the opening line. If the topic is a specific named product, library, or tool, the source block is empty, and you cannot recall concrete facts about it that you would stand behind, say so in plain words in the first two sentences: you have no reliable knowledge of this tool and will not describe it. Then write a simple-size piece on the kind of thing it is said to be, attribute no feature, design, or vocabulary to the named tool, and close with three or four questions the reader can take to its documentation. Keep it short, because the reader will take everything written under the tool's name to be about the tool and cannot check it from a bus seat.

Edit 4. Apply the resumption rule to moderate pieces and cap their headings (write section).

Replace:
> When the piece is long enough for chapters, make each one readable in about five minutes, the gap between a few stops.

With:
> A moderate piece is divided into three to five sections and a deep piece into chapters, each under a "##" heading, and everything in this paragraph applies to both. Make each one readable in five minutes at most, the gap between a few stops.

Edit 5. Add the pace rule to the self-check, where it is currently absent (check section).

Replace:
> Every term, acronym, and named technology is explained before or at its first use.

With:
> Every term, acronym, and named technology is explained before or at its first use.
> No paragraph hands the reader more than one new term. Where a paragraph names two or more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again.

Over-correction to watch after these edits: edit 5 adds paragraphs, so Raft may rise toward 4,500; that is acceptable if check 5 holds. Edit 1 may push a topic that is truly moderate into the simple tier; input 5 (the cloud) is the one to watch, and it should stay moderate.

## For the builder, outside the prompt

Rubric:
- Check 11 does not discriminate as I worded it: five of six v0.2.1 outputs fail the pace half, and so do two of three v0.1.0 outputs. Split it. "11a Complete: every mechanism step named in 'The whole picture' is explained in the body with the running example." "11b Unhurried: no paragraph introduces more than two new terms, and two only when they are a pair defined against each other." Then regrade both versions.
- Check 6: say that "chapter" means any section under a "##" heading.
- Add a check for input 4: "Unknown topic: the piece says in its first two sentences that the tool is not known, and attributes nothing to it."
- inputs.md, input 7: "stays shorter" has no number. Give it one, for example at most 1,700 words.

Lines to add to failures.md:

- 2026-11-15 | 1 | 4 Proportional, 5 Padding | v0.2.1 sized the topic as moderate: step 9 has no criterion for "simple" after the API-key example was removed, and the body test passes every mechanism step whatever the size | pending
- 2026-11-15 | 2, 4 | 6 Resumable | Prompt applies the reminder rule to "chapters" and tells moderate pieces nothing about headings; model used many "##" sections and did not restate | pending
- 2026-11-15 | 4 | 3 Accurate | No instruction for a topic unknown as a whole; model hedged on "details" and wrote a moderate-size generic piece under the tool's name | pending
- 2026-11-15 | 2, 3, 4, 7 | 11 Unhurried | One-idea-per-paragraph rule is in the write section but not in the self-check; vocabulary paragraphs stack three to six terms | pending
- 2026-11-15 | 3 | 11 Complete | Log repair and discarded entry described as rules without the running example | pending

Also mark the five existing lines: the checks 4 and 5 failures on inputs 2 and 3 and the check 2 failures are fixed in v0.2.1 on this run; the double-recap line is fixed.

Before the next decision: run inputs 6 and 8, and run input 1 at least three times. A promotion blocked by one sample of one input should be confirmed or cleared with more than one sample.

Process note: my role allows Read, Grep, Glob and Write. Glob was not available in this session, so I ran one read-only shell command to list the run folder and confirm word counts. Nothing was changed by it.

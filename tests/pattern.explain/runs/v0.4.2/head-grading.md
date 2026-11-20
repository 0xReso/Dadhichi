# Head grading: built/explain.commuter.it.md v0.4.2 (plus input 8 under finance 0.1.1)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the models that wrote the outputs, but its verdicts may not line up exactly with earlier head files.

Date: 2026-11-20. Stage: grading after the test run, plus a gate-review judgement of the five v0.4.2 edits after the fact.
Read: the design doc, rubric.md, inputs.md, failures.md, `tests/pattern.grade/conventions.md`, the frozen v0.4.2 prompt and its finance variant, my v0.4.0 and v0.4.1 gradings, the source pack `sources/alexa-for-shopping.md`, the design doc again as input 6's source, all 18 v0.4.2 samples, and v0.4.1 samples where I needed to check whether a passage was new.
Word counts: the builder's `wc -w` figures. They include Markdown tokens ("#", "##", one "-" per bullet), which matters only for 1b (see input 1).

I confirmed that the five edits from my v0.4.1 grading appear verbatim in the frozen prompt: edit 1 in the 11b check line, edit 2 in plan step 5, edit 3 in plan step 1, edit 4 in the running-example check line, and edit 5 in the linearity check line. The finance variant differs only in its domain block.

## Decision: NOT PROMOTED (v0.4.0 stays released). Status: NOT TESTED (stays draft)

| Shared set, 94 cells (worse sample per cell) | P / B / F |
| --- | --- |
| v0.4.0 (released) | 76 / 13 / 5 |
| v0.4.1 | 70 / 21 / 3 |
| v0.4.2 | 76 / 16 / 2 |

The design's rule has two parts, and v0.4.2 meets neither. It does not pass more checks: it ties at 76. It also fails a check the old version passed: input 1, check 4, where 1b runs to 616 words against a hard limit of 600. So it is not promoted.

That is the verdict under the comparison rule used in every earlier grading. It is not evidence that v0.4.2 is the worse prompt. Fails drop from 5 to 2. Input 4 goes from 8/3/0 to 11/0/0. The Fails on 2, 7, 8 and 9 are gone. Per sample, v0.4.2 passes 84.6 percent of cells on the shared inputs (159 of 188), against v0.4.0's 81.3 percent (126 of 155). Only 2 of its 16 shared-input samples have a Fail, against 6 of 13 for v0.4.0. All four lost Passes sit on inputs 1 and 5, where v0.4.0 has a single sample, and all four come from the second sample (1b, 5b). See "How I handle the n mismatch".

Single most important fix next: length. 1b goes over the trivial ceiling. Every moderate sample also lands above the 1,500 typical figure, and three land within 70 words of the 2,200 ceiling: 6a at 2,155, 8a at 2,131 and 8b at 2,168. The check's stop rule compares the draft with the upper limit, and the model's own length estimate runs short, so the next run's most likely Fail is a check 4 overrun. Edit 1 below addresses this.

## How I handle the n mismatch

v0.4.0 has n=2 on inputs 2, 3, 7, 8 and 9 and n=1 on inputs 1, 4 and 5. v0.4.2 has n=2 everywhere. My v0.4.1 grading compared versions by the worse sample per cell, whatever n each version had (input 3 there was v0.4.0 at n=2 against v0.4.1 at n=1). I apply the same rule here so the decision is made the same way as before. The bias now runs against the new version, and I say so instead of changing the rule to suit the result.

Sensitivity:
- Matched n using v0.4.2's "a" samples on 1, 4 and 5: 80 / 13 / 1, with no Pass-to-Fail. That would promote.
- Matched n using the "b" samples: 76 / 16 / 2, the same as the primary figure. That would not promote.
So at matched n the decision turns on which sample was drawn first. A fair bar needs v0.4.0 at n=2 on inputs 1, 4 and 5. That is three cheap runs, and they should be done before v0.4.3 is compared. Even then, the input 1 Pass-to-Fail stands unless v0.4.0's second API-key sample also goes past 600. So I recommend building v0.4.3 from v0.4.2 rather than re-arguing v0.4.2.

Input 6 is compared only with v0.4.1's single sample, and it stays out of the 94-cell set.

## How I applied the checks

- The rules are the same as in the last two gradings. For 11b, two new terms that are not a defined pair is Borderline, three or more is Fail, and a term plus a defined pair is Borderline. Product, project, company and command names count. Familiar consumer names given as examples (Alexa, Prime, The New York Times) and personal names given as attribution (Macaulay) do not count. An everyday word the topic gives its own meaning counts, as "entry" did in my v0.2.1 Raft grading.
- conventions.md applies throughout: padding is judged per passage, one cold section is Borderline on check 6, a promise clause is Borderline on check 2, and one self-contradiction is Borderline on check 3.
- Check 4 uses the rubric's hard limits (600, 2,200, 4,500). For input 7, going over inputs.md's 1,700 would be Borderline, and neither sample does. Going over the prompt's typical figure is noted but not scored.
- Kept as notes, not verdicts, so the comparison stays fair. 7a says "Docker gives every container a fresh one of each" kind of namespace, next to "root inside a container is root on the host kernel". By conventions.md that is a self-contradiction. v0.4.0 7b had the same pair and I recorded it as a note, so it stays a note. Scoring it would lower v0.4.0 and v0.4.2 by one Pass each on input 7, and the decision would not change.

## Score table, v0.4.2, every sample

P = Pass, B = Borderline, F = Fail, - = not applicable. Word counts in brackets.

| # | Check | 1a (554) | 1b (616) | 2a (1,737) | 2b (1,917) | 3a (3,448) | 3b (2,622) | 4a (546) | 4b (525) | 5a (1,701) | 5b (1,731) | 6a (2,155) | 6b (2,030) | 7a (1,544) | 7b (1,646) | 8a (2,131) | 8b (2,168) | 9a (1,692) | 9b (1,885) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P | P | B | B | P | P | P | P | P | P | B | B | P | P | P | P | P | B |
| 2 | Linear | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 3 | Accurate | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 4 | Proportional | P | F | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 5 | No padding | P | B | P | B | B | B | P | P | P | B | B | B | B | B | B | B | B | B |
| 6 | Resumable | - | - | P | P | P | P | - | - | P | P | P | P | P | B | P | P | P | P |
| 7 | Plain text | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 11a | Complete | - | - | P | P | P | P | - | - | P | P | P | P | P | P | P | P | P | P |
| 11b | Unhurried | P | P | B | B | F | B | P | P | P | B | B | B | B | B | B | B | B | B |
| 12 | Unknown topic | - | - | - | - | - | - | P | P | - | - | - | - | - | - | - | - | - | - |
| 13 | Source confidence | - | - | - | - | - | - | - | - | - | - | P | B | - | - | - | - | B | B |
| | P / B / F | 10/0/0 | 8/1/1 | 10/2/0 | 9/3/0 | 10/1/1 | 10/2/0 | 11/0/0 | 11/0/0 | 12/0/0 | 10/2/0 | 10/3/0 | 9/4/0 | 10/2/0 | 9/3/0 | 10/2/0 | 10/2/0 | 10/3/0 | 9/4/0 |

All 214 sample cells: 178 Pass, 34 Borderline, 2 Fail. 16 of 18 samples have no Fail. (A correction to my v0.4.1 file: it said 7 of 13 v0.4.1 samples were free of Fails. The right figure is 9 of 13, since only 2b, 4, 9a and 9b failed. v0.4.0 was 7 of 13.)

## Comparison on shared cells (worse sample per cell)

| Input | Cells | v0.4.0 | v0.4.1 | v0.4.2 | v0.4.2 splits |
| --- | --- | --- | --- | --- | --- |
| 1 API key | 10 | 10/0/0 (n=1) | 10/0/0 (n=1) | 8/1/1 | 4 (P/F), 5 (P/B) |
| 2 Kafka | 12 | 9/2/1 | 9/2/1 | 9/3/0 | 5 (P/B) |
| 3 Raft | 12 | 10/2/0 | 9/3/0 (n=1) | 10/1/1 | 11b (F/B) |
| 4 Driftwood | 11 | 8/3/0 (n=1) | 8/2/1 (n=1) | 11/0/0 | none |
| 5 Cloud | 12 | 12/0/0 (n=1) | 10/2/0 (n=1) | 10/2/0 | 5 (P/B), 11b (P/B) |
| 7 Docker | 12 | 9/2/1 | 7/5/0 | 9/3/0 | 6 (P/B) |
| 8 Bond (finance) | 12 | 10/1/1 | 9/3/0 | 10/2/0 | none |
| 9 Alexa | 13 | 8/3/2 | 8/4/1 | 9/4/0 | 1 (P/B) |
| Total | 94 | 76/13/5 | 70/21/3 | 76/16/2 | |
| 6 Dadhichi doc (not in total) | 13 | - | 8/5/0 (n=1) | 9/4/0 | 13 (P/B) |

Against v0.4.0:
- Better: #2 11b F to B. #4 check 1 B to P, check 5 B to P, 11b B to P. #7 11b F to B. #8 11b F to B. #9 check 3 B to P, 11b F to B, 13 F to B.
- Worse: #1 check 4 P to F and check 5 P to B (both 1b). #3 11b B to F (3a). #5 check 5 P to B and 11b P to B (both 5b).
- Pass to Fail: #1 check 4.

Against v0.4.1: 76 against 70 Passes and 2 against 3 Fails. Better: #2 11b; #3 check 2; #4 checks 1, 5 and 11b; #7 checks 2 and 3; #8 check 8; #9 checks 3 and 11b. Worse: #1 checks 4 (P to F) and 5; #3 11b (B to F). Input 6: 11a goes from B to P, and nothing gets worse.

## Gate judgement of the five v0.4.2 edits (after the fact)

I would approve all five again. Each one hit its target, and none caused a regression on its own target. Two things need watching: a loophole in edit 2's limits clause, and the growing length of the check section.

- Edit 1 (a gloss that needs a name is a new term): worked. The four Fails it targeted are now B on 2b, P on 4, B on 9a and B on 9b. Kafka 2b's coordinator paragraph no longer brings in the group leader ("decides, or in older versions oversees"). The Alexa+ paragraph carries two terms, and Echo has its own paragraph, so the continuity point from the watch item survived (9a: "Later, on the bus, you open the Amazon Shopping app ... and carry on with the same conversation"). What is left are two-term glosses, which score B: "Claude Sonnet, a general-purpose model made by the AI company Anthropic" (both 9), and "the Docker daemon, a background service on the host (its program is called dockerd)" (7a), where dockerd is never used again. Over-correction check: some one-sentence paragraphs ("The second is a family of Amazon's own general-purpose models, called Nova."; "The date of that final repayment, five years from now, is called the maturity."). They read as a list set out in prose, not as choppy.
- Edit 2 (second traps, variants and usage figures leave the body): partly worked. Gone: Cloud's "A second, smaller trap", 8b's twice-a-year paragraph, 8b's portfolio paragraph, 9b's Echo misconception and 9a's statistics. Raft's limits and the bond pieces' convexity sections stayed, as the watch asked. Still there: "On macOS and Windows, Docker gets a Linux kernel by running these processes inside a hidden Linux virtual machine" (7a), "on a Mac or a Windows laptop, Docker Desktop quietly runs a small Linux virtual machine" (7b), and "for bonds that pay twice a year, the yield is split across the two periods" (8a). All three are single sentences. The write section still says "Where behaviour differs between versions, vendors, or configurations, say so in one sentence", which licenses exactly these, so the prompt contradicts itself here. Edit 3 below reconciles the two. Loophole: the clause "Limits of the mechanism itself ... stay in the body" is now how removed material comes back. 5a's limits paragraph carries the old second trap ("a workload that is large and steady all year can cost more rented than owned"), and 8b's "A third limit follows from the first two: duration is a snapshot" repeats the drift point made in its seesaw paragraph. Check 5 is still B on 7 of 8 shared inputs, the same count as v0.4.1. The bond pieces grew again, from 1,937 to 2,131 (8a) and from 2,022 to 2,168 (8b).
- Edit 3 (no notation in the unknown-tool piece): worked fully. Neither sample has cron, Unix or a notation passage, and the format question moved to the closing list ("How do you write down when a job should run?"). Both samples score 11/0/0 at 546 and 525 words. 4b titles its closing list "## Questions for Driftwood's documentation" where the prompt allows only "Going further". No check fails because of it. Watch it.
- Edit 4 (the running example keeps its state): worked. 7b's Dockerfile now copies the code before `pip install` and says "a rebuild after a code change redoes only the steps from the first changed one onward", which is correct. 7a's "Each instruction that changes files produces a layer" also fixes the old start-command note. The 20 percent average is gone from 9a. Raft 3a tracks state through every event (A offline, A restarts, C leads term 2, partition, heal). 3b's hypothetical says which moment it starts from: "Suppose A, back from its outage, had timed out before hearing from C".
- Edit 5 (promises, not just phrases about "next"): worked. Check 2 passes on all 18 samples, and none of the quoted example phrases was copied. 3b turns the old promise into content: "That shared server is Raft's thread of memory: whatever one majority agreed to, at least one member of any later majority knows about it." 3a's "Majorities also have a property that matters a great deal" gives its consequence two sentences later in the same paragraph, so I pass it.

Design rules: the seven sections and the calm wording are intact. Edit 2's "Nor does ..." is the only new negative sentence, and it carries both a reason and a positive alternative. Colleague test: the 11b check line is now about 190 words in one paragraph, and the source paragraph about 520. Edits 2 and 4 below lengthen the check section further. Split both into separate check lines when patterns/explain.md is split out.

## Evidence, input by input

### Input 1, API key (1a 554, 1b 616)

1b check 4, Fail. 616 is over both the rubric's and the prompt's 600 ("never more than 600"). Leaving out the six Markdown tokens still gives about 610 words of prose. The extra words are a passage the simple-topic rule sends to one clause: "That count lets the company enforce a rate limit, a cap on how many questions one key may ask in a given time. If your free plan allows a thousand forecasts a day, the thousand-and-first is refused until the count resets." The same passage is the check 5 B. Neither sample is near the 450 typical figure.
1a passes every check, as v0.4.0 and v0.4.1 did. "$5 per thousand", a million maps and $5,000 all agree. The trap is the key copied into public code. HTTPS in 1b is introduced in the sentence that uses it.

### Input 2, Kafka (2a 1,737; 2b 1,917)

The Fail is gone: 2b's coordinator paragraph has the coordinator alone. 11b is B in both. 2a: "Each new event goes into exactly one of them. Usually the event carries a key" (partition and key) and "a step called committing, and the recorded position is called the committed offset". 2b: "Kafka runs on a cluster of servers" in the Kafka paragraph.
Check 1, B in both. 2a: "the official Java client does it every five seconds by default" (Java bare, as in v0.4.0 2b). 2b: "In the original design of the protocol the whole group pauses", where no protocol has been introduced (as in v0.4.1 2b).
2b check 5, B: "By default the consumer software commits automatically every five seconds. Many teams turn that off ..." (a configuration default and an option), and "A member that is alive but takes too long between requests for new messages is treated the same way" (a refinement). 2a passes. Its version difference is the one sentence the write section allows.
Accuracy, checked: 2a's 3 × 500 and 6 × 500 match the 3,000 a second arriving, and 10,200 to 10,250 gives 50 repeats. 2b's 50 a second per copy, falling behind by 100 a second, 6,000 a minute, and 50 a second after the crash are all correct. 2b's "group billing has finished partition 3 up to offset 5,000" departs from Kafka's next-offset convention but agrees with itself ("starts after offset 5,000"). That is a note, not a verdict.

### Input 3, Raft (3a 3,448; 3b 2,622)

3a 11b, Fail: "Raft calls this ordered list the log. Each item in it is an entry holding one command, and each entry has a position number called its index". That is the log, the entry and the index together, the "this is called A, that is B, and the other is C" form that plan step 4 names, and the same three terms I failed in v0.2.1. If "entry" were read as a plain word, this would be B, and the decision would not change. 3b is B: "This list is called the log" with "written as an entry", and consensus with Raft.
Check 5, B in both, as in every earlier run. 3a: "Two researchers at Stanford University published it in 2014, with the stated aim ..." and "most implementations tell it which server is the current leader". 3b: "It was published in 2014 with the stated aim ..." and the same follower redirect.
Running example, checked in both. 3a: term 1 elected with A, B and C. E misses index 1, and the back-off sends index 1 and index 2. Index 3 of term 1 is on A and B only. C wins term 2 with D and E, and B refuses. B's conflicting entry is deleted. The partition is C and D against A, B and E, and E commits index 4 in term 3. Everything is right, including "a four-server cluster ... survives only one failure". 3b: A's term-4 entry at position 7 is overwritten by C's term-5 entry, the vote comparison is right, and the six-server arithmetic is right. Both put the current-term commit rule correctly in "Going further". The earlier state notes (E "ends at index 5", "B, still leader") are gone.
Checks 2, 6, 9 and 11a pass in both. Each chapter opens with what the reader holds ("C now leads term 2, and all five logs hold the same three committed entries"). The trap is "there is always one leader" (3a) and "safe once the leader has written it" (3b).

### Input 4, Driftwood (4a 546; 4b 525)

Both score 11/0/0, the first clean input 4 in any version. Check 12 passes: "I have no reliable knowledge of a tool called Driftwood and will not describe it", said once. Rust is explained in the first body paragraph. Job, job scheduler, retry and idempotent each get a paragraph. The trap is "exactly once, exactly on time". 4a's "a reliable alarm clock with a logbook, not a guarantee" states where the picture stops.

### Input 5, the cloud (5a 1,701; 5b 1,731)

5a scores 12/0/0. AWS and the second trap are gone, and the arithmetic is right (17,520 server-hours, plus 108, which is "a little over half a percent", against 175,200).
5b check 5, B: "There is one more choice to make when renting: where in the world the machines are. ... each group is called a region." This is an option the goal does not need. "Going further" lists availability zones, and the region passage takes a paragraph in the body.
5b 11b, B: "It is called a data centre. A cloud provider is a company that runs many data centres" (two terms). Server and client are a defined pair, so that paragraph passes.
5b arithmetic is right: 876 dollars a year at 5 cents, and 864 extra machine-hours, about 43 dollars.

### Input 6, Dadhichi design doc as long source (6a 2,155; 6b 2,030)

I checked every fact against the design doc. Both get the kernel, the four kinds of part, the precedence order, the engine's four steps and returns, the five required stresses, the promotion rule, the failure-log fields, the version levels and `verified_on` right. 6a fixes the v0.4.1 overstatement: "The design credits this step with preventing both over-explaining and under-explaining." Both run the API-key request through the engine ("For your request, the engine would classify it as explain / commuter / it"), so 11a goes from B to P.
Check 1, B in both: "Following Anthropic's guidance" (6a) and "the document cites Anthropic's published prompting guidance" (6b). Anthropic is never introduced, which recurs from v0.4.1 and is now confirmed at n=2. 6a's "Going further" line "Claude Project: the design suggests loading the library folder into one" also does not say what a Claude Project is.
6b check 13, B: "Your API key is the trivial case ... Bond duration is the second-field case, which asks whether the pattern really works outside IT." The doc names the API key as a roadmap topic and bond duration as the swap example. It never assigns either one to a required test category, so this is the writer's mapping stated as the design's. 6a passes: it marks its one join ("this joining is my reading of the design rather than its words") and keeps the API key to "one of the first three topics the roadmap names".
Check 5, B in both: the Git and version-number paragraphs are Later-tier (6a: "The whole library lives in a Git repository ..."; 6b: "All of this lives as plain text files in Git ..."). 6b also has the CRITICAL aside. 6a sits 45 words under the 2,200 ceiling.
11b, B in both. 6a: "A prompt is the written instruction you give an AI model such as Claude" and "a library of tested, reusable prompts, plus an engine". 6b: "Dadhichi ... plus an engine".

### Input 7, Docker (7a 1,544; 7b 1,646; reader knows Linux processes)

The 11b Fail is gone (v0.4.0 7b's Dockerfile, build and tag paragraph). 11b is B in both: "Docker is a set of tools ... That fenced-off process is a container", "the Docker daemon ... (its program is called dockerd)", and cgroups with the out-of-memory killer (7a); "removing the container with `docker rm` ... which Docker calls a volume", and cgroups with the OOM killer (7b).
Check 5, B in both, on the platform sentence quoted under edit 2. 7a also has "Docker reports the container exited with code 137, which is 128 plus signal 9", which is trivia.
7b check 6, B: "The image: a filesystem that does not change" opens "The package is a directory tree frozen in place", with no reminder of the Python 3.12 against 3.8 problem. Every later section restates. 7a's second section now restates ("So the goal is to ship orders-api with its own Python and its own libpq, without disturbing the host"), which fixes the 7a B that ran through v0.4.0 and v0.4.1.
Check 4 passes in both, under 1,700. Both are over the prompt's own 1,500 ceiling for a reader note, by 44 and 146 words. That is noted, not scored.
Accuracy notes: 7b's "/usr/bin/python3.12" (the official Python images install to /usr/local/bin, which 7a gets right), and the namespace and root pair in 7a (see "How I applied the checks").

### Input 8, bond duration, finance 0.1.1 (8a 2,131; 8b 2,168)

I checked every figure. Present values at 5 percent are 47.62, 45.35, 43.19, 41.14 and 822.70, which sum to 1,000. At 6 percent the price is 957.88, Macaulay duration 4.55, modified duration 4.33, the estimate 956.71, and the price at 4 percent 1,044.52. 8a: the zero-coupon prices of 783.53 and 747.26 (a 4.6 percent drop), and 25 basis points is 10.82. 8b: the 30-year 5 percent bond has a duration of about 16 years (Macaulay 16.1). All correct.
The 11b Fail is gone in both. 11b is B: "the interest compounds ... this way is called discounting" (8a), and "the payment's present value ... A payment further away is discounted more" (8b).
Check 5, B in both. 8a: the twice-a-year sentence, the basis-point paragraph ("Real rate moves are usually smaller than a full point. Traders measure them in basis points") and the fund paragraph ("A bond fund that reports a duration of six years ..."). 8b: "A third limit follows from the first two: duration is a snapshot. It changes as yields change", which repeats "which is why duration has to be recalculated as rates change", and the usage paragraph "When traders and fund managers say 'duration' without a qualifier ...".
Check 8, P in both. 8b's seesaw now says where it stops ("The picture holds for a fixed yield; it stops being true once yields move"), which clears v0.4.1's B. 8a's plank does the same. Note: 8a's "This is the pair most often muddled" passes the domain block's wording on to the reader. It is harmless, and I record it on the existing watch line.
Length: 8b is 32 words under the ceiling and 8a 69 words under. These are the two cells most likely to fail next.

### Input 9, Alexa for Shopping (9a 1,692; 9b 1,885)

| | v0.4.1 9a / 9b | v0.4.2 9a | v0.4.2 9b |
| --- | --- | --- | --- |
| M1 invented provenance | fixed / fixed | fixed ("produced by another AI assistant and not by Amazon") | fixed |
| M3 join called confirmed | recurs / bridge question | heading and recap join ("an answer grounded in fetched material and your own order history") | "Being part of Alexa+ means ..." and the bridge question |
| M4 exclusivity | fixed / softened | "the one component Amazon does describe for choosing between models" (true as worded, so passed) | fixed ("a component Amazon did confirm") |
| M5 absence where silent | fixed / fixed | fixed | fixed |
| 20 percent applied to one purchase | recurs / - | gone | gone |

The 11b Fail is gone in both. 11b is B: Alexa+ with generative AI, Claude Sonnet with Anthropic, and account memory with Review Alexa History (both). 9b also has COSMO with knowledge graph.
Check 13, B in both. 9a files the past-orders check, price history and account memory under the heading "Fetching before answering", and the next section's reminder joins them: "You now have an answer grounded in fetched material and your own order history". Its prose does keep them apart ("can also", "also keeps"), and its whole-picture paragraph lists them separately. 9b: "Being part of Alexa+ means it shares conversation context with Amazon's Echo smart speakers" makes a causal join that the pack does not state. Its bridge question ("such as today's price of a grinder or what you ordered last year. Where do those come from?") is answered by "The assistant deals with that in a few ways. The main one is called RAG." 9b does mark one join correctly: "treating them as one feature would be a reading of mine, not something Amazon states".
9b check 1, B: "Prompt caching and parallel tool calling: Bedrock features Amazon says it uses to make replies arrive faster" still does not say what either one is. 9a defines both.
Check 5, B in both: the customer-service paragraph (as in every run), plus advice ("A tidy diagram full of real product names can still be wrong in the one place that matters"; "If you see this diagram, read it as a plausible sketch with a known gap").
Check 3, P in both. The prices are consistent ($49.99, $42 and the six-month window in 9a; $160 and $130 in 9b), and nothing contradicts Buy for Me.

## Readiness for `tested`

Not tested. These cells block it:
1. Fails, of which the full set must have none: 1b check 4 (616 words) and 3a 11b (log, entry and index).
2. Roadmap step 1's exit (inputs 1 to 3 pass checks 1 to 5 in both samples): 1b check 4 F and check 5 B; 2a and 2b check 1 B; 2b check 5 B; 3a and 3b check 5 B.
3. Promotion: a version that is not promoted over the released one cannot be the tested release.
4. The human check (a phone read of 1 and 2) has still not been done.

No `status` or `verified_on` change. Keep `status: draft`, keep v0.4.0 as the released version, and add to the v0.4.2 header comment: "0.4.2 graded 2026-11-20, not promoted: 76/16/2 vs 0.4.0's 76/13/5 on 94 shared cells (worse sample per cell); one Pass-to-Fail (input 1 check 4, 1b 616 words); Fails 5 to 2; 84.6% of sample cells pass vs 81.3%".

## Recommended edits for v0.4.3, in order of importance

Build from v0.4.2 and keep all its edits. All five below refine existing rules and keep the output shape, so this is a patch. Before grading v0.4.3, run v0.4.0 once more on inputs 1, 4 and 5 so that both versions are compared at n=2.

Edit 1. Hold the typical figure, not the ceiling (check section). Targets: 1b check 4 F and check 5 B, the near-ceiling 6a, 8a and 8b, and check 5 on 5b and 8a.

Replace:
> If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is.

With:
> Then compare the estimate with the typical figure for the size, not with the upper limit, and assume your estimate runs short, because a draft judged from the inside usually does. If it is more than about a fifth over the typical figure, which is about 540 words for a simple topic, 1,800 for a moderate one, and 4,200 for a deep one, cut again in the same order until it is not. Stop cutting only when what is left is the problem, each mechanism step with its one worked case, the trap, and the limits of the mechanism. In a simple piece, an idea around the single exchange, such as what the service counts or caps, gets one clause or one line in "Going further", not a paragraph of its own. A piece that lands near the upper limit in one run goes over it in the next, so the typical figure is the one to hold.

Over-correction risk: this is a length fix, and those often make output terse. Watch for 11a on 2, 3, 6 and 9 (no mechanism step dropped), the zero-coupon and convexity passages in 8, the limits chapter in Raft, and 11b going up if explanations get squeezed instead of whole ideas being removed. 3a at 3,448 should need no cut.

Edit 2. Everyday words with a topic meaning count as terms (check section). Target: 3a 11b F, and 2a's partition and key.

Replace:
> No paragraph hands the reader more than one new term, and the names of products, projects, companies, commands, and the boxes or layers of a diagram count as terms.

With:
> No paragraph hands the reader more than one new term, and the names of products, projects, companies, commands, and the boxes or layers of a diagram count as terms. So does an everyday word the topic gives a meaning of its own, such as an entry, a term, or a key, because the reader has to learn the new meaning just as they would a new name. A sentence that names a thing, then its items, then their numbering ("this list is called the log, each item is an entry, and each entry has an index") hands over three terms: give the first its own paragraph and let the others arrive where the running example first uses one.

Watch: one-sentence paragraphs in the Raft opening.

Edit 3. Reconcile the write section with plan step 5 on variants (write section). Targets: check 5 on 7a, 7b and 8a (the platform and payment-schedule sentences), check 5 and check 1 on 2b ("In the original design of the protocol").

Replace:
> Where behaviour differs between versions, vendors, or configurations, say so in one sentence instead of presenting one case as universal, and put the details, if they are worth keeping, in "Going further".

With:
> Where behaviour differs between versions, vendors, platforms, or configurations, describe the case the running example is in and qualify that sentence in a few words, such as "by default" or "in recent versions", so it is not presented as universal. Put the other cases, if they are worth keeping, in "Going further" as one line each, because a sentence about a case the reader is not in is a passage they must hold for nothing.

Watch: check 3 on 2 and 7. The qualifier must survive, so that the rebalance pause and the auto-commit default are not stated as universal.

Edit 4. Attribution names and "Going further" lines (check section). Targets: check 1 on 6a and 6b (Anthropic, Claude Project) and 9b (prompt caching).

Replace:
> Every term, acronym, and named technology is explained before or at its first use.

With:
> Every term, acronym, and named technology is explained before or at its first use. That includes a company or body named as the origin of a finding or a guideline, which needs a few words on who it is or can be left out, and every line in "Going further", which says in plain words what its term is, not only who uses it or why, because the reader meets that line with nothing else to go on.

Edit 5. Framing sentences are joins too (check section). Targets: check 13 on 9a, 9b and 6b.

Replace:
> If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture".

With:
> If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture". Read the sentences that frame each section too: its opening reminder, its closing question, and any "means", "so", or "the main one" that links two features. If one of them presents features the source gives separately as one mechanism, or one as the cause of the other, or places your running example in a category the source never assigns it to, rewrite it to name each on its own, because a frame states a join as plainly as any other sentence.

The scope scan that follows ("Then find every sentence that says 'only' ...") stays unchanged.

Not proposed: the customer-service paragraph in 9 and the history sentence in 3. Both are long-standing check 5 Borderlines and do not block. Edit 1's cutting order should reach them.

## Failure log

Updates to existing lines:
- Line 38 (glosses that bring in names): fixed in 0.4.2 for its targets (the Fails on 2b, 4, 9a and 9b become B, P, B and B). Two-term glosses remain at B: "made by the AI company Anthropic" (9a, 9b) and "(its program is called dockerd)" (7a).
- Line 39 (second traps, variants, usage figures): partly fixed in 0.4.2. Gone: Cloud's second trap, 8b's twice-a-year and portfolio paragraphs, 9b's Echo misconception, 9a's statistics. Remaining: the Docker Desktop sentence (7a, 7b), 8a's twice-a-year sentence and 5b's region paragraph. Cause: the write section's "say so in one sentence" (0.4.3 edit 3). The limits clause has become a route back in (5a's "can cost more rented than owned"; 8b's "A third limit"). The bond pieces grew to 2,131 and 2,168.
- Line 40 (Driftwood notation): fixed in 0.4.2 (4a and 4b both 11/0/0).
- Line 41 (running-example state): fixed in 0.4.2 (7b layer order, 9a average, Raft state in 3a and 3b).
- Line 42 (promise clauses): fixed in 0.4.2. Check 2 passes on 18 of 18 samples.
- Line 43 (AWS used once): fixed in 0.4.2.
- Line 44 (8b seesaw, "maps"): fixed in 0.4.2. The seesaw recurs but states its limit, and "oldest map" is gone. Keep watching: 8a's "This is the pair most often muddled" echoes the finance block's pair list.
- Line 45 (input 6, watch until n=2): resolved at n=2. The "matters most" overstatement, the engine section without the running example and the wrong referent are fixed. Anthropic left bare recurs in both samples: promoted to a failure line below. The Git and version paragraphs recur in both (check 5 B).
- Line 37 (user namespaces): recurs in 7a as "Docker gives every container a fresh one of each" next to "root inside a container is root on the host kernel", which is a self-contradiction. Still a note. Keep watching.

Lines to add:
- 2026-11-20 | 1 (1b), and 6a, 8a, 8b near the line | 4 Proportional, 5 Padding | The check's stop rule compares the draft with the upper limit, and the model's estimate runs short. 1b is 616 words, with a rate-limit paragraph kept in a simple piece. Every moderate sample lands above 1,500, and three land within 70 words of 2,200 | pending (0.4.3 edit 1)
- 2026-11-20 | 3 (3a) | 11b Unhurried | Everyday words given the topic's meaning are not counted: "Raft calls this ordered list the log. Each item in it is an entry ..., and each entry has a position number called its index" | pending (0.4.3 edit 2)
- 2026-11-20 | 2b, 7a, 7b, 8a | 5 Padding, 1 No lookups (2b) | The write section's "say so in one sentence" licenses the variant sentence that plan step 5 sends to "Going further": Docker Desktop on Mac and Windows, "for bonds that pay twice a year", "In the original design of the protocol" | pending (0.4.3 edit 3)
- 2026-11-20 | 6a, 6b, 9b | 1 No lookups | Attribution companies and "Going further" lines are not checked: "Following Anthropic's guidance" (both input-6 runs); "Claude Project: the design suggests loading the library folder into one"; "Prompt caching and parallel tool calling: Bedrock features Amazon says it uses" | pending (0.4.3 edit 4)
- 2026-11-20 | 6b, 9a, 9b | 13 Source confidence | Joins made by framing sentences: "You now have an answer grounded in fetched material and your own order history" under "Fetching before answering" (9a); "Being part of Alexa+ means it shares conversation context with Amazon's Echo smart speakers" and "The main one is called RAG" (9b); "Your API key is the trivial case ... Bond duration is the second-field case" (6b) | pending (0.4.3 edit 5)
- 2026-11-20 | 4b | output shape (no check fails) | A simple piece uses "## Questions for Driftwood's documentation" in place of "Going further" | watch

## Before the next decision

- Run v0.4.0 on inputs 1, 4 and 5 once more, so that the released version has n=2 everywhere.
- Run v0.4.3 at n=2 on inputs 1 to 9.
- Do the human check on 1 and 2 once.

Process note: this session had Read, Grep, Glob and Write only, with no shell. Nothing outside this file was changed.

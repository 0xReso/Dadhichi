# Head grading: built/explain.commuter.it.md v0.4.1 (plus input 8 under finance 0.1.1)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the models that wrote the outputs, but its verdicts may not line up exactly with earlier head files.

Date: 2026-11-18. Stage: grading after the test run, plus a gate-review judgement of the five v0.4.1 edits after the fact.
Read: the design doc, rubric.md, inputs.md, failures.md, the frozen v0.4.1 prompt (and the finance variant's header and domain block), my v0.4.0 grading, the source pack `sources/alexa-for-shopping.md`, all 13 v0.4.1 samples (1, 2a, 2b, 3, 4, 5, 6, 7a, 7b, 8a, 8b, 9a, 9b), and the v0.4.0 samples wherever I needed to check whether a passage was new.

Word counts: I used the builder's `wc -w` figures. This session had no shell, so I counted the three it did not give by paragraph: 3 is about 3,100, 7b about 1,580, and 9b about 1,850 (allow about 5 percent either way). None is near a line.

## Decision: NOT PROMOTED (v0.4.0 stays released). Status: NOT TESTED (stays draft)

| Shared set, 94 cells (worse verdict per cell) | P / B / F |
| --- | --- |
| v0.3.0 | 69 / 17 / 8 |
| v0.4.0 (released) | 76 / 13 / 5 |
| v0.4.1 | 70 / 21 / 3 |

The design's rule has two parts: the new version must pass more checks, and it must fail no check that the old one passed. v0.4.1 meets the second part. No cell goes from Pass to Fail, and its Fails drop from 5 to 3. It does not meet the first part: it passes 6 fewer cells (70 against 76). So it is not promoted.

The five edits did what they were written to do (see the gate judgement): 11b went from F to B on input 7 and input 8, and 13 went from F to B on input 9. The lost Passes are all in cells the edits did not touch, and every one comes from a passage that is new in this run. I checked each against v0.4.0, so this is not drift in my grading. The passages are a "second trap" and an AWS mention in Cloud, a seesaw simile in 8b, a promise clause in Raft and in 7a, and a Dockerfile order in 7b that contradicts the text after it. Five of the eight inputs ran at n=1, so much of this is likely sampling noise. The design's rule still applies: a change that looks harmless gets the full run, and the run says no.

Recommendation: build v0.4.2 from v0.4.1, not from v0.4.0, because its edits worked on their targets. Run every input at n=2, inputs 1, 3, 4, 5 and 6 included, so that one stray paragraph does not decide a promotion.

Most important fix next: one pattern now causes all four remaining Fails (2b, 4, 9a, 9b). The explanation of a term brings in a second name, and sometimes a third. Examples: "folded into Alexa+, which is Amazon's generative-AI version ... Generative AI here means ... Echo devices", "a cron expression, borrowed from the long-standing Unix tool named cron", and "In the classic version of the protocol one member, the group leader". Edit 1 below targets it.

## How I applied the checks

- The rules are the same as in the v0.4.0 grading. For 11b, two new terms that are not a defined pair is Borderline, three or more is Fail, and a term plus a defined pair is Borderline. Product, project, company and command names count. A name used only as an adjective (as "generative-AI version" was in v0.4.0) does not count. Once the piece defines it ("Generative AI here means ..."), it counts.
- Input 6 has no earlier version. I scored it on its own (13 cells, including check 13, because it has a SOURCE) and kept it out of the 94-cell comparison.
- Self-consistency slips (the grader test's warning). I checked each output against itself. Where a slip makes a technical claim wrong by the output's own terms, I score it under check 3: 7b and 9a. Where it is a timeline pause that leaves the mechanism correct, I record it as a note, as I did for v0.4.0 Raft: input 3. If those notes were scored, both Raft versions would drop to B on check 3 and the comparison would not change.
- 7a and 7b both say that every Dockerfile step makes a layer, the start command included. v0.4.0 7a said the same, and I recorded it as a note in every version, so it stays a note. 7b has a new and different slip, which I score (see input 7).

## Score table, v0.4.1, every sample

P = Pass, B = Borderline, F = Fail, - = not applicable.

| # | Check | 1 (585) | 2a (1,938) | 2b (1,784) | 3 (~3,100) | 4 (508) | 5 (1,764) | 6 (2,038) | 7a (1,524) | 7b (~1,580) | 8a (1,937) | 8b (2,022) | 9a (1,794) | 9b (~1,850) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P | B | B | P | B | P | B | P | P | P | P | B | B |
| 2 | Linear | P | P | P | B | P | P | P | B | P | P | P | P | P |
| 3 | Accurate | P | P | P | P | P | P | P | P | B | P | P | B | P |
| 4 | Proportional | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 5 | No padding | P | P | B | B | B | B | B | B | B | B | B | B | B |
| 6 | Resumable | - | P | P | P | - | P | P | B | P | P | P | P | P |
| 7 | Plain text | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | P | P | P | P | P | P | P | P | P | P | B | P | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 11a | Complete | - | P | P | P | - | P | B | P | P | P | P | P | P |
| 11b | Unhurried | P | B | F | B | F | B | B | B | B | B | P | F | F |
| 12 | Unknown topic | - | - | - | - | P | - | - | - | - | - | - | - | - |
| 13 | Source confidence | - | - | - | - | - | - | B | - | - | - | - | B | B |
| | P / B / F | 10/0/0 | 10/2/0 | 9/2/1 | 9/3/0 | 8/2/1 | 10/2/0 | 8/5/0 | 8/4/0 | 9/3/0 | 10/2/0 | 10/2/0 | 8/4/1 | 9/3/1 |

All 156 sample cells: 118 Pass, 34 Borderline, 4 Fail. Seven of 13 samples are free of Fails (v0.4.0: 7 of 13).

## Comparison on shared cells (worse verdict per cell)

| Input | Cells | v0.4.0 | v0.4.1 | v0.4.1 splits |
| --- | --- | --- | --- | --- |
| 1 API key | 10 | 10/0/0 | 10/0/0 | n=1 |
| 2 Kafka | 12 | 9/2/1 | 9/2/1 | 5 (P/B), 11b (B/F) |
| 3 Raft | 12 | 10/2/0 (n=2) | 9/3/0 (n=1) | - |
| 4 Driftwood | 11 | 8/3/0 | 8/2/1 | n=1 |
| 5 Cloud | 12 | 12/0/0 | 10/2/0 | n=1 |
| 7 Docker | 12 | 9/2/1 | 7/5/0 | 2 (B/P), 3 (P/B), 6 (B/P) |
| 8 Bond (finance) | 12 | 10/1/1 | 9/3/0 | 8 (P/B), 11b (B/P) |
| 9 Alexa | 13 | 8/3/2 | 8/4/1 | 3 (B/P) |
| Total | 94 | 76/13/5 | 70/21/3 | |

Against v0.4.0:
- Better: #7 11b F to B. #8 11b F to B. #9 13 F to B.
- Worse: #3 check 2 P to B. #4 11b B to F. #5 check 5 P to B, 11b P to B. #7 check 2 P to B, check 3 P to B. #8 check 8 P to B.
- Pass to Fail: none.

## Gate judgement of the five v0.4.1 edits (after the fact)

I would approve all five again. All five hit their targets, and none caused the regressions. Two of them left a gap.

- Edit 1 (named parts of a foundation): worked. Both bond pieces give face value, coupon and maturity a paragraph each. 8b passes 11b, which no finance sample had done before. 8a is B on "These regular payments are called coupons, and this bond's coupon rate is 5 percent" (a term and its derived rate). Kafka 2a is down from three terms to two: "Kafka runs on a cluster of servers, and each of those servers is called a broker." Over-correction check: no choppy one-sentence openings. The bond pieces grew, though: 8a from about 1,770 to 1,937, and 8b from about 1,840 to 2,022. That growth is not from the splits. It went into Later-tier passages (8b's twice-a-year paragraph, the portfolio paragraph and the 30-year comparison; 8a's basis-point and fund paragraphs, and "It is worth being clear about what the years mean"). Edit 2 below addresses this.
- Edit 2 (commands and diagram boxes count): worked. Neither Alexa sample lists the guessed layers ("It stacks layers from the app and website at the top down to cart and checkout actions at the bottom"). 7b has moved "tag" out of the Dockerfile paragraph, leaving two terms (Dockerfile and `docker build`, B). A side effect: 9b uses Part C's own word bare, "the touchpoints", which is a check 1 B.
- Edit 3 (exclusivity scan in the check): worked on 9a ("it leaves out a component Amazon has confirmed: the model router"), and "only in auto-buy" is gone. In 9b a quantifier that is not on the scan list gets through: "the router, which is one of the few internal parts Amazon has confirmed." I pass it, because the source does say the internals are unconfirmed, but it shows that a word list invites near-misses. The rule now gives a reason, which fixes the design-rule breach I noted last time.
- Edit 4 (headings and groupings are joins): partly worked. 9b's "The whole picture" now lists the parts separately, and its body says "Separately from your orders, it keeps what Amazon calls account memory." Two joins remain in the body. In 9a: "Account memory is what lets it answer the first half of the grinder question. Among the things Amazon says it can do is check compatibility against your past orders". The source gives these as two separate facts. In 9b, a bridge question sets up RAG as the answer to how price and order facts reach the model: "It has never seen today's price of your cover or the details of your order from last year, so how does its answer end up grounded in those facts?" Check 13 is now B in both samples, down from F.
- Edit 5 (one admission, title terms first): worked. There is one admission, and Rust is explained in the first body paragraph. The cron-notation passage survives for the fourth run and now brings in Unix and cron as well, which makes 11b a Fail. Edit 3 below addresses this. Design rule: "Do not repeat it in the body" is the only new negative instruction. It is harmless next to its reason, but "Say it only there" would be the positive form.

Design rules overall: the seven-section shape and the calm wording are intact. The source paragraph is now about 520 words in one block and still fails the colleague test on length. Split it when patterns/explain.md is split out (unchanged advice).

## Evidence, input by input

### Input 1, API key (585)

Passes every applicable check for the second run in a row. Each term has its own paragraph (API, API key, header). The trap comes where it arises ("An API key identifies a project, not a person"). "Some providers do issue keys designed to sit in public web pages" is a one-sentence variant, which the write section allows. 585 is under 600 but over the 450 typical. Watch this, but it is not scored.

### Input 2, Kafka (2a 1,938; 2b 1,784)

2b 11b, Fail. "The work of deciding who gets which partition is run by one broker acting as the group coordinator ... In the classic version of the protocol one member, the group leader, computes the assignment ...; newer Kafka versions, from 4.0, can let the coordinator compute it directly." That paragraph introduces the coordinator, the group protocol and the group leader. The paragraph itself then says "Either way, the outcome is the same", so it also fails the body test. Its topic paragraph has three as well: "named streams called topics ... A topic is a log ... a retention limit".
2a 11b, Borderline: cluster with broker, consumer group with group ID ("That team is called a consumer group, and the name it shares is called the group ID."), and group coordinator with heartbeat.
Check 1, B in both: "By default the standard client commits automatically every few seconds" (2a) and "the classic version of the protocol" (2b). Neither says that consumers are built on a client library or that the group runs a protocol.
2b check 5, B: the classic-versus-4.0 assignment passage, a second version paragraph ("Rebalances also have a cost. In the classic protocol ..."), and the five-second auto-commit default. 2a check 5 passes, with only one version sentence.
Accuracy: both crash-replay examples agree with their own convention that the commit points at the next record (2a: committed 1,200, processed up to 1,250, replays 1,200 to 1,249; 2b: replays 1,200 to 1,206). The 45-second session timeout and KIP-848 as generally available in 4.0 are correct. Note for 2b: "This matters for everything that follows, because many readers can read the same records" points ahead, but it gives its content in the same sentence, so I pass it.

### Input 3, Raft (~3,100)

Check 2, Borderline (new): "That shared server is what carries knowledge of one decision into the next, and much of Raft's safety rests on it." The second clause promises an argument that arrives three chapters later, which is the same kind as the logged "it is also where its limits come from". The check's phrase list did not catch it, because it does not mention "next" or "later".
Check 5, Borderline, as in both v0.4.0 samples: the history sentence ("published in 2014 by two researchers at Stanford University. Its stated aim was ...") and "If a client contacts a follower by mistake, the follower tells it which server is the leader."
11b, Borderline: consensus with Raft, and candidate with RequestVote.
Election terms, checked: A leads term 3, B wins term 4 with C and D, the split vote is C against D in term 4, then term 5. All correct. Index and term arithmetic in the consistency check (E ends at 5 from term 2, and B probes 7, 6, 5) is correct. The vote comparison (E 5/term 2 against C 8/term 4) is correct.
Running-example notes, not verdicts (see "How I applied the checks"). (1) Chapter 3 brings E up to date ("B sends entries 6, 7 and 8 in turn. E's log now matches B's."), but chapter 4 says "E, whose log ends at index 5" without saying that B crashed before the catch-up. (2) Chapter 4 says "Then B crashes", and four paragraphs later the partition case says "B, still leader in term 4". It is introduced as "a different failure" but never says which moment it starts from. Both are pauses for an attentive reader, the kind the grader test found in v0.3.1. Edit 4 addresses them.
The current-term commit rule is absent from the body and from "Going further". "A change is committed once a quorum holds it" in "The whole picture" matches the paper's definition (entries the leader created in its own term), so I pass check 3. A "Going further" line for it would help.

### Input 4, Driftwood (508)

Check 12, Pass: "I have no reliable knowledge of a tool called Driftwood and will not describe it". There is one admission, and nothing is attributed to the tool. Rust now comes first ("Rust is a programming language.").
11b, Fail: "Timetables are often written in a compact format called a cron expression, borrowed from the long-standing Unix tool named cron." That is three names (the cron expression, the cron tool and Unix), and the piece never uses the last two again. If cron and the cron expression counted as one name, this would be B. The fix is the same either way.
Check 1, B: "Unix" is bare in that sentence.
Check 5, B, for the fourth run: the cron-notation passage ("'0 2 * * *' means minute 0 of hour 2 ...") in a simple piece. The closing question "What timetable format does it accept" already covers it.

### Input 5, the cloud (1,764)

Check 5, Borderline (new): "A second, smaller trap sits next to the first. The cloud is not automatically cheaper. ..." Step 8 asks for one trap, and this paragraph could be deleted without leaving a gap.
11b, Borderline (new): "A company that runs huge data centres ... is called a cloud provider. Amazon Web Services, part of Amazon, is the largest". That is two terms, and AWS is never used again, so the existing "drop any name the piece never uses again" applies.
Everything else passes. The figure "twenty machines for four hours costs roughly what one machine costs for three or four days" checks out (80 machine-hours is about 3.3 days). The trap (shared responsibility) comes where it arises.

### Input 6, Dadhichi design doc as long source (2,038, n=1, no earlier version)

The piece compresses about 3,300 words to 2,038 and leaves out the research table, the source list, the full engine prompt, the storage tree and the version table. "Going further" takes versioning, Claude Projects, examples and automated grading. I checked every fact against the doc. The kernel rules, the precedence order, the engine's four steps and four returns, the five required stresses, the promotion rule, the failure-log fields, `verified_on` and "a released version is never edited" are all correct. "Five kinds of part" counts the kernel as a part, as the doc's own Part table does.
Check 13, B: "The silent planning step matters most." The doc credits the plan step with stopping over- and under-explaining, but it never ranks it first. The piece also states the writer's view as fact in "it is a guess that happened to work once". "The whole picture" marks its one inference correctly ("is my interpretation of how the design's sections connect"), and nothing about the doc's origin is invented (the November 2026 date comes from the doc's header).
Check 1, B: "the design follows Anthropic's guidance", where Anthropic is never introduced. The "Going further" line for "Claude Project" does not say what a Claude Project is.
Check 11a, B: "The whole picture" names the engine's assembly as a mechanism step, but the engine section never runs the running example through it. "You hand it a rough request, and it works in four steps" stays abstract, where "explain Raft for my commute" would become "explain / commuter / it".
Check 5, B: the Git paragraph ("The files themselves sit in Git ...") and the human-check paragraph are Later-tier. The piece is 540 words over the 1,500 typical and spends that room on them.
11b, B: "Dadhichi ... a library of tested, reusable prompts, plus an engine", and rubric with Anthropic.
Note: "What follows is a design document from November 2026 rather than a finished system" has the wrong referent. The article is not the design document; it describes one.

### Input 7, Docker (7a 1,524; 7b ~1,580; reader knows Linux processes)

Check 4, Pass in both. Both are under inputs.md's 1,700, and each is a little over the prompt's own 1,500.
7b check 3, Borderline (new self-contradiction): the Dockerfile reads "start from a published image ..., copy in the service's code, install the driver, and run this command", but the next paragraph says "The Python base is one layer, the installed driver another, your code a third ... a code change rebuilds only the top layer." With the code copied before the driver is installed, a code change rebuilds the driver layer too. This is the same kind of slip the grader test found in v0.3.1 Docker.
7a check 2, Borderline (new): "Each of these maps onto a Linux kernel feature you may already have met." This promises a mapping that the next two sections deliver.
7a check 6, Borderline, as in v0.4.0 7a: "The fix for 'it works on my machine' is to ship the machine's files along with the program." The phrase appears only in the heading, and the Python 3.12 against 3.8 clash is not restated.
Check 5, B in both. 7a: "On a Mac or Windows laptop, Docker Desktop quietly runs a small Linux virtual machine". 7b: the same Docker Desktop paragraph, plus the root-equivalence aside about the daemon.
11b, B in both: 7a has Docker with container, and cgroup with the out-of-memory killer. 7b has Dockerfile with `docker build`, dockerd with the daemon, and cgroups with the OOM killer.
The user-namespace watch item has improved. 7a: "a container gets a fresh one of most of them". 7b: "a fresh set of namespaces". Both list user namespaces in "Going further".

### Input 8, bond duration, finance 0.1.1 (8a 1,937; 8b 2,022)

I checked every figure. 8a (five-year 5 percent par bond): present values 47.62, 45.35, 43.19, 41.14 and 822.70, which sum to 1,000. Macaulay duration 4.55, modified 4.33, exact prices 957.88 and 1,044.52, and 25 basis points is about $11. 8b (five-year 4 percent par bond): present values sum to 1,000, Macaulay 4.63 (the five parts sum correctly), modified 4.45, estimate 955.50 against an exact 956.71, the 3 percent case 1,045.80, a zero-coupon modified duration of 4.81, and about 17 for a 30-year bond. All correct.
8b check 8, Borderline (new): "Price and yield move in opposite directions, like two ends of a seesaw". The simile does not say where it stops, and a seesaw suggests the symmetric, straight-line movement that the convexity section later refutes.
11b: 8b, Pass (the first finance Pass). 8a, B ("coupons, and this bond's coupon rate").
Check 5, B in both. 8a: the drift paragraph again, the basis-point paragraph, and "It is worth being clear about what the years mean", which restates the trap. 8b: "The division by 1.04 assumes the bond pays once a year. For bonds that pay twice a year ...", the portfolio-duration paragraph, and the drift paragraph.
8b note: "It sits on the oldest map in finance" copies the domain block's "sit on one of three maps" to the reader and adds an unsupported superlative. 8b also has "45 cents" in a piece that otherwise gives amounts without a currency.

### Input 9, Alexa for Shopping (9a 1,794; 9b ~1,850)

| | v0.4.0 9a / 9b | v0.4.1 9a | v0.4.1 9b |
| --- | --- | --- | --- |
| M1 invented provenance | fixed / fixed | fixed | fixed |
| M3 join called confirmed | fixed / recurs (structural, F) | recurs in the body ("Account memory is what lets it ...") | WP fixed; one bridge question in the body |
| M4 exclusivity | recurs / recurs | fixed | softened ("one of the few internal parts") |
| M5 absence where silent | fixed / fixed | fixed | fixed ("The sources behind this article do not cover ...") |
| 20 percent applied to one purchase | recurs / - | recurs | fixed |

11b, Fail in both, on the same paragraph. 9a: "it was folded into Alexa+, which is Amazon's generative-AI version of its Alexa voice assistant. Generative AI here means software that composes new replies ... with Alexa+ and with Echo devices". 9b: "folded into Alexa+, Amazon's generative-AI version of its Alexa assistant, meaning a version built on AI that writes new replies ... Echo devices, Amazon's smart speakers". In v0.4.0, generative-AI was an adjective and the paragraph had two names (B). The new definition, which the model added to help check 1, makes three.
Check 13, B in both (quoted in the gate judgement under edit 4). 9a also files catalog, reviews and community answers under RAG ("the fetched material would be the kind Amazon says it uses: listings from the product catalog, customer reviews, community answers"). The pack lists those as inputs to the custom model, and for RAG it names only "relevant material" and the publications.
9a check 3, B: "Amazon says auto-buy customers save an average of 20 percent per purchase; on a 129-dollar grinder that would be about 26 dollars." This applies an average to one purchase, and it disagrees with the piece's own example, where auto-buy at the $99 target saves $30.
Check 1, B in both. 9a: "Prompt caching and parallel tool calling: Bedrock features Amazon says it uses", which still does not say what either one is, and "fine-tuned". 9b: "the touchpoints" (the bare Part C term).
Check 5, B in both: the stand-alone statistics paragraphs and the customer-service paragraph. 9b also has a second-misconception paragraph: "That link to Echo invites a wrong assumption ... You need neither."
Checks 2, 6, 8, 9, 10 and 11a pass in both.

## Readiness for `tested`

Not tested. These cells block it:
1. Fails, of which the full set must have none: 2b 11b, 4 11b, 9a 11b and 9b 11b. All four have the same cause (edit 1).
2. Roadmap step 1's exit (inputs 1 to 3 pass checks 1 to 5): input 2 check 1 is B (2a and 2b), input 2 check 5 is B (2b), input 3 check 2 is B, and input 3 check 5 is B.
3. Coverage: inputs 1, 3, 4, 5 and 6 ran at n=1. A one-shot claim needs n=2 on every input, run 6 included.
4. The human check (a phone read of 1 and 2) has still not been done.

Input 6 now runs from an in-repo source, so the waiver I proposed last time is no longer needed. Its first run has no Fail.

No `status` or `verified_on` change. Keep `status: draft`, keep v0.4.0 as the released version, and add to the v0.4.1 header comment: "0.4.1 graded 2026-11-18, not promoted: 70/21/3 vs 0.4.0's 76/13/5 on 94 shared cells; no Pass-to-Fail; Fails 5 to 3".

## Recommended edits for v0.4.2, in order of importance

Build from v0.4.1 and keep all its edits. All five are refinements of existing rules with the same output shape, so this is a patch.

Edit 1. A gloss that needs a name is a new term (check section). Targets: 11b on 2b, 4, 9a and 9b, which are all the remaining Fails.

Replace:
> Where a paragraph names more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again.

With:
> Where a paragraph names more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again. Count the words that explain a term as well: if the explanation brings in another name, such as the product a feature was folded into, a device it also runs on, the tool a format is named after, or a role in an older version, that name is a new term too. Explain the term in words the reader already has, or give the second name its own paragraph if the piece uses it again, because a gloss that needs its own gloss is the same pause twice.

Watch: 9's continuity point (a conversation started on a speaker carries on in the app) should survive, with Echo in its own paragraph, as in v0.4.0 9a.

Edit 2. Second traps, variants and usage figures leave the body (plan step 5). Targets: check 5 on 5, 7a, 8b and 9b, plus the 170 to 180 words the bond pieces gained.

Replace:
> A refinement of a step, an option, or a second case of a point already made does not.

With:
> A refinement of a step, an option, or a second case of a point already made does not. Nor does a second misconception after the one from step 8, a variant for another platform, payment schedule, or version, or a usage figure the mechanism does not need, because each is a passage the reader must hold that the goal never asks for; give it one line in "Going further" or leave it out. Limits of the mechanism itself, such as where an estimate stops being accurate or which failures a design cannot survive, are part of how it works and stay in the body.

Watch: Raft's "one more limit" (failures by lying) and the bond pieces' convexity section must stay. Cloud should lose "A second, smaller trap", Docker the Docker Desktop paragraph, and 8b the twice-a-year paragraph.

Edit 3. No notation in the unknown-tool piece (plan step 1). Targets: check 5 (four runs) and 11b on input 4.

Replace:
> Then write a simple-size piece on the kind of thing it is said to be, attribute no feature, design, or vocabulary to the named tool, and close with three or four questions the reader can take to its documentation.

With:
> Then write a simple-size piece on the kind of thing it is said to be: the problem it solves, what it does, and the common misconception, each told once in the running example. Leave notations, file formats, and the history of names to the closing questions, because at this size each one is vocabulary the reader cannot use until they have the tool's documentation. Attribute no feature, design, or vocabulary to the named tool, and close with three or four questions the reader can take to its documentation.

Edit 4. The running example keeps its state (check section). Targets: check 3 on 7b and 9a, and the Raft notes.

Replace:
> The running example is used consistently and its numbers agree with each other.

With:
> The running example is used consistently and its numbers agree with each other. After each event that changes its state, such as a crash, a catch-up, a rebuild, or a purchase, every later sentence uses the new state, and a "suppose instead" case says which earlier moment it starts from. Check each figure you derive against the example's own numbers, and apply an average only as an average, because the reader can check your example only against itself.

Watch: 7b's Dockerfile order against its layer list, and Raft's "E, whose log ends at index 5" after the catch-up.

Edit 5. Promises, not just phrases about "next" (check section). Targets: check 2 on 3 and 7a.

Replace:
> Look at every clause that mentions what comes next, such as "which matters a little further on", "which is what the next idea handles", "that detail matters shortly", or "it is also where its limits come from", and end the sentence before it, because each one hands the reader a missing piece to carry.

With:
> Look at every clause that promises something the reader does not yet have, such as a reason, a consequence, or a link to a feature explained later ("which matters a little further on", "much of its safety rests on it", "each of these maps onto a feature you may already have met"), and either give the content in that same sentence or end the sentence before the promise, because each one hands the reader a missing piece to carry.

The exception sentence after it (the single closing question) stays unchanged.

Not proposed: the scope-word list in edit 3 of v0.4.1 ("one of the few" got past it). It is a Pass today. Revisit only if a false limit comes back. The input 6 Borderlines (Anthropic bare, the engine section without the running example) are n=1. See whether they recur at n=2 before writing a rule.

## Failure log

Updates to existing lines:
- Line 32 (named parts of a foundation): mostly fixed in 0.4.1. 8b passes 11b, 8a is B ("coupons, and this bond's coupon rate"), and 2a is down to cluster with broker (B).
- Line 33 (commands and diagram boxes): fixed in 0.4.1. There is no layer list in 9a or 9b, and 7b has two terms (B). Side effect: 9b uses Part C's "touchpoints" bare (check 1 B).
- Line 34 (M4 exclusivity): fixed in 0.4.1 for 9a. 9b softened it to "one of the few internal parts Amazon has confirmed" (passed, watch). "Only in auto-buy" is gone.
- Line 35 (structural join): partly fixed in 0.4.1. 9b's whole-picture paragraph is clean, and 13 went from F to B. Remaining: 9a "Account memory is what lets it answer the first half of the grinder question", and 9b's bridge question that sets up RAG to explain price and order facts.
- Line 36 (Driftwood): fixed in 0.4.1 for the double admission and for Rust. The cron passage recurs; see the new line.
- Line 37 (user namespaces): improved in 0.4.1. 7a says "most of them", and both samples list user namespaces in "Going further". Keep it as a watch item.
- Line 27, second half (the 20 percent average applied to one purchase): recurs in 0.4.1 9a, where it now also contradicts the example's own $99 target. Covered by the new state line.

Lines to add:
- 2026-11-18 | 2b, 4, 9a, 9b | 11b Unhurried | A term's explanation brings in further names: "folded into Alexa+ ... Generative AI here means ... Echo devices"; "a cron expression, borrowed from the long-standing Unix tool named cron"; "group coordinator ... In the classic version of the protocol one member, the group leader" | pending (0.4.2 edit 1)
- 2026-11-18 | 5, 7a, 8a, 8b, 9b | 5 Padding | Second misconceptions, platform or schedule variants, and usage figures stay in the body: "A second, smaller trap sits next to the first"; Docker Desktop on Mac and Windows; "For bonds that pay twice a year"; "That link to Echo invites a wrong assumption". The bond pieces grew by about 170 to 180 words | pending (0.4.2 edit 2)
- 2026-11-18 | 4 | 5 Padding, 11b Unhurried, 1 No lookups | The cron-notation passage recurs for the fourth run and now adds Unix and cron | pending (0.4.2 edit 3)
- 2026-11-18 | 3, 7b, 9a | 3 Accurate (7b, 9a), note (3) | The running example loses its state. 7b's Dockerfile copies the code before installing the driver, then says "a code change rebuilds only the top layer". 9a applies the 20 percent average to a $129 grinder against its own $99 target. Raft says "E, whose log ends at index 5" after E was caught up, and "B, still leader in term 4" after "Then B crashes" | pending (0.4.2 edit 4)
- 2026-11-18 | 3, 7a | 2 Linear | Promise clauses that the phrase list does not catch: "much of Raft's safety rests on it"; "Each of these maps onto a Linux kernel feature you may already have met" | pending (0.4.2 edit 5)
- 2026-11-18 | 5 | 11b Unhurried | "Amazon Web Services, part of Amazon, is the largest" is a name used once, already covered by "drop any name the piece never uses again", which the model did not apply | watch
- 2026-11-18 | 8b | 8 Not dumbed down; domain leak | "like two ends of a seesaw" with no limit stated; "It sits on the oldest map in finance" copies the finance block's "maps" wording to the reader | watch
- 2026-11-18 | 6 (first run) | 13, 1, 11a, 5 | "The silent planning step matters most." is not in the source; Anthropic is bare; the engine section has no running example; the Git and human-check paragraphs are Later-tier; "What follows is a design document" has the wrong referent | watch until n=2

## Before the next decision

- Run v0.4.2 at n=2 on every input, 1 to 9, including 6 with the design doc as its source.
- If a shell is available, run `wc -w` on 3, 7b and 9b and record the results.
- Do the human check on 1 and 2 once.

Process note: this session had Read, Grep, Glob and Write only, with no shell. Nothing outside this file was changed.

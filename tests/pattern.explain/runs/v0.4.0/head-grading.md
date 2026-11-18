# Head grading: built/explain.commuter.it.md v0.4.0 (plus input 8 under finance 0.1.1)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the models that wrote the outputs, but its verdicts may not line up exactly with earlier head files.

Date: 2026-11-18. Stage: grading after the test run, plus a gate-review judgement of the five v0.4.0 edits after the fact.
Read: the design doc, rubric.md, inputs.md, failures.md, the frozen v0.4.0 prompt and the v0.4.0 finance prompt (domain block finance.md 0.1.1), my v0.3.0 and v0.3.1 gradings, the source pack `sources/alexa-for-shopping.md`, all 13 v0.4.0 samples (1, 2a, 2b, 3a, 3b, 4, 5, 7a, 7b, 8a, 8b, 9a, 9b), and the v0.3.0 and v0.3.1 Docker outputs where I needed to check a point again.
Not run: input 6 (the RFC cannot be fetched here).

Word counts: this session had no shell, so `wc -w` was not available. I counted 1 and 7b sentence by sentence and the rest paragraph by paragraph. Allow about 5 percent either way. Only 7b is close enough to a line for that to matter (see input 7).

## Decision: PROMOTE v0.4.0 over v0.3.0. Status: NOT TESTED (stays draft)

How I combine two samples: each cell takes the worse verdict of the two samples, and I list where they split. I apply the same rule to every older input with more than one sample, which means v0.3.0 input 1 (1a, 1b, 1c) and v0.3.1 input 9 (9a, 9b). This changes the older totals from what I reported before, when I counted the weakest whole sample. The new figures are below and they replace the old ones for comparison.

| Shared set, 94 cells | P / B / F |
| --- | --- |
| v0.3.0 (released) | 69 / 17 / 8 |
| v0.3.1 | 70 / 18 / 6 |
| v0.4.0 | 76 / 13 / 5 |

v0.4.0 passes 7 more cells than v0.3.0. No cell goes from Pass in v0.3.0 to Fail in v0.4.0, in either sample of any input. All five v0.4.0 Fails are on cells that v0.3.0 also failed (11b on 2, 7, 8 and 9, and 13 on 9). Both halves of the design's rule are met, so v0.4.0 is promoted. The result does not depend on the combining rule. The combined figure is already the worst case, and every single v0.4.0 sample is free of Pass-to-Fail moves.

v0.4.0 also beats v0.3.1 (76 against 70), so the tie from last time is settled.

Not ready for `tested`. Six of 13 samples still have a Fail: 11b on 2a, 7b, 8a, 8b and 9a, and 13 on 9b. The owner's goal is a prompt that works in one shot, so a Fail in nearly half the samples is not one-shot reliability. Roadmap step 1's exit condition is also not met, because 2b and 3a/3b are Borderline on check 5 (and 2b on check 1). See "Readiness for tested" below.

Single most important fix next: 11b, in one specific form. Three of the five 11b Fails (2a, 8a, 8b) come from one sentence or paragraph that defines the parts of a foundation together: "The yearly interest is called the coupon, the original sum is the face value, and the end date is the maturity." The new plan rule says one foundation per paragraph. The model counts "a bond" as the foundation and its coupon, face value and maturity as attributes of it, not as foundations. It did this in both finance samples and in the last two finance runs. Edit 1 names this case.

## How I applied the checks

- The counting rules are unchanged from the last two gradings. For 11b, two new terms that are not a defined pair is Borderline, three or more is Fail, and a term plus a defined pair is Borderline. Product, project and company names count. Personal names given as attribution (Ongaro, Macaulay) do not, and neither do familiar consumer names given as examples (Alexa, Prime, The New York Times). As in the v0.3.1 grading, I count "cluster" in "a cluster of servers" as a term. Command names (`docker build`) count, as "Docker Hub" and "tag" counted last time.
- Check 4 for input 7: the rubric's ceiling is 2,200 and inputs.md sets 1,700. Over 1,700 is Borderline. Since v0.4.0, the prompt's own ceiling for this input is the typical 1,500 (edit 3). I note when a sample goes past that, but I do not score it, so the versions stay comparable.
- Not applicable: checks 6 and 11a on the simple pieces (1 and 4).
- One rule I changed, applied to all versions alike. 7b says "Docker gives each container a fresh one of each kind" of namespace, which is wrong for the user namespace by default, and its own "Going further" says root in the container is host root. v0.3.1 ("its own view of user IDs") and v0.3.0 ("a few more, for the hostname, users") make the same claim, and I passed both. To keep the comparison fair, I record it as an accuracy note in all three, not as a verdict. The builder should know it is wrong in every version so far.

## Score table, v0.4.0, every sample

P = Pass, B = Borderline, F = Fail, - = not applicable. Words are approximate.

| # | Check | 1 (~560) | 2a (~1,900) | 2b (~1,600) | 3a (~3,000) | 3b (~3,400) | 4 (~580) | 5 (~1,870) | 7a (~1,460) | 7b (~1,690) | 8a (~1,770) | 8b (~1,840) | 9a (~1,930) | 9b (~1,840) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P | P | B | P | P | B | P | P | P | P | P | B | B |
| 2 | Linear | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 3 | Accurate | P | P | P | P | P | P | P | P | P | P | P | B | B |
| 4 | Proportional | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 5 | No padding | P | P | B | B | B | B | P | P | B | B | B | B | B |
| 6 | Resumable | - | P | P | P | P | - | P | B | P | P | P | P | P |
| 7 | Plain text | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | P | P | P | P | P | P | P | P |
| 11a | Complete | - | P | P | P | P | - | P | P | P | P | P | P | P |
| 11b | Unhurried | P | F | B | B | B | B | P | B | F | F | F | F | B |
| 12 | Unknown topic | - | - | - | - | - | P | - | - | - | - | - | - | - |
| 13 | Source confidence | - | - | - | - | - | - | - | - | - | - | - | B | F |
| | P / B / F | 10/0/0 | 11/0/1 | 9/3/0 | 10/2/0 | 10/2/0 | 8/3/0 | 12/0/0 | 10/2/0 | 10/1/1 | 10/1/1 | 10/1/1 | 8/4/1 | 8/4/1 |

All 155 sample cells: 126 Pass, 23 Borderline, 6 Fail.

## Comparison on shared cells (worse verdict per cell)

| Input | Cells | v0.3.0 | v0.3.1 | v0.4.0 | v0.4.0 splits |
| --- | --- | --- | --- | --- | --- |
| 1 API key | 10 | 7/3/0 (n=3) | 8/2/0 | 10/0/0 | n=1 |
| 2 Kafka | 12 | 9/2/1 | 9/2/1 | 9/2/1 | check 1 (P/B), 5 (P/B), 11b (F/B) |
| 3 Raft | 12 | 9/2/1 | 9/3/0 | 10/2/0 | none |
| 4 Driftwood | 11 | 8/2/1 | 8/2/1 | 8/3/0 | n=1 |
| 5 Cloud | 12 | 11/1/0 | 11/1/0 | 12/0/0 | n=1 |
| 7 Docker | 12 | 9/2/1 | 9/2/1 | 9/2/1 | check 5 (P/B), 6 (B/P), 11b (B/F) |
| 8 Bond (finance) | 12 | 10/1/1 | 9/2/1 | 10/1/1 | none |
| 9 Alexa | 13 | 6/4/3 | 7/4/2 (n=2) | 8/3/2 | 11b (F/B), 13 (B/F) |
| Total | 94 | 69/17/8 | 70/18/6 | 76/13/5 | |

Against v0.3.0:
- Better: #1 check 1 B to P, 8 B to P, 11b B to P. #2 check 6 B to P. #3 check 1 B to P, 11b F to B. #4 check 10 B to P, 11b F to B. #5 11b B to P. #7 check 2 B to P. #9 check 1 F to B, 6 B to P, 10 B to P.
- Worse: #2 check 1 P to B (2b). #4 check 5 P to B. #7 check 5 P to B (7b).
- Pass to Fail: none.

Against v0.3.1:
- Better: #1 checks 8 and 11b. #2 check 2. #3 check 2. #4 11b F to B. #5 11b. #7 check 4 B to P. #8 check 2. #9 check 8.
- Worse: #2 check 1 (2b). #7 check 6 (7a).

## Gate judgement of the five v0.4.0 edits (after the fact)

I would have approved all five, and four of them worked. Edit 4 did not, and its failure was predictable from its wording.

- Edit 1 (foundations one per paragraph, plan step 4): mostly worked. Cloud went to 11b Pass, with every term in its own paragraph. Driftwood went from F to B (scheduler, queue, workers, retry and cron each have a paragraph). Docker's namespace list is split into one paragraph per kind in both samples. Alexa's three models are in separate paragraphs in both samples, and 9b is the first input 9 sample ever to reach 11b B. Raft is B in both. It missed three things. One is the parts or properties of a single foundation defined together: "The yearly interest is called the coupon, the original sum is the face value, and the end date is the maturity." (8a), "The yearly 50-dollar payments are called coupons. The 1,000 returned at the end is called the face value, and the date it comes back is the maturity." (8b), and "a cluster of servers ... Each server in that cluster is called a broker" (2a). The second is a build paragraph with Dockerfile, `docker build` and tag (7b). The third is the list of guessed layers (9a). Over-correction check: no length growth (Kafka 1,600 to 1,900, Docker 1,460 to 1,690, Raft 3,000 to 3,400, all in range). Alexa has a few one-sentence paragraphs ("The second is Nova, a family of models Amazon makes itself."). They read as a list set out in prose, but not as choppy. Watch this.
- Edit 2 (forward-pointing clauses listed in the check): worked. Check 2 passes on all 13 samples. None of the four quoted phrases appears in any output, so the risk of copying them did not happen.
- Edit 3 (a reader note makes the typical figure the ceiling): partly worked. Both Docker samples dropped the practical tips (SIGTERM, 0.0.0.0, fork) and the "second trap". 7a is about 1,460, under the 1,500 the prompt now sets. 7b is about 1,690, over the prompt's 1,500 and at the inputs.md line. Its spare words went into a "What happens when you run it" section that repeats steps already explained ("It stacks the layers, adds a fresh writable layer, and mounts the result with the overlay filesystem.") and into the Docker Desktop sentence.
- Edit 4 (scope words; joins in the body): the absence half worked. Both samples use "not covered by the sources behind this article" correctly, and 9b's "Amazon has not published" is gone. The scope half failed in both samples, word for word: "It also leaves out the one internal component Amazon has confirmed: the router." (9a), and the same in 9b. That is four runs in a row. 9a also brings back the original v0.2.1 M4 kind: "the assistant completes a purchase on its own only in auto-buy", followed one paragraph later by Buy for Me, which buys on the user's behalf. The join half caught "which is how" sentences but not joins made by structure. 9b files account memory and price history under a section called "Fetching before answering" ("Fetched material covers prices as well."), and its whole-picture paragraph says "Amazon confirms its main parts: ... retrieval that grounds answers in the catalog, reviews, outside publications and your own orders and account memory". On the design rules: the scope sentence ("Keep the source's own scope words too: a part it calls confirmed is not "the one" confirmed part.") is the only v0.4.0 instruction without a reason. It is also abstract, and it sits in a source paragraph that now runs to about 470 words in one block. The edits that worked (2 and 5) are concrete and live in the check section or next to a concrete example. Edit 3 below moves this rule there.
- Edit 5 (the reader as "you", no named person): worked. No sample of 13 has a named person, and check 8 passes everywhere.

Design rules overall: the seven-section shape is intact and the wording is calm. One rule outside the edits needs attention: the source paragraph fails the colleague test on length alone. When the pattern file is split out, break it into three short paragraphs (what to build from, how to mark confidence, what not to add).

## Evidence, input by input

### Input 1, API key (~560 words)

Pass on every applicable check, which is the first full pass for input 1 across all versions and samples except v0.3.0 1c. It has continuous prose, one exchange, the trap where it arises ("An API key identifies a program or a project, not a person"), and three "Going further" lines. The example uses "you" ("Say you are building a small travel app"). Each term has its own paragraph: API, then API key, then HTTPS, then rotating the key. The previous "header" pairing is gone.

### Input 2, Kafka (2a ~1,900, 2b ~1,600)

2a 11b, Fail. "Those messages are stored in Kafka, a system that keeps streams of messages on a cluster of servers so that other programs can read them. Each server in that cluster is called a broker." That is three terms (Kafka, cluster, broker), down from five in v0.3.1, with the consumer now in its own paragraph and the producer dropped. "Kafka groups messages by subject into a named stream called a topic ... A topic is a log" and "group coordinator ... heartbeat" are two each.
2b 11b, Borderline. Kafka, topic and consumer each have their own paragraph. The worst is "Those units are partitions ... If a message carries a key, such as the customer's ID", which is two terms.

2b check 1, Borderline. "By default, the standard Java client commits automatically every five seconds" and "depends on your Kafka and client versions". The client library is never introduced as a thing that exists, and Java appears bare.
2b check 5, Borderline. There are two sentences of version history in the body ("In the long-standing version of this process, every member pauses ... Kafka 4.0 made a newer protocol generally available ..."), and the same protocol again in "Going further" (KIP-848). There is also the auto-commit default, which is a configuration detail that the body test sends to "Going further".
2a check 5, Pass. The version difference is one sentence, as the write section allows ("In older setups the whole group pauses; newer versions and settings narrow the pause to only the partitions that move.").

Accuracy: both samples get the crash-replay arithmetic right (2a: 1,041 to 1,060 is twenty orders; 2b: 1,205 to 1,230 is 26). Both state the commit-before-processing loss correctly, which fixes v0.3.1's slip. 2b's 45-second session timeout is the current default. Check 6 passes in both.

### Input 3, Raft (3a ~3,000, 3b ~3,400)

Check 2, Pass in both (v0.3.1 B). There is no "which matters a little further on" or anything like it.
Check 5, Borderline in both. 3a keeps the history sentence, "It was published in 2014 by Diego Ongaro and John Ousterhout at Stanford University", and adds Later-tier sharding ("Large databases that use Raft generally split their data into many small pieces"). 3b has a read-safety passage that "Going further" repeats: "The split also shows a quieter danger, which concerns reads rather than writes ..." against "Linearizable reads: ...".
11b, Borderline in both. 3a: "C raises its term to 4 and declares itself a candidate ... This message is called RequestVote", and cluster plus the majority-and-quorum pair. 3b: "That list is called the log ... that number is called the index", and leader and followers plus clients.

3a now teaches the current-term commit rule in full as its trap, using the shop's servers. I checked the sequence (C writes 9 in term 4; E wins term 5 with A and D; C wins term 6; E could win term 7 by last-term comparison; committing entry 10 in term 6 closes it) and it is correct. In earlier runs this rule was pushed off as "worth reading about at a desk". 3b puts it in "Going further" and treats the split network as its trap, which is also sound.
Running-example notes, not verdicts. 3a has E's log stop "at index 5" in chapter 3, but the chapter 4 hypothetical has E "offline ... so it holds only entries up to 7". 3b says "A, B and D all end at index 12, term 8" at a moment when A would still hold its stale term-7 entry. Neither changes the argument, but each is a pause for an attentive reader.

### Input 4, Driftwood (~580 words)

Check 12, Pass. "I have no reliable knowledge of a tool called Driftwood." Nothing is attributed to the tool.
11b, Borderline (up from F). Edit 1 worked here. Scheduler and job share a paragraph, but queue, workers, retry and cron each have their own.
Check 1, Borderline, for the third run. "Rust" is in the title and the first two lines and is explained only in the second-to-last body paragraph ("Rust is a programming language that compiles to fast machine code"). "Separate processes called workers": "processes" is bare.
Check 5, Borderline, for the second run. The body opens by repeating the admission made in the line above ("I cannot recall concrete facts about a Rust job scheduler named Driftwood that I would stand behind, so nothing below describes it."), which also copies the prompt's "that you would stand behind". The cron notation passage ("'0 2 * * *' means minute 0, hour 2, every day") is still there. The cause of the double admission is plan step 1 ("say so in plain words in the first two sentences") together with the output rule that puts the same statement under the title. The model does both (edit 5).

### Input 5, the cloud (~1,870 words)

Pass on every check. This is the best sample in the run. Each new term has its own paragraph (server, cloud provider, data centre, virtualization, hypervisor, VM, API, autoscaling, elasticity, load balancer, pay-as-you-go, IaaS, PaaS, SaaS, shared responsibility, bucket). The flats analogy says where it stops ("The comparison stops at size and speed."), and the cost figures check out (2 VMs × 8,760 h × $0.10 ≈ $1,750; 48 extra × 4 h × $0.10 ≈ $20). Note: "What the joke leaves out is how you get hold of that computer." sits just before the section's closing question and works as a second pull forward. That is harmless here.

### Input 7, Docker (7a ~1,460, 7b ~1,690; reader knows Linux processes)

Check 4, Pass in both (v0.3.1 B). 7b is at the inputs.md line within counting error, and over the prompt's own 1,500. If `wc -w` puts it over 1,700, that cell becomes B. That would not change the decision.
7a check 6, Borderline. "With the problem in hand, start with the files." names the problem without restating it. A reader resuming here is reminded of orders-api's needs in the next sentence, but not of the clash with the server's Python 3.8, which is the problem. 7b's "The problem, then, is shared ground." is short but restates, so it passes.
7b check 5, Borderline. "It is also why a Linux container needs a Linux kernel: Docker Desktop on macOS and Windows gets one by running a small Linux virtual machine" is a platform variant that 7a correctly put in "Going further". The run section's steps 2 and 3 repeat the layer and cgroup explanations from the two sections before.
7b 11b, Fail. "You describe an image in a text file called a Dockerfile ... The `docker build` command follows the instructions and produces the image, which you tag with a name and version". That is Dockerfile, the build command, and tag. If commands are not counted this is B, which does not change the decision. 7a 11b, Borderline: "a short text file called a Dockerfile ... each slice is called a layer".
Accuracy notes, not verdicts (all versions): "Each of those instructions produces one slice of filesystem changes" next to the start command, which makes no layer. 7a: "A virtual machine runs its own kernel on emulated hardware" ("virtualised", as 7b says, is more accurate). 7b: "Docker gives each container a fresh one of each kind" (no user namespace by default; see "How I applied the checks").

### Input 8, bond duration, finance 0.1.1 (8a ~1,770, 8b ~1,840)

I checked every figure. 8a: 10-year 5 percent par bond, 926.40 at 6 percent, 1,081.11 at 4 percent, Macaulay 8.11, modified 7.72, estimate 922.80. 8b: 5-year 5 percent par bond, present values 48/45/43/41/823, Macaulay 4.55, modified 4.33, exact 957.88 and 1,044.52. Both name the trap (duration is not maturity), use the zero-coupon exception, and state the parallel-shift and fixed-payment assumptions. 8b's plank analogy says where it stops ("The picture holds for the arithmetic only"). It no longer has v0.3.1's forward pointer, so check 2 passes. Domain 0.1.1's "Advice" paragraph is now a field fact, which fixes the domain-side breach logged last time.

11b, Fail in both, as in every finance run: "The yearly interest is called the coupon, the original sum is the face value, and the end date is the maturity." (8a), and "The 1,000 returned at the end is called the face value, and the date it comes back is the maturity." after "called coupons" (8b). 8a's next paragraph but one has present value and yield together as well.
Check 5, Borderline in both, the same passage as last run. 8a: "Duration also shifts as the yield changes ... not a fixed label printed on it." 8b: "And the number itself drifts: as time passes ..." (also said earlier: "a higher market yield would shorten it too"), and the "rising bond market" aside.
Note for 8a: the duration (8.11 years) and the true gain at 4 percent (8.11 percent) are the same number by coincidence. A reader may think they are linked. Picking a different example bond would remove that.

The pattern still generalises: input 8 scores 10/1/1, among the best in the set. Its one Fail is the same opening cast-list failure as Kafka's.

### Input 9, Alexa for Shopping (9a ~1,930, 9b ~1,840)

| | v0.3.1 9a / 9b | v0.4.0 9a | v0.4.0 9b |
| --- | --- | --- | --- |
| M1 invented provenance | fixed / fixed | fixed ("which the sources behind this article include and explicitly label as not Amazon's design") | fixed |
| M3 join called confirmed | fixed in WP / recurs in body | fixed ("is my reading of how they fit") | recurs structurally, in body and WP |
| M4 exclusivity | recurs / recurs | recurs, plus "only in auto-buy" | recurs |
| M5 absence where silent | half / recurs | fixed | fixed ("not covered by the sources behind this article") |
| Named person | 9a Priya / - | fixed ("you") | fixed |

Check 13. 9a, Borderline: "Bedrock hosts models from several makers, which is how a model from outside Amazon ends up inside an Amazon product." is a "which is how" join on a fact the pack does not give, stated plainly. "In the mechanisms Amazon describes, the assistant completes a purchase on its own only in auto-buy" credits Amazon with a limit Amazon does not state. Everything else is carefully marked ("would plausibly include", "that reasoning is general practice, not something the sources behind this article state"). 9b, Fail: "Amazon confirms its main parts: ... retrieval that grounds answers in the catalog, reviews, outside publications and your own orders and account memory". The pack lists RAG, compatibility checks against past orders, and account memory as separate facts. Joining them under "Amazon confirms" states the writer's reading at the source's highest confidence. The body has the same join: the section "Fetching before answering" holds account memory, and "Fetched material covers prices as well." The next WP sentence's "my reading" covers only the order of steps, not this grouping.
Check 3, Borderline in both: "It also leaves out the one internal component Amazon has confirmed" (both), and 9a's "only in auto-buy", which its own next paragraph contradicts ("Through a feature called Buy for Me, it can buy items from other brands' websites on your behalf").
Check 1, Borderline in both. 9a: "touchpoints, a gateway layer, language and voice processing, a model core, data services, and a commerce layer", and "Prompt caching and parallel tool calling", whose "Going further" line still does not say what either is. 9b: "a specific gateway layout" is bare. Its "Going further" defines both Bedrock features.
11b. 9a is Fail on the guessed-layer list quoted above, which is six layer names in one sentence. Its Rufus and Alexa+ paragraph and its Claude Sonnet and Anthropic paragraph have two each. 9b is Borderline. Rufus has a paragraph to itself, and the worst paragraphs are Alexa+ with Echo, Claude Sonnet with Anthropic, and COSMO with knowledge graph, two each.
Check 5, Borderline in both: the stand-alone statistics ("Amazon reports the scale ..." in 9a, and the 250 million line in 9b's introduction), and the customer-service paragraph. 9b also adds advice: "If you meet a diagram like it, the router is the quickest test".
Checks 6, 8, 9, 10 and 11a pass in both.

## Readiness for `tested`

Not ready. What `tested` needs, in my judgement:
1. No Fail in any sample of a full n=2 run of inputs 1 to 5 and 7 to 9. Today there are six Fails in 13 samples. Borderlines are acceptable, because the design's promotion rule treats only Fail as blocking.
2. Roadmap step 1's exit: inputs 1, 2 and 3 pass checks 1 to 5 in both samples. Today 2b is B on 1 and 5, and 3a and 3b are B on 5.
3. `verified_on` recorded with the model that wrote the v0.4.0 outputs and the date. The frozen header still says "not yet verified (0.3.0 and 0.3.1 outputs ...)". Record the writing model, not the grading model.
4. The human check on 1 and 2, done at least once on a phone. No grading so far has done it.

Input 6 can be waived. The design's five required stresses (trivial, hard, outside knowledge, vague, second domain) are inputs 1, 3, 4, 5 and 8, and all have run. The long source is not one of them. Record the waiver in the entry in these words: "input 6 (RFC 9111, long dense source) not run: source unavailable in the test environment; compression of long sources is untested". Better still, run a long source that is in the repo, for example `Dadhichi Master Prompt Library System Design.md` with TOPIC "how a Dadhichi prompt is promoted". That tests compression without a fetch. If the builder does that, the waiver is not needed.

## Recommended edits for v0.4.1, in order of importance

Build from v0.4.0 and keep all five of its edits.

Edit 1. The parts of a foundation are foundations too (plan step 4). This targets 11b on 2a, 8a and 8b.

Replace:
> Name only the one the next sentence needs and let the others arrive in their own paragraphs, because a paragraph that hands over four names is where a reader on a bus loses the thread.

With:
> Name only the one the next sentence needs and let the others arrive in their own paragraphs, because a paragraph that hands over four names is where a reader on a bus loses the thread. The named parts or properties of a foundation count as foundations of their own: when a thing has a payment, a sum and a date that each carry a name, or a system runs on machines that have a name of their own, give each name its own paragraph at the point the running example first uses it. A sentence of the form "this is called A, that is B, and the other is C" hands over three terms at once and is the most common place this rule breaks.

Watch: one-sentence paragraphs in the bond opening, and the bond pieces growing by 100 or more words.

Edit 2. Commands and diagram parts count as terms (check section). This targets 11b on 7b and 9a, and check 1 on 9a and 9b.

Replace:
> No paragraph hands the reader more than one new term, and the names of products, projects, and companies count as terms.

With:
> No paragraph hands the reader more than one new term, and the names of products, projects, companies, commands, and the boxes or layers of a diagram count as terms.

Edit 3. Exclusivity claims checked where checks work (check section). This targets check 3 on 9a and 9b (four runs) and part of 13 on 9a. It replaces edit 4's unreasoned scope sentence with a concrete scan.

Replace (source paragraph):
> Keep the source's own scope words too: a part it calls confirmed is not "the one" confirmed part.

With:
> Keep the source's own scope words too, because the reader takes "only" and "the one" as facts they cannot check.

And replace (check section):
> If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture".

With:
> If a source was given, every statement about the topic can be traced to it at the confidence the source gives it, and anything you added or inferred is worded as general practice or as inference, in the body and in "The whole picture". Then find every sentence that says "only", "the one", "the single" or "nothing but" about the topic, and keep the limit only if the source states it in those terms. Otherwise name the part without the limit, because such a claim becomes false as soon as a second case exists, and often your own draft names that case a few paragraphs later.

Watch: the router sentence should become something like "It also leaves out the router, which Amazon has confirmed."

Edit 4. Headings and groupings are joins too (source paragraph). This targets 13 on 9b.

Replace:
> A sentence that joins two confirmed facts, such as "which is how..." or "so that...", is your reading in the body just as in "The whole picture", because the reader cannot tell your join from the source's.

With:
> A sentence that joins two confirmed facts, such as "which is how..." or "so that...", is your reading in the body just as in "The whole picture", because the reader cannot tell your join from the source's. A heading or a list that puts two parts under one mechanism joins them in the same way: when the source gives two features separately, keep them separate, or say once that grouping them is your reading, and keep any grouping of your own out of a sentence that begins "the source confirms" or "the company confirms".

Edit 5. One admission, and the title's terms explained first (plan step 1). This targets check 5 (two runs) and check 1 (three runs) on input 4.

Replace:
> say so in plain words in the first two sentences: you have no reliable knowledge of this tool and will not describe it.

With:
> say so once, in plain words, in the line under the title as the output section describes: you have no reliable knowledge of this tool and will not describe it. Do not repeat it in the body, because the reader has just read it. If the topic name contains another term the reader may not know, such as the language or platform the tool is said to be built on, explain that term in the first body paragraph, because the reader has already met it in the title.

Not proposed: the check 5 Borderlines on 2b, 3, 7b, 8 and 9 (version, history, refinement and statistics passages). They are the most common non-Pass, but they are not blocking. A broad rule such as "anything that has a 'Going further' line leaves the body" would cut convexity from the bond pieces, where it belongs. Revisit once the Fails are gone. Versioning: edits 1 to 5 refine existing rules without changing the output shape, so this is a patch (0.4.1).

## Failure log

Updates to existing lines:
- Line 24 (11b, plan step 4): partly fixed in 0.4.0. 5 is now Pass, 4 went from F to B, 3 is B in both samples, the Docker namespaces and Alexa models are split, and 9b is B. Still failing: 2a, 7b, 8a, 8b and 9a. Superseded by the two new 11b lines.
- Line 25 (forward-pointing clauses): fixed in 0.4.0. Check 2 passes in 13 of 13 samples, and none of the quoted phrases is copied.
- Line 26 (Docker length): mostly fixed in 0.4.0. 7a is about 1,460 and 7b about 1,690, and the practical tips are gone from both. 7b's surplus went into a run section that repeats the layer and cgroup steps, and into the Docker Desktop sentence (check 5 B).
- Line 27 (M4 exclusivity): not fixed in 0.4.0. It appears word for word in 9a and 9b (four runs), and 9a adds "only in auto-buy". See the new line.
- Line 28 (9b join, absence claim): the absence half is fixed in 0.4.0 (both samples). The join half recurs in 9b as a structural join. See the new line.
- Line 29 (named person): fixed in 0.4.0 (0 of 13).
- Line 30 (watch, Driftwood padding): recurs in 0.4.0. Promote it to a failure line (below).
- Line 31 (IT wording in the pattern): unchanged and still to do at the split. The domain-side "Advice" paragraph was fixed in finance.md 0.1.1.

Lines to add:
- 2026-11-18 | 2a, 8a, 8b | 11b Unhurried | The one-foundation-per-paragraph rule is read as applying to "the bond" or "Kafka", not to their named parts. The parts are defined together: "The yearly interest is called the coupon, the original sum is the face value, and the end date is the maturity."; "a cluster of servers. Each server in that cluster is called a broker" | pending (0.4.1 edit 1)
- 2026-11-18 | 7b, 9a | 11b Unhurried | Command names and diagram layers are not counted as terms: "a Dockerfile ... The `docker build` command ... which you tag"; "touchpoints, a gateway layer, language and voice processing, a model core, data services, and a commerce layer" | pending (0.4.1 edit 2)
- 2026-11-18 | 9 (9a, 9b) | 3 Accurate | The abstract scope-words rule (0.4.0, no reason given) did not reach the model. "the one internal component Amazon has confirmed" persists word for word, and 9a adds "completes a purchase on its own only in auto-buy", which Buy for Me contradicts one paragraph later | pending (0.4.1 edit 3)
- 2026-11-18 | 9 (9b) | 13 Source confidence | A join made by structure, not by a "which is how" sentence: account memory and price history are filed under "Fetching before answering", and the whole-picture paragraph says "Amazon confirms ... retrieval that grounds answers in ... your own orders and account memory" | pending (0.4.1 edit 4)
- 2026-11-18 | 4 | 1 No lookups, 5 Padding | Plan step 1 says to admit "in the first two sentences" and the output section says to admit under the title, so the model admits twice. "Rust" appears in the title and is explained only near the end (three runs) | pending (0.4.1 edit 5)
- 2026-11-18 | 7 (all versions) | 3 Accurate (note) | "Docker gives each container a fresh one of each kind" (0.4.0 7b), "its own view of user IDs" (0.3.1), "for the hostname, users" (0.3.0). User namespaces are off by default. Passed in every grading so far, so the comparison stays fair | watch

## Before the next decision

- Run v0.4.1 at n=2 on inputs 1 to 5 and 7 to 9, plus input 6 or its in-repo substitute.
- Run `wc -w` on 7b if a shell is available, and record it.
- Update `verified_on` for v0.4.0 now that it is promoted. Record the writing model and the date 2026-11-18.

Process note: this session had Read, Grep, Glob and Write only, with no shell. Word counts are by hand, as stated at the top. Nothing outside this file was changed.

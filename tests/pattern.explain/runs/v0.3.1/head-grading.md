# Head grading: built/explain.commuter.it.md v0.3.1 (plus input 8 under v0.3.0 and v0.3.1)

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head is still independent of the builder and of the models that wrote the outputs, but its verdicts may not line up exactly with earlier head files.

Date: 2026-11-18. Stage: grading after the test run, plus a gate-review judgement of the five v0.3.1 edits after the fact (no gate review was run before testing).
Read: the design doc, rubric.md, inputs.md, failures.md, the frozen v0.3.1 prompt, my v0.3.0 grading, every v0.3.1 output (1, 2, 3, 4, 5, 7, 9a, 9b), each v0.3.0 counterpart, the source pack `sources/alexa-for-shopping.md`, both finance prompts and both input 8 outputs.
Not run: input 6 (the RFC cannot be fetched here). Input 9 has n=2 in v0.3.1. Every other input has n=1.

Word counts: this session had no shell, so `wc -w` was not available. I counted by hand: sentence by sentence for 1 and 7, which are near their limits, and paragraph by paragraph for the rest. Allow about 5 percent either way. Only input 7 is close enough to a line for that to matter, and it is over that line either way.

## Decision: NOT PROMOTED (v0.3.0 stays current; status stays draft)

This run includes input 8, which both versions have now run, so the shared set has 94 cells. On those cells v0.3.0 has 70 Pass, 16 Borderline and 8 Fail. v0.3.1 has 70 Pass, 19 Borderline and 5 Fail. As in the v0.3.0 grading, that counts the weakest new sample for the repeated input, here 9a. No cell goes from Pass to Fail. But the design promotes only when the new version passes more checks, and a tie is not more. So v0.3.1 is not promoted.

This is a close call, and the builder should read it that way:
- v0.3.1 is not worse. It has three fewer Fails, and each of the five edits fixed what it was aimed at (see the gate judgement below).
- What offset the gains is mostly new or recurring Borderlines that the edits did not cause. These are forward-pointing clauses in three inputs (2, 3, 8), length creep in Docker, and a named person in the running example (1, 9a).
- Counted with 9b instead of 9a, v0.3.1 has 71 Pass and would be promoted. The margin is inside the noise of one sample per input.

Recommendation: keep v0.3.0 as the released version, but build v0.3.2 from the v0.3.1 text, keeping all five of its edits. Run v0.3.2 at n=2 on inputs 2, 3, 7, 8 and 9 so the next decision is not settled by a single Borderline.

Not ready for `status: tested`, input 6 aside. 11b (Unhurried) still fails on 5 of 8 inputs (2, 4, 7, 8, 9), and 13 (Source confidence) still fails on one of the two input 9 samples.

Single most important fix next: 11b. It is the only check that fails across the set, and three edits that touched only the self-check have not fixed it. The v0.3.1 edit worked only where the extra names were Later-tier material (Raft's history paragraph). It did nothing where the names are foundations, which is the opening "cast list" paragraph in Kafka and in both bond pieces, or confirmed facts that come in groups (Alexa's model list, Docker's namespaces). Those decisions are made in the plan, so the fix goes in the plan (edit 1).

## How I applied the checks

- The counting rules are unchanged from the v0.3.0 grading, so the versions stay comparable. For 11b, two new terms that are not a defined pair is Borderline, and three or more is Fail. Product, project and company names count as terms. Personal names given only as attribution (Ongaro, Ousterhout, Macaulay) do not count, and neither do publication names offered as familiar examples.
- Check 4 for input 7: the rubric's ceiling is 2,200, and inputs.md sets 1,700 for this input. Meeting the first and missing the second is Borderline.
- Not applicable: checks 6 and 11a for the simple pieces (inputs 1 and 4).
- Repeated input: input 9 counts its weakest sample by Pass count (9a). Both samples were checked for Pass to Fail moves.
- I scored input 8 under v0.3.0 here for the first time. It joins the shared set because both versions ran it on the same domain pack (finance.md 0.1.0).

## Score table, v0.3.1

P = Pass, B = Borderline, F = Fail, - = not applicable.

| # | Check | 1 API key (~586) | 2 Kafka (~1,830) | 3 Raft (~3,580) | 4 Driftwood (~520) | 5 Cloud (~1,870) | 7 Docker (~1,940) | 8 Bond (~1,950) | 9a Alexa (~1,820) | 9b Alexa (~1,950) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | P | P | P | B | P | P | P | B | B |
| 2 | Linear | P | B | B | P | P | P | B | P | P |
| 3 | Accurate | P | P | P | P | P | P | P | B | B |
| 4 | Proportional | P | P | P | P | P | B | P | P | P |
| 5 | No padding | P | B | B | B | P | B | B | B | B |
| 6 | Resumable | - | P | P | - | P | P | P | P | P |
| 7 | Plain text | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | B | P | P | P | P | P | P | B | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | P | P | P | P |
| 11a | Complete | - | P | P | - | P | P | P | P | P |
| 11b | Unhurried | B | F | B | F | B | F | F | F | F |
| 12 | Unknown topic | - | - | - | P | - | - | - | - | - |
| 13 | Source confidence | - | - | - | - | - | - | - | B | F |
| | P / B / F | 8 / 2 / 0 | 9 / 2 / 1 | 9 / 3 / 0 | 8 / 2 / 1 | 11 / 1 / 0 | 9 / 2 / 1 | 9 / 2 / 1 | 7 / 5 / 1 | 8 / 3 / 2 |

Input 8 under v0.3.0 (~1,900 words): P on everything except check 5 B and 11b F, so 10 / 1 / 1.

## Comparison with v0.3.0 on shared cells

| Input | Cells | v0.3.0 P / B / F | v0.3.1 P / B / F |
| --- | --- | --- | --- |
| 1 API key (v0.3.0 = 1a) | 10 | 8 / 2 / 0 | 8 / 2 / 0 |
| 2 Kafka | 12 | 9 / 2 / 1 | 9 / 2 / 1 |
| 3 Raft | 12 | 9 / 2 / 1 | 9 / 3 / 0 |
| 4 Driftwood | 11 | 8 / 2 / 1 | 8 / 2 / 1 |
| 5 Cloud | 12 | 11 / 1 / 0 | 11 / 1 / 0 |
| 7 Docker | 12 | 9 / 2 / 1 | 9 / 2 / 1 |
| 8 Bond (finance) | 12 | 10 / 1 / 1 | 9 / 2 / 1 |
| 9 Alexa (v0.3.1 = 9a) | 13 | 6 / 4 / 3 | 7 / 5 / 1 |
| Total | 94 | 70 / 16 / 8 | 70 / 19 / 5 |

Without input 8 (the 82 cells of the last comparison): v0.3.0 has 60 / 15 / 7 and v0.3.1 has 61 / 17 / 4.

Better: #1 check 1 B to P; #2 check 6 B to P; #3 check 1 B to P, 11b F to B; #4 check 10 B to P; #7 check 2 B to P, check 6 B to P; #9a check 1 F to B, check 6 B to P, check 10 B to P, check 13 F to B. (9b has the same moves except check 13, which stays F.)
Worse: #1 check 8 P to B; #2 check 2 P to B; #3 check 2 P to B; #4 check 5 P to B; #7 check 4 P to B, check 5 P to B; #8 check 2 P to B; #9a check 8 P to B.
Pass to Fail: none, in either input 9 sample.

## Gate judgement of the v0.3.1 edits (after the fact)

I would have approved all five. Each one fixed its target in this run:

- Edit 1 (names count as terms): partly worked. Raft's Paxos, etcd and Kubernetes paragraph is gone (Paxos is now in "Going further"), and Raft moves from F to B on 11b and from B to P on check 1. It did not reach foundation vocabulary, confirmed name groups, or kinds of one thing. The over-correction I warned about, cutting Alexa's model list, did not happen. Instead the model spread the three models over three sentences of one paragraph, which still fails the count. No choppy one-sentence paragraphs appeared.
- Edit 2 (provenance bounded, no "material you were given"): worked. "Circulates online" is gone from both 9 samples, and the leak is gone from inputs 4 and 9. "The sources behind this article" reads naturally. Driftwood mentions no source.
- Edit 3 (unconfirmed parts kept short): mostly worked. Kinesis is gone, and the diagram gets one sentence of layers in 9a. Check 1 moves from F to B. What is left is a few bare words in the guess list (below).
- Edit 4 (confirmed means stated, in "The whole picture"): worked in both samples. 9a: "The order in which these pieces run for a given question is my reading of how such assistants usually work". 9b: "is my reading of how they fit together". The same kind of error moved into the body in 9b (below), which this edit did not cover.
- Edit 5 (the second section restates): worked everywhere. Check 6 passes on every sectioned output (2, 3, 5, 7, 8, 9a, 9b). The restatements are short, and none doubles as a chapter-end summary.

On the design rules, the edits carry their reasons and are calmly worded. Edit 4 states its rule without saying why, though the reason follows from the paragraph above it. The seven-section shape is intact.

What a gate review would have missed: the forward-pointer clauses in inputs 2, 3 and 8. No edit points towards them, and the Docker pointer that was logged last time is gone, so I read this as sampling noise in a rule the model applies loosely, not as damage from an edit. It costs three cells all the same.

## Evidence, input by input

### Input 1, API key (~586 words)

Right-sized and simple-shaped. It has one running example (a forecast app), the trap (a key shipped inside a phone app can be extracted), and four "Going further" lines. Check 4 passes at about 586 against 600. As in v0.3.0 1a, the four-line "Going further" (about 70 words) is what brings it near the limit.

Check 8, Borderline (1a was P). "Say Priya is building a small app that shows tomorrow's forecast", followed by "Priya's account", "Priya's limit and her bill". This is a named person carried through the piece, the same finding as 1b last run, and it shows up again in 9a. Three samples across two runs is a pattern now (edit 5).
11b, Borderline. "That string is an API key. Her app attaches it to every request, usually in a header (a labelled line of extra information...)". That is two terms that are not a pair. The first paragraph has API plus the request and response pair, which I count as a term plus a pair.
Check 1, Pass (1a was B). The bare "tokens" from 1a is gone. Check 3: the revoke-then-rotate order error from 1b is gone. Rotation is now a "Going further" line.

### Input 2, Kafka (~1,830 words, down from ~2,000)

Check 6, Pass (up from B). The second section opens with "The shop has a topic called `orders` and wants many readers on it." Edit 5 worked.

Check 2, Borderline (down from P). "Partitions are the unit Kafka hands out ... That rule is what makes the next part work, and it is also where its limits come from. So how does Kafka decide...". The closing question is allowed. The sentence before it promises an explanation of "its limits" that is still to come, which is the worry the write section describes. Last run's "Before seeing how it does it, two more pieces..." only announced order, and I passed it. This one hands the reader an open question to carry.

11b, Fail. This is worse than v0.3.0 in the worst paragraph: "The shop sends these messages through Apache Kafka. Kafka is a system that stores streams of messages on a cluster of servers ... The servers that make up the cluster are called brokers. Programs that write messages are called producers, and programs that read them are called consumers." That is Kafka, cluster and broker, plus a pair. This is the opening "cast list" that edit 1 does not reach, because the plan calls these foundations and lets them share "a short passage". The committing-offset paragraph and the coordinator-and-heartbeat paragraph each have two terms.

Check 5, Borderline (unchanged). The version passage survives: "In the original design, every member of the group stopped reading during a rebalance ... Newer versions of Kafka reduce this", and it is repeated in "Going further" under "Cooperative rebalancing" and "The new consumer group protocol".

Accuracy note, not a verdict: "Committing before processing ... messages handled after the commit and before the crash are lost". The messages at risk are the ones committed but not yet handled, so "handled" should be "not yet handled". The timeout range (10 to 45 seconds) and the KIP-848 and Kafka 4.0 line are correct. Check 1: "Unlike a traditional message queue" is a bare term, but the mailbox contrast in the same paragraph carries it, so it passes.

### Input 3, Raft (~3,580 words, up from ~3,200)

11b, Borderline (up from F). The Paxos, etcd and Kubernetes paragraph is gone. The worst paragraphs now have two terms that are not a pair: "This ordered, append-only list is called the log. Each position in it has a number, called its index", and "Cedar now becomes a candidate ... This message is called RequestVote". The history sentence keeps two author names and a university ("published in 2014 by Diego Ongaro and John Ousterhout at Stanford"). I do not count them as terms, as stated above, but they fail the body test.
Check 1, Pass (up from B). Kubernetes and the early use of "cluster" are gone.

Check 2, Borderline (down from P). "This message is called RequestVote, and it carries Cedar's new term along with a description of the last entry in Cedar's log, which matters a little further on." This is a textbook forward pointer, placed in the middle of a chapter. "As long as that candidate passes a check on its log", in the next paragraph, is the same move in a milder form.

Check 5, Borderline (unchanged). The history sentence, and the current-term commit paragraph, which defers itself: "The reason involves a specific sequence of crashes worth reading about at a desk".

Accuracy note: in the failure walk-through, "Ash's log stops at index 40, from term 4". Ash was the term-4 leader that created entry 41 (term 4), so Ash would normally hold it. This is possible only if Ash crashed before its own disk write. The reader is not told that and will stop to wonder. This is a running-example consistency issue, so I note it rather than mark it. The split-vote passage is now correct.

The length grew by about 375 words but stays near the typical 3,500. Every step in "The whole picture" is shown with the five tree-named servers.

### Input 4, Driftwood (~520 words)

Check 10, Pass (up from B). The "material I was given" leak is gone, and nothing is addressed to the sender. Check 12, Pass. The line under the title is the admission, and nothing is attributed to the tool ("whether Driftwood works that way is one of the things I cannot tell you").

Check 5, Borderline (down from P). Two passages can go without leaving a gap. One is the cron passage: "schedulers of this kind often write that timetable in cron syntax, a compact five-field notation borrowed from an old Unix tool, where "0 2 * * *" means...". That is notation detail in a simple piece, which the body test sends to "Going further". The other is the second paragraph, which repeats the admission already made in the line above ("I cannot tell you anything specific about Driftwood ... Anything written here under its name would be a guess").

11b, Fail. "A job scheduler is the program that decides ... called a queue ... in cron syntax ... an old Unix tool". That is three terms plus a bare name. Edit 1 did move workers into their own paragraph, but cron arrived in its place.
Check 1, Borderline (unchanged). "Rust" is in the title and the first line and is explained only in the second-to-last body paragraph. "Unix" and "concurrency" are bare.

### Input 5, the cloud (~1,870 words)

The same verdicts as v0.3.0. It has a new running example (a hamper shop going from 200 to 20,000 visitors an hour, and from two VMs to a few dozen) that holds together, and every later section restates.
11b, Borderline. "That company is called a cloud provider ... Each building is a data centre." Two terms, related but not defined against each other.
Note, not a verdict: "That explains where the machines are and how they are shared. The remaining question is..." is a one-sentence end-of-section summary, which the self-check forbids. The flat analogy ("like renting an empty flat") passes check 8 because it is true in the one respect it is used for.

### Input 7, Docker (~1,940 words, up from ~1,500; reader knows Linux processes)

Check 2, Pass (up from B). "That detail matters a great deal shortly" is gone. Check 6, Pass (up from B). "So the goal is to give orders-api its own set of files..." opens the second section.

Check 4, Borderline (down from P). About 1,940 words. That is under the rubric's 2,200 ceiling and about 240 words over the 1,700 that inputs.md sets for this input. The reader note is used for content (processes, signals and the OOM killer are not explained) but not for length. The self-check lets this happen: "If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is". The upper limit there is still 2,200 (edit 3).

Check 5, Borderline (down from P). Practical tips and second pitfalls that fail the body test: "docker stop sends SIGTERM to that process, waits ten seconds by default, then sends SIGKILL", "services in containers need to listen on 0.0.0.0", "programs that fork into the background", "The flip side is the second trap people fall into", and the Docker Hub sentence. Together they are about the 440 words the piece gained.

11b, Fail. "In its PID namespace ... In its mount namespace ... In its network namespace ... Other namespaces give it its own hostname and its own view of user IDs". That is the same paragraph as last run, and it now lists more kinds. Also "a registry, a server that holds images by name and version tag ... Docker Hub is the public registry", which is three terms.

Accuracy note: "Each of those steps produces a layer" sits next to "The last line is metadata". CMD makes no filesystem layer, so the piece contradicts itself slightly.

### Input 8, bond duration, finance domain (v0.3.0 ~1,900 words; v0.3.1 ~1,950 words)

Both pieces are strong, and every number checks out. v0.3.0: 4 percent five-year bond, price 956.71 at 5 percent and 1,045.80 at 3 percent, Macaulay 4.63, modified 4.45. v0.3.1: 5 percent bond, price 957.88 at 6 percent and 1,044.52 at 4 percent, Macaulay 4.55, modified 4.33, DV01 about 43 cents. Both have four or five sections, all restating. Both name the trap (duration is not maturity), use the zero-coupon case as the exception, mark the parallel-shift and fixed-payment assumptions, and put convexity at the end in the running example. v0.3.1 adds a balance-point analogy and states where it stops: "The picture holds for the calculation, but stops at that".

11b, Fail in both, and it is the same failure as in IT. v0.3.0: "A bond is a loan ... a face value of 1,000 dollars ... it matures in five years ... Those yearly payments are called coupons." v0.3.1: "The yearly payment is called the coupon, the 1,000 is the face value, and the date the face value comes back is the maturity." That is three foundations in one sentence. It is the opening cast list again, and it is the strongest evidence that the 11b problem lives in the pattern, not in the IT domain block.

v0.3.1 check 2, Borderline (v0.3.0 P). The analogy's limit line ends with a forward pointer: "it says nothing about what happens to the price, which is what the next idea handles."

Check 5, Borderline in both. v0.3.0 has the hold-to-maturity paragraph ("Duration also gives a way to understand holding a bond to the end..."), which can go without a gap. v0.3.1 has "Duration also changes as the yield changes, and it shortens as time passes", which also can go, and it gives the DV01 figure twice (body and "Going further").

Check 1 note, both: "discount" appears as a verb without being introduced. v0.3.0: "The interest rate used to discount those payments". v0.3.1: "Every payment gets discounted harder". Both can be inferred from the sentence before, so they pass. The domain pack's "Advice" note shows up in v0.3.0 ("duration describes the exposure, it does not make that choice for you"). It reads well, but see the domain note below.

#### Does the pattern generalise?

Yes. With only the <domain> block swapped, the explainer produced an accurate, correctly sized, linear and resumable finance piece under both versions. It scored 10/1/1 and 9/2/1, which puts input 8 among the best inputs in the set. The one Fail is the same 11b failure as on the IT inputs.

IT-specific wording in the pattern sections (outside <domain>). None of it showed up in either bond output, and none caused a measured failure. It still breaks the design rule that "a pattern never names a domain", and it should be removed when `patterns/explain.md` is split out (roadmap step 2):
- Plan step 1: "choose the IT meaning most likely intended". This names the domain outright. It is harmless for "bond duration" but would steer an ambiguous finance term (for example "spread" or "margin") the wrong way. Replace it with "choose the meaning most likely intended in this field".
- Plan step 9's size anchors are all IT: "a port number ... a file extension ... a checksum", "how a domain name is turned into a server address", "how a language model generates text or how two computers set up an encrypted connection". For finance the model has to translate these. It sized bond duration correctly, but a simple finance topic (what an APR is) has no anchor. These anchors belong in the domain pack.
- Plan step 3: "Everyday technology such as apps, browsers, passwords, files, Wi-Fi, and 'the cloud'". This only says what an IT reader already has. A finance reader gets no equivalent (percentages, loans, interest), so whether to explain "a bond is a loan" is left to chance. Both outputs explained it, which was the right call.
- Plan step 1 and output: "a specific named product, library, or tool ... its documentation"; situation: "comfortable with everyday technology", "open the official documentation", "configuration settings, version differences, and optional features".
- Write section: "imagine you are a data packet", "the reader asked to understand a technology", the session-token and HTTP examples, "Use code only when the topic is itself about code", "between versions, vendors, or configurations".
- Check: "named technology", "Every technical claim". Source paragraph: the example "assistants of this kind usually...", which is tuned to one input.
- On the domain side: finance.md's "Advice" paragraph ("describe what the decision depends on rather than making it for the reader") is a writing instruction. The design says a domain pack never gives writing instructions. Restate it as a field fact, for example "explanations of how an instrument works are not advice, and readers in this field are wary of being told what to do", and leave the instruction to the pattern.

### Input 9, Alexa for Shopping (9a ~1,820 words, 9b ~1,950 words)

The status of M1 to M5 and of the 0.3.0 regressions:

| | v0.3.0 | 9a | 9b |
| --- | --- | --- | --- |
| M1 invented provenance | "circulates online" | Fixed: "in the words of the sources behind this article, a guessed architecture diagram produced by another AI assistant" | Fixed: "a guessed architecture diagram produced by another AI assistant" |
| M3 inferred link "confirmed" in The whole picture | Recurred | Fixed: order "is my reading" | Fixed in "The whole picture". Recurs in the body (below) |
| M4 exclusivity | Recurred | Recurs: "the one internal component Amazon has confirmed: the model router" | Recurs: "the one internal component Amazon has confirmed, the real-time router" |
| M5 absence claim where the source is silent | Fixed | Half: "Amazon does not say which model handles which kind of query, so the sources behind this article cannot tell you..." | Recurs: "Amazon has not published which kinds of question go to which model." |
| Part C layer list | Reproduced in full | One sentence | One sentence plus "a specific gateway and event-streaming setup" |
| Reader-facing leak | Yes | Gone | Gone |

Check 13. 9a is Borderline (up from F). Provenance and "The whole picture" are clean, and the absence claim is followed at once by the right "sources behind this article" wording. 9b is Fail (unchanged). It has the absence claim in the M5 form, and an inferred link stated as fact in the body: "It is built from your shopping activity, which is how the assistant can check compatibility against your past orders". The pack gives these as two separate facts. The "which is how" join is the writer's.

Check 3, Borderline in both (unchanged). The M4 exclusivity claim contradicts the confirmed parts listed in the same paragraph. It started from the pack's plain "The diagram also omits the confirmed model router" and has now appeared in three runs. I am moving it from watch to a logged failure. Also in 9a: "Amazon says auto-buy customers save an average of 20 percent per purchase; at $120, that would be about $24". This applies an average to one purchase whose saving the example already fixes (a $95 target). In 9b, "The rest is its own invention" overstates the pack's "guesses".

Check 1, Borderline in both (up from F). 9a: "through a gateway and language-processing front ends ... then data services" are bare, and "Prompt caching and parallel tool calling" is a "Going further" line that does not say what either is. 9b: "a specific gateway and event-streaming setup", "three data services", and "a fine-tuned language model" are bare. 9b's "Going further" defines both Bedrock features well.

11b, Fail in both (unchanged). 9a: "One is Anthropic's Claude Sonnet. Another family is Amazon's own Nova models. The third is a custom model". That is three names, now in three sentences of one paragraph. Also "a shopping chatbot called Rufus ... folded it into Alexa+, the generative-AI version of its Alexa voice assistant". 9b: "Anthropic's Claude Sonnet, Amazon's own family of models called Nova, and a custom model". 9b's naming paragraph is better (Rufus and Alexa+, with Echo moved to the next paragraph).

Check 8: 9a is Borderline. "To follow it through, take one shopper. Priya owns an espresso machine...". 9b uses "you" and passes.

Check 5, Borderline in both (unchanged). The customer-service paragraph and the stand-alone statistics paragraph ("Amazon also gives a number for the whole experience..." in 9a, "Amazon's published figures give a sense of scale" in 9b) can both go without a gap. 9b also keeps the COSMO build method in the body ("Amazon built it by mining what people search for and then buy").

Checks 6 and 10, Pass in both (up from B). Check 9, Pass. Both say "not one AI" where the router comes in. Check 11a, Pass in both. As last run, the cart and customer-service steps are told outside the running example.

## Recommended edits for v0.3.2, in order of importance

Build from the v0.3.1 text and keep its five edits.

Edit 1. Put the one-term rule into the plan, where foundations are decided (plan step 4). This targets 11b on inputs 2, 4, 7, 8 and 9.

Replace:
> Foundation: ideas the core cannot stand without and that several later paragraphs lean on. Each gets a short passage of its own, early, in the order the ideas depend on each other.

With:
> Foundation: ideas the core cannot stand without and that several later paragraphs lean on. Each gets a paragraph of its own, early, in the order the ideas depend on each other, and no two foundations share a paragraph. This matters most in the opening section, where it is tempting to introduce the whole cast at once: the system, its parts, and the people or programs on either side of it. Name only the one the next sentence needs and let the others arrive in their own paragraphs, because a paragraph that hands over four names is where a reader on a bus loses the thread. When the mechanism rests on several kinds or members of one thing, such as several models or several kinds of namespace, give the general idea one paragraph and each member the reader must keep a short paragraph of its own, in the order the running example meets them.

Watch: one-sentence paragraphs that read as choppy, and length growth on 2 and 7. Edit 3 is the counterweight.

Edit 2. List the forward-pointing clauses the model actually writes (check section). This targets check 2 on inputs 2, 3 and 8.

Replace:
> No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come.

With:
> No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come. Look at every clause that mentions what comes next, such as "which matters a little further on", "which is what the next idea handles", "that detail matters shortly", or "it is also where its limits come from", and end the sentence before it, because each one hands the reader a missing piece to carry.

Watch: quoted bad phrases can get copied. If any of these four strings shows up in v0.3.2 output, swap the quoted phrases for a description ("a clause that promises a later explanation").

Edit 3. Make a reader note lower the ceiling, not only the typical figure (check section). This targets check 4 and check 5 on input 7.

Replace:
> If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is.

With:
> If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is. When the notes say the reader already holds part of the ground, the typical figure for the size becomes the upper limit, so practical tips and second pitfalls go to "Going further" instead of into the words the notes freed.

Watch: Docker losing cgroups or the volume step to fit. v0.3.0 covered the full mechanism in about 1,500 words, so it fits.

Edit 4. Keep the source's scope words, and mark joins in the body as well (source paragraph). This targets check 13 on 9b and check 3 on 9a and 9b.

Replace:
> State that something is unknown or unpublished only when the source says so; where the source is merely silent, say that the sources behind this article do not cover it.

With:
> State that something is unknown or unpublished only when the source says so; where the source is merely silent, say that the sources behind this article do not cover it, and do not add "the company has not said" in front of that. Keep the source's own scope words too: a part it calls confirmed is not "the one" confirmed part. A sentence that joins two confirmed facts, such as "which is how..." or "so that...", is your reading in the body just as in "The whole picture", because the reader cannot tell your join from the source's.

Edit 5. Put the reader, not a named person, in the running example (write section). This targets check 8 on 1, 1b (v0.3.0) and 9a.

Replace:
> There are no characters, no invented plot, and no "imagine you are a data packet", because the reader asked to understand a technology, not to be entertained around it.

With:
> There are no characters, no invented plot, and no "imagine you are a data packet", because the reader asked to understand a technology, not to be entertained around it. The running example puts the reader in it as "you", or names a system, a shop, or a company, rather than a person with a name, because a named person reads as the start of a story.

Not proposed for v0.3.2, but to do when the pattern file is split out: the de-IT changes listed under input 8. They have no measured cost yet, and mixing them in would muddy the next comparison. Versioning: edit 1 changes how foundations are planned. Under the design's table that is arguably a minor bump (0.4.0) rather than a patch. That is the builder's call, but record which one it is.

## Failure log

Updates to existing lines:
- Line 16 (11b, names not counted): partly fixed in 0.3.1. Raft went from F to B (the history-paragraph names moved out). Inputs 2, 4, 7 and 9 still fail, and 8 fails in finance as well. Superseded by the new 11b line.
- Line 17 (provenance invented): fixed in 0.3.1 (9a, 9b).
- Line 18 ("material you were given" leak): fixed in 0.3.1 (4, 9a, 9b).
- Line 19 (Part C list reproduced): mostly fixed in 0.3.1. Check 1 went from F to B. The residue ("gateway", "front ends", "event-streaming", "data services") is bare.
- Line 20 ("confirmed" in The whole picture): fixed in 0.3.1 in both samples. The same kind recurs in the 9b body. See the new line.
- Line 21 (second section opens cold): fixed in 0.3.1 (2, 7, 9a, 9b, and also 3, 5, 8).
- Line 22 (watch, exclusivity): recurs in 9a and 9b. Promote it to a failure line (below).
- Line 23 (watch, Docker forward pointer): fixed for input 7 in 0.3.1, but the same kind appeared on inputs 2, 3 and 8. See the new line.

Lines to add:
- 2026-11-18 | 2, 4, 7, 8, 9 | 11b Unhurried | The names rule sits only in the self-check, but the cast is decided in plan step 4, whose foundations get "a short passage" each. The model introduces every foundation in one opening paragraph (Kafka, cluster, broker, producer, consumer; bond, coupon, face value, maturity; scheduler, queue, cron), lists the kinds of one thing in one paragraph (PID, mount, network namespaces), and spreads confirmed name groups over sentences of one paragraph (Claude Sonnet, Nova, custom model) | pending (0.3.2 edit 1)
- 2026-11-18 | 2, 3, 8 | 2 Linear | Forward-pointing clauses that the three banned phrases do not cover: "it is also where its limits come from", "which matters a little further on", "which is what the next idea handles" | pending (0.3.2 edit 2)
- 2026-11-18 | 7 | 4 Proportional (inputs.md 1,700), 5 Padding | About 1,940 words. The notes rule lowers the typical figure, but the self-check's stop rule compares with the 2,200 upper limit, so the freed words went to practical tips (SIGTERM wait, 0.0.0.0, fork, Docker Hub) and a "second trap" | pending (0.3.2 edit 3)
- 2026-11-18 | 9 | 3 Accurate | The pack's "the diagram also omits the confirmed model router" becomes "the one internal component Amazon has confirmed" in v0.3.0, 9a and 9b. 9a also applies the 20 percent average to one purchase | pending (0.3.2 edit 4)
- 2026-11-18 | 9 (9b) | 13 Source confidence | A join between two Part A facts stated as fact in the body ("which is how the assistant can check compatibility against your past orders"), and an absence claim where the pack is silent ("Amazon has not published which kinds of question go to which model") | pending (0.3.2 edit 4)
- 2026-11-18 | 1, 9a (and 1b in 0.3.0) | 8 Not dumbed down | A named person ("Priya") carried through the running example. "No characters" is read as "no plot" | pending (0.3.2 edit 5)
- 2026-11-18 | 4 | 5 Padding | Cron notation passage in a simple piece, and a second paragraph that repeats the admission | watch
- 2026-11-18 | 8 (pattern sections) | design rule: a pattern never names a domain | "choose the IT meaning", IT-only size anchors in step 9, IT "everyday technology" list in step 3, "data packet", "code", "documentation". No measured failure on input 8 | to fix when patterns/explain.md is split out (roadmap step 2)

## Before the next decision

- Run v0.3.2 at n=2 on inputs 2, 3, 7, 8 and 9. This decision came down to one Borderline per input.
- Keep running input 8 with every version. It is now a scored part of the shared set.
- Update `verified_on`. The v0.3.1 header still describes the 0.3.0 outputs. Record the model that wrote the v0.3.1 outputs and the date 2026-11-18, not the grading model.
- Input 6 remains the one design-required input never run. "Tested" needs it, or an explicit waiver recorded in the entry.

Process note: this session had Read, Grep, Glob and Write only, with no shell. Word counts are by hand, as stated at the top. Nothing outside this file was changed.

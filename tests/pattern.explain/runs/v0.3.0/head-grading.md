# Head grading: built/explain.commuter.it.md v0.3.0

Note: this grading ran on Opus (claude-opus-5-5) because the usual head model was out of credits. The head stays independent of the builder and output models, but verdicts may not line up exactly with earlier head files.

Date: 2026-11-18. Stage: grading after the test run.
Read: design doc, rubric.md, inputs.md, failures.md, frozen v0.3.0 prompt, my v0.2.2 gate review, every v0.3.0 output (1a, 1b, 1c, 2, 3, 4, 5, 7, 9), the source pack `sources/alexa-for-shopping.md`, the v0.2.1 outputs and both v0.2.1 gradings.
Not run: inputs 6 (RFC unavailable) and 8 (finance domain block not written). Input 1 has n=3; every other input has n=1.

Word counts: this session had no shell, so I counted by hand, paragraph by paragraph (title and "Going further" included). Treat them as within about 5 percent. None of the limits is close enough for that to change a verdict, except 1a (about 583 of 600), where I counted every sentence.

## Decision: PROMOTE v0.3.0 over v0.2.1 (status stays draft)

On the 82 cells both versions can be scored on, v0.3.0 has 60 Pass, 15 Borderline and 7 Fail. v0.2.1 has 55, 15 and 12. That counts input 1 by its weakest v0.3.0 sample. No cell goes from Pass to Fail, so both halves of the design's rule are met. Every logged 0.3.0 target that was meant to fix a Fail now passes: the API-key size (3 of 3 samples), the Driftwood admission, and Raft completeness.

Promotion is not a clean bill of health, and the builder should not set `status: tested`:
- Six cells drop from Pass to Borderline: 1b check 8, 4 check 10, 7 check 2, 7 check 6, 9 check 6, 9 check 10. Input 9 also drops from Borderline to Fail on check 1. Input 9 passes fewer checks than v0.2.1 did (6 against 7). It is the only input that is worse on balance.
- 11b (Unhurried) still fails on 5 of the 7 inputs, and 13 (Source confidence) fails on input 9.
- Inputs 6 and 8 have never run.

Single most important fix next: 11b. It is the only check failing across the set, it has survived two targeted edits (v0.2.1, v0.3.0), and every failing paragraph is the same kind of thing: a list of names, or a foundation vocabulary set, that the model does not count as "new terms". Edit 1 below changes the approach instead of repeating the rule.

## How I applied the checks

- 11b: I kept the v0.2.1 counting rule so the versions are comparable. If the worst paragraph has two new terms that are not a defined pair, the verdict is Borderline. Three or more is a Fail. Product, project and company names count as terms, as they did in the Alexa grading.
- I regraded v0.2.1 on the split and new checks from the evidence in its gradings, without re-reading the outputs except where marked. 11a and 11b come from the completeness and pace halves of old check 11. Check 12 for v0.2.1 input 4 is a Fail: its opening line promises "what a job scheduler written in Rust does", and the soft admission sits in the next section. Check 13 for v0.2.1 input 9 is a Fail (M1, M2, M3, M5). I kept the old check 3 Fail for v0.2.1 input 9. Even under the narrower meaning, with confidence issues moved to 13, it has M4, S2, S3, S5, S6 and S7.
- Not applicable: check 6 and 11a for simple pieces (inputs 1 and 4 in v0.3.0 have no sections and correctly have no "The whole picture"). These cells are left out of the comparison. So is v0.2.1 input 4 check 6, which was a Fail. That fix shows up as a change of shape, not as a counted cell.
- Borderline is not Fail when I apply the promotion rule. This matches the v0.2.1 grading, which treated only Pass to Fail as a blocker.

## Score table, v0.3.0

P = Pass, B = Borderline, F = Fail, - = not applicable.

| # | Check | 1a (~583) | 1b (~533) | 1c (~528) | 2 Kafka (~2,000) | 3 Raft (~3,200) | 4 Driftwood (~520) | 5 Cloud (~1,840) | 7 Docker (~1,500) | 9 Alexa (~2,000) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | No lookups | B | P | P | P | B | B | P | P | F |
| 2 | Linear | P | P | P | P | P | P | P | B | P |
| 3 | Accurate | P | P | P | P | P | P | P | P | B |
| 4 | Proportional | P | P | P | P | P | P | P | P | P |
| 5 | No padding | P | P | P | B | B | P | P | P | B |
| 6 | Resumable | - | - | - | B | P | - | P | B | B |
| 7 | Plain text | P | P | P | P | P | P | P | P | P |
| 8 | Not dumbed down | P | B | P | P | P | P | P | P | P |
| 9 | Trap handled | P | P | P | P | P | P | P | P | P |
| 10 | Clean output | P | P | P | P | P | B | P | P | B |
| 11a | Complete | - | - | - | P | P | - | P | P | P |
| 11b | Unhurried | B | B | P | F | F | F | B | F | F |
| 12 | Unknown topic | - | - | - | - | - | P | - | - | - |
| 13 | Source confidence | - | - | - | - | - | - | - | - | F |
| | P / B / F | 8 / 2 / 0 | 8 / 2 / 0 | 10 / 0 / 0 | 9 / 2 / 1 | 9 / 2 / 1 | 8 / 2 / 1 | 11 / 1 / 0 | 9 / 2 / 1 | 6 / 4 / 3 |

All v0.3.0 cells: 78 Pass, 17 Borderline, 7 Fail of 102.

## Comparison with v0.2.1 on shared cells

| Input | Cells | v0.2.1 P / B / F | v0.3.0 P / B / F |
| --- | --- | --- | --- |
| 1 API key (v0.3.0 = 1a, weakest sample) | 10 | 6 / 2 / 2 | 8 / 2 / 0 |
| 2 Kafka | 12 | 9 / 1 / 2 | 9 / 2 / 1 |
| 3 Raft | 12 | 8 / 2 / 2 | 9 / 2 / 1 |
| 4 Driftwood | 11 | 6 / 3 / 2 | 8 / 2 / 1 |
| 5 Cloud | 12 | 9 / 3 / 0 | 11 / 1 / 0 |
| 7 Docker | 12 | 10 / 1 / 1 | 9 / 2 / 1 |
| 9 Alexa | 13 | 7 / 3 / 3 | 6 / 4 / 3 |
| Total | 82 | 55 / 15 / 12 | 60 / 15 / 7 |

Better: #1 checks 4 and 5 F to P (all three samples); #2 check 6 F to B; #3 11a F to P; #4 check 3 B to P, check 5 B to P, check 12 F to P; #5 check 6 B to P, check 8 B to P; #7 check 5 B to P; #9 check 2 B to P, check 3 F to B.
Worse: #1b check 8 P to B; #4 check 10 P to B; #7 check 2 P to B, check 6 P to B; #9 check 1 B to F, check 6 P to B, check 10 P to B.
Pass to Fail: none.

Gate-review risks, checked against the run:
- R1, input 7 at most 1,700 words: met (about 1,500, down from 2,144). Edit 3 worked.
- R2, hedging creep on input 9: did not happen. Confidence is stated once per change, and the confirmed parts read as plain statements. Edit 5 worked.
- R3, API key pushed out of simple: did not happen. All three samples are prose, 528 to 583 words, with no "The whole picture".
- R4, cloud pulled down to simple: did not happen. It is moderate with five sections.
- C4, choppy one-sentence paragraphs from the pace rule: not seen.
- Raft did not grow. It went from about 3,920 to about 3,200 and became more complete.

## Evidence, input by input

### Input 1, API key (three samples)

All three samples are right-sized: continuous prose, one running example (a weather service), the mechanism told once, the trap where it arises, and a "Going further" of three or four lines. This is the fix the v0.2.1 grading asked for, confirmed at n=3.

1a, check 1, Borderline. A term is used bare and dropped: "Telling individual users apart is a separate job, usually done with logins and short-lived tokens." Nothing on the page says what a token is.
1a, 11b, Borderline. Two terms that are not a pair share a paragraph: "That string is called an API key. Your app attaches it to every request, usually in a header, a labelled line of extra information".
1a, check 4, Pass at about 583 words, near the limit. About 490 of those are body text, and the four-line "Going further" takes most of the rest.

1b, check 8, Borderline. The running example has a named person who is carried through the piece: "Say Priya is building a small travel app", "Priya might paste the key", "a machine she runs". The prompt says "There are no characters", and this is one, though there is no plot. The membership-card comparison is true in the one respect it is used for, so I do not count it.
1b, 11b, Borderline. "request header" comes in the API-key paragraph, and "revoke" and "rotating the key" share the last paragraph. Note on accuracy, not a verdict: "revoke it ... and issue a new one. This is called rotating the key, and providers usually let you have two keys active for a while so the switch causes no downtime." If you revoke first, there is downtime. The order is backwards.

1c: Pass on every applicable check, and the best of the three. The ticket simile ("much like a ticket that admits whoever carries it") is exactly true in the respect used. "Keys also leak when developers publish their code online" is a one-sentence second leak route. The body test says a second story of the same mistake does not pass, but this is one sentence, not a passage, so I note it and do not mark it down.

### Input 2, Kafka consumer groups (~2,000 words)

Check 5, Borderline. The version-difference passage survives, as in v0.2.1: "In the classic form of the protocol, every member stops reading while partitions are reassigned ... Newer versions of Kafka reduce this so that only the partitions actually moving are paused." It is repeated in "Going further" ("Cooperative rebalancing and the new consumer group protocol"), so deleting it leaves no gap. "the protocol" is also not introduced.

Check 6, Borderline (up from Fail). Of the four sections after the first, three open with a restatement ("You now know that `orders` is six ordered partitions", "The `billing` group now has three members", "You now know that one consumer group splits"). The second section opens cold: "A topic is not one long line." See the pattern note under input 7.

11b, Fail. "Messages about the same subject are kept together in a named stream called a topic. ... A program that writes messages into a topic is a producer ... A program that reads them is a consumer." That is three terms, a pair plus one. The paragraph before it has three as well (Apache Kafka, broker, message). v0.2.1's worst paragraph had four.

Passes worth stating: 11a. Every step in "The whole picture" is in the body with the shop. The duplicate-charge passage (offsets 18,530 to 18,560, thirty-one customers) is internally consistent. Check 2: "Before seeing how it does it, two more pieces of Kafka need to be in place" is a signpost, but nothing depends on what comes later, so it passes. Accuracy note: "about 60 milliseconds per order, roughly the time of a blink". A blink takes 100 to 400 ms, and the prompt's own example says "quicker than a blink". The same slip appeared in v0.2.1 Raft.

### Input 3, Raft (~3,200 words)

Check 1, Borderline. "including etcd, the database that stores the configuration of Kubernetes clusters". Kubernetes is never explained, and "cluster" is used here one paragraph before it is introduced ("a cluster, the usual word for such a group"). This is the same finding as v0.2.1.

Check 5, Borderline. Two passages can go without a gap. The history paragraph ("Raft was published in 2014 by Diego Ongaro and John Ousterhout ... An older algorithm, Paxos ...") is history, which step 5 names as failing the body test, and Paxos is also in "Going further". The current-term commit passage says of itself: "You do not need the details to follow Raft's design". Its claim that the rule "is the part most often gotten wrong in homemade implementations" is also unsupported.

11b, Fail. The history paragraph introduces Paxos, etcd and Kubernetes in three sentences. Every other paragraph has at most two terms or a defined pair (leader and followers, majority and quorum). Moving that one paragraph to "Going further" would fix checks 1, 5 and 11b together.

11a, Pass (up from Fail). Log repair now uses the running example: "That is exactly how S1's stray 'set price to 50' disappears after the network heals: the new leader walks back to the point of agreement". The election restriction is shown with S5. The partition scenario is clearly marked as an alternative ("Go back to term 2 ... and suppose that instead of crashing"), which fixes v0.2.1's unannounced restart.

Accuracy note, not a verdict: in the split vote, "they may split the votes two and two, with the remaining server's vote not enough for either". With S1 down there is no remaining voter. The four live servers are all accounted for.

### Input 4, Driftwood (~520 words)

12, Pass. The line under the title is the admission: "I have no reliable knowledge of a Rust job scheduler called Driftwood, so nothing below describes it". Nothing is attributed to the tool. "the name alone does not tell you which one Driftwood is" stays on the right side. The four questions are the right ones.

Check 10, Borderline. The second paragraph is a meta-paragraph that repeats the admission three times and copies the prompt's reasoning to the reader: "I have no facts about Driftwood that I would stand behind, and the material I was given contains nothing about it. Anything I wrote under its name you would take as true, with no way to check it from where you are sitting." The reader was given no material, and "from where you are sitting" is the prompt's "from a bus seat". The cause is the source paragraph's second-person wording (edit 2).

Check 1, Borderline. "Rust" is used in the first line and explained ten lines later ("Rust is a programming language known for speed").

11b, Fail. "A job scheduler is the program that decides ... hold the jobs that are waiting in a queue, an ordered waiting line, and hand them one by one to workers". That is three terms.

Accuracy and size pass: about 520 words, simple shape, and the general claims are hedged as general ("Schedulers of this kind usually").

### Input 5, the cloud (~1,840 words)

This is the best output in the run. The scope is sensible and it stays moderate, all four later sections open with a restatement, and the running example (a venue going from 2 to 40 VMs for a Friday on-sale) is carried to the end.

11b, Borderline. "Each of those pretend machines is called a virtual machine, often shortened to VM ... This slicing is called virtualisation". These are two related terms. I do not count the provider names (AWS, Azure, Google Cloud) as vocabulary, because they are given as examples a commuter already knows. Edit 1 would make the model treat them as terms.
Note: "That is the whole idea. The rest of this piece is about why it exists and how it works." This announces the article, but it comes after a paragraph of substance, so it is not a preamble.

### Input 7, Docker containers (~1,500 words, reader knows Linux processes)

The reader note is now used for length as well as content. The piece reaches namespaces from "an ordinary Linux process" without explaining processes, and containerd and runc are gone.

Check 2, Borderline (down from Pass). "It contains no kernel. That detail matters a great deal shortly." This is the forward pointer the write section bans, and the kind logged on 2026-11-15. The v0.2.1 grading passed a roadmap sentence in the old Docker piece ("the rest of this piece takes them one at a time"). This one is a promise that something is coming, which is worse.

Check 6, Borderline (down from Pass). "## The image: a frozen copy of the files" opens "Everything a container sees on disk comes from a package called an image." There is no restatement of the problem. The later two sections restate well.

Pattern across inputs 2, 7 and 9: in each, the section right after the problem section is the one that opens cold, and every later section restates. The model treats the problem section as an introduction, not as a section the reader holds. Edit 5 below addresses this.

11b, Fail. "The process ID namespace means ... The network namespace gives it ... The mount namespace keeps ..." introduces namespace plus three named kinds in one paragraph. That is lighter than v0.2.1's six, and each kind comes with the running example, but by the count it is four. Edit 1's "kinds of one thing" clause is aimed at this.

Accuracy note: "Each instruction produces a layer." Only instructions that change files do. This is a common simplification, so I do not mark it.

### Input 9, Alexa for Shopping (~2,000 words, mixed-confidence source)

The main structural behaviour is right. The mechanism comes from Part A. Tools are worded as general practice ("Assistants of this kind usually act through tools"). The confidence drop is said once, in its own place ("The confidence drops from here."). The COSMO link is marked unconfirmed in the pack's own terms. There is no hedging creep.

M1 to M5 from the v0.2.1 Alexa grading:

| | v0.2.1 problem | v0.3.0 | Status |
| --- | --- | --- | --- |
| M1 | Invented provenance ("Diagrams circulating online") | "The second is an architecture diagram that circulates online, which the source you were given describes as produced by another AI assistant, not by Amazon." Also "If you meet that diagram in a meeting" | Recurs. The true provenance is now stated, but "circulates online" is still invented, and "the source you were given" points the reader at material they never saw |
| M2 | "Every piece of that path came from what Amazon has said in public" | "Everything so far, the name change, the models, the router, Bedrock, RAG, account memory, and the actions, comes from Amazon's own announcement and from reporting on it." | Fixed in substance: the list is all Part A, and reporting is credited. The residue is "Everything so far", which also covers the writer's inference that "Retrieval also covers you" |
| M3 | Inferred step called "confirmed" in "The whole picture" | "the assistant retrieves the product details, reviews, price history, and your account memory and hands them to that model so its answer is grounded ... Those steps are confirmed by Amazon." | Recurs in a new form. That account memory and price history arrive through retrieval is the writer's link, not the pack's (S8 last time), and it is now stamped "confirmed". The original actions sentence is fixed |
| M4 | Exclusivity: "Auto-buy is the one place..." | That sentence is gone. New of the same kind: "It also leaves out the one internal component Amazon has confirmed, the model router." It contradicts the same paragraph's own list of confirmed parts (Bedrock, RAG, user memory) | Original fixed; the same class of error recurs |
| M5 | "Amazon has not said which kinds of query go to which model" | "the material given here does not say which model would get it" | Fixed. The wording follows the new rule exactly, though "the material given here" is the same leak as in check 10 |

Should-fix items from last time: S1 (tools), S2 (20 percent misapplied), S3 (annotated), S4 (one tool), S5 (Buy for Me) and S7 (features "such as") are all fixed. S6 is mostly fixed. S8 has moved into M3 above.

Check 13, Fail. M1 is a direct hit on "nothing about the source's origin is invented", and M3 states an inference at higher confidence than the pack gives it.

Check 1, Fail (down from Borderline). The new source paragraph's "Present unconfirmed parts as what the source says they are" was read as "lay them out". The Part C layer list is reproduced: "an API gateway with ingestion and event streaming on Amazon Kinesis; parallel voice and search-bar front ends; ... three data services". API gateway, ingestion, event streaming, Kinesis, front ends and data services are all bare, and Kinesis is reused as the main example of a guess. v0.2.1 was praised for never naming Kinesis. "session-based recommendations" and "fine-tuned" are also bare. Edit 3 addresses this.

Check 3, Borderline. Apart from the provenance and confidence issues under 13, there are two factual slips. One is "the one internal component Amazon has confirmed" (above). The other is "a standing order with fixed limits that you set, a price, a time window, and a cancellation period": the 24-hour cancellation is Amazon's term, and the pack does not say the user sets the six-month window. Also note "can hand you over to a human agent when it needs to" (the condition is added) and "instead of a results page" (added). Both are minor and both recur from last time.

Check 5, Borderline. The customer-service paragraph and the COSMO build detail ("trained on about 30,000 human-annotated instructions. It covers 18 major product categories.") can both go without a gap, as last time. So can the full Part C layer list.

Check 6, Borderline (down from Pass). "## Several models and a router" opens "The engine underneath any assistant like this is a large language model". It is cold, and it is again the section right after the problem. The later three sections restate.

Check 10, Borderline (down from Pass). "the source you were given" and "the material given here" address the reader as if they had received the source pack. This is the same leak as input 4, from the same phrase in the prompt.

11b, Fail. "It began life as a shopping chatbot called Rufus ... Alexa for Shopping and folded it into Alexa+ ... Echo speakers" (three names), and "Anthropic's Claude Sonnet, Amazon's own Nova models, and a custom model" (three). These are the same two paragraphs that failed in v0.2.1.

11a, Pass. The router, retrieval, memory, alert and auto-buy each appear with the cartridge example. The cart step uses a grocery-list photo, not the cartridge, which is a small miss.

## Recommended edits for v0.3.1, in order of importance

Edit 1. Make the pace check count names and lists of kinds (check section). This targets 11b on inputs 2, 3, 4, 7 and 9, and indirectly check 1 on inputs 3 and 9.

Replace:
> No paragraph hands the reader more than one new term. Where a paragraph names two or more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again.

With:
> No paragraph hands the reader more than one new term, and the names of products, projects, and companies count as terms. The one exception is a pair defined against each other, such as a request and its response, which can share a paragraph. Where a paragraph names more, give each term its own paragraph at the point the piece first needs it, and drop any name the piece never uses again. Where a paragraph lists several kinds or examples of one thing, keep the one the running example uses and leave the others out or give one a line in "Going further", because to a reader on a bus a list of names is a list of lookups.

Over-correction to watch: in input 9, the confirmed list of three model sources could be cut to one, losing a Part A fact the router depends on. Watch whether the models are spread across sentences or dropped. In input 7, splitting the namespace paragraph adds words, though there is about 200 words of headroom under 1,700.

Edit 2. Bound provenance, and stop the second-person leak (source paragraph). This targets M1, check 13 on input 9, and check 10 on inputs 4 and 9.

Replace:
> Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms.

With:
> Present unconfirmed parts as what the source says they are, and say where they come from in the source's own terms, adding nothing about who made them, where they circulate, or who uses them, because the reader cannot tell an origin you invented from one the source reported.

And replace:
> where the source is merely silent, say that the material you were given does not cover it.

With:
> where the source is merely silent, say that the sources behind this article do not cover it. The reader never saw the material you were given, so refer to it only in those words, and when the source block is empty, do not mention a source at all.

Edit 3. Give unconfirmed material only the space needed to recognise it (source paragraph). This targets check 1 Fail and check 5 on input 9.

Replace:
> Build the mechanism and the running example from the confirmed parts.

With:
> Build the mechanism and the running example from the confirmed parts. Give unconfirmed parts only the space the reader needs to recognise them and to see where they differ from the confirmed ones, not a full account of their contents, because every detail of a guess is a term the reader must learn for something that may not be true.

Edit 4. Keep inferred links out of "confirmed" in the closing paragraph (output section). This targets M3 and check 13 on input 9.

Replace:
> This is not a list of everything said; it is the core sentence from your plan, now fully earned.

With:
> This is not a list of everything said; it is the core sentence from your plan, now fully earned. If you say which steps are confirmed, call a step confirmed only when the source states it; a link you drew between confirmed parts, such as which part feeds which, stays marked as your reading there.

Edit 5. Make the second section restate as well (check section). This targets check 6 on inputs 2, 7 and 9.

Replace:
> Every "##" section or chapter after the first, apart from "The whole picture" and "Going further", opens with a sentence or two on what the reader now holds, so it can be picked up cold.

With:
> Every "##" section or chapter after the first, apart from "The whole picture" and "Going further", opens with a sentence or two on what the reader now holds, so it can be picked up cold. This includes the second one: the problem set up in the first section is something the reader holds, and the second section opens by restating it.

Not proposed as edits (watch on the next run): the Docker forward pointer (check 2), the Driftwood double admission (mostly fixed by edit 2), the named character in 1b (one sample of three), and Raft's history paragraph (edit 1 should move it). Version: these change the self-check and source handling but not the output shape, so by the design's table this is a minor bump at most. v0.3.1 is acceptable if the builder treats it as a wording fix.

## Failure log

Lines to add:

- 2026-11-18 | 2, 3, 4, 7, 9 | 11b Unhurried | The self-check counts "terms", but the model does not count product, project or company names, or lists of kinds or examples. Failing paragraphs are name lists (Paxos, etcd, Kubernetes; Rufus, Alexa+, Echo; Claude Sonnet, Nova; PID, network, mount namespace) and foundation vocabulary sets (topic, producer, consumer; job scheduler, queue, workers) | pending (0.3.1 edit 1)
- 2026-11-18 | 9 | 13 Source confidence | "Say where they come from in the source's own terms" is not bounded; model kept the true origin and added an invented one ("an architecture diagram that circulates online") | pending (0.3.1 edit 2)
- 2026-11-18 | 4, 9 | 10 Clean output | Prompt phrase "the material you were given" copied to the reader ("the material I was given contains nothing about it"; "which the source you were given describes"); in input 4 it fires with an empty source block | pending (0.3.1 edit 2)
- 2026-11-18 | 9 | 1 No lookups, 5 Padding | "Present unconfirmed parts as what the source says they are" read as "lay them out"; Part C layer list reproduced with API gateway, ingestion, event streaming, Kinesis and front ends unexplained | pending (0.3.1 edit 3)
- 2026-11-18 | 9 | 13 Source confidence | "The whole picture" stamps "Those steps are confirmed by Amazon" over an inferred link (account memory and price history arrive through retrieval) | pending (0.3.1 edit 4)
- 2026-11-18 | 2, 7, 9 | 6 Resumable | The section right after the problem section opens cold in all three; every later section restates. Model treats the problem section as an introduction, not as something the reader holds | pending (0.3.1 edit 5)
- 2026-11-18 | 9 | 3 Accurate | Exclusivity claim of the M4 kind recurs: "the one internal component Amazon has confirmed, the model router", contradicting the same paragraph; "fixed limits that you set ... a cancellation period" (the 24 hours is Amazon's term) | watch
- 2026-11-18 | 7 | 2 Linear | Forward pointer "That detail matters a great deal shortly." survives the write-section ban; the self-check does not list that phrase | watch

Existing "0.3.0 (edit applied, not yet tested)" lines:

- Line 10 (input 1, sized as moderate): fixed in 0.3.0. 3 of 3 samples are simple, 528 to 583 words, with no "The whole picture"; checks 4 and 5 pass.
- Line 11 (inputs 2 and 4, Resumable): partly fixed in 0.3.0. Input 4 is now simple (no sections, so check 6 does not apply). Input 2 moved from Fail to Borderline, with 3 of 4 sections restating. The remaining gap is logged as a new line (second section).
- Line 12 (input 4, unknown tool, Accurate): fixed in 0.3.0. Check 3 and new check 12 pass.
- Line 13 (inputs 2, 3, 4, 7, Unhurried): still failing on all four, and on input 9. The worst paragraphs are lighter (Kafka 4 to 3 terms, Docker 6 to 4), but each still has three or more. Superseded by the new 11b line.
- Line 14 (input 3, Complete): fixed in 0.3.0. Log repair and the discarded entry are shown with S1's "set price to 50".
- Line 15 (alexa, source confidence): partly fixed in 0.3.0. M2 and M5 are fixed, as are S1 to S5 and S7, and hedging creep was avoided. M1 and M3 recur in new forms, and the M4 kind recurs; see the new lines. 11b still fails.

## Before the next decision

- Run inputs 6 and 8. The design requires the second-domain input before "tested", and input 6 is the only check on compressing a long source.
- Run input 9 at least twice. It is the only input that regressed, and it rests on one sample.
- Record `verified_on` with the model that wrote the outputs and the date 2026-11-18. The grading model is not the verified model.

Process note: this session had Read, Grep, Glob and Write only, with no shell. Word counts are by hand, as stated at the top. Nothing outside this file was changed.

# Head gate review: built/explain.commuter.it.md v0.2.0

Date: 2026-11-15. Reviewer: dadhichi-head. Stage: gate review, before testing.

## Verdict: REVISE

Every logged v0.1.0 failure has a matching change, and the seven-section shape, variable list, and calm wording all hold. The version is held back for two reasons. First, the length fix is likely to over-correct on deep and moderate topics, and the rubric as written cannot detect that. Second, the word-budget examples name two of the test inputs. Five edits follow; none changes the direction of the version.

v0.1.0 was not saved as a file, so "what changed" is inferred from CHANGELOG.md and failures.md.

## 1. Does each change address a logged failure?

| Logged failure | Change in v0.2.0 | Judgement |
| --- | --- | --- |
| Inputs 2, 3: config keys, versions, variants in body (checks 4, 5) | Situation now sends "configuration settings, version differences, and optional features" to a closing list; the accuracy rule sends details to "Going further"; plan step 5 adds the body test | Addressed |
| Input 3: read strategies, pre-vote, history in body (check 5) | Body test names "performance optimisations, alternative implementations, and history" | Addressed |
| Inputs 2, 3: model plans to the top of the range; no word-count step (check 4) | Step 9 sets one number with a typical figure and a ceiling; the check adds a word estimate and a cut order | Addressed, with over-correction risk (section 2) |
| Input 3: chapters recap at both ends (check 5) | "End each chapter with a single sentence that raises the question the next chapter answers" and "Do not summarise a chapter at its end" | Addressed, but it now conflicts with a check line (section 3) |
| Inputs 2, 3: "as you will see" forward references (check 2) | Write rule lists the phrases and gives the reason; check line repeats it | Partly addressed. The phrases are banned, but the Raft case that produced them is not handled (section 3) |

## 2. Over-correction risk on length

This is the main finding.

I counted what v0.1.0 Raft (5,988 words) loses if everything the scorecard and failure log call padding is removed, plus the new recap limits:

- Paxos history paragraph, the "no algorithm can guarantee progress" paragraph, most of the Byzantine paragraph: about 240 words
- Read strategies (two paragraphs) and pre-vote: about 315
- Current-term commit rule and most of the durable-storage paragraph: about 260
- Odd-cluster-size paragraph, write latency, client redirect, faster back-off, etcd default: about 240
- Chapter-end recaps cut to one sentence, chapter openings cut to two sentences: about 220

Total about 1,300 to 1,350 words. What remains is roughly 4,400 to 4,650 words, and all of it is material no grader called padding: the problem, majorities, leaders and terms, the election, log replication with the consistency check, the election restriction, the discarded-entry case, and the partition scenario.

So the padding-free core of v0.1.0 Raft sits at the new ceiling (4,500), not at the new typical figure (3,500). The same holds for Kafka: 2,751 words minus the logged padding (rebalance protocol detail, static membership, auto.offset.reset, max.poll.interval.ms, the off-by-one note, exactly-once) is about 2,100 to 2,250, against a typical of 1,500 and a ceiling of 2,200.

Three pieces of v0.2.0 wording then push the model below that core:

1. Step 9 uses Raft itself as the example of a 3,500-word topic and says the ceiling is "for unusual cases, not a target". The model will plan Raft at 3,500, about 1,000 words under the clean core.
2. The cut order ends with "then the least needed foundation detail". Once the padding is gone and the piece is still over, this is the only instruction left, and it tells the model to thin the foundations.
3. The body test keeps a passage only if "the reader could not follow the core sentence". The core sentence is defined in step 1 as "what the topic is and why it exists". A reader can follow that sentence for Raft without the consistency check, the election restriction, or the partition scenario. Read literally, the mechanism itself fails the test. The goal section asks for more ("how it works at the level that matters"), so the test is anchored on the wrong thing.

Likely result on input 3: either the worked steps are compressed (several terms per paragraph, the running example dropped in places), or a whole mechanism step goes, most likely the log-repair walk-through or the discarded-entry case. The second would also weaken check 9, because the Raft trap ("in the log is not the same as committed") is only convincing once the reader has watched an entry get thrown away. Either result works against the stated aim of novel-like ease: a dense piece is harder on a bus than a longer one.

The rubric would not catch this. Check 4 says "Length fits difficulty" with a number only for input 1, and no check fails an output for being rushed or for skipping a mechanism step. A v0.2.0 Raft at 3,400 words with the consistency check squeezed into one paragraph could pass all ten checks and be promoted. See "Before the test run" below.

Smaller risk, same direction: the situation now sends "configuration settings" to the closing list. Protocol names that are part of the mechanism (RequestVote, AppendEntries, the poll loop in Kafka) are not settings, but a cautious model may drop them. Watch check 3 ("real terminology is used") and check 8 on inputs 2 and 3.

## 3. Other new-failure risks

Check line against chapter endings. The write section asks each chapter to end with "a single sentence that raises the question the next chapter answers". The check says "no phrase points ahead to an explanation still to come". A closing question is exactly a phrase that points ahead. A model running the check faithfully will delete its own chapter hooks, or keep them and treat the check line as soft, which weakens it for the real cases.

The Raft forward reference is structural, not a phrasing habit. In v0.1.0 the election chapter says: "There is one more check they make before voting, which matters a great deal for safety and gets its own chapter later; for now, assume C passes it." The election restriction cannot be explained until the reader knows what a committed entry is, and that comes two chapters later. v0.2.0 says "move its explanation earlier", which does not work here. With the phrases banned and no alternative given, the model will either write the same sentence in new words or reorder the piece badly. It needs to be told what to do when a rule's reason arrives late.

Test contamination. Step 9 uses "what an API key is" and "Raft consensus" as its calibration examples. These are test inputs 1 and 3. The prompt now states the expected length of two of the three topics run so far, so a pass on check 4 for those inputs would show the model can read a number, not that it can size a topic. It also hides whether the sizing generalises to inputs 5 to 8.

Plan order, minor. Step 5 refers to "the trap from step 8" before the trap has been chosen. No edit proposed; if step 9's rewrite is taken, consider moving the body test after the trap step in a later version.

## 4. Design rules

- Seven sections present and in order; source material sits above the instructions; TOPIC, SOURCE, NOTES are all listed in inputs. Pass.
- Reasons: every new instruction carries one ("because every extra passage on a bus costs attention", "summarising at both ends repeats the same material twice"). Pass.
- Calm wording: no capitals. "never more than" appears three times in step 9; firm but acceptable.
- Positive instructions: the new bans ("Do not summarise a chapter at its end", "Leave out phrases such as") each come with the positive form next to them. Pass.
- Process: "A released version is never edited. A fix is a new version." The project is not a Git repository and v0.1.0 was overwritten, so the old prompt cannot be diffed or rerun on inputs 4 to 8 for the promotion comparison. Not a prompt edit; see below.

## 5. Edits, in order of importance

Edit 1. Anchor the body test on the goal, not the core sentence (plan step 5).

Replace:
> keep it in the body only if, without it, the reader could not follow the core sentence or would fall into the trap from step 8.

With:
> keep it in the body only if, without it, the reader could not do what the goal promises, which is to say what the topic is, why it exists, and how its mechanism works step by step, or would fall into the trap from step 8. Each step of the mechanism passes, together with the one worked case that shows it. A refinement of a step, an option, or a second case of a point already made does not.

Edit 2. Stop the cut order from thinning the core (check section).

Replace:
> cut in this order until it fits: passages that fail the body test, repeated explanations of the same point, extra examples beyond the running one, then the least needed foundation detail.

With:
> cut in this order: passages that fail the body test, repeated explanations of the same point, extra examples beyond the running one, then whole in-flow ideas the core can stand without. Remove an idea whole rather than squeezing the explanation of the ones that stay, because a compressed explanation is harder to follow on a bus than a longer piece. If everything left passes the body test and the piece is under the upper limit for its size, leave it as it is.

Edit 3. Give the room above the typical figure a defined use, and take the test topics out of the examples (plan step 9).

Replace:
> A simple concept, such as what an API key is, gets about 400 words and no chapters, never more than 500.

With:
> A simple concept, such as what a port number is, gets about 400 words and no chapters, never more than 500.

Replace:
> A deep one, such as Raft consensus or how a language model generates text, gets about 3,500, never more than 4,500, split into chapters. Aim for the typical figure; the upper limit is a ceiling for unusual cases, not a target.

With:
> A deep one, such as how a language model generates text or how two computers set up an encrypted connection, gets about 3,500, never more than 4,500, split into chapters. Aim for the typical figure. The room between it and the upper limit is for a topic whose mechanism has more steps than usual; spend it only on passages that pass the body test, never on Later-tier material.

Edit 4. Remove the conflict between the forward-reference check and the chapter hook (check section).

Replace:
> No sentence relies on something that appears later, and no phrase points ahead to an explanation still to come.

With:
> No sentence relies on something that appears later, and no phrase inside a chapter points ahead to an explanation still to come. The single question that closes a chapter is the one exception, and it is sound only if nothing before it depended on the answer.

Edit 5. Say what to do when a rule's reason arrives late (write section).

Replace:
> If you find you need something you have not explained yet, move its explanation earlier.

With:
> If you find you need something you have not explained yet, move its explanation earlier. Sometimes that is impossible, because a rule's purpose depends on a mechanism the reader meets later. In that case describe the step as far as the present case needs, with no hint that more is coming, and introduce the further rule as a new fact at the point where the reader can see why it exists.

## 6. Before the test run (not prompt edits)

- Add a rubric check so over-correction is measurable, and grade the v0.1.0 outputs on it too so the promotion comparison stays like for like. Suggested wording: "11. Complete and unhurried: every mechanism step named in 'The whole picture' is explained in the body with the running example, and no paragraph introduces more than one new term." By my reading all three v0.1.0 outputs pass it.
- Settle the trivial-input limit. The design doc says about 400 words, the rubric and inputs.md say about 600, the prompt says 400 with a ceiling of 500. v0.1.0 input 1 was 615 words with check 5 passed, so 400 means cutting a third of an output nobody called padded. Decide the number and put it in one place.
- Save a copy of each prompt version in its run folder (for example runs/v0.2.0/prompt.md) so old and new can be rerun on the same inputs.
- Run inputs 4 to 8 this time. Three inputs, two of them named in the prompt, are not enough to promote on.
- After the run, fill the "fixed in version" column of failures.md; all five lines still say "pending".

## 7. What to look at first in the v0.2.0 Raft output

1. Whether the log-repair walk-through (follower E missing entry 6) and the discarded-entry case (A's uncommitted entry 7) both survive, each with the running example.
2. Whether any paragraph in the replication or safety chapters introduces two terms at once.
3. Whether RequestVote and AppendEntries are still named.
4. How the election restriction is introduced without a forward pointer.

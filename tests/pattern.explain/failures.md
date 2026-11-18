# Failure log: pattern.explain

One line per failure: date | input # | check failed | suspected cause | fixed in version

2026-11-15 | 2 | 4 Proportional, 5 Padding | Situation says reader will "open official documentation later" and write rules say "say so" for version differences, which licenses config keys, protocol versions, and implementation variants in the body | 0.2.1 (inputs 2, 3)
2026-11-15 | 3 | 5 Padding | Same cause; plus read strategies, pre-vote, and history kept in body instead of Going further | 0.2.1 (inputs 2, 3)
2026-11-15 | 2, 3 | 4 Proportional | Length ranges say "roughly"; model plans toward the top of the range, and the self-check has no word-count step | 0.2.1 (inputs 2, 3)
2026-11-15 | 3 | 5 Padding | Rule "end each chapter on what is now possible" read as "end with a recap", so chapters recap at both ends | 0.2.1
2026-11-15 | 2, 3 | 2 Linear | "This matters in a moment" exception generalized into "as you will see" forward references | 0.2.1 (inputs 2, 3)
2026-11-15 | 1 | 4 Proportional, 5 Padding | v0.2.1 sized the topic as moderate: step 9 has no criterion for "simple" after the API-key example was removed, and the body test passes every mechanism step whatever the size | fixed in 0.3.0
2026-11-15 | 2, 4 | 6 Resumable | Prompt applies the reminder rule to "chapters" and tells moderate pieces nothing about headings; model used many "##" sections and did not restate | partly fixed in 0.3.0 (second-section gap logged 2026-11-18)
2026-11-15 | 4 | 3 Accurate | No instruction for a topic unknown as a whole; model hedged on "details" and wrote a moderate-size generic piece under the tool's name | fixed in 0.3.0
2026-11-15 | 2, 3, 4, 7 | 11 Unhurried | One-idea-per-paragraph rule is in the write section but not in the self-check; vocabulary paragraphs stack three to six terms | still failing in 0.3.0; superseded by the 2026-11-18 11b line
2026-11-15 | 3 | 11 Complete | Log repair and discarded entry described as rules without the running example | fixed in 0.3.0
2026-11-15 | alexa (real use, mixed-confidence source) | 3 Accurate, 11 Unhurried | Prompt silent on carrying source confidence through: invented provenance, writer inferences stated as fact, claims of absence where source is silent, hedges dropped in The whole picture | partly fixed in 0.3.0 (M2, M5 fixed; M1, M3 and M4 kind recur, logged 2026-11-18)
2026-11-18 | 2, 3, 4, 7, 9 | 11b Unhurried | The self-check counts "terms", but the model does not count product, project or company names, or lists of kinds or examples. Failing paragraphs are name lists (Paxos, etcd, Kubernetes; Rufus, Alexa+, Echo; Claude Sonnet, Nova; PID, network, mount namespace) and foundation vocabulary sets (topic, producer, consumer; job scheduler, queue, workers) | pending (0.3.1 edit 1)
2026-11-18 | 9 | 13 Source confidence | "Say where they come from in the source's own terms" is not bounded; model kept the true origin and added an invented one ("an architecture diagram that circulates online") | pending (0.3.1 edit 2)
2026-11-18 | 4, 9 | 10 Clean output | Prompt phrase "the material you were given" copied to the reader ("the material I was given contains nothing about it"; "which the source you were given describes"); in input 4 it fires with an empty source block | pending (0.3.1 edit 2)
2026-11-18 | 9 | 1 No lookups, 5 Padding | "Present unconfirmed parts as what the source says they are" read as "lay them out"; Part C layer list reproduced with API gateway, ingestion, event streaming, Kinesis and front ends unexplained | pending (0.3.1 edit 3)
2026-11-18 | 9 | 13 Source confidence | "The whole picture" stamps "Those steps are confirmed by Amazon" over an inferred link (account memory and price history arrive through retrieval) | pending (0.3.1 edit 4)
2026-11-18 | 2, 7, 9 | 6 Resumable | The section right after the problem section opens cold in all three; every later section restates. Model treats the problem section as an introduction, not as something the reader holds | pending (0.3.1 edit 5)
2026-11-18 | 9 | 3 Accurate | Exclusivity claim of the M4 kind recurs: "the one internal component Amazon has confirmed, the model router", contradicting the same paragraph; "fixed limits that you set ... a cancellation period" (the 24 hours is Amazon's term) | watch
2026-11-18 | 7 | 2 Linear | Forward pointer "That detail matters a great deal shortly." survives the write-section ban; the self-check does not list that phrase | watch

# Scores: built/explain.commuter.it.md v0.1.0

Run 2026-11-15. Each output written by a fresh agent with no context except the filled prompt. Graded by the session model (same model family as the writer, so weaker than the rubric asks for).

| # | Check | 1 API key (615 w) | 2 Kafka groups (2,751 w) | 3 Raft (5,988 w) |
| --- | --- | --- | --- | --- |
| 1 | No lookups | Pass | Pass | Pass |
| 2 | Linear | Pass | Minor ("as you will see", line 21) | Fail (line 131 relies on A's log, explained only at line 137) |
| 3 | Accurate | Pass | Pass | Pass |
| 4 | Proportional | Borderline (615 vs ~600) | Fail (2,751 vs 2,500 ceiling) | Borderline (at the 6,000 ceiling) |
| 5 | No padding | Pass | Fail (static membership, protocol internals, leader election in body) | Fail (read strategies, pre-vote, Paxos history, double recaps) |
| 6 | Resumable | n/a | Partial (2 chapters open cold) | Pass (overdone: recap at start and end of chapters) |
| 7 | Plain text | Pass | Pass | Pass |
| 8 | Not dumbed down | Pass | Pass | Pass |
| 9 | Trap handled | Pass | Pass | Pass |
| 10 | Clean output | Pass | Pass | Pass |

Verdict: strong on clarity, accuracy, and no-lookups. One systematic failure: Later-tier material leaks into the body, pushing length to or past the top of the budget.

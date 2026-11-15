# Test inputs: pattern.explain

Run each input through `built/explain.commuter.it.md` and score the output with `rubric.md`.

| # | Type | TOPIC | SOURCE | NOTES | What it stresses |
| --- | --- | --- | --- | --- | --- |
| 1 | Trivial | What an API key is | empty | empty | Stays short (about 450 words, at most 600, no chapters) |
| 2 | Moderate | Kafka consumer groups | empty | empty | Tiering: partitions/offsets as foundation, rebalancing in-flow |
| 3 | Hard | Raft consensus | empty | empty | Clarity at depth; chapters resumable; running example holds |
| 4 | Outside knowledge | "Driftwood, the Rust job scheduler" (fictional on purpose) | empty | empty | Says it does not know the tool instead of inventing details |
| 5 | Vague | The cloud | empty | empty | Picks a sensible scope; does not sprawl |
| 6 | Long source | HTTP caching | Paste RFC 9111 sections 1 to 4 | empty | Compresses a dense source; cuts tangents |
| 7 | Reader note | Docker containers | empty | "I'm a backend developer, I know Linux processes well" | Skips what the reader knows; stays shorter |
| 8 | Second domain | Bond duration | empty | empty | Run with the IT domain block swapped for a finance one; tests that the pattern generalizes |

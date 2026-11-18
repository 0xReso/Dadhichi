# Rubric: pattern.grade

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | Complete | One verdict per rubric check, in rubric order, none missing or merged |
| 2 | Agreement | Verdicts match the reference on at least 90% of checks, counting Borderline vs Pass as half a miss |
| 3 | No false Fail | No Fail where the reference gives Pass |
| 4 | Evidence | Every non-Pass verdict quotes the output exactly, states a count, or names a specific absence |
| 5 | Quotes real | Every quote appears verbatim in the output |
| 6 | Counts | Word counts within 5% of `wc -w`, or marked approximate |
| 7 | Independent | No verdict cites a fault that belongs only to another check |
| 8 | Clean output | Only the verdict lines and the summary; no preamble, no rewrite advice |

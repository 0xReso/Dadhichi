# Test inputs: pattern.rubric

| # | Type | JOB | READER | PROMPT | FAILURES | What it stresses |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Known answer | Explain one IT concept so it can be understood in a single linear read on an e-reader, with no lookups | A commuter reading on a Kindle, no browser | tests/pattern.explain/runs/v0.4.0/prompt.md (paste only its prompt block) | Only the suspected-cause field from tests/pattern.explain/failures.md lines 5–9 | Compared with the hand-built explain rubric: does it rediscover the checks that mattered? |
| 1b | Known answer without prompt | Same as 1 | Same as 1 | empty | Same as 1 | Rediscovery without the self-check |
| 2 | Code | Review a pull request diff and report real defects, ranked, each with a concrete failing scenario; no style comments | The author of the PR, who will fix what is reported | empty | empty | Code domain; accuracy vs noise; numbers where possible |
| 3 | Writing under a name | Draft a cover letter for a specific job from the candidate's CV and the job ad | The hiring manager, who reads it in under a minute | empty | "Invented a degree the CV does not list"; "Opened with 'I am writing to apply for'" | Faithfulness to a source; checks that catch invented facts |
| 4 | Structured output | Turn a plain-English description into a SQL query, plus one line on cases it does not handle | A developer who will paste the query into a database console | empty | empty | Code checks (it runs, it parses) vs grader checks |
| 5 | Vague job | "Make my emails better" | empty | empty | empty | Handles a vague job: states the assumption, keeps checks decidable |
| 6 | Second domain | Explain a medication's dosing schedule to a patient leaving hospital | A patient at home, not medically trained, possibly tired | empty | empty | Safety-relevant domain; a check that the output does not overreach |
| 7 | Trivial, run twice | Return the number of nonblank lines in a supplied text as one decimal integer | A developer reading the result in a terminal | empty | empty | Avoids redundant checks for a one-number job |
| 8 | Unknown format | Validate an export against our internal Larkspur ledger format and report each invalid record by line number | An operator with access to the internal format specification | empty | empty | Names the missing specification and avoids inventing fields or limits |

The reference for inputs 1 and 1b is tests/pattern.explain/rubric.md. For the others the head judges the rubric directly against the rubric.md checks below.

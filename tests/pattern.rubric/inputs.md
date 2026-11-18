# Test inputs: pattern.rubric

| # | Type | JOB | READER | PROMPT | FAILURES | What it stresses |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Known answer | Explain one IT concept so it can be understood in a single linear read on an e-reader, with no lookups | A commuter reading on a Kindle, no browser | built/explain.commuter.it.md (released 0.4.0) | The first lines of tests/pattern.explain/failures.md (lines 4 to 9) | Compared with the hand-built explain rubric: does it rediscover the checks that mattered? |
| 2 | Code | Review a pull request diff and report real defects, ranked, each with a concrete failing scenario; no style comments | The author of the PR, who will fix what is reported | empty | empty | Code domain; accuracy vs noise; numbers where possible |
| 3 | Writing under a name | Draft a cover letter for a specific job from the candidate's CV and the job ad | The hiring manager, who reads it in under a minute | empty | "Invented a degree the CV does not list"; "Opened with 'I am writing to apply for'" | Faithfulness to a source; checks that catch invented facts |
| 4 | Structured output | Turn a plain-English description into a SQL query, plus one line on cases it does not handle | A developer who will paste the query into a database console | empty | empty | Code checks (it runs, it parses) vs grader checks |
| 5 | Vague job | "Make my emails better" | empty | empty | empty | Handles a vague job: states the assumption, keeps checks decidable |
| 6 | Second domain | Explain a medication's dosing schedule to a patient leaving hospital | A patient at home, not medically trained, possibly tired | empty | empty | Safety-relevant domain; a check that the output does not overreach |

The reference for input 1 is tests/pattern.explain/rubric.md. For the others the head judges the rubric directly against the rubric.md checks below.

# Rubric: pattern.explain

Yes/no checks. Grade with a different model from the one that wrote the output, and let the grader reason before giving each verdict.

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | No lookups | Every term, acronym, and named technology is introduced before or at first use |
| 2 | Linear | No sentence depends on something that comes later |
| 3 | Accurate | No technical error; real terminology is used |
| 4 | Proportional | Within the prompt's budget: simple ≤600, moderate ≤2,200, deep ≤4,500 words |
| 5 | No padding | No section could be deleted without leaving a gap |
| 6 | Resumable | Each section or chapter (anything under a "##" heading, excluding "The whole picture" and "Going further") after the first restates what the reader holds so far |
| 7 | Plain text | Reads correctly on an e-reader: no tables, links, images, nested lists, or wide code |
| 8 | Not dumbed down | No fictional framing or characters; real names kept; analogies state where they break |
| 9 | Trap handled | The most common misconception about the topic is named and corrected |
| 10 | Clean output | No visible plan, no preamble, no offer to expand |
| 11a | Complete | Every mechanism step named in "The whole picture" is explained in the body with the running example |
| 11b | Unhurried | No paragraph introduces more than two new terms, and two only when they are a pair defined against each other |
| 12 | Unknown topic (input 4 only) | The first two sentences say the tool is not known, and nothing is attributed to it |
| 13 | Source confidence (inputs with a SOURCE) | No statement is presented at higher confidence than the source gives it, and nothing about the source's origin is invented |

## Human check

Checks 1 and 2 are the point of this prompt, and a grader can miss them. Read the output on a phone, away from a desk, and count every pause where you wanted to look something up or scroll back. Target: zero.

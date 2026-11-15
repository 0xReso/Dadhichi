# Rubric: pattern.explain

Yes/no checks. Grade with a different model from the one that wrote the output, and let the grader reason before giving each verdict.

| # | Check | Pass condition |
| --- | --- | --- |
| 1 | No lookups | Every term, acronym, and named technology is introduced before or at first use |
| 2 | Linear | No sentence depends on something that comes later |
| 3 | Accurate | No technical error; real terminology is used |
| 4 | Proportional | Within the prompt's budget: simple ≤600, moderate ≤2,200, deep ≤4,500 words |
| 5 | No padding | No section could be deleted without leaving a gap |
| 6 | Resumable | Each chapter after the first restates what the reader holds so far |
| 7 | Plain text | Reads correctly on an e-reader: no tables, links, images, nested lists, or wide code |
| 8 | Not dumbed down | No fictional framing or characters; real names kept; analogies state where they break |
| 9 | Trap handled | The most common misconception about the topic is named and corrected |
| 10 | Clean output | No visible plan, no preamble, no offer to expand |
| 11 | Complete and unhurried | Every mechanism step named in "The whole picture" is explained in the body with the running example, and no paragraph introduces more than one new term |

## Human check

Checks 1 and 2 are the point of this prompt, and a grader can miss them. Read the output on a phone, away from a desk, and count every pause where you wanted to look something up or scroll back. Target: zero.

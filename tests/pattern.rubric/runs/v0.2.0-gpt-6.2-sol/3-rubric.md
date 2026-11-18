| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Letter length | The output contains at most 200 words. | code |
| 2 | Ready to send | The output consists of a finished cover letter addressed to the employer. | grader |
| 3 | Target position | The letter identifies the advertised role and, when named in the ad, the employer. | grader |
| 4 | Substantive opening | The first body sentence names a concrete candidate qualification or a specific aspect of the advertised work that interests the candidate. | grader |
| 5 | Supported candidate claims | Every factual claim about the candidate is supported by the CV. | grader |
| 6 | Evidence of fit | The body connects at least one concrete example from the CV to a specific responsibility or qualification in the job ad. | grader |
| 7 | Accurate job details | Every factual claim about the role or employer, other than its identity, is supported by the job ad. | grader |

## Grading conventions

1. Count whitespace-separated tokens across the entire output, including any salutation and sign-off. A count of 200 passes and 201 fails.
2. Treat the output as one document. One instance of drafting commentary, an instruction to the candidate, an alternate version, or an unfilled placeholder fails. A generic salutation or an omitted recipient name passes when the ad supplies no recipient name.
3. Compare the role and employer names with the job ad. An unambiguous shortened title or employer name passes. Omit the employer-name requirement when the ad does not identify the employer. Score wrong role or employer names here only.
4. Read the first sentence after any salutation. An announcement of the application alone fails, regardless of wording. A sentence that announces the application and also names a concrete qualification or aspect of the work passes. Grade the opening separately from the accuracy of its details.
5. Compare each distinct factual claim about the candidate with the CV. One unsupported degree, credential, skill, duty, result, or other factual claim fails. A faithful paraphrase or a calculation directly supported by the CV passes. Statements of present interest or intent fall outside this check.
6. Use the CV and job ad to identify the example and the corresponding requirement. A project, task performed, or result counts as an example. The connection may appear in one sentence or across adjacent sentences if the letter makes the link explicit. Score a missing connection here and unsupported details under check 5 or 7.
7. Compare each distinct factual claim about the role or employer with the job ad. One unsupported assertion fails. A faithful paraphrase or a statement of what the candidate hopes to contribute passes. Score the role and employer names under check 3.
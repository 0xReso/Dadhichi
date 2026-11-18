| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Word budget | The output stays within the explicit word limit for each applicable part and uses a 1,500-word total cap if the assignment supplies no word limits. | code |
| 2 | Requested concept | The body explains the assigned IT concept and answers each question explicitly asked about it, or explains one IT concept if the topic is open. | grader |
| 3 | Mechanism shown | The body follows one concrete case from its starting conditions through the concept’s defining operation to an observable result. | grader |
| 4 | Technical accuracy | Every technical claim is correct within the conditions the output states. | grader |
| 5 | Definitions at use | Every unfamiliar term or abbreviation needed to follow the explanation is defined on or before its first use. | grader |
| 6 | Offline completeness | The output supplies the information needed to complete the explanation without consulting another resource. | grader |
| 7 | Optional detail placement | Every technical detail beyond the requested scope and unnecessary to the core explanation appears only in an explicitly optional section after the body. | grader |
| 8 | Linear reading order | Every statement in the body can be understood where it appears without a later explanation of how or why it is true. | grader |
| 9 | Chapter endings | The final paragraph of each chapter that has an ending takeaway adds a consequence, inference, or practical use beyond what that chapter has already stated. | grader |

## Grading conventions

1. Count whitespace-separated tokens containing at least one letter or digit in the rendered text, including headings, captions, code, and optional material. Apply stated endpoints as inclusive limits even when qualified by “roughly” or “about.” One word outside an applicable limit fails. Use the assignment to identify limits and the parts they cover.
2. Compare the body with the assignment’s topic and explicit questions. One unanswered question or substitution of a neighboring topic fails. Introducing a supporting concept passes when it serves the assigned explanation.
3. Use one case as the unit. If no case contains all three elements, fail. A hypothetical with a stated input, an explained operation, and a stated output passes.
4. Use the technical claim as the unit. One false claim fails. A simplified claim passes if it holds within its stated conditions. Use the assignment’s reference material or an authoritative technical source to resolve disputed claims.
5. Use the first occurrence of each necessary technical term as the unit. One undefined term fails. A plain-language explanation in the same sentence passes. Treat terms the assignment explicitly says the reader knows as familiar. Score defined terms whose mechanism is deferred under check 8.
6. Use each external dependency as the unit. One required lookup, download, or inspection fails. A citation or optional reading link passes if the explanation is complete offline. Score missing definitions and internal deferrals under checks 5 and 8, respectively.
7. Use each removable technical detail as the unit. One detail in the body fails if removing it leaves the requested explanation and its example intact. Apply this rule to configuration keys, protocol versions, implementation variants, optimization strategies, and history. A version or implementation detail passes in the body when the assignment asks for it or the mechanism depends on it. A final section titled “Going further” or another clearly optional label passes.
8. Use the statement as the unit. One statement that requires an explanation supplied only later fails, whether or not it explicitly points ahead. A preview passes if the reader can understand its present role using what they already know. Score an undefined label by itself under check 5.
9. Use the last prose paragraph of each chapter or equivalent main section as the unit. One paragraph whose sole function is to restate points already made in that section fails. A closing inference grounded in the preceding explanation passes, as does ending on the last substantive step without a takeaway. Apply the same rule to the final paragraph of an unsectioned explanation.
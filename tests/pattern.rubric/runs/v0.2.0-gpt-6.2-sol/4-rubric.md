| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | SQL deliverable | The output contains a SQL block that attempts the requested operation. | grader |
| 2 | Console syntax | The SQL block parses as written in the applicable dialect. | grader |
| 3 | Schema fidelity | Every reference to an existing database object agrees with the supplied schema or is identified as an assumption when the input leaves it unspecified. | grader |
| 4 | Requested behavior | The SQL implements every result or state change required by the request. | grader |
| 5 | Statement scope | Every database operation in the SQL block is necessary for the requested task or explicitly requested. | grader |
| 6 | Limitation line | After the SQL block, the output has exactly one nonblank prose line. | code |
| 7 | Limitation accuracy | The final prose line names at least one material unhandled case or states that there are no known exclusions within the stated scope when none can be identified. | grader |
| 8 | Output boundaries | The SQL block and final prose line are the only nonblank content in the output. | code |

### Grading conventions

1. Unit is the SQL block, either fenced or plain text. A block that attempts the operation passes this check even if it has defects scored elsewhere. Prose, pseudocode, or a block that only performs a different task fails. Compare with the original request.
2. Unit is each SQL statement. One syntax error, an unsupported dialect construct, or an unresolved template token fails. Native parameters pass when the request or named console supports binding them. Use the requested dialect, then any dialect identified by the output. If neither is specified, accept syntax valid in a mainstream SQL dialect. Score database object references under check 3.
3. Unit is each reference to a table, column, or other existing schema object. One contradiction or undeclared assumption fails. An assumption may appear in a SQL comment or the final line. Query-defined aliases and common table expressions need no assumption. Use the supplied schema and identifiers in the request.
4. Unit is each requested result or state change. One missing or incorrect requirement fails, including a requested filter, output column, aggregation, ordering, or row boundary. Evaluate the logic assuming syntax defects are repaired and references resolve as intended. Score separate, unnecessary operations under check 5.
5. Unit is each database operation, including operations embedded in a statement. One unnecessary operation fails, such as an unrelated lookup appended to a report or a write added to a read-only request. Required joins, subqueries, and explicitly requested setup pass. Score predicates and row-selection errors under check 4.
6. Unit is the prose section after the SQL block. Count physical lines after trimming trailing whitespace and ignoring blank lines. Zero or two or more nonblank prose lines fail. Display wrapping does not add a line. If the SQL block is absent, score that omission under check 1 only.
7. Unit is the limitation claim. One concrete, accurate exclusion that could change how the developer uses the query is sufficient, and one false claim fails. An actual exclusion caused by a stated assumption qualifies. A missing requested behavior is scored under check 4 even if disclosed here. Skip this check if there is no single prose line to grade.
8. Unit is each section outside the SQL block and its following prose section. One extra heading, preamble, or other nonblank section fails. SQL fence markers and an optional language tag pass. Extra lines within the following prose section are scored under check 6.
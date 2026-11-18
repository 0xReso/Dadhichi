| # | Check | Pass condition | Decided by |
|---|---|---|---|
| 1 | Invalid record coverage | Every record the grader identifies as invalid under the supplied Larkspur specification appears in the report. | grader |
| 2 | Valid record exclusion | No valid record or source line without a record is reported as invalid. | grader |
| 3 | Source line numbers | The line number or range given for each reported invalid record locates that record in the original export. | grader |
| 4 | Duplicate record entries | Each invalid record identified in the report has at most one report entry. | grader |
| 5 | Supported violation claims | Every stated reason for flagging a record is supported by both the supplied specification and the export. | grader |
| 6 | Clean export result | When validation is complete and the export contains zero invalid records, the output explicitly says that no invalid records were found. | grader |
| 7 | Missing validation inputs | When the export or the applicable Larkspur rules are unavailable, the output identifies the missing prerequisite without claiming a validation result that depends on it. | grader |

## Grading conventions

1. Score per invalid record against the grader’s reference list, using the same export and specification available to the model. One omission is Fail. If an entry clearly identifies the record despite an incorrect line number, count it as present and score the locator under check 3. Apply only to records the available inputs let the grader assess.
2. Score per flagged record or non-record line against the original export and specification. One false positive is Fail. A wrong locator for an otherwise identifiable invalid record belongs to check 3. Apply only where the available inputs establish that the flagged item is valid or is not a record.
3. Score per entry that refers to an invalid record. One missing or incorrect locator is Fail. Follow the specification’s numbering convention if it supplies one. Otherwise, count physical lines from 1, including headers and blank lines, and accept either the record’s starting line or its exact span. If the record can be identified only by its locator, use that locator to score checks 1 and 2 and do not also infer a locator error.
4. Score per identifiable invalid record. One extra entry is Fail. Multiple violations listed together for a single record count as one entry. Apply only when the output reports invalid records.
5. Score per stated violation reason against the export and the applicable rule. One unsupported reason is Fail. An accurate paraphrase passes, and an entry with no reason does not fail this check. Score the validity of the flagged record itself under check 2.
6. Apply only when the supplied inputs support a complete validation and the grader’s reference list is empty. An empty report or a bare success label is Fail. “0 invalid records” passes.
7. Score per missing prerequisite and per reported result that depends on it. One unnamed missing prerequisite or one unsupported result is Fail. A partial finding passes if the available inputs establish it and the output states the limit of what could be checked. Apply only when a required input or rule is unavailable.
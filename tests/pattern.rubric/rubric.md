# Rubric: pattern.rubric

| # | Check | Pass condition | Decided by |
| --- | --- | --- | --- |
| 1 | Size | Between 5 and 12 checks | code |
| 2 | Decidable | Every pass condition can be decided by a quote, a count, or a named absence; no bare adjective where a number or comparison fits | grader |
| 3 | Matters | Every check is about something the stated reader would notice; none is unfailable | grader |
| 4 | No overlap | No single plausible fault would fail two checks | grader |
| 5 | Failures covered | Every line in FAILURES is caught by a named check, and that check would also catch a reworded instance of the same kind | grader |
| 6 | Marked | Each check is marked code or grader, and every check that plain code could run is marked code | grader |
| 7 | On task | Includes a check that the output does the asked job and not an easier nearby one | grader |
| 8 | Recall (inputs 1, 1b) | Covers at least 6 of the 8 explain checks the library found most decisive (1, 2, 3, 4, 5, 6, 9, 11b) on input 1, and at least 4 on input 1b | grader |
| 9 | Clean output | Only the table, the conventions section, and on a vague job one "Assumed:" line | grader |
| 10 | Conventions | Every check that covers the whole output has a convention line giving its unit and its single-instance verdict, and no convention softens a check where one instance fails the reader | grader |
| 11 | Assumption (input 5) | The first line begins "Assumed:" and names a reader and an output; no other input has one | code |

# Grade: upskill quiz v0.2.0, input 3 (PostgreSQL isolation levels, high), part 1 of 2

Scope: check 2 (Correct) and check 3 (Determinate), questions 1 to 50 only. Questions 51 to 100 and all other checks are graded in part 2.

Method: I worked each question from the question text and the stated assumptions (PostgreSQL 16 defaults, autocommit unless BEGIN, numbered order, a blocked step blocks only its own session) before reading its answer. I tracked statement and transaction snapshots, row-lock modes, the READ COMMITTED EvalPlanQual re-check, REPEATABLE READ "concurrent update" failures, SSI rw-conflicts, unique-index waits, table-lock queueing, and deadlock_timeout. Then I compared my result with the stated one and read each Why trace for false steps, since a false step is Borderline under check 2.

## Per-question results

| Q | My result | Stated result | Agree |
| --- | --- | --- | --- |
| 1 | (a) 100 at once; the reader does not block | (a) | yes |
| 2 | 70; 100 | 70; 100 | yes |
| 3 | 100; 500 (new snapshot per statement under RC) | 100; 500 | yes |
| 4 | 0; 0 (autocommit already committed; ROLLBACK gives a "no transaction in progress" WARNING) | 0; 0 | yes |
| 5 | (a) waits | (a) | yes |
| 6 | 300; 300 (snapshot taken at first statement, not BEGIN) | 300; 300 | yes |
| 7 | 3, 3, 4 | 3, 3, 4 | yes |
| 8 | (a) could not serialize access due to concurrent update; B already committed, so no wait | (a) | yes |
| 9 | 130 (B waits, re-checks on 110) | 130 | yes |
| 10 | 200, 200, 200 | 200, 200, 200 | yes |
| 11 | returned 6, seen 5 | 6, 5 | yes |
| 12 | no wait; 0 | no wait; 0 | yes |
| 13 | 130 (lost update) | 130 | yes |
| 14 | step 4 ERROR current transaction is aborted; step 5 reports ROLLBACK; step 6 (1,100),(2,100) | same | yes |
| 15 | (c) waits on the uncommitted duplicate, then succeeds | (c) | yes |
| 16 | only step 4 waits; step 3 returns 100 | same | yes |
| 17 | (a) "must be called before any query" | (a) | yes |
| 18 | 1; 2 | 1; 2 | yes |
| 19 | (c) at A's COMMIT | (c) | yes |
| 20 | UPDATE 0, no error; 0 | same | yes |
| 21 | waits, then UPDATE 0, no error | same | yes |
| 22 | 100 + 140 = 240 | 240 | yes |
| 23 | 3 (snapshot covers all tables) | 3 | yes |
| 24 | 3; 4 | 3; 4 | yes |
| 25 | 0 rows deleted; (1,10),(2,11) | same | yes |
| 26 | waits, then succeeds after B rolls back; 101 | same | yes |
| 27 | (a) 0 (write skew) | (a) | yes |
| 28 | 2 | 2 | yes |
| 29 | no wait; 2 bookings | same | yes |
| 30 | step 4 ERROR could not obtain lock on row; step 5 ERROR current transaction is aborted | same | yes |
| 31 | step 4 waits, returns 150; final 180 | same | yes |
| 32 | 1,000,000 | 1,000,000 | yes |
| 33 | B waits for A's ACCESS SHARE; C queues behind B's ACCESS EXCLUSIVE request; after step 5 B completes, then C returns 3 | same | yes |
| 34 | no wait (FOR NO KEY UPDATE and FOR KEY SHARE are compatible) | no wait | yes |
| 35 | (b) | (b) | yes |
| 36 | (b) exactly one fails; in practice B, when it commits | (b), "normally B, at COMMIT" | yes |
| 37 | read committed (SET TRANSACTION outside a block only warns) | read committed | yes |
| 38 | 1, 2, 3 | 1, 2, 3 | yes |
| 39 | 150 | 150 | yes |
| 40 | 100; no rows | same | yes |
| 41 | step 3 no; step 4 yes (its snapshot matches row 1 at 100, which A has locked) | same | yes |
| 42 | 200; 600 | 200; 600 | yes |
| 43 | 0; waits, then duplicate key error on acct_pkey after A commits | same | yes |
| 44 | 0 (SSI does not track the READ COMMITTED transaction) | 0 | yes |
| 45 | yes, waits | yes | yes |
| 46 | 70 / 3, about 23.33 | 23.33 (70 / 3) | yes |
| 47 | 1 | 1 | yes |
| 48 | 'new'; serialization failure | same | yes |
| 49 | A 1, B 2; neither waits | same | yes |
| 50 | step 5 ERROR current transaction is aborted; step 6 ROLLBACK; step 7 0 | same | yes |

Totals: 50 agree, 0 disagree, 0 ambiguous.

## Check 2 (Correct), Q1 to Q50: Pass

All 50 stated results match my own. I found no false step in any Why trace. Points I checked with extra care:

- Q25: the trace says correctly that row 1 is never considered. B's snapshot shows hits = 9, so the row is never locked or re-checked, even though its committed value later becomes 10.
- Q33: C queueing behind B's waiting ACCESS EXCLUSIVE request is correct. A new lock request that conflicts with an earlier waiter waits behind it.
- Q36: "normally B, at COMMIT" matches how SSI behaves here. At A's pre-commit check, B is a pivot whose out-conflict partner A commits first, so B is doomed, and B's COMMIT fails.
- Q37: the warning text "SET TRANSACTION can only be used in transaction blocks" is accurate, and the following BEGIN runs at the default level.
- Q44: accurate. SerializationNeededForWrite is false for the READ COMMITTED writer, so no rw-conflict is ever recorded against A's SIREAD lock.

Advisory only (this is a Rule line, not a trace step, so it does not lower the grade): the Q28 Rule says "INSERT ... ON CONFLICT always ends in either an insert or an update, never an error." That is overgeneral. The statement can still fail on a different unique index, on another constraint, or with "ON CONFLICT DO UPDATE command cannot affect row a second time" when a multi-row insert repeats a key. A safer wording would be: "under READ COMMITTED, INSERT ... ON CONFLICT on the conflicting key ends in either an insert or an update, never a duplicate key error."

## Check 3 (Determinate), Q1 to Q50: Pass

Every question has exactly one defensible answer under the stated assumptions. I looked hardest at these candidates and found none ambiguous:

- Q19: (b) and (c) are close in time, because A's COMMIT follows the sleep. But the stem asks when B finishes, and only the commit releases the lock, so (c) is the only defensible choice.
- Q35 and Q36: which transaction is the victim is not fixed by the stem, but the options are worded as "one transaction" and "exactly one of them", so the answer is still determinate.
- Q46: "divides the sum by the count" happens in the application. Integer division would give 23 rather than 23.33. Both rest on the same inconsistent inputs (70 and 3), and the answer states the result as 70 / 3, so I do not count it as ambiguous. If the builder wants it airtight, it could add "as a decimal".
- Q11: the scalar subquery over `u` makes the CTE run, and the outer read of `t` sees the pre-statement snapshot whatever the evaluation order, so the answer is determinate.

## Most important fix next (within this scope)

There is nothing that changes a verdict. The only edit worth making is the Q28 Rule wording above, so the rule is not overgeneral.

# Head grading — PostgreSQL 16 transaction isolation

Input 3 · high depth · sheet mode · frozen prompt v0.2.0 · writer `gemini-4-neon`

**8 Pass, 1 Borderline, 6 Fail.** Check 15 is inapplicable. The first repair is Q54 and mechanism 25. Both teach that `ON CONFLICT DO NOTHING` can suppress a conflict with a row committed after a Repeatable Read snapshot. In this schedule the insert raises `40001`. The final table happens to look the same whichever outcome the learner predicts. The error is in whether the transaction succeeded. [PostgreSQL 16 executor, conflict handling](https://github.com/postgres/postgres/blob/REL_16_STABLE/src/backend/executor/nodeModifyTable.c)

I recorded all 100 results from the questions before opening the answer key. These are manual schedule traces checked against PostgreSQL 16 documentation and implementation. The counts for checks 8 and 11 were computed with Python 3. The comparison table distinguishes a wrong result from a correct result that requires an extra premise or has a faulty explanation.

## Rubric decisions

1. **Count.** The high-depth questions and answers are both numbered 1 through 100 exactly once, in order. **Pass**
2. **Correct.** Q54 states “T1 succeeds (0 rows inserted, no `40001`); `kv` contains `('x', 1)`.” T1 acquired an empty snapshot at step 2. When the unique index finds T2’s committed row at step 4, the executor’s `DO NOTHING` path calls `ExecCheckTIDVisible`. The row was inserted by another transaction and is invisible to T1’s transaction snapshot, so this check raises `40001`. Step 5 ends the failed transaction with a rollback. T2’s row remains. Q91 also overstates a conditional failure. Correct final outcomes with false trace steps are identified below. A single definitely wrong outcome is sufficient. [PostgreSQL 16 executor](https://github.com/postgres/postgres/blob/REL_16_STABLE/src/backend/executor/nodeModifyTable.c) **Fail**
3. **Determinate.** Q46 asks “Which single change eliminates these deadlocks?” Both (c) and “(d) Remove `BEGIN ... COMMIT` so each `UPDATE` runs as its own autocommit statement” eliminate this two-row cycle. Only (c) preserves an atomic transfer, a condition absent from the question. Q91 says “when two requests hit the same row concurrently” without ordering their first reads. Both requests can start, the first can read, update and commit, and the second can then take its first snapshot and succeed. If both take the old snapshot, the stale writer fails. Q83 says “while a 10-minute reporting `SELECT` is active” without saying how much longer it holds the lock. A release 200 ms later permits the DDL, while a wait exceeding one second times out. Q99 omits the transaction boundary for (c), as detailed in the table. These are schedule and wording issues independent of server settings. [PostgreSQL 16 isolation](https://www.postgresql.org/docs/16/transaction-iso.html) · [Lock timeout](https://www.postgresql.org/docs/16/runtime-config-client.html#GUC-LOCK-TIMEOUT) **Fail**
4. **Assumptions.** The opening fixes the version, default isolation, autocommit, lock timeouts and indexed Serializable scan convention. It leaves sequence state unspecified. Q33 says “`logs(id SERIAL PRIMARY KEY, msg text) starts empty`”; Q80 likewise says “`t(id SERIAL PRIMARY KEY, u int UNIQUE) starts empty`”. A default sequence can previously have issued values even when its table contains zero rows. Both exact-ID answers, and Q100’s, require an unused sequence starting at 1. For these self-contained exercises, specifying freshly created sequences with no other consumers would suffice. Q70 supplies the first ID explicitly. [PostgreSQL 16 sequence functions](https://www.postgresql.org/docs/16/functions-sequence.html) **Fail**
5. **Prediction.** The 90 questions with fenced schedules or SQL all ask what a statement returns, whether a transaction waits or fails, or which state results. That subset alone exceeds the 50% threshold. **Pass**
6. **No trivia.** Q84, for example, supplies both error names and codes. Choosing between them requires tracing a unique check against a committed post-snapshot row. The other questions likewise ask about behavior. **Pass**
7. **Trap named.** Each of the 100 trap fields identifies a particular mistaken inference. Q48 distinguishes waiting for a first table access from taking a snapshot at the first query. Q54 even names a specific belief, although the key wrongly calls that belief a mistake. Its factual error is scored under checks 2 and 14. **Pass**
8. **Answer shape.** All 100 entries have Why, Answer, The trap and Rule, once each and in that order. Removing field labels and splitting the remaining text on whitespace gives **95/100** within the inclusive 60–150 range. The five exceptions are Q57 (167), Q69 (159), Q79 (170), Q97 (157), and Q99 (171). The shortest has 71 words. Counting the labels too gives the same 95 passing entries. **Pass**
9. **Coverage.** The key opens with 30 mapped mechanisms and the questions omit the map. However, Q1 and Q2 repeat the same entire artifact, including “3. T2: SELECT bal FROM accounts WHERE id = 1;”. Q2 asks for the same read with its wait behavior added and offers the value as a choice. Q32 and Q75 also repeat a pair of disjoint writes after relation-wide predicate reads with the same commit order. The map further assigns Q65 to fresh snapshots *per statement*, although “What value does step 3 return once step 5 commits?” tests a locking read following an updated row *within* one statement. **Fail**
10. **Distractors.** All 19 multiple-choice questions have four options. Q46(d) eliminates the specified deadlock and therefore rewards a valid inference. Q38 asks “Which output is impossible for T1?” but (d), “Either `(10, 10)` or `(99, 99)` depending on timing”, is a statement about two other options, not a returned row or a distinct wrong model. Replace it with a concrete output and make the snapshot timing explicit. **Fail**
11. **Artifact size.** Python found 90 SQL fences, each at most **9 physical lines**, counting schema comments, continuations and numbered steps and excluding the fence markers. The other 10 questions use prose or inline SQL. The longest setup/stem is 51 whitespace-delimited words (Q100), excluding choices and code. Q5 nevertheless asks “What happens to T2 at step 3” and then supplies “5. -- T2 finishes (autocommit)” after T1’s rollback. That gives away the wait portion of the requested answer. The learner still has to derive the final quantity. **Borderline**
12. **Progression.** Q1–20, Q21–70 and Q71–100 give exactly 20/50/30. In the last band Q79 combines snapshot qualification with a post-wait recheck, Q87 tests a same-row write with a rolled-back subtransaction, and Q100 combines a transaction retry, a sequence and an external side effect. **Pass**
13. **Answers hidden.** The questions file contains the three bands. The worked solutions, marked choices, rules and mechanism map are in the separate key. Q5’s timing hint is scored under check 11. **Pass**
14. **Honesty and source.** This input supplies no external source. The key publishes an invented isolation-level exception as reusable advice. Mechanism 25 says “while `DO NOTHING` skips cleanly”, and Q54’s trap calls “Predicting `40001`” a mistake. The executor explicitly checks snapshot visibility for this conflict action. Repeating the exception in the map and teaching the correct answer as a misconception makes this an undeclared unreliable area. [PostgreSQL 16 executor](https://github.com/postgres/postgres/blob/REL_16_STABLE/src/backend/executor/nodeModifyTable.c) **Fail**
15. **Diagnosis.** This is sheet-mode input 3. The check applies only to interactive input 9. **N/A**
16. **No copying.** Neither the React effects example, the coupon-bond comparison, nor the Python mutable-default example reappears. The artifacts use SQL statements and transaction schedules throughout. **Pass**

## Independent comparison

“Yes” compares the requested outcome. “Conditional” identifies an additional premise needed for the stated result, and “Incomplete” identifies an omitted defensible answer. Trace qualifications follow the table.

| Q# | Independent result | Stated result | Agree? |
| --- | --- | --- | --- |
| 1 | 100, the committed balance | `100` | Yes |
| 2 | (b) 100 immediately, plain read | (b) T2 returns `100` immediately without blocking. | Yes |
| 3 | Empty. Division by zero aborts the transaction | Empty table (0 rows). | Yes |
| 4 | 1, 2, 10, 20. The insert reads the original two rows once | `1, 2, 10, 20` (4 rows). | Yes |
| 5 | Wait, then write 8 after rollback | T2 blocks at step 3 until step 4 rolls back; afterward `qty` is `8`. | Yes |
| 6 | 100 then 200, two statement snapshots | Step 2 returns `100`; step 4 returns `200`. | Yes |
| 7 | 3 including the newly committed row | `3` | Yes |
| 8 | 0 updated, balance 20 after recheck | Step 3 updates `0` rows; final `bal` is `20`. | Yes |
| 9 | 9, both commit the literal 9 | `stock` is `9`; neither transaction fails. | Yes |
| 10 | (a) Wait for the uncommitted unique key | (a) T2 blocks until T1 commits or rolls back. | Yes |
| 11 | ('a',3), 1 plus the proposed 2 | `('a', 3)` | Yes |
| 12 | (c) Only T3 waits | (c) Only T3 blocks; T2 returns `'open'` immediately. | Yes |
| 13 | 2, the first unlocked job | `2` | Yes |
| 14 | (b) One victim gets 40P01, the other continues | (b) PostgreSQL detects the cycle and aborts one transaction with `40P01`, allowing the other to proceed. | Yes |
| 15 | 1 and 3 survive | `1` and `3` | Yes |
| 16 | (c) T2 waits on T1, T3 queues behind T2 | (c) T2 blocks on T1, and T3 blocks behind T2. | Yes |
| 17 | 5, first snapshot after the update | `5` | Yes |
| 18 | 2 at both counts | `2` | Yes |
| 19 | 40001, the target changed since the snapshot | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 20 | 0, RR permits disjoint writes | `0` | Yes |
| 21 | 100, dirty version invisible even at RU | `100` | Yes |
| 22 | 300, the waiting update doubles 150 | `300` | Yes |
| 23 | 20, max in the original statement snapshot | `20` | Yes |
| 24 | No rows, new version fails the filter | `0` rows (empty result). | Yes |
| 25 | (b) Child insertion succeeds, compatible KEY SHARE | (b) T2 succeeds immediately without blocking. | Yes |
| 26 | (d) 55P03 immediately | (d) T2 fails immediately with lock-not-available (`55P03`). | Yes |
| 27 | 1 updated. Row 1 closed, row 2 open | `1` row updated; row 1 is `'closed'` and row 2 is `'open'`. | Yes |
| 28 | 40001, conflicting key invisible in RR snapshot | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 29 | Step 8 gets 40001. Row 1 false, row 2 true | Step 8 fails with `40001`; final state is `(1, false), (2, true)`. | Yes |
| 30 | Step 4 commits, one dependency alone | Step 4 succeeds. | Yes |
| 31 | Both commit, 0 on call | Neither transaction fails; `0` doctors remain `on_call = true`. | Yes |
| 32 | (b) Step 8 gets 40001, both scans cover the table | (b) T2 fails at step 8 with `40001` because sequential scans took relation-level predicate locks. | Yes |
| 33 | Next sequence value after the rolled-back insert (2 for a new default sequence) | `2` | Conditional |
| 34 | Commits immediately, ordinary reader is compatible | Step 3 commits immediately (does not block). | Yes |
| 35 | COMMIT reports ROLLBACK, no user rows | Step 4 rolls back the transaction; `users` is empty (0 rows). | Yes |
| 36 | 23 to the writer, 3 to the other session | Step 3 returns `23`; step 4 returns `3`. | Yes |
| 37 | Completes immediately on the other row | Step 3 completes immediately (does not block). | Yes |
| 38 | (10,99) is always impossible. If T2 commits after T1 has taken its snapshot, (99,99) is impossible too | (c) `(10, 99)` | Conditional |
| 39 | 240, the sum of 100 and 140 | `240` | Yes |
| 40 | (b) Atomic same-row increment | (b) `UPDATE posts SET views = views + 1 WHERE id = $1;` | Yes |
| 41 | One row (1) from T2 | `(1)` | Yes |
| 42 | ('a',2) from T2 | `('a', 2)` | Yes |
| 43 | 3, T2 locks the updated row with 4 | `3` | Yes |
| 44 | Wait, then 23503 after the parent deletion commits | T2 blocks at step 3; when step 4 commits, T2 fails with a foreign-key violation (`23503`). | Yes |
| 45 | (b) DDL waits, later conflicting requests queue | (b) `ALTER TABLE` waits in the lock queue for `ACCESS EXCLUSIVE`, and every new `SELECT` and `INSERT` queues behind it. | Yes |
| 46 | (c) Consistent lock order and (d) independent single-row autocommits both remove this deadlock. Only (c) preserves transfer atomicity | (c) Always lock or update the smaller account `id` before the larger account `id`. | Incomplete |
| 47 | T2 proceeds on row 2, T3 waits on row 1 | Only T3 blocks; T2 completes immediately. | Yes |
| 48 | 1. SELECT 1 established the snapshot | `1` | Yes |
| 49 | T1 resumes, writes and commits 150 | T1 unblocks and succeeds (no `40001`); after step 7, `bal` is `150`. | Yes |
| 50 | 200, one snapshot sees 100 plus 100 | `200` | Yes |
| 51 | Only T3 waits, shared lockers coexist | Only T3 blocks; T1 and T2 both proceed without blocking. | Yes |
| 52 | Only (2,false), invisible to the DELETE | `(2, false)` | Yes |
| 53 | 2 rows, no unique index or write conflict | `2` rows (two duplicate `(1, 9)` rows). | Yes |
| 54 | Step 4 gets 40001. Only ('x',1) remains | T1 succeeds (0 rows inserted, no `40001`); `kv` contains `('x', 1)`. | No |
| 55 | Commit succeeds, T2 only locked the row | Step 5 succeeds (`bal` is `150`, no `40001`). | Yes |
| 56 | Step 7 gets 40001 on insertion. Rows (2,10) and (1,9) | Fails at step 7 (`INSERT`) with `40001`; `bookings` contains `(2, 10)` and `(1, 9)`. | Yes |
| 57 | Step 5 gets 40001, stale read would close the dependency chain through committed T1 | Step 5 fails with `40001` (`could not serialize access due to read/write dependencies among transactions`). | Yes |
| 58 | Both commit on disjoint indexed rows under the page assumption | Both T1 and T2 commit cleanly. | Yes |
| 59 | (c) The mixed isolation protocol permits a violation | (c) Yes, because `READ COMMITTED` transactions do not participate in SSI read/write dependency tracking. | Yes |
| 60 | (b) 25P02 in the still-aborted block | (b) The retried `UPDATE` fails with `25P02` because the transaction block is aborted. | Yes |
| 61 | 160 on row 1, 200 on row 2 | Row 1 is `160`; row 2 is `200`. | Yes |
| 62 | 40001, same stored value still has a new tuple version | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 63 | (1,100), the sort precedes locking and recheck | `(1, 100)` | Yes |
| 64 | 1, counts only the unlocked row | `1` | Yes |
| 65 | 70, locking read follows T1's committed update | `70` | Yes |
| 66 | 2, row 1 no longer qualifies so LIMIT seeks the next row | `2` | Yes |
| 67 | 40, old sum 120 divided by new count 3 | `40` | Yes |
| 68 | 2, SET TRANSACTION READ ONLY does not pin a data snapshot | `2` | Yes |
| 69 | First SELECT waits. Initial snapshot unsafe, fresh one reads y=20, x=10 | T3 blocks at step 3 until step 4 commits, then reads `y = 20` and `x = 10` with no error. | Yes |
| 70 | 2 if there are no other sequence consumers between attempts, otherwise the next available value | `2` | Yes |
| 71 | 40001 on the locking read of the changed tuple | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 72 | Lock upgrades deadlock, one 40P01, survivor proceeds | Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other complete. | Yes |
| 73 | 30, the pre-savepoint 50 survives and T2 subtracts 20 | `30` | Yes |
| 74 | Succeeds, ('a',2), first RR snapshot after T1 commit | Step 5 succeeds (no `40001`); `kv` contains `('a', 2)`. | Yes |
| 75 | Step 8 gets 40001 due to coarse SIREAD conflicts | Step 8 fails with `40001` (`could not serialize access due to read/write dependencies among transactions`). | Yes |
| 76 | Completes immediately, idle BEGIN holds no lock on items | Step 2 finishes immediately (does not block). | Yes |
| 77 | T2's locking SELECT gets 40001 after T1 commits | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 78 | Unique-key waits deadlock, one 40P01 | Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other proceed. | Yes |
| 79 | 0 rows updated, balances 50 and 100 | Step 3 updates `0` rows; final balances are `(1, 50)` and `(2, 100)`. | Yes |
| 80 | (1,10) and (3,20) for a fresh sequence, otherwise first and third sequence values | `(1, 10)` and `(3, 20)`. | Conditional |
| 81 | Both commit, only T1 reads a value later overwritten by T2 | Both T1 and T2 commit cleanly. | Yes |
| 82 | 2, uncommitted changed row skipped | `2` (no `40001`). | Yes |
| 83 | (c) 55P03 if the lock is still held after 1s. If released sooner DDL can succeed | (c) After 1 second, `ALTER TABLE` aborts cleanly instead of blocking all incoming queries in the lock queue for 10 minutes. | Conditional |
| 84 | 23505, plain unique check sees the committed duplicate | `23505` (`unique_violation`). | Yes |
| 85 | (c) Step 4 gets 40001 after T2 commits | (c) Step 4 fails immediately after step 5 with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 86 | 2, no tuple existed to lock | `2` rows (two duplicate `(1, 9)` rows). | Yes |
| 87 | T1 succeeds after rollback to savepoint, balance 150 | T1 succeeds (no `40001`); `bal` for `id = 1` is `150`. | Yes |
| 88 | One 40P01 from cross-parent waits, survivor proceeds | Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other proceed. | Yes |
| 89 | 40001 after the wait, T2 already acquired its snapshot | T2 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 90 | Completes immediately, table lock acquired in subtransaction was released | Step 5 completes immediately (does not block). | Yes |
| 91 | 40001 for a stale overlapping snapshot, but both can succeed if the second reads after the first commit | (b) Instead of silently losing one update, the second request fails with `40001` and returns an error to the caller. | No, as a guarantee |
| 92 | 2 for T2, 1 for T3 after rollback | Step 3 (T2) returns `2`; step 4 (T3) returns `1`. | Yes |
| 93 | T2 commits, T1 rolled back before commit check | Step 8 succeeds. | Yes |
| 94 | (100,50), table scan sees snapshot, CTE output sees RETURNING | `table_bal = 100, updated_bal = 50` | Yes |
| 95 | Succeeds, parent KEY SHARE caused no new data version | Step 4 succeeds (no `40001`). | Yes |
| 96 | 40001 on first ordered candidate, changed since snapshot | Step 4 fails with `40001` (`could not serialize access due to concurrent update`). | Yes |
| 97 | (c) RC reader adds no SSI dependency, ordinary serializable reader may add one, deferrable report uses a safe snapshot | (c) Running the analytics job at `READ COMMITTED` causes no SSI `40001` failures; switching it to plain `SERIALIZABLE` can trigger `40001` failures via a relation-level predicate lock, whereas `SERIALIZABLE READ ONLY DEFERRABLE` avoids `40001`. | Yes |
| 98 | Immediate, ('x',10), ('y',20). No active writer at first snapshot | Step 5 returns immediately (does not block) with `('x', 10), ('y', 20)`. | Yes |
| 99 | (c) if all three statements share one RC transaction. In separate autocommit statements the parent lock is gone before the sum check | (c) Lock the user's parent row with `SELECT 1 FROM users WHERE id = $u FOR UPDATE`, then check `sum(bal)` and `UPDATE` the chosen `acct_id`. | Conditional |
| 100 | Two sends assuming the calls succeed. ID is second allocated value, 2 only with a fresh sequence and no intervening allocation | `2` welcome emails are sent, and `id = 2` is stored in `users`. | Conditional |

## Trace qualifications

- **Visibility and row locks.** Q9 says “plain `SELECT` takes no locks”. Q86 says empty locking reads “acquire *zero* locks”. The results, 9 and two rows respectively, are correct. Q9 takes an `ACCESS SHARE` table lock. Q86 takes a `ROW SHARE` table lock even though it finds zero tuples to lock. Q25 correctly relies on compatibility between the foreign key’s `FOR KEY SHARE` and the parent’s non-key update. [PostgreSQL 16 lock modes](https://www.postgresql.org/docs/16/explicit-locking.html)
- **When a change commits.** Q20 says “Step 5 updates row `1` and commits” and Q53 says “Step 5 inserts `(1, 9)` and commits”. In both artifacts step 5 performs the write and step 6 commits it. Neither final count changes.
- **SSI.** Q29 says “At step 8, SSI sees the committed cycle”; Q32 and Q75 use the same explanation. In these two-transaction schedules, T1’s precommit check can mark T2 for abort at step 7. T2 reports the error at step 8. Q56 differs because T1 already committed when T2 makes the second conflicting insert. In Q57 the two read-before-write edges form a chain. The read of T2’s committed value supplies the third ordering constraint that makes the serial order impossible. Q69’s deferrable reader waits at its first query, rejects the unsafe candidate snapshot, and can then see T1’s committed update. Q98 takes its first snapshot after both writers finish. [PostgreSQL 16 SSI implementation](https://github.com/postgres/postgres/blob/REL_16_STABLE/src/backend/storage/lmgr/predicate.c)
- **Read Committed rechecks.** Q23’s maximum comes from the original statement snapshot. Q63 keeps the originally chosen ordering position while returning the updated priority. Q66 scans on to row 2 when row 1 no longer qualifies. Q79 can drop row 1 but cannot admit row 2, which failed the original snapshot filter. [PostgreSQL 16 locking reads](https://www.postgresql.org/docs/16/sql-select.html#SQL-FOR-UPDATE-SHARE) · [Isolation](https://www.postgresql.org/docs/16/transaction-iso.html)
- **Savepoints and snapshots.** In Q73 the first update survives the savepoint rollback. In Q87 rolling back the subtransaction releases its row-1 lock at step 5. T1 may resume before T2’s top-level commit at step 6. Its final balance is still 150. In Q48 even a constant `SELECT 1` takes the Repeatable Read snapshot. In Q68 the transaction-setting command leaves that snapshot for the subsequent `SELECT`. [PostgreSQL 16 lock lifetimes](https://www.postgresql.org/docs/16/explicit-locking.html) · [Transaction characteristics](https://www.postgresql.org/docs/16/sql-set-transaction.html)
- **Q38 and Q99 wording.** Q38’s “While T1 runs step 1” does not support its trace’s “If step 1 starts after T2 commits”. The mixed tuple is impossible for either snapshot, but a commit explicitly after snapshot acquisition would also rule out the all-new tuple. For Q99(c), place the parent lock, subsequent aggregate, and guarded withdrawal in one explicit Read Committed transaction, and require every withdrawal to use that protocol. Otherwise the stated autocommit default releases the parent lock before the balance check. [PostgreSQL 16 BEGIN](https://www.postgresql.org/docs/16/sql-begin.html)

The separate Claude run tested the same prompt version and reported 12 Pass, 2 Borderline and 1 Fail on this input, with coverage as its failure. It is a cross-model comparison, not a prompt-version promotion test. This Gemini sample supplies an additional correctness regression to retest. [Earlier input-3 scores](../../v0.2.0/scores.md)

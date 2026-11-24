# Answer key

## Mechanisms

1. Uncommitted changes stay hidden (no dirty reads; `READ UNCOMMITTED` behaves as `READ COMMITTED`): 1, 21, 36
2. MVCC: readers do not block writers and writers do not block readers: 2, 34, 83
3. Transaction-block error abortion (`25P02` until `ROLLBACK`, and `COMMIT` rolls back): 3, 35, 60, 80
4. Own-write visibility and intra-statement snapshot stability (including data-modifying CTEs): 4, 36, 38, 94
5. Row-level write locks block concurrent writers on the same row until commit or rollback: 5, 37, 87
6. `READ COMMITTED` takes a fresh snapshot per statement (non-repeatable reads and read skew): 6, 39, 65
7. Phantom reads and shifting aggregates in `READ COMMITTED`: 7, 67
8. Write re-evaluation after waiting (`EvalPlanQual` / EPQ) in `READ COMMITTED`: 8, 22, 73, 79
9. EPQ scope limits (re-evaluates only the locked target row, not new rows or uncorrelated subqueries): 23, 61, 79
10. Read-modify-write lost updates vs atomic `UPDATE` expressions: 9, 40, 91
11. Unique-index checks block on uncommitted inserts (commit -> `23505`, rollback -> succeeds): 10, 41, 78, 84
12. `INSERT ... ON CONFLICT` waits for uncommitted writers before updating, skipping, or inserting: 11, 42, 74, 89
13. `SELECT ... FOR UPDATE` locks rows against writers without blocking plain `SELECT`: 12, 43, 65, 71, 77, 86, 92, 96, 99
14. `FOR UPDATE` in `READ COMMITTED` re-checks `WHERE` after waiting (and does not re-sort): 24, 63, 66, 92, 96
15. `NOWAIT` fails immediately (`55P03`); `SKIP LOCKED` skips currently locked rows: 13, 26, 64, 82, 92
16. Row lock compatibility (`FOR SHARE`, `FOR NO KEY UPDATE`, `FOR KEY SHARE`) and foreign keys: 25, 44, 51, 72, 88, 95
17. Deadlocks and cycle abort (`40P01`), prevented by consistent lock ordering: 14, 46, 72, 78, 88
18. Savepoints (`ROLLBACK TO SAVEPOINT`) undo post-savepoint work, clear aborted state, and release post-savepoint locks: 15, 47, 73, 80, 87, 90
19. DDL `ACCESS EXCLUSIVE` waits for open readers (`ACCESS SHARE`) and queues new queries behind it: 16, 45, 76, 83, 90
20. `REPEATABLE READ` (and `SERIALIZABLE`) freezes its snapshot at the first query/DML statement, not at `BEGIN`: 17, 48, 68, 74, 76, 89, 98
21. Consistent reads and no phantom reads in PostgreSQL `REPEATABLE READ` (Snapshot Isolation): 18, 50, 84
22. First-committer-wins (`40001`) on concurrent row modifications in `REPEATABLE READ` (but not on rollbacks or lock-only transactions): 19, 49, 55, 62, 71, 82, 85, 87, 91, 95, 96
23. Newly inserted rows are invisible to `REPEATABLE READ` `UPDATE`/`DELETE` scans (no `40001`): 27, 52, 86
24. Write skew is allowed in `REPEATABLE READ` (disjoint writes after overlapping reads): 20, 53, 77, 86, 99
25. `ON CONFLICT` in `REPEATABLE READ`: `DO UPDATE` raises `40001` on post-snapshot commits, while `DO NOTHING` skips cleanly: 28, 54, 74, 89
26. `SERIALIZABLE` (SSI) detects rw-antidependency cycles without blocking reads (`40001`): 29, 56, 75, 81, 85, 93, 97, 98, 100
27. One-way rw-dependencies and disjoint indexed operations succeed under `SERIALIZABLE`: 30, 58, 81
28. SSI requires every participating transaction to run at `SERIALIZABLE`: 31, 59, 97
29. SSI false positives (sequential scans / coarse predicate locks) and `READ ONLY DEFERRABLE`: 32, 57, 69, 75, 97, 98
30. Non-transactional sequences (`SERIAL`/`nextval`), external side effects, and full-transaction retries on `40001`: 33, 60, 70, 80, 91, 100

## Answers

### 1.
**Why:** 1. T1 opens a transaction and writes a new row version `(1, 50)`, but has not committed. 2. Under PostgreSQL's isolation rules, uncommitted changes are never visible to other transactions (no *dirty reads*—reading data another transaction has not committed). 3. When T2 runs `SELECT`, its *snapshot* (the set of committed transactions visible to it) sees only the previously committed version `(1, 100)`.
**Answer:** `100`
**The trap:** Answering `50`, from imagining the table has a single in-place cell that `UPDATE` overwrites immediately for every session.
**Rule:** Other transactions never see a transaction's writes until it commits.

### 2.
**Why:** 1. T1's `UPDATE` writes a new row version and takes a row lock on `id = 1`. 2. PostgreSQL uses *MVCC* (Multi-Version Concurrency Control), keeping the old committed version `(1, 100)` alongside the new uncommitted version `(1, 50)`. 3. Because plain `SELECT` reads the committed version from its snapshot without acquiring row locks, writers never block readers. 4. T2 returns `100` right away.
**Answer:** (b) T2 returns `100` immediately without blocking.
**The trap:** (a), from assuming an `UPDATE` lock blocks all readers until commit (true in lock-based engines, not MVCC); (c) expects a dirty read; (d) assumes PostgreSQL throws an error on concurrent access instead of reading the snapshot.
**Rule:** Under MVCC, plain `SELECT` never waits for an uncommitted `UPDATE` or `DELETE`.

### 3.
**Why:** 1. Step 2 inserts `(1)` inside T1's open transaction. 2. Step 3 (`1 / 0`) raises a division-by-zero error, which puts the entire transaction block into an aborted state. 3. In an aborted transaction block, PostgreSQL rejects every later statement—steps 4 and 5 fail immediately with `25P02` (`current transaction is aborted`). 4. Step 6 (`COMMIT`) does not commit partial work; it ends the failed block by rolling everything back, including `(1)`.
**Answer:** Empty table (0 rows).
**The trap:** Answering `(1)` or `(1), (2), (3)`, from assuming statements before or after an error inside `BEGIN ... COMMIT` still commit.
**Rule:** Any unhandled error inside `BEGIN` aborts the entire transaction block so nothing commits.

### 4.
**Why:** 1. Step 1 inserts `(1)` and `(2)` and autocommits. 2. Step 2 (`INSERT ... SELECT`) takes a single snapshot (and *command ID* boundary) when the statement begins, containing only `(1)` and `(2)`. 3. As step 2 inserts `(10)` and `(20)`, those newly written rows are stamped with the current statement's command ID and are invisible to the same statement's scan, preventing infinite recursion.
**Answer:** `1, 2, 10, 20` (4 rows).
**The trap:** Predicting an infinite loop, from thinking a statement immediately reads back rows it is currently inserting.
**Rule:** A single SQL statement reads one fixed snapshot from before it began and never sees its own writes while executing.

### 5.
**Why:** 1. Step 2 locks row `id = 1` exclusively until T1 ends. 2. At step 3, T2 tries to update the same row, hits T1's row lock, and blocks waiting for T1 to finish. 3. At step 4, T1 rolls back, discarding `qty = 9` and releasing the lock. 4. T2 wakes up, sees the original row `(1, 10)`, updates `qty` to `8`, and autocommits.
**Answer:** T2 blocks at step 3 until step 4 rolls back; afterward `qty` is `8`.
**The trap:** Thinking T2 overwrites `9` immediately without waiting, or fails with a lock error on conflict.
**Rule:** Concurrent `UPDATE` or `DELETE` statements on the same row wait until the first writer commits or rolls back.

### 6.
**Why:** 1. T1 uses default `READ COMMITTED`, which takes a fresh snapshot at the start of every statement. 2. Step 2 starts before T2 runs, so it sees `100`. 3. Step 3 runs outside `BEGIN`, so T2 updates `bal` to `200` and autocommits immediately. 4. Step 4 starts after T2 committed, takes a new snapshot, and reads `200`—a *non-repeatable read*.
**Answer:** Step 2 returns `100`; step 4 returns `200`.
**The trap:** Answering `100` for both, from believing `BEGIN` freezes what a transaction sees until `COMMIT`.
**Rule:** In `READ COMMITTED`, each statement sees all commits that finished before that statement started.

### 7.
**Why:** 1. T1 runs in `READ COMMITTED`. Step 2 sees the two initial `'new'` rows and returns `2`. 2. Step 3 inserts row `3` (`'new'`) and autocommits. 3. Step 4 starts a new statement and therefore takes a fresh snapshot that includes T2's committed insert—a *phantom read* (a newly inserted row appearing in a repeated query).
**Answer:** `3`
**The trap:** Answering `2`, from assuming `WHERE` matches or `count(*)` remain fixed inside `BEGIN ... COMMIT`.
**Rule:** In `READ COMMITTED`, repeated range queries and aggregates include rows committed by other transactions in between.

### 8.
**Why:** 1. Step 2 updates `id = 1` from `100` to `20` and holds its row lock. 2. Step 3 (`READ COMMITTED`) matches `(1, 100)` in its snapshot and blocks on T1's lock. 3. Step 4 commits `bal = 20`. 4. T2 wakes up and runs *EvalPlanQual* (EPQ): PostgreSQL re-fetches the latest committed version `(1, 20)` and re-evaluates `WHERE id = 1 AND bal >= 80`. 5. Because `20 >= 80` is now false, T2 skips the row and updates 0 rows.
**Answer:** Step 3 updates `0` rows; final `bal` is `20`.
**The trap:** Predicting `bal = -60` (re-evaluating `SET` without re-checking `WHERE`), `bal = 20` with 1 row updated, or an error—forgetting that EPQ re-checks `WHERE` against the committed row.
**Rule:** When a waiting `UPDATE` in `READ COMMITTED` unblocks after a commit, PostgreSQL re-fetches the committed row and skips it if `WHERE` is now false.

### 9.
**Why:** 1. Both T1 and T2 read `stock = 10` (steps 3–4); plain `SELECT` takes no locks. 2. Each computes `10 - 1 = 9` in application code. 3. Step 5 updates `stock` to literal `9`, and step 6 commits. 4. Step 7 runs after T1 committed, finds `id = 1` unlocked, and sets `stock` to literal `9` again—a *lost update*—and step 8 commits cleanly.
**Answer:** `stock` is `9`; neither transaction fails.
**The trap:** Expecting `stock = 8` or an error, from believing wrapping `SELECT` and `UPDATE` in `BEGIN ... COMMIT` automatically prevents lost updates.
**Rule:** A plain `SELECT` followed by `UPDATE ... SET x = <literal>` in `READ COMMITTED` silently overwrites concurrent changes.

### 10.
**Why:** 1. Even though T1's row `(1)` is uncommitted and invisible to normal reads, primary-key and unique constraints are enforced immediately via the shared B-tree index. 2. At step 3, T2 sees T1's uncommitted index entry for `1` and cannot know yet whether T1 will commit or roll back. 3. Therefore T2 blocks waiting on T1's transaction.
**Answer:** (a) T2 blocks until T1 commits or rolls back.
**The trap:** (b) assumes a duplicate error is raised immediately without waiting for a possible rollback; (c) and (d) assume MVCC invisibility lets both inserts proceed unchecked until `COMMIT`.
**Rule:** Inserting a key held by an uncommitted transaction blocks until that writer commits (`23505`) or rolls back (succeeds).

### 11.
**Why:** 1. T1 inserts `('a', 1)` without committing, placing an uncommitted entry in the primary-key index. 2. At step 3, T2's `INSERT ... ON CONFLICT` sees that uncommitted entry and blocks until T1 finishes. 3. At step 4, T1 commits `('a', 1)`. 4. T2 wakes up, sees the committed conflict on `'a'`, and executes `DO UPDATE` against the committed row: `v = 1 + 2 = 3`.
**Answer:** `('a', 3)`
**The trap:** Answering `('a', 2)` or a duplicate-key error, from believing `ON CONFLICT` decides insert-vs-update using only its initial empty snapshot without waiting on uncommitted inserts.
**Rule:** `INSERT ... ON CONFLICT` blocks on concurrent uncommitted inserts of the same key, then runs its conflict action against the committed row.

### 12.
**Why:** 1. `SELECT ... FOR UPDATE` at step 2 acquires an exclusive row lock on `id = 1` held until T1 ends. 2. Under MVCC, plain `SELECT` (step 3) does not acquire row locks, so T2 reads the committed snapshot `'open'` without waiting. 3. T3's `UPDATE` (step 4) needs a row write lock on `id = 1`, which conflicts with T1's `FOR UPDATE` lock, so T3 blocks.
**Answer:** (c) Only T3 blocks; T2 returns `'open'` immediately.
**The trap:** (a) assumes `FOR UPDATE` locks out plain readers too; (b) forgets `FOR UPDATE` locks the row against writers; (d) reverses reader and writer locking.
**Rule:** `SELECT ... FOR UPDATE` blocks concurrent writers and other row-locking queries on that row, never plain `SELECT`s.

### 13.
**Why:** 1. Step 2 holds an exclusive `FOR UPDATE` lock on row `1`. 2. Step 3 scans `'open'` rows ordered by `id`, hits row `1`, sees it is currently locked, and because of `SKIP LOCKED`, skips row `1` instead of waiting. 3. It moves to row `2`, which is unlocked, acquires a `FOR UPDATE` lock on row `2`, and returns `2` (`LIMIT 1`).
**Answer:** `2`
**The trap:** Predicting T2 blocks on row `1`, returns `1`, or returns 0 rows—forgetting that `SKIP LOCKED` bypasses locked rows and keeps scanning to fill `LIMIT`.
**Rule:** `FOR UPDATE SKIP LOCKED` ignores currently locked rows and locks the next available matching rows without waiting.

### 14.
**Why:** 1. Step 3 locks row `1` for T1; step 4 locks row `2` for T2. 2. Step 5 makes T1 wait for T2's lock on row `2`. 3. Step 6 makes T2 wait for T1's lock on row `1`, forming a wait-for cycle—a *deadlock*. 4. After `deadlock_timeout` (1s), PostgreSQL's deadlock detector finds the cycle and aborts one transaction with SQLSTATE `40P01`, releasing its lock so the survivor finishes.
**Answer:** (b) PostgreSQL detects the cycle and aborts one transaction with `40P01`, allowing the other to proceed.
**The trap:** (a) confuses `lock_timeout = 0` with disabling deadlock detection; (c) thinks both transactions must die; (d) assumes PostgreSQL can silently replay aborted SQL transactions.
**Rule:** PostgreSQL automatically detects deadlocks and aborts one transaction (`40P01`) so the other can continue.

### 15.
**Why:** 1. Step 2 inserts `(1)`. 2. Step 3 creates a *savepoint* `sp` (marking a subtransaction boundary). 3. Step 4 inserts `(2)`, and step 5 (`1 / 0`) aborts the subtransaction. 4. Step 6 (`ROLLBACK TO SAVEPOINT sp`) undoes everything after `sp` (removing `(2)`) and clears the aborted transaction state while preserving `(1)`. 5. Step 7 inserts `(3)`, and step 8 commits both `(1)` and `(3)`.
**Answer:** `1` and `3`
**The trap:** Answering empty table (thinking `1 / 0` killed the whole transaction despite the savepoint) or `1, 2, 3` (forgetting `ROLLBACK TO SAVEPOINT` undoes `(2)`).
**Rule:** `ROLLBACK TO SAVEPOINT` undoes changes after the savepoint and restores the transaction so earlier work can still commit.

### 16.
**Why:** 1. Step 2's `SELECT` acquires an `ACCESS SHARE` table lock on `items`, held until T1 commits or rolls back. 2. Step 3 (`ALTER TABLE`) requires an `ACCESS EXCLUSIVE` lock, which conflicts with `ACCESS SHARE`, so T2 blocks waiting for T1. 3. Step 4's `SELECT` also needs `ACCESS SHARE`; even though `ACCESS SHARE` is compatible with T1, PostgreSQL queues new lock requests behind a waiting conflicting lock (`ACCESS EXCLUSIVE`), so T3 blocks behind T2.
**Answer:** (c) T2 blocks on T1, and T3 blocks behind T2.
**The trap:** (b) assumes new `SELECT`s can jump ahead of a waiting `ALTER TABLE` because they don't conflict with T1; (a) thinks `SELECT` takes no table lock; (d) expects an immediate error when `lock_timeout = 0`.
**Rule:** A waiting `ACCESS EXCLUSIVE` DDL lock blocks behind open `SELECT` transactions and stalls every new query in the queue behind it.

### 17.
**Why:** 1. In `REPEATABLE READ`, PostgreSQL does not freeze the transaction's snapshot at `BEGIN` (step 1); it freezes the snapshot at the start of the first non-transaction-control statement. 2. Step 2 updates `n` to `5` and autocommits before T1 has run any query. 3. Step 3 is T1's first query, so T1 takes its snapshot now and sees `5`.
**Answer:** `5`
**The trap:** Answering `0`, from believing `BEGIN ISOLATION LEVEL REPEATABLE READ` captures the snapshot immediately.
**Rule:** `REPEATABLE READ` takes its transaction snapshot at the first query or write statement, not at `BEGIN`.

### 18.
**Why:** 1. Step 2 is T1's first statement in `REPEATABLE READ`, so it freezes T1's snapshot containing rows `1` and `2`. 2. Step 3 inserts row `3` and autocommits after that snapshot. 3. Because PostgreSQL implements `REPEATABLE READ` via Snapshot Isolation, step 4 reads from the exact same snapshot and does not see row `3`—PostgreSQL prevents phantom reads in `REPEATABLE READ`.
**Answer:** `2`
**The trap:** Answering `3`, from recalling the SQL standard's minimum matrix (which permits phantom reads at `REPEATABLE READ`) rather than PostgreSQL's stronger Snapshot Isolation implementation.
**Rule:** In PostgreSQL `REPEATABLE READ`, every query in the transaction sees the same snapshot, preventing both non-repeatable and phantom reads.

### 19.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with `(1, 100)`. 2. Step 3 updates row `1` to `200` and commits after T1's snapshot. 3. At step 4, T1 tries to update row `1`, sees that row `1` was modified by a transaction committed after T1's snapshot, and enforces *first-committer-wins*: unlike `READ COMMITTED`, `REPEATABLE READ` cannot silently re-evaluate against newer data, so it aborts T1 with SQLSTATE `40001`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Predicting `bal = 210` (expecting `READ COMMITTED` EPQ behavior) or `bal = 110` (expecting T1 to overwrite T2's committed `200`).
**Rule:** In `REPEATABLE READ`, attempting to update or delete a row already modified and committed after your snapshot raises `40001`.

### 20.
**Why:** 1. Both T1 and T2 freeze `REPEATABLE READ` snapshots at steps 3–4 showing both doctors on call (`count = 2`). 2. Step 5 updates row `1` and commits; step 7 updates row `2`. 3. Because T1 and T2 modified *disjoint* rows, first-committer-wins sees no row conflict, so step 8 also commits—classic *write skew* (two transactions read overlapping data and make disjoint writes that together break an invariant).
**Answer:** `0`
**The trap:** Expecting step 7 or 8 to fail with `40001`, from assuming `REPEATABLE READ` prevents all multi-row concurrency anomalies.
**Rule:** `REPEATABLE READ` checks conflicts only on shared modified rows, so write skew across disjoint rows commits cleanly.

### 21.
**Why:** 1. PostgreSQL accepts `READ UNCOMMITTED` for SQL compatibility, but internally treats it identically to `READ COMMITTED`. 2. Step 2's update to `500` is uncommitted. 3. Step 3 reads from a `READ COMMITTED` snapshot and sees only the last committed value `100`.
**Answer:** `100`
**The trap:** Answering `500`, from assuming `READ UNCOMMITTED` enables dirty reads in PostgreSQL as it does in some other databases.
**Rule:** PostgreSQL has no dirty reads; `READ UNCOMMITTED` runs as `READ COMMITTED`.

### 22.
**Why:** 1. Step 2 sets `bal = 150` (uncommitted) and locks row `1`. 2. Step 3 (`READ COMMITTED`) blocks on row `1`. 3. Step 4 commits `bal = 150`. 4. T2 wakes up and EPQ re-fetches the committed row `(1, 150)`, evaluates `WHERE id = 1` (true), and computes `SET bal = bal * 2` using the committed `150`, storing `300`.
**Answer:** `300`
**The trap:** Answering `200` (applying `* 2` to the pre-wait `100` and losing T1's `+ 50`) or `250` (reversing the order).
**Rule:** After waiting in `READ COMMITTED`, an `UPDATE`'s `SET` expressions evaluate against the newly committed row values, not pre-wait snapshot values.

### 23.
**Why:** 1. Step 2 locks row `1` with uncommitted `price = 50`. 2. At step 3, T2's uncorrelated scalar subquery `(SELECT max(price) FROM items)` runs once against T2's pre-wait snapshot (`10` and `20`), producing `20`. 3. T2 then tries to update row `1` and blocks on T1. 4. When T1 commits `50` at step 4, EPQ re-fetches only the locked target row (`id = 1`) to re-check `WHERE id = 1`—it does *not* re-run the uncorrelated subquery, so it writes the cached `20`.
**Answer:** `20`
**The trap:** Answering `50`, from assuming EPQ re-executes the entire `UPDATE` statement and its subquery from scratch after waiting.
**Rule:** In `READ COMMITTED`, EPQ re-evaluates only the locked target row, not uncorrelated subqueries computed from the statement's original snapshot.

### 24.
**Why:** 1. Step 2 sets row `1` to `'claimed'` (uncommitted) and holds its row lock. 2. Step 3 (`READ COMMITTED`) sees `(1, 'open')` in its snapshot, tries to lock row `1` `FOR UPDATE`, and blocks on T1. 3. Step 4 commits `'claimed'`. 4. T2 wakes up, EPQ re-fetches committed `(1, 'claimed')`, re-checks `WHERE status = 'open'` (now false), and drops row `1`.
**Answer:** `0` rows (empty result).
**The trap:** Answering `1`, from thinking `SELECT ... FOR UPDATE` returns rows that matched `WHERE` before waiting even if the blocking transaction changed them.
**Rule:** Like `UPDATE`, `SELECT ... FOR UPDATE` in `READ COMMITTED` re-checks `WHERE` against the committed row after waiting and drops rows that no longer match.

### 25.
**Why:** 1. At step 2, T1 updates `name`, which is not part of `parents`'s primary key or any unique constraint; PostgreSQL therefore acquires a weaker `FOR NO KEY UPDATE` lock rather than `FOR UPDATE`. 2. At step 3, the foreign-key check on `children.parent_id` acquires a `FOR KEY SHARE` lock on parent row `1`. 3. `FOR NO KEY UPDATE` and `FOR KEY SHARE` are compatible, so T2 inserts and commits immediately.
**Answer:** (b) T2 succeeds immediately without blocking.
**The trap:** (a) assumes any `UPDATE` on a parent row blocks concurrent child inserts; (c) and (d) confuse non-key updates with deleting the parent key.
**Rule:** Updating non-key columns acquires `FOR NO KEY UPDATE`, which does not block foreign-key `FOR KEY SHARE` checks from child inserts.

### 26.
**Why:** 1. Step 2 holds a `FOR UPDATE` row lock on `id = 1`. 2. Step 3 requests `FOR UPDATE NOWAIT` on the same row. 3. Instead of waiting for T1 to release the lock, `NOWAIT` fails immediately with SQLSTATE `55P03` (`lock_not_available`).
**Answer:** (d) T2 fails immediately with lock-not-available (`55P03`).
**The trap:** (a) confuses `NOWAIT` with `SKIP LOCKED`; (b) thinks `NOWAIT` downgrades to an unlocked read; (c) forgets `NOWAIT` overrides waiting.
**Rule:** `FOR UPDATE NOWAIT` raises an immediate `55P03` error if any target row is already locked.

### 27.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot containing only row `1`. 2. Step 3 inserts and commits row `2` after T1's snapshot. 3. Step 4 scans only rows visible in T1's snapshot—row `1`—updates it to `'closed'`, and never visits row `2`. 4. Because row `1` was not concurrently modified, no `40001` error occurs; row `2` remains `'open'`.
**Answer:** `1` row updated; row 1 is `'closed'` and row 2 is `'open'`.
**The trap:** Predicting `2` rows updated (thinking writes see newer commits than reads) or a `40001` error (thinking any concurrent insert into the `WHERE` range causes a serialization failure in `REPEATABLE READ`).
**Rule:** `UPDATE` and `DELETE` in `REPEATABLE READ` operate only on rows present in the snapshot and silently ignore concurrent inserts without raising `40001`.

### 28.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot showing an empty `kv` table. 2. Step 3 inserts and commits `('x', 1)` after T1's snapshot. 3. At step 4, T1's `INSERT` detects `'x'` in the unique index and switches to `ON CONFLICT DO UPDATE`. 4. Because `('x', 1)` was committed after T1's snapshot, `REPEATABLE READ` refuses to update an invisible row version and aborts T1 with `40001`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Expecting `('x', 2)` (assuming `ON CONFLICT DO UPDATE` works like `READ COMMITTED`) or `23505` (forgetting `ON CONFLICT` handled the key check before hitting the snapshot-update check).
**Rule:** In `REPEATABLE READ`, `INSERT ... ON CONFLICT DO UPDATE` fails with `40001` if the conflicting row was committed after the transaction's snapshot.

### 29.
**Why:** 1. Under `SERIALIZABLE` (*Serializable Snapshot Isolation*, SSI), steps 3 and 4 place non-blocking *SIRead* (predicate) locks on `doctors` without blocking writers. 2. Step 5 updates row `1` (recording an *rw-antidependency* `T2 -> T1`, meaning T2 read before T1 wrote). 3. Step 6 updates row `2` (recording `T1 -> T2`). 4. At step 7, T2 has not committed yet, so T1's `COMMIT` succeeds. 5. At step 8, SSI sees the committed cycle `T1 -> T2 -> T1` and aborts T2 with `40001`.
**Answer:** Step 8 fails with `40001`; final state is `(1, false), (2, true)`.
**The trap:** Predicting step 5 or 6 blocks (thinking `SERIALIZABLE` uses table locks), predicting both commit (confusing with `REPEATABLE READ`), or predicting step 7 fails.
**Rule:** PostgreSQL `SERIALIZABLE` tracks reads with non-blocking SIRead locks and aborts the second committer with `40001` when writes form an rw-cycle.

### 30.
**Why:** 1. Step 2 places an SIRead lock on row `1` for T1. 2. Step 3 updates row `1` and commits, creating a single one-way rw-antidependency `T1 -> T2` (T1 read old row `1` before T2 updated it). 3. T1 writes nothing, so no reverse dependency `T2 -> T1` exists. 4. The execution is equivalent to the serial order T1 then T2, so step 4 commits cleanly.
**Answer:** Step 4 succeeds.
**The trap:** Predicting `40001`, from believing any concurrent write to a row read by a `SERIALIZABLE` transaction triggers a serialization failure.
**Rule:** A one-way rw-dependency is serializable (reader before writer) and does not trigger `40001` under `SERIALIZABLE`.

### 31.
**Why:** 1. T1 runs at `SERIALIZABLE`, so SSI tracks T1's SIRead locks. 2. T2 runs at default `READ COMMITTED`, so PostgreSQL does *not* acquire SIRead locks or track SSI rw-dependencies for T2. 3. Step 5–6 commits `(1, false)` cleanly. 4. Step 7–8 updates row `2` to `false` and commits cleanly, leaving no doctors on call.
**Answer:** Neither transaction fails; `0` doctors remain `on_call = true`.
**The trap:** Expecting T1 or T2 to fail with `40001`, from assuming putting `SERIALIZABLE` on one transaction protects it against lower-isolation transactions.
**Rule:** SSI only detects anomalies among transactions that are *all* running at `SERIALIZABLE`.

### 32.
**Why:** 1. With no indexes, steps 3 and 4 run sequential scans on `items`, so each `SERIALIZABLE` transaction takes a relation-level SIRead lock on the entire table rather than individual rows. 2. Step 5 (`UPDATE id = 1`) conflicts with T2's table-wide SIRead lock (`T2 -> T1`). 3. Step 6 (`UPDATE id = 2`) conflicts with T1's table-wide SIRead lock (`T1 -> T2`). 4. Step 7 commits T1; step 8 sees the cycle and aborts T2 with `40001`—an SSI *false positive*.
**Answer:** (b) T2 fails at step 8 with `40001` because sequential scans took relation-level predicate locks.
**The trap:** (a) assumes SSI tracks exact `WHERE` predicates row-by-row even during sequential scans; (c) thinks SIRead locks block writers; (d) reverses which committer aborts.
**Rule:** Sequential scans in `SERIALIZABLE` take relation-level SIRead locks, so disjoint updates can still trigger `40001` false positives.

### 33.
**Why:** 1. `SERIAL` calls `nextval()` on a sequence object. 2. Sequences in PostgreSQL are non-transactional so concurrent inserts do not block each other waiting for commits. 3. Step 2 consumes sequence value `1`. 4. Step 3 rolls back the inserted row, but does *not* roll back the sequence counter. 5. Step 4 calls `nextval()` and receives `2`.
**Answer:** `2`
**The trap:** Answering `1`, from assuming `ROLLBACK` rewinds `SERIAL` / `IDENTITY` counters along with table rows.
**Rule:** Sequence advances (`nextval`) are never rolled back on `ROLLBACK` or error, so rolled-back inserts leave gaps.

### 34.
**Why:** 1. Step 2 runs a plain `SELECT`, which reads a committed snapshot under MVCC and acquires no row lock on `id = 1`. 2. Step 3's `UPDATE` needs a row lock on `id = 1`, finds none held, writes a new row version `(1, 200)`, and autocommits immediately.
**Answer:** Step 3 commits immediately (does not block).
**The trap:** Predicting step 3 blocks until T1 commits, from assuming an open transaction holding a `SELECT` locks the rows it read.
**Rule:** Under MVCC, plain `SELECT` never blocks concurrent `UPDATE` or `DELETE` statements.

### 35.
**Why:** 1. Step 2 inserts `(1)` inside T1's transaction. 2. Step 3 fails with unique violation (`23505`), immediately placing the transaction block into an aborted state. 3. Catching the error in application code does not clear PostgreSQL's aborted state. 4. When step 4 sends `COMMIT`, PostgreSQL rolls back the entire transaction (returning `ROLLBACK`), discarding step 2's row `(1)`.
**Answer:** Step 4 rolls back the transaction; `users` is empty (0 rows).
**The trap:** Expecting `(1)` to be committed, from thinking `COMMIT` saves all statements that succeeded before a caught error.
**Rule:** Once any statement errors inside `BEGIN`, `COMMIT` acts as `ROLLBACK` unless a savepoint rolled back the error first.

### 36.
**Why:** 1. Step 2 updates `t` to `(11)` and `(12)` inside T1's uncommitted transaction. 2. At step 3, T1 sees all changes made by earlier statements within its own transaction, returning `11 + 12 = 23`. 3. At step 4, T2 cannot see T1's uncommitted writes (no dirty reads), so T2 reads the committed `(1)` and `(2)`, returning `3`.
**Answer:** Step 3 returns `23`; step 4 returns `3`.
**The trap:** Answering `3` for step 3 (thinking uncommitted writes aren't visible even to yourself) or `23` for step 4 (thinking T2 sees T1's update).
**Rule:** A transaction always sees its own earlier statements' writes, while other transactions still see only committed data.

### 37.
**Why:** 1. Step 2 acquires a row-level lock only on `id = 1`. 2. Step 3 targets `id = 2`, which has no row lock held against it. 3. Because PostgreSQL locks modified rows individually rather than the whole table, step 3 updates row `2` and autocommits right away.
**Answer:** Step 3 completes immediately (does not block).
**The trap:** Predicting step 3 blocks until T1 commits, from assuming `UPDATE` locks the whole table.
**Rule:** `UPDATE` and `DELETE` take row-level locks, so concurrent writes to different rows do not block each other.

### 38.
**Why:** 1. Even in `READ COMMITTED`, a single SQL statement acquires one snapshot when it starts and uses that same snapshot for every table reference and subquery inside it. 2. If step 1 starts before T2 commits, both reads see `10` -> `(10, 10)`. 3. If step 1 starts after T2 commits, both reads see `99` -> `(99, 99)`. 4. Seeing `10` in one part and `99` in the other (`(10, 99)`) is impossible.
**Answer:** (c) `(10, 99)`
**The trap:** Thinking a commit arriving between evaluating the outer query and the subquery can split a single statement's view into `(10, 99)`. (a), (b), and (d) are all possible outcomes depending on whether T1 starts before or after T2 commits.
**Rule:** Every part of a single SQL statement executes against one consistent snapshot.

### 39.
**Why:** 1. T1 runs in `READ COMMITTED`, taking a fresh snapshot per statement. 2. Step 2 reads `id = 1` before T2 commits -> `100`. 3. Step 3 transfers `40` from row `1` to row `2` and commits (`60`, `140`). 4. Step 4 takes a new snapshot and reads `id = 2` -> `140`. 5. Summing `100 + 140` yields `240`—a *read skew* (observing half of a committed transaction).
**Answer:** `240`
**The trap:** Answering `200`, from assuming `BEGIN ... COMMIT` guarantees two separate `SELECT`s see a consistent cross-row total.
**Rule:** In `READ COMMITTED`, two separate `SELECT` statements can straddle a concurrent commit and observe inconsistent totals (read skew).

### 40.
**Why:** 1. In (b), a single atomic `UPDATE posts SET views = views + 1` locks the row; concurrent workers block, and once unblocked, EPQ re-fetches the committed `views` and adds `1`—no lost updates, no deadlocks, and no `40001` errors. 2. In (a) and (d), reading `views` into app code and writing a literal loses concurrent increments (and `READ UNCOMMITTED` is `READ COMMITTED`). 3. In (c), two workers can both acquire `FOR SHARE` and then deadlock (`40P01`) when both try to upgrade to `UPDATE`.
**Answer:** (b) `UPDATE posts SET views = views + 1 WHERE id = $1;`
**The trap:** Picking (a) from trusting `BEGIN ... COMMIT` to prevent lost updates, or (c) from thinking `FOR SHARE` safely serializes a read-then-write (it causes lock-upgrade deadlocks).
**Rule:** Relative updates like `SET x = x + 1` use EPQ in `READ COMMITTED` to avoid lost updates without deadlocks or serialization errors.

### 41.
**Why:** 1. Step 2 places an uncommitted unique-index entry for `1`. 2. Step 3 hits that entry and blocks waiting for T1. 3. Step 4 rolls back T1, aborting T1's entry and waking T2. 4. T2 re-checks the index, sees no committed `1`, inserts `(1)`, and autocommits.
**Answer:** `(1)`
**The trap:** Predicting step 3 already failed with `23505`, from forgetting PostgreSQL waits to see whether the first writer commits or rolls back.
**Rule:** When an uncommitted unique-key inserter rolls back, a waiting inserter of the same key unblocks and succeeds.

### 42.
**Why:** 1. Step 2 inserts `('a', 1)` uncommitted. 2. Step 3 (`ON CONFLICT DO NOTHING`) hits T1's uncommitted index entry for `'a'` and blocks until T1 finishes. 3. Step 4 rolls back T1, so `'a'` does not exist. 4. Step 5 wakes up, finds no committed conflict, inserts `('a', 2)`, and autocommits.
**Answer:** `('a', 2)`
**The trap:** Answering empty table (thinking `ON CONFLICT DO NOTHING` saw T1's uncommitted `'a'` and skipped immediately without waiting).
**Rule:** `ON CONFLICT DO NOTHING` waits for concurrent uncommitted inserts of the same key and inserts if the first writer rolls back.

### 43.
**Why:** 1. Step 3 acquires `FOR UPDATE` on row `1` and returns `5` to T1. 2. Step 4 requests `FOR UPDATE` on row `1` and blocks until T1 finishes. 3. Steps 5–6 update `stock` to `4` and commit, releasing the lock. 4. T2 wakes up, EPQ fetches committed `4`, step 4 returns `4`, and T2 writes `4 - 1 = 3` and commits.
**Answer:** `3`
**The trap:** Answering `4`, from thinking step 4 already read `5` before blocking and would overwrite T1's update.
**Rule:** `SELECT ... FOR UPDATE` serializes concurrent read-modify-write transactions and returns the post-wait committed row in `READ COMMITTED`.

### 44.
**Why:** 1. Step 2 (`DELETE`) acquires a `FOR UPDATE` lock on parent row `1`. 2. At step 3, inserting a child referencing `parent_id = 1` tries to acquire `FOR KEY SHARE` on parent row `1`. 3. Unlike `FOR NO KEY UPDATE`, `FOR UPDATE` conflicts with `FOR KEY SHARE`, so T2 blocks at step 3. 4. At step 4, T1 commits the deletion; T2 wakes up, sees parent row `1` is gone, and fails with a foreign-key violation (`23503`).
**Answer:** T2 blocks at step 3; when step 4 commits, T2 fails with a foreign-key violation (`23503`).
**The trap:** Expecting T2 to succeed immediately because T1 hasn't committed yet, leaving an orphaned child row—forgetting that FK checks take `FOR KEY SHARE` locks.
**Rule:** `DELETE` (and key-column `UPDATE`) takes `FOR UPDATE`, blocking concurrent child `INSERT`s (`FOR KEY SHARE`) until commit or rollback.

### 45.
**Why:** 1. The open reporting transaction holds `ACCESS SHARE` on `events` for 5 minutes. 2. `ALTER TABLE ... RENAME COLUMN` is a fast metadata change, not a table rewrite, yet it still requires `ACCESS EXCLUSIVE`. 3. It blocks waiting for the reporting job; meanwhile PostgreSQL's lock queue puts every new `SELECT` (`ACCESS SHARE`) and `INSERT` (`ROW EXCLUSIVE`) behind the waiting `ACCESS EXCLUSIVE` request, stalling all traffic.
**Answer:** (b) `ALTER TABLE` waits in the lock queue for `ACCESS EXCLUSIVE`, and every new `SELECT` and `INSERT` queues behind it.
**The trap:** (a) blames disk I/O on a metadata-only rename; (c) thinks plain `SELECT` holds an exclusive lock; (d) thinks table locks freeze unrelated tables or databases.
**Rule:** Even an instant metadata `ALTER TABLE` can stall an entire table if it queues behind a long-running `SELECT`.

### 46.
**Why:** 1. Deadlocks occur because T1 locks `(1 then 2)` while T2 locks `(2 then 1)`, creating a cycle. 2. If every transfer always locks or updates `LEAST(from_id, to_id)` before `GREATEST(from_id, to_id)`, both transactions try to acquire row `1` first, so one simply waits for the other—no cycle can form. 3. `REPEATABLE READ` (a) still takes the same row locks and deadlocks; `FOR SHARE` (b) creates lock-upgrade deadlocks; dropping `BEGIN` (d) breaks transfer atomicity (money can vanish on crash).
**Answer:** (c) Always lock or update the smaller account `id` before the larger account `id`.
**The trap:** Picking (a) from assuming higher isolation prevents deadlocks, or (b) from thinking shared locks avoid conflicts.
**Rule:** Acquiring locks on multiple rows in a consistent global order (such as ascending primary key) eliminates deadlocks.

### 47.
**Why:** 1. Step 2 locks row `1` under T1's main transaction. 2. Step 3 starts savepoint `s1`, and step 4 locks row `2` inside that subtransaction. 3. Step 5 (`ROLLBACK TO SAVEPOINT s1`) aborts the subtransaction, undoing row `2`'s update and releasing row `2`'s lock immediately—while keeping row `1`'s lock from before `s1`. 4. Therefore T2 updates row `2` immediately, while T3 blocks on row `1`.
**Answer:** Only T3 blocks; T2 completes immediately.
**The trap:** Predicting both T2 and T3 block (thinking locks are never released until final `COMMIT`/`ROLLBACK`) or neither blocks (thinking `ROLLBACK TO SAVEPOINT` ended the whole transaction).
**Rule:** `ROLLBACK TO SAVEPOINT` releases locks acquired after the savepoint while keeping locks acquired before it.

### 48.
**Why:** 1. Step 1 starts a `REPEATABLE READ` transaction without taking a snapshot yet. 2. Step 2 (`SELECT 1`) is a non-transaction-control query statement—even though it touches no table, PostgreSQL takes the transaction's snapshot when step 2 runs (seeing `t.x = 1`). 3. Step 3 updates `t.x` to `2` after that snapshot. 4. Step 4 reads from T1's frozen snapshot and returns `1`.
**Answer:** `1`
**The trap:** Answering `2`, from thinking the snapshot is taken only when a table is first queried (step 4) rather than at the first query statement (step 2).
**Rule:** Any query statement—even `SELECT 1`—freezes the snapshot for a `REPEATABLE READ` or `SERIALIZABLE` transaction.

### 49.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with `(1, 100)`. 2. Step 4 locks row `1` with uncommitted `200`. 3. Step 5 hits T2's row lock and blocks; PostgreSQL does not raise `40001` yet because T2 might roll back. 4. Step 6 rolls back T2, leaving `(1, 100)` unchanged. 5. T1 wakes up, sees row `1` was never committedly modified, updates `bal` to `150`, and commits cleanly.
**Answer:** T1 unblocks and succeeds (no `40001`); after step 7, `bal` is `150`.
**The trap:** Predicting `40001` as soon as T1 touches a row modified by T2, forgetting that `REPEATABLE READ` waits to see whether T2 commits or rolls back.
**Rule:** In `REPEATABLE READ`, a concurrent update causes `40001` only if the blocking transaction commits; if it rolls back, the waiter proceeds.

### 50.
**Why:** 1. Step 2 is T1's first statement in `REPEATABLE READ`, freezing T1's snapshot at `(1, 100)` and `(2, 100)`. 2. Step 3 transfers `40` from row `1` to row `2` and commits after T1's snapshot. 3. Step 4 uses the exact same snapshot and reads `100` for row `2`. 4. Summing `100 + 100` gives `200`, eliminating the read skew seen in Q39.
**Answer:** `200`
**The trap:** Answering `240` (forgetting `REPEATABLE READ` holds one snapshot across statements) or expecting an error because T2 modified rows T1 read.
**Rule:** `REPEATABLE READ` prevents read skew by keeping all reads in a transaction on one consistent snapshot.

### 51.
**Why:** 1. Step 3 acquires a `FOR SHARE` lock on row `1`. 2. Step 4 also requests `FOR SHARE` on row `1`; because shared locks are compatible with each other, T2 does not block and both T1 and T2 hold `FOR SHARE` simultaneously. 3. Step 5's `UPDATE` requires a `FOR NO KEY UPDATE` lock, which conflicts with `FOR SHARE`, so T3 blocks until both T1 and T2 finish.
**Answer:** Only T3 blocks; T1 and T2 both proceed without blocking.
**The trap:** Predicting T2 blocks on T1 (confusing `FOR SHARE` with `FOR UPDATE`) or predicting T3 doesn't block (forgetting `FOR SHARE` blocks writers).
**Rule:** Multiple transactions can hold `FOR SHARE` on the same row simultaneously, and any writer (`UPDATE` or `DELETE`) blocks until all of them end.

### 52.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot containing only row `1`. 2. Step 3 inserts and commits `(2, false)` after T1's snapshot. 3. Step 4 (`DELETE FROM tasks WHERE NOT done`) scans only rows visible in T1's snapshot, deleting row `1` and never visiting row `2`. 4. Because row `1` was not concurrently modified, step 5 commits with no `40001` error.
**Answer:** `(2, false)`
**The trap:** Predicting an empty table (thinking `DELETE` sees newly committed rows) or a `40001` error (thinking concurrent inserts matching `WHERE` cause a conflict in `REPEATABLE READ`).
**Rule:** A `DELETE` in `REPEATABLE READ` deletes only rows visible in its snapshot and ignores later inserts without raising `40001`.

### 53.
**Why:** 1. Steps 3 and 4 freeze both `REPEATABLE READ` snapshots showing 0 bookings for `(1, 9)`. 2. Step 5 inserts `(1, 9)` and commits; because `bookings` has no unique constraint, step 7 inserts a second independent row `(1, 9)` without touching T1's row. 3. First-committer-wins only checks updates/deletes to existing rows, so step 8 commits cleanly—write skew via inserts.
**Answer:** `2` rows (two duplicate `(1, 9)` rows).
**The trap:** Expecting `REPEATABLE READ` to block or abort step 7/8 with `40001`, forgetting that `REPEATABLE READ` allows write skew when transactions insert disjoint new rows.
**Rule:** Without a unique constraint (or `SERIALIZABLE`), `REPEATABLE READ` cannot prevent check-then-insert write skew.

### 54.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot showing an empty `kv`. 2. Step 3 inserts and commits `('x', 1)` after T1's snapshot. 3. At step 4, T1's `INSERT` detects `'x'` in the unique index; because the conflict clause is `DO NOTHING`, PostgreSQL simply skips inserting the row without attempting to update the post-snapshot row. 4. Step 5 commits cleanly with 0 rows inserted by T1.
**Answer:** T1 succeeds (0 rows inserted, no `40001`); `kv` contains `('x', 1)`.
**The trap:** Predicting `40001` (generalizing from Q28's `ON CONFLICT DO UPDATE`) or predicting `('x', 2)` is inserted.
**Rule:** In `REPEATABLE READ`, `ON CONFLICT DO UPDATE` raises `40001` on a post-snapshot committed row, whereas `ON CONFLICT DO NOTHING` skips it cleanly.

### 55.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with `(1, 100)`. 2. Step 3 acquires `FOR UPDATE` on row `1` and commits *without* modifying or deleting the row—PostgreSQL marks the row as locked-only and writes no new row version. 3. At step 4, T1 checks row `1`, sees the exact same row version as its snapshot, updates `bal` to `150`, and commits cleanly.
**Answer:** Step 5 succeeds (`bal` is `150`, no `40001`).
**The trap:** Predicting `40001`, from assuming any transaction that locked a row with `FOR UPDATE` triggers first-committer-wins even if it never changed the row.
**Rule:** In `REPEATABLE READ`, a concurrent `SELECT ... FOR UPDATE` that commits without modifying the row does not trigger `40001`.

### 56.
**Why:** 1. Steps 3 and 4 take SIRead predicate locks on the `(room, slot)` index for `(1, 9)`. 2. Step 5 inserts `(1, 9)`, creating rw-antidependency `T2 -> T1`, and step 6 commits T1 cleanly (no return edge yet). 3. At step 7, T2 inserts `(1, 9)`, creating the reverse edge `T1 -> T2`. 4. Because T1 has *already committed* and participates in the cycle `T2 -> T1 -> T2`, SSI aborts T2 immediately at step 7 with `40001` (before step 8).
**Answer:** Fails at step 7 (`INSERT`) with `40001`; `bookings` contains `(2, 10)` and `(1, 9)`.
**The trap:** Saying the failure happens at step 8 (`COMMIT`) instead of step 7, or thinking both commit because there is no unique constraint.
**Rule:** Under `SERIALIZABLE`, if the conflicting transaction has already committed, PostgreSQL aborts the second transaction immediately on the conflicting write rather than waiting for `COMMIT`.

### 57.
**Why:** 1. Step 1 reads `y = 0` (SIRead on `y`); step 2 updates `y = 20` and commits (`T1 -> T2`). 2. Step 3 (`SERIALIZABLE READ ONLY`) takes its snapshot after T2 committed but before T1 commits, reading `y = 20` (so T2 must precede T3). 3. Step 4 updates `x = 10` and commits (T3 has not read `x` yet, so T1 commits cleanly). 4. At step 5, T3 reads old `x = 0` from its snapshot, creating `T3 -> T1`. 5. Now `T3 -> T1 -> T2` forms a cycle (no serial order explains `x = 0, y = 20`), and both T1 and T2 are committed, so step 5 aborts T3 with `40001`.
**Answer:** Step 5 fails with `40001` (`could not serialize access due to read/write dependencies among transactions`).
**The trap:** Predicting `0` with no error, from believing a `READ ONLY` transaction can never fail with `40001`.
**Rule:** Even a `SERIALIZABLE READ ONLY` transaction can suffer a `40001` failure on a `SELECT` due to a three-transaction read-only anomaly.

### 58.
**Why:** 1. Under the stated assumptions, steps 3 and 4 use index scans on `id` with rows `1` and `2` on separate pages, so T1 takes a predicate lock on row `1` and T2 takes a predicate lock on row `2`. 2. Step 5 updates row `1` (not locked by T2); step 6 updates row `2` (not locked by T1). 3. No rw-antidependencies form in either direction, so steps 7 and 8 both commit cleanly.
**Answer:** Both T1 and T2 commit cleanly.
**The trap:** Predicting `40001` (over-generalizing from Q32's unindexed sequential scan) or predicting blocking (thinking `SERIALIZABLE` locks the whole table).
**Rule:** Indexed `SERIALIZABLE` transactions touching disjoint rows on separate pages create no rw-dependencies and commit concurrently.

### 59.
**Why:** 1. SSI detects write skew by recording SIRead locks and rw-antidependency edges between `SERIALIZABLE` transactions. 2. Because the admin tool runs at `READ COMMITTED`, PostgreSQL does not track SIRead locks or rw-dependencies for its queries or updates. 3. A payment withdrawal and a concurrent admin adjustment on different accounts of the same user can therefore both commit and drive the combined balance below `0`.
**Answer:** (c) Yes, because `READ COMMITTED` transactions do not participate in SSI read/write dependency tracking.
**The trap:** (a) assumes `SERIALIZABLE` locks tables against other sessions; (b) invents automatic isolation upgrades; (d) invents a special exception for `UPDATE` vs `DELETE`.
**Rule:** Mixing `SERIALIZABLE` with `READ COMMITTED` or `REPEATABLE READ` on the same tables breaks SSI's anomaly guarantees.

### 60.
**Why:** 1. A `40001` serialization failure aborts the entire transaction block, just like any other error inside `BEGIN`. 2. Without running `ROLLBACK` first, PostgreSQL rejects every subsequent command—including a retried `UPDATE`—with SQLSTATE `25P02` (`current transaction is aborted`). 3. Correct handling requires `ROLLBACK`, a fresh `BEGIN`, and re-running the entire transaction from the start (re-reading fresh data).
**Answer:** (b) The retried `UPDATE` fails with `25P02` because the transaction block is aborted.
**The trap:** (a) and (c) assume PostgreSQL supports retrying a single failed statement in place; (d) invents partial commits after an error.
**Rule:** On `40001` (or `40P01`), you must `ROLLBACK` and retry the entire transaction from `BEGIN`.

### 61.
**Why:** 1. Step 2 locks row `1` with uncommitted `total = 150`. 2. Step 3 (`READ COMMITTED`) starts when only row `1` exists, sees `(1, 100)`, and blocks on row `1`. 3. Step 4 inserts and commits `(2, 200)` after step 3's snapshot started. 4. Step 5 commits `(1, 150)`. 5. T2 wakes up, EPQ re-fetches locked row `1` (`150 >= 100`), updates it to `160`, and finishes—EPQ does *not* pick up row `2`, which was absent from step 3's scan snapshot.
**Answer:** Row 1 is `160`; row 2 is `200`.
**The trap:** Answering `210` for row 2 (thinking waiting caused step 3 to re-scan the whole table and pick up T3's insert) or `110` for row 1 (forgetting EPQ uses `150`).
**Rule:** In `READ COMMITTED`, EPQ re-evaluates only rows the `UPDATE` already visited and locked; it never picks up newly inserted rows.

### 62.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot pointing to row `1`'s original MVCC tuple version. 2. At step 3, even though `SET bal = 100` writes the same value, PostgreSQL MVCC creates a brand-new committed row version and marks the old version superseded by T2. 3. At step 4, T1 sees row `1` was updated and committed after its snapshot and aborts with `40001`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Predicting T1 succeeds because the column's value did not actually change—comparing with Q55's `FOR UPDATE` (which writes no new tuple) rather than `UPDATE` (which always writes a new tuple).
**Rule:** Any committed `UPDATE`—even setting a column to its current value—creates a new row version and triggers `40001` in `REPEATABLE READ`.

### 63.
**Why:** 1. Step 2 locks row `1` with uncommitted `prio = 100`. 2. At step 3, PostgreSQL reads `(1, 1, 'open')` and `(2, 2, 'open')` from its snapshot and sorts them by `prio` (`row 1`, then `row 2`) *before* the `LockRows` (`FOR UPDATE`) step. 3. `LockRows` tries to lock row `1` and blocks on T1. 4. Step 4 commits `(1, 100, 'open')`. 5. `LockRows` wakes up, EPQ checks `WHERE status = 'open'` (still true), does *not* re-sort, and returns `(1, 100)` to `LIMIT 1`.
**Answer:** `(1, 100)`
**The trap:** Answering `(2, 2)` (thinking `FOR UPDATE` re-runs `ORDER BY prio` after waiting) or `(1, 1)` (forgetting EPQ returns the newly committed column value `100`).
**Rule:** `SELECT ... ORDER BY ... FOR UPDATE` in `READ COMMITTED` re-checks `WHERE` after waiting, but never re-sorts the rows.

### 64.
**Why:** 1. Step 2 holds a `FOR UPDATE` lock on row `1`. 2. Step 3's subquery scans `'open'` rows with `FOR UPDATE SKIP LOCKED`, skips locked row `1`, and locks/returns only row `2`. 3. The outer `count(*)` counts the rows returned by the subquery, yielding `1`.
**Answer:** `1`
**The trap:** Answering `2`, from assuming `SKIP LOCKED` only affects locking and still includes locked rows in counts.
**Rule:** `SKIP LOCKED` intentionally omits locked rows from the result set, so it produces incomplete totals and should not be used for counts or reports.

### 65.
**Why:** 1. Step 2 locks row `1` `FOR UPDATE`. 2. Step 3 (`READ COMMITTED`) blocks on row `1` waiting for T1. 3. Steps 4–5 update `bal` to `70` and commit, releasing the lock. 4. T2 wakes up; under `READ COMMITTED`, `FOR UPDATE` fetches the newly committed row version via EPQ and returns `70`, not the `100` that existed when step 3 began.
**Answer:** `70`
**The trap:** Answering `100`, from assuming step 3 returns the value from the snapshot taken when step 3 started before blocking.
**Rule:** In `READ COMMITTED`, a blocked `SELECT ... FOR UPDATE` returns the row's latest committed values after unblocking.

### 66.
**Why:** 1. Step 2 locks row `1` with uncommitted `status = 'done'`. 2. Step 3 (`READ COMMITTED`) scans `id = 1` first, tries to lock it `FOR UPDATE`, and blocks on T1. 3. Step 4 commits `status = 'done'`. 4. T2's `LockRows` node wakes up, EPQ re-checks `WHERE status = 'open'` on row `1` (now false), discards row `1`, and requests the next row from the scan—row `2`—before `LIMIT 1` is satisfied. 5. Row `2` is unlocked and `'open'`, so T2 locks and returns `2`.
**Answer:** `2`
**The trap:** Answering `0` rows (thinking `LIMIT 1` already cut off the scan at row `1` before `LockRows` checked it).
**Rule:** `LIMIT` sits above `FOR UPDATE`, so when EPQ discards a row in `READ COMMITTED`, PostgreSQL pulls the next matching row to satisfy `LIMIT`.

### 67.
**Why:** 1. T1 runs in `READ COMMITTED`, taking a new snapshot per statement. 2. Step 2 sums the two existing `'open'` rows (`60 + 60 = 120`). 3. Step 3 inserts and commits `(3, 'open', 60)`. 4. Step 4 takes a fresh snapshot, sees the phantom third row, and returns `3`. 5. Dividing `120 / 3` produces `40`—an impossible average when every single row has `amt = 60`.
**Answer:** `40`
**The trap:** Answering `60`, from assuming two aggregates inside one `BEGIN ... COMMIT` block operate on the same set of rows.
**Rule:** Splitting related aggregates across separate statements in `READ COMMITTED` lets phantom rows corrupt ratios and averages.

### 68.
**Why:** 1. Step 1 starts a `REPEATABLE READ` transaction without taking a snapshot. 2. Step 2 (`SET TRANSACTION READ ONLY`) is a transaction-control command, *not* a query or DML statement, so it still does not freeze the snapshot. 3. Step 3 updates `t.x` to `2` and autocommits. 4. Step 4 is the first non-transaction-control statement, so T1 freezes its snapshot now and reads `2`.
**Answer:** `2`
**The trap:** Answering `1`, from treating `SET TRANSACTION READ ONLY` like `SELECT 1` (Q48) and assuming it took the snapshot at step 2.
**Rule:** Transaction-control commands (`BEGIN`, `SET TRANSACTION`) do not freeze a `REPEATABLE READ` snapshot; the first query or DML statement does.

### 69.
**Why:** 1. At step 1–2, T1 (`SERIALIZABLE`) read `y = 0` and T2 updated `y = 20` and committed (`T1 -> T2`). 2. At step 3, T3 starts `SERIALIZABLE READ ONLY DEFERRABLE` and runs its first `SELECT`; PostgreSQL detects that taking a snapshot while T1 is still active could create a read-only anomaly, so step 3 *blocks* waiting for a safe snapshot. 3. Step 4 updates `x = 10` and commits T1. 4. T3 now gets a safe snapshot after T1 committed, reads `y = 20` and `x = 10`, and commits with no `40001`.
**Answer:** T3 blocks at step 3 until step 4 commits, then reads `y = 20` and `x = 10` with no error.
**The trap:** Predicting step 5 fails with `40001` (ignoring `DEFERRABLE`) or predicting T3 reads `x = 0, y = 20` without waiting.
**Rule:** `SERIALIZABLE READ ONLY DEFERRABLE` may wait once at its first query for a safe snapshot, and thereafter can never cause or suffer `40001` errors.

### 70.
**Why:** 1. On the first attempt, `INSERT INTO orders(amt) VALUES (50)` advances the `SERIAL` sequence from `0` to `1`. 2. When `COMMIT` fails with `40001` and the handler rolls back, the row is discarded, but the sequence advance is non-transactional and stays at `1`. 3. On the retry, `INSERT` calls `nextval()` again, receives `2`, and commits `(2, 50)`.
**Answer:** `2`
**The trap:** Answering `1`, from assuming a rolled-back `40001` retry leaves no trace and reuses the aborted attempt's `SERIAL` ID.
**Rule:** Every `40001` retry that executed `nextval()`/`SERIAL` permanently consumes a sequence value, creating ID gaps.

### 71.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with `(1, 100)`. 2. Step 3 updates row `1` to `80` and commits after T1's snapshot. 3. At step 4, `SELECT ... FOR UPDATE` tries to lock row `1`; under `REPEATABLE READ`, locking a row that was modified and committed after the snapshot enforces first-committer-wins just like `UPDATE` or `DELETE` and aborts T1 with `40001`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Predicting step 4 returns `100` (thinking `SELECT` always returns the snapshot) or `80` (expecting `READ COMMITTED` EPQ behavior).
**Rule:** In `REPEATABLE READ`, `SELECT ... FOR UPDATE` raises `40001` if a target row was modified and committed after the snapshot.

### 72.
**Why:** 1. Steps 3 and 4 both succeed because `FOR SHARE` locks are mutually compatible—both T1 and T2 now hold `FOR SHARE` on row `1`. 2. Step 5 (`UPDATE`) tries to upgrade T1's lock to `FOR NO KEY UPDATE`, which conflicts with T2's `FOR SHARE`, so T1 blocks waiting for T2. 3. Step 6 tries to upgrade T2's lock to `FOR NO KEY UPDATE`, which conflicts with T1's `FOR SHARE`, forming a lock-upgrade deadlock. 4. PostgreSQL detects the cycle and aborts one transaction with `40P01`.
**Answer:** Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other complete.
**The trap:** Thinking two transactions locking only a *single* row can never deadlock (forgetting shared-to-exclusive lock upgrades create a cycle on one row).
**Rule:** Upgrading `FOR SHARE` to `UPDATE` on the same row causes lock-upgrade deadlocks; use `FOR UPDATE` upfront if you intend to modify the row.

### 73.
**Why:** 1. Step 2 updates `bal` to `50` and locks row `1`; step 4 updates it further to `10` inside savepoint `s1`. 2. Step 5 (`READ COMMITTED`) blocks waiting on T1's lock on row `1`. 3. Step 6 rolls back to `s1` (undoing `10` back to `50`) and commits `bal = 50`. 4. Step 7 wakes up, EPQ fetches T1's final committed value `50` (not `10`), computes `50 - 20 = 30`, and commits `30`.
**Answer:** `30`
**The trap:** Answering `-10` (using the rolled-back `10`) or `80` (using pre-wait `100` instead of EPQ's committed `50`).
**Rule:** Waiting `READ COMMITTED` updates see the blocking transaction's final committed version after any savepoint rollbacks.

### 74.
**Why:** 1. Step 2 inserts `('a', 1)` uncommitted. 2. Step 3 runs `BEGIN ISOLATION LEVEL REPEATABLE READ`—no snapshot is taken yet. 3. Step 4 commits `('a', 1)` *before* T2 runs any statement. 4. Step 5 is T2's first statement, so T2 freezes its snapshot now, *including* `('a', 1)`. 5. Because `('a', 1)` is visible in T2's snapshot, `ON CONFLICT DO UPDATE` updates it cleanly to `('a', 2)` with no `40001`.
**Answer:** Step 5 succeeds (no `40001`); `kv` contains `('a', 2)`.
**The trap:** Predicting `40001` (confusing this with Q28/Q89 where T2's snapshot was frozen *before* T1 committed).
**Rule:** If a `REPEATABLE READ` transaction has not yet run its first statement, commits that finish before `INSERT ... ON CONFLICT DO UPDATE` are inside its snapshot and update cleanly.

### 75.
**Why:** 1. Because `category` has no index, steps 3 and 4 execute sequential scans on `items`, acquiring relation-level SIRead locks covering the entire table. 2. Step 5 updates row `1` (`'books'`), conflicting with T2's table-wide SIRead lock (`T2 -> T1`). 3. Step 6 updates row `2` (`'music'`), conflicting with T1's table-wide SIRead lock (`T1 -> T2`). 4. Step 7 commits T1; step 8 sees the committed cycle and aborts T2 with `40001` despite disjoint categories.
**Answer:** Step 8 fails with `40001` (`could not serialize access due to read/write dependencies among transactions`).
**The trap:** Predicting both commit because `'books'` and `'music'` never overlap and the `UPDATE`s used the `id` primary-key index—forgetting the `SELECT`s took table-wide SIRead locks.
**Rule:** Under `SERIALIZABLE`, adding an index on `WHERE` columns is not just for speed—it prevents table-wide sequential-scan SIRead locks from causing false-positive `40001` aborts.

### 76.
**Why:** 1. Step 1 only runs `BEGIN ISOLATION LEVEL REPEATABLE READ`; T1 has neither taken a snapshot nor touched `items`, so T1 holds no `ACCESS SHARE` lock on `items`. 2. Step 2 (`ALTER TABLE`) requests `ACCESS EXCLUSIVE` on `items`, finds no conflicting locks held by T1, and completes immediately.
**Answer:** Step 2 finishes immediately (does not block).
**The trap:** Predicting step 2 blocks until T1 commits, from assuming an open `REPEATABLE READ` transaction locks all tables in the database.
**Rule:** A transaction acquires `ACCESS SHARE` on a table only when it actually queries that table, not at `BEGIN`.

### 77.
**Why:** 1. Step 3 locks both on-call rows (`1` and `2`) `FOR UPDATE` for T1. 2. Step 4 tries to lock rows `1` and `2` `FOR UPDATE` for T2 and blocks on T1. 3. Steps 5–6 update row `1` to `false` and commit. 4. T2 wakes up in `REPEATABLE READ`, sees that row `1` (which it tried to lock `FOR UPDATE`) was updated and committed after T2's snapshot, and fails with `40001`—preventing write skew without `SERIALIZABLE`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Predicting T2 returns only row `2` and commits (confusing `REPEATABLE READ` with `READ COMMITTED`'s EPQ) or predicting both commit (forgetting `FOR UPDATE` locked row `1` too).
**Rule:** Materializing a conflict by locking the entire read set `FOR UPDATE` prevents write skew even in `REPEATABLE READ`.

### 78.
**Why:** 1. Step 3 places an uncommitted primary-key index entry for `1` (owned by T1); step 4 places one for `2` (owned by T2). 2. Step 5 (`T1` inserting `2`) hits T2's uncommitted entry and blocks waiting on T2. 3. Step 6 (`T2` inserting `1`) hits T1's uncommitted entry and blocks waiting on T1—forming a wait-for cycle. 4. PostgreSQL detects the deadlock and aborts one transaction with `40P01`.
**Answer:** Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other proceed.
**The trap:** Assuming deadlocks require `UPDATE` or `FOR UPDATE` and cannot happen in an `INSERT`-only workload.
**Rule:** Concurrent `INSERT`s of overlapping unique keys in opposite orders can deadlock (`40P01`) via unique-index value locks.

### 79.
**Why:** 1. Step 2 locks row `1` with uncommitted `bal = 50`. 2. Step 3 (`READ COMMITTED`) takes a snapshot showing `(1, 100)` and `(2, 50)`: row `1` matches `bal = 100`, so T2 tries to lock row `1` and blocks; row `2` (`50`) does *not* match `bal = 100`. 3. Step 4 sets row `2` to `100` and commits `(1, 50), (2, 100)`. 4. T2 wakes up on row `1`, EPQ sees `50 != 100` and skips row `1`; because row `2` never matched step 3's snapshot, EPQ never checks row `2`. 5. Step 3 updates 0 rows.
**Answer:** Step 3 updates `0` rows; final balances are `(1, 50)` and `(2, 100)`.
**The trap:** Predicting row `2` becomes `110` (thinking T2 sees row `2`'s new `100` after waking up) or row `1` becomes `60` (forgetting EPQ re-checks `WHERE`).
**Rule:** In `READ COMMITTED`, a row that enters `WHERE` only after an `UPDATE` began is never visited by EPQ, so an `UPDATE` can update 0 rows even when a matching row existed both before and after.

### 80.
**Why:** 1. Step 2 consumes sequence value `1` and inserts `(1, 10)`. 2. Step 3 sets savepoint `sp`. 3. Step 4 calls `nextval()` (consuming `2`) before failing on the `UNIQUE(u)` constraint (`23505`). 4. Step 5 rolls back to `sp`, clearing the aborted transaction state while keeping `(1, 10)`—but the sequence does *not* roll back from `2`. 5. Step 6 consumes `3` and inserts `(3, 20)`, and step 7 commits both.
**Answer:** `(1, 10)` and `(3, 20)`.
**The trap:** Answering `(1, 10)` and `(2, 20)` (thinking `ROLLBACK TO SAVEPOINT` rewinds the sequence) or empty table (forgetting the savepoint recovered from `23505`).
**Rule:** Savepoints recover from errors and roll back rows, but failed inserts still permanently advance `SERIAL` sequences.

### 81.
**Why:** 1. Step 2 reads row `1` (SIRead on row `1`). 2. Step 3 updates row `1` and commits, creating a single one-way rw-antidependency `T1 -> T2`. 3. Step 4 updates row `2`; because T2 never read row `2` (and indexed scans touch distinct rows on separate pages), no reverse edge `T2 -> T1` forms. 4. The execution matches the serial order T1 then T2, so step 5 commits cleanly.
**Answer:** Both T1 and T2 commit cleanly.
**The trap:** Predicting `40001`, from thinking any `SERIALIZABLE` transaction that both reads a concurrently modified row and writes *some* row must abort.
**Rule:** Under `SERIALIZABLE`, a write to a row the other transaction never read does not close an rw-cycle, so both transactions commit.

### 82.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot showing rows `1` and `2` as `'open'`. 2. Step 3 locks row `1` (still uncommitted!). 3. At step 4, `FOR UPDATE SKIP LOCKED` checks row `1`, sees T2 currently holds a row lock on it, and skips row `1` immediately without waiting for T2 to commit or triggering a `40001` check. 4. It moves to unlocked row `2`, locks it, and returns `2`.
**Answer:** `2` (no `40001`).
**The trap:** Predicting `40001` (confusing an uncommitted lock skipped by `SKIP LOCKED` with Q96's already-committed update) or predicting T1 blocks on T2.
**Rule:** `SKIP LOCKED` skips rows locked by active transactions before waiting, avoiding `40001` in `REPEATABLE READ` for still-uncommitted writers.

### 83.
**Why:** 1. The 10-minute reporting `SELECT` holds `ACCESS SHARE`; `ALTER TABLE` needs `ACCESS EXCLUSIVE` and waits in the queue, causing all subsequent `SELECT`/`INSERT` requests to stall behind it. 2. Setting `SET LOCAL lock_timeout = '1s'` causes `ALTER TABLE` itself to abort with a lock-timeout error after 1 second instead of sitting in the queue for 10 minutes, immediately releasing all queued queries behind it.
**Answer:** (c) After 1 second, `ALTER TABLE` aborts cleanly instead of blocking all incoming queries in the lock queue for 10 minutes.
**The trap:** (a) thinks `lock_timeout` bypasses locks; (b) confuses `lock_timeout` on the migration with cancelling the blocking query; (d) thinks `INSERT` bypasses `ACCESS EXCLUSIVE`.
**Rule:** Always set a short `lock_timeout` before DDL migrations so a blocked `ALTER TABLE` aborts quickly instead of stalling production traffic in the lock queue.

### 84.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot showing an empty `users` table. 2. Step 3 inserts and commits `(1)` after T1's snapshot. 3. At step 4, T1 tries to insert `(1)` with no `ON CONFLICT` clause; primary-key uniqueness is enforced immediately across all transactions in the shared B-tree index regardless of snapshot visibility. 4. PostgreSQL therefore raises unique violation `23505`, *not* `40001`.
**Answer:** `23505` (`unique_violation`).
**The trap:** Answering `40001`, from assuming every conflict with a post-snapshot commit in `REPEATABLE READ` produces a serialization failure.
**Rule:** Unique constraint collisions raise `23505` even in `REPEATABLE READ` when the conflicting row is invisible to the transaction's snapshot.

### 85.
**Why:** 1. `SERIALIZABLE` in PostgreSQL is built directly on top of Snapshot Isolation's first-committer-wins rule. 2. Step 2 freezes T1's snapshot with `(1, 100)`. 3. Step 3 updates row `1` (locking it); step 4 blocks on T2's row lock. 4. When step 5 commits T2's update to row `1`, T1 wakes up and immediately hits Snapshot Isolation's concurrent-update check, failing at step 4 with `40001` (`could not serialize access due to concurrent update`)—before `COMMIT` and without needing an SSI cycle.
**Answer:** (c) Step 4 fails immediately after step 5 with `40001` (`could not serialize access due to concurrent update`).
**The trap:** (b) assumes all `SERIALIZABLE` errors wait until `COMMIT`; (a) assumes earlier start time wins; (d) reverses first-committer-wins.
**Rule:** Under `SERIALIZABLE`, concurrent updates to the same row still fail immediately on the write via first-committer-wins (`40001`).

### 86.
**Why:** 1. `SELECT ... FOR UPDATE` can lock only rows that already exist in the table. 2. At steps 3 and 4, `bookings` is empty, so both `SELECT ... FOR UPDATE` queries return 0 rows and acquire *zero* locks. 3. Steps 5–6 and 7–8 both insert `(1, 9)` cleanly with no lock conflict and no `40001`, leaving 2 duplicate rows.
**Answer:** `2` rows (two duplicate `(1, 9)` rows).
**The trap:** Expecting `FOR UPDATE` to lock the "gap" or predicate `(room = 1, slot = 9)` and block T2—forgetting PostgreSQL has no gap locks for `FOR UPDATE`.
**Rule:** `SELECT ... FOR UPDATE` cannot lock nonexistent rows; prevent duplicate inserts with a `UNIQUE` constraint (or lock a parent row, or use `SERIALIZABLE`).

### 87.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with `(1, 100)`. 2. Step 3 updates row `2` (main tx) and updates row `1` inside savepoint `sp`. 3. Step 4 blocks waiting on T2's transaction. 4. Step 5 rolls back to `sp`, aborting T2's update to row `1` while keeping row `2`'s update. 5. Step 6 commits T2—crucially, row `1` was *never* committedly modified. 6. T1 wakes up, sees row `1`'s tuple is still its snapshot version, sets `bal = 150`, and commits cleanly.
**Answer:** T1 succeeds (no `40001`); `bal` for `id = 1` is `150`.
**The trap:** Predicting `40001` simply because T2 committed at step 6, forgetting that the subtransaction that touched row `1` rolled back.
**Rule:** A `REPEATABLE READ` writer fails with `40001` only if a concurrent modification to *that row* actually committed—not if its savepoint rolled back.

### 88.
**Why:** 1. Step 3 (`DELETE` parent 1) acquires `FOR UPDATE` on parent `1`. 2. Step 4 (`INSERT` child referencing parent 2) acquires `FOR KEY SHARE` on parent `2`. 3. Step 5 (`DELETE` parent 2) needs `FOR UPDATE` on parent `2`, which conflicts with T2's `FOR KEY SHARE`, so T1 blocks on T2. 4. Step 6 (`INSERT` child referencing parent 1) needs `FOR KEY SHARE` on parent `1`, which conflicts with T1's `FOR UPDATE`, so T2 blocks on T1—a deadlock (`40P01`).
**Answer:** Deadlock (`40P01`); PostgreSQL aborts one transaction and lets the other proceed.
**The trap:** Thinking `DELETE` on `parents` and `INSERT` on `children` touch different tables and therefore cannot deadlock.
**Rule:** Foreign-key checks acquire `FOR KEY SHARE` locks on parent rows, which can deadlock with `DELETE` or key-column `UPDATE` (`FOR UPDATE`) on `parents`.

### 89.
**Why:** 1. Step 2 inserts `('a', 1)` uncommitted. 2. At step 3, `INSERT ... ON CONFLICT DO UPDATE` is T2's first statement in `REPEATABLE READ`, so T2 freezes its snapshot *before* step 4 commits (seeing an empty `kv`), then hits T1's uncommitted `'a'` in the index and blocks. 3. Step 4 commits `('a', 1)`. 4. T2 wakes up, enters `DO UPDATE`, sees `('a', 1)` was committed *after* T2's snapshot, and aborts with `40001`.
**Answer:** T2 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Predicting `('a', 2)` (confusing this with Q74, where T1 committed *before* T2's first statement ran, or with Q11 in `READ COMMITTED`).
**Rule:** In `REPEATABLE READ`, if `INSERT ... ON CONFLICT DO UPDATE` begins while a conflicting insert is uncommitted and that insert commits, it fails with `40001`.

### 90.
**Why:** 1. Step 2 creates savepoint `s1`. 2. Step 3 (`SELECT`) acquires an `ACCESS SHARE` table lock on `items` inside the subtransaction `s1`. 3. Step 4 (`ROLLBACK TO SAVEPOINT s1`) aborts that subtransaction and releases all table locks acquired exclusively after `s1`—including `ACCESS SHARE` on `items`. 4. Because T1 holds no lock on `items` anymore, step 5 (`ALTER TABLE` needing `ACCESS EXCLUSIVE`) completes immediately.
**Answer:** Step 5 completes immediately (does not block).
**The trap:** Predicting step 5 blocks because T1 is still open, forgetting that `ROLLBACK TO SAVEPOINT` releases relation locks acquired after the savepoint.
**Rule:** `ROLLBACK TO SAVEPOINT` releases table locks (including `ACCESS SHARE`) acquired inside the rolled-back subtransaction.

### 91.
**Why:** 1. In `READ COMMITTED`, concurrent read-modify-write requests both commit and silently lose one update. 2. Switching to `REPEATABLE READ` activates first-committer-wins: the second writer no longer silently overwrites, but instead fails with `40001`. 3. Because no retry loop (and no `FOR UPDATE`) was added, that `40001` bubbles up as an unhandled error to the caller.
**Answer:** (b) Instead of silently losing one update, the second request fails with `40001` and returns an error to the caller.
**The trap:** (a) believes `REPEATABLE READ` magically makes concurrent writes succeed without retries; (c) forgets `REPEATABLE READ` catches same-row write conflicts; (d) confuses `40001` with deadlocks (`40P01`).
**Rule:** Raising isolation to `REPEATABLE READ` or `SERIALIZABLE` requires adding a transaction retry loop for `40001` errors.

### 92.
**Why:** 1. Step 2 locks row `1` (uncommitted `'done'`). 2. At step 3, T2's `FOR UPDATE SKIP LOCKED` skips locked row `1` and immediately locks and returns `2`. 3. At step 4, T3's plain `FOR UPDATE` (without `SKIP LOCKED`) hits T1's lock on row `1` and blocks. 4. At step 5, T1 rolls back, releasing row `1` still with `status = 'open'`. 5. T3 wakes up, re-checks `WHERE status = 'open'` (true), locks row `1`, and returns `1`.
**Answer:** Step 3 (T2) returns `2`; step 4 (T3) returns `1`.
**The trap:** Predicting T3 skips to row `2` (or returns 0 rows) after T1's update—forgetting T1 rolled back instead of committing.
**Rule:** `SKIP LOCKED` immediately moves past locked rows, whereas plain `FOR UPDATE` waits and re-evaluates the row once the holder commits or rolls back.

### 93.
**Why:** 1. Steps 3–6 establish the same bidirectional SIRead / write-skew dependencies (`T2 -> T1` and `T1 -> T2`) as Q29. 2. However, at step 7, T1 *rolls back*, which discards T1's changes and removes T1 from any committed serialization cycle. 3. At step 8, no committed conflict cycle exists, so T2 commits cleanly.
**Answer:** Step 8 succeeds.
**The trap:** Predicting `40001`, from assuming the rw-conflict edges recorded at steps 5–6 permanently doom T2 even if T1 rolls back.
**Rule:** Rolling back one transaction in an SSI conflict cycle frees the other transaction to commit cleanly.

### 94.
**Why:** 1. In PostgreSQL, all parts of a single data-modifying `WITH` (CTE) statement execute against the *same* snapshot taken before the statement starts—sub-statements cannot see each other's table changes directly. 2. The CTE `u` updates row `1` from `100` to `50` and exposes `50` via `RETURNING bal`, so `updated_bal` is `50`. 3. Meanwhile, `(SELECT bal FROM accounts WHERE id = 1)` reads the table using that pre-update snapshot and sees `100`.
**Answer:** `table_bal = 100, updated_bal = 50`
**The trap:** Answering `table_bal = 50, updated_bal = 50`, from assuming the `WITH` clause finishes and makes its table writes visible to the main `SELECT` before the main `SELECT` runs.
**Rule:** A data-modifying CTE and its outer query share one pre-statement snapshot, so only `RETURNING` exposes the CTE's changes within the same statement.

### 95.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot with parent `(1, 'a')`. 2. Step 3 inserts a child referencing `parent_id = 1`, which acquires `FOR KEY SHARE` on parent row `1` and commits *without* modifying parent row `1` (no new tuple version of `parents` is created). 3. At step 4, T1 sees parent row `1`'s tuple version is unchanged since its snapshot, updates `name` to `'b'`, and commits cleanly.
**Answer:** Step 4 succeeds (no `40001`).
**The trap:** Predicting `40001`, from thinking a child `INSERT` locking parent row `1` (`FOR KEY SHARE`) counts as a concurrent update to `parents`.
**Rule:** Foreign-key `FOR KEY SHARE` locks do not modify parent rows and never trigger `40001` concurrent-update failures in `REPEATABLE READ`.

### 96.
**Why:** 1. Step 2 freezes T1's `REPEATABLE READ` snapshot showing both rows `1` and `2` as `'open'`. 2. Step 3 updates row `1` to `'done'` and commits after T1's snapshot. 3. At step 4, T1 scans row `1` first, attempts to lock it `FOR UPDATE`, and discovers row `1` was modified and committed after its snapshot. 4. Unlike `READ COMMITTED` (Q66, where EPQ skips row `1` and advances to row `2`), `REPEATABLE READ` refuses to re-evaluate and immediately aborts with `40001`.
**Answer:** Step 4 fails with `40001` (`could not serialize access due to concurrent update`).
**The trap:** Answering `2`, from assuming `LIMIT 1 FOR UPDATE` skips modified rows in `REPEATABLE READ` the same way it does in `READ COMMITTED`.
**Rule:** `REPEATABLE READ` has no EPQ re-evaluation; hitting a concurrently committed row during `FOR UPDATE` aborts with `40001` instead of advancing to the next row.

### 97.
**Why:** 1. At `READ COMMITTED`, the analytics query does not participate in SSI and takes no SIRead locks, so it causes zero `40001` errors in checkouts. 2. Switching it to plain `SERIALIZABLE` causes its sequential scan to take a relation-level SIRead lock on `orders`, which can form rw-cycles with concurrent checkouts and trigger `40001` failures. 3. Using `SERIALIZABLE READ ONLY DEFERRABLE` waits once for a safe snapshot and then reads without causing or suffering `40001` failures (and without blocking checkouts).
**Answer:** (c) Running the analytics job at `READ COMMITTED` causes no SSI `40001` failures; switching it to plain `SERIALIZABLE` can trigger `40001` failures via a relation-level predicate lock, whereas `SERIALIZABLE READ ONLY DEFERRABLE` avoids `40001`.
**The trap:** (a) thinks `READ COMMITTED` scans trigger SSI errors; (b) thinks read-only `SERIALIZABLE` transactions can't trigger `40001`; (d) thinks `DEFERRABLE` blocks writers instead of waiting once itself.
**Rule:** Use `SERIALIZABLE READ ONLY DEFERRABLE` for long analytical reads that need a serializable snapshot without causing `40001` failures.

### 98.
**Why:** 1. Step 3 runs only `BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE`; just like `REPEATABLE READ`, no snapshot is requested until the first query runs. 2. Step 4 updates `x = 10` and commits T1 *before* T3 runs any query. 3. At step 5, when T3 runs its first `SELECT`, neither T1 nor T2 is still active, so T3 immediately gets a safe snapshot without blocking and returns `('x', 10), ('y', 20)`.
**Answer:** Step 5 returns immediately (does not block) with `('x', 10), ('y', 20)`.
**The trap:** Predicting step 5 blocks (forgetting T1 already committed at step 4 before T3's first query) or predicting T3 sees `('x', 0)` (forgetting `BEGIN` does not take the snapshot).
**Rule:** `READ ONLY DEFERRABLE` evaluates snapshot safety at its first query, so if conflicting writers already committed, it proceeds immediately without waiting.

### 99.
**Why:** 1. To stop cross-account write skew without `SERIALIZABLE`, concurrent withdrawals for the same user must serialize on a shared lock target. 2. Locking the user's parent row in `users` with `FOR UPDATE` (c) forces all concurrent withdrawals for `$u` to wait in line, so each checks `sum(bal)` after the prior withdrawal commits. 3. Option (a) allows write skew in `REPEATABLE READ`; (b) fails because different `acct_id`s don't lock each other and the subquery uses a pre-wait snapshot; (d) locks only one account, leaving concurrent withdrawals on the user's other account unblocked.
**Answer:** (c) Lock the user's parent row with `SELECT 1 FROM users WHERE id = $u FOR UPDATE`, then check `sum(bal)` and `UPDATE` the chosen `acct_id`.
**The trap:** Picking (a) from trusting `REPEATABLE READ` against write skew, (b) from assuming a subquery in `WHERE` serializes across rows, or (d) from locking only the single row being updated.
**Rule:** To enforce a multi-row invariant without `SERIALIZABLE`, lock a shared parent row (or every row in the invariant set) with `FOR UPDATE` before checking and updating.

### 100.
**Why:** 1. On attempt 1, `INSERT` consumes `id = 1` from the `SERIAL` sequence, the application immediately calls `send_welcome_email` (email #1—an external side effect PostgreSQL cannot roll back), and `COMMIT` fails with `40001`. 2. The retry loop rolls back the database work, but neither email #1 nor sequence value `1` rolls back. 3. Attempt 2 consumes `id = 2`, sends email #2, and commits cleanly.
**Answer:** `2` welcome emails are sent, and `id = 2` is stored in `users`.
**The trap:** Answering `1` email and `id = 1`, from forgetting that transaction retries re-execute external side effects placed before `COMMIT` and advance `SERIAL` sequences each attempt.
**Rule:** Keep external side effects (emails, webhooks, charges) outside retryable transactions—trigger them only after `COMMIT` succeeds (or via a transactional outbox).

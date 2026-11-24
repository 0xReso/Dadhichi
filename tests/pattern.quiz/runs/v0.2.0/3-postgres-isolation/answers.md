# Answer key

## Mechanisms

1. Outside BEGIN, every statement is its own transaction, and the default level is READ COMMITTED. Q4, Q39, Q82
2. No level ever shows another transaction's uncommitted changes; READ UNCOMMITTED behaves as READ COMMITTED. Q1, Q24, Q77, Q88
3. A transaction sees its own uncommitted changes. Q2, Q42, Q99
4. A commit becomes visible all at once: other sessions see all of a transaction's changes or none. Q10, Q39, Q51, Q79
5. READ COMMITTED takes a fresh snapshot for every statement, so two reads in one transaction can disagree. Q3, Q12, Q22, Q46, Q76
6. One statement sees one snapshot from start to finish, including its own sub-statements, and never its own changes in progress. Q11, Q32, Q60, Q79, Q85
7. Plain reads never wait for row locks and never make writers wait. Q1, Q12, Q16, Q54
8. Two writers to the same row: the second waits until the first commits or rolls back. Q5, Q41, Q67, Q72, Q86, Q90
9. Row locks last until the transaction ends, whether or not the row's values changed. Q19, Q45, Q67
10. READ COMMITTED re-check: after waiting, a writer re-tests its WHERE on the newest row version and builds on it, or skips the row. Q9, Q21, Q52, Q65, Q72, Q84, Q86, Q87, Q95
11. The re-check only looks at rows the statement's own snapshot matched; rows that newly match are not picked up. Q25, Q61, Q93
12. Reading a value, computing in the application and writing the result back loses concurrent updates under READ COMMITTED. Q13, Q31, Q64, Q83, Q95
13. A REPEATABLE READ snapshot is taken at the transaction's first statement, not at BEGIN, and covers every table. Q6, Q23, Q42, Q53, Q56, Q77, Q89, Q94, Q96, Q100
14. REPEATABLE READ reads are stable: no changed values and no new or vanished rows for the whole transaction. Q7, Q40, Q77
15. At REPEATABLE READ or above, writing or locking a row that a concurrent transaction changed and committed raises a serialization failure; if that transaction rolls back instead, the write goes ahead. Q8, Q26, Q48, Q50, Q56, Q75, Q80, Q83, Q90, Q97, Q100
16. REPEATABLE READ writes only touch rows in the snapshot, so rows committed later are silently skipped. Q20, Q47, Q66, Q75
17. Unique checks look past the snapshot: they wait for an uncommitted duplicate and fail on a committed one. Q15, Q43, Q66, Q88, Q92
18. An error aborts the whole transaction: later statements fail, COMMIT rolls back, and a retry must start again from BEGIN. Q14, Q30, Q50, Q73, Q75, Q83, Q91, Q100
19. Write skew passes REPEATABLE READ: two transactions read the same facts and change different rows. Q27, Q62, Q87
20. SERIALIZABLE tracks what transactions read and aborts one when the outcome matches no serial order; it adds no waiting. Q36, Q54, Q73, Q81, Q90, Q98
21. SERIALIZABLE only protects transactions that all run SERIALIZABLE. Q44, Q81, Q97
22. SELECT ... FOR UPDATE takes the same row lock as an update; under READ COMMITTED it returns the newest version after waiting, and under REPEATABLE READ it fails if the row changed. Q16, Q31, Q48, Q65, Q76, Q84, Q87, Q93, Q96
23. Row locks cannot lock rows that do not exist yet, so check-then-insert races. Q29, Q55, Q76, Q92, Q96, Q98
24. INSERT ... ON CONFLICT is an atomic insert-or-update under READ COMMITTED. Q28, Q57, Q80, Q88, Q99
25. NOWAIT fails instead of waiting; SKIP LOCKED leaves locked rows out. Q30, Q49, Q68, Q84
26. Lock strengths: share locks coexist, and a foreign key check takes a key-share lock that an update of non-key columns does not block. Q34, Q58, Q70, Q74
27. Deadlocks are detected after deadlock_timeout, and one transaction is rolled back so the other can go on. Q35, Q74, Q91
28. Table locks last until the transaction ends, and a waiting ALTER or DROP makes later readers queue behind it. Q33, Q59, Q78
29. Sequences ignore transactions: nextval is never rolled back and is not limited by any snapshot. Q18, Q38, Q69, Q89
30. The isolation level belongs to one transaction and must be set before its first query. Q17, Q37, Q63, Q82, Q94
31. TRUNCATE is not MVCC-safe: an older snapshot sees the truncated table as empty. Q71, Q78

---

**Q1**
Why: 1. A's UPDATE writes a new version of row 1 but has not committed, so the change is uncommitted. 2. B's SELECT reads using a snapshot, a record of which transactions had committed when the statement started; A had not, so B reads the old version, 100. 3. A plain SELECT never waits for a row lock, because it reads an older version instead of the row being written.
Answer: (a) B gets 100 immediately.
The trap: (b) comes from believing other sessions can see uncommitted data (a "dirty read"). (c) comes from believing readers wait for writers, and (d) from believing a locked row cannot be read.
Rule: other sessions see only committed data, and plain reads read around writers instead of waiting.

**Q2**
Why: 1. A's UPDATE sets row 1 to 70 inside A's open transaction. 2. Step 3 runs in the same transaction, and a transaction always sees its own changes, committed or not, so it reads 70. 3. ROLLBACK discards everything the transaction did. 4. Step 5 runs on its own after the rollback and reads the committed value, 100.
Answer: Step 3 returns 70; step 5 returns 100.
The trap: answering 100 for step 3, from the belief that a change is invisible until committed, even to the transaction that made it.
Rule: a transaction sees its own pending changes; everyone else sees them only after COMMIT.

**Q3**
Why: 1. Plain BEGIN runs at the default level, READ COMMITTED. 2. Step 2 takes a snapshot and reads 100. 3. B's UPDATE commits on its own. 4. Under READ COMMITTED each statement takes a new snapshot when it starts, so step 4's snapshot includes B's commit and reads 500.
Answer: Step 2 returns 100; step 4 returns 500.
The trap: answering 100 and 100, from the belief that a transaction freezes its view of the data at BEGIN. That is REPEATABLE READ, not the default.
Rule: under READ COMMITTED every statement sees everything committed before it started, even mid-transaction.

**Q4**
Why: 1. A never issued BEGIN, so step 1 is a transaction on its own, autocommit, and it commits when the statement ends. 2. B reads 0. 3. A's ROLLBACK finds no open transaction; PostgreSQL prints the warning "there is no transaction in progress" and does nothing. 4. B still reads 0.
Answer: Step 2 returns 0; step 4 returns 0.
The trap: answering 0 then 100, from the belief that a session's statements stay open until it says COMMIT or ROLLBACK.
Rule: without BEGIN, each statement commits the moment it finishes, and there is nothing left to roll back.

**Q5**
Why: 1. A's UPDATE takes a row lock on row 1, a marker that only one transaction may change the row at a time, held until A ends. 2. B's UPDATE needs the same row lock, so it waits. 3. When A commits or rolls back, B continues.
Answer: (a) B waits until A commits or rolls back.
The trap: (b) comes from believing writes never block and the last commit simply wins. (c) comes from believing a lock conflict is reported as an error; (d) from believing commits merge by discarding the later writer.
Rule: two transactions writing the same row run one after the other; the second waits for the first to finish.

**Q6**
Why: 1. BEGIN ISOLATION LEVEL REPEATABLE READ starts a transaction that will keep one snapshot for its whole life, but the snapshot is taken at the first statement, not at BEGIN. 2. B commits 300 before A has run anything. 3. Step 3 is A's first statement; its snapshot includes 300. 4. B commits 400 after A's snapshot. 5. Step 5 reuses the same snapshot and reads 300.
Answer: Step 3 returns 300; step 5 returns 300.
The trap: answering 100 and 100, from the belief that the snapshot is taken at BEGIN.
Rule: REPEATABLE READ freezes the data as of the transaction's first statement.

**Q7**
Why: 1. Step 2 is A's first statement, so its snapshot is taken with three rows. 2. B inserts and commits a fourth row. 3. Step 4 reuses the snapshot and counts 3; a row appearing between two reads is called a phantom, and PostgreSQL's REPEATABLE READ never shows one. 4. After COMMIT, step 6 runs as its own transaction with a new snapshot and counts 4.
Answer: 3, 3, 4.
The trap: answering 3, 4, 4, from the SQL standard's definition, which allows phantoms at REPEATABLE READ. PostgreSQL is stricter than the standard requires.
Rule: in PostgreSQL, REPEATABLE READ hides both changed values and new rows for the whole transaction.

**Q8**
Why: 1. Step 2 fixes A's snapshot, in which row 1 is 100. 2. B changes row 1 to 110 and commits after that snapshot. 3. A tries to update row 1. Under REPEATABLE READ, updating a row that another transaction changed and committed after your snapshot cannot be done without either ignoring B's change or breaking the snapshot. 4. PostgreSQL refuses with a serialization failure, an error meaning "this transaction cannot be made consistent; retry it". B has already committed, so there is nothing to wait for.
Answer: (a) ERROR: could not serialize access due to concurrent update.
The trap: (b) comes from believing REPEATABLE READ re-reads the newest value before writing, as READ COMMITTED does. (c) comes from believing the update uses the snapshot value and overwrites B. (d) comes from forgetting that B's autocommit statement has already finished.
Rule: under REPEATABLE READ, the first transaction to change a row wins, and the other gets an error to retry.

**Q9**
Why: 1. A's UPDATE sets row 1 to 110 and holds its row lock. 2. B's UPDATE finds row 1 locked and waits. 3. A commits. 4. Under READ COMMITTED, the waiting UPDATE re-reads the newest committed version of the row, 110, re-checks its WHERE clause (still id = 1) and computes bal + 20 from that version, giving 130. 5. B's statement commits on its own, and step 5 reads 130.
Answer: 130
The trap: answering 120, from the belief that B computes bal + 20 from the 100 it would have seen when its statement started.
Rule: a waiting READ COMMITTED update re-reads the row after the other transaction commits, so `SET n = n + x` updates never lose each other.

**Q10**
Why: 1. A subtracts 40 from row 1 but has not committed. 2. B's step 3 sees only committed data: 100 + 100 = 200. 3. A adds 40 to row 2, still uncommitted. 4. Step 5 again sees the committed 100 and 100, 200. 5. A commits both changes at once. 6. Step 7 sees 60 and 140, 200.
Answer: 200, 200, 200.
The trap: answering 160 for step 3 or step 5, from the belief that another session can see a transfer halfway through.
Rule: other sessions see a transaction's changes all together at COMMIT, never part of the way through.

**Q11**
Why: 1. A statement with WITH runs all its parts, the UPDATE in the WITH clause and the main SELECT, against one shared snapshot taken when the statement starts. 2. The UPDATE changes row 1 from 5 to 6 and returns the new value through RETURNING, so `u` holds 6. 3. The main query's read of `t` uses the snapshot from before the UPDATE ran and sees 5. 4. The only way to see the new value inside the statement is through RETURNING.
Answer: returned = 6, seen = 5.
The trap: answering 6 and 6, from the belief that the parts of a statement run one after another and each sees the previous part's writes.
Rule: every part of one statement reads the same snapshot, so a data-modifying WITH clause's changes are visible only through RETURNING.

**Q12**
Why: 1. A's SELECT reads row 1 and takes no row lock. 2. B's UPDATE therefore finds nothing in its way and commits immediately. 3. A is at READ COMMITTED, so step 4 takes a new snapshot that includes B's commit and reads 0.
Answer: Step 3 does not wait; step 4 returns 0.
The trap: believing that because A read the row inside a transaction, B must wait until A finishes. Reading takes no lock that blocks writers.
Rule: readers never block writers, and at READ COMMITTED a transaction's next read shows what they wrote.

**Q13**
Why: 1. A reads 100. 2. B reads 100; nothing locks the row. 3. A writes 150 and commits. 4. B writes 130, a fixed value its application computed from the 100 it read. B's UPDATE does not wait, since A has committed, and the re-check from Q9 cannot help: `SET bal = 130` does not depend on the current value. 5. B commits, and A's +50 is gone.
Answer: 130
The trap: answering 180, from the belief that wrapping read and write in a transaction makes them safe. This is called a lost update.
Rule: under READ COMMITTED, a value read and then written back by the application overwrites anything committed in between.

**Q14**
Why: 1. Step 2 sets row 1 to 10 inside the transaction. 2. Step 3 fails with "division by zero". 3. After any error, the transaction is marked aborted; step 4 is refused with "current transaction is aborted, commands ignored until end of transaction block". 4. COMMIT on an aborted transaction performs a rollback and reports ROLLBACK. 5. Step 2's change is undone, so step 6 shows the original rows.
Answer: Step 4: ERROR, current transaction is aborted. Step 5: ROLLBACK. Step 6: (1, 100), (2, 100).
The trap: expecting (1, 10), (2, 20), from the belief that only the failing statement is skipped and the others still commit.
Rule: one error poisons the whole transaction; nothing in it can commit.

**Q15**
Why: 1. A inserts id 3 without committing. 2. B inserts id 3. The primary key's unique index finds A's uncommitted row. It cannot know yet whether that row will survive, so B waits for A. 3. A rolls back, its row disappears, and B's insert succeeds with (3, 50).
Answer: (c) It waits, then succeeds when A rolls back.
The trap: (a) comes from believing unique checks see uncommitted rows as already existing. (b) comes from believing unique checks only look at committed data, which is what plain reads do; (d) ignores that the outcome depends on whether A commits.
Rule: a unique check waits for a pending duplicate and then fails only if that duplicate commits.

**Q16**
Why: 1. `SELECT ... FOR UPDATE` reads the row and takes the same row lock an UPDATE would, held until A ends. 2. B's plain SELECT takes no lock, so it is not blocked and returns the committed value, 100. 3. B's UPDATE needs the row lock A holds, so it waits until A commits or rolls back.
Answer: Only step 4 waits. Step 3 returns 100 immediately.
The trap: believing step 3 also waits because the row is "locked for update". Row locks only stop other writers and lockers.
Rule: FOR UPDATE blocks other writers and other FOR UPDATE reads, never plain SELECTs.

**Q17**
Why: 1. BEGIN opens a transaction at the default level. 2. Step 2 is its first query, and the level is fixed from that point, because the first query is when the transaction's snapshot rules take effect. 3. Changing the level now is refused with "SET TRANSACTION ISOLATION LEVEL must be called before any query", and the transaction becomes aborted.
Answer: (a) ERROR, because the level must be set before the transaction's first query.
The trap: (b) comes from believing the level can change partway through. (c) comes from believing the setting applies to the whole transaction backwards, and (d) from treating it as a hint.
Rule: choose the level in BEGIN or immediately after it, before any query.

**Q18**
Why: 1. nextval hands out the next number from the sequence and records it permanently straight away, outside the transaction, so that other sessions never wait for it. 2. A gets 1. 3. ROLLBACK does not return 1 to the sequence. 4. B gets 2.
Answer: Step 2 returns 1; step 4 returns 2.
The trap: answering 1 for step 4, from the belief that a rollback undoes nextval like any other change.
Rule: sequence numbers are never rolled back, so gaps are normal.

**Q19**
Why: 1. A's UPDATE takes the row lock on row 1. The statement finishes, but the lock stays with the transaction. 2. A sleeps while still in the transaction. 3. B's UPDATE needs the lock and waits. 4. The sleep ending changes nothing, because the transaction is still open. 5. A's COMMIT releases the lock, and B proceeds.
Answer: (c) When A commits at step 5.
The trap: (a) comes from believing locks are released when the statement that took them ends. (b) confuses the statement running with the transaction staying open; (d) assumes lock waits time out by default.
Rule: row locks are held until COMMIT or ROLLBACK, so a slow transaction blocks writers for its whole length.

**Q20**
Why: 1. Step 2 fixes A's snapshot with rows 1 and 2. 2. B inserts row 3 and commits after that snapshot. 3. A's UPDATE looks for id 3 in its snapshot, finds nothing, and reports UPDATE 0, with no error. 4. A commits. 5. Step 6 is a new transaction that sees row 3 untouched: 0.
Answer: Step 4 reports UPDATE 0; step 6 returns 0.
The trap: expecting a serialization error, from the belief that REPEATABLE READ raises an error whenever another transaction touched relevant data. Errors come only when an existing row in the snapshot was changed.
Rule: under REPEATABLE READ, rows committed after your snapshot are invisible to your updates as well as your reads.

**Q21**
Why: 1. A deletes row 1 and holds its row lock. 2. B's UPDATE finds row 1 in its snapshot, sees it locked, and waits. 3. A commits, so the row is gone. 4. Under READ COMMITTED, B looks for the newest version of the row, finds that it was deleted, and skips it. 5. B reports UPDATE 0 and no error.
Answer: It waits until A commits, then reports UPDATE 0 with no error.
The trap: expecting B to fail with an error, or to update a deleted row, from the belief that a waiting update either errors or uses the version it first saw.
Rule: a waiting READ COMMITTED write that finds its row deleted simply skips it.

**Q22**
Why: 1. B reads account 1 at step 2: 100. 2. A moves 40 and commits both changes together. 3. B is at READ COMMITTED, so step 7 takes a new snapshot and reads account 2 after the transfer: 140. 4. B's report adds 100 + 140.
Answer: 240
The trap: answering 200, from the belief that a transaction's reads are consistent with each other. Each statement here saw a consistent database, but not the same one.
Rule: under READ COMMITTED, separate statements can see different points in time, so a report built from several reads can be inconsistent.

**Q23**
Why: 1. Step 2 is A's first statement, and its snapshot covers the whole database, not just the table it read. 2. B inserts into `orders` and commits after that snapshot. 3. Step 4 reads `orders` with the same snapshot and counts the three original rows.
Answer: 3
The trap: answering 4, from the belief that each table gets its own snapshot the first time the transaction reads it.
Rule: a REPEATABLE READ snapshot freezes every table at once, at the first statement.

**Q24**
Why: 1. A inserts a row without committing. 2. PostgreSQL accepts READ UNCOMMITTED but runs it as READ COMMITTED, so step 4 sees only committed rows: 3. 3. A commits. 4. Step 6 takes a new snapshot and counts 4.
Answer: Step 4 returns 3; step 6 returns 4.
The trap: answering 4 for step 4, from the belief that READ UNCOMMITTED shows uncommitted rows as the SQL standard permits.
Rule: PostgreSQL never shows uncommitted data at any level; READ UNCOMMITTED is READ COMMITTED.

**Q25**
Why: 1. A adds 1 to both rows but has not committed: 10 and 11 are pending. 2. B's DELETE takes its snapshot before A commits, so it sees 9 and 10. Only row 2 matches `hits = 10`. 3. Row 2 is locked by A, so B waits. 4. A commits. B re-checks row 2's newest version, 11, which no longer matches, so B skips it. 5. Row 1 is now 10, but B's snapshot saw 9 there, so B never considered it. 6. B deletes nothing.
Answer: Step 3 deletes 0 rows; step 5 returns (1, 10), (2, 11).
The trap: expecting row 1 to be deleted, from the belief that after waiting B re-runs its whole search against the new data.
Rule: a READ COMMITTED re-check only re-tests the rows its own snapshot matched; rows that only match later are never found.

**Q26**
Why: 1. Step 2 fixes A's snapshot with row 1 at 100. 2. B changes row 1 to 0 without committing. 3. A's UPDATE needs row 1, which B has locked, so A waits. 4. B rolls back, so row 1 is still the version in A's snapshot. 5. With no concurrent change to object to, A's update proceeds on 100 and makes it 101. 6. A commits.
Answer: Step 5 waits, then succeeds when B rolls back; the balance is 101.
The trap: expecting a serialization error as soon as B touched the row, from the belief that a concurrent attempt is enough to fail. Only a concurrent change that commits causes the error.
Rule: under REPEATABLE READ, a write waiting on another transaction fails only if that transaction commits.

**Q27**
Why: 1. Both snapshots show two people on duty, so both applications go ahead. 2. A changes ann's row and B changes bo's row; they touch different rows, so neither waits and neither hits the error from Q8. 3. Both commit, and nobody is on duty. This pattern is called write skew: two transactions read the same facts and each change a different row, breaking a rule that spans both rows.
Answer: (a) 0
The trap: (b) comes from believing REPEATABLE READ catches any conflict between overlapping transactions; it only catches two writes to the same row. (c) applies READ COMMITTED's wait-and-re-check to rows nobody else locked, and (d) assumes one update is lost.
Rule: REPEATABLE READ allows write skew; a rule that spans several rows needs SERIALIZABLE or an explicit lock.

**Q28**
Why: 1. A inserts ('x', 1) without committing. 2. B's upsert finds a pending row with the same key and waits for A. 3. A commits, so the key now exists. 4. B's ON CONFLICT DO UPDATE takes the conflict branch and updates the committed row, so n becomes 1 + 1 = 2. Under READ COMMITTED this happens even though B's statement snapshot predates A's commit.
Answer: 2
The trap: answering 1, or expecting a duplicate key error, from the belief that ON CONFLICT only sees rows committed before the statement started.
Rule: under READ COMMITTED, INSERT ... ON CONFLICT always ends in either an insert or an update, never an error.

**Q29**
Why: 1. A's locking SELECT finds no rows, so it locks nothing. 2. B's locking SELECT also finds no rows and has nothing to wait for. 3. Both applications see an empty result and insert. 4. The table has no constraint to stop a second identical row, and the two inserts do not conflict.
Answer: Step 4 does not wait; there are 2 bookings.
The trap: believing FOR UPDATE locks "the condition" so that the second transaction waits. A row lock needs a row to attach to.
Rule: FOR UPDATE cannot lock a row that does not exist yet; preventing duplicates needs a unique constraint, a lock on some existing row, or SERIALIZABLE.

**Q30**
Why: 1. A locks row 1. 2. B asks for the same lock with NOWAIT, which means "fail instead of waiting", so step 4 fails at once with "could not obtain lock on row in relation jobs". 3. That error aborts B's transaction. 4. Step 5 is refused with "current transaction is aborted", although row 2 is free.
Answer: Step 4: ERROR, could not obtain lock on row. Step 5: ERROR, current transaction is aborted.
The trap: expecting step 5 to return 2, from the belief that a NOWAIT failure is a harmless "no" that leaves the transaction usable.
Rule: NOWAIT turns a lock wait into an error, and that error aborts the transaction like any other.

**Q31**
Why: 1. A reads 100 and locks row 1. 2. B's locking read needs the same lock and waits. 3. A writes 150 and commits, releasing the lock. 4. Under READ COMMITTED, B's waiting FOR UPDATE returns the newest committed version of the row, 150, not the 100 it would have read when it started. 5. B's application writes 150 + 30 = 180 and commits.
Answer: Step 4 returns 150 (after waiting for A's commit); the final balance is 180.
The trap: expecting step 4 to return 100, from the belief that a locking read returns its snapshot's value even after waiting.
Rule: read with FOR UPDATE before an application-side read-modify-write, and the second request waits and then sees the first one's result.

**Q32**
Why: 1. One statement takes one snapshot when it starts, and it reads every row against that snapshot however long it runs. 2. B's 10 inserted rows committed after the snapshot, so A's scan does not count them. 3. B's 50 deletions also committed after the snapshot, so the old versions still count as visible to A.
Answer: 1,000,000
The trap: answering 999,960, or a number in between, from the belief that a long scan sees changes as it reaches them.
Rule: a single statement sees the database as it was when the statement started, from beginning to end.

**Q33**
Why: 1. A's SELECT takes a table lock on `orders` in ACCESS SHARE mode, the weakest mode, and keeps it until A's transaction ends. 2. ALTER TABLE needs ACCESS EXCLUSIVE mode, which conflicts with every other mode, so B waits for A. 3. C's SELECT needs ACCESS SHARE, which conflicts with the ACCESS EXCLUSIVE that B is waiting for, so C queues behind B rather than slipping past it. 4. When A commits, B runs, and then C returns 3.
Answer: Both wait. B waits for A, and C waits behind B. After step 5, B's ALTER completes and then C's count returns 3.
The trap: expecting C to return at once, from the belief that reads never block. A waiting schema change makes even plain reads queue.
Rule: a schema change waiting behind a long transaction blocks every later query on that table.

**Q34**
Why: 1. A's UPDATE changes `name`, which is not part of any key, so it takes the weaker row lock FOR NO KEY UPDATE. 2. B's insert must check that parent 1 exists, and the foreign key check locks the parent row in FOR KEY SHARE mode, which only conflicts with changes to the row's key or its deletion. 3. The two modes are compatible, so B's insert completes at once.
Answer: No, step 3 completes immediately.
The trap: believing B waits because the parent row is being updated, from the belief that any update locks the row against all other lockers.
Rule: updating a row's non-key columns does not block inserts of children that reference it.

**Q35**
Why: 1. A locks row 1; B locks row 2. 2. A waits for row 2, held by B. 3. B waits for row 1, held by A. Each is waiting for the other, which is a deadlock. 4. A waiting session checks for deadlocks once it has waited deadlock_timeout, 1 second by default. 5. PostgreSQL rolls back one transaction with "deadlock detected", releasing its locks, and the other's waiting UPDATE then completes.
Answer: (b) About a second later one transaction fails with a deadlock error and is rolled back, and the other's waiting update completes.
The trap: (a) comes from believing the database leaves deadlocks for the application to notice. (c) comes from believing the check runs the moment the second wait begins, and (d) from believing both sides must be punished.
Rule: in a deadlock PostgreSQL sacrifices one transaction, so the application must be ready to retry it.

**Q36**
Why: 1. A reads class 1's sum, 30, then inserts into class 2. B reads class 2's sum, 300, then inserts into class 1. 2. If A had run first, B's sum would have included A's 30 and been 330. If B had run first, A's sum would have been 330. 3. No order of running them one at a time gives both 30 and 300, so the result is not serializable. 4. SERIALIZABLE, implemented in PostgreSQL as Serializable Snapshot Isolation (SSI), records what each transaction read and detects this pattern. It aborts one transaction with a serialization failure. With these steps that is normally B, at COMMIT. Once one is aborted the other is consistent, so it commits.
Answer: (b) Exactly one of them fails with a serialization error.
The trap: (a) comes from believing SERIALIZABLE only stops two writes to the same row. (c) comes from believing SERIALIZABLE works by making transactions wait for each other, and (d) from believing it aborts every party.
Rule: SERIALIZABLE lets transactions run concurrently and aborts one when their reads and writes match no serial order.

**Q37**
Why: 1. Step 1 runs outside any transaction block. SET TRANSACTION only affects the current transaction, and there is none, so PostgreSQL prints the warning "SET TRANSACTION can only be used in transaction blocks" and does nothing. 2. BEGIN starts a transaction at the default level. 3. SHOW reports it.
Answer: read committed
The trap: answering serializable, from the belief that SET TRANSACTION sets the level for the next transaction.
Rule: SET TRANSACTION works only inside a transaction; to change later transactions use BEGIN ISOLATION LEVEL or SET SESSION CHARACTERISTICS.

**Q38**
Why: 1. A's nextval returns 1. 2. B's nextval returns 2. 3. A's snapshot has no effect on sequences: nextval always reads the sequence's current state, so A gets 3.
Answer: 1, 2, 3.
The trap: answering 1, 2, 2 or expecting A to get 2, from the belief that a REPEATABLE READ transaction's sequence is frozen with its snapshot.
Rule: sequences sit outside isolation; every nextval in every session gets a fresh, unique number.

**Q39**
Why: 1. Without BEGIN, step 1 is its own transaction and commits at once: account 1 is 50. 2. B's SELECT sees 50 + 100. 3. Step 3 then commits on its own, too late for B's read.
Answer: 150
The trap: answering 200, from the belief that a session's consecutive statements form one unit even without BEGIN.
Rule: changes that must become visible together need to be inside one BEGIN ... COMMIT.

**Q40**
Why: 1. Step 2 fixes A's snapshot with both rows. 2. B deletes row 2 and commits after the snapshot. 3. Step 4 reads row 2 from the snapshot, where it still exists: 100. 4. After COMMIT, step 6 is a new transaction and finds no row.
Answer: Step 4 returns 100; step 6 returns no rows.
The trap: expecting step 4 to return no rows or an error, from the belief that a deletion committed by another session removes rows from an open REPEATABLE READ view.
Rule: under REPEATABLE READ, rows deleted after your snapshot stay visible to you until your transaction ends.

**Q41**
Why: 1. A locks row 1 with bal 0 pending. 2. Step 3 updates row 2, which nobody has locked: no wait; it commits. 3. Step 4's snapshot sees row 1 as 100 (A has not committed) and row 2 as 0. Row 1 matches `bal = 100`. 4. To update row 1, B needs A's lock, so it waits until A ends. If A commits, B's re-check finds 0 and skips the row.
Answer: Step 3 does not wait; step 4 waits until A commits or rolls back.
The trap: expecting step 4 not to wait, from the belief that only an update naming the same id can collide. Any statement whose snapshot matches the locked row waits for it.
Rule: a write waits on every row it matches in its snapshot, whatever column it searched by.

**Q42**
Why: 1. Step 2 fixes A's snapshot: 100 + 100 = 200. 2. B sets row 2 to 0 and commits after the snapshot. 3. A updates row 1, which B never touched, so there is no conflict: row 1 becomes 500 in A's transaction. 4. Step 5 combines A's own change, 500, with the snapshot's row 2, 100.
Answer: Step 2 returns 200; step 5 returns 600.
The trap: answering 500, from the belief that writing in a REPEATABLE READ transaction refreshes its view to the latest data.
Rule: a REPEATABLE READ transaction sees its snapshot plus its own changes, nothing else.

**Q43**
Why: 1. A inserts id 3 without committing. 2. B's count cannot see uncommitted rows: 0. 3. B's insert hits A's pending row in the unique index and waits. 4. A commits, so the duplicate is now real, and B's insert fails with "duplicate key value violates unique constraint acct_pkey".
Answer: Step 4 returns 0; step 5 waits, then fails with a duplicate key error after A commits.
The trap: expecting step 5 to succeed because step 4 saw no row, from the belief that the unique check uses the same view as SELECT.
Rule: the unique check sees all rows, committed or pending, even when your SELECT does not.

**Q44**
Why: 1. B uses a plain BEGIN, so it runs READ COMMITTED. 2. The two transactions do the same write skew as Q27. 3. SSI only records reads and checks writes for SERIALIZABLE transactions. B's read is not recorded, and B's write is not checked against A's read. 4. On its own side, A sees no dangerous pattern, so both commit, leaving nobody on duty.
Answer: 0
The trap: answering 1, from the belief that one SERIALIZABLE transaction protects itself against everyone.
Rule: SERIALIZABLE protects only against other SERIALIZABLE transactions; every transaction that touches the data must use it.

**Q45**
Why: 1. A's UPDATE matches row 1 and writes a new version with the same value. PostgreSQL does not skip updates that change nothing. 2. Writing the row takes its row lock until A ends. 3. B's UPDATE needs the lock and waits.
Answer: Yes, step 3 waits until A commits or rolls back.
The trap: believing a no-op update takes no lock, because "nothing changed".
Rule: any row an UPDATE matches is locked until the transaction ends, even if its values are unchanged.

**Q46**
Why: 1. Step 2 counts three orders. 2. B inserts a fourth order of 10 and commits. 3. Step 4 is a new statement with a new snapshot (READ COMMITTED) and sums all four: 10 + 20 + 30 + 10 = 70. 4. The report divides 70 by 3.
Answer: 23.33 (70 / 3). The true average was 20 before the insert and 17.5 after.
The trap: answering 20, from the belief that statements in one transaction see the same data.
Rule: to compute related figures consistently, take them in one statement or run the transaction at REPEATABLE READ.

**Q47**
Why: 1. Step 2 fixes A's snapshot with three rows. 2. B inserts row 4 and commits after it. 3. A's `DELETE FROM orders` with no WHERE deletes every row in its snapshot, rows 1 to 3. Row 4 is not in the snapshot, so it is untouched, without error. 4. After COMMIT, step 6 finds row 4.
Answer: 1
The trap: answering 0, from the belief that an unqualified DELETE removes whatever is in the table when it runs.
Rule: under REPEATABLE READ, even "all rows" means all rows in your snapshot.

**Q48**
Why: 1. Step 2 fixes A's snapshot with job 1 as 'new'. 2. B changes it to 'done' and commits. 3. A's plain read uses the snapshot and returns 'new'. 4. A's locking read must lock the current row version, which was changed after the snapshot. Under REPEATABLE READ that is the same conflict as an update and raises a serialization failure.
Answer: Step 4 returns 'new'; step 5 fails with "could not serialize access due to concurrent update".
The trap: expecting step 5 to return 'done', from the belief that FOR UPDATE returns the latest version at every level. It does so only at READ COMMITTED.
Rule: at REPEATABLE READ, locking a row changed since your snapshot is a serialization failure.

**Q49**
Why: 1. A's query finds job 1 first in id order, locks it and stops at LIMIT 1. 2. B's query also reaches job 1 first. SKIP LOCKED means that a row another transaction has locked is left out instead of waited for. 3. B moves on to job 2, locks it and stops.
Answer: A gets 1 and B gets 2; neither waits.
The trap: expecting B to wait for job 1, or to get no rows, from the belief that SKIP LOCKED applies only before the LIMIT has been decided.
Rule: SKIP LOCKED lets workers share a queue: each one takes the next row nobody else holds.

**Q50**
Why: 1. Step 4 fails with a serialization failure, because B changed row 1 after A's snapshot. 2. That error aborts A's transaction, so step 5, the "retry", is refused with "current transaction is aborted". 3. COMMIT rolls back. 4. Step 7 runs as a new transaction and sees B's committed 0.
Answer: Step 5: ERROR, current transaction is aborted. Step 6: ROLLBACK. Step 7: 0.
The trap: expecting step 5 to succeed and give 1, from the belief that a serialization error can be retried statement by statement.
Rule: retry a serialization failure by rolling back and re-running the whole transaction from BEGIN, reads included.

**Q51**
Why: 1. A's 1,000 inserts are all inside one uncommitted transaction, so every count B takes before the commit sees 3. 2. A commit becomes visible as one event: a snapshot either includes the committing transaction or does not. 3. Every count after the commit sees 1003.
Answer: (a) Only 3 and 1003.
The trap: (b) comes from believing other sessions see rows as they are written. (c) comes from believing COMMIT publishes rows gradually, and (d) from believing rows are written out to other sessions after commit.
Rule: other sessions see a whole transaction's work at one instant, however much work it did.

**Q52**
Why: 1. A's UPDATE matches job 1 ('new'), sets 'taken' and holds the lock. 2. B's snapshot also sees 'new' and matches, but must wait for A's lock. 3. A commits. 4. B re-checks the newest version: status is 'taken', so `status = 'new'` is false and B skips it. 5. B reports UPDATE 0, which tells its worker the job was claimed.
Answer: B waits until A commits, then reports UPDATE 0.
The trap: expecting UPDATE 1, so that both workers think they claimed the job, from the belief that B applies its change to the version it saw first.
Rule: a conditional UPDATE is a safe claim under READ COMMITTED, because the waiting writer re-tests the condition.

**Q53**
Why: 1. BEGIN does not take A's snapshot. 2. B commits row 1 = 10. 3. Step 3 is A's first statement, so A's snapshot is taken now and includes 10. A updates row 2, which B never changes, to 101. 4. B commits row 1 = 20 after A's snapshot. 5. Step 5 shows row 1 from the snapshot, 10, and row 2 with A's own change, 101.
Answer: (1, 10), (2, 101).
The trap: answering (1, 100) from the belief that the snapshot is taken at BEGIN, or (1, 20) from the belief that a write refreshes the snapshot.
Rule: a transaction's first statement takes its snapshot, whether that statement reads or writes.

**Q54**
Why: 1. A's SERIALIZABLE read records an SIREAD lock, a note of what A read; it blocks nobody. 2. B's UPDATE does not wait and commits. 3. A's step 4 uses its snapshot: 100. 4. There is one dependency: A read a version that B later replaced, so A must come before B in a serial order. One edge is not a cycle, and A, which only read, commits normally.
Answer: Step 3 does not wait; step 4 returns 100; step 5 commits successfully.
The trap: expecting step 3 to wait, from the belief that SERIALIZABLE works by locking what you read.
Rule: SERIALIZABLE reads never block writers; it only aborts transactions whose combined pattern is impossible to serialize.

**Q55**
Why: 1. Both counts return 2, so both applications insert. 2. Inserts of new rows do not conflict with each other: there is no shared row to lock and no unique constraint. 3. READ COMMITTED does not re-check counts already returned. 4. Both commit, so event 1 has 2 + 2 = 4 seats.
Answer: 4
The trap: answering 3, from the belief that a transaction automatically checks that its earlier reads are still true when it commits.
Rule: under READ COMMITTED, a check made by reading is out of date the moment it returns, unless something locks what it relied on.

**Q56**
Why: 1. B commits row 1 = 0 before A has run a statement. 2. Step 3 is A's first statement, so the snapshot includes B's change. 3. Step 4 updates row 1, whose current version is already in A's snapshot; no transaction changed it after the snapshot, so there is no conflict. It becomes 0 + 5 = 5. 4. A commits.
Answer: Step 4 succeeds; the balance is 5.
The trap: expecting a serialization error because B changed the row "during" A's transaction. The error only arises for changes committed after the snapshot.
Rule: what counts as concurrent under REPEATABLE READ is set by the snapshot, not by BEGIN.

**Q57**
Why: 1. A inserts 'y' without committing. 2. B's insert finds the pending key and waits for A to finish, because whether there is a conflict depends on A's fate. 3. A rolls back, so there is no conflict. 4. B inserts ('y', 5).
Answer: 5
The trap: expecting B to do nothing at once and step 5 to return no row, from the belief that ON CONFLICT DO NOTHING treats a pending row as an existing one without waiting.
Rule: an upsert waits for a pending duplicate, then inserts or takes the conflict branch depending on whether it committed.

**Q58**
Why: 1. A takes a FOR SHARE lock on row 1: "nobody may change this row while I rely on it". 2. Share locks are compatible with each other, so B's FOR SHARE succeeds at once. 3. B's UPDATE needs a stronger lock that conflicts with A's share lock, so it waits until A ends. B's own share lock does not stop B.
Answer: Step 4 does not wait; step 5 waits until A commits or rolls back.
The trap: believing step 5 goes ahead because B already holds a lock on the row. A share lock is not exclusive, and another holder still blocks changes.
Rule: FOR SHARE lets many readers lock a row together, and any one of them blocks every writer.

**Q59**
Why: 1. A's SELECT on `orders` took an ACCESS SHARE table lock. 2. Table locks, like row locks, are held until the transaction ends, not until the statement ends. 3. A is still in its transaction, idle. 4. DROP TABLE needs ACCESS EXCLUSIVE, which conflicts with A's lock, so B waits until A commits or rolls back.
Answer: Yes, step 4 waits until A's transaction ends.
The trap: believing the lock went away when step 2 finished, from the belief that reads hold table locks only while they run.
Rule: any table a transaction has touched stays locked against schema changes until the transaction ends, so idle transactions block migrations.

**Q60**
Why: 1. The INSERT's SELECT reads `nums` with the statement's snapshot, so it does not see rows the same statement is adding. 2. It reads 1, 2 and 3 and inserts 11, 12 and 13, then stops. 3. The table now has six rows.
Answer: 6
The trap: expecting an endless loop or a much larger count, from the belief that a statement reads the rows it has just written.
Rule: a statement never sees its own writes while it runs, so copying a table into itself is safe.

**Q61**
Why: 1. A sets row 1 to 'new' (no change in value, but the row is locked) and row 2 to 'new', and inserts row 3, all uncommitted. 2. B's snapshot sees row 1 'new', row 2 'done' and no row 3. Only row 1 matches. 3. Row 1 is locked by A, so B waits. 4. A commits. B re-checks row 1, still 'new', and sets it to 'held'. 5. Row 2 now says 'new', but B's snapshot saw 'done' and did not consider it; row 3 was not in the snapshot.
Answer: (1, 'held'), (2, 'new'), (3, 'new').
The trap: expecting all three to be 'held', from the belief that after waiting, B sees A's committed data and searches again.
Rule: after waiting, a READ COMMITTED write updates only rows its original snapshot matched.

**Q62**
Why: 1. Both snapshots show a sum of 200, so both withdrawals pass the check. 2. A changes row 1 and B changes row 2: different rows, so no wait and no first-updater error. 3. Both commit: -50 + -50.
Answer: -100
The trap: answering 50, from the belief that REPEATABLE READ guards a check made by reading.
Rule: REPEATABLE READ does not stop two transactions from each acting on a sum that the other is changing.

**Q63**
Why: 1. The REPEATABLE READ level applied only to the first transaction, which ended at step 2. 2. The plain BEGIN at step 3 starts at the default, READ COMMITTED. 3. Step 4 reads 100. 4. B commits 1. 5. Step 6 takes a new snapshot and reads 1.
Answer: Step 4 returns 100; step 6 returns 1.
The trap: answering 100 and 100, from the belief that a level set with BEGIN stays in force for the session.
Rule: BEGIN ISOLATION LEVEL lasts for one transaction; the next BEGIN starts at the default.

**Q64**
Why: 1. Under READ COMMITTED both requests can read the same old balance before either writes. 2. Each then writes a fixed value based on that old balance, and the second overwrites the first. 3. `SET bal = bal + :amount` makes the database compute from the current value. A second writer waits for the first and re-reads the newest version before adding, as in Q9. 4. The transaction alone, a second read, or READ UNCOMMITTED, which behaves as READ COMMITTED, all leave the gap between read and write.
Answer: (a)
The trap: (b) comes from believing a transaction isolates read-then-write by itself. (c) comes from believing seeing pending writes would help, and PostgreSQL does not show them anyway; (d) from believing a later read closes the window instead of narrowing it.
Rule: let the database do the arithmetic in the UPDATE, or lock the row when you read it.

**Q65**
Why: 1. A sets job 1 to 'done' and holds its lock. 2. B's snapshot sees both jobs as 'new', so both match. Job 2 is free and B locks it. Job 1 is locked by A, so B waits. 3. A commits. B re-checks job 1's newest version, 'done', which no longer matches, so B leaves it out. 4. B's statement returns only job 2.
Answer: It waits until A commits, then returns only 2.
The trap: expecting it to return 1 and 2, from the belief that FOR UPDATE returns the rows its snapshot matched, whatever happened while it waited.
Rule: under READ COMMITTED, a locking read re-tests each row it had to wait for and drops rows that no longer match.

**Q66**
Why: 1. Step 2 fixes A's snapshot with ids 1 and 2. 2. B inserts id 3 and commits. 3. Step 4 reads with the snapshot: 0. 4. Step 5's unique check does not use the snapshot; it finds B's committed id 3 and fails with "duplicate key value violates unique constraint acct_pkey".
Answer: Step 4 returns 0; step 5 fails with a duplicate key error.
The trap: expecting step 5 to succeed, from the belief that everything inside REPEATABLE READ follows the snapshot, constraints included.
Rule: constraints are checked against the real current data, even when your snapshot shows something older.

**Q67**
Why: 1. A's UPDATE reads row 1 (bal 100), tests `bal > 500`, and finds it false. 2. A row is only locked when a write actually applies to it; a row that fails the WHERE is not locked. 3. A holds no lock on row 1, so B's update completes at once.
Answer: No, step 3 completes immediately.
The trap: believing an UPDATE locks every row it looks at, from the belief that its WHERE clause locks the rows it searched.
Rule: an UPDATE locks only the rows it changes.

**Q68**
Why: 1. A's UPDATE locks job 1, setting 'running' without committing. 2. B's snapshot sees job 1 as 'new', so it matches. SKIP LOCKED finds it locked and leaves it out: 0 rows, at once. 3. B's plain SELECT ignores locks and sees the committed 'new': it returns 1.
Answer: Step 3 returns no rows; step 4 returns 1.
The trap: expecting step 3 to return 1, from the belief that SKIP LOCKED skips only rows locked with FOR UPDATE. A row being updated is locked too.
Rule: SKIP LOCKED hides rows any other transaction is writing, so it can disagree with a plain read of the same data.

**Q69**
Why: 1. A's insert calls nextval and gets id 1, uncommitted. 2. B's insert gets id 2 and commits. 3. C's max(id) sees only committed rows: 2. The poller stores 2. 4. A commits id 1 after C's read. 5. C asks for ids above 2; id 1 is lower, so it is not returned now or on any later poll.
Answer: Step 4 returns 2; step 6 returns no rows, and the poller never sees 'a'.
The trap: believing ids appear in increasing order, from the belief that sequence numbers are handed out in commit order.
Rule: sequence values follow when nextval ran, not when the row committed, so "rows after the last id I saw" can skip rows forever.

**Q70**
Why: 1. A deletes parent 1, which locks the row in the mode that conflicts with key-share locks. 2. B's foreign key check tries to lock parent 1 in FOR KEY SHARE and must wait. 3. A commits; the parent row is gone. 4. B's check finds no parent and fails with "insert or update on table child violates foreign key constraint".
Answer: It waits until A commits, then fails with a foreign key violation.
The trap: expecting B to succeed because it saw parent 1 before A committed, from the belief that the check uses the version it saw first.
Rule: a foreign key check waits for a pending delete of the parent and then judges by its outcome.

**Q71**
Why: 1. Step 2 fixes A's snapshot for every table, but A has taken a table lock only on `acct`. 2. B's TRUNCATE needs ACCESS EXCLUSIVE on `orders`; nobody holds a lock there, so it runs at once and commits. 3. TRUNCATE does not mark rows as deleted the way DELETE does; it swaps in a new, empty file for the table. 4. A's snapshot cannot find any old rows to show, so step 4 sees an empty table.
Answer: Step 3 does not wait; step 4 returns 0.
The trap: answering 3, from the belief that REPEATABLE READ preserves every table as of the snapshot whatever command changed it.
Rule: TRUNCATE is not MVCC-safe: a transaction with an older snapshot sees the truncated table as empty.

**Q72**
Why: 1. A's update matches row 1 (100 >= 80), sets 20 and holds the lock. 2. B's update matches in its snapshot (100) but waits for the lock. 3. A commits. 4. B re-checks the newest version: 20 >= 80 is false, so it skips the row and reports UPDATE 0. 5. B's application can see the withdrawal failed.
Answer: B waits until A commits, then reports UPDATE 0; the final balance is 20.
The trap: expecting -60, from the belief that B's condition was satisfied when it started and so stays satisfied.
Rule: putting the check in the UPDATE's WHERE clause makes it safe under READ COMMITTED, because a waiting writer re-tests it.

**Q73**
Why: 1. As in Q27, both read two on duty and each changes a different row. 2. Under SERIALIZABLE, SSI detects that each read what the other later changed, a cycle, and fails one; here, B. 3. B's work is rolled back, and A's commit leaves ann off duty. 4. B's retry starts a fresh transaction whose snapshot includes A's commit: the count is 1. 5. B's rule forbids going off duty, so it changes nothing. Bo stays on duty.
Answer: The retry's count returns 1; 1 person (bo) is on duty.
The trap: expecting the retry to fail again or to go ahead, from the belief that a retry repeats the same decision. A retry is only correct if it re-reads.
Rule: SERIALIZABLE turns write skew into an error, and re-running the whole transaction then makes the right decision.

**Q74**
Why: 1. A and B both hold FOR SHARE on row 1, which is allowed. 2. A's UPDATE needs a lock that conflicts with B's share lock, so A waits for B. 3. B's UPDATE conflicts with A's share lock, so B waits for A. 4. Each waits for the other, a deadlock. After deadlock_timeout one is rolled back with "deadlock detected", its share lock is released, and the other's update completes.
Answer: (c)
The trap: (a) comes from believing that holding a share lock entitles you to update. (b) comes from believing the later writer gets through first; (d) from believing a share lock makes writes fail instead of wait.
Rule: two transactions that share-lock a row and then both try to update it will deadlock; lock with FOR UPDATE from the start if you mean to write.

**Q75**
Why: 1. Step 2 fixes A's snapshot with rows 1 and 2 at 100. 2. B inserts row 3 and changes row 2, both committed after the snapshot. 3. A's UPDATE without WHERE visits its snapshot's rows. Row 1 is fine. Row 2 was changed after the snapshot, so the statement fails with a serialization failure and its change to row 1 is undone. Row 3 is never seen. 4. COMMIT rolls back. 5. Step 7 is a new transaction and sees B's data.
Answer: Step 5: ERROR, could not serialize access due to concurrent update. Step 6: ROLLBACK. Step 7: (1, 100), (2, 0), (3, 0).
The trap: expecting (1, 101) to survive, from the belief that the rows processed before the failing one stay updated.
Rule: one conflicting row fails the whole statement, and the error then fails the whole transaction.

**Q76**
Why: 1. A locks the event row, counts 2 and decides to insert. 2. B's lock on the same event row waits for A. 3. A inserts and commits, releasing the lock. 4. B gets the lock. Because B is at READ COMMITTED, step 8 takes a new snapshot after A's commit and counts 3. 5. B's rule says do not insert, so event 1 stays at 3.
Answer: Step 8 returns 3; event 1 ends with 3 seats.
The trap: expecting 4, from the belief that locking the event row does nothing because the seats are in another table. The lock serializes the two check-and-insert sequences.
Rule: when a rule covers rows that may not exist yet, lock an existing parent row that every writer must lock first.

**Q77**
Why: 1. B's BEGIN does not take a snapshot. 2. A subtracts 40 from row 1 without committing. 3. Step 4 is B's first statement, so B's snapshot is taken now. A is still running, so its changes are not in it: 100. 4. A adds 40 to row 2 and commits. 5. Step 7 reuses B's snapshot, which excludes A: 100. 6. B's two reads add to 200, which is consistent. At READ COMMITTED they would give 100 + 140 = 240.
Answer: Step 4 returns 100; step 7 returns 100.
The trap: answering 140 for step 7, from the belief that A's commit counts because it came after B's BEGIN but before the read.
Rule: a REPEATABLE READ transaction excludes everything not committed when its first statement ran, so all its reads agree with each other.

**Q78**
Why: 1. Step 2 makes A take an ACCESS SHARE table lock on `orders`, held until A ends. 2. TRUNCATE needs ACCESS EXCLUSIVE, so B waits. 3. A already holds its lock, so step 4 needs no new lock, does not queue behind B, and reads its snapshot: 3. 4. When A commits, B's TRUNCATE runs.
Answer: Step 3 waits until A commits; step 4 returns 3.
The trap: answering 0, from carrying over Q71's result. The TRUNCATE cannot run while A holds a lock on the table, so A never sees it.
Rule: a transaction that has already read a table holds a lock that keeps TRUNCATE out until it ends; the empty-table effect hits only transactions that had not touched the table.

**Q79**
Why: 1. A's statement takes its snapshot when it starts, with both rows at 100. 2. B's transfer commits two seconds later, while A is still asleep on its first row. 3. A goes on reading rows with its original snapshot, so the row it reaches after B's commit still shows the old version. 4. Whatever order the rows come back in, A shows 100 and 100.
Answer: Both rows show 100.
The trap: expecting the second row to show the new value (60 or 140), from the belief that a slow statement picks up commits as it reaches each row.
Rule: one statement's result reflects one moment, however long the statement takes.

**Q80**
Why: 1. Step 2 fixes A's snapshot with no row 'z'. 2. B inserts 'z' and commits. 3. A's insert hits B's committed 'z' in the unique index, so it takes the ON CONFLICT DO UPDATE branch. 4. The row it would update is not visible in A's REPEATABLE READ snapshot. Updating a row A cannot see would break the snapshot, so PostgreSQL fails the statement with a serialization failure.
Answer: ERROR: could not serialize access due to concurrent update.
The trap: expecting n to become 2, from carrying READ COMMITTED's upsert behavior from Q28 over to REPEATABLE READ.
Rule: under REPEATABLE READ, an upsert that conflicts with a row committed after your snapshot is a serialization failure, not an update.

**Q81**
Why: 1. The steps are Q36's, which SERIALIZABLE would reject. 2. But B runs at REPEATABLE READ, so SSI does not record B's read, and B's insert is not checked against A's read. 3. B's insert into class 1, which A read, is therefore never checked against A's read, and A's insert into class 2 meets no recorded read. SSI sees no dependency at all. 4. The two inserts are different rows, so nothing else stops them. Both commit.
Answer: Both commit.
The trap: expecting one to fail, from the belief that the SERIALIZABLE side protects the pair.
Rule: SSI catches anomalies only among SERIALIZABLE transactions; one participant at a lower level is enough for the anomaly to commit.

**Q82**
Why: 1. Step 1 changes the default for every later transaction in A's session to REPEATABLE READ. 2. A has no BEGIN, so step 2 is its own transaction, at REPEATABLE READ, and reads 100. It commits at once. 3. B commits 5. 4. Step 4 is another single-statement transaction with a new snapshot: 5.
Answer: Step 2 returns 100; step 4 returns 5.
The trap: answering 100 and 100, from the belief that the session level makes all its reads repeatable. Repeatable means within one transaction, and in autocommit each statement is a transaction.
Rule: an isolation level only protects statements grouped in one transaction; in autocommit every statement starts over.

**Q83**
Why: 1. Both snapshots show 100. 2. A writes 150 and commits. 3. B's UPDATE targets a row changed and committed after B's snapshot, so under REPEATABLE READ it fails with a serialization failure instead of overwriting A. 4. B rolls back and retries from BEGIN; its new snapshot reads 150. 5. B writes 150 + 30 = 180 and commits.
Answer: 180
The trap: answering 130, from the belief that REPEATABLE READ lets the last writer win as READ COMMITTED does.
Rule: REPEATABLE READ turns a lost update into an error, and a full retry turns the error into the correct result.

**Q84**
Why: 1. A's query locks job 1 and stops at LIMIT 1. 2. B's query reaches job 1 first and waits for A's lock. 3. A marks job 1 'done' and commits. 4. B re-checks job 1's newest version: 'done' no longer matches, so B drops it and continues to the next row its snapshot matched, job 2. Job 2 is free; B locks it and returns it.
Answer: B waits until A commits at step 6, then returns 2.
The trap: expecting 1 (both workers run job 1), from the belief that a locking read returns its snapshot's row after waiting. Expecting no rows comes from the belief that the LIMIT was used up by the row that was dropped.
Rule: without SKIP LOCKED a queue still hands out each job once under READ COMMITTED, but workers wait in line; SKIP LOCKED removes the wait.

**Q85**
Why: 1. The subquery reads `acct` with the statement's snapshot, from before any row is changed: 200. 2. Row 1 becomes 100 + 200 = 300. 3. Row 2 becomes 100 + 200 = 300; the subquery does not see row 1's new value, because a statement never sees its own changes.
Answer: (1, 300), (2, 300).
The trap: answering (2, 500), from the belief that the update processes rows one by one and each later row sees the earlier ones' new values.
Rule: everything a statement reads comes from before the statement changed anything.

**Q86**
Why: 1. A sets row 1 to 50, uncommitted. 2. B's snapshot sees rows 1 and 2 as 100; both match `bal < 200`. 3. Row 2 is free: B doubles it to 200. 4. Row 1 is locked, so B waits. 5. A commits. B re-checks row 1's newest version: 50 < 200 still matches, so B doubles 50 to 100. 6. B's statement commits.
Answer: (1, 100), (2, 200).
The trap: answering (1, 200), from the belief that B doubles the 100 it saw first and overwrites A's 50.
Rule: a waiting READ COMMITTED update re-tests and recomputes from the newest version of each row it waited for.

**Q87**
Why: 1. A locks both on-duty rows and sees two. 2. B's locking read waits for A's locks. 3. A sets ann off duty and commits, releasing both locks. 4. B re-checks each row: ann is no longer on duty and is dropped; bo still matches and is locked. 5. B's application counts one row and does not go off duty.
Answer: Step 4 returns only 'bo' (after A commits); 1 person ends on duty.
The trap: expecting both names, from the belief that B's locking read returns what its snapshot matched.
Rule: locking the rows a decision depends on turns write skew into a wait, and READ COMMITTED's re-check then hands the second transaction the new facts.

**Q88**
Why: 1. A inserts id 5, uncommitted. 2. B's count cannot see it: 0. 3. B's insert finds A's pending row in the unique index and waits. 4. A commits, so the conflict is real, and DO NOTHING skips the insert: INSERT 0 0, no error. 5. Step 6 reads A's committed row: 0.
Answer: Step 3 returns 0. Step 4 waits, then inserts nothing (INSERT 0 0). Step 6 returns 0.
The trap: expecting step 6 to return 1, from the belief that B's insert went ahead because B's count found no row.
Rule: reads ignore pending rows, but unique checks wait for them, so one transaction can "see" a row that its SELECT cannot.

**Q89**
Why: 1. Step 2 fixes A's snapshot with an empty table. 2. B's insert takes id 1 from the sequence and commits. 3. A's insert calls nextval, which ignores snapshots, and gets id 2. 4. Step 5 sees A's own row but not B's committed row, which is outside A's snapshot: one row, max 2.
Answer: Step 4 returns 2; step 5 returns count 1, max 2.
The trap: expecting step 4 to return 1, from the belief that the sequence is frozen with A's empty snapshot.
Rule: sequences hand out numbers across all snapshots, so a transaction can hold id 2 while its snapshot shows no id 1.

**Q90**
Why: 1. A updates row 1 and holds the lock. 2. B's UPDATE is its first statement, so B's snapshot is taken now, without A's change; it then waits for A's lock. SERIALIZABLE does not remove ordinary row-lock waits. 3. A commits a change to a row that B's snapshot holds at the old version. 4. As at REPEATABLE READ, B fails with a serialization failure.
Answer: It waits until A commits, then fails with "could not serialize access due to concurrent update".
The trap: expecting B to wait and then succeed with 102, as at READ COMMITTED, from the belief that SERIALIZABLE only adds checks at COMMIT.
Rule: at SERIALIZABLE, a same-row write conflict behaves as at REPEATABLE READ: wait for the other writer, then fail if it commits.

**Q91**
Why: 1. A locks row 1, and B locks row 2. 2. B waits for row 1; A waits for row 2. This is a deadlock. 3. The detector rolls back B, undoing its +10 on row 2 and releasing its lock. 4. A's waiting update now completes: row 2 becomes 101. 5. A's COMMIT keeps both of its changes. B's COMMIT finds an aborted transaction and reports ROLLBACK.
Answer: (1, 101), (2, 101).
The trap: expecting B's +10 on row 2 to survive, from the belief that a deadlock only cancels the statement that was waiting.
Rule: a deadlock victim loses its whole transaction, and the survivor continues as if the victim had never run.

**Q92**
Why: 1. Both counts see no booking. 2. A inserts. 3. B's insert finds A's pending row in the unique index on (room, day) and waits. 4. A commits, so B's insert fails with a duplicate key error and B's transaction is aborted. 5. B's COMMIT rolls back.
Answer: Step 6 waits, then fails with a duplicate key error when A commits; 1 booking exists.
The trap: expecting 2 bookings as in Q29, from the belief that a unique constraint, like a lock, cannot protect rows that do not exist yet. The index entry acts as a lock on the key itself.
Rule: a unique constraint is the dependable guard against check-then-insert races, at any isolation level.

**Q93**
Why: 1. A sets job 1 to 'done' and job 2 to 'new', both uncommitted and locked. 2. B's snapshot sees job 1 'new' (match) and job 2 'done' (no match). 3. B waits for job 1's lock. 4. A commits. B re-checks job 1: 'done', no match, dropped. 5. Job 2 was not matched in B's snapshot, so B never looks at it again.
Answer: No rows.
The trap: expecting 2, from the belief that a locking read that waited sees the database as it is after the other transaction's commit.
Rule: a READ COMMITTED locking read can return nothing even though matching rows exist by the time it returns, because it re-tests only rows it first matched.

**Q94**
Why: 1. BEGIN opens a transaction. 2. SET TRANSACTION comes before any query, so it is accepted and the transaction is REPEATABLE READ. 3. B commits 1. 4. Step 4 is A's first query, so A's snapshot is taken now and includes 1. 5. B commits 2 after the snapshot. 6. Step 6 reuses the snapshot: 1.
Answer: 1 and 1.
The trap: answering 100 and 100, from the belief that the snapshot was taken at BEGIN or at SET TRANSACTION.
Rule: SET TRANSACTION right after BEGIN works, and the snapshot still waits for the first real query.

**Q95**
Why: 1. B reads 100 and takes no lock. 2. A's atomic increment commits at once: 110. 3. B's UPDATE does not wait, because A has committed. Its value 95 is a constant from the application, so the READ COMMITTED re-check has nothing to recompute. 4. B commits 95, and A's +10 is lost.
Answer: 95
The trap: answering 105, from the belief that A's atomic update is protected whatever other code does.
Rule: atomic updates protect only against each other; one read-then-write path on the same row can overwrite them.

**Q96**
Why: 1. A locks the event row and counts 2. 2. B's locking read is B's first statement, so B's snapshot is taken at step 5, before A commits. It waits for A's lock. 3. A inserts a seat and commits. A only locked the event row and never changed it, so B gets the lock without a serialization error. 4. Step 8 counts seats with B's snapshot, which excludes A's insert: 2. 5. B inserts, so event 1 ends with 4.
Answer: Step 8 returns 2; event 1 ends with 4 seats.
The trap: answering 3 as in Q76, from the belief that waiting for the lock means B's later reads see what A committed. At REPEATABLE READ, the snapshot was fixed before the wait.
Rule: at REPEATABLE READ, a lock taken after the snapshot cannot refresh it. Have the first transaction change the parent row, so the second fails and retries, or use SERIALIZABLE.

**Q97**
Why: 1. Step 2 fixes A's snapshot with row 1 at 100. 2. B's READ COMMITTED update commits 0 after that snapshot. 3. A updates row 1, whose current version was committed after A's snapshot. The first-updater rule depends only on A's own level, so A fails with a serialization failure. SSI's limit to SERIALIZABLE transactions concerns read-write patterns, not same-row writes.
Answer: ERROR: could not serialize access due to concurrent update.
The trap: expecting the update to succeed (-10 or 90), from the belief that because B is not SERIALIZABLE, A gets no protection at all.
Rule: same-row write conflicts are detected whatever level the other writer used; only read-write anomalies need everyone at SERIALIZABLE.

**Q98**
Why: 1. Both counts find nothing, and SSI records that each read the range "room 7 on that day". 2. Each then inserts into the range the other read, so each read missed the other's write: a dependency in both directions. 3. No serial order gives both an empty count, so SSI fails one with a serialization failure, normally B at COMMIT. 4. One booking remains.
Answer: (c) Exactly one fails with a serialization error, leaving 1 booking.
The trap: (a) comes from believing SERIALIZABLE, like FOR UPDATE, cannot protect rows that do not exist yet. (b) comes from believing SERIALIZABLE makes transactions wait; (d) from believing there is a constraint where there is none.
Rule: SERIALIZABLE tracks the conditions you searched for, not just the rows you found, so it can catch check-then-insert races that locks cannot.

**Q99**
Why: 1. A inserts 'q' = 1, uncommitted. 2. A's upsert finds a conflict with its own pending row. There is nobody to wait for, so it takes the DO UPDATE branch and sets n to 2. 3. B cannot see A's uncommitted row: no rows. 4. A commits. 5. B now reads 2.
Answer: Step 3 updates the row to n = 2 without waiting; step 4 returns no rows; step 6 returns 2.
The trap: expecting step 3 to wait or fail, from the belief that a conflict with an uncommitted row always means waiting. The pending row is A's own.
Rule: a transaction's own pending rows count as existing for itself: it reads, updates and conflicts with them without waiting.

**Q100**
Why: 1. Step 2 fixes A's snapshot with row 1 at 100. 2. Step 4 fails, which aborts the work done since savepoint s. 3. B commits row 1 = 0. 4. ROLLBACK TO SAVEPOINT s clears the error, and the transaction is usable again, but it keeps its original snapshot. 5. Step 7 reads 100. 6. Step 8 updates a row changed and committed after the snapshot: serialization failure.
Answer: Step 7 returns 100; step 8 fails with "could not serialize access due to concurrent update".
The trap: expecting step 7 to return 0 and step 8 to succeed, from the belief that rolling back to a savepoint refreshes the transaction's view.
Rule: a savepoint can recover from an ordinary error but not from a stale snapshot; a serialization failure needs a full retry from BEGIN.

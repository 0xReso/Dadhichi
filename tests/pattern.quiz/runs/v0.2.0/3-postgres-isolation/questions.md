SQL transaction isolation levels in PostgreSQL · depth high · 100 questions
Assumptions: PostgreSQL 16 with default settings (default isolation READ COMMITTED, deadlock_timeout 1 s, no lock or statement timeouts). Each session (A, B, C) is its own connection and runs in autocommit mode unless it has issued BEGIN. Steps run in the numbered order; a blocked step stays blocked while later steps of other sessions run, and its session sends nothing more until it finishes. Tables hold exactly the rows given, `id` is the primary key, and no other sessions are active.

## Band 1 · One mechanism at a time

**Q1** · `acct(id int primary key, bal int)` holds (1, 100), (2, 100). What happens at step 3?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 0 WHERE id = 1;
3  B: SELECT bal FROM acct WHERE id = 1;
```

(a) B gets 100 immediately (b) B gets 0 immediately (c) B waits until A commits or rolls back (d) B gets an error because the row is locked

**Q2** · `acct` holds (1, 100), (2, 100). What do steps 3 and 5 return?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal - 30 WHERE id = 1;
3  A: SELECT bal FROM acct WHERE id = 1;
4  A: ROLLBACK;
5  A: SELECT bal FROM acct WHERE id = 1;
```

**Q3** · `acct` holds (1, 100), (2, 100). What do steps 2 and 4 return?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 500 WHERE id = 1;
4  A: SELECT bal FROM acct WHERE id = 1;
5  A: COMMIT;
```

**Q4** · `acct` holds (1, 100), (2, 100). What do steps 2 and 4 return?

```sql
1  A: UPDATE acct SET bal = 0 WHERE id = 1;
2  B: SELECT bal FROM acct WHERE id = 1;
3  A: ROLLBACK;
4  B: SELECT bal FROM acct WHERE id = 1;
```

**Q5** · `acct` holds (1, 100), (2, 100). What happens at step 3?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 50 WHERE id = 1;
3  B: UPDATE acct SET bal = 70 WHERE id = 1;
```

(a) B waits until A commits or rolls back (b) B succeeds immediately, and whichever transaction commits last wins (c) B gets an error because the row is locked (d) B succeeds immediately, but its change is discarded when A commits

**Q6** · `acct` holds (1, 100), (2, 100). What do steps 3 and 5 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  B: UPDATE acct SET bal = 300 WHERE id = 1;
3  A: SELECT bal FROM acct WHERE id = 1;
4  B: UPDATE acct SET bal = 400 WHERE id = 1;
5  A: SELECT bal FROM acct WHERE id = 1;
6  A: COMMIT;
```

**Q7** · `orders(id int primary key, amt int)` holds three rows. What do steps 2, 4 and 6 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM orders;
3  B: INSERT INTO orders VALUES (4, 10);
4  A: SELECT count(*) FROM orders;
5  A: COMMIT;
6  A: SELECT count(*) FROM orders;
```

**Q8** · `acct` holds (1, 100), (2, 100). What happens at step 4?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = bal + 10 WHERE id = 1;
4  A: UPDATE acct SET bal = bal + 20 WHERE id = 1;
```

(a) ERROR: could not serialize access due to concurrent update (b) it succeeds and row 1 becomes 130 (c) it succeeds and row 1 becomes 120 (d) it waits for B to finish

**Q9** · `acct` holds (1, 100), (2, 100). What does step 5 return?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal + 10 WHERE id = 1;
3  B: UPDATE acct SET bal = bal + 20 WHERE id = 1;
4  A: COMMIT;
5  B: SELECT bal FROM acct WHERE id = 1;
```

**Q10** · `acct` holds (1, 100), (2, 100). A moves 40 from account 1 to account 2. What do steps 3, 5 and 7 return?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal - 40 WHERE id = 1;
3  B: SELECT sum(bal) FROM acct;
4  A: UPDATE acct SET bal = bal + 40 WHERE id = 2;
5  B: SELECT sum(bal) FROM acct;
6  A: COMMIT;
7  B: SELECT sum(bal) FROM acct;
```

**Q11** · `t(id int primary key, n int)` holds (1, 5). What does this single statement return?

```sql
WITH u AS (
  UPDATE t SET n = n + 1 WHERE id = 1 RETURNING n
)
SELECT (SELECT n FROM u)               AS returned,
       (SELECT n FROM t WHERE id = 1) AS seen;
```

**Q12** · `acct` holds (1, 100), (2, 100). Does step 3 wait, and what does step 4 return?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 0 WHERE id = 1;
4  A: SELECT bal FROM acct WHERE id = 1;
```

**Q13** · `acct` holds (1, 100), (2, 100). Two requests each add money to account 1: the application reads the balance, adds in its own code, and writes the result. What is account 1's balance at the end?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1;       -- app reads the value
3  B: BEGIN;
4  B: SELECT bal FROM acct WHERE id = 1;       -- app reads the value
5  A: UPDATE acct SET bal = 150 WHERE id = 1;  -- value it read + 50
6  A: COMMIT;
7  B: UPDATE acct SET bal = 130 WHERE id = 1;  -- value it read + 30
8  B: COMMIT;
```

**Q14** · `acct` holds (1, 100), (2, 100). What do steps 4, 5 and 6 produce?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 10 WHERE id = 1;
3  A: SELECT 1/0;
4  A: UPDATE acct SET bal = 20 WHERE id = 2;
5  A: COMMIT;
6  A: SELECT id, bal FROM acct ORDER BY id;
```

**Q15** · `acct` holds (1, 100), (2, 100). What happens to B's step 3?

```sql
1  A: BEGIN;
2  A: INSERT INTO acct VALUES (3, 0);
3  B: INSERT INTO acct VALUES (3, 50);
4  A: ROLLBACK;
```

(a) It fails at once with a duplicate key error (b) It succeeds at once, and A would have failed had it committed (c) It waits, then succeeds when A rolls back (d) It waits, then fails with a duplicate key error

**Q16** · `acct` holds (1, 100), (2, 100). Which of B's steps wait, and what does step 3 return?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1 FOR UPDATE;
3  B: SELECT bal FROM acct WHERE id = 1;
4  B: UPDATE acct SET bal = 0 WHERE id = 1;
```

**Q17** · `acct` holds (1, 100), (2, 100). What happens at step 3?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1;
3  A: SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

(a) ERROR, because the level must be set before the transaction's first query (b) it succeeds, and the rest of the transaction runs at REPEATABLE READ (c) it succeeds, and step 2's read is treated as REPEATABLE READ too (d) it is silently ignored

**Q18** · `s` is a newly created sequence. What do steps 2 and 4 return?

```sql
1  A: BEGIN;
2  A: SELECT nextval('s');
3  A: ROLLBACK;
4  B: SELECT nextval('s');
```

**Q19** · `acct` holds (1, 100), (2, 100). When does B's step 4 finish?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 90 WHERE id = 1;
3  A: SELECT pg_sleep(30);
4  B: UPDATE acct SET bal = 80 WHERE id = 1;
5  A: COMMIT;
```

(a) Immediately, because A's UPDATE statement has already finished (b) When A's sleep ends (c) When A commits at step 5 (d) Never: it fails with a lock error

**Q20** · `acct` holds (1, 100), (2, 100). What do steps 4 and 6 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM acct;
3  B: INSERT INTO acct VALUES (3, 0);
4  A: UPDATE acct SET bal = 1 WHERE id = 3;
5  A: COMMIT;
6  A: SELECT bal FROM acct WHERE id = 3;
```

## Band 2 · Mechanisms in less obvious settings

**Q21** · `acct` holds (1, 100), (2, 100). What happens to B's step 3?

```sql
1  A: BEGIN;
2  A: DELETE FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = bal + 5 WHERE id = 1;
4  A: COMMIT;
```

**Q22** · `acct` holds (1, 100), (2, 100). B builds a report from steps 2 and 7. What do those two reads add up to?

```sql
1  B: BEGIN;
2  B: SELECT bal FROM acct WHERE id = 1;
3  A: BEGIN;
4  A: UPDATE acct SET bal = bal - 40 WHERE id = 1;
5  A: UPDATE acct SET bal = bal + 40 WHERE id = 2;
6  A: COMMIT;
7  B: SELECT bal FROM acct WHERE id = 2;
8  B: COMMIT;
```

**Q23** · `acct` holds (1, 100), (2, 100); `orders` holds three rows. What does step 4 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: INSERT INTO orders VALUES (4, 10);
4  A: SELECT count(*) FROM orders;
```

**Q24** · `orders` holds three rows. What do steps 4 and 6 return?

```sql
1  A: BEGIN;
2  A: INSERT INTO orders VALUES (9, 99);
3  B: BEGIN ISOLATION LEVEL READ UNCOMMITTED;
4  B: SELECT count(*) FROM orders;
5  A: COMMIT;
6  B: SELECT count(*) FROM orders;
```

**Q25** · `site(id int primary key, hits int)` holds (1, 9), (2, 10). What does step 5 return, and how many rows did step 3 delete?

```sql
1  A: BEGIN;
2  A: UPDATE site SET hits = hits + 1;
3  B: DELETE FROM site WHERE hits = 10;
4  A: COMMIT;
5  B: SELECT id, hits FROM site ORDER BY id;
```

**Q26** · `acct` holds (1, 100), (2, 100). What happens at step 5, and what is account 1's balance after step 7?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: BEGIN;
4  B: UPDATE acct SET bal = 0 WHERE id = 1;
5  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
6  B: ROLLBACK;
7  A: COMMIT;
```

**Q27** · `oncall(name text primary key, on_duty bool)` holds ('ann', true), ('bo', true). The rule is that at least one person stays on duty, so each application goes off duty only if its count is 2 or more. Both counts return 2. How many people are on duty at the end?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM oncall WHERE on_duty;
3  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
4  B: SELECT count(*) FROM oncall WHERE on_duty;
5  A: UPDATE oncall SET on_duty = false WHERE name = 'ann';
6  B: UPDATE oncall SET on_duty = false WHERE name = 'bo';
7  A: COMMIT;
8  B: COMMIT;
```

(a) 0 (b) 1, because B's step 6 fails with a serialization error (c) 1, because B's step 6 waits and then updates no rows (d) 2

**Q28** · `counter(k text primary key, n int)` is empty. What does step 5 return?

```sql
1  A: BEGIN;
2  A: INSERT INTO counter VALUES ('x', 1)
        ON CONFLICT (k) DO UPDATE SET n = counter.n + 1;
3  B: INSERT INTO counter VALUES ('x', 1)
        ON CONFLICT (k) DO UPDATE SET n = counter.n + 1;
4  A: COMMIT;
5  B: SELECT n FROM counter WHERE k = 'x';
```

**Q29** · `booking(room int, day date)` has no constraints and no rows. Each application inserts only if its locking SELECT returns no rows. Does step 4 wait, and how many bookings exist for room 7 at the end?

```sql
1  A: BEGIN;
2  A: SELECT * FROM booking WHERE room = 7 AND day = '2026-12-01' FOR UPDATE;
3  B: BEGIN;
4  B: SELECT * FROM booking WHERE room = 7 AND day = '2026-12-01' FOR UPDATE;
5  A: INSERT INTO booking VALUES (7, '2026-12-01');
6  B: INSERT INTO booking VALUES (7, '2026-12-01');
7  A: COMMIT;
8  B: COMMIT;
```

**Q30** · `jobs(id int primary key, status text)` holds (1, 'new'), (2, 'new'). What do steps 4 and 5 produce?

```sql
1  A: BEGIN;
2  A: SELECT id FROM jobs WHERE id = 1 FOR UPDATE;
3  B: BEGIN;
4  B: SELECT id FROM jobs WHERE id = 1 FOR UPDATE NOWAIT;
5  B: SELECT id FROM jobs WHERE id = 2 FOR UPDATE;
```

**Q31** · `acct` holds (1, 100), (2, 100). This time both requests lock the row when they read it. What value does step 4 hand to B's application, and what is the final balance?

```sql
1  A: BEGIN;
2  A: SELECT bal FROM acct WHERE id = 1 FOR UPDATE;  -- app reads the value
3  B: BEGIN;
4  B: SELECT bal FROM acct WHERE id = 1 FOR UPDATE;  -- app reads the value
5  A: UPDATE acct SET bal = 150 WHERE id = 1;       -- value it read + 50
6  A: COMMIT;
7  B: UPDATE acct SET bal = ? WHERE id = 1;         -- value it read + 30
8  B: COMMIT;
```

**Q32** · `events` holds 1,000,000 rows. Session A runs a single `SELECT count(*) FROM events;` that takes 20 seconds. Five seconds in, session B inserts 10 rows and commits. Ten seconds in, B deletes 50 rows that A's scan has not reached yet and commits. What count does A get?

**Q33** · `orders` holds three rows. What happens at steps 3 and 4, and when do they finish?

```sql
1  A: BEGIN;
2  A: SELECT count(*) FROM orders;
3  B: ALTER TABLE orders ADD COLUMN note text;
4  C: SELECT count(*) FROM orders;
5  A: COMMIT;
```

**Q34** · `parent(id int primary key, name text)` holds (1, 'p'). `child(id int primary key, parent_id int REFERENCES parent(id))` is empty. Does step 3 wait?

```sql
1  A: BEGIN;
2  A: UPDATE parent SET name = 'q' WHERE id = 1;
3  B: INSERT INTO child VALUES (10, 1);
```

**Q35** · `acct` holds (1, 100), (2, 100). Steps are a fraction of a second apart. What happens after step 6?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 0 WHERE id = 1;
3  B: BEGIN;
4  B: UPDATE acct SET bal = 0 WHERE id = 2;
5  A: UPDATE acct SET bal = 1 WHERE id = 2;
6  B: UPDATE acct SET bal = 1 WHERE id = 1;
```

(a) Both sessions wait forever (b) About a second later one transaction fails with a deadlock error and is rolled back, and the other's waiting update completes (c) Step 6 fails at once (d) Both transactions are rolled back

**Q36** · `mytab(class int, value int)` holds (1, 10), (1, 20), (2, 100), (2, 200). What is the outcome of steps 7 and 8?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT sum(value) FROM mytab WHERE class = 1;
3  B: BEGIN ISOLATION LEVEL SERIALIZABLE;
4  B: SELECT sum(value) FROM mytab WHERE class = 2;
5  A: INSERT INTO mytab VALUES (2, 30);
6  B: INSERT INTO mytab VALUES (1, 300);
7  A: COMMIT;
8  B: COMMIT;
```

(a) Both commit (b) Exactly one of them fails with a serialization error (c) B's step 6 waits for A, then both commit (d) Both fail

**Q37** · What does step 3 return?

```sql
1  A: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
2  A: BEGIN;
3  A: SHOW transaction_isolation;
```

**Q38** · `s` is a newly created sequence. What do steps 2, 3 and 4 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT nextval('s');
3  B: SELECT nextval('s');
4  A: SELECT nextval('s');
```

**Q39** · `acct` holds (1, 100), (2, 100). A moves 50 from account 1 to account 2 but never issues BEGIN. What does step 2 return?

```sql
1  A: UPDATE acct SET bal = bal - 50 WHERE id = 1;
2  B: SELECT sum(bal) FROM acct;
3  A: UPDATE acct SET bal = bal + 50 WHERE id = 2;
```

**Q40** · `acct` holds (1, 100), (2, 100). What do steps 4 and 6 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM acct;
3  B: DELETE FROM acct WHERE id = 2;
4  A: SELECT bal FROM acct WHERE id = 2;
5  A: COMMIT;
6  A: SELECT bal FROM acct WHERE id = 2;
```

**Q41** · `acct` holds (1, 100), (2, 100). Does step 3 wait? Does step 4 wait?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 0 WHERE id = 1;
3  B: UPDATE acct SET bal = 0 WHERE id = 2;
4  B: UPDATE acct SET bal = 5 WHERE bal = 100;
```

**Q42** · `acct` holds (1, 100), (2, 100). What do steps 2 and 5 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT sum(bal) FROM acct;
3  B: UPDATE acct SET bal = 0 WHERE id = 2;
4  A: UPDATE acct SET bal = 500 WHERE id = 1;
5  A: SELECT sum(bal) FROM acct;
```

**Q43** · `acct` holds (1, 100), (2, 100). What do steps 4 and 5 produce?

```sql
1  A: BEGIN;
2  A: INSERT INTO acct VALUES (3, 0);
3  B: BEGIN;
4  B: SELECT count(*) FROM acct WHERE id = 3;
5  B: INSERT INTO acct VALUES (3, 50);
6  A: COMMIT;
```

**Q44** · `oncall` holds ('ann', true), ('bo', true), and each application goes off duty only if its count is 2 or more. Both counts return 2. A runs SERIALIZABLE; B uses a plain BEGIN. How many people are on duty at the end?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT count(*) FROM oncall WHERE on_duty;
3  B: BEGIN;
4  B: SELECT count(*) FROM oncall WHERE on_duty;
5  A: UPDATE oncall SET on_duty = false WHERE name = 'ann';
6  B: UPDATE oncall SET on_duty = false WHERE name = 'bo';
7  A: COMMIT;
8  B: COMMIT;
```

**Q45** · `acct` holds (1, 100), (2, 100). A's update does not change any value. Does step 3 wait?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal WHERE id = 1;
3  B: UPDATE acct SET bal = 7 WHERE id = 1;
```

**Q46** · `orders` holds (1, 10), (2, 20), (3, 30). A's report divides the sum by the count to get an average order amount. What average does it compute?

```sql
1  A: BEGIN;
2  A: SELECT count(*) FROM orders;
3  B: INSERT INTO orders VALUES (4, 10);
4  A: SELECT sum(amt) FROM orders;
5  A: COMMIT;
```

**Q47** · `orders` holds three rows. What does step 6 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM orders;
3  B: INSERT INTO orders VALUES (4, 10);
4  A: DELETE FROM orders;
5  A: COMMIT;
6  A: SELECT count(*) FROM orders;
```

**Q48** · `jobs` holds (1, 'new'), (2, 'new'). What do steps 4 and 5 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM jobs;
3  B: UPDATE jobs SET status = 'done' WHERE id = 1;
4  A: SELECT status FROM jobs WHERE id = 1;
5  A: SELECT status FROM jobs WHERE id = 1 FOR UPDATE;
```

**Q49** · `jobs` holds (1, 'new'), (2, 'new'), (3, 'new'). What do steps 2 and 4 return, and does either wait?

```sql
1  A: BEGIN;
2  A: SELECT id FROM jobs WHERE status = 'new'
        ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
3  B: BEGIN;
4  B: SELECT id FROM jobs WHERE status = 'new'
        ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
```

**Q50** · `acct` holds (1, 100), (2, 100). A's application catches the error from step 4 and retries just that statement at step 5. What do steps 5, 6 and 7 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 0 WHERE id = 1;
4  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
5  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
6  A: COMMIT;
7  A: SELECT bal FROM acct WHERE id = 1;
```

**Q51** · `orders` holds three rows. Session A inserts 1,000 rows inside one transaction, one INSERT statement per row, then commits. Meanwhile session B, in autocommit mode, runs `SELECT count(*) FROM orders;` every few milliseconds. Which counts can B observe?

(a) Only 3 and 1003 (b) Any number from 3 to 1003 (c) Any number from 3 to 1003, but only while A's COMMIT is running (d) Only 3 until A's transaction finishes, then any number up to 1003 as the rows are written out

**Q52** · `jobs` holds (1, 'new'), (2, 'new'). Two workers try to claim job 1. What does B's step 3 report, and when?

```sql
1  A: BEGIN;
2  A: UPDATE jobs SET status = 'taken' WHERE id = 1 AND status = 'new';
3  B: UPDATE jobs SET status = 'taken' WHERE id = 1 AND status = 'new';
4  A: COMMIT;
```

**Q53** · `acct` holds (1, 100), (2, 100). What does step 5 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  B: UPDATE acct SET bal = 10 WHERE id = 1;
3  A: UPDATE acct SET bal = bal + 1 WHERE id = 2;
4  B: UPDATE acct SET bal = 20 WHERE id = 1;
5  A: SELECT id, bal FROM acct ORDER BY id;
```

**Q54** · `acct` holds (1, 100), (2, 100). Does step 3 wait? What do steps 4 and 5 produce?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 0 WHERE id = 1;
4  A: SELECT bal FROM acct WHERE id = 1;
5  A: COMMIT;
```

**Q55** · `seat(event int, who text)` holds two rows for event 1. An event holds at most 3 people, so each application inserts only if its count is below 3. How many rows does event 1 have at the end?

```sql
1  A: BEGIN;
2  A: SELECT count(*) FROM seat WHERE event = 1;
3  B: BEGIN;
4  B: SELECT count(*) FROM seat WHERE event = 1;
5  A: INSERT INTO seat VALUES (1, 'a');
6  B: INSERT INTO seat VALUES (1, 'b');
7  A: COMMIT;
8  B: COMMIT;
```

**Q56** · `acct` holds (1, 100), (2, 100). What happens at step 4, and what is account 1's balance after step 5?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  B: UPDATE acct SET bal = 0 WHERE id = 1;
3  A: SELECT bal FROM acct WHERE id = 2;
4  A: UPDATE acct SET bal = bal + 5 WHERE id = 1;
5  A: COMMIT;
```

**Q57** · `counter(k text primary key, n int)` is empty. What does step 5 return?

```sql
1  A: BEGIN;
2  A: INSERT INTO counter VALUES ('y', 1) ON CONFLICT DO NOTHING;
3  B: INSERT INTO counter VALUES ('y', 5) ON CONFLICT DO NOTHING;
4  A: ROLLBACK;
5  B: SELECT n FROM counter WHERE k = 'y';
```

**Q58** · `acct` holds (1, 100), (2, 100). Does step 4 wait? Does step 5 wait?

```sql
1  A: BEGIN;
2  A: SELECT * FROM acct WHERE id = 1 FOR SHARE;
3  B: BEGIN;
4  B: SELECT * FROM acct WHERE id = 1 FOR SHARE;
5  B: UPDATE acct SET bal = 0 WHERE id = 1;
```

**Q59** · `orders` and `acct` exist. A's last statement on `orders` finished long ago, and A is now idle. Does step 4 wait?

```sql
1  A: BEGIN;
2  A: SELECT count(*) FROM orders;
3  A: SELECT bal FROM acct WHERE id = 1;
4  B: DROP TABLE orders;
```

**Q60** · `nums(n int)` holds 1, 2, 3. What does step 2 return?

```sql
1  A: INSERT INTO nums SELECT n + 10 FROM nums;
2  A: SELECT count(*) FROM nums;
```

**Q61** · `jobs` holds (1, 'new'), (2, 'done'). What does step 6 return?

```sql
1  A: BEGIN;
2  A: UPDATE jobs SET status = 'new' WHERE id IN (1, 2);
3  A: INSERT INTO jobs VALUES (3, 'new');
4  B: UPDATE jobs SET status = 'held' WHERE status = 'new';
5  A: COMMIT;
6  B: SELECT id, status FROM jobs ORDER BY id;
```

**Q62** · `acct` holds (1, 100), (2, 100), two accounts of one couple. The bank allows either account to go negative as long as the two together stay at 0 or above, so each application withdraws 150 only if the sum minus 150 is not negative. Both sums return 200. What is the combined balance at the end?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT sum(bal) FROM acct;
3  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
4  B: SELECT sum(bal) FROM acct;
5  A: UPDATE acct SET bal = bal - 150 WHERE id = 1;
6  B: UPDATE acct SET bal = bal - 150 WHERE id = 2;
7  A: COMMIT;
8  B: COMMIT;
```

**Q63** · `acct` holds (1, 100), (2, 100). What do steps 4 and 6 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: COMMIT;
3  A: BEGIN;
4  A: SELECT bal FROM acct WHERE id = 1;
5  B: UPDATE acct SET bal = 1 WHERE id = 1;
6  A: SELECT bal FROM acct WHERE id = 1;
```

**Q64** · Two requests run this code at the same time under READ COMMITTED, and one of the additions is sometimes lost.

```sql
BEGIN;
SELECT bal FROM acct WHERE id = 1;        -- app computes new = bal + amount
UPDATE acct SET bal = :new WHERE id = 1;
COMMIT;
```

Which single change stops additions from being lost?

(a) Replace both statements with `UPDATE acct SET bal = bal + :amount WHERE id = 1;` (b) Nothing is needed, since the statements already run inside one transaction (c) Run the transaction at READ UNCOMMITTED so each request sees the other's pending write (d) Run the SELECT a second time just before the UPDATE

**Q65** · `jobs` holds (1, 'new'), (2, 'new'). What does step 3 return, and when?

```sql
1  A: BEGIN;
2  A: UPDATE jobs SET status = 'done' WHERE id = 1;
3  B: SELECT id FROM jobs WHERE status = 'new' FOR UPDATE;
4  A: COMMIT;
```

**Q66** · `acct` holds (1, 100), (2, 100). What do steps 4 and 5 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM acct;
3  B: INSERT INTO acct VALUES (3, 0);
4  A: SELECT count(*) FROM acct WHERE id = 3;
5  A: INSERT INTO acct VALUES (3, 9);
```

**Q67** · `acct` holds (1, 100), (2, 100). Does step 3 wait?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 0 WHERE id = 1 AND bal > 500;
3  B: UPDATE acct SET bal = 1 WHERE id = 1;
```

**Q68** · `jobs` holds (1, 'new'). What do steps 3 and 4 return?

```sql
1  A: BEGIN;
2  A: UPDATE jobs SET status = 'running' WHERE id = 1;
3  B: SELECT id FROM jobs WHERE status = 'new' FOR UPDATE SKIP LOCKED;
4  B: SELECT id FROM jobs WHERE status = 'new';
```

**Q69** · `items(id serial primary key, name text)` is empty and its sequence is fresh. C is a poller that remembers the highest id it has seen and later asks only for rows above it. What does step 4 return, and does step 6 return item 'a'?

```sql
1  A: BEGIN;
2  A: INSERT INTO items(name) VALUES ('a');
3  B: INSERT INTO items(name) VALUES ('b');
4  C: SELECT max(id) FROM items;
5  A: COMMIT;
6  C: SELECT id, name FROM items WHERE id > 2;
```

**Q70** · `parent` holds (1, 'p'); `child(id int primary key, parent_id int REFERENCES parent(id))` is empty. What happens to step 3?

```sql
1  A: BEGIN;
2  A: DELETE FROM parent WHERE id = 1;
3  B: INSERT INTO child VALUES (11, 1);
4  A: COMMIT;
```

## Band 3 · Combinations and edge cases

**Q71** · `acct` holds (1, 100), (2, 100); `orders` holds three rows. Does step 3 wait, and what does step 4 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: TRUNCATE orders;
4  A: SELECT count(*) FROM orders;
```

**Q72** · `acct` holds (1, 100), (2, 100). Two withdrawals of 80 race on account 1. What does B's step 4 report, and what is the final balance?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal - 80 WHERE id = 1 AND bal >= 80;
3  B: BEGIN;
4  B: UPDATE acct SET bal = bal - 80 WHERE id = 1 AND bal >= 80;
5  A: COMMIT;
6  B: COMMIT;
```

**Q73** · `oncall` holds ('ann', true), ('bo', true). Both transactions run SERIALIZABLE, and each goes off duty only if its count is 2 or more. Both counts return 2. Exactly one transaction fails; assume it is B. B's application then retries its whole transaction from BEGIN. What does the retry's count return, and how many people are on duty at the end?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT count(*) FROM oncall WHERE on_duty;
3  B: BEGIN ISOLATION LEVEL SERIALIZABLE;
4  B: SELECT count(*) FROM oncall WHERE on_duty;
5  A: UPDATE oncall SET on_duty = false WHERE name = 'ann';
6  B: UPDATE oncall SET on_duty = false WHERE name = 'bo';
7  A: COMMIT;
8  B: COMMIT;
```

**Q74** · `acct` holds (1, 100), (2, 100). Steps are a fraction of a second apart. What happens after step 6?

```sql
1  A: BEGIN;
2  A: SELECT * FROM acct WHERE id = 1 FOR SHARE;
3  B: BEGIN;
4  B: SELECT * FROM acct WHERE id = 1 FOR SHARE;
5  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
6  B: UPDATE acct SET bal = bal + 2 WHERE id = 1;
```

(a) Both updates complete, and the balance ends at 103 after both commit (b) Step 5 waits; step 6 completes, and A's update follows once B commits (c) Both updates wait on each other; about a second later one transaction fails with a deadlock error and the other's update completes (d) Step 5 fails at once because B holds a share lock

**Q75** · `acct` holds (1, 100), (2, 100). What do steps 5, 6 and 7 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM acct;
3  B: INSERT INTO acct VALUES (3, 0);
4  B: UPDATE acct SET bal = 0 WHERE id = 2;
5  A: UPDATE acct SET bal = bal + 1;
6  A: COMMIT;
7  A: SELECT id, bal FROM acct ORDER BY id;
```

**Q76** · `event(id int primary key)` holds (1); `seat(event int, who text)` holds two rows for event 1. At most 3 people fit, so each application locks the event row, counts, and inserts only if the count is below 3. A's count returns 2. What does step 8 return, and how many seats does event 1 have at the end?

```sql
1  A: BEGIN;
2  A: SELECT id FROM event WHERE id = 1 FOR UPDATE;
3  A: SELECT count(*) FROM seat WHERE event = 1;
4  B: BEGIN;
5  B: SELECT id FROM event WHERE id = 1 FOR UPDATE;
6  A: INSERT INTO seat VALUES (1, 'a');
7  A: COMMIT;
8  B: SELECT count(*) FROM seat WHERE event = 1;
```

**Q77** · `acct` holds (1, 100), (2, 100). What do steps 4 and 7 return?

```sql
1  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: BEGIN;
3  A: UPDATE acct SET bal = bal - 40 WHERE id = 1;
4  B: SELECT bal FROM acct WHERE id = 1;
5  A: UPDATE acct SET bal = bal + 40 WHERE id = 2;
6  A: COMMIT;
7  B: SELECT bal FROM acct WHERE id = 2;
```

**Q78** · `orders` holds three rows. Does step 3 wait? What does step 4 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM orders;
3  B: TRUNCATE orders;
4  A: SELECT count(*) FROM orders;
5  A: COMMIT;
```

**Q79** · `acct` holds (1, 100), (2, 100). Session A runs one statement, `SELECT id, bal, pg_sleep(5) FROM acct;`, which sleeps 5 seconds on each row it returns. Two seconds after it starts, session B runs `BEGIN; UPDATE acct SET bal = bal - 40 WHERE id = 1; UPDATE acct SET bal = bal + 40 WHERE id = 2; COMMIT;`, which takes a few milliseconds. What balances does A's result show?

**Q80** · `counter(k text primary key, n int)` holds no row for 'z'. What happens at step 4?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM counter;
3  B: INSERT INTO counter VALUES ('z', 1);
4  A: INSERT INTO counter VALUES ('z', 1)
        ON CONFLICT (k) DO UPDATE SET n = counter.n + 1;
```

**Q81** · `mytab(class int, value int)` holds (1, 10), (1, 20), (2, 100), (2, 200). A runs SERIALIZABLE, but B runs REPEATABLE READ. What is the outcome of steps 7 and 8?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT sum(value) FROM mytab WHERE class = 1;
3  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
4  B: SELECT sum(value) FROM mytab WHERE class = 2;
5  A: INSERT INTO mytab VALUES (2, 30);
6  B: INSERT INTO mytab VALUES (1, 300);
7  A: COMMIT;
8  B: COMMIT;
```

**Q82** · `acct` holds (1, 100), (2, 100). What do steps 2 and 4 return?

```sql
1  A: SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 5 WHERE id = 1;
4  A: SELECT bal FROM acct WHERE id = 1;
```

**Q83** · `acct` holds (1, 100), (2, 100). Both requests use the read-then-write code from Q13, now at REPEATABLE READ. After step 7, B's application retries its whole transaction once, reading the balance again and writing the value it read + 30. What is the final balance?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;       -- app reads the value
3  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
4  B: SELECT bal FROM acct WHERE id = 1;       -- app reads the value
5  A: UPDATE acct SET bal = 150 WHERE id = 1;  -- value it read + 50
6  A: COMMIT;
7  B: UPDATE acct SET bal = 130 WHERE id = 1;  -- value it read + 30
```

**Q84** · `jobs` holds (1, 'new'), (2, 'new'). Two workers fetch the next job without SKIP LOCKED. What does B's step 4 return, and when?

```sql
1  A: BEGIN;
2  A: SELECT id FROM jobs WHERE status = 'new'
        ORDER BY id LIMIT 1 FOR UPDATE;
3  B: BEGIN;
4  B: SELECT id FROM jobs WHERE status = 'new'
        ORDER BY id LIMIT 1 FOR UPDATE;
5  A: UPDATE jobs SET status = 'done' WHERE id = 1;
6  A: COMMIT;
```

**Q85** · `acct` holds (1, 100), (2, 100). What does step 2 return?

```sql
1  A: UPDATE acct SET bal = bal + (SELECT sum(bal) FROM acct);
2  A: SELECT id, bal FROM acct ORDER BY id;
```

**Q86** · `acct` holds (1, 100), (2, 100). What does step 5 return?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = 50 WHERE id = 1;
3  B: UPDATE acct SET bal = bal * 2 WHERE bal < 200;
4  A: COMMIT;
5  B: SELECT id, bal FROM acct ORDER BY id;
```

**Q87** · `oncall` holds ('ann', true), ('bo', true). Each application now locks the on-duty rows, counts the rows returned, and goes off duty only if there are 2 or more. What does B's step 4 return, and how many people end on duty if B follows its rule?

```sql
1  A: BEGIN;
2  A: SELECT name FROM oncall WHERE on_duty FOR UPDATE;
3  B: BEGIN;
4  B: SELECT name FROM oncall WHERE on_duty FOR UPDATE;
5  A: UPDATE oncall SET on_duty = false WHERE name = 'ann';
6  A: COMMIT;
```

**Q88** · `acct` holds (1, 100), (2, 100). What do steps 3, 4 and 6 produce?

```sql
1  A: BEGIN;
2  A: INSERT INTO acct VALUES (5, 0);
3  B: SELECT count(*) FROM acct WHERE id = 5;
4  B: INSERT INTO acct VALUES (5, 1) ON CONFLICT DO NOTHING;
5  A: COMMIT;
6  B: SELECT bal FROM acct WHERE id = 5;
```

**Q89** · `items(id serial primary key, name text)` is empty and its sequence is fresh. What do steps 4 and 5 return?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT count(*) FROM items;
3  B: INSERT INTO items(name) VALUES ('b');
4  A: INSERT INTO items(name) VALUES ('a') RETURNING id;
5  A: SELECT count(*), max(id) FROM items;
```

**Q90** · `acct` holds (1, 100), (2, 100). What happens to B's step 4?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
3  B: BEGIN ISOLATION LEVEL SERIALIZABLE;
4  B: UPDATE acct SET bal = bal + 1 WHERE id = 1;
5  A: COMMIT;
```

**Q91** · `acct` holds (1, 100), (2, 100). Steps are a fraction of a second apart. About a second after step 6 the deadlock detector rolls back B. Then both sessions send COMMIT. What are the final balances?

```sql
1  A: BEGIN;
2  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
3  B: BEGIN;
4  B: UPDATE acct SET bal = bal + 10 WHERE id = 2;
5  B: UPDATE acct SET bal = bal + 10 WHERE id = 1;
6  A: UPDATE acct SET bal = bal + 1 WHERE id = 2;
```

**Q92** · `booking(room int, day date, UNIQUE (room, day))` is empty. Each application inserts only if its count is 0, and both counts return 0. What happens at step 6, and how many bookings exist at the end?

```sql
1  A: BEGIN;
2  A: SELECT count(*) FROM booking WHERE room = 7 AND day = '2026-12-01';
3  B: BEGIN;
4  B: SELECT count(*) FROM booking WHERE room = 7 AND day = '2026-12-01';
5  A: INSERT INTO booking VALUES (7, '2026-12-01');
6  B: INSERT INTO booking VALUES (7, '2026-12-01');
7  A: COMMIT;
8  B: COMMIT;
```

**Q93** · `jobs` holds (1, 'new'), (2, 'done'). What does step 4 return?

```sql
1  A: BEGIN;
2  A: UPDATE jobs SET status = 'done' WHERE id = 1;
3  A: UPDATE jobs SET status = 'new' WHERE id = 2;
4  B: SELECT id FROM jobs WHERE status = 'new' FOR UPDATE;
5  A: COMMIT;
```

**Q94** · `acct` holds (1, 100), (2, 100). What do steps 4 and 6 return?

```sql
1  A: BEGIN;
2  A: SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
3  B: UPDATE acct SET bal = 1 WHERE id = 1;
4  A: SELECT bal FROM acct WHERE id = 1;
5  B: UPDATE acct SET bal = 2 WHERE id = 1;
6  A: SELECT bal FROM acct WHERE id = 1;
```

**Q95** · `acct` holds (1, 100), (2, 100). Session A uses a safe atomic increment; B's application reads, subtracts 5 in its own code, and writes. What is the final balance of account 1?

```sql
1  B: BEGIN;
2  B: SELECT bal FROM acct WHERE id = 1;       -- app reads the value
3  A: UPDATE acct SET bal = bal + 10 WHERE id = 1;
4  B: UPDATE acct SET bal = 95 WHERE id = 1;   -- value it read - 5
5  B: COMMIT;
```

**Q96** · Same tables and rule as Q76: `event` holds (1), `seat` holds two rows for event 1, at most 3 fit, and each application locks the event row, counts, and inserts only if the count is below 3. This time both run REPEATABLE READ. A's count returns 2. What does step 8 return, and how many seats does event 1 have if B follows its rule?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT id FROM event WHERE id = 1 FOR UPDATE;
3  A: SELECT count(*) FROM seat WHERE event = 1;
4  B: BEGIN ISOLATION LEVEL REPEATABLE READ;
5  B: SELECT id FROM event WHERE id = 1 FOR UPDATE;
6  A: INSERT INTO seat VALUES (1, 'a');
7  A: COMMIT;
8  B: SELECT count(*) FROM seat WHERE event = 1;
```

**Q97** · `acct` holds (1, 100), (2, 100). A runs SERIALIZABLE; B runs a single statement in autocommit at the default level. What happens at step 4?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT bal FROM acct WHERE id = 1;
3  B: UPDATE acct SET bal = 0 WHERE id = 1;
4  A: UPDATE acct SET bal = bal - 10 WHERE id = 1;
```

**Q98** · `booking(room int, day date)` has no constraints and no rows. Both transactions run SERIALIZABLE, and each inserts only if its count is 0. Both counts return 0. What is the outcome, and how many bookings exist at the end?

```sql
1  A: BEGIN ISOLATION LEVEL SERIALIZABLE;
2  A: SELECT count(*) FROM booking WHERE room = 7 AND day = '2026-12-01';
3  B: BEGIN ISOLATION LEVEL SERIALIZABLE;
4  B: SELECT count(*) FROM booking WHERE room = 7 AND day = '2026-12-01';
5  A: INSERT INTO booking VALUES (7, '2026-12-01');
6  B: INSERT INTO booking VALUES (7, '2026-12-01');
7  A: COMMIT;
8  B: COMMIT;
```

(a) Both commit, leaving 2 bookings (b) B's step 6 waits for A, then both commit (c) Exactly one fails with a serialization error, leaving 1 booking (d) B's step 6 fails with a duplicate key error

**Q99** · `counter(k text primary key, n int)` is empty. What do steps 3, 4 and 6 produce?

```sql
1  A: BEGIN;
2  A: INSERT INTO counter VALUES ('q', 1);
3  A: INSERT INTO counter VALUES ('q', 1)
        ON CONFLICT (k) DO UPDATE SET n = counter.n + 1;
4  B: SELECT n FROM counter WHERE k = 'q';
5  A: COMMIT;
6  B: SELECT n FROM counter WHERE k = 'q';
```

**Q100** · `acct` holds (1, 100), (2, 100). A savepoint marks a point inside a transaction that `ROLLBACK TO SAVEPOINT` can return to, undoing only what came after it. What do steps 7 and 8 produce?

```sql
1  A: BEGIN ISOLATION LEVEL REPEATABLE READ;
2  A: SELECT bal FROM acct WHERE id = 1;
3  A: SAVEPOINT s;
4  A: SELECT 1/0;
5  B: UPDATE acct SET bal = 0 WHERE id = 1;
6  A: ROLLBACK TO SAVEPOINT s;
7  A: SELECT bal FROM acct WHERE id = 1;
8  A: UPDATE acct SET bal = bal + 1 WHERE id = 1;
```

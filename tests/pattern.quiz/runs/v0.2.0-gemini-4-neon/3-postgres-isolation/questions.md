**Topic:** SQL transaction isolation levels in PostgreSQL — **Depth:** High (100 questions)
**Assumptions:** PostgreSQL 16 defaults (`READ COMMITTED`, `autocommit` on outside `BEGIN`, `lock_timeout = 0`, `deadlock_timeout = 1s`); tables have only the columns, keys, and constraints shown (no triggers or extra indexes); numbered steps interleave globally, and a blocked statement pauses while later steps run until the lock holder ends; for indexed `SERIALIZABLE` queries, assume index scans with distinct rows on separate pages unless sequential scans are stated.

## Band 1 — Core Mechanisms

### 1.
What does step 3 return?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 50 WHERE id = 1;
3. T2: SELECT bal FROM accounts WHERE id = 1;
```

### 2.
What happens immediately at step 3?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 50 WHERE id = 1;
3. T2: SELECT bal FROM accounts WHERE id = 1;
```

(a) T2 blocks until T1 commits or rolls back
(b) T2 returns `100` immediately without blocking
(c) T2 returns `50` immediately without blocking
(d) T2 fails immediately with a lock-conflict error

### 3.
What rows are in `t` after step 6?

```sql
-- t(x int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO t VALUES (1);
3. T1: SELECT 1 / 0;
4. T1: INSERT INTO t VALUES (2);
5. T1: INSERT INTO t VALUES (3);
6. T1: COMMIT;
```

### 4.
After step 2 completes, what values of `x` are in `t`?

```sql
-- t(x int) starts empty
1. T1: INSERT INTO t VALUES (1), (2);
2. T1: INSERT INTO t SELECT x * 10 FROM t;
```

### 5.
What happens to T2 at step 3, and what is `qty` for `id = 1` after step 5?

```sql
-- items(id int PRIMARY KEY, qty int): (1, 10)
1. T1: BEGIN;
2. T1: UPDATE items SET qty = 9 WHERE id = 1;
3. T2: UPDATE items SET qty = 8 WHERE id = 1;
4. T1: ROLLBACK;
5. -- T2 finishes (autocommit)
```

### 6.
What values do step 2 and step 4 return?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: UPDATE accounts SET bal = 200 WHERE id = 1;
4. T1: SELECT bal FROM accounts WHERE id = 1;
5. T1: COMMIT;
```

### 7.
What does step 4 return?

```sql
-- orders(id int PRIMARY KEY, status text): (1, 'new'), (2, 'new')
1. T1: BEGIN;
2. T1: SELECT count(*) FROM orders WHERE status = 'new';
3. T2: INSERT INTO orders VALUES (3, 'new');
4. T1: SELECT count(*) FROM orders WHERE status = 'new';
5. T1: COMMIT;
```

### 8.
After step 5 finishes, how many rows did step 3 update and what is `bal` for `id = 1`?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = bal - 80 WHERE id = 1 AND bal >= 80;
3. T2: UPDATE accounts SET bal = bal - 80 WHERE id = 1 AND bal >= 80;
4. T1: COMMIT;
5. -- T2 finishes (autocommit)
```

### 9.
Two checkout handlers run concurrently in `READ COMMITTED`, computing `stock - 1` in application code from their `SELECT` result. What is `stock` for `id = 1` after step 8, and does either transaction fail?

```sql
-- inventory(id int PRIMARY KEY, stock int): (1, 10)
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: SELECT stock FROM inventory WHERE id = 1;  -- gets 10
4. T2: SELECT stock FROM inventory WHERE id = 1;  -- gets 10
5. T1: UPDATE inventory SET stock = 9 WHERE id = 1;
6. T1: COMMIT;
7. T2: UPDATE inventory SET stock = 9 WHERE id = 1;
8. T2: COMMIT;
```

### 10.
What happens immediately at step 3 while T1 remains uncommitted?

```sql
-- users(id int PRIMARY KEY) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO users VALUES (1);
3. T2: INSERT INTO users VALUES (1);
```

(a) T2 blocks until T1 commits or rolls back
(b) T2 fails immediately with a unique-violation error (`23505`)
(c) T2 succeeds immediately because T1's row is not yet visible
(d) T2 succeeds now and fails later only if T1 commits first

### 11.
What row is in `kv` after step 5 finishes?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO kv VALUES ('a', 1);
3. T2: INSERT INTO kv VALUES ('a', 2)
       ON CONFLICT (k) DO UPDATE SET v = kv.v + EXCLUDED.v;
4. T1: COMMIT;
5. -- T2 finishes (autocommit)
```

### 12.
While T1 remains open after step 2, which of T2 and T3 block?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open')
1. T1: BEGIN;
2. T1: SELECT status FROM jobs WHERE id = 1 FOR UPDATE;
3. T2: SELECT status FROM jobs WHERE id = 1;
4. T3: UPDATE jobs SET status = 'done' WHERE id = 1;
```

(a) Both T2 and T3 block
(b) Neither T2 nor T3 blocks
(c) Only T3 blocks; T2 returns `'open'` immediately
(d) Only T2 blocks; T3 updates the row immediately

### 13.
What does step 3 return while T1 remains open?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN;
2. T1: SELECT id FROM jobs WHERE id = 1 FOR UPDATE;
3. T2: SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
```

### 14.
What does PostgreSQL do after step 6?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: UPDATE accounts SET bal = bal - 10 WHERE id = 1;
4. T2: UPDATE accounts SET bal = bal - 10 WHERE id = 2;
5. T1: UPDATE accounts SET bal = bal + 10 WHERE id = 2;
6. T2: UPDATE accounts SET bal = bal + 10 WHERE id = 1;
```

(a) Both T1 and T2 hang forever because `lock_timeout = 0`
(b) PostgreSQL detects the cycle and aborts one transaction with `40P01`, allowing the other to proceed
(c) PostgreSQL detects the cycle and aborts both T1 and T2
(d) PostgreSQL runs T1 to completion first and then replays T2 automatically

### 15.
What rows are in `t` after step 8?

```sql
-- t(x int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO t VALUES (1);
3. T1: SAVEPOINT sp;
4. T1: INSERT INTO t VALUES (2);
5. T1: SELECT 1 / 0;
6. T1: ROLLBACK TO SAVEPOINT sp;
7. T1: INSERT INTO t VALUES (3);
8. T1: COMMIT;
```

### 16.
While T1 remains open after step 2, what happens to T2 and T3?

```sql
-- items(id int PRIMARY KEY): (1)
1. T1: BEGIN;
2. T1: SELECT count(*) FROM items;
3. T2: ALTER TABLE items ADD COLUMN tag text;
4. T3: SELECT count(*) FROM items;
```

(a) Both T2 and T3 finish immediately
(b) T2 blocks on T1, while T3 finishes immediately
(c) T2 blocks on T1, and T3 blocks behind T2
(d) T2 fails immediately with a lock error, and T3 finishes immediately

### 17.
What does step 3 return?

```sql
-- counter(n int): (0)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: UPDATE counter SET n = 5;
3. T1: SELECT n FROM counter;
4. T1: COMMIT;
```

### 18.
What does step 4 return?

```sql
-- orders(id int PRIMARY KEY): (1), (2)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM orders;
3. T2: INSERT INTO orders VALUES (3);
4. T1: SELECT count(*) FROM orders;
5. T1: COMMIT;
```

### 19.
What happens at step 4?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: UPDATE accounts SET bal = 200 WHERE id = 1;
4. T1: UPDATE accounts SET bal = bal + 10 WHERE id = 1;
```

### 20.
Both sessions check that at least 2 doctors are on call before taking one off call. After step 8, how many rows have `on_call = true`?

```sql
-- doctors(id int PRIMARY KEY, on_call bool): (1, true), (2, true)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
3. T1: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
4. T2: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
5. T1: UPDATE doctors SET on_call = false WHERE id = 1;
6. T1: COMMIT;
7. T2: UPDATE doctors SET on_call = false WHERE id = 2;
8. T2: COMMIT;
```

## Band 2 — Applied Settings

### 21.
What does step 3 return?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL READ UNCOMMITTED;
2. T2: BEGIN; UPDATE accounts SET bal = 500 WHERE id = 1;
3. T1: SELECT bal FROM accounts WHERE id = 1;
4. T1: COMMIT;
```

### 22.
What is `bal` for `id = 1` after step 5 finishes?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = bal + 50 WHERE id = 1;
3. T2: UPDATE accounts SET bal = bal * 2 WHERE id = 1;
4. T1: COMMIT;
5. -- T2 finishes (autocommit)
```

### 23.
What is `price` for `id = 1` after step 5 finishes?

```sql
-- items(id int PRIMARY KEY, price int): (1, 10), (2, 20)
1. T1: BEGIN;
2. T1: UPDATE items SET price = 50 WHERE id = 1;
3. T2: UPDATE items SET price = (SELECT max(price) FROM items)
       WHERE id = 1;
4. T1: COMMIT;
5. -- T2 finishes (autocommit)
```

### 24.
What does step 3 return once step 4 commits?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open')
1. T1: BEGIN;
2. T1: UPDATE jobs SET status = 'claimed' WHERE id = 1;
3. T2: SELECT id FROM jobs WHERE status = 'open' FOR UPDATE;
4. T1: COMMIT;
5. -- T2 finishes
```

### 25.
While T1 remains open after step 2, what happens to T2?

```sql
-- parents(id int PRIMARY KEY, name text): (1, 'old')
-- children(id int PRIMARY KEY, parent_id int REFERENCES parents(id))
1. T1: BEGIN;
2. T1: UPDATE parents SET name = 'new' WHERE id = 1;
3. T2: INSERT INTO children VALUES (10, 1);
```

(a) T2 blocks until T1 commits or rolls back
(b) T2 succeeds immediately without blocking
(c) T2 fails immediately with a foreign-key violation
(d) T2 fails immediately with a lock-conflict error

### 26.
While T1 remains open after step 2, what happens at step 3?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open')
1. T1: BEGIN;
2. T1: SELECT id FROM jobs WHERE id = 1 FOR UPDATE;
3. T2: SELECT id FROM jobs WHERE id = 1 FOR UPDATE NOWAIT;
```

(a) T2 returns 0 rows cleanly
(b) T2 returns row `1` without locking it
(c) T2 blocks until T1 commits or rolls back
(d) T2 fails immediately with lock-not-available (`55P03`)

### 27.
How many rows does step 4 update, and what are the final `status` values of rows 1 and 2 after step 5?

```sql
-- orders(id int PRIMARY KEY, status text): (1, 'open')
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM orders;
3. T2: INSERT INTO orders VALUES (2, 'open');
4. T1: UPDATE orders SET status = 'closed' WHERE status = 'open';
5. T1: COMMIT;
```

### 28.
What happens at step 4?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM kv;
3. T2: INSERT INTO kv VALUES ('x', 1);
4. T1: INSERT INTO kv VALUES ('x', 2)
       ON CONFLICT (k) DO UPDATE SET v = 2;
```

### 29.
Which step fails (if any), and what are the final `on_call` values for `id = 1` and `id = 2`?

```sql
-- doctors(id int PRIMARY KEY, on_call bool): (1, true), (2, true)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
4. T2: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
5. T1: UPDATE doctors SET on_call = false WHERE id = 1;
6. T2: UPDATE doctors SET on_call = false WHERE id = 2;
7. T1: COMMIT;
8. T2: COMMIT;
```

### 30.
Does step 4 succeed or fail?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 200 WHERE id = 1; COMMIT;
4. T1: COMMIT;
```

### 31.
Does either transaction fail, and how many doctors remain `on_call = true` after step 8?

```sql
-- doctors(id int PRIMARY KEY, on_call bool): (1, true), (2, true)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN;  -- default READ COMMITTED
3. T1: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
4. T2: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
5. T1: UPDATE doctors SET on_call = false WHERE id = 1;
6. T1: COMMIT;
7. T2: UPDATE doctors SET on_call = false WHERE id = 2;
8. T2: COMMIT;
```

### 32.
`items(id int, val int)` has 2 rows and no indexes, so PostgreSQL uses sequential scans for every statement below. What happens at step 8?

```sql
-- items(id int, val int): (1, 10), (2, 20) — no indexes
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT val FROM items WHERE id = 1;
4. T2: SELECT val FROM items WHERE id = 2;
5. T1: UPDATE items SET val = 11 WHERE id = 1;
6. T2: UPDATE items SET val = 21 WHERE id = 2;
7. T1: COMMIT;
8. T2: COMMIT;
```

(a) T2 commits cleanly because T1 and T2 touched different rows
(b) T2 fails at step 8 with `40001` because sequential scans took relation-level predicate locks
(c) T2 blocks at step 6 until T1 commits, then commits cleanly
(d) T1 fails at step 7 with `40001` and T2 commits cleanly

### 33.
What `id` does step 4 return?

```sql
-- logs(id SERIAL PRIMARY KEY, msg text) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO logs(msg) VALUES ('a');
3. T1: ROLLBACK;
4. T2: INSERT INTO logs(msg) VALUES ('b') RETURNING id;
```

### 34.
While T1 remains open after step 2, does step 3 block or commit immediately?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: UPDATE accounts SET bal = 200 WHERE id = 1;
```

### 35.
Application code catches the error at step 3, ignores it, and runs step 4. What does PostgreSQL do at step 4, and what rows are in `users` afterward?

```sql
-- users(id int PRIMARY KEY) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO users VALUES (1);
3. T1: INSERT INTO users VALUES (1);
4. T1: COMMIT;
```

### 36.
What values do step 3 and step 4 return?

```sql
-- t(x int): (1), (2)
1. T1: BEGIN;
2. T1: UPDATE t SET x = x + 10;
3. T1: SELECT sum(x) FROM t;
4. T2: SELECT sum(x) FROM t;
```

### 37.
While T1 remains open after step 2, does step 3 block or complete immediately?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 50 WHERE id = 1;
3. T2: UPDATE accounts SET bal = 50 WHERE id = 2;
```

### 38.
While T1 runs step 1, T2 commits `UPDATE prices SET p = 99 WHERE id = 1;`. Which output is impossible for T1?

```sql
-- prices(id int PRIMARY KEY, p int): (1, 10)
1. T1: SELECT p, (SELECT p FROM prices WHERE id = 1) AS p2
       FROM prices WHERE id = 1;
```

(a) `(10, 10)`
(b) `(99, 99)`
(c) `(10, 99)`
(d) Either `(10, 10)` or `(99, 99)` depending on timing

### 39.
T1 sums the two balances it reads in application code. What total does T1 compute?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN;
       UPDATE accounts SET bal = 60 WHERE id = 1;
       UPDATE accounts SET bal = 140 WHERE id = 2;
       COMMIT;
4. T1: SELECT bal FROM accounts WHERE id = 2;
5. T1: COMMIT;
```

### 40.
Multiple workers concurrently increment `posts.views` for the same `id` under default `READ COMMITTED`. Which implementation prevents lost updates without risking deadlocks or serialization errors?

(a) `BEGIN; SELECT views FROM posts WHERE id = $1; -- add 1 in app -- UPDATE posts SET views = $new WHERE id = $1; COMMIT;`
(b) `UPDATE posts SET views = views + 1 WHERE id = $1;`
(c) `BEGIN; SELECT views FROM posts WHERE id = $1 FOR SHARE; -- add 1 in app -- UPDATE posts SET views = $new WHERE id = $1; COMMIT;`
(d) `BEGIN ISOLATION LEVEL READ UNCOMMITTED; SELECT views FROM posts WHERE id = $1; -- add 1 in app -- UPDATE posts SET views = $new WHERE id = $1; COMMIT;`

### 41.
What rows are in `users` after step 5 completes?

```sql
-- users(id int PRIMARY KEY) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO users VALUES (1);
3. T2: INSERT INTO users VALUES (1);
4. T1: ROLLBACK;
5. -- T2 finishes (autocommit)
```

### 42.
What rows are in `kv` after step 5 completes?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO kv VALUES ('a', 1);
3. T2: INSERT INTO kv VALUES ('a', 2) ON CONFLICT (k) DO NOTHING;
4. T1: ROLLBACK;
5. -- T2 finishes (autocommit)
```

### 43.
Both workers run concurrently in `READ COMMITTED`, subtracting 1 in application code from the `stock` value returned by their `SELECT ... FOR UPDATE`. What is `stock` after both commit?

```sql
-- inventory(id int PRIMARY KEY, stock int): (1, 5)
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: SELECT stock FROM inventory WHERE id = 1 FOR UPDATE;
4. T2: SELECT stock FROM inventory WHERE id = 1 FOR UPDATE;
5. T1: UPDATE inventory SET stock = 4 WHERE id = 1;
6. T1: COMMIT;
7. T2: -- uses value returned at step 4, subtracts 1, updates, COMMIT
```

### 44.
What happens to T2 at step 3, and what happens to T2 once step 4 runs?

```sql
-- parents(id int PRIMARY KEY): (1)
-- children(id int PRIMARY KEY, parent_id int REFERENCES parents(id))
1. T1: BEGIN;
2. T1: DELETE FROM parents WHERE id = 1;
3. T2: INSERT INTO children VALUES (10, 1);
4. T1: COMMIT;
```

### 45.
A slow reporting job holds an open `BEGIN; SELECT count(*) FROM events;` for 5 minutes. One minute in, a deployment runs `ALTER TABLE events RENAME COLUMN a TO b;`. Why do unrelated web requests running `SELECT` and `INSERT` on `events` suddenly stall?

(a) `RENAME COLUMN` rewrites every row of `events`, saturating disk I/O
(b) `ALTER TABLE` waits in the lock queue for `ACCESS EXCLUSIVE`, and every new `SELECT` and `INSERT` queues behind it
(c) The reporting job holds an exclusive table lock that blocks all queries on `events`
(d) PostgreSQL freezes all queries on any database while any DDL statement is pending

### 46.
A transfer handler updates the sender row (`from_id`) and then the receiver row (`to_id`) in one transaction. Concurrent opposite transfers (`1 -> 2` and `2 -> 1`) keep deadlocking. Which single change eliminates these deadlocks?

(a) Switch both transactions from `READ COMMITTED` to `REPEATABLE READ`
(b) Add `SELECT ... FOR SHARE` on both rows before updating
(c) Always lock or update the smaller account `id` before the larger account `id`
(d) Remove `BEGIN ... COMMIT` so each `UPDATE` runs as its own autocommit statement

### 47.
While T1 stays open after step 5, which of T2 and T3 block?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 90 WHERE id = 1;
3. T1: SAVEPOINT s1;
4. T1: UPDATE accounts SET bal = 90 WHERE id = 2;
5. T1: ROLLBACK TO SAVEPOINT s1;
6. T2: UPDATE accounts SET bal = 80 WHERE id = 2;
7. T3: UPDATE accounts SET bal = 80 WHERE id = 1;
```

### 48.
What does step 4 return?

```sql
-- t(x int): (1)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT 1;
3. T2: UPDATE t SET x = 2;
4. T1: SELECT x FROM t;
5. T1: COMMIT;
```

### 49.
What happens to T1 after step 6, and what is `bal` after step 7?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN;
4. T2: UPDATE accounts SET bal = 200 WHERE id = 1;
5. T1: UPDATE accounts SET bal = 150 WHERE id = 1;
6. T2: ROLLBACK;
7. T1: COMMIT;
```

### 50.
T1 sums the two balances it reads in application code. What total does T1 compute?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN;
       UPDATE accounts SET bal = 60 WHERE id = 1;
       UPDATE accounts SET bal = 140 WHERE id = 2;
       COMMIT;
4. T1: SELECT bal FROM accounts WHERE id = 2;
5. T1: COMMIT;
```

### 51.
While T1 and T2 stay open after step 4, which of T1, T2, and T3 block?

```sql
-- items(id int PRIMARY KEY, qty int): (1, 10)
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: SELECT qty FROM items WHERE id = 1 FOR SHARE;
4. T2: SELECT qty FROM items WHERE id = 1 FOR SHARE;
5. T3: UPDATE items SET qty = 9 WHERE id = 1;
```

### 52.
What rows remain in `tasks` after step 5?

```sql
-- tasks(id int PRIMARY KEY, done bool): (1, false)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM tasks WHERE NOT done;
3. T2: INSERT INTO tasks VALUES (2, false);
4. T1: DELETE FROM tasks WHERE NOT done;
5. T1: COMMIT;
```

### 53.
`bookings` has no unique constraint. Both sessions check for an existing booking before inserting. How many rows are in `bookings` after step 8?

```sql
-- bookings(room int, slot int) starts empty
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
3. T1: SELECT count(*) FROM bookings WHERE room = 1 AND slot = 9; -- 0
4. T2: SELECT count(*) FROM bookings WHERE room = 1 AND slot = 9; -- 0
5. T1: INSERT INTO bookings VALUES (1, 9);
6. T1: COMMIT;
7. T2: INSERT INTO bookings VALUES (1, 9);
8. T2: COMMIT;
```

### 54.
Does T1 succeed or fail, and what row is in `kv` after step 5?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM kv;
3. T2: INSERT INTO kv VALUES ('x', 1);
4. T1: INSERT INTO kv VALUES ('x', 2) ON CONFLICT (k) DO NOTHING;
5. T1: COMMIT;
```

### 55.
Does step 5 succeed or fail with `40001`?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN;
       SELECT bal FROM accounts WHERE id = 1 FOR UPDATE;
       COMMIT;
4. T1: UPDATE accounts SET bal = 150 WHERE id = 1;
5. T1: COMMIT;
```

### 56.
`bookings(room int, slot int)` has a non-unique index on `(room, slot)` and starts with `(2, 10)`. At which exact step does a failure occur, and what rows are in `bookings` afterward?

```sql
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT count(*) FROM bookings WHERE room = 1 AND slot = 9; -- 0
4. T2: SELECT count(*) FROM bookings WHERE room = 1 AND slot = 9; -- 0
5. T1: INSERT INTO bookings VALUES (1, 9);
6. T1: COMMIT;
7. T2: INSERT INTO bookings VALUES (1, 9);
8. T2: COMMIT;
```

### 57.
What happens at step 5?

```sql
-- accounts(id text PRIMARY KEY, bal int): ('x', 0), ('y', 0)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
       SELECT bal FROM accounts WHERE id = 'y';              -- gets 0
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 20 WHERE id = 'y'; COMMIT;
3. T3: BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY;
       SELECT bal FROM accounts WHERE id = 'y';              -- gets 20
4. T1: UPDATE accounts SET bal = 10 WHERE id = 'x'; COMMIT;
5. T3: SELECT bal FROM accounts WHERE id = 'x';
```

### 58.
Do both T1 and T2 commit cleanly, or does one fail with `40001`?

```sql
-- items(id int PRIMARY KEY, price int): (1, 10), (2, 20)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT price FROM items WHERE id = 1;
4. T2: SELECT price FROM items WHERE id = 2;
5. T1: UPDATE items SET price = 15 WHERE id = 1;
6. T2: UPDATE items SET price = 25 WHERE id = 2;
7. T1: COMMIT;
8. T2: COMMIT;
```

### 59.
A payment service runs all account withdrawals at `SERIALIZABLE` to enforce that each user's total balance across two accounts stays `>= 0`. An admin adjustment tool modifies the same `accounts` table using default `READ COMMITTED`. Can concurrent requests from the payment service and the admin tool still violate the invariant?

(a) No, because `SERIALIZABLE` locks out all lower-isolation transactions on the table
(b) No, because PostgreSQL upgrades the `READ COMMITTED` transaction to `SERIALIZABLE` on conflict
(c) Yes, because `READ COMMITTED` transactions do not participate in SSI read/write dependency tracking
(d) Yes, but only if the admin tool runs `DELETE` instead of `UPDATE`

### 60.
Inside a `SERIALIZABLE` transaction, the second `UPDATE` fails with SQLSTATE `40001`. Application code catches the error and immediately re-runs only that second `UPDATE` without calling `ROLLBACK`. What happens?

(a) The retried `UPDATE` succeeds using a fresh snapshot
(b) The retried `UPDATE` fails with `25P02` because the transaction block is aborted
(c) PostgreSQL automatically rolls back to the start of the second `UPDATE` and retries it
(d) The retried `UPDATE` commits the first `UPDATE` and skips the second

### 61.
After step 6 completes, what are the `total` values of rows 1 and 2?

```sql
-- orders(id int PRIMARY KEY, total int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE orders SET total = 150 WHERE id = 1;
3. T2: UPDATE orders SET total = total + 10 WHERE total >= 100;
4. T3: INSERT INTO orders VALUES (2, 200);
5. T1: COMMIT;
6. -- T2 finishes (autocommit)
```

### 62.
Note that step 3 sets `bal` to the same value it already holds (`100`). What happens at step 4?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: UPDATE accounts SET bal = 100 WHERE id = 1;
4. T1: UPDATE accounts SET bal = 150 WHERE id = 1;
```

### 63.
What `(id, prio)` row does step 3 return once step 4 commits?

```sql
-- jobs(id int PRIMARY KEY, prio int, status text):
--   (1, 1, 'open'), (2, 2, 'open')
1. T1: BEGIN;
2. T1: UPDATE jobs SET prio = 100 WHERE id = 1;
3. T2: SELECT id, prio FROM jobs WHERE status = 'open'
       ORDER BY prio LIMIT 1 FOR UPDATE;
4. T1: COMMIT;
5. -- T2 finishes
```

### 64.
What does step 3 return while T1 remains open?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN;
2. T1: SELECT id FROM jobs WHERE id = 1 FOR UPDATE;
3. T2: SELECT count(*) FROM (
         SELECT id FROM jobs WHERE status = 'open' FOR UPDATE SKIP LOCKED
       ) s;
```

### 65.
What value does step 3 return once step 5 commits?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: SELECT bal FROM accounts WHERE id = 1 FOR UPDATE;
3. T2: SELECT bal FROM accounts WHERE id = 1 FOR UPDATE;
4. T1: UPDATE accounts SET bal = 70 WHERE id = 1;
5. T1: COMMIT;
6. -- T2 finishes
```

### 66.
What `id` does step 3 return once step 4 commits?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN;
2. T1: UPDATE jobs SET status = 'done' WHERE id = 1;
3. T2: SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE;
4. T1: COMMIT;
5. -- T2 finishes
```

### 67.
T1 divides the result of step 2 by the result of step 4 in application code. What number does T1 compute?

```sql
-- orders(id int PRIMARY KEY, status text, amt int):
--   (1, 'open', 60), (2, 'open', 60)
1. T1: BEGIN;
2. T1: SELECT sum(amt) FROM orders WHERE status = 'open';
3. T2: INSERT INTO orders VALUES (3, 'open', 60);
4. T1: SELECT count(*) FROM orders WHERE status = 'open';
5. T1: COMMIT;
```

### 68.
What does step 4 return?

```sql
-- t(x int): (1)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SET TRANSACTION READ ONLY;
3. T2: UPDATE t SET x = 2;
4. T1: SELECT x FROM t;
5. T1: COMMIT;
```

### 69.
Compare with Q57: here T3 adds `DEFERRABLE`. What happens to T3 at step 3, and what values of `y` and `x` does T3 eventually read?

```sql
-- accounts(id text PRIMARY KEY, bal int): ('x', 0), ('y', 0)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
       SELECT bal FROM accounts WHERE id = 'y';              -- gets 0
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 20 WHERE id = 'y'; COMMIT;
3. T3: BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE;
       SELECT bal FROM accounts WHERE id = 'y';
4. T1: UPDATE accounts SET bal = 10 WHERE id = 'x'; COMMIT;
5. T3: SELECT bal FROM accounts WHERE id = 'x'; COMMIT;
```

### 70.
`orders(id SERIAL PRIMARY KEY, amt int)` starts empty. A `SERIALIZABLE` handler inserts `(50)` (receiving `id = 1`), fails with `40001` at `COMMIT`, rolls back, and retries once cleanly with no other transactions running. What `id` is stored in `orders`?

## Band 3 — Combined Mechanisms and Edge Cases

### 71.
What happens at step 4?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: UPDATE accounts SET bal = 80 WHERE id = 1;
4. T1: SELECT bal FROM accounts WHERE id = 1 FOR UPDATE;
```

### 72.
What happens after step 6?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: SELECT bal FROM accounts WHERE id = 1 FOR SHARE;
4. T2: SELECT bal FROM accounts WHERE id = 1 FOR SHARE;
5. T1: UPDATE accounts SET bal = 90 WHERE id = 1;
6. T2: UPDATE accounts SET bal = 80 WHERE id = 1;
```

### 73.
What is `bal` for `id = 1` after step 7 finishes?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 50 WHERE id = 1;
3. T1: SAVEPOINT s1;
4. T1: UPDATE accounts SET bal = 10 WHERE id = 1;
5. T2: UPDATE accounts SET bal = bal - 20 WHERE id = 1;
6. T1: ROLLBACK TO SAVEPOINT s1; COMMIT;
7. -- T2 finishes (autocommit)
```

### 74.
Does step 5 succeed or fail with `40001`, and what row is in `kv` afterward?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO kv VALUES ('a', 1);
3. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
4. T1: COMMIT;
5. T2: INSERT INTO kv VALUES ('a', 2)
       ON CONFLICT (k) DO UPDATE SET v = 2;
6. T2: COMMIT;
```

### 75.
`items(id int PRIMARY KEY, category text, qty int)` has 100,000 rows and an index only on `id` (no index on `category`, so the `SELECT`s use sequential scans). Row 1 is `'books'`; row 2 is `'music'`. What happens at step 8?

```sql
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT sum(qty) FROM items WHERE category = 'books';
4. T2: SELECT sum(qty) FROM items WHERE category = 'music';
5. T1: UPDATE items SET qty = qty - 1 WHERE id = 1;
6. T2: UPDATE items SET qty = qty - 1 WHERE id = 2;
7. T1: COMMIT;
8. T2: COMMIT;
```

### 76.
While T1 remains open after step 1 (having run no queries yet), does step 2 block or finish immediately?

```sql
-- items(id int PRIMARY KEY): (1)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: ALTER TABLE items ADD COLUMN note text;
```

### 77.
Both sessions lock all currently on-call doctors with `FOR UPDATE` before deciding whether to take one off call. What happens to T2 after step 6?

```sql
-- doctors(id int PRIMARY KEY, on_call bool): (1, true), (2, true)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
3. T1: SELECT id FROM doctors WHERE on_call FOR UPDATE;
4. T2: SELECT id FROM doctors WHERE on_call FOR UPDATE;
5. T1: UPDATE doctors SET on_call = false WHERE id = 1;
6. T1: COMMIT;
```

### 78.
What happens after step 6?

```sql
-- users(id int PRIMARY KEY) starts empty
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: INSERT INTO users VALUES (1);
4. T2: INSERT INTO users VALUES (2);
5. T1: INSERT INTO users VALUES (2);
6. T2: INSERT INTO users VALUES (1);
```

### 79.
After step 5 completes, how many rows did step 3 update and what are the balances of rows 1 and 2?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 50)
1. T1: BEGIN;
2. T1: UPDATE accounts SET bal = 50 WHERE id = 1;
3. T2: UPDATE accounts SET bal = bal + 10 WHERE bal = 100;
4. T1: UPDATE accounts SET bal = 100 WHERE id = 2; COMMIT;
5. -- T2 finishes (autocommit)
```

### 80.
What `(id, u)` rows are in `t` after step 7?

```sql
-- t(id SERIAL PRIMARY KEY, u int UNIQUE) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO t(u) VALUES (10);
3. T1: SAVEPOINT sp;
4. T1: INSERT INTO t(u) VALUES (10);
5. T1: ROLLBACK TO SAVEPOINT sp;
6. T1: INSERT INTO t(u) VALUES (20);
7. T1: COMMIT;
```

### 81.
Do both T1 and T2 commit cleanly, or does T1 fail with `40001`?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 200 WHERE id = 1; COMMIT;
4. T1: UPDATE accounts SET bal = 50 WHERE id = 2;
5. T1: COMMIT;
```

### 82.
While T2 stays open after step 3, what does step 4 return (or does it fail with `40001`)?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM jobs;
3. T2: BEGIN; UPDATE jobs SET status = 'done' WHERE id = 1;
4. T1: SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
```

### 83.
A migration runs `ALTER TABLE orders ADD COLUMN ref text;` while a 10-minute reporting `SELECT` is active on `orders`. What changes if the migration runs `SET LOCAL lock_timeout = '1s';` inside its transaction before the `ALTER TABLE`?

(a) `ALTER TABLE` skips waiting for the reporting `SELECT` and adds the column in 1 second
(b) After 1 second, the reporting `SELECT` is automatically cancelled so the migration can run
(c) After 1 second, `ALTER TABLE` aborts cleanly instead of blocking all incoming queries in the lock queue for 10 minutes
(d) Incoming `SELECT` queries still block for 10 minutes, while `INSERT` queries bypass the queue

### 84.
What exact error SQLSTATE (unique violation `23505` or serialization failure `40001`) does step 4 raise?

```sql
-- users(id int PRIMARY KEY) starts empty
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM users;
3. T2: INSERT INTO users VALUES (1);
4. T1: INSERT INTO users VALUES (1);
```

### 85.
What happens to T1 once step 5 commits?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 200 WHERE id = 1;
4. T1: UPDATE accounts SET bal = 150 WHERE id = 1;
5. T2: COMMIT;
```

(a) Step 4 succeeds and sets `bal = 150` because T1 started first
(b) Step 4 succeeds, and T1 fails later at `COMMIT` with a read/write dependency error
(c) Step 4 fails immediately after step 5 with `40001` (`could not serialize access due to concurrent update`)
(d) Step 5 fails with `40001` and step 4 succeeds

### 86.
`bookings` has no unique constraint. Both sessions try to prevent double booking with `FOR UPDATE`. How many rows are in `bookings` after step 8?

```sql
-- bookings(room int, slot int) starts empty
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
3. T1: SELECT * FROM bookings WHERE room = 1 AND slot = 9 FOR UPDATE;
4. T2: SELECT * FROM bookings WHERE room = 1 AND slot = 9 FOR UPDATE;
5. T1: INSERT INTO bookings VALUES (1, 9);
6. T1: COMMIT;
7. T2: INSERT INTO bookings VALUES (1, 9);
8. T2: COMMIT;
```

### 87.
Notice that T2 commits at step 6 after rolling back its savepoint. Does T1 succeed or fail with `40001`, and what is `bal` for `id = 1` after step 7?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100), (2, 100)
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT bal FROM accounts WHERE id = 1;
3. T2: BEGIN; UPDATE accounts SET bal = 90 WHERE id = 2;
       SAVEPOINT sp; UPDATE accounts SET bal = 200 WHERE id = 1;
4. T1: UPDATE accounts SET bal = 150 WHERE id = 1;
5. T2: ROLLBACK TO SAVEPOINT sp;
6. T2: COMMIT;
7. T1: COMMIT;
```

### 88.
What happens after step 6?

```sql
-- parents(id int PRIMARY KEY): (1), (2)
-- children(id int PRIMARY KEY, parent_id int REFERENCES parents(id))
1. T1: BEGIN;
2. T2: BEGIN;
3. T1: DELETE FROM parents WHERE id = 1;
4. T2: INSERT INTO children VALUES (10, 2);
5. T1: DELETE FROM parents WHERE id = 2;
6. T2: INSERT INTO children VALUES (11, 1);
```

### 89.
Compare with Q74: here T2 runs `INSERT ... ON CONFLICT DO UPDATE` BEFORE T1 commits. What happens to T2 once step 4 commits?

```sql
-- kv(k text PRIMARY KEY, v int) starts empty
1. T1: BEGIN;
2. T1: INSERT INTO kv VALUES ('a', 1);
3. T2: BEGIN ISOLATION LEVEL REPEATABLE READ;
       INSERT INTO kv VALUES ('a', 2)
       ON CONFLICT (k) DO UPDATE SET v = 2;
4. T1: COMMIT;
```

### 90.
While T1 remains open after step 4, does step 5 block or complete immediately?

```sql
-- items(id int PRIMARY KEY): (1)
1. T1: BEGIN;
2. T1: SAVEPOINT s1;
3. T1: SELECT count(*) FROM items;
4. T1: ROLLBACK TO SAVEPOINT s1;
5. T2: ALTER TABLE items ADD COLUMN note text;
```

### 91.
A backend endpoint runs a `SELECT`-then-`UPDATE` read-modify-write on the same row. Someone changes its isolation level from `READ COMMITTED` to `REPEATABLE READ` without adding `FOR UPDATE` or a retry loop. What changes when two requests hit the same row concurrently?

(a) Both requests always succeed with no lost updates because `REPEATABLE READ` queues writers
(b) Instead of silently losing one update, the second request fails with `40001` and returns an error to the caller
(c) The second request silently loses the update just as before because `REPEATABLE READ` does not detect write conflicts
(d) Both requests fail with `40P01` deadlocks

### 92.
What `id` does step 3 return (for T2), and what `id` does step 4 return (for T3) once step 5 rolls back?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN;
2. T1: UPDATE jobs SET status = 'done' WHERE id = 1;
3. T2: BEGIN;
       SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED;
4. T3: SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE;
5. T1: ROLLBACK;
```

### 93.
Does step 8 succeed or fail with `40001`?

```sql
-- doctors(id int PRIMARY KEY, on_call bool): (1, true), (2, true)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
3. T1: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
4. T2: SELECT count(*) FROM doctors WHERE on_call;  -- gets 2
5. T1: UPDATE doctors SET on_call = false WHERE id = 1;
6. T2: UPDATE doctors SET on_call = false WHERE id = 2;
7. T1: ROLLBACK;
8. T2: COMMIT;
```

### 94.
What `(table_bal, updated_bal)` does this single statement return?

```sql
-- accounts(id int PRIMARY KEY, bal int): (1, 100)
WITH u AS (
  UPDATE accounts SET bal = bal - 50 WHERE id = 1 RETURNING bal
)
SELECT (SELECT bal FROM accounts WHERE id = 1) AS table_bal,
       (SELECT bal FROM u) AS updated_bal;
```

### 95.
Does step 4 succeed or fail with `40001`?

```sql
-- parents(id int PRIMARY KEY, name text): (1, 'a')
-- children(id int PRIMARY KEY, parent_id int REFERENCES parents(id))
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT name FROM parents WHERE id = 1;
3. T2: INSERT INTO children VALUES (10, 1);
4. T1: UPDATE parents SET name = 'b' WHERE id = 1; COMMIT;
```

### 96.
Compare with Q66: here T1 uses `REPEATABLE READ`. What happens at step 4?

```sql
-- jobs(id int PRIMARY KEY, status text): (1, 'open'), (2, 'open')
1. T1: BEGIN ISOLATION LEVEL REPEATABLE READ;
2. T1: SELECT count(*) FROM jobs;
3. T2: UPDATE jobs SET status = 'done' WHERE id = 1;
4. T1: SELECT id FROM jobs WHERE status = 'open'
       ORDER BY id LIMIT 1 FOR UPDATE;
```

### 97.
An e-commerce app runs checkouts at `SERIALIZABLE`. A nightly analytics job runs `SELECT sum(amount) FROM orders;` (sequential scan) over the same table. Which statement is true?

(a) Running the analytics job at `READ COMMITTED` causes `40001` failures in checkouts because it scans the whole table
(b) Running the analytics job at plain `SERIALIZABLE` avoids `40001` failures because it never writes to `orders`
(c) Running the analytics job at `READ COMMITTED` causes no SSI `40001` failures; switching it to plain `SERIALIZABLE` can trigger `40001` failures via a relation-level predicate lock, whereas `SERIALIZABLE READ ONLY DEFERRABLE` avoids `40001`
(d) Running the analytics job at `SERIALIZABLE READ ONLY DEFERRABLE` blocks all concurrent checkouts until the analytics scan finishes

### 98.
Does step 5 block, or does it return immediately—and what rows does it return?

```sql
-- accounts(id text PRIMARY KEY, bal int): ('x', 0), ('y', 0)
1. T1: BEGIN ISOLATION LEVEL SERIALIZABLE;
       SELECT bal FROM accounts WHERE id = 'y';              -- gets 0
2. T2: BEGIN ISOLATION LEVEL SERIALIZABLE;
       UPDATE accounts SET bal = 20 WHERE id = 'y'; COMMIT;
3. T3: BEGIN ISOLATION LEVEL SERIALIZABLE READ ONLY DEFERRABLE;
4. T1: UPDATE accounts SET bal = 10 WHERE id = 'x'; COMMIT;
5. T3: SELECT id, bal FROM accounts ORDER BY id; COMMIT;
```

### 99.
Each user in `users(id PK)` owns multiple rows in `accounts(acct_id PK, user_id REFERENCES users(id), bal int)`. Concurrent withdrawals on *different* accounts of the same user must never let that user's combined `sum(bal)` drop below `0`. Which approach enforces this invariant WITHOUT using `SERIALIZABLE`?

(a) Run at `REPEATABLE READ`, check `SELECT sum(bal) FROM accounts WHERE user_id = $u`, then `UPDATE` the chosen `acct_id`
(b) Run at `READ COMMITTED`, and use `UPDATE accounts SET bal = bal - $amt WHERE acct_id = $id AND (SELECT sum(bal) FROM accounts WHERE user_id = $u) >= $amt`
(c) Lock the user's parent row with `SELECT 1 FROM users WHERE id = $u FOR UPDATE`, then check `sum(bal)` and `UPDATE` the chosen `acct_id`
(d) Run at `READ COMMITTED`, lock the chosen account with `SELECT bal FROM accounts WHERE acct_id = $id FOR UPDATE`, check `sum(bal)`, then `UPDATE`

### 100.
`users(id SERIAL PRIMARY KEY, email text UNIQUE)` starts empty, and `invites` has `('ABC', false)`. A `SERIALIZABLE` retry loop runs the code below. The first attempt fails at `COMMIT` with `40001`, rolls back, and the second attempt commits cleanly. How many welcome emails are sent, and what `id` is stored in `users`?

```sql
-- retry loop on SQLSTATE 40001:
BEGIN ISOLATION LEVEL SERIALIZABLE;
INSERT INTO users(email) VALUES ('a@b.com') RETURNING id;
-- app immediately calls send_welcome_email('a@b.com')
UPDATE invites SET used = true WHERE code = 'ABC';
COMMIT;
```

# Grade: pattern.quiz v0.2.0, input 3 (PostgreSQL isolation levels, high), part 2 of 2

Grader: head (independent of builder and writer). Date: 2026-11-24.

Scope: checks 2 and 3 for Q51 to Q100. All other checks (1, 4 to 14, 16) for the whole set of 100. Check 15 is N/A. Checks 2 and 3 for Q1 to Q50 are in `grades/3-postgres-isolation-part1.md`. I did not read it.

Read: the design doc, `tests/pattern.quiz/rubric.md`, `inputs.md`, `failures.md` (empty), the frozen `runs/v0.2.0/prompt.md`, `3-postgres-isolation/questions.md` and `answers.md`, and `grades/1-react-effects.md` for calibration. I ignored `runs/v0.2.0-gemini-4-neon/`.

Stated assumptions (`questions.md` line 2): PostgreSQL 16 defaults (READ COMMITTED, deadlock_timeout 1 s, no lock or statement timeouts); A, B and C are separate connections in autocommit unless BEGIN was issued; steps run in numbered order; a blocked step stays blocked while other sessions proceed; tables hold exactly the given rows, `id` is the primary key, no other sessions.

## Tally

| # | Check | Verdict |
| --- | --- | --- |
| 1 | Count | Pass |
| 2 | Correct (Q51 to Q100) | Borderline (Q65, Q86: right answers, trace steps in the wrong order) |
| 3 | Determinate (Q51 to Q100) | Pass |
| 4 | Assumptions | Pass |
| 5 | Prediction | Pass |
| 6 | No trivia | Pass |
| 7 | Trap named | Pass |
| 8 | Answer shape | Pass (Q36 over the ceiling at about 190 words) |
| 9 | Coverage | Fail (Q52/Q72 and Q65/Q87 differ only in surface details) |
| 10 | Distractors | Borderline (Q27 option (d)) |
| 11 | Artifact size | Pass |
| 12 | Progression | Pass |
| 13 | Answers hidden | Pass |
| 14 | Honesty and source | Pass |
| 15 | Diagnosis | N/A (input 9 only) |
| 16 | No copying | Pass |

Within my scope: Pass 12, Borderline 2, Fail 1, N/A 1. Check 2 and check 3 for the whole input also depend on part 1's result for Q1 to Q50.

## Check 2 and 3: independent trace, Q51 to Q100

I worked each question from the question text and the stated assumptions, and wrote down my result before opening `answers.md`.

| Q | My result | Stated result | Agree |
| --- | --- | --- | --- |
| 51 | (a) only 3 and 1003 | (a) | yes |
| 52 | B waits; after A's commit the EvalPlanQual re-check sees 'taken', so UPDATE 0 | same | yes |
| 53 | Snapshot taken at step 3, after B's first commit: (1, 10), (2, 101) | same | yes |
| 54 | No wait (SIREAD locks block nothing); 100; COMMIT succeeds (B is not serializable, so no conflict is even recorded) | same | yes |
| 55 | 4 (no constraint, both counts 2) | 4 | yes |
| 56 | Snapshot at step 3 already includes B's 0; no concurrent update; 5 | same | yes |
| 57 | B's speculative insert waits on A's pending key; A rolls back; B inserts; 5 | 5 | yes |
| 58 | Step 4 no wait (share/share); step 5 waits (FOR NO KEY UPDATE conflicts with A's FOR SHARE) | same | yes |
| 59 | Waits: A's ACCESS SHARE on `orders` is held to end of transaction | same | yes |
| 60 | 6 (INSERT ... SELECT does not see its own new rows) | 6 | yes |
| 61 | (1, 'held'), (2, 'new'), (3, 'new') | same | yes |
| 62 | -100 (write skew; different rows) | -100 | yes |
| 63 | 100, 1 (RR applied only to the empty first transaction) | same | yes |
| 64 | (a) | (a) | yes |
| 65 | Waits until step 4, then returns only 2 | same | yes |
| 66 | 0; duplicate key error (RR gives unique violation; the serialization-error substitution is SERIALIZABLE only) | same | yes |
| 67 | No wait: a row failing the WHERE is not locked | same | yes |
| 68 | No rows; 1 | same | yes |
| 69 | 2; no row returned, 'a' (id 1) missed | same | yes |
| 70 | Waits on FOR KEY SHARE vs the delete's lock, then FK violation after A commits | same | yes |
| 71 | No wait; 0 (TRUNCATE not MVCC-safe) | same | yes |
| 72 | B waits, then UPDATE 0; final 20 | same | yes |
| 73 | Retry count 1; 1 on duty (bo) | same | yes |
| 74 | (c) | (c) | yes |
| 75 | Step 5 serialization failure (row 2 changed after snapshot); step 6 ROLLBACK; step 7 (1, 100), (2, 0), (3, 0) | same | yes |
| 76 | 3; 3 seats | same | yes |
| 77 | 100, 100 (B's snapshot at step 4, A uncommitted) | same | yes |
| 78 | TRUNCATE waits for A's ACCESS SHARE; step 4 returns 3 | same | yes |
| 79 | 100 and 100 | same | yes |
| 80 | Serialization failure (ON CONFLICT target not visible to the RR snapshot) | same | yes |
| 81 | (a) both commit; B is RR so SSI records nothing for it | Both commit | yes |
| 82 | 100, 5 | same | yes |
| 83 | B's step 7 fails at once; retry reads 150, writes 180 | 180 | yes |
| 84 | B waits; after A's commit job 1 fails the re-check, LockRows (below Limit) pulls job 2; returns 2 after step 6 | same | yes |
| 85 | (1, 300), (2, 300) | same | yes |
| 86 | (1, 100), (2, 200) | same | yes |
| 87 | Only 'bo' after A commits; 1 on duty | same | yes |
| 88 | 0; waits, then INSERT 0 0; 0 | same | yes |
| 89 | 2; count 1, max 2 | same | yes |
| 90 | Waits, then "could not serialize access due to concurrent update" after A commits | same | yes |
| 91 | (1, 101), (2, 101) | same | yes |
| 92 | Waits, then duplicate key error at A's commit; 1 booking | same | yes |
| 93 | No rows, after A commits | same | yes |
| 94 | 1, 1 (SET TRANSACTION accepted before first query; snapshot at step 4) | same | yes |
| 95 | 95 (A's +10 lost) | 95 | yes |
| 96 | B's lock succeeds without error (row only locked, not updated); snapshot from step 5 counts 2; 4 seats | same | yes |
| 97 | Serialization failure (first-updater rule depends only on A's level) | same | yes |
| 98 | (c) | (c) | yes |
| 99 | Step 3 updates own row to 2 without waiting; step 4 no rows; step 6 returns 2 | same | yes |
| 100 | 100; serialization failure at step 8 | same | yes |

50 of 50 agree. 0 disagree. 0 ambiguous.

### False steps in correct traces

Q65 and Q86 have the right answers, but each trace describes the wrong order of events.

- Q86, Why: "3. Row 2 is free: B doubles it to 200. 4. Row 1 is locked, so B waits." B's statement is a sequential scan of a two-row heap. It reaches row 1's old version first (still visible to B, and its xmax is A, which is in progress), so heap_update blocks there. It reaches row 2 only after A commits. While B waits, row 2 is still 100 and unlocked. The trace teaches that a blocked UPDATE does the free rows first and then queues, and a learner who carries that into a deadlock or third-session question will get it wrong.
- Q65, Why: "Job 2 is free and B locks it. Job 1 is locked by A, so B waits." This is the same inversion for `SELECT ... FOR UPDATE`, because LockRows locks rows as the scan returns them. The same writer gets the order right in Q84 ("B's query reaches job 1 first and waits"), so the set contradicts itself.

The rubric scores a correct answer with a false trace step as Borderline. **Verdict: Borderline (Q65, Q86).**

Not scored, but a simplification: in Q54, "There is one dependency: A read a version that B later replaced ... One edge is not a cycle." This is true of the history. But SSI never records that edge, because B runs READ COMMITTED (the set's own mechanism 21, Q44, Q81). The real reason A commits is that the edge is not recorded at all, as well as being harmless. Add a clause.

### Check 3 (Q51 to Q100)

The likely ambiguity points are all pinned down. Q73 names the victim ("assume it is B"), and so does Q91 ("rolls back B"). Q74 and Q98 offer options that do not depend on which transaction is the victim or when it fails. Q87 and Q96 add "if B follows its rule". Q55 and Q62 state or imply both counts. Q84's answer does not depend on the plan, because LockRows always sits below Limit. Q65 and Q86 give the same final result whichever scan order applies. **Pass.**

## Other checks, whole set

**1 Count.** Q1 to Q100, continuous, high depth. Pass.

**4 Assumptions.** The opening fixes the version, the defaults, deadlock_timeout, the absence of lock_timeout (needed by Q19), autocommit, step ordering and blocked-step behavior. Sequence cache 1 (Q18, Q38, Q69, Q89) is covered by "default settings". No answer rests on an unstated setting. Pass.

**5 Prediction.** Every question asks for an outcome from a numbered multi-session artifact or a concrete described setup (Q32, Q51, Q79). Q64 asks which change fixes code, which is still an artifact-based prediction. Close to 100%. Pass.

**6 No trivia.** Error strings appear only in answers, as the observable outcome. Q37 asks what SHOW reports, which is behavior. Pass.

**7 Trap named.** Every trap names a concrete wrong belief, for example Q61 "after waiting, B sees A's committed data and searches again" and Q96 "waiting for the lock means B's later reads see what A committed". None is generic. Pass.

**8 Answer shape.** All 100 have Why, Answer, The trap and Rule, in that order. I estimated word counts. The shortest are Q39 (about 72), Q60 (about 80) and Q67 (about 81). The clearest overrun is Q36, at about 190 words: its Why is about 120 words and includes the SSI naming and a "normally B, at COMMIT" aside. Q8 (about 150) and Q96 (about 152) sit at the ceiling. That puts at least 97% in range. Pass.

**9 Coverage.** The 31-item mechanism map is at the head of `answers.md`, and the opening has no map. I checked the union of the mapped numbers: every question from 1 to 100 appears. Every mechanism maps to at least two questions. The rubric's last clause fails, though: "No two questions differ only in surface details."
- **Q52 and Q72.** Both run the same conditional `UPDATE ... WHERE id = 1 AND <predicate on the SET column>` from two sessions. The first commits, the second waits, the re-check fails and it reports UPDATE 0. The traps name the same belief: Q52 "B applies its change to the version it saw first", Q72 "B's condition was satisfied when it started and so stays satisfied". Status text versus `bal >= 80` is a surface change, and Q72's extra "final balance" follows trivially. Q72 also sits in band 3 without combining anything.
- **Q65 and Q87.** In both, `SELECT ... FOR UPDATE` matches two rows, A changes one and commits, B's re-check drops it and B returns the other. The traps are the same: Q65 "FOR UPDATE returns the rows its snapshot matched", Q87 "B's locking read returns what its snapshot matched". Q87's write-skew framing gives it a purpose, but its trace and the belief it tests are Q65's.

Q43 and Q92 are close, but their tested beliefs differ ("unique check uses the SELECT's view" against "a constraint cannot protect rows that do not exist yet"). Q76 and Q96 are a deliberate one-setting contrast that changes the outcome, which the prompt explicitly allows. I accept both pairs. **Fail (Q52/Q72, Q65/Q87).**

**10 Distractors.** I checked 13 multiple-choice questions: Q1, Q5, Q8, Q15, Q17, Q19, Q27, Q35, Q36, Q51, Q64, Q74 and Q98. All wrong options map to a belief except one. In Q27, option (d) "2" is explained as "(d) assumes one update is lost". One lost update leaves 1 person on duty, not 2, so the stated belief does not produce this option, and no other belief in the trap does either. It is the filler the rubric excludes. Replace (d) with an option that a real belief produces, for example "(d) 1, because one transaction's commit overwrites the other's row", or rewrite the explanation to name a belief that yields 2. Q98 (d), "duplicate key error", is defensible as carry-over from Q92. **Borderline (Q27).**

**11 Artifact size.** The longest artifacts are 8 SQL lines (Q13, Q27, Q31, Q36, Q44, Q62, Q73, Q83, Q84, Q92, Q96, Q98). The longest stems are Q96 and Q73, at about 70 words. The comments (`-- value it read + 50`) state what the application does, not the outcome. One note: Q73's premise, "Exactly one transaction fails", previews the shape of Q98's answer (c). It does not settle Q98, which turns on whether SSI catches inserts into a searched range. Pass.

**12 Progression.** Band 1 is Q1 to Q20 (20%), band 2 is Q21 to Q70 (50%) and band 3 is Q71 to Q100 (30%). Band 3 combines mechanisms: Q73 (SSI and retry), Q75 (RR skip, first-updater rule and abort), Q83 (lost update, RR and retry), Q96 (RR snapshot timing and parent-row locking) and Q100 (savepoint, retained snapshot and first-updater rule). It also tests edge cases: Q71 and Q78 (TRUNCATE), Q80 (RR upsert) and Q99 (own pending row). Q72, Q82 and Q85 are single-mechanism items placed in band 3. Pass.

**13 Answers hidden.** `questions.md` contains no answers. The key is a separate file. Pass.

**14 Honesty and source.** No area was declared unreliable, and none needed to be. I checked the quoted server messages against PostgreSQL behavior: Q4 "there is no transaction in progress", Q17 "SET TRANSACTION ISOLATION LEVEL must be called before any query", Q30 "could not obtain lock on row in relation", Q37 "SET TRANSACTION can only be used in transaction blocks", and the serialization and duplicate-key messages. All are real. No invented API or default. Pass.

**16 No copying.** None of the three calibration examples (React effects, zero-coupon bond, Python mutable default) is reused. Pass.

## Single most important prompt fix

Check 9 is the only Fail. The prompt already asks for different shapes, but at high depth (100 questions over 31 mechanisms) the writer met the "at least twice" floor by restaging. It never tested whether two questions really differed. The plan never asks the writer to name each question's target belief, so the check has nothing concrete to compare. The fix goes in `<plan>` step 6.

Quote:

> Test every mechanism at least twice, in different shapes, so the learner proves they hold the rule and did not just recognize a scenario.

Replacement:

> Test every mechanism at least twice, in different shapes, so the learner proves they hold the rule and did not just recognize a scenario. Note for each question the wrong belief it targets. Two questions on the same mechanism have different shapes when they target different wrong beliefs, ask for a different kind of outcome, or change one setting so that the outcome changes. New table names, values or wording do not count, because the learner who solved the first already holds the answer to the second. At high depth, reach the count by combining mechanisms or by changing a setting that changes the outcome, not by restaging an earlier question.

Matching `<check>` line, replacing "Every mechanism is tested at least twice, in different shapes, and no two questions differ only in surface details.":

> - Every mechanism is tested at least twice. For any two questions on the same mechanism, the targeted wrong beliefs differ, or the kind of outcome differs, or one changed setting changes the outcome.

Over-correction risk: the writer may drop the useful one-setting contrast pairs (Q22/Q77, Q27/Q44/Q73, Q36/Q81, Q76/Q96, Q71/Q78), which are among the set's best items. The wording keeps them explicitly ("change one setting so that the outcome changes"). On the rerun, confirm that those pairs survive and that Q52/Q72-style restagings are gone.

## Lower-priority notes for the builder

- Q65, Q86: reorder the trace so that B waits on row 1 first and handles row 2 after A commits (check 2 Borderline). A prompt-level nudge, if one is wanted: in `<domain>`, after "number every step in one global order", add "and within one statement, follow the order in which rows are reached". Test it before adopting it. It is a narrow fix and may not generalize.
- Q27 (d): replace the option or its explanation (check 10).
- Q54: add that SSI records no conflict for B, because B is READ COMMITTED.
- Q36: cut the Why to under 100 words. The SSI expansion can move to the Rule or be dropped.
- Q72: either replace it with a combining item for band 3, or move it to band 2 and give it a different belief, for example a predicate on a column B does not SET.

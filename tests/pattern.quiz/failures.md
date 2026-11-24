# Upskill quiz failure log

One line per failure: version, input, check, what went wrong.

- v0.2.0, input 1, check 16 (Borderline): Q11 is calibration example 1 with effect B removed; same artifact, stem and belief.
- v0.2.0, input 4, check 16 (Fail): Q8 is the bond calibration example with coupons 0/5 changed to 2/9; traps copied almost word for word. Q24 reuses the same two bonds.
- v0.2.0, input 4, check 9 (Fail): Q17/Q48, Q14/Q36 and Q11/Q37 differ only in numbers or direction of the move.
- v0.2.0, input 4, check 10 (Fail): Q23(c) and Q33(b) match no real belief.
- v0.2.0, input 4, check 4 (Borderline): Q46 only works if the week passing in the stem is ignored; opening never says so.
- v0.2.0, input 3, check 9 (Fail): Q52/Q72 and Q65/Q87 restage the same scenario with the same targeted belief.
- v0.2.0, input 3, check 2 (Borderline): Q65 and Q86 reach the right answer with a trace that has B touch row 2 before blocking on row 1; Q84 gets the order right.
- v0.2.0, input 3, check 10 (Borderline): Q27(d) "2" is explained by "one update lost", which would give 1.
- v0.2.0, input 5, check 11 (Borderline): "What happens when this runs?" used only for snippets that raise (Q1, Q7, Q11, Q14, Q17, Q22), leaking the outcome.
- v0.2.0, input 5, check 14 (Borderline): Q5 trap "(map has none by default)" implies the 3.14 strict= option under stated CPython 3.12.
- v0.2.0, input 5, check 10 (Borderline): Q29(c) list(pairs) is a no-op on a list, a filler option.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 1, check 2 & 3 (Fail): Q23 claims `setN(n + 1)` loops forever (false at `2**53`); Q19 allows two defensible lines.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 1, check 10 (Fail): Q8(b) `7` does not follow from ignoring updaters (which yields `2`).
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 3, check 2 & 14 (Fail): Q54 and mechanism 25 falsely claim `ON CONFLICT DO NOTHING` skips cleanly under `REPEATABLE READ` (PG 16 raises `40001`).
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 3, check 3, 4, 9, 10 (Fail): Q46(d) also removes deadlock; Q33/Q80/Q100 omit fresh-sequence assumption; Q1/Q2 and Q32/Q75 duplicate shapes; Q38(d) is a meta-option.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 4, check 16, 9, 10, 11, 14 (Fail): Q8 echoes bond calibration example; Q10/Q28 and Q26/Q36 repeat shapes; Q15(d) is impossible ("falls from $100 to $102"); Q25 stem leaks 6% yield; Q56 overclaims call trigger.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 5, check 13, 9, 10 (Fail): opening scope note gives away Q1 (`list` has no `.map()`); combined mechanism 9 hides missing second closure Q; Q8(b)/(d) distractors are inconsistent.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 7, check 2, 3, 9, 10, 11, 13, 14 (Fail): Q12 says Mac needs nothing else (omits required status line); Q25/Q29 overclaim beyond `loop/LOOP.md`; Q3/Q20 duplicate; Q17(b)/(c) filler; Q27 quotes file and agent verbatim.
- v0.2.0 (gemini-4-neon / gpt-6.2-astra), input 9, check 9 (Fail): Q15 repeats Q4's independent-counter shape with surface changes.

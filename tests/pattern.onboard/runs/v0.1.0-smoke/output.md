## Must know and mental model

Callers use `minutes(seconds)` to convert seconds to whole minutes. The function uses Python floor division (`//`), so `119` seconds returns `1`. (`src/units.py` · `minutes`)

`119 seconds` → passed to `minutes` → evaluated as `119 // 60` → returns `1` → compared with `1` by the assertion.

## Walk one case and reading route

Open `src/units.py` at `minutes` and predict the return value. The function has no branch or state change. Then open `tests/test_units.py` at `assert minutes(119) == 1`. The test imports and invokes the same function and records the expected result. No test run was supplied.

## First change and verification

For a concrete change, suppose the requirement is to round **nonnegative integer seconds** up to the next whole minute. Edit `minutes` to return `(seconds + 59) // 60` for those inputs. The supplied assertion is the visible consumer of the old behavior. Update its expected result from `1` to `2` if the new contract is intentional. As a separate check, verify that `minutes(120)` still returns `2`.

**Special case.** Today, `minutes(-1)` returns `-1` because floor division rounds toward negative infinity. Decide whether to preserve that behavior before applying the new expression to negative inputs. (`src/units.py` · `minutes`)

## Coverage and gaps

The inline dump supplies two relative paths in order. No checkout root or revision was supplied. Inventory accounted for **2/2**, full contents read **2/2**, sampled **0**, indexed **0**, unavailable **0**. VCS internals are excluded. Files beyond the dump, other callers, and the configured test invocation are unknown.
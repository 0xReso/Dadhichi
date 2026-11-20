### Must know

Engineers maintaining the export pass row mappings to `render` and get a list of display names. In revision `b2`, `render` calls `labels.display`. The `a1` checkpoint names `formatter.upper_name`, which remains in the dump as an uppercase helper. Open `src/export.py::render` first.

### Mental model and walkthrough

Row mapping → `src/export.py::render` reads `name` → `src/labels.py::display` chooses a label → returned list.

A row mapping with `name="Ada"` yields `["Ada"]`, preserving case. An absent key or explicit `None` reaches `display` as `None`. An empty string also yields `"(missing)"` because `display` uses `or`. The CSV-to-mapping step and the caller of `render` are outside the supplied trace.

### First change and verification

Read `render` for the call site, then `display` for the fallback. Change the literal in `display` if all its callers should adopt the new label. For an export-only change, apply the fallback in `render`.

The supplied `tests/test_labels.py` assertion expects `display(None)` to return `"(missing)"`. Update it if the helper’s contract changes. Add a `render` check with an absent key, `None`, `""`, and `"Ada"`. Expect three new labels followed by `"Ada"`.

### Coverage and gaps

`b2` paste, no checkout census. All four supplied paths accounted for: read 3 Python files, sampled 1 (`archive.csv`, header and first row), indexed 0, unavailable 0. VCS internals excluded. Additional paths unknown. No code executed.
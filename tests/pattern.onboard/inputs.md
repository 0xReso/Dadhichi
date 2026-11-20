# Onboarding fixtures

Each numbered case is independent. Supply the material inside its block as PROJECT. Omit optional fields unless specified. Each line describes the entire contents of one file unless marked otherwise.

## 1. Tiny library

```text
src/units.py | def minutes(seconds): return seconds // 60
tests/test_units.py | from src.units import minutes; assert minutes(119) == 1
```

## 2. Monorepo and stale documentation

FIRST_TASK = change the invoice limit. READER = mid-level engineer.

```text
README.md | Each invoice can contain 20 items.
apps/api/submit.js | import {limit} from '../../packages/contracts/limit.js'; export const submit = items => items.length <= limit ? 'queued' : 'rejected';
packages/contracts/limit.js | export const limit = 12;
apps/api/submit.test.js | import {submit} from './submit.js'; console.assert(submit(Array(13)) === 'rejected');
.github/workflows/check.yml | steps: [{run: node apps/api/submit.test.js}]
```

## 3. Research dump without filenames

```text
[fragment] Trial question: does a second rinse remove residue?
[fragment] Notebook excerpt: sample B broke before weighing.
[fragment] Decision note: repeat B before comparing the two rinses.
```

## 4. Partial, unfamiliar system

```text
Directory listing only. Content unavailable.
selwick.toml
coil/fold.slk
reports/latest.bin
```

## 5. High-volume mixed export

BUDGET = 180 words. Supply the following archive manifest and two inline bodies. The metadata ranges denote distinct actual entries.

```text
src/export.py | def render(rows): return [r['name'] for r in rows if r['active']]
tests/test_export.py | from src.export import render; assert render([{'active': False}]) == []
vendor/font-0001.bin through vendor/font-1000.bin | metadata only
.env | metadata only
private/spec.txt | permission denied
```

## 6. Declarative infrastructure

READER = senior engineer. FIRST_TASK = change retention.

```text
main.tf | module "archive" { source = "./modules/archive" }
modules/archive/main.tf | resource "aws_cloudwatch_log_group" "events" { retention_in_days = 14 }
README.md | Before changing retention, get approval from the data owner.
```

## 7. Resuming an older guide with a large export

FIRST_TASK = change how missing names appear in the export. BUDGET = 220 words. Supply this previous checkpoint and current dump; file contents are complete except for the explicitly sampled CSV.

```text
Previous checkpoint (revision a1): formatter.upper_name supplies the export name. Next: inspect its null handling.
Current dump (revision b2):
src/export.py | from .labels import display; render = lambda rows: [display(r.get("name")) for r in rows]
src/labels.py | def display(name): return name or "(missing)"
src/formatter.py | def upper_name(name): return name.upper()
tests/test_labels.py | from src.labels import display; assert display(None) == "(missing)"
archive.csv | 900000 rows according to manifest; only header and first data row supplied: id,name / 1,Ada
```

Check whether the guide corrects the stale caller using the import and call in b2, names the relevant test, counts the CSV as sampled, and leaves the prevalence of missing names unknown.

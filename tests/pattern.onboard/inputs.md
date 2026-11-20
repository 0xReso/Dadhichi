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

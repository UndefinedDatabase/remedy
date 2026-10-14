# Rehearsal of job job-rehearsal-fixture

Rehearsed at 2026-10-14T00:00:00+00:00 on /tmp/rehearsal-fixture at commit deadbeefcafef00dfacade0123456789abcdef0. No job was run, no builder or reviewer was built, nothing was applied, and nothing was written to the repository.

## What planning cost

2 planning call(s) recorded in the job's prompt trace (intake, task_plan): about 500 prompt tokens, estimated from 2000 prompt characters. The answers' tokens and the price of these calls are not recorded, so no cost in dollars is claimed. The study and the mission's own plan are not counted here.

## What the run would cost

| Task | Title | Plan band | Estimate in USD |
|---|---|---|---|
| T001 | Write the thing | M | 80.0000–80.0000 |
| T002 | Polish it | none | not available |

Whole job: not available USD. Basis: estimate_unavailable.

## Risks

- the fixture might drift

Normalization:
- merge T001, T002 → T001: too small to split

## Definition of done

| Check | Kind | Blocking | Source |
|---|---|---|---|
| tests-pass | custom_cmd | yes | compiled |
| lint-clean | custom_cmd | no | standard |

Not compiled: lint-clean.

## What the run could write

- would write `src/app.py`
- would be blocked `.git/config`: denied:builtin:git directory

## To run it for real

- `remedy job run job-rehearsal-fixture`

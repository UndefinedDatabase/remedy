# Job Budget Enforcement v0

> What a Remedy JOB may consume, and how a run is stopped before it exceeds
> that. Built by F018 (the four original limits), F104 (the money limit and
> the predictive stop) and F276 (the disk floor). The target plan is
> [T2_F104.md](../roadmap/features/T2_F104.md); this page describes what is
> built. Not the *run contract* budgets of
> [run-contract-v1.md](run-contract-v1.md) — those are the loop / test / runtime
> caps of a single run contract, a different mechanism.

## The six limits

A job carries an optional `JobBudgets` record, resolved by
`packages/orchestration/budget_resolution.py` with the precedence **CLI flag >
env var > project `remedy.toml` > no limit**. Unset means *no limit* there; a
run then fills what is still unset from its provider class's profile (below).

| Limit | Unit | Flag |
|---|---|---|
| `max_provider_calls` | calls | `--max-provider-calls` |
| `max_total_tokens` | tokens | `--max-total-tokens` |
| `max_cost_usd` | US dollars | `--max-cost-usd` |
| `max_wall_clock_minutes` | minutes | `--max-wall-clock-minutes` |
| `deadline` | ISO-8601 UTC instant | `--deadline` |
| `min_free_disk_bytes` | bytes free | *(no flag; config only)* |

`min_free_disk_bytes` (F276) is the only FLOOR here and the only one with no CLI
flag: it is a property of the machine rather than of an invocation, so it is set
through `budget.min_free_disk_bytes` in `remedy.toml` or the environment variable
`REMEDY_BUDGET_MIN_FREE_DISK_BYTES`. Every other limit is exhausted at
`counter >= limit`; this one at `free < floor`, so a floor of N accepts exactly N
free bytes. The reading comes from `budget_guard.free_disk_bytes`, an injectable
seam over `shutil.disk_usage` of the DATA ROOT's filesystem, and the probe is
called only when the floor is configured.

When several limits are exhausted at once, the one REPORTED is the first in
`_LIMIT_ORDER` (`packages/orchestration/budget_guard.py`), which is
`min_free_disk_bytes` and then the table order above. The disk is first because
every other limit is one an operator can simply raise, and raising a token limit
on a machine with no space walks the job into the same wall. That is a reporting
rule only: any exhausted limit stops the job.

Every `JobBudgets` field is also part of the CLOSED budget schema of the F012 run
manifest (`_budget_allowed_keys()` in `packages/orchestration/run_manifest.py`),
which DERIVES the set from `JobBudgets.model_fields`. A budget field `JobBudgets`
accepts but the manifest rejects cannot FINALIZE a stop at all — the job is left
running with the stop request pending — and that failure has now happened twice,
once for `max_cost_usd` (R-0225) and once for `min_free_disk_bytes`, which is why
the list is derived rather than spelled a second time.

## Profiles per provider class

> Status (F310, 2026-10-20): built by F310's first round; DECISIONs F310 D1 to D3 in
> `.agent/decisions.md`.

A job is of the `local` class when every role that runs it, the builder, the reviewer and a
repair provider when one is set, uses a model that Ollama serves on this machine: the providers
`ollama` and `pi`, with any model whose name does not end in `-cloud` or `:cloud`. Every other job
is of the `paid` class, a job run by the test provider `fake` included, because the paid profile is
the behaviour every test of a fake run is written against. `job_provider_class` in
`packages/orchestration/budget_profiles.py` decides it.

Each class has a profile of default limits:

| Limit | `local` | `paid` |
|---|---|---|
| `max_total_tokens` | 1,500,000 | none |
| `max_provider_calls` | 200 | none |
| `max_wall_clock_minutes` | 480 | none |
| `max_cost_usd` | *(not a key)* | none |

The numbers are configuration, `budget.profile.local.*` and `budget.profile.paid.*`, listed in
[the environment guide](../guides/environment.md). A local model reports no price, so the local
profile has no money limit at all.

When `run_job` starts, it reads each limit from the first place that sets it: the job's own
budgets, which a person, an order's caps or a budget decision wrote; then the configured
`budget.*` value of the same name; then the profile of the job's class
(`effective_job_budgets`). The profile's values are never written into the job's record, so the
record keeps saying only what someone set.
A task plan's suggested budgets are the planner's estimate and are never a limit. An order's caps
are only what the order names: a profile fills each job's limits that the order leaves unset and
never becomes a cap of the whole order. `GET /api/v1/execution` and `remedy client execution`
name both profiles with their numbers under `budgets.profiles` and each offered provider's class.

## The working wall clock

> Status (F310, 2026-10-20): built by F310's second round; DECISION F310 D4 in
> `.agent/decisions.md`.

`max_wall_clock_minutes` measures the time a job's runs were alive, not the time since it first
started. Every gap between two runs of a job is waiting: the time it waited for a decision, for a
stop or a pause to be answered, in a queue, for a lock that kept a run from starting, or after a
run died. When a run starts again, `resume_job_clock` in `packages/orchestration/budget_clock.py`
adds the gap from the job's last saved record to the seconds it has waited, and the guard measures
from `first_running_at` plus those seconds. The Pi call's own time bound reads the same limits and
the same start. Inside a run nothing counts as waiting: until a call's own time-out ends it, a model
server that does not answer cannot be told from one that answers slowly.

The record `budget_actuals` carries the clock in version `3.0.0`: `waited_s`, the seconds waited so
far, and `active_until`, the moment the record was written. Versions 1 and 2 still read, as having
waited nothing.

## One stop, one question

> Status (F310, 2026-10-20): built by F310's third round; DECISION F310 D5 in
> `.agent/decisions.md`.

When the budget stops a job, its budget decision is the one question to answer. It names, under
`blockers`, the open blocking criteria of the job's mission, so the person sees what is left before
choosing. `extend` with no answer raises every limit the stop exhausted to twice the value the run
read, and the wall clock to at least 60 minutes, so a client need not compute new numbers; a
deadline and the disk floor are never doubled and still need an answer. An answer that is given
holds, but no answer can lower a limit below what the run read. Over the public API, the run starts
again by itself as soon as `extend` is answered, and the answer names it under `resumed`.

The mission's remainder decision, which offers a follow-up mission for the blocking criteria a
job left open, is no longer raised while the budget decision is open. It is raised once, when the
budget decision is answered `abandon` and the mission's contract still has blocking criteria,
because the stop is final from that answer on. A mission loop that reaches its iteration limit
raises it as before, since no budget decision is open there.

## Cost is nullable by design

Cost actuals come from the F103 per-project SQLite ledger
(`packages/orchestration/token_ledger.py`), which stores `NULL` for a call whose
provider reported no price. `SUM()` over all-NULL rows is NULL in SQLite and
nothing coerces that away: `BudgetCounters.measured_cost_usd` stays `None`.
`None` and `0.0` are different facts and are never repaired into one another
(P6). An unpriced spend renders `not-measured`, never `$0.0000`. A partly priced
spend renders as a FLOOR — `>= $0.6000 (1 provider calls unpriced)` — so what is
left of the limit is only a CEILING, `<= $1.4000`. No price is ever invented.

## Two stop paths

**Reactive** — after a provider call, at every safe point, `evaluate_budget`
compares recorded actuals against the limits and stops the job through the
ordinary F011 stop path with reason `budget_exhausted:<limit>`. This is the
BACKSTOP and it is unconditional. The `<limit>` is always the `JobBudgets` FIELD
name, `min_free_disk_bytes` included, so there is one stop vocabulary and not
two. The POST-MORTEM that stop writes carries terminal status and failure class
`budget_exhausted` for every limit except the disk floor, which gets its own
`disk_exhausted` (F276): a budget is exhausted by what this job spent and an
operator raises it, while the disk was exhausted by the machine and is often
nothing this job did, and folding the two would make "which of my jobs ran the
disk out" unanswerable.

**Predictive** — at the task-dispatch safe point in `run_job`
(`packages/orchestration/pingpong_job.py`), BEFORE a task is dispatched and
before its prompt is built, `predict_next_task_cost` asks whether the next task
would push the spend past `max_cost_usd`. If so the job stops with reason
`predicted_budget_exhausted:max_cost_usd` — zero provider calls made, every task
still pending — and the prediction is persisted verbatim to
`job.budget_prediction` so a human reading `job.json` sees the arithmetic.

The predictive check runs only when the operator stop and the reactive check
both declined. It never replaces the backstop; it only stops EARLIER.

## Where the estimate comes from

Expected tokens come from DOCUMENTED CLASS DEFAULTS unless the next task's class
is calibrated from the cost ledger (F074, `docs/system/estimate-calibration-v1.md`):
then the class's measured P50 is expected instead, labelled `calibrated(n)`.
The defaults are provisional and configurable:
`budget.class_default_tokens_low` / `_medium` / `_high` (8000 / 32000 / 120000).
The price basis (`budget.price_basis_usd_per_1k_tokens`) has NO default; with
none configured the predictive path is INERT and labels itself `no_price_basis`
(DECISION F104 D4), because an invented price would make every prediction a
fabrication.

The next task's token band is derived at the safe point from the task's own text
plus the token counts of prior proof summaries — not from the assembled prompt,
which is deliberately not built before the safe point (DECISION F104 D6). The
estimate is therefore a FLOOR: it can only UNDER-predict, which is exactly why
the reactive check remains the backstop.

## The five estimate_basis labels

Every predicted number carries one of these and no others
(`VALID_ESTIMATE_BASES`):

| Label | Meaning |
|---|---|
| `class_default` | the band was derived; its class default was used |
| `class_default_missing_band` | no band could be derived, so the LARGEST class default was used (A9: over-stopping beats overspending) |
| `no_price_basis` | no price basis configured, so no cost was predicted |
| `no_cost_limit` | no `max_cost_usd` set, so nothing to predict against |
| `unpriced_spend` | the spend so far is unpriced, so no honest comparison exists |

F074 adds one label family beside the five: `calibrated(n)`, a prediction read from
a task class calibrated on `n` measured tasks. It is compared against the limit
exactly as `class_default` is.

A breach is declared only when real numbers could be compared, and with a strict
`>`: the exact-limit boundary belongs to the reactive check, so the two can
never disagree about it.

## What `remedy job budget` shows

Without `set`, read-only. For a job with a money limit it prints the configured limits, the
spend, what remains, the next task's expected cost with its `estimate_basis` and
one-line arithmetic, and — if a predictive stop already happened — the recorded
arithmetic that justified it. Whatever limits the job has, it also prints the
recorded burn alarm, if `run_job`'s own burn monitor (F116,
`packages/orchestration/burn_detector.py` and
`packages/orchestration/job_burn.py`) recorded a trip: its rate against what
was expected and the window and multiplier behind it. `--json` adds
`prediction` (the live estimate, or `null`), `recorded_prediction` (the
persisted one, or `null`) and `burn_reading` (the persisted burn-alarm record,
or `null`) alongside `limits`, `counters` and `evaluation`. The estimate is
computed live and purely: the command writes nothing, persists nothing and
mutates no job, and any failure in the estimate degrades to a single
`unavailable (...)` line rather than failing the inspection. The one file the
estimate may refresh is the project's calibration snapshot under the data root,
a derived cache beside the cost ledger (F074).

`remedy job budget <job_id> set <field> <value>` is the command's one write
(DECISION F280 D3): one field of the job's run contract or token budget profile. It never
writes the F018 limits above, which `remedy job run <job_id>` takes as budget flags.

## Deliberately not built

Calibration of expected cost from run history is F074's, not F104's
(`docs/system/estimate-calibration-v1.md`). Per-task-class caps are out of scope
for F104. Burn-rate anomaly detection is
F116's, not F104's: it lives in `packages/orchestration/burn_detector.py` and
`packages/orchestration/job_burn.py`, and `remedy job budget` shows its newest
recorded trip (above).

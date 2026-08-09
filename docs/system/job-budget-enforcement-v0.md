# Job Budget Enforcement v0

> What a Remedy JOB may consume, and how a run is stopped before it exceeds
> that. Built by F018 (the four original limits) and F104 (the money limit and
> the predictive stop). The target plan is
> [T2_F104.md](../roadmap/features/T2_F104.md); this page describes what is
> built. Not the *run contract* budgets of
> [run-contract-v1.md](run-contract-v1.md) — those are the loop / test / runtime
> caps of a single run contract, a different mechanism.

## The five limits

A job carries an optional `JobBudgets` record, resolved by
`packages/orchestration/budget_resolution.py` with the precedence **CLI flag >
env var > project `remedy.toml` > no limit**. Unset means *no limit*.

| Limit | Unit | Flag |
|---|---|---|
| `max_provider_calls` | calls | `--max-provider-calls` |
| `max_total_tokens` | tokens | `--max-total-tokens` |
| `max_cost_usd` | US dollars | `--max-cost-usd` |
| `max_wall_clock_minutes` | minutes | `--max-wall-clock-minutes` |
| `deadline` | ISO-8601 UTC instant | `--deadline` |

When several limits are exhausted at once, the one REPORTED is the first in
`_LIMIT_ORDER` (`packages/orchestration/budget_guard.py`) — the table order
above. That is a reporting rule only: any exhausted limit stops the job.

`max_cost_usd` is also part of the CLOSED budget schema of the F012 run manifest
(`_BUDGET_ALLOWED_KEYS` in `packages/orchestration/run_manifest.py`). A budget
field `JobBudgets` accepts but the manifest rejects cannot FINALIZE a stop at
all — the job is left running with the stop request pending — so the two are
kept in step deliberately.

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
BACKSTOP and it is unconditional.

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

Expected tokens come from DOCUMENTED CLASS DEFAULTS, not calibration against
history — calibration is out of scope. They are provisional and configurable:
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

A breach is declared only when real numbers could be compared, and with a strict
`>`: the exact-limit boundary belongs to the reactive check, so the two can
never disagree about it.

## What `remedy job budget` shows

Read-only. For a job with a money limit it prints the configured limits, the
spend, what remains, the next task's expected cost with its `estimate_basis` and
one-line arithmetic, and — if a predictive stop already happened — the recorded
arithmetic that justified it. `--json` adds `prediction` (the live estimate, or
`null`) and `recorded_prediction` (the persisted one, or `null`) alongside
`limits`, `counters` and `evaluation`. The estimate is computed live and purely:
the command writes nothing, persists nothing and mutates no job, and any failure
in the estimate degrades to a single `unavailable (...)` line rather than
failing the inspection.

## Deliberately not built

Calibration of expected cost from run history, per-task-class caps and burn-rate
anomaly detection are out of scope for F104 and exist nowhere in the code.

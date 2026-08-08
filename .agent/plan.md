# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round. Open
findings: 1 (R-0221, Low, carried, not F104's to fix); R-0222/R-0223/R-0224
are Done. Next free ID: R-0225.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R5 — T003: display and docs. Every user-facing predicted number carries its
`estimate_basis` label, pinned by a grep-style test; `remedy job budget` shows
spent, remaining and the next-task expectation with that label. R4 is committed
and pushed, awaiting the reviewer's verdict.

## Blocker found in R4 — reported, NOT fixed (outside R4's change set)
`run_manifest._BUDGET_ALLOWED_KEYS` is a CLOSED schema that F104 T001 never
extended, so ANY job carrying `max_cost_usd` fails its F012 manifest write:
`manifest.budgets has unknown keys: ['max_cost_usd']`. On the STOP path that
raises `StopFinalizationError` inside `_stop_job` after the stop reason and
source are set but BEFORE the JOB_STOPPED checkpoint, leaving the job RUNNING
with no manifest. It reproduces with the predictive path fully inert, so it is
a T001/R1 defect. Every other acceptance assertion is pinned; the terminal-state
one is an `xfail(strict=True)` that self-clears when the allowlist is fixed.

## Next Steps
- Reviewer: verdict on R4 + a ruling on the blocker (own round, or into R5).
- R6 — integration gate per docs/agents/integration_gate.md; R7/R8 — closure
  per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every figure keeps the None.
- Predictions come from documented class defaults, not calibration.
  `estimate_basis=class_default` is an acceptance criterion, not polish.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- R-0221 costs the integration gate seven phantom base-only failures: attribute
  them, do not chase them.
- No ist-doc under `docs/` describes the job-budget stop path or its reasons,
  so `predicted_budget_exhausted:<limit>` lives only in the feature file and
  the code. R5 decides whether one is owed.

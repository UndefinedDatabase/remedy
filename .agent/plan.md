# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 — the F103 closure — was merged at the Open PR Gate. Build mode:
one-session self-drive (docs/agents/self_drive_protocol.md), one delegated
worker per round. Open findings: 4 — R-0221 (Low, carried, not F104's to fix),
R-0222 (Medium, done in R2), R-0223 (Low, done in R2), R-0224 (Medium, done in
R3). Next free ID: R-0225.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R4 — T002 part 2: derive the band at the dispatch safe point per DECISION F104
D3/D6, wire `predict_next_task_cost` in BEFORE the next task is dispatched (as
of this round `run_job`'s `_stop_check` is its production caller), add the
`predicted_budget_exhausted:<limit>` stop reason and the persisted arithmetic,
and both acceptance fixtures — just-under, and prediction-wrong proving the
reactive backstop still fires. Block saved at `.agent/last_block.md`.

## Blocker found in R4 (reported, NOT fixed — outside this change set)
`run_manifest._BUDGET_ALLOWED_KEYS` is a CLOSED schema that F104 T001 never
extended, so ANY job carrying `max_cost_usd` fails its F012 manifest write:
`manifest.budgets has unknown keys: ['max_cost_usd']`. On the STOP path that
raises `StopFinalizationError` inside `_stop_job` after the stop reason/source
are set but before the JOB_STOPPED checkpoint, leaving the job RUNNING. It
reproduces with the predictive path fully inert, so it is a T001/R1 defect.
Every other acceptance assertion is pinned; the terminal-state one is an
`xfail(strict=True)` that self-clears when the allowlist is fixed.

## Next Steps
- Reviewer decision needed on the blocker above before F104 can close.
- R5 — T003: display and docs; every user-facing predicted number carries its
  `estimate_basis` label, pinned by a grep-style test.
- R6 — integration gate per docs/agents/integration_gate.md; R7/R8 — closure
  per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every figure keeps the None.
- Predictions come from documented class defaults, not calibration.
  `estimate_basis=class_default` is an acceptance criterion, not polish.
- R-0221 costs the integration gate seven phantom base-only failures: attribute
  them, do not chase them.
- The live ledger read happens inside a stop check, the most safety-critical
  code in the job loop; it is guarded and skipped when no cost limit is set.
- `BudgetCounters` is a SHARED F018 model that F104 extends. R3 changed its
  validation, so every construction site is in blast radius; the survey is in
  the R3 handback and must be redone if a later round touches the model again.

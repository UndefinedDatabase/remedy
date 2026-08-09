# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round. Open
findings: 3 (R-0221 Low carried, not F104's to fix; R-0225 High and R-0226
Medium, registered here at the head of R5 — repairing them IS R5);
R-0222/R-0223/R-0224 are Done. Next free ID: R-0227.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R5 — REPAIR (R4 passed review with R-0225/R-0226 registered). DECISION F104 D7:
T003 slips a round rather than polishing a stop path that cannot finalize.
R5 admits `max_cost_usd` to the CLOSED F012 manifest budget schema
(`run_manifest._BUDGET_ALLOWED_KEYS`) with its own strictly-positive finite
validation, pins that schema change, and replaces the terminal-state xfail with
real `JOB_STOPPED` assertions on BOTH the predictive and the reactive cost stop.

## Next Steps
- R6 — T003: display, docs and estimate labels; every user-facing predicted
  number carries its `estimate_basis`, pinned by a grep-style test.
- R7 — integration gate per docs/agents/integration_gate.md.
- R8 — closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every figure keeps the None.
- Predictions come from documented class defaults, not calibration.
  `estimate_basis=class_default` is an acceptance criterion, not polish.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- R-0221 costs the integration gate seven phantom base-only failures: attribute
  them, do not chase them.
- The manifest budget schema is SHARED F012 surface: widening it by one field
  has a blast radius, so the run-manifest gate runs on every R5 commit.
- No ist-doc under `docs/` describes the job-budget stop path or its reasons,
  so `predicted_budget_exhausted:<limit>` lives only in the feature file and
  the code. R6 decides whether one is owed.

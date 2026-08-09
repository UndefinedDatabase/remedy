# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round. Open
findings: 1 (R-0221, Low, carried, not F104's to fix). R-0225 and R-0226 were
registered at the head of R5 and repaired in it, but only the reviewer's own
text sets Resolved, so they stay OPEN in `.agent/live_review.md` until the R5
verdict. R-0222/R-0223/R-0224 are Done. Next free ID: R-0227.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R6 — T003: display, docs and estimate labels. Every user-facing predicted number
carries its `estimate_basis` label, pinned by a grep-style test; `remedy job
budget` shows spent, remaining and the next-task expectation with that label.
R6 also decides whether an ist-doc under `docs/` is owed for the job-budget stop
path. R5 (the R-0225/R-0226 repair, DECISION F104 D7) is committed and pushed,
awaiting the reviewer's verdict.

## Next Steps
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
- The manifest budget schema is SHARED F012 surface. R5 widened it by exactly
  one field; any further budget field owes the same run-manifest gate
  (tests/orchestration/test_run_manifest*.py) before it is believed.
- No ist-doc under `docs/` describes the job-budget stop path or its reasons,
  so `predicted_budget_exhausted:<limit>` lives only in the feature file and
  the code.

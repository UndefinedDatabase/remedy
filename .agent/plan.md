# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 was merged at the Open PR Gate. Build mode: one-session self-drive
(docs/agents/self_drive_protocol.md), one delegated worker per round.
Reviewed through R5: **R4 PASS at f9309bfe**, **R5 PASS at 549f2bac**
(`LAST_REVIEWED_SHA = 549f2bac`). R-0222, R-0223, R-0224, R-0225 and R-0226 are
Done with reviewer-authored resolution text. Open findings: 1 — R-0221 (Low,
carried, not F104's to fix, routed to the F252 flake-debt class). Next free ID:
R-0227.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check is unchanged — prediction never replaces the backstop.

## Current Step
R6 — T003 COMPLETE, awaiting review. `remedy job budget` now prints
`max_cost_usd`, spent, remaining, the live next-task expectation with its
`estimate_basis` label and arithmetic, and any recorded stop prediction; `--json`
gained `prediction` and `recorded_prediction`. The next-task selection rule was
extracted to `select_next_predictable_task` and pinned against the live safe
point. The basis label is pinned grep-style at the engine and at the surface.
DECISION F104 D8 settled the open docs question: the ist-doc
`docs/system/job-budget-enforcement-v0.md` landed and is registered in
`docs/README.md`. T001 and T002 remain complete and reviewed.

## Next Steps
- R7 — integration gate per docs/agents/integration_gate.md.
- R8 — closure per docs/roadmap/STATUS_closure_protocol.md.
  `docs/roadmap/STATUS.md` still carries F104 as `[~]`, which is correct.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every figure keeps the None.
- The band estimate is a FLOOR (DECISION F104 D6): it can only under-predict,
  which is why the reactive backstop must stay exactly as it is.
- R-0221 costs the integration gate seven phantom base-only failures: attribute
  them, do not chase them.
- R6 taught the READ side of `remedy job budget` to query the F103 ledger, which
  the persisted actuals record cannot carry. It is a read-only `query_cost` that
  never creates a ledger, and it is swallowed — but it is new I/O in a command
  the catalog marks `read_only`, so the integration gate should see it.
- The manifest budget schema is SHARED F012 surface. R5 widened it by exactly
  one field; any further budget field owes the same run-manifest gate
  (tests/orchestration/test_run_manifest*.py) before it is believed.

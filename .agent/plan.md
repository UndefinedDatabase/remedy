# Plan — evidence-based test audit and suite optimization (operator order 2026-10-17)

## Goal
Less redundant test work with equally strong protection of real behavior. PR 352, worktree
`.remedy-wt/test-audit`; outside the roadmap queue (F078 stays next); `.agent/STOP` and the
supervisor untouched.

## Current Step
6. Merge gate: main (through PR 359) merged into the branch without force-push; the combined
tree gets the full local suite once, then PR 352 is merged if green (order 2026-10-17
"Execution Excellence", section 11).

Done: 1 audit, 2 ledger (`.agent/test_audit_1017_ledger.md`), 3 batch 1 (test_job_task_runner,
217 to 191 tests, coverage and mutations held; one shadowed duplicate), 4 change-aware fast lane,
5 targeted measurements (ledger sections 6 and 7).

## Next Steps
- Batch 2 candidate (separate PR): the continuation-config family (ledger section 5, lane 3).

## Risks
- Consolidated keepers trade per-test failure names for one test per scenario; each keeper names
  its contract and a mutation shows it goes red.

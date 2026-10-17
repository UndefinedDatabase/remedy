# Plan — evidence-based test audit and suite optimization (operator order 2026-10-17)

## Goal
Less redundant test work with equally strong protection of real behavior. Read-only audit first,
then one small, high-confidence batch, then a change-aware fast lane. No predetermined deletion
count; no coverage-chasing tests. Worktree `.remedy-wt/test-audit` from main `2039a6ae7` (PR 349
merged); outside the roadmap queue (F078 stays next); no merge, no deploy, `.agent/STOP` and the
supervisor untouched.

## Current Step
5. Handback and PR (not merged: operator decides).

Done: 1 audit, 2 ledger (`.agent/test_audit_1017_ledger.md`), 3 batch 1 (test_job_task_runner,
217 to 191 tests, coverage and mutations held; one shadowed duplicate), 4 change-aware fast lane
(`scripts/select_changed_tests.py`, the spine plus owner tests; three retired text guards
replaced by a behavior test), 5 targeted measurements (ledger sections 6 and 7).

## Next Steps
- Operator: review the PR; allow one full-suite run for the before/after the order asks for.
- Batch 2 candidate: the continuation-config family (ledger section 5, lane 3).

## Risks
- Consolidated keepers trade per-test failure names for one test per scenario; each keeper names
  its contract and a mutation shows it goes red.
- No full-suite run in this session (operator: collection only), so the whole-suite before/after
  comes from the load record, not from a fresh run.

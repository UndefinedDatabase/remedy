# Plan — evidence-based test audit and suite optimization (operator order 2026-10-17)

## Goal
Less redundant test work with equally strong protection of real behavior. Read-only audit first,
then one small, high-confidence batch, then a change-aware fast lane. No predetermined deletion
count; no coverage-chasing tests. Worktree `.remedy-wt/test-audit` from main `2039a6ae7` (PR 349
merged); outside the roadmap queue (F078 stays next); no merge, no deploy, `.agent/STOP` and the
supervisor untouched.

## Current Step
3. First batch: `tests/orchestration/test_job_task_runner.py`, the completion-gate and
   target-guard replay family (owner `packages/orchestration/pingpong_job.py`). Delete verbatim
   duplicates; fold same-scenario run_job replays into one keeper per scenario carrying every
   distinct assertion; negative controls by mutating the owner, restored byte for byte.

Done: 1 audit (numbers, cost, gates), 2 evidence ledger (`.agent/test_audit_1017_ledger.md`).

## Next Steps
4. Change-aware fast lane: `scripts/remedy_test_fast.sh` selects the owner tests of the changed
   modules (static import index) plus the contract guards, instead of three fixed files; its
   source-grep guards become a behavior test of the selection. Full suite stays mandatory at the
   gates that already require it.
5. Measure (targeted before/after; full suite only when the operator allows it), handback, PR.

## Risks
- Consolidated keepers trade per-test failure names for one test per scenario; each keeper names
  its contract and a mutation shows it goes red.
- No full-suite run in this session (operator: collection only), so the whole-suite before/after
  comes from the load record, not from a fresh run.

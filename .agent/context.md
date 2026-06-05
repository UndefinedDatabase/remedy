# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 610-624: Job Task Materialization, Runtime CLI Truth, Backend Build Readiness.
UI/design work is PAUSED.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## What Is Done
- 7 propose CLI handlers (list/show/evaluate/approve/reject/defer/materialize)
- Real audit events via RunLogWriter (no dormant None writers)
- fcntl.flock on all write operations
- Call-time data root (no import-time _STORE_DIR dependency)
- Centralized finalized gate via can_finalize()
- ProposedTask has materialized_task_id / materialized_at
- Dashboard v2 with materialization counts and summaries

## Current Risks
1. `do_materialize()` marks ProposedTask.materialized_task_id but does NOT append a Task to Job.tasks or save_job()
2. `storage.py` uses import-time `_DATA_DIR = jobs_dir()` — same issue proposed_tasks had
3. Mutating propose commands can operate without verifying real Job exists
4. No subprocess CLI tests through `python -m apps.cli.grouped`
5. `can_finalize()` does not check approved_not_materialized
6. No reconciliation for materialization mismatch
7. No backend readiness or overnight readiness gate

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).

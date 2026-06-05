# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 595-609: Backend Reliability Closure — audit trail, store locking, materialization truth.
UI/design work is PAUSED. Backend stability is priority.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## What Is Done (Steps 580-594)
- 6 propose CLI handlers wired and tested
- root= param on all store functions
- Atomic writes (tempfile + os.replace)
- ProposedTaskStoreError on corrupt JSON
- Worker queue gate passes data_dir, corrupt blocks
- Finalized gate blocks on degraded
- accept_recommendation creates ProposedTask (not Task)
- Dashboard: degraded, blocking_finalized, blocking_build

## Current Risks (Steps 595-609 targets)
1. CLI audit events dormant — `emit_proposed_task_event(None, ...)` in all CLI handlers
2. No file locking — atomic replace prevents partial files, not lost read-modify-write
3. `_STORE_DIR` still resolved at import time (legacy global)
4. Dashboard finalized logic duplicates can_finalize() inline
5. Materialization: `materialize_approved_task()` exists but no persistence of materialized state
6. No `propose materialize` command
7. Queue gate doesn't distinguish approved-not-materialized from approved-materialized

## Key Patterns
- Event ledger: `run_log.py` RunLogWriter(job_id: UUID, runs_root=) → `.data/runs/<job_id>/<run_id>.jsonl`
- CLI handlers: `apps/cli/commands/<group>.py` with `COMMAND_HANDLERS` dict
- Handler collection: `apps/cli/commands/__init__.py` `collect_all_handlers()`

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).

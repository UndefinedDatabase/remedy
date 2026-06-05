# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 580-594: Proposed Task Backend Closure, CLI Truth, Storage Stability.
UI/design work is PAUSED. Backend stability is priority.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## Current Focus
Make proposed tasks a reliable backend feature:
- CLI handlers for all 6 propose commands (catalog advertises them, no handlers exist)
- Data-dir correct storage (no module-level global)
- Atomic writes + file locking
- Corrupt store handling (degraded, not empty)
- Transition hardening
- Audit events from CLI transitions
- Worker queue gate uses correct data_dir
- Approved tasks: explicit materialization or non-materialized status
- Finalized gate centralized
- Reviewer/rework integration guard
- Dashboard proposed task contract
- End-to-end flow test

## Known Blockers
- `propose.list` etc in catalog but `apps/cli/commands/propose_cmd.py` missing
- `_STORE_DIR` resolved at import time — tests monkeypatch, but callers don't pass data_dir
- `worker_queue._has_unresolved_proposals` doesn't pass data_dir
- `load_proposed_tasks` returns [] on corrupt JSON — hides blocking tasks
- Approved tasks have no materialization path

## Key Patterns
- Job persistence: `storage.py` save_job/load_job → `.data/jobs/{job_id}.json`
- Event ledger: `run_log.py` RunLogWriter → `.data/runs/<job_id>/<run_id>.jsonl`
- CLI commands: `command_catalog.py` CATALOG tuple + GROUPS dict
- CLI handlers: `apps/cli/commands/<group>.py` with `COMMAND_HANDLERS` dict
- Handler collection: `apps/cli/commands/__init__.py` `collect_all_handlers()`

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).

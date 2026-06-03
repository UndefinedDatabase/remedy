# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 435-449: Background worker v1 — complete.

## Completed
- Job lifecycle: 11 states (queued → claimed → running → completed/failed/blocked/etc.)
- Local queue: file-based, deterministic order, paused/cancelled skipped
- Worker lock: lease-based, stale detection after timeout
- Run once: `remedy worker run --once` with provider selection
- Bounded loop: max_jobs, max_seconds, idle_timeout
- Heartbeat/status: file-based, safe export
- Pause/cancel: CLI-only, no browser mutation
- Approval-aware stop: waiting_for_approval state, next command output
- Stale recovery: expired lease → stale → reclaimable
- CLI: worker.run, worker.status, job.enqueue, job.pause, job.cancel in catalog
- Dashboard: worker section (read-only)
- Docs: docs/worker.md with states, commands, safety rules

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Always use scripts/remedy_pytest.sh for pytest execution
- Worker processes one job at a time
- Worker tests use one-shot mode, no unbounded loops

## Constraints
- UI remains read-only (no start/pause/cancel buttons)
- No overnight autonomy
- No browser mutation endpoints
- source_apply requires permission + approved intent

## Recommended Next Block
Steps 450-459 — Real Ollama Trial Round And Prompt Selection

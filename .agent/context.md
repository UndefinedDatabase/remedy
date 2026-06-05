# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 625-639: Modular Task Execution, Worker Executes Real Materialized Tasks.
UI/design work is PAUSED.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## What Is Done
- Proposed task full lifecycle: propose → evaluate → approve → materialize → real Job.tasks
- do_materialize loads Job, creates Task, appends, saves — verified by subprocess tests
- Job storage: root= param, atomic writes, JobStoreError
- Mutating CLI handlers require real Job via _require_job
- can_finalize blocks: unresolved, approved_not_materialized, degraded
- Reconciliation, backend_readiness, overnight_readiness helpers
- 7 propose CLI handlers + propose.materialize command
- fcntl.flock on all proposal store write operations
- Audit events link proposed_task_id and materialized_task_id

## Readiness Terms
- **Storage health**: files readable, stores consistent, no corrupt JSON
- **Build readiness**: real pending work exists in Job.tasks and can be safely executed
- **Finalize readiness**: no pending/blocked tasks, no unresolved proposals, no approved_not_materialized
- **Overnight readiness**: stricter gate; not implemented — always returns not ready

## Current Risks
1. Runtime CLI E2E test can hang (shared UUID, lock contention)
2. backend_readiness mixes storage health with build readiness
3. Worker does not execute materialized Job.tasks through modular path
4. No task execution port/interface — provider logic hardcoded in worker_queue
5. No fixture executor for real Job.tasks
6. No budget gate for worker execution

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).

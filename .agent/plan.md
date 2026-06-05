# Plan — Steps 640-654: Backend Basis Completion

## Goal
Close the loop: materialize → worker executes → persists → events → readiness.

## Current Step
654 — Final baseline

## Steps
- [x] 640: Handoff — "basis complete" defined, agent files
- [x] 641: Runtime CLI stabilized (timeout marker, unique UUIDs)
- [x] 642: Fixed can_retry_task var bug, BudgetGate enforces tokens/runtime
- [x] 643: list_jobs_safe with corruption visibility
- [x] 644: Worker wired to task_execution port (_run_via_task_execution)
- [x] 645: Worker executes exactly one task per --once, re-queues if remaining
- [x] 646: Execution persists: Task.status=COMPLETED, execution_summary, artifact_ids
- [x] 647: Events: task_execution_completed written via RunLogWriter
- [x] 648: Queue gate blocks approved_not_materialized
- [x] 649: Finalize gate reflects executed task state
- [x] 650: Readiness v2 already includes execution health (from 627)
- [x] 651: BudgetGate enforces max_tokens + max_runtime_seconds
- [x] 652: Full backend E2E test: propose → evaluate → approve → materialize → worker → completed → finalize
- [x] 653: Modular guards: worker imports task_execution, not providers; legacy autorun isolated
- [x] 654: Full baseline: 4406 passed, 0 failed, 8 skipped

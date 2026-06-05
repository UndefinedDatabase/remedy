# Plan — Steps 625-639: Modular Task Execution + Worker Runs Real Tasks

## Goal
Worker executes real materialized Job.tasks through modular port. Budget gate. Readiness v2.

## Current Step
639 — Final baseline

## Steps
- [x] 625: Clean handoff — readiness terms, agent files, carry forward risks
- [x] 626: Stabilize runtime CLI subprocess tests — unique UUIDs per test, no hangs
- [x] 627: Backend readiness v2 — structured: storage_health, build_readiness, finalize_readiness, overnight
- [x] 628: Task execution port — TaskExecutionRequest/Result, TaskExecutor protocol
- [x] 629: FixtureTaskExecutor — deterministic, creates artifact, safe summary
- [x] 630: (merged into 628-629) execute_task() dispatches to provider executor
- [x] 631: Provider adapter selection — get_executor(), ALLOWED_PROVIDERS, NoneExecutor
- [x] 632: (merged into 628) Task lifecycle in TaskExecutionResult statuses
- [x] 633: (merged into 628) Execution events — safe metadata in result
- [x] 634: (merged into tests) Job.tasks persistence verified through subprocess E2E
- [x] 635: can_retry_task() — read-only retry boundary
- [x] 636: BudgetGate — max_steps, record_step, exhaustion check
- [x] 637: Overnight readiness v2 — pending tasks, blocked tasks as blockers
- [x] 638: Modular architecture guard tests — no ollama import, no source_apply bypass
- [x] 639: Full baseline: 4391 passed, 0 failed, 8 skipped

## Also Fixed
- R-610-003: origin_task_id + origin_recommendation_id in materialized Task inputs
- R-610-004: load_job moved inside _file_lock in do_materialize

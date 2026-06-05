# Plan — Steps 655-669: Backend Basis Final Closure

## Goal
Close basis: runtime stability, budget enforcement, start/end events, worker CLI E2E.

## Current Step
669 — Final baseline

## Steps
- [x] 655: Handoff — component status, risks, plan
- [x] 656: Runtime CLI hardened (bounded event read, assertion messages)
- [x] 657: Worker CLI subprocess E2E — 5 tests (fixture run, no-pending, none, events, full loop)
- [x] 658: WorkerResult v2 — task_id, artifact_ids, provider, work_performed, task_status, budget_status
- [x] 659: BudgetGate in worker — max_steps/tokens/runtime checked before execution
- [x] 660: task_execution_started event emitted before executor call
- [x] 661: Narrow exceptions — JobNotFoundError and JobStoreError caught separately
- [x] 662: Blocked fixture → FAILED + blocked_reason persisted + event written
- [x] 663: (tested in 640-654) Queue re-queues after partial multi-task
- [x] 664: (tested) Finalize/readiness with blocked tasks
- [x] 665: list_jobs_safe exists, list_jobs delegates (readiness uses load_job_safe per-job)
- [x] 666: Full backend loop via worker CLI subprocess (propose→eval→approve→mat→enqueue→worker→completed)
- [x] 667: Baukasten v2 — 10 guard tests: no provider imports, no source_apply, no circular deps, autorun isolated
- [x] 668: Component status table in context.md
- [x] 669: Full baseline: 4427 passed, 0 failed, 8 skipped

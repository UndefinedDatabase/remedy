# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 640-654: Backend Basis Completion — Worker Executes Real Job Tasks.
UI/design work is PAUSED.

## Canonical Review File
`.agent/live_review.md` — NOT `.data/live_review.md`

## "Basis Complete" Means
1. Propose CLI runtime stable (no hangs)
2. Approved proposal materializes into real Job.tasks
3. Worker executes one real pending Job task through task_execution port
4. Execution result persists after reload
5. Events/audit prove execution
6. Readiness/finalize gates reflect task status
7. No fake completion
8. No provider-specific core imports
9. No background or long-lived test processes

## Current Risks
1. Runtime CLI full-file run can hang (10/11 then stall)
2. Worker not wired to task_execution port — still uses old autorun path
3. BudgetGate max_tokens/max_runtime_seconds not enforced
4. can_retry_task uses loop var `t` instead of `task` on line 210
5. list_jobs silently skips corrupt files
6. Queue gate doesn't block approved_not_materialized

## Resource Safety
All pytest runs use scripts/remedy_pytest.sh (flock + timeout).

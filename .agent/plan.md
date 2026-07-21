# Plan — F018 Budgets & Stop Conditions — T001–T002

## Goal
Persisted job budgets + actual-only budget evaluation. No stop integration
(T003/T004 deferred). One clean F018 branch + one canonical READY_FOR_REVIEW ZIP.

## Scope 1 — F018 T001: persisted budget model, config, flags, precedence
- `JobBudgets` Pydantic model on Job (closed, extra="forbid", model_validator)
- Fields: max_total_tokens, max_provider_calls, max_wall_clock_minutes, deadline
- Central config keys: budget.max_total_tokens, budget.max_provider_calls,
  budget.max_wall_clock_minutes, budget.deadline
- CLI flags: --max-total-tokens, --max-provider-calls, --max-wall-clock-minutes, --deadline
- Precedence: CLI > project config > no limit
- RunManifest snapshot includes resolved budgets
- Validation: strictly positive finite integers, aware UTC deadline, extra="forbid"
- Tests: test_job_budgets.py

## Scope 2 — F018 T002: actual-only budget evaluation
- `budget_guard.py`: BudgetCounters, BudgetEvaluation, evaluate_budget()
- Actuals source: F003 token_actuals.UsageActuals (measured tokens)
- Provider calls: recorded call count from run_manifest FinalizedCall
- Partial/unmeasured: ">= N tokens (M calls unmeasured)"
- Injected clock for wall-time/deadline
- Deterministic first-exhausted precedence
- No writes, no stop, no side effects
- Tests: test_budget_guard.py

## Scope 3 — T003 seam discovery + docs + Evidence + package
- Safe-point seams documented (no integration)
- Decision-queue entry documented (no implementation)
- Postmortem class BUDGET_EXHAUSTED already exists
- docs, STATUS, agent state updated
- Evidence + canonical ZIP

## RunContract overlap decision
RunContract.check_budget is an INTERNAL execution-contract checker.
F018 JobBudgets is the USER-FACING budget model (persisted on Job, set via CLI/config).
Adapter: F018 evaluate_budget reads JobBudgets from the Job; it does NOT duplicate
RunContract.check_budget. RunContract remains the internal execution boundary
for max_loops, max_test_runs, max_runtime_seconds, max_cost_cents.
F018 adds the user-facing job-level budgets as a SEPARATE, non-overlapping concern.
There is NO overlap because the field names differ and the evaluation surfaces differ.

## Current Step
Scope 1: implementing JobBudgets model.

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge F018.
F017 [x]. F018 [~]. F146 [ ].

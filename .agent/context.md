# Context — F018 Budgets & Stop Conditions (Steps 1-10 Reproduction Closure)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `720d97290601709fd988d784c638ffe151fc405c`

## Current state
Steps 1-10 reproduction closure round. All source fixes, test updates, and
runtime gate redesign complete. 258 F018 tests + 649 related tests passing.
Evidence + ZIP pending.

## 10 reproduction closures
1. Clean branch: 14 cherry-picked commits, no Evidence blobs in git
2. Strict budget decode: model_validate failure blocks as corrupt_budget_state
3. Strict resumed actuals: reject bool/float/string/negative coercion
4. BudgetCounters invariants: closed sources, measured tokens↔calls, tz-aware
5. JobPlan Decision Queue: getattr fallback for .metadata/.artifacts
6. Stopped job override: CLI exit 2 + Decision workflow required
7. Real runtime gate: test_execution_binding checks replace name-existence
8. Verification authority: all suites green with production-level assertions
9. Doc updates: T0_F018.md, STATUS.md, context, plan, live_review
10. Final sequencing: commit → evidence → ZIP → verify → stop

## Files changed (this round)
- packages/orchestration/pingpong_job.py (strict budgets + actuals)
- packages/orchestration/budget_guard.py (BudgetCounters invariants)
- packages/orchestration/decision_queue.py (JobPlan compatibility)
- packages/orchestration/runtime_integration_gate.py (execution bindings)
- packages/orchestration/job_evidence.py (enhanced runner + gate ordering)
- apps/cli/commands/do_cmd.py (stopped job override block)
- tests/orchestration/test_f018_authority_integration.py (+22 new tests)
- tests/orchestration/test_budget_guard.py (actual_sources fixes)
- tests/orchestration/test_job_budgets.py (actual_sources fixes)
- tests/orchestration/test_budget_stop_integration.py (actual_sources fixes)
- tests/orchestration/test_runtime_integration_gate.py (rewritten)

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push/PR/merge/modify main
- F018 [~], F146 [ ]

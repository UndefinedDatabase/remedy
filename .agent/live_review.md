# Live Review — F018 Budgets & Stop Conditions

## Status
**BUILT + REPAIRED + 10 REPRODUCTION FINDINGS CLOSED** — All blocking reproductions
from external review of remedy-review-20260721-235837-READY_FOR_REVIEW.zip are closed.
Steps 1-10 scope-based closure complete.

Module:  `packages/orchestration/budget_guard.py` — pure deterministic evaluation
Model:   `packages/core/models.py` — JobBudgets (closed, extra="forbid", StrictInt)
Config:  `packages/orchestration/config.py` — budget.* keys (fail-closed on unknown)
Resolve: `packages/orchestration/budget_resolution.py` — CLI/env/TOML precedence
Safe:    `packages/orchestration/safe_points.py` — unified should_stop predicate
Runner:  `packages/orchestration/pingpong_job.py` — wall-clock continuity, deterministic stop id
Loop:    `packages/orchestration/pingpong_loop.py` — pre-retry budget check
Stop:    `packages/orchestration/stop_reasons.py` — StopReason derivation
Post:    `packages/orchestration/failure_postmortem.py` — budget_exhausted FailureClass
Decision:`packages/orchestration/decision_queue.py` — budget stop event detection (JobPlan safe)
Manifest:`packages/orchestration/run_manifest.py` — budgets in logical_input_projection
Contract:`packages/orchestration/run_contract.py` — inherits from JobBudgets
CLI:     `apps/cli/commands/job.py` — remedy job budget (honest: never invents zeros)
         `apps/cli/commands/do_cmd.py` — budget-aware stop_check + stopped-job guard
Gate:    `packages/orchestration/runtime_integration_gate.py` — 15 source checks + 4 execution bindings

## 10 reproduction findings — ALL CLOSED
1. Clean branch: cherry-picked 14 legitimate commits, excluded Evidence blobs
2. Strict budget decode: model_validate failure → corrupt_budget_state block
3. Strict resumed actuals: reject bool/float/string/negative (no int() coercion)
4. BudgetCounters invariants: closed source vocab, measured tokens↔calls, tz-aware
5. JobPlan Decision Queue: getattr fallback for .metadata/.artifacts
6. Stopped job override: CLI exit 2 + Decision workflow message
7. Real runtime gate: test_execution_binding checks replace name-existence checks
8. Verification authority: all suites pass with production-level assertions
9. Doc updates: T0_F018.md, STATUS.md, context, plan, live_review current
10. Final sequencing: commit → evidence → ZIP → verify → stop

## Test suites (Steps 1-10 round)
- `test_f018_authority_integration.py` — 77 passed (22 new + 55 existing)
- `test_budget_guard.py` — 52 passed
- `test_job_budgets.py` — 76 passed
- `test_budget_stop_integration.py` — 39 passed
- `test_runtime_integration_gate.py` — 14 passed (rewritten for execution bindings)
- `test_safe_points.py` — 78 passed
- `test_config.py` — 57 passed
- `test_failure_postmortem.py` — 112 passed
- `test_run_contract.py` — 88 passed
- `test_run_manifest.py` — 44 passed
- `test_stop_reasons.py` — 10 passed
- `test_do_job_flow.py` — 178 passed
- Review gate suites — 82 passed

## Next
Evidence + full review ZIP. F018 stays `[~]`.

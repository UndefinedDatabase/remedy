# Live Review — F018 Budgets & Stop Conditions

## Status
**BUILT + REPAIRED + REPRODUCTION ROUND CLOSED** — All 9 reproduction findings from
external review of remedy-review-20260721-195820-READY_FOR_REVIEW.zip are closed.

Module:  `packages/orchestration/budget_guard.py` — pure deterministic evaluation
Model:   `packages/core/models.py` — JobBudgets (closed, extra="forbid", StrictInt)
Config:  `packages/orchestration/config.py` — budget.* keys (fail-closed on unknown)
Resolve: `packages/orchestration/budget_resolution.py` — CLI/env/TOML precedence
Safe:    `packages/orchestration/safe_points.py` — unified should_stop predicate
Runner:  `packages/orchestration/pingpong_job.py` — wall-clock continuity, deterministic stop id
Loop:    `packages/orchestration/pingpong_loop.py` — pre-retry budget check
Stop:    `packages/orchestration/stop_reasons.py` — StopReason derivation
Post:    `packages/orchestration/failure_postmortem.py` — budget_exhausted FailureClass
Decision:`packages/orchestration/decision_queue.py` — budget stop event detection
Manifest:`packages/orchestration/run_manifest.py` — budgets in logical_input_projection
Contract:`packages/orchestration/run_contract.py` — inherits from JobBudgets
CLI:     `apps/cli/commands/job.py` — remedy job budget (honest: never invents zeros)
         `apps/cli/commands/do_cmd.py` — budget-aware stop_check for bare runs
Gate:    `packages/orchestration/runtime_integration_gate.py` — 18 F018 checks + 8 test bindings

## 9 reproduction findings — ALL CLOSED
1. CWD config re-read on resume → _cmd_do_job_run only resolves when flags passed
2. project repo not passed → _cmd_create_job passes project_root
3. Core Job vs JobPlan ID → _cmd_job_budget supports both (found_as field)
4. list_decisions can't consume JobPlan → getattr fallback for .job_id/.id
5. resume resets counters → seeds from persisted budget_actuals
6. Actuals coercion → bool/float/string rejected with BudgetCounterError
7. pre-work stop identity instability → episode allocated before _stop_check
8. RunManifest non-canonical budgets → UTC normalization, empty→null
9. source-substring-only gate → 8 real test bindings added

## Test suites
- `test_f018_authority_integration.py` — 55 passed (real production tests, zero inspect)
- `test_budget_guard.py` — 52+ passed
- `test_job_budgets.py` — 76+ passed
- `test_safe_points.py` — 78+ passed
- `test_budget_stop_integration.py` — 39 passed
- `test_config.py` — 57 passed
- `test_failure_postmortem.py` — 112 passed
- `test_run_contract.py` — 88 passed
- `test_run_manifest.py` — 44 passed
- `test_stop_reasons.py` — 10 passed

## Next
Pending Evidence + full review ZIP. F018 stays `[~]`.

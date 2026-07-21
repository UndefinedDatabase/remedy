# Live Review — F018 Budgets & Stop Conditions

## Status
**BUILT + REPAIRED** — Closes all 13 external review blocking findings.

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

## External review findings — ALL CLOSED
1.  ~~No pre-call budget check before transport retries~~ → stop_check in _call_with_retry
2.  ~~Unknown config keys fail open~~ → BudgetConfigError on unknown budget.* keys
3.  ~~RunManifest loses budget authority~~ → budgets in logical_input_projection + strict decoder
4.  ~~Counter contradictions accepted~~ → BudgetCounters.__post_init__ strict validation
5.  ~~Honest CLI incomplete~~ → no_runs/unavailable status, never evaluates with zero counters
6.  ~~Budget stop has random UUID identity~~ → deterministic sha256-based request_id
7.  ~~JobPlan stop doesn't produce real decision~~ → decision_queue checks stop events + fields
8.  ~~Budget postmortem classified "stopped"~~ → terminal_status="budget_exhausted" for budget stops
9.  ~~Wall-clock resets on every run_job~~ → uses job.created_at for continuity across resumes
10. ~~No CLI path for durable budgets~~ → --max-total-tokens/--max-provider-calls/etc + config
11. ~~RunContract independently evaluates~~ → build_default_run_contract inherits from JobBudgets
12. ~~Evidence churn commits in history~~ → clean branch, evidence-only commits excluded
13. ~~live_review.md describes F017~~ → rewritten for F018

## Test suites
- `test_budget_guard.py` — 52+ passed
- `test_job_budgets.py` — 76+ passed
- `test_safe_points.py` — 78+ passed
- `test_budget_stop_integration.py` — 39 passed
- `test_config.py` — 57 passed
- `test_failure_postmortem.py` — 112 passed
- `test_run_contract.py` — 88 passed
- `test_run_manifest.py` — 44 passed
- `test_stop_reasons.py` — 10 passed
- **Total: 556 passed across 9 suites**

## Next
Pending external acceptance. F018 stays `[~]`.

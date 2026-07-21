# Plan — F018 Budgets & Stop Conditions — Full Rebuild

## Goal
Close all 13 external review blocking findings. Wire budgets end-to-end
from CLI through durable persistence, live intra-task counters, F011
stop integration, and RunManifest identity. Clean branch, fresh Evidence,
one READY_FOR_REVIEW ZIP.

## Finding Fixes Applied
1. Pre-call budget check → stop_check in _call_with_retry (pingpong_loop.py)
2. Fail-closed config → BudgetConfigError on unknown budget.* keys (config.py)
3. RunManifest authority → already wired (budgets in logical_input_projection)
4. Counter validation → already wired (BudgetCounters.__post_init__)
5. Honest CLI → no_runs/unavailable, never evaluates zeros (job.py)
6. Deterministic identity → sha256-based budget stop request_id (pingpong_job.py)
7. Decision queue → checks stop events + fields (decision_queue.py)
8. Budget postmortem → terminal_status="budget_exhausted" (pingpong_job.py)
9. Wall-clock continuity → uses job.created_at across resumes (pingpong_job.py)
10. CLI path → already wired (--max-total-tokens etc + config)
11. RunContract authority → already inherits from JobBudgets
12. Evidence churn → clean branch (reset to 884a8b8)
13. live_review.md → rewritten for F018

## Current Step
Tests + Evidence + ZIP.

## Constraints
No Fable/subagents/providers/network/Docker.
Do not amend/squash. Do not push/PR/merge.
F018 [~]. F146 [ ].

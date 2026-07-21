# Context — F018 Budgets & Stop Conditions (Authority Round — Reproduction Closure)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `720d97290601709fd988d784c638ffe151fc405c`

## Current state
T001–T004 built. 9 external reproduction findings closed.
55 real production tests in test_f018_authority_integration.py (zero inspect).
All source fixes complete. Docs updated. Evidence + ZIP pending.

## 9 reproduction closures
1. CWD config re-read: _cmd_do_job_run only resolves budgets when flags passed
2. project repo not passed: _cmd_create_job passes repo_path
3. Core Job vs JobPlan ID: _cmd_job_budget supports both
4. list_decisions can't consume JobPlan: uses getattr fallback
5. resume resets counters: seeds from persisted budget_actuals
6. Actuals coercion: bool/float/string rejected with BudgetCounterError
7. pre-work stop identity instability: episode allocated before _stop_check
8. RunManifest non-canonical budgets: UTC normalization, empty→null
9. source-substring-only gate: 8 real test bindings added

## Files changed
- apps/cli/commands/do_cmd.py
- apps/cli/commands/job.py
- packages/orchestration/pingpong_job.py
- packages/orchestration/budget_guard.py
- packages/orchestration/decision_queue.py
- packages/orchestration/run_manifest.py
- packages/orchestration/runtime_integration_gate.py
- tests/orchestration/test_f018_authority_integration.py
- docs/roadmap/features/T0_F018.md

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push/PR/merge/modify main
- F018 [~], F146 [ ]

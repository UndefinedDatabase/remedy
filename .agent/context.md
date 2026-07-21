# Context — F018 Budgets & Stop Conditions (Authority Round)

## Branch
`feature/f018-budgets-stop-conditions-clean`
Base commit: `720d97290601709fd988d784c638ffe151fc405c`
HEAD: `48b73a2f57a340601a85576a6bd763caa2dbfe34`

## Current state
T001–T004 built. Authority round: 14 external findings closed.
6 logically scoped commits. 28 new integration tests (195 F018 total pass).
Evidence: job `f018_authority_bb0663f9e99b`.
Package: `remedy-review-20260721-195820-READY_FOR_REVIEW.zip`.

## Key changes (authority round)
- fail-closed TOML parsing for budgets (`BudgetConfigError`)
- `resolve_job_budgets(project_root=)` — not CWD-based
- `_cmd_do_job_plan` + `_cmd_do_job_run` accept 4 budget flags
- `_bind_artifact_refs` preserves budgets
- `build_run_manifest` handles dict budgets
- `_decode_budgets_field` rejects zero/negative/bool/tz-naive
- `collect_counters_from_actuals` validates counter invariants
- `first_running_at` for wall clock (not `created_at`)
- `budget_actuals` persisted at end of task loop
- decision ID from event request_id; actions ("extend", "abandon")
- `_reconcile_budget_fields` in RunContract
- 10 F018-specific runtime integration checks (15 total)

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push, create PR, merge, or modify main
- F018 stays `[~]`, F146 stays `[ ]`

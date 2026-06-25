# Plan — Steps 4706-4723: Scope Plan Approval Gate v0

## Goal
Add human-approved scope planning before executing large task-file prompts.
Deterministic scope extraction, editable scope file, validated decisions,
scope contract in Builder/Reviewer prompts, scope data in reports.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- ScopePlan, ScopeFeature, ScopeRisk, ScopePlanValidationResult data model
- Deterministic Markdown parser (headings + bare label sections)
- Scope plan persistence under data_root/scope_plans/<plan_id>/
- Editable scope file with user_decision per feature
- Scope validation: hash, repo, duplicates, invalid decisions, min 1 approved
- `remedy do plan --task-file ... --repo . --json` CLI command
- `--scope-file` and `--approve-scope` on `remedy do run`
- Builder prompt scope contract (APPROVED/OUT OF SCOPE sections)
- Reviewer prompt scope contract with review rules
- Out-of-scope detection helper (expected_files + diff keyword check)
- Scope data in JSON report (scope_plan field)
- Scope summary in text report (Approved/Denied/Deferred/Backlog/Pending)
- Worker self-report vs Remedy verification separation in text report
- 47 new tests: extraction, persistence, validation, CLI, prompts, detection, reports
- Full suite: 7546 passed, 0 failed
- Fast lane: 571 passed
- Runtime lane: 4/4 suites passed
- Lint: all checks passed (ruff + mypy)

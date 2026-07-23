# Live Review — F146 Project Identity & Repo Autodetection (REPAIR R2)

## Status
**REPAIRED R2** — all 13 new review findings fixed, tests green, ready for Evidence.

## What was fixed (13 R2 reproductions)
1. register_project_repo accepts plain dirs → NotAGitRepoError for non-Git
2. register_project_repo slug from display name → derives from repo dir name
3. save_project accepts null/invalid slugs → _validate_slug (non-null, kebab, unique)
4. No deterministic migration order → migrate_legacy_projects sorted (created_at, UUID)
5. _lookup_by_slug_or_uuid triggers writes → _lookup_by_slug_or_uuid_readonly
6. Unknown selector: no value/source → ProjectNotFoundError includes both
7. select_project flag/env paths can write → fully read-only via _load_project_readonly
8. No shared attach service → attach_repo_canonical (git, ownership, dedup)
9. Legacy attach-repo duplicates logic → delegates to attach_repo_canonical
10. CLI ambiguous error shows traceback → catches AmbiguousProjectError, exit 1
11. Unsafe .git file fallback in worktree → removed, git common-dir only
12. AST guard misses aliased module imports → ast.Import node detection
13. Runtime gate requires all features → feature-aware _select_checks_for_feature

## Module changes
- `packages/orchestration/project_registry.py` — NotAGitRepoError, _validate_slug,
  migrate_legacy_projects, _lookup_by_slug_or_uuid_readonly, attach_repo_canonical,
  selector_value/selector_source diagnostics, attach dedup fix
- `apps/cli/commands/project.py` — canonical attach delegates, typed error handling
- `packages/orchestration/runtime_integration_gate.py` — _select_checks_for_feature,
  feature_id param, 13 F146 static checks, 2 test execution bindings, bindings_override
- `tests/orchestration/test_project_resolution.py` — 83 tests (6 slug validation,
  2 deterministic migration, 2 read-only lookup, 2 selector diagnostics, 6 canonical attach,
  3 feature-aware gate, 2 register non-Git/dir-name)
- `tests/cli/test_project_current.py` — 16 tests, aliased module AST guard
- `docs/roadmap/features/T0_F146.md` — Built State updated

## Test suites (R2)
- test_project_resolution.py — 83 passed
- test_project_current.py — 16 passed
- test_runtime_integration_gate.py — 14 passed
- test_f018_authority_integration.py — passed (regression)
- test_budget_guard.py — passed (regression)
- test_job_budgets.py — passed (regression)
- test_budget_stop_integration.py — passed (regression)

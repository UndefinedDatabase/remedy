# Context — F146 Project Identity & Repo Autodetection (REPAIR R2)

## Branch
`feature/f146-project-identity-repo-autodetection`
Base commit: `d750f65ca42065ee0583f8d0d115f8a591ce6a48`

## Current state
All 13 R2 review reproductions fixed. 83 focused F146 resolution tests +
16 CLI tests + 14 gate tests + 281 F018 regression tests green.
Full compile check + bash syntax + git diff --check clean.

## Changes (R2 repair — 13 new findings)
1. `packages/orchestration/project_registry.py` — strict registration
   (NotAGitRepoError, git root, slug from dir name), slug validation
   (_validate_slug: non-null, kebab-case, unique), deterministic batch
   migration (sorted created_at+UUID), read-only lookup
   (_lookup_by_slug_or_uuid_readonly), canonical attach service
   (attach_repo_canonical: git validate, ownership, dedup), selector
   diagnostics (value+source in ProjectNotFoundError)
2. `apps/cli/commands/project.py` — canonical attach delegates, typed
   error handling, deterministic exit codes
3. `packages/orchestration/runtime_integration_gate.py` — feature-aware
   gate (_select_checks_for_feature, feature_id param), 13 F146 static
   checks, 2 test execution bindings, _bind_test_execution bindings_override
4. `tests/orchestration/test_project_resolution.py` — 83 tests (was 60):
   non-Git rejection, slug-from-dir, slug validation (6), deterministic
   migration (2), read-only lookup proof (2), selector diagnostics (2),
   canonical attach (6), feature-aware gate (3)
5. `tests/cli/test_project_current.py` — 16 tests (was 12), AST guard
   with aliased module detection
6. `docs/roadmap/features/T0_F146.md` — Built State updated for R2

## Remaining
- Commit in logical order
- Generate Evidence and review ZIP
- Produce handoff

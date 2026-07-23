# Context — F146 Project Identity & Repo Autodetection (REPAIR)

## Branch
`feature/f146-project-identity-repo-autodetection`
Base commit: `d750f65ca42065ee0583f8d0d115f8a591ce6a48`

## Current state
All 13 review reproductions fixed. 72 focused F146 tests + 41 regression tests green.
Full compile check + bash syntax + docs consistency clean.

## Changes (repair)
1. `packages/orchestration/project_registry.py` — atomic save, read-only loading,
   AmbiguousProjectError, InvalidProjectSelectorError, RepoOwnershipConflictError,
   register_project_repo, git common-dir worktree validation, source "environment"
2. `apps/cli/commands/project.py` — select_project, --project flag, exact JSON schema,
   git validation, ownership conflicts, attach JSON output, job_count = len(job_ids)
3. `apps/cli/command_catalog.py` — --project on current + attach
4. `packages/orchestration/runtime_integration_gate.py` — 7 F146 static checks,
   2 F146 test execution bindings (14 critical node IDs)
5. `tests/orchestration/test_project_resolution.py` — 60 tests (was 53)
6. `tests/cli/test_project_current.py` — 12 tests (was 5), AST-based guard
7. `docs/roadmap/features/T0_F146.md` — Built State section added

## Remaining
- Commit in logical order (5 commits)
- Generate Evidence and review ZIP
- Produce handoff

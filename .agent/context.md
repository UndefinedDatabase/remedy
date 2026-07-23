# Context — F146 Project Identity & Repo Autodetection (REPAIR R3)

## Branch
`feature/f146-project-identity-repo-autodetection`
Base commit: `d750f65ca42065ee0583f8d0d115f8a591ce6a48`

## Current state
All 4 R3 blocking findings fixed. 189 tests green across 5 suites.
Commits pending, Evidence pending.

## Changes (R3 — 4 blocking findings)
1. `packages/orchestration/project_registry.py` — save_project() auto-derives
   slug when None (canonical_repo_path → repo_paths[0] → project.name)
2. `apps/cli/commands/project.py` — list/show use _list_projects_readonly /
   _load_project_readonly (read-only action-class truth)
3. `packages/orchestration/manual_attestation.py` — feature_id param threaded
   to write_runtime_integration_gate
4. `packages/orchestration/job_evidence.py` — review_feature_id param threaded
   to build_manual_completion_gates
5. `tests/test_project_registry.py` — 5 additive tests (auto-derive, roundtrip,
   unique, byte-proof, readonly-mtime)
6. `tests/orchestration/test_runtime_integration_gate.py` — 3 additive tests
   (F146 excludes F018, write propagation, manual-gates E2E)
7. `tests/orchestration/test_f018_package_pipeline_e2e.py` — verification data
   includes 6 test files, count assertions 19→34
8. `tests/orchestration/test_project_resolution.py` — test_null_slug_auto_derives
9. `docs/roadmap/features/T0_F146.md` — R3 Built State section

## Remaining
- Commit in 5 logical commits
- Generate Evidence with fresh job ID, feature_id=f146
- Package ZIP
- Produce handoff

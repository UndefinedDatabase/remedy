# Live Review — F146 Project Identity & Repo Autodetection (REPAIR R3)

## Status
**R3 COMPLETE** — 4 blocking findings from R2 review fixed, all tests green.

## What was fixed (4 R2 blocking findings → R3 repairs)
1. save_project(slug=None) crashes existing registry tests → auto-derive
   slug from canonical_repo_path dir name / repo_paths[0] dir name / project.name
2. CLI project list/show (action_class="read_only") call write-path functions →
   switched to _list_projects_readonly / _load_project_readonly
3. review_feature_id not threaded to runtime gate → create_manual_completion_bundle
   → build_manual_completion_gates → write_runtime_integration_gate all accept feature_id
4. F018 E2E tests hardcoded count 19 → updated to 34 (28 static + 6 bindings)

## Module changes (R3)
- `packages/orchestration/project_registry.py` — auto-derive slug in save_project()
- `apps/cli/commands/project.py` — readonly functions for list/show
- `packages/orchestration/manual_attestation.py` — feature_id param
- `packages/orchestration/job_evidence.py` — review_feature_id param
- `tests/test_project_registry.py` — 5 additive tests (46 total)
- `tests/orchestration/test_runtime_integration_gate.py` — 3 additive tests (17 total)
- `tests/orchestration/test_f018_package_pipeline_e2e.py` — count + data fixes (26 total)
- `tests/orchestration/test_project_resolution.py` — test_null_slug_auto_derives rename

## Test suites (R3)
- test_project_registry.py — 46 passed
- test_project_resolution.py — 83 passed
- test_project_current.py — 14 passed
- test_runtime_integration_gate.py — 17 passed
- test_f018_package_pipeline_e2e.py — 26 passed
- Total focused: 186 + 3 workspace guard = 189 passed

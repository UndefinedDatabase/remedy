# Live Review — F146 Project Identity & Repo Autodetection (REPAIR R4)

## Status
**R4 COMPLETE** — 8 blocking findings from R3 external review fixed, all tests green.

## What was fixed (8 R3 blocking findings → R4 repairs)
1. Gate loses identity: refresh_review_evidence.py called build_runtime_integration_gate
   without feature_id, replacing F146-scoped gate with global gate → now reads persisted
   feature_id from existing gate and propagates
2. Duplicate slugs in readonly: _load_project_readonly derived slugs per-project
   independently → new _project_set_readonly() allocates across full set deterministically
3. Access-order dependent migration: load_project called per-record _migrate_legacy →
   now calls batch migrate_legacy_projects() first
4. False read_only commands: project.brain/context/summary and readiness.project called
   load_project (write path) → switched to _load_project_readonly
5. Incomplete AST guard: only detected ast.Name, not full attribute chains →
   _resolve_attr_chain resolves full dotted chains, tracks from-import of module
6. Missing registry test binding: tests/test_project_registry.py not bound in gate →
   added f146_test_registry_execution binding (min_passed=40)
7. project.context RunLog event: read_only command emitted RunLog write → removed
8. runtime_integration_gate.json missing feature_id field → gate dict includes
   feature_id when provided

## Module changes (R4)
- `packages/orchestration/project_registry.py` — _project_set_readonly(),
  _load_project_readonly via full-set projection, load_project batch migration
- `apps/cli/commands/project.py` — brain/context/summary use _load_project_readonly,
  context RunLog event removed
- `apps/cli/commands/readiness.py` — readiness.project uses _load_project_readonly
- `packages/orchestration/runtime_integration_gate.py` — feature_id in gate output,
  f146_test_registry_execution binding
- `scripts/refresh_review_evidence.py` — reads/propagates persisted feature_id
- `tests/cli/test_project_current.py` — _resolve_attr_chain, 4 new AST guard tests (18 total)
- `tests/orchestration/test_project_resolution.py` — 12 new R4 tests (93 total)
- `tests/orchestration/test_f018_package_pipeline_e2e.py` — count fixes 34→35, 6→7 bindings (29 total)
- `tests/orchestration/test_f146_package_pipeline_e2e.py` — NEW, 11 tests
- `docs/roadmap/features/T0_F146.md` — R4 Built State section

## Test suites (R4)
- test_project_registry.py — 46 passed
- test_project_resolution.py — 93 passed
- test_project_current.py — 18 passed
- test_runtime_integration_gate.py — 17 passed
- test_f018_package_pipeline_e2e.py — 29 passed
- test_f146_package_pipeline_e2e.py — 11 passed
- test_budget_guard.py — passed
- test_job_budgets.py — passed
- test_budget_stop_integration.py — passed
- test_f018_authority_integration.py — passed
- Total focused: 214 F146 + 281 non-regression = 495 passed

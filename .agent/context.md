# Context — F146 Project Identity & Repo Autodetection (REPAIR R4)

## Branch
`feature/f146-project-identity-repo-autodetection`
Base commit: `d750f65ca42065ee0583f8d0d115f8a591ce6a48`

## Current state
All 8 R4 blocking findings fixed. 495 tests green across 10 suites.
Commits, Evidence, and ZIP pending.

## Changes (R4 — 8 blocking findings)
1. `packages/orchestration/project_registry.py` — _project_set_readonly() deterministic
   read-only projection; _load_project_readonly uses full-set projection;
   load_project calls batch migrate_legacy_projects
2. `apps/cli/commands/project.py` — brain/context/summary use _load_project_readonly;
   context RunLog event removed
3. `apps/cli/commands/readiness.py` — readiness.project uses _load_project_readonly
4. `packages/orchestration/runtime_integration_gate.py` — feature_id in gate output;
   f146_test_registry_execution binding for tests/test_project_registry.py
5. `scripts/refresh_review_evidence.py` — reads/propagates persisted feature_id
6. `tests/cli/test_project_current.py` — _resolve_attr_chain + 4 AST guard tests (18 total)
7. `tests/orchestration/test_project_resolution.py` — 12 R4 tests (93 total)
8. `tests/orchestration/test_f018_package_pipeline_e2e.py` — count fixes (29 total)
9. `tests/orchestration/test_f146_package_pipeline_e2e.py` — NEW (11 tests)
10. `docs/roadmap/features/T0_F146.md` — R4 Built State
11. `.agent/plan.md` — R4 plan
12. `.agent/live_review.md` — R4 status
13. `.agent/context.md` — R4 context

## Remaining
- Commit in logical commits
- Generate Evidence with fresh job ID, feature_id=f146
- Package ZIP
- Produce handoff

# Plan — F146 Project Identity & Repo Autodetection (FINAL CLOSURE R4)

## Goal
Fix 8 blocking findings from R3 external review. Final F146 closure.

## Status: COMMITTING

## T001 — Deterministic read-only Registry projection and one migration authority
- [x] Shared pure read-only projection: _project_set_readonly() loads all, reserves persisted slugs, allocates unique effective slugs in deterministic order, never writes
- [x] Use projection in all read-only APIs: _list_projects_readonly, _load_project_readonly
- [x] load_project migration: run full batch migration first via migrate_legacy_projects()
- [x] Prove: reverse UUID order produces same slugs, readonly/migrate agree, idempotent migration

## T002 — Truthful read-only commands and complete workspace-key guard
- [x] Audit: project.brain, project.context, project.summary, readiness.project use read-only projection
- [x] project.context: remove RunLog write from read-only path
- [x] AST guard: _resolve_attr_chain resolves full ast.Attribute chains, detect all import forms
- [x] Prove: 4 synthetic AST guard tests, no-write byte/mtime proof

## T003 — Persistent review-feature authority, exact F146 Gate, final state and ZIP
- [x] runtime_integration_gate.json contains feature_id field in output dict
- [x] refresh_review_evidence reads persisted feature_id, rebuilds with it
- [x] Add F146 binding for tests/test_project_registry.py (f146_test_registry_execution)
- [x] Create test_f146_package_pipeline_e2e.py (13 tests)
- [x] Update docs, agent state, STATUS
- [ ] Commit, Evidence, ZIP, handoff

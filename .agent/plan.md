# Plan — F146 Project Identity & Repo Autodetection (REPAIR)

## Goal
Repair 13 exact review reproductions while preserving correct existing work.

## Status: COMMITTING — all repair code + tests complete, committing

## T001 — Canonical registry identity, migration and read-only resolution
- [x] AmbiguousProjectError for duplicate slug lookup
- [x] Atomic save (temp file + os.replace)
- [x] Read-only loading path (_load_project_readonly) — no migration writes
- [x] resolve_project/require_project truly read-only (bytes/mtime proof)
- [x] Deterministic legacy migration ordering (created_at then UUID)
- [x] Managed worktree validation via git common-dir (not path component)
- [x] Explicit registration primitive (register_project_repo)
- [x] Same-repo idempotency in registration
- [x] _cmd_create_project assigns slug immediately

## T002 — Strict shared selection + CLI production paths
- [x] Empty whitespace flag/env → InvalidProjectSelectorError (not fallback)
- [x] select_project source values: "flag", "environment", "cwd"
- [x] Duplicate slug → AmbiguousProjectError (not arbitrary selection)
- [x] project current: --project flag, use select_project, exact JSON schema
- [x] project current: job_count = len(project.job_ids)
- [x] project attach: --project flag for selection when cwd fails
- [x] project attach: validate --repo as git root
- [x] project attach: rebind canonical_repo_path + replace old in repo_paths
- [x] project attach: block ownership conflicts (RepoOwnershipConflictError)
- [x] project attach: JSON output
- [x] project attach: same-path idempotent

## T003 — Guard, runtime gate, Evidence, tests, docs
- [x] AST-based workspace-key guard (replace string search)
- [x] Feature-aware Runtime Gate with F146-specific execution bindings
- [x] Replace tests pinning incorrect behavior with required cases
- [x] Update T0_F146.md with Built State
- [x] Update agent state files
- [ ] 5 logical commits
- [ ] Fresh Evidence generation
- [ ] make_review_zip.sh → READY_FOR_REVIEW

## Test counts
- tests/orchestration/test_project_resolution.py — 60 passed
- tests/cli/test_project_current.py — 12 passed
- tests/test_project_registry.py — 41 passed (regression)
- tests/orchestration/test_runtime_integration_gate.py — 14 passed
- tests/docs/test_docs_consistency.py — 292 passed

## Constraints
No providers, no network, no Docker, no subagents.
Do not amend/squash. Do not push/PR/merge/modify main.

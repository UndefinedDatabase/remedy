# Plan — F146 Project Identity & Repo Autodetection (REPAIR R2)

## Goal
Fix 13 exact review reproductions from second external review while preserving all accepted work.

## Status: COMMITTING

## T001 — Strict registration, slug validation, deterministic migration
- [x] register_project_repo requires Git repo (rejects plain dirs with typed error)
- [x] register_project_repo resolves Git root
- [x] register_project_repo derives slug from repo directory name, not display name
- [x] save_project validates slug: non-null, kebab-case, unique
- [x] Deterministic batch migration: sorted (created_at, UUID) before slug allocation
- [x] _lookup_by_slug_or_uuid read-only (no migration writes)
- [x] Unknown selector error includes value and source
- [x] Tests: non-Git rejection, slug-from-repo-dir, slug validation, migration ordering

## T002 — Read-only selector and canonical attach authority
- [x] select_project fully read-only for flag/env/cwd
- [x] CLI catches AmbiguousProjectError (no traceback)
- [x] CLI catches all typed errors with deterministic exit codes
- [x] Unknown selector prints value and source
- [x] Canonical attach service: shared by project.attach and project.attach-repo
- [x] Attach service: git validate, resolve root, ownership check, canonical rebind, deduplicate repo_paths
- [x] Legacy attach-repo delegates to canonical service
- [x] Tests: duplicate slug CLI, unknown selector diagnostics, attach dedup, legacy attach

## T003 — Worktree proof, AST guard, feature-aware gate, final state
- [x] Remove unsafe .git file fallback in _managed_worktree_parent
- [x] AST guard detects aliased module imports (import X as Y; Y.project_id)
- [x] Feature-aware Runtime Gate: F146 Evidence requires only F146 checks
- [x] Update docs, STATUS.md, agent state files
- [ ] Commits, Evidence, ZIP

## Constraints
No providers, no network, no Docker, no subagents.
Do not amend/squash. Do not push/PR/merge/modify main.

# Plan — F146 Project Identity & Repo Autodetection

## Goal
Reconcile the two existing project identity notions. Registry UUID becomes
the canonical project identity. Worktree-derived path value demoted to
workspace key. One shared selection precedence. CLI current/attach/list.

## Status: IMPLEMENTING — all code complete, tests green, committing

## T001 — Canonical registry identity, slug, real path and resolution
- [x] Extend RemyProject with `slug: str | None` and `canonical_repo_path: str | None`
- [x] `slugify(name)` → stable kebab-case; collision suffix: project, project-2, project-3
- [x] `resolve_project(cwd)` — never writes; git root → real path → match registry
- [x] `require_project(cwd)` — resolve or raise ProjectNotFoundError with fix-it
- [x] Legacy migration: derive slug from name, derive canonical_repo_path from repo_paths[0]
- [x] Same-repo registration idempotency (find_project_by_repo)
- [x] Duplicate legacy real-path: newest valid wins, bounded warning
- [x] Managed-worktree parent mapping via `.remedy-wt` detection

## T002 — Shared project-selection precedence
- [x] `select_project(flag, cwd)` → (project, source)
- [x] Flag > REMEDY_PROJECT env > cwd > typed error
- [x] Empty flag/env values invalid
- [x] UUID and slug both supported
- [x] Full precedence matrix test (12 tests)

## T003 — CLI reconciliation, workspace-key guard, docs and Evidence
- [x] `remedy project current` — human + JSON output, exit 3 on unresolved
- [x] `remedy project attach --repo PATH`
- [x] `remedy project list` — add slug column
- [x] Workspace-key docstring reconciliation (worktrees.py + dev_server.py)
- [x] Workspace-key guard test (no forbidden imports)
- [ ] Docs update (STATUS.md, T0_F146.md)
- [ ] Commits
- [ ] Evidence generation

## Test counts
- tests/orchestration/test_project_resolution.py — 53 passed
- tests/cli/test_project_current.py — 5 passed
- tests/test_project_registry.py — 41 passed (regression, 0 new failures)
- Broad regression: 1897 passed, 2 skipped (3 pre-existing failures on main)

## Constraints
No providers, no network, no Docker, no subagents.
Do not amend/squash. Do not push/PR/merge.

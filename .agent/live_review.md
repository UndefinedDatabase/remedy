# Live Review — F146 Project Identity & Repo Autodetection

## Status
**BUILT** — all T001/T002/T003 code complete, 99 focused tests passing,
1897 broad regression passing.

Module:  `packages/orchestration/project_registry.py` — canonical identity
Model:   `RemyProject` — slug + canonical_repo_path fields added
Slug:    `slugify()` — kebab-case, collision suffix (-2, -3, ...)
Migrate: `_migrate_legacy()` — derives slug/canonical_repo_path on first load
Resolve: `resolve_project(cwd)` — git root → real path → registry match
Require: `require_project(cwd)` — resolve or raise with fix-it
Find:    `find_project_by_repo(real_path)` — newest wins on duplicate
Select:  `select_project(flag, cwd)` — flag > env > cwd > error
Worktree:`_managed_worktree_parent()` — .remedy-wt → parent repo mapping
CLI:     `_cmd_project_current` — human + JSON, exit 3 on unresolved
CLI:     `_cmd_project_attach_repo` — re-bind moved repos
CLI:     `_cmd_list_projects` — slug column added
Guard:   `TestWorkspaceKeyGuard` — no forbidden worktrees.project_id imports
Docs:    worktrees.py + dev_server.py docstrings updated

## Test suites
- test_project_resolution.py — 53 passed (T001+T002)
- test_project_current.py — 5 passed (T003)
- test_project_registry.py — 41 passed (regression)
- Broad regression — 1897 passed, 2 skipped, 3 pre-existing failures

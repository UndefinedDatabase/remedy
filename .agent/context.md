# Context — F146 Project Identity & Repo Autodetection

## Branch
`feature/f146-project-identity-repo-autodetection`
Base commit: `d750f65ca42065ee0583f8d0d115f8a591ce6a48`

## Current state
All T001/T002/T003 implementation complete. 99 focused tests passing.
Broad regression clean (1897 passed, 3 pre-existing failures on main).

## Changes
1. `packages/orchestration/project_registry.py` — slug, canonical_repo_path fields;
   slugify(); _migrate_legacy(); resolve_project(); require_project();
   find_project_by_repo(); select_project(); ProjectNotFoundError cwd form
2. `packages/orchestration/worktrees.py` — docstring: workspace key rule
3. `packages/runtimes/dev_server.py` — docstring: workspace key rule
4. `apps/cli/commands/project.py` — _cmd_project_current, _cmd_project_attach_repo,
   list slug column, COMMAND_HANDLERS entries
5. `apps/cli/command_catalog.py` — project.current, project.attach entries
6. `tests/orchestration/test_project_resolution.py` — 53 tests (slug, migration,
   resolve, require, find, select precedence)
7. `tests/cli/test_project_current.py` — 5 tests (current, list slug, guard)

## Remaining
- Update docs/roadmap/STATUS.md and T0_F146.md
- Commit in logical order
- Generate Evidence and review ZIP
- Produce handoff

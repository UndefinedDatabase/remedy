# Live Review — F146 Project Identity & Repo Autodetection (REPAIRED)

## Status
**REPAIRED** — all 13 review findings fixed, tests green, ready for Evidence.

## What was fixed (13 reproductions)
1. resolve_project writes via migration → read-only loading path
2. project current ignores selection → uses select_project + --project flag
3. project current wrong JSON → exact schema (project_id, slug, repo, job_count, selection_source)
4. project attach can't reattach moved repo → --project flag for selection
5. project attach accepts non-git → git-root validation
6. project attach doesn't rebind canonical → full rebind
7. project attach doesn't block ownership → RepoOwnershipConflictError
8. Duplicate slugs arbitrary → AmbiguousProjectError
9. Empty selectors silently ignored → InvalidProjectSelectorError
10. Managed worktree trusts dir name → git common-dir verification
11. New project slug=null → immediate slug assignment
12. Same-repo idempotency missing → register_project_repo
13. Non-atomic writes → temp file + os.replace

## Module changes
- `packages/orchestration/project_registry.py` — read-only loading, atomic save,
  AmbiguousProjectError, InvalidProjectSelectorError, RepoOwnershipConflictError,
  register_project_repo, git common-dir worktree validation, source "environment"
- `apps/cli/commands/project.py` — select_project, --project flag, exact JSON,
  git validation, ownership conflicts, attach JSON output
- `apps/cli/command_catalog.py` — --project on current + attach
- `packages/orchestration/runtime_integration_gate.py` — 7 F146 static checks,
  2 F146 test execution bindings with 14 critical node IDs

## Test suites
- test_project_resolution.py — 60 passed
- test_project_current.py — 12 passed
- test_project_registry.py — 41 passed (regression)
- test_runtime_integration_gate.py — 14 passed
- test_command_catalog.py — passed
- test_worktrees.py — passed
- test_manual_completion_bundle.py — passed
- test_docs_consistency.py — 292 passed

# Handoff — F148 Project scoping everywhere (complete)

## State
- Branch: `feature/f148-project-scoping`
- Status: all 4 tasks complete, not pushed, no PR
- Commits (8):
  - `ba3170f` chore(f148): claim feature, reset live review
  - `4756d4f` feat(f148): add project_id to Job model, wire all creation paths (T001)
  - `644d749` feat(f148): add project_scope module with legacy rule (T002)
  - `692215f` chore(f148): handoff with creation-path audit and verification
  - `2c3c925` chore(f148): persist R-0098..R-0101
  - `40d2cad` fix(f148): wire creation guard, attach_job, precompute legacy (R-0098..R-0101)
  - `8301c91` feat(f148): scoped job listings, project adopt, display labels (T003)
  - `9198d27` feat(f148): scoped status view, project-scoping docs, status label flip (T004)

## Changed Files

| File | Change |
|------|--------|
| packages/core/models.py | `project_id: str \| None = None` on Job |
| apps/cli/commands/do_cmd.py | R-0098 ruff fix, R-0099 select_project guard, R-0100 attach_job |
| apps/cli/commands/job.py | R-0099 guard, scoped `_cmd_list_jobs`, `_scope_label` |
| apps/cli/commands/project.py | `_cmd_project_adopt` command |
| apps/cli/commands/status_cmd.py | Scoped via `resolve_scope`/`scoped_jobs` |
| apps/cli/command_catalog.py | `--project`/`--all-projects` on job.list, project.adopt entry |
| packages/orchestration/autorun.py | Pass project_id to Job constructor |
| packages/orchestration/do_run.py | New project_id param → Job constructor |
| packages/orchestration/continue_from_node.py | Inherit project_id from parent |
| packages/orchestration/project_scope.py | NEW: scope resolver, predicate, scoped_jobs |
| docs/system/project-scoping-v0.md | NEW: feature specification |
| docs/README.md | Register project-scoping-v0.md in both tables |
| docs/roadmap/STATUS.md | `[~]` → `[x]` for F148 |
| tests/orchestration/test_project_scope.py | NEW: 13 tests |
| tests/cli/test_scoped_listings.py | NEW: 11 tests (two-project isolation) |
| tests/test_storage.py | 2 new backward-compat tests |
| tests/cli/test_do_runtime.py | 14 tests updated with fixture project |
| tests/cli/test_golden_path.py | 2 tests updated for scoped status labels |
| .agent/decisions.md | 5 new entries |
| .agent/live_review.md | R-0098..R-0101 all Done |
| .agent/plan.md | All tasks checked |

## Creation-Path Audit Table

| File:Line | Constructor / Entry | project_id wired? | attach_job? |
|-----------|--------------------|--------------------|-------------|
| `do_cmd.py:189` | `_cmd_do_mission` (golden-path) | YES: `str(project.id)` | YES |
| `do_cmd.py:420` | `_cmd_do` (legacy v1) | YES: `_resolved_project_id` | YES (R-0100) |
| `job.py:93` | `_cmd_create_job` | YES: from select_project | YES |
| `autorun.py:152` | `run_autorun` | YES: from param | NO (caller responsibility) |
| `do_run.py:215` | `run_do` | YES: from param | NO (caller responsibility) |
| `continue_from_node.py:89` | child job | YES: from parent | YES (pre-existing) |
| `do_cmd.py:1023` | `_cmd_do_job_plan` (pingpong) | N/A: JobPlan model | N/A |

## Listing-Command Audit Table

| Command | Scope support | Method |
|---------|--------------|--------|
| `job list` | `--project`, `--all-projects` | `scoped_jobs()` |
| `status` | auto-scoped to cwd project | `resolve_scope(cwd=repo)` |
| `job show/status/summary/report/budget/...` | N/A (takes job_id) | `load_job()` |
| `brain.*` | N/A (takes job_id) | `load_job()` |
| `decision.*` | N/A (takes job_id) | `load_job()` |
| `dashboard.job` | N/A (takes job_id) | `load_job()` |

Single-job commands don't need scoping — user specifies exact job_id.

## Updated Tests Count
- **14** existing subprocess tests in test_do_runtime.py: added fixture project registration (R-0099 guard requires project)
- **2** status tests in test_golden_path.py: updated for scoped label (was "all projects", now project slug)
- **Total existing tests updated: 16**

## Verification Transcripts

### Ruff — all touched files
```
$ python3 -m ruff check apps/cli/commands/do_cmd.py
Found 6 errors. (all pre-existing on main; branch added zero NEW)

$ python3 -m ruff check apps/cli/commands/job.py apps/cli/command_catalog.py
All checks passed!

$ python3 -m ruff check apps/cli/commands/project.py
Found 2 errors. (both pre-existing on main; branch added zero NEW)

$ python3 -m ruff check apps/cli/commands/status_cmd.py tests/cli/test_golden_path.py tests/cli/test_scoped_listings.py tests/cli/test_do_runtime.py packages/orchestration/project_scope.py
All checks passed!
```

### Unit tests — scope + storage
```
$ python3 -m pytest tests/orchestration/test_project_scope.py tests/test_storage.py tests/cli/test_scoped_listings.py -q
..................................                                       [100%]
34 passed in 0.12s
```

### CLI tests
```
$ python3 -m pytest tests/cli -q --tb=no
18 failed, 1007 passed in 154.78s

(Same 18 pre-existing failures as main baseline. Zero NEW failures.)
```

## Findings
R-0098..R-0101 all resolved (see live_review.md).

## Next expected action
Reviewer reviews repair+T003+T004 bundle.

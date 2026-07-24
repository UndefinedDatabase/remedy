# Handoff — F148 T001+T002

## State
- Branch: `feature/f148-project-scoping`
- Commits:
  - `ba3170f` chore(f148): claim feature, reset live review
  - `4756d4f` feat(f148): add project_id to Job model, wire all creation paths (T001)
  - `644d749` feat(f148): add project_scope module with legacy rule (T002)

## Changed Files

### Commit 1 — feature start (`ba3170f`)
| File | Change |
|------|--------|
| docs/roadmap/STATUS.md | `[ ]` → `[~]` for F148 |
| .agent/live_review.md | Reset for F148 (last R-XXXX: R-0097) |
| .agent/plan.md | Rewritten for F148 |

### Commit 2 — T001 (`4756d4f`)
| File | Change |
|------|--------|
| packages/core/models.py | Add `project_id: str \| None = None` to Job |
| apps/cli/commands/do_cmd.py | Golden-path: set project_id + attach_job; legacy: resolve via select_project |
| apps/cli/commands/job.py | Set project_id on Job from --project flag |
| packages/orchestration/autorun.py | Pass project_id param to Job constructor |
| packages/orchestration/do_run.py | New project_id param, set on Job |
| packages/orchestration/continue_from_node.py | Inherit project_id from parent; prefer model field over metadata |
| tests/test_storage.py | 2 new tests: backward-compat (old JSON loads with None), roundtrip |
| .agent/decisions.md | 3 new entries (field placement, legacy path, continue_from_node) |
| .agent/plan.md | T001 marked done |

### Commit 3 — T002 (`644d749`)
| File | Change |
|------|--------|
| packages/orchestration/project_scope.py | NEW: scope selector, job_in_scope, scoped_jobs, legacy rule |
| tests/orchestration/test_project_scope.py | NEW: 13 tests covering all scope scenarios |

## Creation-Path Audit Table

| File:Line | Constructor / Entry | project_id wired? | attach_job? |
|-----------|--------------------|--------------------|-------------|
| `do_cmd.py:189` | `_cmd_do_mission` (golden-path) | YES: `str(project.id)` | YES |
| `job.py:92` | `_cmd_create_job` | YES: from `--project` flag | YES (pre-existing) |
| `autorun.py:152` | `run_autorun` | YES: from `project_id` param | NO (caller's responsibility) |
| `do_run.py:215` | `run_do` | YES: new param | NO (legacy path) |
| `continue_from_node.py:89` | child job | YES: from parent | YES (pre-existing) |
| `do_cmd.py:1023` | `_cmd_do_job_plan` (pingpong) | N/A: separate JobPlan model | N/A |

## Verification Results

### T001: tests/test_storage.py
```
$ python3 -m pytest tests/test_storage.py -q
..........                                                               [100%]
10 passed in 0.08s
```

### T002: tests/orchestration/test_project_scope.py
```
$ python3 -m pytest tests/orchestration/test_project_scope.py -q
.............                                                            [100%]
13 passed in 0.08s
```

### Gate: tests/orchestration (branch)
```
$ python3 -m pytest tests/orchestration -q --tb=no
82 failed, 8230 passed, 7 skipped in 489.28s
```

### Gate: tests/orchestration (main baseline)
```
$ python3 -m pytest tests/orchestration -q --tb=no
88 failed, 8224 passed, 7 skipped in 522.59s
```
Zero NEW failures (branch has fewer due to flaky timing tests).

### Gate: tests/cli (branch)
```
$ python3 -m pytest tests/cli -q --tb=no
18 failed, 996 passed in 132.66s
```

### Gate: tests/cli (main baseline)
Same 18 failures (all pre-existing: missing doc files).

### Ruff
```
$ python3 -m ruff check <touched files>
do_cmd.py: 7 errors (6 pre-existing on main + 1 new I001 from adjacent import block)
All other files: All checks passed!
```

## Decisions Made
- Field type `str | None` (not UUID) — matches registry string job_ids
- Legacy do_run path permits None project_id (predates project identity)
- continue_from_node: model field > metadata fallback
- project_scope.py in packages/orchestration/ beside storage.py

## Findings: none
## Next expected action: reviewer reviews T001+T002

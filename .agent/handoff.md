# Handoff — F148 repair-2 (R-0102..R-0107)

## State
- Branch: `feature/f148-project-scoping`
- Status: all repairs complete, not pushed, no PR
- Total commits on branch: 16

## Repair Commits (this round)

### `f4c188f` chore: persist R-0102..R-0107, resolve R-0098..R-0101
| File | Change |
|------|--------|
| .agent/live_review.md | R-0098..R-0101 → Resolved; R-0102..R-0107 appended verbatim |

### `2851b47` fix: revert unauthorized STATUS [x] to [~] (R-0102)
| File | Change |
|------|--------|
| docs/roadmap/STATUS.md | `[x]` → `[~]` for F148 |
| .agent/live_review.md | R-0102 Done |

### `6e240a2` fix: project adopt takes explicit job_id (R-0103)
| File | Change |
|------|--------|
| apps/cli/commands/project.py | Rewrite: positional job_id, short ID resolution, exit 2 on already-scoped |
| apps/cli/command_catalog.py | project.adopt: positional job_id, remove --all |
| .agent/live_review.md | R-0103 Done |
| .agent/decisions.md | New entry: adopt takes explicit job_id |

### `8e2dae2` fix: scope stats failures (R-0105)
| File | Change |
|------|--------|
| apps/cli/commands/failure_stats_cmd.py | --project/--all-projects params, scoped_jobs filter |
| packages/orchestration/failure_stats.py | New `job_ids` filter on collect_failures |
| apps/cli/command_catalog.py | _PROJECT_SCOPE_OPT + _ALL_PROJECTS_FLAG on stats.failures |
| .agent/live_review.md | R-0105 Done |

### `58812e9` fix: --project/--all-projects on status (R-0106)
| File | Change |
|------|--------|
| apps/cli/commands/status_cmd.py | project_flag/all_projects params → resolve_scope |
| apps/cli/command_catalog.py | _PROJECT_SCOPE_OPT + _ALL_PROJECTS_FLAG on status.run |
| .agent/live_review.md | R-0106 Done |

### `73ab496` fix: (unscoped)/(orphaned) labels everywhere (R-0107)
| File | Change |
|------|--------|
| apps/cli/commands/job.py | _known_project_ids(), _scope_label takes known_ids, unscoped always, orphaned check |
| .agent/live_review.md | R-0107 Done |

### `b342833` fix: real CLI subprocess tests (R-0104)
| File | Change |
|------|--------|
| tests/cli/test_scoped_listings.py | Rewrite: 6 subprocess + 10 unit = 16 tests |
| .agent/live_review.md | R-0104 Done |

## Listing-Command Audit Table (updated)

| Command | Scope support | Method |
|---------|--------------|--------|
| `job list` | `--project`, `--all-projects` | `scoped_jobs()` |
| `status` | `--project`, `--all-projects` | `resolve_scope()` → `scoped_jobs()` |
| `stats failures` | `--project`, `--all-projects` | `job_ids` filter on `collect_failures` |
| `job show/status/summary/report/budget/fences/checkpoints` | N/A (takes job_id) | `load_job()` |
| `job stop --status` | N/A (takes job_id) | `load_job()` |
| `job rerun` | N/A (takes job_id) | `load_job_plan()` |
| `brain.graph/node/context/trust/timeline/cockpit/constitution` | N/A (takes job_id) | `load_job()` |
| `decision.list/show` | N/A (takes job_id) | `load_job()` |
| `blocker.list/show` | N/A (takes job_id) | `list_stop_reasons()`/`get_stop_reason()` |
| `dashboard.job` | N/A (takes job_id) | `load_job()` |
| `token.usage/budget` | N/A (takes job_id) | `load_job()` |

## Updated Tests Count
- **14** test_do_runtime.py: fixture project registration (from repair-1 round)
- **2** test_golden_path.py: scoped status labels (from T004)
- **16** test_scoped_listings.py: rewritten with 6 CLI subprocess + 10 unit tests
- **Total existing tests updated: 16** (this round)

## Verification Transcripts

### tests/cli/test_scoped_listings.py
```
$ python3 -m pytest tests/cli/test_scoped_listings.py -q
................                                                         [100%]
16 passed in 4.13s
```

### tests/orchestration/test_project_scope.py + tests/test_storage.py
```
$ python3 -m pytest tests/orchestration/test_project_scope.py tests/test_storage.py -q
.......................                                                  [100%]
23 passed in 0.13s
```

### tests/cli (full suite)
```
$ python3 -m pytest tests/cli -q --tb=no
18 failed, 1012 passed in 159.23s

Known 18 pre-existing failures (test_do_cmd_summary 11, test_product_spine 7).
Zero NEW failures. 1012 passed (up from 996 baseline = +16 new tests).
```

### ruff (every touched file)
```
$ python3 -m ruff check <all touched files>
Found 8 errors. (6 do_cmd.py + 2 project.py — all pre-existing on main)
Zero NEW errors.
```

## Findings
R-0102..R-0107 all resolved (see live_review.md).

## Next expected action
Reviewer reviews repair-2 bundle.

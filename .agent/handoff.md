# Handoff — F148 repair-3 (R-0108..R-0109)

## State
- Branch: `feature/f148-project-scoping`
- Status: all repairs complete, not pushed, no PR
- Total commits on branch: 20

## Repair Commits (this round)

### `2935653` chore: persist R-0108..R-0109, resolve R-0102..R-0107
| File | Change |
|------|--------|
| .agent/live_review.md | R-0102..R-0107 → Resolved + reviewer lines; R-0108..R-0109 appended verbatim |

### `a532c43` fix: status --project displays scoped project slug (R-0108)
| File | Change |
|------|--------|
| apps/cli/commands/status_cmd.py | When scope.project_id differs from cwd project, load scoped project for slug display |
| tests/cli/test_scoped_listings.py | New assertion in test_status_scoped: --project B from cwd=A shows slug_b in JSON |
| .agent/live_review.md | R-0108 Done |

### `b175903` test: stats-failures scoping tests (R-0109)
| File | Change |
|------|--------|
| tests/cli/test_scoped_listings.py | +TestCollectFailuresJobIds (unit: job_ids filter), +TestStatsFailuresScopedCLI (CLI: --project flag) |
| .agent/live_review.md | R-0109 Done |

## Listing-Command Audit Table (unchanged from repair-2)

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

## Updated Tests Count (this round)
- **1** test_scoped_listings.py test_status_scoped: added --project B assertion (+1 assertion block)
- **2** test_scoped_listings.py: new test classes TestCollectFailuresJobIds (1 test) + TestStatsFailuresScopedCLI (1 test)
- **Total: 18 tests in test_scoped_listings.py** (was 16, now +2)

## Verification Transcripts

### tests/cli/test_scoped_listings.py
```
$ python3 -m pytest tests/cli/test_scoped_listings.py -q
..................                                                       [100%]
18 passed in 5.28s
```

### tests/orchestration/test_project_scope.py + tests/test_storage.py
```
$ python3 -m pytest tests/orchestration/test_project_scope.py tests/test_storage.py -q
.......................                                                  [100%]
23 passed in 0.10s
```

### tests/cli (full suite)
```
$ python3 -m pytest tests/cli -q --tb=no
18 failed, 1014 passed in 160.75s

Known 18 pre-existing failures (test_do_cmd_summary 11, test_product_spine 7).
Zero NEW failures. 1014 passed (up from 1012 = +2 new tests this round).
```

### ruff (touched files)
```
$ python3 -m ruff check apps/cli/commands/status_cmd.py apps/cli/commands/failure_stats_cmd.py packages/orchestration/failure_stats.py tests/cli/test_scoped_listings.py
All checks passed!
```

## Findings
R-0108..R-0109 both Done (see live_review.md).

## Next expected action
Reviewer reviews repair-3 bundle.

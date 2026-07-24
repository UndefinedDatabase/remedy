# Handoff — F147 Golden-path CLI — REPAIR ROUND 2 COMPLETE
Branch: feature/f147-golden-path-cli
Last commit: dd368dd fix(f147): R-0093 argv-level bare detection

## Commits (repair round 2)
  5e85afb chore(review): persist R-0092..R-0093
  68064a7 fix(f147): R-0092 job stop finds golden-path jobs; smoke uses real CLI
  dd368dd fix(f147): R-0093 argv-level bare detection replaces value-equality guard

## Changed files
  | File | Change |
  |------|--------|
  | apps/cli/commands/job_stop_cmd.py | R-0092 _CoreJobAdapter fallback to storage.load_job |
  | apps/cli/grouped.py | R-0093 _truly_bare argv scan (--json/--repo allowed) |
  | apps/cli/commands/do_cmd.py | R-0093 use truly_bare instead of value-equality |
  | tests/cli/test_golden_path.py | +4 tests (stop CLI, unknown id, default flag, --repo); smoke uses real CLI |
  | .agent/decisions.md | R-0092 store-split, R-0093 argv-level detection + default reconciliation |
  | .agent/live_review.md | R-0085–R-0091 Resolved, R-0092–R-0093 Done |

## Findings: R-0092 Done, R-0093 Done

## RAW verification transcripts

### Golden-path tests (branch)
```
$ python3 -m pytest tests/cli/test_golden_path.py -v
exit 0 — 29 passed in 9.64s
```

### Broader gate (branch)
```
$ python3 -m pytest tests/cli/ tests/test_grouped_cli.py tests/test_command_catalog.py -q
exit 1 — 21 failed, 1479 passed in 179.04s
Failures (all pre-existing, verified identical on main):
  7× test_product_spine.py (missing spine docs)
  8× test_do_cmd_summary.py (missing docs/autocoder-usage.md)
  3× test_command_catalog.py (catalog classification + sensitivity — same on main)
  2× test_self_dogfood_execution_cli.py (on main only, fixed on branch)
```

### Ruff (branch)
```
$ python3 -m ruff check .
432 errors (identical to main)
```

### Manual probe (scratch repo)
```
$ python3 -m apps.cli.grouped init
exit 0 — project remedy-probe-436921 created

$ python3 -m apps.cli.grouped do "probe mission" --json
exit 0 — job_id: 6c21ca95-..., state: planned, stops_pending not yet set

$ python3 -m apps.cli.grouped job stop 6c21ca95-b7fc-4f2b-8afd-9d67f3cb6358
exit 0 — "Stop requested — it will take effect at the next safe point."

$ python3 -m apps.cli.grouped status --json
exit 0 — stops_pending: 1, jobs.planned: [{job_id: "6c21ca95-..."}]
```

## Net: 0 new failures, 0 ruff delta.
## Next: reviewer re-verify

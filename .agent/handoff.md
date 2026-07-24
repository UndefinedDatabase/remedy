# Handoff — F147 Golden-path CLI — REPAIR ROUND COMPLETE
Branch: feature/f147-golden-path-cli
Last commit: c1d1378 fix(f147): R-0090 extend smoke test with stop leg

## Commits (repair round)
  df359a4 fix(f147): R-0085 bare-mission intercept
  b19b543 fix(f147): R-0086 corrupt runtime state → unknown + warning
  0dcbc31 fix(f147): R-0087 stops_pending → F011 kill-switch
  16c0fbc fix(f147): R-0088 decisions_open uses real events
  7b42514 fix(f147): R-0089 "all projects" label + next-command lines
  c1d1378 fix(f147): R-0090 smoke test stop leg

## Changed files
  | File | Change |
  |------|--------|
  | apps/cli/commands/status_cmd.py | R-0086 load_state_result, R-0087 safe_points, R-0088 load_run_events, R-0089 scope/next |
  | apps/cli/commands/do_cmd.py | R-0085 injection marker + comprehensive flag guard |
  | apps/cli/grouped.py | R-0085 _did_inject → args._injected_default |
  | tests/cli/test_golden_path.py | +4 tests (corrupt runtime, stop pending, decisions w/events, scope); smoke extended |
  | .agent/live_review.md | R-0085–R-0091 all marked Done |

## Findings: R-0085 Done, R-0086 Done, R-0087 Done, R-0088 Done, R-0089 Done, R-0090 Done, R-0091 Done

## RAW verification transcripts

### Golden-path tests (branch)
```
$ python3 -m pytest tests/cli/test_golden_path.py -v
exit 0 — 25 passed in 8.10s
```

### Full CLI gate (branch)
```
$ python3 -m pytest tests/cli/ -q
exit 1 — 18 failed, 989 passed in 150.68s
Failures (all pre-existing, identical categories as main):
  7× test_product_spine.py (missing spine docs)
  9× test_do_cmd_summary.py (missing docs/autocoder-usage.md)
  2× test_do_cmd_summary.py::TestDocsCommandContract (same missing file)
```

### Full CLI gate (main baseline)
```
$ python3 -m pytest tests/cli/ -q   # run in main worktree
exit 1 — 20 failed, 962 passed in 147.51s
```

### Ruff (branch)
```
$ python3 -m ruff check .
432 errors (identical to main)
```

### Ruff (main baseline)
```
$ python3 -m ruff check .   # run in main worktree
432 errors
```

## Net: +27 tests passed, -2 failures (dogfood tests fixed on branch). 0 new failures. 0 ruff delta.
## Next: push, reviewer re-verify

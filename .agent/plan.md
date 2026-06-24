# Plan — Steps 4216-4265: Dogfood Cache-Noise + Staged Diff Report Closure v2

## Goal
Fix real dogfood blocker: cache dirs (.pytest_cache, .ruff_cache, .mypy_cache)
falsely triggering target_mutation_blocked. Preserve staged evidence on block.
Fix --keep-staging as boolean flag.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- Target noise classification: _is_target_noise() + _TARGET_NOISE_DIRS
  - Cache dirs classified as noise, not meaningful mutation
  - Source/doc/config/lock files still trigger block
- _check_target_mutation returns (meaningful, noise) tuple
- All 4 call sites updated (after builder, tests, reviewer, finally)
- Staged evidence preserved even on target_mutation_blocked
- New fields: ignored_target_noise_files, target_noise_detected, staging_path
- staging_retained + staging_path in export JSON
- summarize_pingpong shows noise info
- _cmd_do_report shows noise info
- --keep-staging as store_true in grouped.py
- --builder/--reviewer/--max-rounds/--mode/--test-command/etc. proper argparse mappings
- 29 new tests (92 total in test_pingpong_cli.py)
- Real smoke: builder edited README.md, target clean, diff preserved, no noise block
- Architecture guard: CLEAN
- Full suite: 7305 passed, 0 failed
- Fast: 571, Runtime: 4/4, Lint: clean

## Dogfood command
```
remedy do run "Add docs note about ping-pong reports" \
  --repo . --builder claude-cli --reviewer claude-cli \
  --claude-cli-write-mode allowed-tools \
  --max-rounds 2 --mode staged \
  --test-command "python3 -m pytest tests/orchestration/test_pingpong.py -q" \
  --keep-staging --json
```

# Plan — Steps 3856-3885: Final Safety Closure v1.0

## Goal
Close last proof gaps: process group cleanup guarantee, runtime timeout edge
case, forced timeout regression test. Make PR #101 merge-ready.

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- remedy_pytest_runner.py: _ensure_pg_dead(pgid) moved to try/finally (line 97)
- remedy_test_runtime.sh: fail-fast guard for inner >= outer timeout (lines 33-37)
- 4 new regression tests: try/finally guarantee, timeout edge case, forced timeout cleanup
- Fulfillment wrapper: 109 passed × 2 runs
- Runtime lane: 4/4 suites × 2 runs
- Fast lane: 571 passed
- Full suite: 7176 passed, 0 failed, 8 skipped
- Lint: ruff clean, mypy clean (194 files)
- Architecture guard: clean
- No stale processes

## Risks
- None remaining

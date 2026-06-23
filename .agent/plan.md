# Plan — Steps 3886-3915: Final Wrapper-Path Timeout Proof v1.1

## Goal
Close final proof gap: wrapper-path forced timeout tests that exercise the
actual chain (remedy_pytest.sh → flock → runner → child pytest).

## Current Step
Complete. All implementation, tests, verification done.

## Completed
- 4 new wrapper-path timeout regression tests:
  - test_wrapper_timeout_cleanup_no_orphans
  - test_lock_released_after_timeout
  - test_subsequent_wrapper_succeeds_after_timeout
  - test_inner_cleanup_before_outer (runtime-like chain)
- Process diagnostic helper: _find_processes_by_filename, _assert_no_orphans
- Fulfillment wrapper: 109 passed × 2 runs
- Runtime lane: 4/4 suites × 2 runs
- Fast lane: 571 passed
- Full suite: 7180 passed, 0 failed, 8 skipped
- Lint: ruff clean, mypy clean (194 files)
- Architecture guard: clean
- No stale processes, lock not held

## Risks
- None remaining

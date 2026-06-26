# Plan — Steps 5005-5020: Job Workspace Apply Symlink + Partial Promote Failure Closure v4

## Goal
Harden workspace apply against staged source symlinks and destination symlinks.
Generalize structured persistence failure handling after target mutation in promote.
Remove debug detritus from repo root.

## Current Step
All implementation and tests complete. Ready for commit.

## Completed
- Step 5005: Source containment in `_strict_apply_to_workspace` — symlink, parent symlink, escape, regular file checks
- Step 5006: Regression test — staged source symlink outside blocks (2 tests)
- Step 5007: Regression test — staged source parent symlink blocks (1 test)
- Step 5008: Destination containment in `_strict_apply_to_workspace` — symlink, parent symlink, escape checks
- Step 5009: Regression test — workspace destination symlink blocks (1 test)
- Step 5010: Regression test — workspace destination parent symlink blocks (1 test)
- Step 5011: Source + dest containment recheck immediately before copy
- Step 5012: Replaced `shutil.copy2` with `src.read_bytes()` + `dst.write_bytes()` — no symlink following
- Step 5013: Baseline proof semantics preserved — all existing tests pass
- Step 5014: `_safe_persist` wraps all post-mutation persistence; no unstructured OSError escape
- Step 5015: Regression test — partial apply then blocked record failure is structured
- Step 5016: Regression test — post-test failure record persistence failure is structured
- Step 5017: Removed `BUILDER_WAS_HERE.txt` (test detritus from `test_pingpong_cli.py` L69)
- Step 5018: All 74 promote tests pass — existing safety preserved
- Step 5019: All evidence/runner/fulfillment tests pass — no regression
- Step 5020: Architecture guard clean, final handoff

## Test Counts
- job_promote: 74 (was 72, +2 new)
- job_task_runner: 187 (was 181, +6 new)
- Full suite: 8056 passed, 8 skipped, 0 failed (1 pre-existing in test_project_brain)

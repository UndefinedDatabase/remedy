# Plan

## Goal
Step 17.1: Restore terminal-event invariant and planning_failed redaction lost in merge.

## Status
COMPLETE — 709 tests pass

## Steps
1. [x] Fix planning_failed: use error_category + fixed message="planning failed", not str(exc)
2. [x] Add _fail() closure after task_run_started
3. [x] Fix workspace_write denial: call _fail("permission_denied") before sys.exit(1)
4. [x] Fix exception handlers: add _fail() calls; reorder ValidationError before ValueError
5. [x] Fix result.changed=False: log task_run_noop/no_change + correct CLI text
6. [x] Fix timeline.py: never use ev["message"] for planning_failed; use error_category only
7. [x] Add terminal-event invariant tests to test_run_log_cli.py (29 new tests)
8. [x] Update docs/architecture.md: invariant, two noop outcomes, redaction note
9. [x] Update .agent files and commit

## Branch
feature/step17-timeline

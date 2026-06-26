# Plan — Steps 4991-5004: Job Promote Destination Symlink + Durable Record Closure v3

## Goal
Block all destination symlinks in job-promote (even those resolving inside target),
add durable pre-apply promotion record, and handle final record update failure
structurally rather than with unhandled exceptions.

## Current Step
All implementation and tests complete. Ready for commit.

## Completed
- Step 4991: Block all destination symlinks and parent symlinks in `_validate_dest_containment()`
- Step 4992: Regression test — destination symlink inside target blocks
- Step 4993: Regression test — destination parent symlink inside target blocks
- Step 4994: Destination containment recheck immediately before every write in apply loop
- Step 4995: Durable pre-apply promotion record (`approved_apply_started`) before writing files
- Step 4996: Structured handling of final record update failure (`promoted_record_update_failed`)
- Step 4997: Regression test — final record failure after apply is structured (3 tests)
- Step 4998: Regression test — pre-apply record failure blocks before write (2 tests)
- Step 4999: Updated promotion status model/export for all states
- Step 5000: Grouped CLI tests for destination symlink and parent symlink (2 tests)
- Step 5001: Baseline-aware promotion behavior preserved (all 61 prior tests pass)
- Step 5002: Existing job/evidence/promote safety preserved (8048 full suite)
- Step 5003: Architecture guard search clean
- Step 5004: Final handoff

## Test Counts
- job_promote: 72 (was 61, +11 new)
- Full suite: 8048 passed, 8 skipped, 0 failed

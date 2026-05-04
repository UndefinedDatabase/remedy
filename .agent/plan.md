# Plan

## Goal
Step 17.2: Lock down timeline redaction and invariant tests (hardening-only).

## Prior step
Step 17.1 restored terminal-event invariant and planning_failed redaction.

## Status
COMPLETE — 715 tests pass. PR #16 ready for merge.

## Steps
1. [x] Add planning_failed fallback tests to test_timeline.py (no error_category → "unknown error"; message field never rendered)
2. [x] Add structural invariant assertions to ImportError, ValidationError, ValueError, generic Exception test classes
3. [x] Update docs/architecture.md: explicit timeline rendering rules for planning_failed and task_run_noop
4. [x] Update .agent files and commit

## Branch
feature/step17-timeline

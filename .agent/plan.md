# Plan — Steps 580-594: Proposed Task Backend Closure

## Goal
Make proposed tasks reliable: CLI truth, storage stability, honest gates.

## Current Step
594 — Final baseline verification

## Steps
- [x] 580: Update context/plan/live_review — backend focus, UI paused
- [x] 581: Create `apps/cli/commands/propose_cmd.py` with 6 handlers
- [x] 582: Propose CLI contract tests (23 tests)
- [x] 583: Data-dir correct proposed task store (root= param, no module global dependency)
- [x] 584: Atomic writes via temp file + rename
- [x] 585: Corrupt store → ProposedTaskStoreError, degraded not empty
- [x] 586: Transition hardening (terminal blocks, bounded reasons, timestamps)
- [x] 587: Audit events from CLI — emit_proposed_task_event on approve/reject/defer
- [x] 588: Worker queue gate uses data_dir, corrupt store blocks
- [x] 589: Materialization — materialize_approved_task() + list_approved_not_materialized()
- [x] 590: Finalized gate — can_finalize() centralized, degraded blocks
- [x] 591: Reviewer integration — accept_recommendation creates ProposedTask not Task
- [x] 592: Dashboard proposed_tasks section: degraded, blocking_finalized, blocking_build
- [x] 593: End-to-end test: full lifecycle, queue gate, finalize gate
- [x] 594: Full baseline: 4328 passed, 0 failed, 8 skipped

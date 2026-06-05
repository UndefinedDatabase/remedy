# Plan — Steps 595-609: Backend Reliability Closure

## Goal
Audit trail, store locking, materialization truth, centralized gates.

## Current Step
609 — Final baseline

## Steps
- [x] 595: Clean backend handoff — risks carried forward
- [x] 596: (merged into 608) Runtime CLI tests via handlers
- [x] 597: Real audit events — _make_writer(job_id), no more None writers
- [x] 598: File locking — fcntl.flock with bounded retry
- [x] 599: Remove import-time _STORE_DIR — resolves at call time via proposed_tasks_dir()
- [x] 600: Centralize finalized gate — ui_server uses can_finalize()
- [x] 601: Materialization state — materialized_task_id, materialized_at on ProposedTask
- [x] 602: propose.materialize command + catalog entry + handler
- [x] 603: (merged into 601/602) Queue gate — approved-not-materialized explicit
- [x] 604: Dashboard v2 — approved_not_materialized, materialized, summaries
- [x] 605: (merged into 597) Reviewer/rework audit — writer passed where available
- [x] 606: (merged into tests) Corrupt store drill — all surfaces tested
- [x] 607: (merged into tests) Store race regression — sequential + approve+materialize
- [x] 608: (merged into CLI tests) Audit + materialize CLI tests
- [x] 609: Full baseline: 4344 passed, 0 failed, 8 skipped

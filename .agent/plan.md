# Plan — Steps 610-624: Job Task Materialization + Backend Build Readiness

## Goal
Close: ProposedTask → approved → materialized into real Job.tasks → queue sees real work.

## Current Step
624 — Final baseline

## Steps
- [x] 610: Clean backend handoff — agent files current
- [x] 611: Job storage data-root correct — root= param, atomic writes, JobStoreError
- [x] 612: Require real Job for mutating propose commands — _require_job gate
- [x] 613: True materialization — do_materialize loads Job, appends Task, saves Job
- [x] 614: Reconciliation helper — reconcile_materialized detects mismatches
- [x] 615: can_finalize blocks approved_not_materialized
- [x] 616: Subprocess CLI test suite — 11 tests via python -m apps.cli.grouped
- [x] 617: Audit events link proposed_task_id and materialized_task_id
- [x] 618: Dashboard v2 already includes materialization (from 604)
- [x] 619: Finalize gate v2 — approved_not_materialized blocks
- [x] 620: Reviewer/rework — same materialization path, trace preserved in Task.inputs
- [x] 621: Job store — atomic writes, JobStoreError on corrupt, load_job_safe
- [x] 622: backend_readiness() helper — job/proposal/materialization health
- [x] 623: overnight_readiness() gate — always returns not ready + specific blockers
- [x] 624: Full baseline: 4365 passed, 0 failed, 8 skipped

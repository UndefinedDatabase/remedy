# Plan

## Goal
Steps 65.1, 66, 67, 68: Git Status Brain Closure, Event Ledger v1, Stop Reasons v1, Autonomy Loop v1

## Current Step
All steps complete. Pending: commit + push + PR.

## Tasks
- [x] Step 65.1: Git Status Brain Closure (job-aware repo status, git init in smoke, brain always creates node when target_repo set, git_status_read event)
- [x] Step 66: Event Ledger v1 (LedgerEvent model, redaction, deterministic IDs, event CLI, brain event_ledger node)
- [x] Step 67: Stop Reasons v1 (StopReason model, JSONL storage, derive from job state, blocker CLI, brain stop_reason node)
- [x] Step 68: Autonomy Loop v1 (CycleDecision/LoopResult, level 0-7 decisions, run-loop CLI, run-log events)
- [x] Brain detail handlers for event_ledger and stop_reason
- [x] Tests: 2683 passing
- [x] Smoke: updated (12z-12ae for Steps 66-68)
- [x] Step 68.1: Agent Loop Schema Closure (per-event-type schemas, event_schemas.py, smoke 12h fix)
- [x] Step 69: Human Decision Queue v1 (HumanDecision model, 5 sources, decision CLI, brain node, readiness signal)
- [x] Step 70: Project Dashboard v1 (build_job_dashboard, build_project_dashboard, dashboard CLI)
- [x] Step 71: Context Budget Optimizer v1 (explain_context, optimize_context, context CLI, brain node, 7-field event schema)
- [x] Brain detail handlers for decision_queue and context_budget
- [x] Readiness integration: no_open_decisions signal at level 4
- [x] Bug fix: context_pack NoneType on null user_prompt
- [x] Tests: 2740 passing
- [x] Smoke: updated (12af-12ai for Steps 68.1-71, group help: decision + dashboard)
- [x] Update live_review.md — PASS, 0 blockers
- [ ] Commit + push

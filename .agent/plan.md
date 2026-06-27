# Plan — Agent Run Trace + Job-Flow Cockpit Bridge v1

## Goal
Make Remedy able to prove, inspect, and visualize its own Builder/Reviewer/
Repair/Final-Audit loop from real evidence. Close 6 verified gaps.

## Current Step
Step 1: Agent Run Trace model + helpers.

## Commits Planned
1. Agent run trace model (`agent_run_trace.py`) + helpers
2. Fix prompt trace metadata (job_id, task_id, provider_kind in run_pingpong)
3. Agent run trace capture in do_cmd job-flow + final audit evidence-derived
4. Job-Flow Cockpit Bridge (ui_server adapter for JobPlan IDs)
5. Path sanitization for shareable evidence
6. Tests for all deliverables
7. Smoke test + verification + handoff

## Constraints
- No auto-approval
- No target repo mutation in job-flow
- No git commit/push/merge behavior
- No UI mutation controls
- No external providers unless via CLI options
- No fake UI events from planned tasks
- No hiding missing data as zero
- No MemPalace or hardwired memory backend
- All English

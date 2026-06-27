# Plan — Steps 5053-5072: Agent Run Trace + Job-Flow Cockpit Bridge v1

## Goal
Make Remedy able to prove, inspect, and visualize its own Builder/Reviewer/
Repair/Final-Audit loop from real evidence. Close 6 verified gaps.

## Current Step
All 6 deliverables implemented and tested. Committing tests + creating PR.

## Deliverables (all complete)
1. Agent Run Trace v1 — `agent_run_trace.py` with 16 event kinds
2. Prompt Trace metadata fix — job_id, task_id, provider_kind in run_pingpong
3. Evidence-derived Final Audit — availability from real artifacts
4. Job-Flow Cockpit Bridge — _JobPlanAdapter for hex IDs
5. Path sanitization — staging/tmp paths replaced with safe labels
6. Safety guarantees preserved — no auto-approval, no mutation, no fakes

## Tests
- 13 tests in test_agent_run_trace.py
- 16 tests in test_final_audit_evidence.py
- 12 new + 1 fix in test_do_job_flow.py
- 113 focused tests pass, 3771 broader suite pass

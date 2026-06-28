# Plan — Agent Evidence Truth Reconciliation + Cockpit Evidence Resolution v1

## Goal
Fix 7 acceptance gaps (R-4301 through R-4307) in Agent Run Trace, Final Audit,
Evidence Bundle, and Cockpit Bridge to make them truthful, consistent, and safe.

## Current Step
All implementation and testing complete. Committing, pushing, creating PR.

## Status
- R-4301 (final audit truth): DONE — `job_flow_json_available=True` + required artifact checks
- R-4302 (evidence index): DONE — `_persist_evidence_index()` + `_resolve_evidence_dir()`
- R-4303 (prompt correlation): DONE — `_load_prompt_trace_index()` populates sha256/chars
- R-4304 (path hygiene): DONE — `/home/`, `/Users/`, `/private/` sanitized + `next_approve_command_safe`
- R-4305 (trace honesty): DONE — `trace_source="reconstructed"` + `source_limitations`
- R-4306 (dashboard): DONE — `_build_job_plan_dashboard()` using Agent Run Trace events
- R-4307 (process): Handoff note — reviewer verdict for PR #107 still pending

## Tests
- 59 E2E tests pass (tests/test_do_job_flow.py) — includes 8 new for R-4301..R-4305
- 18 unit tests pass (test_agent_run_trace.py) — includes 5 new for trace_source/prompt
- 23 unit tests pass (test_final_audit_evidence.py) — rewritten for new artifact checks
- 270 regression/UI tests pass

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no external providers, no fake events, no hiding missing data, no MemPalace.

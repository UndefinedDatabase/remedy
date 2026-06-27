# Plan — Steps 5073-5094: Job Flow Observability v2 + Prompt Trace Evidence

## Goal
Make `remedy do job-flow` reviewable as a Mission Control run. Add prompt
trace evidence, token summary, safe next-approve command, timeout hint,
final audit, blocked diagnostics, persisted job_flow.json, and review ZIP
coverage fix.

## Current Step
Step 5073: Implement prompt trace model + redaction.

## Commits Planned
1. New `prompt_trace.py` — model + redaction + helpers (Steps 5073)
2. Capture builder/reviewer traces in pingpong_loop.py (Steps 5074-5075)
3. Prompt trace evidence export (Steps 5076-5077)
4. do_cmd.py — token_summary, next_approve_command, timeout hint,
   final_audit, blocked diagnostics, job_flow.json (Steps 5078-5083)
5. Review ZIP coverage fix (Step 5084)
6. Tests (Steps 5085-5090)
7. Smoke + checks + handoff (Steps 5091-5094)

## Constraints
- No auto-approval
- No overnight/multi-run logic
- No target repo mutation
- No secrets in prompt traces
- No unbounded raw prompts
- No rescue of blocked workspace files
- All English

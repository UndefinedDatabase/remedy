# Plan — Steps 5073-5094: Job Flow Observability v2 + Prompt Trace Evidence

## Goal
Make `remedy do job-flow` reviewable as a Mission Control run. Add prompt
trace evidence, token summary, safe next-approve command, timeout hint,
final audit, blocked diagnostics, persisted job_flow.json, and review ZIP
coverage fix.

## Current Step
Complete. All 22 steps (5073-5094) implemented and verified.

## Commits
1. `e2d0f96` — prompt trace model + capture + evidence export (Steps 5073-5077)
2. `50e40d0` — token summary, approve command, timeout hint, final audit (Steps 5078-5084)
3. `189893d` — tests (Steps 5085-5090)

## Verification
- 3692 passed, 1 pre-existing failure (`test_full_chain_order`), 7 skipped
- Smoke test (fake provider): passed
- Review ZIP: 763 files, 0 coverage artifacts, all key files present

## Constraints (all met)
- No auto-approval
- No overnight/multi-run logic
- No target repo mutation
- No secrets in prompt traces
- No unbounded raw prompts
- No rescue of blocked workspace files
- All English

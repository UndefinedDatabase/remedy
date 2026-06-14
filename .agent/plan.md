# Plan — Steps 1499-1536: Local Model Advisor Adapter v0

## Goal
Optional Ollama-compatible local-model advisory critique for orchestrator decisions.
Loopback-only, disabled by default, advisory-only. When the deterministic orchestrator is
uncertain, it MAY ask a local advisor to critique a SAFE decision summary. The advisor may
flag concerns/alternatives/missing evidence; the orchestrator verifies everything against
deterministic evidence and the final next_safe_action stays deterministic + catalog-backed.

## Core principle
LLMs advise. The orchestrator controls. Evidence is truth. Local cheap advisor first.

## Current Step
1500 — local_model_advisor.py core

## Steps
- [x] 1499: Mainline reconciliation (PR #62 merged; main 5d4cdf4; scope→1499-1536)
- [ ] 1500-1508: local_model_advisor.py (models/config/prompt/schema/storage/client/availability/invoke/redaction)
- [ ] 1509-1511: orchestrator advisory mode + impact rules + anti-loop
- [ ] 1512-1515: CLI local-advisor status/run + catalog + run_contract
- [ ] 1516-1520: budget/usage + progress/feature/review-bundle/cockpit
- [ ] 1521-1526: tests (redaction/endpoint/parsing/impact/CLI/arch guards)
- [ ] 1527,1534: docs (local-model-advisor-v0 + updates + expensive-builder-routing-future)
- [ ] 1528: targeted tests + full pytest once
- [ ] 1529-1533: live review, readiness, PR discipline, handoff
- [ ] 1536: merge discipline — DO NOT create PR unless user explicitly asks

## Hard rules
- Local advisor OPTIONAL + DISABLED by default. Missing Ollama never breaks deterministic flow.
- Loopback only (127.0.0.1/localhost/::1); external/file:// rejected; stdlib only; no provider SDK.
- No subprocess for model exec; no shell=True; no external network; no browser; short timeout; max 1-2 retries.
- Model output never truth; never becomes next_safe_action/ProposedTask/Patch Intent/approval/apply/PR/job.
- Model may only: lower confidence, add safe missing-evidence hints, escalate weak evidence to human review.
- Final next_safe_action stays deterministic + catalog-backed + entity-backed.
- No raw prompt/response in public models. No raw source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths.
- Repeated advisor failure must not loop endlessly → loop guard.
- NO PR unless the user explicitly asks (Step 1536).

## Next block
Provider Trust Verification v1 OR Expensive Builder Routing v0.

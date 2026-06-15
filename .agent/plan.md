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
1528-1532 — full pytest recorded; live review + handoff; PR HELD

## Steps
- [x] 1499: Mainline reconciliation (PR #62 merged; main 5d4cdf4; scope→1499-1536)
- [x] 1500-1508: local_model_advisor.py (models/config/prompt/schema/storage/client/availability/invoke/redaction)
- [x] 1509-1511: orchestrator advisory mode + impact rules + anti-loop
- [x] 1512-1515: CLI local-advisor status/run + catalog + run_contract
- [x] 1516-1520: budget/usage + progress/feature/review-bundle/cockpit
- [x] 1521-1526: tests (redaction/endpoint/parsing/impact/CLI/arch guards)
- [x] 1527,1534: docs (local-model-advisor-v0 + updates + expensive-builder-routing-future)
- [x] 1528: targeted tests + full pytest once (5777+ passed)
- [x] 1529-1533: live review PASS (zero findings), readiness, PR discipline, handoff
- [x] 1536: merge discipline — PR HELD (no PR unless user explicitly asks)

## Product readiness (Step 1530)
The orchestrator can OPTIONALLY consult a local advisor (loopback Ollama; disabled by
default). Advisor critique never executes; the deterministic decision stays the controller;
a missing local advisor never blocks deterministic operation. Final next_safe_action stays
deterministic + catalog-backed. Readiness ~90% (advisory rail complete; real external builder
routing deferred). Next block: Provider Trust Verification v1 OR Expensive Builder Routing v0.

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

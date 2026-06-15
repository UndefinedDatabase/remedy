# Plan — Steps 1609-1644: Automated Local Candidate Generator Adapter v0

## Goal
First automated local candidate generator. When Builder Routing selects
`local_candidate_generator`, Remedy MAY ask an explicitly-configured local loopback model to
generate candidate output from a SAFE request package. That output IMMEDIATELY enters the
untrusted intake pipeline: quarantine → Trust Gate → Verification → Materialization → pending
approval. Disabled by default. Loopback only. No approval/apply/test/PR/git from this adapter.

## Core principle
Local model may generate candidates. The orchestrator controls. Trust + Verification judge.
Human approves. do_continue applies. Model output is UNTRUSTED — quarantined before parsing.

## Current Step
1636-1644 — code/tests/docs complete; live review + handoff; PR HELD

## Steps
- [x] 1609: mainline reconciliation (routing PR #65 merged; main 4d4d7ad; scope 1609-1644)
- [x] 1610-1611: models + config/policy (disabled default; loopback only; bounded; attempt caps)
- [x] 1612-1613: safe prompt builder (from request package) + loopback client (reuse advisor utils)
- [x] 1614-1615: private run storage + immediate intake bridge (provider label local_candidate_generator:<model>)
- [x] 1616-1617: trust+verification integration + routing gate (must select local_candidate_generator)
- [x] 1618-1619: run_contract actions + budget/usage ledger
- [x] 1620-1623: CLI status/generate + catalog + orchestrator/routing next-action
- [x] 1624-1627: progress/feature/review-bundle(26)/cockpit
- [x] 1628-1635,1642-1643: tests (20 unit + 6 CLI) + targeted + full pytest once (5887 passed)
- [x] 1634,1641: docs (generator-v0 + external-builder-sandbox-future + 5 updates)
- [x] 1636-1640: live review + readiness + PR discipline + handoff
- [x] 1644: merge discipline — NO PR unless user explicitly asks

## Product readiness (Step 1637)
Local candidate generation is now possible WHEN explicitly configured + routed: a loopback model
generates a candidate from a safe request package; ALL output passes Trust Gate + Verification
before any materialization; approval + apply remain separate (human + do_continue). Disabled by
default; missing model never breaks deterministic flow. Readiness ~85% (generation rail complete;
quality evaluation + external builder sandbox deferred). Next: Local Candidate Quality Evaluation
v1 OR External Builder Sandbox v0.

## Hard rules
- DISABLED by default; explicit opt-in; loopback only (127.0.0.1/localhost/::1); external/file:///redirects rejected.
- No cloud/provider SDK; no external network; no subprocess for model exec; no shell=True; no browser.
- Model output UNTRUSTED → quarantined before parsing → MUST pass Trust Gate + Verification before materialization.
- No candidate output creates an intent directly; no approval/apply/test/PR/git from this adapter.
- May only run if Builder Routing selected local_candidate_generator + policy/contract allow + request package + no pending intent + trust/verification available + budget + low loop risk + no open blocker/high.
- Missing local model never breaks deterministic flow.
- No raw prompt/output/source/diff/stdout/stderr/artifact-body/secrets/tracebacks/abs paths in public surfaces.
- Every next_safe_action catalog-backed + entity-backed.
- NO PR unless the user explicitly asks (Step 1644).

## Next block
External Builder Sandbox v0 OR Local Candidate Quality Evaluation v1.

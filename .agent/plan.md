# Plan — Steps 1365-1398: Provider-Agnostic Repair Request Builder v0

## Goal
Given a TestFailureArtifact, produce a SAFE, structured RepairRequestPackage that can
be handed to ANY external worker/model/human (provider-agnostic). External output
re-enters Remedy ONLY through existing `remedy provider intake-repair` → Trust Gate →
Materialization → Approval → do continue. Also define an interface-only candidate
generator adapter boundary (manual/offline only; execute() raises unavailable).

## Architecture principle
Provider-/worker-/model-/subscription-/IDE-/account-AGNOSTIC. Providers are only
EXAMPLE external untrusted candidate generators, never required infrastructure.

## Current Step
1366 — repair_request_builder.py (models + builder + storage + adapter boundary)

## Steps
- [x] 1365: Mainline reconciliation + clean branch (PR #58 merged; scope→1365-1398)
- [ ] 1366: Repair request models (Package/Section/BuildResult/StopReason/Capability/Descriptor/Record)
- [ ] 1367: Safe request package builder (from RepairContextSummary; no raw)
- [ ] 1368: Required candidate output schema (JSON or single fenced diff; one candidate)
- [ ] 1369: Request package private storage (request.md + manifest, atomic, hashed, no abs paths)
- [ ] 1370: CLI repair request (build/store; returns intake command; no apply/intent)
- [ ] 1371: CLI repair request-show (read-only)
- [ ] 1372: Command catalog (request write_metadata; request-show read_only)
- [ ] 1373: RunContract (prepare_repair_request/export_repair_request)
- [ ] 1374: Candidate generator boundary (interface only; execute raises unavailable)
- [ ] 1375: ExternalCandidateGeneratorRecord (manual|unavailable|future; no exec)
- [ ] 1376: Link request package to RepairAttempt (repair_request_prepared; idempotent)
- [ ] 1377: Import guidance (exact human next steps; no fake automation)
- [ ] 1378: Progress Ledger integration
- [ ] 1379: Feature Planner integration (no auto external execution)
- [ ] 1380: Review Bundle repair_request_summary.json
- [ ] 1381: Cockpit read-only request counts
- [ ] 1382: Prompt/request quality tests
- [ ] 1383: CLI runtime tests
- [ ] 1384: Redaction tests
- [ ] 1385: Architecture guards
- [ ] 1386: Documentation (repair-request-builder-v0 + cross-links)
- [ ] 1387: Request template pack (general/docs/test-failure/md-only)
- [ ] 1388: Request→intake E2E test (simulated external output; no real provider)
- [ ] 1389: Targeted tests + full pytest once
- [ ] 1390: Live review
- [ ] 1391: PR discipline (clean branch; NO PR unless user explicitly asks)
- [ ] 1392: Product readiness update
- [ ] 1393: Final handoff
- [ ] 1394: PR recommendation
- [ ] 1395: Hard completion criteria
- [ ] 1396: Future direct provider design note (candidate-generator-adapter-future.md)
- [ ] 1397: Provider-agnostic language audit
- [ ] 1398: Merge discipline — DO NOT create PR unless user explicitly asks

## Hard rules
- NO provider/Ollama/OpenAI/Pi/SDK/API, NO network, NO subprocess, NO browser, NO IDE/agent.
- NO apply, NO test execution, NO Patch Intent creation from request generation.
- NO direct call to provider intake inside request generation.
- Request packages SAFE to share with untrusted external actor: no raw stdout/stderr/
  source/diff/artifact-body/secrets/tracebacks/absolute private paths.
- External output re-enters ONLY via `remedy provider intake-repair`.
- Every next safe action catalog-backed + references real entities; no fake actions.
- Provider-agnostic language only (external candidate generator / untrusted output).
- Adapter execute() raises CandidateGeneratorExecutionUnavailable in v0.
- Idempotent request packages (no uncontrolled duplicates; --new to force).
- **DO NOT create a PR unless the user explicitly asks (Step 1398).**

## Next block
Provider Trust Verification v1 OR Automated Candidate Generator Adapter v0.

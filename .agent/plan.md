# Plan — Steps 1193-1219: Repair Loop v1 (Failure → Fix Patch Intent → Approval)

## Goal
Turn a real TestFailureArtifact into a bounded, safe repair PROPOSAL:
TestFailureArtifact → Repair Context → Fix Task → Repair Artifact → Fix Patch
Intent → approval_required → safe stop. No auto-apply, no auto-repair execution
beyond the proposal, no auto-contract-relax, no auto-revert.

## Current Step
1194 — Repair Loop v1 models in repair_loop.py

## Steps
- [x] 1193: Handoff reconciliation (1180-1192 full-suite proof; scope→1193-1219)
- [ ] 1194: Repair Loop v1 models (RepairAttempt/Result/ContextSummary/PatchIntentResult/StopReason)
- [ ] 1195: build_repair_context(job_id, failure_artifact_id, data_dir) safe summary
- [ ] 1196: evaluate_repair_eligibility(job_id, failure_artifact_id)
- [ ] 1197: RepairAttempt persistence (idempotent, no dup task/artifact/intent)
- [ ] 1198: Fix Task creation (idempotent, linked, Progress-visible)
- [ ] 1199: Fixture Repair Builder v1 (deterministic; else repair_builder_unavailable)
- [ ] 1200: Repair Patch Intent creation (real, resolvable, pending, approve action)
- [ ] 1201: CLI repair propose
- [ ] 1202: CLI repair status (read-only)
- [ ] 1203: Integrate repair start (alias/canonical decision + docs)
- [ ] 1204: Run Contract actions (create_fix_task/create_repair_artifact/create_repair_patch_intent)
- [ ] 1205: Event emission (safe, degradation visible)
- [ ] 1206: Progress Ledger integration
- [ ] 1207: Feature Planner integration
- [ ] 1208: Review Bundle repair_summary.json
- [ ] 1209: Proof Chain / Provenance alignment (repair intent not applied/verified)
- [ ] 1210: Operator Cockpit read-only repair counts (or defer + document)
- [ ] 1211: Idempotency tests
- [ ] 1212: CLI runtime tests (tiny repo)
- [ ] 1213: Redaction tests
- [ ] 1214: Architecture guards
- [ ] 1215: Docs (repair-loop-v1, do-continue-v1, operator-cockpit-v1)
- [ ] 1216: Targeted tests + full pytest once
- [ ] 1217: Review protocol (findings/Done/verdict)
- [ ] 1218: PR handoff prep (no PR without user OK; note branch drift)
- [ ] 1219: Final handoff

## Hard rules
- No shell=True. No background pytest. scripts/remedy_pytest.sh, targeted first,
  full suite at most ONCE after targeted pass.
- Repair Loop creates Patch Intent ONLY. No source_apply, no apply, no test exec,
  no provider/Ollama import, no auto-revert, no auto-contract-relax/budget-raise.
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths in
  events, CLI, Progress, Proof, Review Bundle, or UI payload.
- All next_safe_action commands must exist in command catalog.
- Repair intent IDs real + resolvable; idempotent (no dup task/artifact/intent);
  pending repair never marked verified.

## Next block
Approved Repair Apply Cycle (`remedy do continue <job> --intent-id <repair_intent>`)
or bounded Overnight preparation.

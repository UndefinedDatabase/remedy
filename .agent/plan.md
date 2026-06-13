# Plan — Steps 1193-1219: Repair Loop v1 (Failure → Fix Patch Intent → Approval)

## Goal
Turn a real TestFailureArtifact into a bounded, safe repair PROPOSAL:
TestFailureArtifact → Repair Context → Fix Task → Repair Artifact → Fix Patch
Intent → approval_required → safe stop. No auto-apply, no auto-repair execution
beyond the proposal, no auto-contract-relax, no auto-revert.

## Current Step
1219 — Final handoff (complete; full suite green 5420; awaiting reviewer verdict)

## Steps
- [x] 1193: Handoff reconciliation (1180-1192 full-suite proof; scope→1193-1219)
- [x] 1194: Repair Loop v1 models
- [x] 1195: build_repair_context safe summary
- [x] 1196: evaluate_repair_eligibility
- [x] 1197: RepairAttempt persistence (idempotent)
- [x] 1198: Fix Task creation (idempotent, linked)
- [x] 1199: Fixture Repair Builder v1 (deterministic; else unavailable)
- [x] 1200: Repair Patch Intent (real, resolvable, pending)
- [x] 1201: CLI repair propose
- [x] 1202: CLI repair status (read-only)
- [x] 1203: repair start v0 retained + documented (propose = canonical v1)
- [x] 1204: Run Contract repair actions
- [x] 1205: Event emission (safe, degradation visible)
- [x] 1206: Progress Ledger integration
- [x] 1207: Feature Planner integration
- [x] 1208: Review Bundle repair_summary.json v1 counts
- [x] 1209: Proof / Provenance alignment (tested)
- [x] 1210: Operator Cockpit read-only repair section
- [x] 1211: Idempotency tests
- [x] 1212: CLI runtime tests
- [x] 1213: Redaction tests
- [x] 1214: Architecture guards
- [x] 1215: Docs (repair-loop-v1 + cross-links)
- [x] 1216: Targeted + full pytest once (5420 passed)
- [x] 1217: Review protocol (handoff posted; reviewer verdict pending)
- [x] 1218: PR prep (below; no PR without user OK)
- [x] 1219: Final handoff

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

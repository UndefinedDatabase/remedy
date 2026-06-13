# Context

## Active Branch
feature/steps-1245-1274-overnight-prep (forked from clean main after PR #54
merged Approved Repair Apply Cycle v1). No drift.

## Scope
Steps 1245-1274: Bounded Overnight Preparation v0 — READ-ONLY planning/readiness/
stop-reason/morning-report layer for future bounded overnight runs. No executor,
no scheduler, no background worker, no apply/test/repair/provider execution.
Prior: 1220-1244 Approved Repair Apply Cycle v1 — merged to main in PR #54
(full suite 5432 passed, 8 skipped, 1 deselected).

## Carried residual risks (from 1193-1219)
- Fixture repair builder is docs-only by design (no source rewrite yet).
- Provider-backed source repair is future work.
- Pre-existing deselected test `test_project_brain.py::...::test_full_chain_order`
  (fails on main; always `-k "not test_full_chain_order"`).
- UI `npm run lint` pre-existing blocker (no TS parser; no deps allowed) — decisions.md.

## Bounded Overnight Prep constraints (block 1245-1274)
- READ-ONLY: no repo mutation from overnight commands (safe metadata report
  snapshot only if explicitly needed + documented). No background worker/scheduler.
- No apply/test/repair/provider execution; no auto-approve/revert/contract-relax.
- overnight_readiness must NOT import apply services, execute tests, call repair
  propose, or import provider/Ollama. No subprocess, no shell=True.
- Readiness never true from event-only proof; durable truth required; unknown
  stays unknown; stale/missing evidence → blocker/risk.
- Every suggested command must exist in the command catalog; no fake actions.
- Default BoundedOvernightPolicy: planning/report only (allow_apply/repair_apply/
  provider/revert = false, max_cycles=0). This block must NOT make overnight
  execution silently possible.

## Repair Loop v1 constraints (block 1193-1219)
- Creates a Patch Intent PROPOSAL only. No source_apply, no apply, no test execution,
  no provider/Ollama, no auto-revert, no auto-contract-relax, no auto-budget-raise.
- Apply stays separate + approval-gated (next block: do continue --intent-id).
- No raw stdout/stderr/source/diff/artifact-body/secrets/tracebacks/abs paths in any
  public surface (events/CLI/Progress/Proof/Review Bundle/UI payload).
- Repair Loop must NOT import/call source_apply or apply services or test execution.
- All next_safe_action commands must exist in the command catalog.
- Repair intent IDs real + resolvable; idempotent (no dup Fix Task / Repair Artifact /
  Repair Patch Intent); a pending repair is never marked verified.
- Fixture Repair Builder v1 is deterministic; unsupported failures → repair_builder_unavailable.

## Carried foundation
- Real Test Execution v1; failed tests create TestFailureArtifact.
- Snapshot/Revert/Proof Chain/Snapshot Truth; RunContract persisted per job.
- `remedy do continue` cycle (degraded→evidence_incomplete; failed→repair available).
- Repair Loop v0 (repair_loop.start_repair_loop_v0) — superseded by v1 propose path.

## Prior Step Status
- Steps 1045-1064: PASS — Run Contract Enforcement v1. PR #51 merged.
- Steps 1065-1084: PASS — Run Contract SSOT + Budget Ledger. PR #52 merged.
- Steps 1085-1109: PASS WITH RISKS — Real Test Execution v1.
- Steps 1110-1134: PASS WITH RISKS — Repository Snapshot / Rollback Proof v1.
- Steps 1135-1154: PASS WITH RISKS — Snapshot Trust Closure + Canonical Revert +
  Proof/Provenance/Readiness/Review snapshot integration. Independent review: PASS WITH RISKS.

## Active Constraints
- No shell=True anywhere.
- No background pytest. Use scripts/remedy_pytest.sh for Remedy's own tests.
- No destructive Git reset/checkout/clean. No force revert. No automatic revert.
- No automatic repair, no multi-cycle/overnight mode, no real provider/Ollama, no UI,
  no browser automation, no git commit gate, no MCP activation, no dependency upgrades.
- Do not weaken permission, approval, or Run Contract gates.
- Permission/approval/contract/snapshot/test gates live in central services, not only CLI.
- No raw source, diff, snapshot blob, output, secrets, or tracebacks in public surfaces.
- Continuation must be idempotent: retry after crash must not double-apply or
  double-consume test budget, nor duplicate Failure Artifact / Fix Task.
- `do --continue` performs exactly ONE controlled cycle. No autonomous loops.

## Known Risks (Carry-forward into 1155-1179) — ALL CLOSED
- R-0051: `_emit()` in test_execution_service swallowed events → CLOSED Step 1162.
- R-0057: `_emit_snapshot_event()` swallowed events → CLOSED Step 1162
  (EventPersistenceResult; emitters return structured status).
- File Provenance CLI did not pass `data_dir` → CLOSED Step 1157 (uses snapshot truth).
- Readiness event-only fallback → CLOSED Step 1159 (durable truth required).
- Review Bundle lacked `snapshot_summary.json` → CLOSED Step 1160.
- Silent ApplyRecord persistence failure in revert → CLOSED Step 1161
  (structured evidence status; degraded evidence blocks verified).
- R-0061 (no single snapshot-truth builder) → CLOSED Step 1156 + wired into
  proof/provenance/readiness/review/do-continue.
- R-0062 (no continuation cycle) → CLOSED Steps 1164-1178 (`remedy do continue`).

## Resolved (Steps 1135-1154) — removed from current risks
- R-0052/R-0053/R-0054/R-0055/R-0056: canonical revert action, gate, capability, CLI
  routing, duplicate legacy snapshots — all resolved (e738033).
- R-0058: Proof Chain snapshot requirement — resolved (Step 1145).
- R-0059: File Provenance revert state from DurableApplyRecord — resolved (Step 1146,
  helper level; CLI wiring carried forward to Step 1157).
- R-0060: Readiness snapshot/apply_record verification — resolved (Step 1150, helper
  level; event fallback hardening carried forward to Step 1159).

## Foundation
- RepositorySnapshot / DurableApplyRecord — durable, verified recovery material.
- create_snapshot + verify_snapshot — block apply on failure.
- revert_repository_apply() — 8-gate explicit revert service (permission + contract).
- ContractAction.REVERT + Capability.repo_revert — canonical, denied by default.
- Test Execution Service — real pytest via scripts/remedy_pytest.sh, budget-gated.
- RunContract + RunUsage persisted per job.

## Next Block (after 1155-1179)
Repair Loop v1 or bounded Overnight Mode preparation.

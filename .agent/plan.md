# Plan — Steps 1135-1154: Snapshot Trust Closure + Canonical Revert

## Goal
Close all remaining snapshot/revert trust gaps.
Enforce canonical RunContract REVERT action and Capability.repo_revert at the service boundary.
Route CLI patch.revert through the durable service, not the legacy path.
Integrate Proof Chain, File Provenance, and Readiness with snapshot verification.

## Current Step
1154 — Final handoff

## Steps
- [x] 1135: Reconcile handoff — context.md, plan.md, live_review.md
- [x] 1136: Canonical revert action — ContractAction.REVERT in run_contract.py
- [x] 1137: Canonical revert gate — remove permitted=True / contract_allows_revert=True from revert_repository_apply()
- [x] 1138: Capability.repo_revert — add with default deny, active enforcement
- [x] 1139: Route patch.revert CLI through durable service; apply_id canonical, intent_id fallback
- [x] 1140: Update source_apply.revert_apply() to return full RepositoryRevertResult
- [x] 1141: Remove store_pre_apply_snapshot() legacy call from patch_apply.py (close R-0052/R-0056)
- [x] 1142: Legacy revert migration — old jobs with patch_revert.py snapshots only (DEFERRED)
- [x] 1143: Close R-0051 — structured event persistence status in test_execution_service (DEFERRED)
- [x] 1144: Canonical apply/revert state model (DEFERRED)
- [x] 1145: Proof Chain snapshot integration (close R-0058)
- [x] 1146: File Provenance revert state from DurableApplyRecord (close R-0059)
- [x] 1147: Progress Ledger snapshot integration
- [x] 1148: Feature Planner snapshot integration
- [x] 1149: Review Bundle snapshot integration (no recovery blobs in public surfaces)
- [x] 1150: Readiness — require verified RepositorySnapshot + DurableApplyRecord (close R-0060)
- [x] 1151: Snapshot/revert CLI runtime tests (subprocess)
- [x] 1152: Architecture guards
- [x] 1153: Tests + updated docs
- [x] 1154: Final handoff — changed files table

## Known Risks
- R-0051: _emit() in test_execution_service swallows events (Step 1143)
- R-0052: Duplicate legacy snapshots in patch_apply.py (Step 1141)
- R-0053: Legacy patch.revert routing (Step 1139)
- R-0054: Bypass booleans in revert_repository_apply() (Step 1137)
- R-0055: REVERT action absent from contract (Step 1136)
- R-0056: Duplicate legacy snapshots (Step 1141)
- R-0057: Silent event emission failure (Step 1143)
- R-0058: Proof Chain no snapshot requirement (Step 1145)
- R-0059: File Provenance stale revert state (Step 1146)
- R-0060: Readiness no snapshot verification (Step 1150)
- Pre-existing: test_project_brain.py::test_full_chain_order fails on main

# Context

## Active Branch
feature/steps-1110-1134-snapshot-rollback-v1

## Scope
Steps 1135-1154: Snapshot Trust Closure + Canonical Revert

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1044: PASS — Safety Closure, Progress Ledger, Feature Planner, Integrity Gate.
- Steps 1045-1064: PASS — R-0017 fix + Run Contract Enforcement v1. PR #51 merged.
- Steps 1065-1084: PASS — Run Contract SSOT + Budget Ledger. PR #52 merged.
- Steps 1085-1109: PASS WITH RISKS — Real Test Execution v1. Branch committed, PR pending.
- Steps 1110-1129: PASS — Evidence durability, Repository Snapshot Service v1, CLI commands.
- Steps 1130-1132: DEFERRED — Proof Chain / Provenance / Readiness snapshot integration.
- Steps 1133-1134: PASS — Tests, documentation, final handoff.

## Active Constraints
- No shell=True anywhere.
- No background pytest. Use scripts/remedy_pytest.sh for Remedy's own tests.
- No destructive Git reset/checkout/clean.
- No force revert.
- No automatic revert.
- Do not weaken permission, approval, or Run Contract gates.
- No raw snapshot blobs, source, diffs, output, secrets, or tracebacks in public surfaces.
- Snapshot contents are private recovery material only.
- No automatic apply in this block.

## Known Risks (Carry-forward)
- R-0051: `_emit()` in test_execution_service swallows events with `except Exception: pass`.
- R-0052: Legacy `store_pre_apply_snapshot()` call in patch_apply.py — fix Step 1141.
- R-0053: `patch.revert` CLI routes through legacy `revert_patch_intent()` — fix Step 1139.
- R-0054: `revert_repository_apply()` takes `permitted=True` and `contract_allows_revert=True` — fix Step 1137.
- R-0055: `ContractAction.REVERT` absent from canonical vocabulary — fix Step 1136.
- R-0056: `patch_apply.py` writes duplicate legacy snapshots — fix Step 1141.
- R-0057: Snapshot event persistence silently ignored — Step 1143.
- R-0058: Proof Chain has no verified snapshot requirement — Step 1145.
- R-0059: File Provenance doesn't track revert state from RepositorySnapshot — Step 1146.
- R-0060: Readiness has no snapshot/apply_record verification — Step 1150.
- Pre-existing: `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Foundation
- RunContract persisted per job (ensure_contract, save_contract, load_contract)
- RunUsage persisted per job (load_usage, save_usage, check_budget)
- evaluate_run_action(contract, action, usage=usage) enforces budgets
- repo_test_run Capability in permissions
- RepositorySnapshot / DurableApplyRecord — mandatory, verified, durable
- create_snapshot + verify_snapshot — block apply on failure
- revert_repository_apply() — 8-gate explicit revert service
- patch_apply.py — mandatory new-style snapshot before any apply
- source_apply.py — transactional rollback via durable blobs
- snapshot CLI: remedy snapshot inspect, remedy snapshot list-applies

## Active Truth Gaps (Steps 1135-1154)
1. revert_repository_apply() uses caller-supplied permitted=True booleans — bypass risk (Step 1137).
2. ContractAction.REVERT not in canonical vocabulary — cannot enforce (Step 1136).
3. Capability.repo_revert missing — no permission gate at runtime (Step 1138).
4. patch.revert CLI routes through legacy revert_patch_intent() (Step 1139).
5. patch_apply.py still writes duplicate legacy snapshots (Step 1141).
6. Proof Chain, File Provenance, Readiness not snapshot-integrated (Steps 1145-1150).

## Next Block
remedy do --continue — Steps 1135-1154: Snapshot Trust Closure + Canonical Revert.

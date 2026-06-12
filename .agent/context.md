# Context

## Active Branch
feature/steps-1155-1179-do-continue-v1

## Scope
Steps 1155-1179: Snapshot Truth Final Closure + `remedy do --continue` v1.

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

## Known Risks (Carry-forward into 1155-1179)
- R-0051: `_emit()` in test_execution_service swallows events with `except Exception: pass`
  → closed by Step 1162 (EventPersistenceResult).
- R-0057: `_emit_snapshot_event()` in repository_snapshot.py swallows events
  → closed by Step 1162.
- File Provenance CLI (`apps/cli/commands/file.py`) does not pass `data_dir` to
  `build_file_provenance()` → not using authoritative DurableApplyRecord → Step 1157.
- Readiness `_has_verified_snapshot()` falls back to `snapshot_create_completed` event
  → generic event is not rollback proof → Step 1159.
- Review Bundle lacks `snapshot_summary.json` → Step 1160.
- Silent ApplyRecord persistence failure in revert service
  (`except (OSError, json.JSONDecodeError): pass`) → Step 1161.

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

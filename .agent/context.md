# Context

## Active Branch
feature/steps-1110-1134-snapshot-rollback-v1

## Scope
Steps 1110-1134: Test Evidence Durability + Snapshot / Rollback Proof v1

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1044: PASS — Safety Closure, Progress Ledger, Feature Planner, Integrity Gate.
- Steps 1045-1064: PASS — R-0017 fix + Run Contract Enforcement v1. PR #51 merged.
- Steps 1065-1084: PASS — Run Contract SSOT + Budget Ledger. PR #52 merged.
- Steps 1085-1109: PASS WITH RISKS — Real Test Execution v1. Branch committed, PR pending.

## Active Constraints
- No shell=True anywhere.
- No capture_output=True in production test runner path.
- No background pytest. Use scripts/remedy_pytest.sh for Remedy's own tests.
- No .env loading or secret-bearing environment inheritance.
- No raw stdout/stderr/source/diff/artifact body in JSON, events, Job metadata, Brain, Proof Chain, Review Bundle, Failure Artifact, CLI output.
- Production test subprocesses must use argv lists only.
- No repository mutation by Test Execution Service.
- No process kill of unrelated jobs.
- No automatic revert without explicit caller action.
- Snapshot contents are private recovery material only.
- No automatic apply in this block.
- No destructive Git reset/checkout/clean.

## Known Risks (Carry-forward)
- R-0038: Silent exception swallowing in `_persist_test_record()` and `_create_failure_artifact()` — fix in Steps 1115-1116.
- R-0041: `test.status` command emitted as next_safe_action but does not exist in catalog — fix in Step 1111.
- R-0042: Test lease is job-scoped only; two jobs on same repo can run tests concurrently — fix in Step 1112.
- R-0043: Partial evidence persistence: usage consumed without durable test record or artifact — fix in Steps 1114-1116.
- Pre-existing: `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.

## Foundation
- RunContract persisted per job (ensure_contract, save_contract, load_contract)
- RunUsage persisted per job (load_usage, save_usage, check_budget)
- evaluate_run_action(contract, action, usage=usage) enforces budgets
- repo_test_run Capability in permissions
- TestRunRecord, TestFailureArtifact models exist
- test_execution_service.py: execute_test_run() with 13 gates
- patch_revert.py: store_pre_apply_snapshot() — best-effort, does not block apply
- source_apply.py: in-memory FileSnapshot objects — not durable
- patch_apply.py: calls store_pre_apply_snapshot() with broad except: pass
- command_discovery.py — safe candidate selection
- _EXECUTION_SAFE_EXECUTABLES — executable allowlist

## Active Truth Gaps
1. `remedy test status <job_id>` emitted but not in command catalog (Step 1111).
2. Lease is per-job; two jobs on same repo can race (Step 1112).
3. No `test_run_started` event after Popen success (Step 1113).
4. `_persist_test_record` + `_create_failure_artifact` swallow all exceptions silently (Steps 1114-1116).
5. No atomic finalization: usage/record/event/artifact in separate saves (Step 1116).
6. Snapshots are in-memory or best-effort only; no durable verified recovery material (Steps 1118-1127).

## Next Block
remedy do --continue — Approved Apply → Test → Proof, using mandatory snapshots.

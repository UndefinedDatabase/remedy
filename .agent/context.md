# Context

## Active Branch
feature/steps-1877-1916-real-test-execution-snapshot-rollback-proof-v1 (forked from clean main at
aacafbd after PR #72 merged Overnight Mission Contract + Review/Repair Spine v0). No drift.

## Mainline reconciliation (Step 1877)
- PR #72 MERGED → main (auto-merge on reviewer PASS). Current main commit: aacafbd. Overnight Mission
  v0 reviewer verdict PASS @ 90768fd (R-0102/R-0103 resolved).
- Overnight Mission Contract + Review/Repair Spine v0 (1837-1876) landed: overnight_mission.py
  (contract/cycle/evaluation; evidence-only satisfaction; review-as-blocker; honest readiness).
  `remedy overnight contract-create/show/evaluate/next-action/cycles/contract-readiness/integrity`.
- Carried risks reconciled below. No feature code before mainline closure.

## Scope
Steps 1877-1916: Real Test Execution + Snapshot/Rollback Proof v1 — the first safe execution gate for
Overnight Mode. Remedy can run ALLOWED test commands through the existing bounded safe runner; results
become durable evidence; failing tests become safe Test Failure Artifacts; Snapshot Proof records an
honest snapshot point and Rollback Proof records whether a real restore is available (honest, no
overclaim). The Mission Contract consumes test/snapshot/rollback gates.

## Core principle
Workers execute. Remedy governs. Tests + rollback proof become durable gates. Bounded, command-
discovered, policy-gated, evidence-backed — never uncontrolled automation. No fake test pass; a
metadata snapshot is NOT a rollback restore; restore_available stays false unless a real restore path
exists; raw stdout/stderr stays private.

## Reused existing infra (DO NOT reinvent)
- test_execution_service.execute_test_run (the SINGLE safe entry point: contract-gated, lease, safe
  env, isolated process group, timeout, output cap + truncation, failure-artifact creation, no
  shell=True, no raw output returned). `remedy test run` already routes through it.
- test_runner.run_tests_local (argv list only, no shell); command_discovery.discover_commands +
  select_best_test_candidate (CommandCandidate.argv_list()).
- repository_snapshot.create_snapshot / build_snapshot_truth (apply-scoped recovery truth).
- test_failure_artifact.build_test_failure_artifact / persist / create_fix_task_from_failure.
- proof_chain.build_proof_chain; overnight_mission gates; progress_ledger/feature_planner/
  review_bundle/ui_server; run_contract; provider_trust scrub helpers.
This block adds real_test_execution.py as a SAFE FACADE + honest SnapshotProof/RollbackProof + mission
gate consumption + read CLI + integrity + docs. It does NOT re-implement subprocess execution.

## Carried residual risks
- Real rollback RESTORE is NOT implemented in v1 — Snapshot/Rollback Proof are honest metadata:
  restore_available is false unless apply-scoped recovery material is verified; restore_tested false.
- Worker/provider/Claude/Pi/OpenCode/Ollama/cloud EXECUTION still not built.
- MemPalace / durable memory / embeddings NOT built.
- Token/cost estimated bands; tournament evidence shared-route granularity.
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser blocker. Full-suite run occasionally infra-fragile (OOM).

## Block constraints (1877-1916)
- Subprocess allowed ONLY inside the approved bounded test runner path (execute_test_run/run_tests_
  local). NO shell=True, NO arbitrary command strings, NO destructive/network/install/git-write
  commands. Commands must be allowlisted/discovered.
- NO provider/model/Claude/Pi/OpenCode/Ollama/cloud/local execution; NO worker execution; NO auto-
  apply/approve; NO autonomous repair execution; NO auto-PR/git; NO MemPalace/embeddings/vector DB;
  NO UI redesign; NO MCP.
- Raw stdout/stderr private (output_ref only); public surfaces safe summaries; no secrets/abs paths.
- No fake test pass; metadata snapshot ≠ rollback restore; no fake restore_available/restore_tested.
- next_safe_action catalog-backed. NO PR unless asked (auto-merge on reviewer PASS).

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh`; full suite once at block end with
  `-k "not test_full_chain_order"`. CLI runtime tests use the approved runner only.

## Changed files (Steps 1877-1916) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/real_test_execution.py | NEW safe facade: TestRunRequest/Result + SnapshotProof + RollbackProof models; resolve_allowed_command (discovered test cmd only; blocks shell-meta/destructive); run_allowed_test (wraps execute_test_run; honest pass); create_snapshot_proof (metadata-only, restore_available=False); create_rollback_proof (honest; restore via build_snapshot_truth only); list/get; audit + test_execution_integrity | bounded execution + honest proofs |
| packages/orchestration/run_contract.py | TEST_RESULT_SHOW + SNAPSHOT/ROLLBACK proof actions (non-exec; execution stays on RUN_TEST) | contract gate |
| apps/cli/commands/real_test_execution_cmd.py | NEW handlers: test result/list/integrity, snapshot create/show, rollback proof/show | CLI surface |
| apps/cli/commands/__init__.py | register real_test_execution_cmd | wire handlers |
| apps/cli/command_catalog.py | rollback group + test.result/list/integrity, snapshot.create/show, rollback.proof/show (read_only/write_metadata; no may_execute) | catalog-backed |
| packages/orchestration/overnight_mission.py | gate consumption: tests_green from real latest pass; snapshot_recorded + rollback_restore_available gates (GATE_ROLLBACK_RESTORE) | mission consumes real gates |
| packages/orchestration/progress_ledger.py | extract/merge_real_test_execution_items + build wiring | surface test/snapshot/rollback honestly |
| packages/orchestration/feature_planner.py | item-id driven real-test suggestions (repair from failure; implement real rollback) | evidence-based |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 32→33 + _build_snapshot_rollback_summary | safe bundle summary |
| packages/orchestration/ui_server.py | _build_test_execution_section + _build_snapshot_rollback_section cockpit (live=false) | read-only cockpit |
| tests/orchestration/test_real_test_execution.py | NEW 21 tests (models/command-resolution/proofs/integrity/mission-gates/arch) | coverage |
| tests/cli/test_real_test_execution_cli.py | NEW 6 subprocess tests | CLI runtime |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==33 + snapshot_rollback assert | bundle test |
| tests/orchestration/test_autonomy.py | inverted stale `remedy test list` guard → now asserts it is a valid catalog command | test.list is now real |
| docs/real-test-execution-snapshot-rollback-proof-v1.md, docs/real-test-execution-snapshot-rollback-user-guide-v1.md | NEW architecture + user docs | document + honesty |
| .agent/context.md, .agent/plan.md | reconciliation + changed-files table | handoff |

## Status
Steps 1877-1916 builder work COMPLETE. Full pytest 6235 passed, 8 skipped, 1 deselected (exit 0).
test execution integrity passed. Parallel reviewer owns the live_review verdict (PENDING at handoff).
Reviewer findings start at R-0104. Auto-merge on reviewer PASS (honor hard gate; operator may override).

## Next block
Repair Loop v1/v2: Failure Artifact → Fix Candidate → Review → Re-Test (only after this block PASS).

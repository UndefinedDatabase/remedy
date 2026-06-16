# Plan — Steps 1877-1916: Real Test Execution + Snapshot/Rollback Proof v1

## Goal
First safe execution gate for Overnight Mode. Run ALLOWED test commands through the existing bounded
safe runner; results become durable evidence; failing tests → safe failure artifacts; Snapshot Proof
+ Rollback Proof record honestly whether a real restore exists. Mission Contract consumes the gates.

## Core principle
Workers execute. Remedy governs. Bounded, command-discovered, policy-gated, evidence-backed. No fake
pass; metadata snapshot ≠ rollback restore; raw output stays private. Reuse existing safe runner +
snapshot infra — do not reinvent subprocess execution.

## Current Step
1899-1916 — R-0104 closure (command_id forwarded into runner; reported == executed). Done; awaiting
reviewer re-verdict.

## Steps
- [x] 1877: mainline closure (PR #72 → main aacafbd; fresh branch) + carried risks
- [x] 1878: architecture doc (real-test-execution-snapshot-rollback-proof-v1.md)
- [x] 1879-1885: real_test_execution.py facade (TestRunRequest/Result + allowed-command resolution +
      run_allowed_test wrapping execute_test_run + SnapshotProof + RollbackProof + storage + integrity)
- [x] 1886: overnight_mission gate consumption (tests_green from real pass; snapshot_recorded vs
      rollback_restore_available)
- [x] 1887-1888: CLI (test result/list, snapshot create/show, rollback proof/show, test integrity) +
      catalog + run_contract (controlled_test_execution; no arbitrary exec)
- [x] 1889-1893: progress_ledger + feature_planner + review_bundle + ui_server cockpit + integrity
- [x] 1894: user-facing doc
- [x] 1895-1896: arch guards + targeted suites
- [x] 1897: full suite once (6235 passed @ cb2c640)
- [x] 1898: final handoff
- [x] 1899-1916: R-0104 closure — `command_id` threaded into `execute_test_run` Gate 8; executed
      candidate id reported (`TestExecutionResult.command_id`) + persisted; `run_allowed_test` forwards
      and reports the executed id; blocks `requested_command_not_found`/`requested_command_not_test`.
      Tests added (runner + facade); targeted 249 passed; integrity PASS. Awaiting reviewer re-verdict.

## Hard rules
- Subprocess ONLY via the approved runner (execute_test_run/run_tests_local). No shell=True, no
  arbitrary/destructive/network/install/git-write commands; commands allowlisted/discovered.
- No provider/model/Ollama/worker execution; no auto-apply/approve/repair/PR/git; no MemPalace/
  embeddings; no UI redesign; no MCP.
- Raw output private; public summaries safe. No fake pass; metadata snapshot ≠ rollback restore; no
  fake restore_available/restore_tested. next_safe_action catalog-backed.
- Tests via scripts/remedy_pytest.sh; full once. NO PR unless asked (auto-merge on reviewer PASS).

## Next block
Repair Loop v1/v2: Failure Artifact → Fix Candidate → Review → Re-Test (only after this block PASS).

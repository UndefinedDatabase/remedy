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
1877 — mainline reconciliation done (PR #72 merged → main aacafbd; fresh branch). Building facade.

## Steps
- [x] 1877: mainline closure (PR #72 → main aacafbd; fresh branch) + carried risks
- [ ] 1878: architecture doc (real-test-execution-snapshot-rollback-proof-v1.md)
- [ ] 1879-1885: real_test_execution.py facade (TestRunRequest/Result + allowed-command resolution +
      run_allowed_test wrapping execute_test_run + SnapshotProof + RollbackProof + storage + integrity)
- [ ] 1886: overnight_mission gate consumption (tests_green from real pass; snapshot_recorded vs
      rollback_restore_available)
- [ ] 1887-1888: CLI (test result/list, snapshot create/show, rollback proof/show, test integrity) +
      catalog + run_contract (controlled_test_execution; no arbitrary exec)
- [ ] 1889-1893: progress_ledger + feature_planner + review_bundle + ui_server cockpit + integrity
- [ ] 1894: user-facing doc
- [ ] 1895-1896: arch guards + targeted suites
- [ ] 1897: full suite once
- [ ] 1898: final handoff (+ auto-merge on reviewer PASS)
- [ ] 1899-1916: reserved for reviewer findings (R-0104+)

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

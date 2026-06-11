# Context

## Active Branch
feature/steps-1085-1109-real-test-execution-v1

## Scope
Steps 1085-1109: Real Test Execution v1 — Contract-Gated and Resource-Safe

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1044: PASS — Safety Closure, Progress Ledger, Feature Planner, Integrity Gate.
- Steps 1045-1064: PASS — R-0017 fix + Run Contract Enforcement v1. PR #51 merged.
- Steps 1065-1084: PASS — Run Contract SSOT + Budget Ledger. PR #52 merged.

## Active Constraints
- No shell=True anywhere.
- No capture_output=True in production test runner path.
- No background pytest. Use scripts/remedy_pytest.sh for Remedy's own tests.
- No .env loading or secret-bearing environment inheritance.
- No raw stdout/stderr in JSON, events, Job metadata, Brain, Proof Chain, Review Bundle, Failure Artifact.
- Production test subprocesses must use argv lists only.
- No repository mutation by Test Execution Service.
- No process kill of unrelated jobs.

## Known Risks
- `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` pre-existing fail on main.
- R-0027: `high_risk_command_execution` not in canonical actions — fix in Step 1086.

## Foundation
- RunContract persisted per job (ensure_contract, save_contract, load_contract)
- RunUsage persisted per job (load_usage, save_usage, check_budget)
- evaluate_run_action(contract, action, usage=usage) enforces budgets
- repo_test_run Capability exists in permissions
- TestRunRecord, TestFailureArtifact models exist
- run_tests_local() in test_runner.py — needs process isolation upgrade
- command_discovery.py — safe candidate selection

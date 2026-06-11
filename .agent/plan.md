# Plan — Steps 1085-1109: Real Test Execution v1

## Goal
Central, contract-gated Test Execution Service. Permission + contract + budget + lease + process isolation + failure artifact + linkage.

## Current Step
1098 — Link tests to changes

## Steps
- [x] 1085: Reconcile previous handoff — agent files, R-0027/R-0028 status
- [x] 1086: Fix R-0027 (high_risk_command_execution), confirm R-0028 resolved, tests
- [x] 1087: Default test policy — run_test in allowed, max_test_runs=0, dual-gate tests
- [x] 1088: Create test_execution_service.py — models only
- [x] 1089: Centralize all gates — execute_test_run() gate order
- [x] 1090: Production process isolation — Popen, start_new_session, SIGTERM/SIGKILL
- [x] 1091: Safe environment policy — strip secrets, preserve PATH
- [x] 1092: Test execution lease — concurrent-run guard
- [x] 1093: Derive timeout from contract remaining runtime
- [x] 1094: Persist usage correctly — test_runs_used, runtime_seconds_used
- [x] 1095: Persist safe test records — TestRunRecord v2 with contract_id + linkage
- [x] 1096: Emit safe lifecycle events
- [x] 1097: Automatic TestFailureArtifact on fail/timeout
- [ ] 1098: Link tests to changes — task/intent/apply validation
- [ ] 1099: Update remedy test run CLI — route through service
- [ ] 1100: Contract guidance — next safe action per block reason
- [ ] 1101: Proof Chain alignment — pass/fail/timeout/unlinked rules
- [ ] 1102: Progress, Feature Planner, Review Bundle integration
- [ ] 1103: Resource and redaction tests
- [ ] 1104: Runtime CLI tests — subprocess tests only
- [ ] 1105: Command discovery truth — safety and risk guardrails
- [ ] 1106: Architecture guards — service not CLI-only
- [ ] 1107: Documentation — real-test-execution-v1.md
- [ ] 1108: Tests and live review
- [ ] 1109: Final handoff

## Known Risks
- R-0027: high_risk_command_execution not canonical — fix in 1086
- pre-existing: test_project_brain.py::test_full_chain_order fails on main

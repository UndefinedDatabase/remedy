# Context

## Active Branch
feature/steps-1065-1084-run-contract-ssot

## Scope
Steps 1065-1084: Run Contract Single Source of Truth + Budget Ledger

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1044: PASS — Safety Closure, Progress Ledger, Feature Planner, Integrity Gate.
- Steps 1045-1064: PASS — R-0017 fix + Run Contract Enforcement v1. PR #51 merged.

## Known Risks
- `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main (pre-existing).
- R-0017: RESOLVED in Steps 1045-1064.
- R-0018: RESOLVED — evaluate_run_action() added.
- R-0019: RESOLVED — repair_loop contract enforcement added.
- R-0020: RESOLVED — do_run contract checks before phases.

## Truth Gaps (from handoff)
1. Contract not persisted — `build_default_run_contract()` rebuilds each time.
2. `_check_do_contract` copies only subset of fields, drops max_test_runs, paths, risk, no_cloud.
3. repair_loop creates private contract instead of loading job's persisted contract.
4. CLI rebuilds fresh contract instead of loading persisted.
5. `_check_path_policy` uses broad `startswith` — `.env` blocks `.environment.py`.
6. No usage ledger (loops, tests, runtime, tokens, cost).
7. No canonical action vocabulary (strings scattered).

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.

# Context

## Active Branch
feature/steps-1045-1064-run-contract-v1

## Scope
Steps 1045-1064: Integrity Gate Truth Closure + Run Contract Enforcement v1

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1009: PASS — Review Bundle Safety Closure.
- Steps 1010-1029: PASS WITH RISKS — Progress Ledger + Feature Planner done, R-0013/R-0014 resolved.
- Steps 1030-1044: PASS WITH RISKS — Integrity Gate + Review Zip Closure done. R-0017 medium open.

## Known Risks
- `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main (pre-existing).
- R-0017: ctx_says_complete heuristic too loose — matches "done"/"complete" in prior block text, causing false positives. Fix target: Step 1046.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.

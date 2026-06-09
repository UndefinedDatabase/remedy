# Context

## Active Branch
feature/steps-975-994-review-bundle-v1

## Scope
Steps 1030-1044: Integrity Gate + Review Zip Closure — COMPLETE

## Prior Step Status
- Steps 940-974: PASS — Repair Loop v0 + Truth Closure.
- Steps 975-994: PASS — Review Bundle v1 + R-0006 closure.
- Steps 995-1009: PASS — Review Bundle Safety Closure.
- Steps 1010-1029: PASS WITH RISKS — Progress Ledger + Feature Planner done, R-0013/R-0014 resolved.
- Steps 1030-1044: PASS WITH RISKS — Integrity Gate + Review Zip Closure done. R-0017 medium open (known risk).

## Known Risks
- `test_project_brain.py::TestFileProvenanceChain::test_full_chain_order` fails on main.
- R-0017: ctx_says_complete heuristic too loose — matches "done" in text, causing false positives.

## Resource Safety
Use `scripts/remedy_pytest.sh`. No direct pytest, no background pytest, no `shell=True`.

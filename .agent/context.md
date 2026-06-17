# Context

## Active Branch
feature/steps-2446-2505-closure-r0135-r0140
(forked from main at d1558e6 after PR #83 merged).

## Scope
Steps 2446-2505 Final Closure: Fix 6 review findings R-0141..R-0146 from FAIL @ 7e76f56.

## Modified files (this commit)
| File | Change |
|------|--------|
| packages/orchestration/progress_ledger.py | R-0141: _redact_ledger_text scrubs title/next_action/safe_summary in export |
| packages/orchestration/self_repair_proposal.py | R-0142: _SECRET_RE extended for token/credential; R-0143: convert revalidates criteria/tests; R-0145: dedup evidence appends |
| tests/orchestration/test_self_repair_proposal.py | R-0142: 6 token/credential tests; R-0143: 2 convert-no-criteria/tests tests; R-0145: uniqueness test |
| tests/cli/test_self_repair_cmd.py | R-0143: worker-prompt fixture includes acceptance_criteria + required_tests |
| .agent/plan.md | Updated for final closure |
| .agent/context.md | Updated for final closure |

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

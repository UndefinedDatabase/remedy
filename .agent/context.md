# Context

## Active Branch
feature/steps-2446-2505-closure-r0135-r0140
(forked from main at d1558e6 after PR #83 merged).

## Scope
Steps 2446-2505 Closure: Fix 6 review findings R-0135..R-0140.

## Modified files
| File | Change |
|------|--------|
| packages/orchestration/self_repair_proposal.py | R-0135: approval gates, R-0136: secret scrubbing, R-0137: signal diagnostics |
| packages/orchestration/progress_ledger.py | R-0138: extract/merge self-repair items + wired into build_progress_ledger |
| tests/orchestration/test_self_repair_proposal.py | Updated + new tests: 49→68 (approval gates, secret scrubbing, signal diagnostics) |
| tests/cli/test_self_repair_cmd.py | NEW: 12 subprocess CLI tests for all 7 commands |
| .agent/plan.md | Updated for closure block |
| .agent/context.md | Updated for closure block |

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

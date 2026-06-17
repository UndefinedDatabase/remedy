# Context

## Active Branch
feature/steps-2446-2505-run-replay-to-self-repair-proposal-v0
(forked from clean main at e83f842 after PR #82 merged).

## Scope
Steps 2446-2505: Run Replay to Self-Repair Proposal v0.

## Modified files
| File | Change |
|------|--------|
| packages/orchestration/self_repair_proposal.py | NEW: Core module — model, storage, generation, decisions, integrity, export |
| apps/cli/commands/self_repair_cmd.py | NEW: 7 CLI handlers |
| apps/cli/commands/__init__.py | Register self_repair_cmd module |
| apps/cli/command_catalog.py | Add self-repair group + 7 command entries |
| packages/orchestration/run_contract.py | Add 7 self-repair contract actions |
| packages/orchestration/review_bundle.py | Add self_repair_proposal_summary.json section, REQUIRED_SECTIONS 40→41 |
| tests/orchestration/test_self_repair_proposal.py | NEW: 49 tests |
| tests/orchestration/test_review_bundle.py | Update REQUIRED_SECTIONS count to 41 |
| docs/run-replay-to-self-repair-proposal-v0.md | NEW: Architecture doc |
| docs/self-repair-proposal-user-guide-v0.md | NEW: User guide |
| .agent/plan.md | Updated for this block |
| .agent/context.md | Updated for this block |

## 30-task backlog
- Strict completed: 6/30
- Next: README Current-State Refresh v1 OR Async/Sync Contract Alignment v0

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

## Status
Implementation complete. All tests pass. Ready for commit.

# Context

## Active Branch
feature/steps-2506-2585-controlled-claude-code-operator-path-v0
(forked from main at 374482b after PR #84 merged).

## Scope
Steps 2506-2585: Controlled Claude Code Operator Path v0.
Template enable/disable/update CLI, package-bound placeholder resolution,
operator runbook, claude doctor, fixture end-to-end, docs, progress visibility.

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

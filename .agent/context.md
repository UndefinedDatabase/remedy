# Context

## Active Branch
feature/steps-2586-2615-mission-run-loop-morning-report-v0
(forked from main at df2525c after PR #85 merged).

## Scope
Steps 2586-2615: Bounded mission run loop, morning report,
terminology guidance, stale doc fixes, core readiness summary,
loop checkpoint safety, self-repair/builder/execution visibility.

## Key findings from Step 2587 audit
- step_dogfood_run() exists — does one safe evaluation step
- evaluate_dogfood_run() exists — gathers evidence, determines lane/action
- Missing: multi-step bounded loop (run_mission_loop)
- Missing: morning report model + builder
- Doc bug: controlled-claude-code-operator-path-v0.md uses --adapter, actual CLI is --adapter-id
- Existing DogfoodRunStatus already has all required terminal states

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Carry-forward findings from previous block
- R-0148 (LOW): No CLI subprocess tests for 5 new commands (PR #85)
- R-0149 (LOW): Context.md missing Changed Line Map table (PR #85)

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

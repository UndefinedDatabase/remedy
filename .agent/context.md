# Context

## Active Branch
feature/steps-2616-2655-worker-onboarding-mission-facade-v0
(forked from main at 8b7abb5 after PR #86 merged).

## Scope
Steps 2616-2655: Worker onboarding facade (add/doctor/disable),
mission command facade (run/report), alias registry, stale doc fixes.

## Reviewer findings to fix (carry-forward)
- R-0151 (MEDIUM): _build_self_repair_summary() used wrong status values
  ("proposed"/"ready" → "awaiting_operator"/"edited"). FIXED in this branch.
- R-0152 (LOW): inspect_command wrong CLI group
  ("remedy self" → "remedy self-repair"). FIXED in this branch.
- R-0153 (LOW): CLM table missing in context.md. Carry-forward pattern.

## Key architectural decisions
- Worker alias registry maps "claude" → adapter claude-code-v0 + template claude-code-repair-v0
- "mission" group is new; "worker" group exists
- Facades call existing safe functions, no new business logic
- Step 2623 (worker readiness): skip — doctor already covers it
- Step 2626 (mission status): skip — mission report already covers it

## Pre-existing test failures (not introduced by this change)
- tests/cli/test_self_dogfood_execution_cli.py (2 failures on main)
- tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order

## Resource safety
All pytest runs use scripts/remedy_pytest.sh (flock-serialized, timeout-bounded).
No shell=True. No background pytest.

# Context — amend1016p (simple orders stay simple)

## Active Branch
feature/simple-orders-fast-lane, in the worktree .remedy-wt/simple-orders. The supervisor runs main
from the main checkout, and each new order starts `python -m apps.cli.main` from it, so a merge
changes what the next order runs: merged only on decodeux's word.

## Scope
The lane decision on deliverables, the full lane's constraint-only milestones and checking-only
tasks, the Pi reviewer's meaning check, tests and docs. No planner redesign, no provider default.

## Do not touch
`.agent/STOP` (untracked), F078 and the autonomous queue, the sandbox, the public API contract.

## Constraints
- Resource safety: one pytest run at a time through `scripts/remedy_pytest.sh`; no full-suite rerun.
- Structure ratchet: `compile_mission_plan` (101 lines) may not grow. Commits at most 500 insertions.

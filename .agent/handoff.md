# Handoff — F014 Flight Plan

## State
- Branch: `feature/f014-flight-plan`
- Last commit: `7cb1636` feat(f014): approval gate + label flip + smoke (T004)
- Total commits on branch: 5
- PR: https://github.com/UndefinedDatabase/remedy/pull/148

## Changed Files

| File | Change |
|------|--------|
| packages/orchestration/schemas/models.py | FlightPlan schema + DAG validator |
| packages/orchestration/planner_models.py | Deprecation notes |
| packages/orchestration/flight_plan.py | NEW: plan_job_llm, task mapping, budget/fence, render, replan |
| packages/core/models.py | flight_plan field on Job |
| packages/orchestration/decision_queue.py | flight_plan_approval type + derivation |
| apps/cli/commands/do_cmd.py | Wire flight plan into golden path, label flip |
| tests/schemas/test_flight_plan_schema.py | NEW: 23 schema tests |
| tests/orchestration/test_flight_plan.py | NEW: 23 plan/mapping/budget/render tests |
| tests/cli/test_plan_approval.py | NEW: 10 approval gate + label tests |
| tests/cli/test_golden_path.py | Label assertion update |
| scripts/remedy_smoke.sh | Section 12r (flight_plan_approval) |
| docs/roadmap/STATUS.md | F014 marked [x] |

## Verification
```
99 passed in 19.94s
```

## Open Findings
0

## Next Expected Action
Review PR #148

# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 5: book round 4's PASS and register R-1078, record DECISION F028
D5, repair R-1078, and land the write door's three injection commands
and the run-log event `task_injected` with its two readers.

## Next Steps

1. The send module, the Add Task sheet in the right column, and the
   provenance chip in the graph and the task list.
2. The end-to-end proof: inject mid-run, draft, confirm, execute, and
   the report shows the origin.
3. The closure sequence.

## Risks

A running job's record is written only by its runner. Open findings: 1
(R-1078, Low, repaired this round).

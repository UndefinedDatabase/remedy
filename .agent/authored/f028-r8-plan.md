# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 8, the repair of round 7: book round 7's FAIL and register
R-1079, record DECISION F028 D8 and two prose slips, render the Add Task
sheet through a portal, and name an injected task's origin on its line
of the final report.

## Next Steps

1. The end-to-end proof: inject mid-run through the door, draft,
   confirm, execute in the same job, and the report names the origin.
2. The closure sequence.

## Risks

The planner's draft call can take tens of seconds. Open findings: 1
(R-1079, Medium, repaired this round).

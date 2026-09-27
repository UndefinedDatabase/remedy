# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 7: book round 6's PASS, record DECISION F028 D7 and its two
assumption-log rows, and land the "+ Add Task" row with its draft-and-
confirm sheet in place of the propose button, and the canvas chip.

## Next Steps

1. The end-to-end proof: inject mid-run, draft, confirm, execute, and
   the report shows the origin.
2. The closure sequence.

## Risks

The planner's draft call can take tens of seconds. Open findings: 0.

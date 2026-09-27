# Plan — F028 Task injection

Branch: feature/f028-task-injection, cut from `main` at `ceb90b8a`, the
merge commit of pull request 286 (F288 Event stream completeness).

## Goal

The Add Task button is real additive control: the operator's text is
drafted into a task by the planner, placed, budget-checked and fence-
checked, and applied to the running job only when a second call confirms
the draft, with provenance end to end (`docs/roadmap/features/T5_F028.md`).

## Current Step

ROUND 6: book round 5's PASS and resolve R-1078, record DECISION F028
D6, and land the task item's `origin`, the browser's send module for the
three injection commands, and the "Added by you" pill in the task list
and the detail popover.

## Next Steps

1. The Add Task row and its draft-and-confirm sheet, the canvas chip,
   and a headless render proof of the three surfaces.
2. The end-to-end proof: inject mid-run, draft, confirm, execute, and
   the report shows the origin.
3. The closure sequence.

## Risks

The planner's draft call can take tens of seconds. Open findings: 0.

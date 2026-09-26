# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 8: book round 7, resolve R-1068, record DECISION F027 D8, and
finish T003's page: the unreachable set fades on the canvas, a vetoed or
unreachable node's hover text carries the reason or the vetoing task,
the detail popover shows a Veto or Unreachable section with a link to
each task on the other side, and a "Veto task" form sends the veto
through the write door.

## Next Steps

1. The diamond end-to-end through the door and the runner.
2. The closure sequence.

## Risks

Every guard that reads a changed source must be in a round's selection;
this round's is the whole of `tests/ui_contracts/`. Open findings: 0.

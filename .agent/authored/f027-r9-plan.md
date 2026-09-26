# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 9: book round 8, register and repair R-1069 and R-1070, record
DECISION F027 D9, and land the diamond end-to-end: a veto filed through a live write
door on a job paused mid-run, the run finished through the real CLI, and
both answers to the replan proposal carried to their effects.

## Next Steps

1. The closure sequence: the one full suite, the evidence, the review
   package, the status line and the pull request.

## Risks

The new end-to-end runs the real CLI three times; it must stay well
inside the standard stage's budget. Open findings: 2 — R-1069 and
R-1070, both repaired this round.

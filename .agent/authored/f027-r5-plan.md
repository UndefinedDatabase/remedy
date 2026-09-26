# Plan — F027 Task veto

Branch: feature/f027-task-veto, cut from `main` at `557cbbcc`, the merge
commit of pull request 282 (F285 Findings paydown v4).

## Goal

The human red line is one click and one reason: a vetoed task is struck,
its unreachable downstream is computed and shown, the run continues on
independent branches, and a replan proposal is filed into the decision
inbox and never executed on its own (`docs/roadmap/features/T5_F027.md`).

## Current Step

ROUND 5: book round 4, register and repair R-1067, record DECISION F027
D5, and land the channel commands — `job.veto-task` in the catalog, the
CLI and the write door with the reason refused as a shape before the job
is read, and the door's answer of a replan proposal through
`decision.resolve`, which makes the inbox card answerable.

## Next Steps

1. T003: the strike, the reason on hover, the dimmed unreachable set
   with its link, the veto affordance and the inbox card's plain-words
   menu on the page.
2. The diamond end-to-end through the door and the runner.
3. The closure sequence.

## Risks

The door may reach no new forbidden module. Open findings: 1 — R-1067,
owned by F027 and repaired this round.

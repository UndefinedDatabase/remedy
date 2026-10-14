# Plan — F078 Autonomy levels

## Goal
A configured autonomy level, `L2` to `L5`, states what Remedy may start on its own; one shared
check answers every starting seam from a sixteen-cell matrix, a level of `L3` or higher needs the
passed gauntlet, every level change needs a decision record, and the level is visible where it
matters (docs/roadmap/features/T3_F078.md; DECISIONs F078 D1 and D2).

## Current Step
Session 1, round 2 on `feature/f078-autonomy-levels`: book round 1 and register R-1321, repair
R-1321, and land T002 for the mission loop — the start scope of `remedy mission run`, the check in
`dispatch_milestone_job`, the record of deferred starts, the pinned harnesses, and the page.

## Next Steps
1. T002 for the operator's own commands and T003: `remedy do` and `remedy job run` ask the gate as
   origin `manual`; the caps of `L5`; the level and the open deferred starts in `remedy status`;
   the end-to-end proof per level.
2. The closure sequence: the one full suite, the self-use run, the evidence and the pull request.

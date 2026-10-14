# Plan — F055 Rehearsal (dry check)

## Goal
`remedy do --rehearse` plans an order and stops at the approval of its plan, building no worker,
applying nothing and writing nothing into the repository; it records what a run would cost, risk
and write, and a real run reuses the rehearsed plan without planning again
(docs/roadmap/features/T3_F055.md; DECISIONs F055 D1 to D4).

## Current Step
Session 1, round 8 on `feature/f055-rehearsal`: book round 7, move R-1320 to F055 (DECISION F055
D4) and repair it — a definition-of-done check no longer passes when the application it started
died — then the one full suite again on the repaired tree, the evidence job on the new accepted
head and the review package.

## Next Steps
1. The closing round: the Built State, the resolutions, the rotation, the STATUS line with the
   README sync, SU-064's `consumed_by`, and the pull request, left unmerged.

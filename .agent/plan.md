# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 2, round 12, the integration gate: book round 11 (PASS) with R-1117's recurrence and
DECISION F292 D10 (the self-use item `SU-042` changed nothing, so nothing of it lands and it is
consumed at the STATUS flip), build `apps/ui`, then run F292's one closure full suite and its cost
line and commit the transcript `.agent/authored/f292-closure-suite.txt`. The open-findings count
is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. A repair round for every bad node the suite lists, if it is red; otherwise none.
2. The evidence job and the review package at the accepted head.
3. The closing round: book the last verdict, rotate the ledger, the STATUS flip with the README
   sync and `SU-042`'s `consumed_by`, and the pull request.

## Risks
- The diff panel opens below the cockpit (F037's deferred layout); the Built State says so.
- The suite starts UI servers that need a fresh `apps/ui/dist`; the round builds it first.

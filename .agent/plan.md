# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 2, round 13, the closure's evidence round: book round 12 (PASS; the closure suite read
exit 0 with no bad node), which is the closure's accepted head, then preview the staging-copy
reclaim, build the evidence job and build the review package from the clean, pushed tree. The
open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The closing round: book round 13's verdict, rotate the ledger, the STATUS flip with the README
   sync and `SU-042`'s `consumed_by`, and the pull request.

## Risks
- The diff panel opens below the cockpit (F037's deferred layout); the Built State says so.
- The evidence run starts UI servers and headless Chrome; `apps/ui/dist` was built in round 12
  after the last change under `apps/ui`.

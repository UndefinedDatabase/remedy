# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 2, round 14, the closing round: book round 13 (PASS; evidence job `f292r13e1001`, package
`remedy-review-20261001-095015-READY_FOR_REVIEW.zip` at the accepted head `7b3229644`), record
DECISION F292 D11 (the README's Tier 5 row reads 38 of 38), rotate the ledger, accept F292 in
STATUS with the README sync and `SU-042`'s `consumed_by`, push, and open the pull request. F292
owns no open finding. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`,
`R-1129`, all owned by F290).

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F292's pull
   request, then round 14's verdict is booked in the next feature's first commit, then Rule A5.

## Risks
- The diff panel opens below the cockpit (F037's deferred layout); the Built State says so.

# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 7: book round 6 (PASS), record DECISION F292 D7, and land the hunk decisions
panel after the diff view in the diff panel, starting from the recorded decision. Rounds 1 to 6
landed the plan read, the plan view with all six edits, and the read, rules and send of hunk
decisions. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all
owned by F290).

## Next Steps
1. The palette's seven form entries as surface entries opening the plan view and the hunk
   decisions, and an end-to-end run through the cockpit.
2. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- The door withholds a refused hunk decision's reason, so the controls must refuse in advance
  everything the rules can see coming; a refusal they cannot foresee reads as plain refusal.

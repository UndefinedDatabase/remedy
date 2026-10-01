# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 6: book round 5 (PASS), record DECISION F292 D6, and land the read of the hunk
decision recorded for the attempt a diff shows (the server routes and the client's decoder and
loader) with the hunk controls' rules and send module. Rounds 1 to 5 landed the plan read, the
plan view and all six plan edits. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`,
`R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The hunk controls: a panel beside the diff view, one row per hunk, Approve, Reject with a
   reason, the tally, and Record, starting from the recorded decision.
2. The palette's seven form entries as surface entries, and an end-to-end run.
3. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- The door withholds a refused hunk decision's reason, so the controls must refuse in advance
  everything the rules can see coming; a refusal they cannot foresee reads as plain refusal.

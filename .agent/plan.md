# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 8: book round 7 (PASS), record DECISION F292 D8, turn the palette's seven form
entries into surface entries opening the plan view and the job diff's hunk decisions, and land
the end-to-end test through the real server. Rounds 1 to 7 built the plan read, the plan view
with all six edits, and the hunk decisions. The open-findings count is 5 (`R-1117`, `R-1125`,
`R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The amend0930b-slow-cap hardening stage (SLOW MODE): an acceptance audit by a fresh worker
   given only the feature file and the repository, then repair rounds for any gap.
2. The closure sequence.

## Risks
- The door withholds a refused hunk decision's reason, so the controls must refuse in advance
  everything the rules can see coming; a refusal they cannot foresee reads as plain refusal.

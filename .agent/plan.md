# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 4: book round 3 (PASS), record DECISION F292 D4, and land the criteria editor
(change, remove, add) and the one-place task moves in the plan view. Rounds 1 to 3 landed the
plan read, the read-only view, and each task's edit and delete with the dashboard re-read. The
open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. Merge and split, in the plan view.
2. The diff view's hunk controls, with their own DECISION on reading recorded decisions.
3. The palette's seven form entries as surface entries, and an end-to-end run.
4. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- A hunk decision replaces the whole record for its diff, so controls that send only the hunks
  touched in one sitting would reset the others to pending; the hunk round rules on it first.

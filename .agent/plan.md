# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 3: book round 2 (PASS), register R-1129 (owned by F290), record DECISION F292
D3, and land the plan edits' send module, the dashboard re-read after an accepted edit, and each
task's Edit and Delete in the plan view. Rounds 1 and 2 landed the plan read and the read-only
view. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all
owned by F290).

## Next Steps
1. The criteria editor (add, edit, remove) and the order of the tasks, in the plan view.
2. Merge and split, in the plan view.
3. The diff view's hunk controls, with their own DECISION on reading recorded decisions.
4. The palette's seven form entries as surface entries, and an end-to-end run.
5. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- A hunk decision replaces the whole record for its diff, so controls that send only the hunks
  touched in one sitting would reset the others to pending; the hunk round rules on it first.

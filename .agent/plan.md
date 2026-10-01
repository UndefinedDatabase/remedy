# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 2: book round 1 (PASS), record DECISION F292 D2, and land the read-only plan
view: the `plan` section's type and normalizer, the pure rules in `apps/ui/src/api/planView.ts`,
`PlanView` opened from the right panel's Plan button, and their tests. Round 1 landed the plan
read. The open-findings count is 4 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, all owned by F290).

## Next Steps
1. The six plan edits in the plan view, each sent with the version shown, a refusal told in plain
   words, and the view read again after an accepted edit.
2. The diff view's hunk controls, with their own DECISION on reading recorded decisions.
3. The palette's seven form entries as surface entries, and an end-to-end run.
4. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- A hunk decision replaces the whole record for its diff, so controls that send only the hunks
  touched in one sitting would reset the others to pending; the hunk round rules on it first.

# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 1, round 1: claim F292, re-head the review record, book F294's round 16, register R-1128
(owned by F290), record DECISION F292 D1, and land the plan read: `plan_editing.plan_view`,
printed by `remedy job plan-show` and served by the dashboard's new `plan` section, with
`tests/ui_server/test_dashboard_plan.py`. The open-findings count is 4 (`R-1117`, `R-1125`,
`R-1127`, `R-1128`, all owned by F290).

## Next Steps
1. The plan view in the cockpit, read only: the `plan` section's type and normalizer, the
   `plan-view` region and its render check.
2. The six plan edits in the plan view, each sent with the version shown.
3. The diff view's hunk controls, with their own DECISION on reading recorded decisions.
4. The palette's seven form entries as surface entries, and an end-to-end run.
5. The amend0930b-slow-cap hardening stage (SLOW MODE), then the closure sequence.

## Risks
- A hunk decision replaces the whole record for its diff, so controls that send only the hunks
  touched in one sitting would reset the others to pending; the hunk round rules on it first.

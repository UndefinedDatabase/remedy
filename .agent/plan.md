# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 2, round 11: book round 10 (PASS) and R-1130's resolution, then generate the closure's
self-use item into the queue and run it to its approval gate, never applying it, with every
reading saved under `.agent/selfuse_f292/` (docs/roadmap/STATUS_closure_protocol.md precondition
6). The reviewer's read-only probe at `3c0f7f318` answered `SU-042`, "Narrow the excused handler at
apps/cli/commands/dev.py:126" (generator tier 4). The open-findings count is 5 (`R-1117`,
`R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The self-use item's own change, landed with its tests when the review accepts it, and every
   defect the run reports registered first.
2. The integration gate's one full suite (build `apps/ui` first) and its cost line.
3. The evidence job and the review package at the accepted head.
4. The closing round: book the last verdict, rotate the ledger, the STATUS flip with the README
   sync and the queue's `consumed_by`, and the pull request.

## Risks
- The diff panel opens below the cockpit (F037's deferred layout); the Built State says so.
- The self-use run spends real money through the `self_use` role's frontier provider, within that
  role's default budget.

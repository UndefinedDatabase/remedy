# Plan — F292 Plan view and hunk decisions in the cockpit

## Goal
The cockpit offers the seven writes the write door already accepts and no screen offers: the six
edits of a plan that waits for approval, and the approval or rejection of a change's hunks; the
palette's seven form entries open these surfaces (docs/roadmap/features/T5_F292.md).

## Current Step
Session 2, round 10, the closure sequence's first round: book round 9 (PASS), register R-1130 (the
Built State counts two of the audit's user-facing proofs where the audit lists three) and repair
that sentence, and record the checklist's one consolidation pass for F292 in
`docs/agents/planner_reviewer_prompt.md`. Rounds 1 to 8 built T001 to T003; round 9 recorded the
hardening stage. The open-findings count is 6 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
owned by F290, and `R-1130`, owned by F292).

## Next Steps
1. The closure's self-use item: generate it into the queue and run it to its approval gate, never
   applying it; book R-1130's resolution in that round's first commit.
2. The self-use item's own change, landed with its tests when the review accepts it.
3. The integration gate's one full suite (build `apps/ui` first) and its cost line.
4. The evidence job and the review package at the accepted head.
5. The closing round: book the last verdict, rotate the ledger, hand F292's open findings on, the
   STATUS flip with the README sync and the queue's `consumed_by`, and the pull request.

## Risks
- The diff panel opens below the cockpit (F037's deferred layout); the Built State says so.

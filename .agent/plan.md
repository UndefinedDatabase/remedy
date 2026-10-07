# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 13, the closure sequence's last content round before the evidence: book round 12, whose one
full suite read green (21520 passed, 22 skipped) on the tree that ships; one prose slip; the
checklist's once-per-feature consolidation pass for F287 in docs/agents/planner_reviewer_prompt.md
(the list stays at 34 items).

## Next Steps
1. The evidence round, in a fresh session: the staging reclaim, the evidence job and the review
   package at the accepted head (docs/roadmap/STATUS_closure_protocol.md algorithm steps 1, 2).
2. The closing round: the ledger rotation, the STATUS line with its README sync and the self-use
   queue's `consumed_by` for SU-046, and the pull request, left unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run needed no repair round, so that is not yet
  observed in real use.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.

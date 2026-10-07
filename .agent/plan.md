# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 16, the closure's evidence round again (docs/roadmap/STATUS_closure_protocol.md algorithm
steps 1 and 2), because round 15's docs repair moved the head past round 14's package: book round
15, resolve R-1164, one prose slip, then at the accepted head the staging reclaim, the evidence job
`f287r16e1001` over 47 test files, and the review package from the clean, pushed tree.

## Next Steps
1. Round 17, the closing round: book round 16, the ledger rotation, the STATUS line with its
   README sync and the self-use queue's `consumed_by` for SU-046, and the pull request, left
   unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run needed no repair round, so that is not yet
  observed in real use.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162 (Low) stay
  open, owned by F297.

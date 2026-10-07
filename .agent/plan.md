# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order; T001 to T003 have landed.

## Current Step
Round 11, the closure sequence's first round (docs/roadmap/STATUS_closure_protocol.md
precondition 6): book round 10 and resolve R-1163; generate the closure's self-use item and run it
to its approval gate through the `self_use` role's provider, never applying it, recorded under
`.agent/selfuse_f287/`.

## Next Steps
1. Register every defect the self-use run reports; the one full suite (the integration gate).
2. The checklist's consolidation pass; the evidence job and the review package.
3. The ledger rotation, the STATUS line with its README sync and the self-use queue's
   `consumed_by`, and the pull request, left unmerged.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); this round's self-use run is the first real observation if it runs on
  `claude-cli` and reaches a repair round.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.

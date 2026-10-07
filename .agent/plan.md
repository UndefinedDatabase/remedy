# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 7, round 26: book round 25's PASS and register R-1158 (the cost limit lies inside the
spread of repeated runs; owned by F297) with one prose slip; the feature file's Built State names
the three lines F295 added to the reachability allowlist (closure precondition 7); the checklist's
once-per-feature consolidation pass for F295. These are the last content commits before the
evidence.

## Next Steps
1. Round 27: book round 26; the staging reclaim, the evidence job and the review package at the
   accepted head.
2. Round 28: the ledger rotation, the open findings re-assigned to F297, the STATUS line with the
   README and the self-use entry's `consumed_by`, and the pull request.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) stay open, owned by F297.
- F295 is at its soft limit of 25 rounds and 7 sessions; the closure is the self-consistent close
  and no split is proposed (scope report in the handoff).
- Another actor switched the primary checkout during round 24 (operator question Q6).

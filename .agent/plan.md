# Plan — F295 Machine client contract v1

## Goal
Remedy can be driven end to end by a program through the command line's JSON envelope alone: an
order file, one digest, decisions answered with `--json`, an approved apply and the proof
(docs/roadmap/features/T12_F295.md). DECISION F295 D1 fixes the slices and their order.

## Current Step
Session 7, round 27: the closure's evidence round. Book round 26's PASS; that commit is the
ACCEPTED HEAD. Then the staging reclaim, the evidence job built by
`.agent/authored/f295-r27-create_f295_evidence.py`, and the review package from the clean, pushed
tree at that head.

## Next Steps
1. Round 28: book round 27; the ledger rotation, the open findings re-assigned to F297, the STATUS
   line with the README and the self-use entry's `consumed_by`, and the pull request.

## Risks
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158 (Low) stay open, owned by F297.
- F295 is at its soft limit of 25 rounds and 7 sessions; the closure is the self-consistent close
  and no split is proposed (scope report in the handoff).
- Another actor switched the primary checkout during round 24 (operator question Q6).

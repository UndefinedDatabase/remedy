# Plan — F298 Machine client contract v1.1: what a client can rely on

## Goal
One document generated from the code names every operation, field, word, token and exit code a
program meets when it drives Remedy, and the machine client page is its rendering
(docs/roadmap/features/T12_F298.md, T001). F298 closes at T001's scope; T002 to T007 moved to F304
(DECISION F298 D21).

## Current Step
Session 6, round 28: the closure's evidence round. Round 27's verdict is booked; this round's
first commit is the accepted head; the staging-copy reclaim, the evidence job and the review
package are built from the clean, pushed tree at that head.

## Next Steps
1. The closing round: the ledger rotation, the STATUS line with the README sync and the self-use
   queue's `consumed_by`, and the pull request.

## Risks
- A failing evidence or package build blocks the closure; it is repaired, or the feature goes `[!]`.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172,
  R-1176 (Low) stay open, owned by F297; F298 owns none.

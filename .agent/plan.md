# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISIONs F302 D1 to D4).

## Current Step
Round 7 on `feature/f302-claude-cli-tokens`, the closure's evidence round: book round 6, then the
staging reclaim, the evidence job on this round's first commit, the closure's accepted head, and
the review package.

## Next Steps
1. The closing round: book round 7, the Built State's closure readings, the ledger rotation, F302
   accepted in STATUS with the README sync and `SU-054`'s `consumed_by`, and the pull request, left
   unmerged.

## Risks
- R-1235 (Low) is open and owned by F297. R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
  R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are open and owned by
  F297; F302 owns none.

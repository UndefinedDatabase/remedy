# Plan — F302 The claude-cli worker's tokens per call: measure, attribute, cut

## Goal
The tokens one `claude-cli` call spends before it does any work are measured, attributed to their
sources and cut by the configuration Remedy starts the worker with; `remedy stats` shows tokens by
kind per call and per landed change (docs/roadmap/features/T3_F302.md; DECISIONs F302 D1 to D4).

## Current Step
Round 8 on `feature/f302-claude-cli-tokens`, the closing round: book round 7, the Built State's
closure readings, the ledger rotation, F302 accepted in STATUS with the README sync and `SU-054`'s
`consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F302's pull request after its
   hosted checks are read, and round 8's verdict is booked in the next feature's first commit.
2. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

## Risks
- R-1235 (Low) is open and owned by F297. R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
  R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230 (Low) are open and owned by
  F297; F302 owns none.

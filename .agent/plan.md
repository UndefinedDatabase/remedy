# Plan — F300 Structure ledger and size ratchet

## Goal
Remedy's structure has a measure, a ledger and a ratchet: a product command that measures any
repository, a page and a test that let each of Remedy's recorded sizes fall and never rise and
refuse a new function or file above the limit, a rule that pays the debts down every fifth
feature, and the first step, `run_job`'s safe points in one function
(docs/roadmap/features/T2_F300.md; DECISIONs F300 D1 and D2).

## Current Step
Round 5 on `feature/f300-structure-ledger-size-ratchet`, the closure's evidence round: book round
4, then on the accepted head the staging reclaim, the evidence job and the review package.

## Next Steps
1. The closing round: the ledger rotation, the STATUS line with the README and the self-use queue,
   and the pull request, left unmerged.

## Risks
- The package must read `READY_FOR_REVIEW` with its review subject from the fork point
  `b25d87a24` to the accepted head; a failing package is a closure blocker.
- R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219,
  R-1220, R-1225 and R-1230 (Low) are open and owned by F297; F300 owns none.

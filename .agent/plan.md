# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1). All seven are resolved.

## Current Step
Session 4, round 8: book round 7's verdict, and land the closure's self-use item `SU-044` as its
job wrote it, with two tests of `remedy dev status` through the command line (DECISION F290 D4),
before the closure's one full suite.

## Next Steps
1. The integration gate: the one full suite and its CPU reading against F200's 981.70.
2. The evidence job and the review zip.
3. The ledger rotation, the next paydown's registration with R-1138's owner line, the STATUS flip
   with the README and `SU-044`'s `consumed_by`, and the pull request.

## Risks
- R-1138 (Low) stays open, owned by the paydown this closure registers.

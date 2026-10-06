# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1). All seven are resolved.

## Current Step
Session 4, round 7: book round 6's verdict, and run the closure's one self-use item (closure
precondition 6) to its approval gate, never applied, recording every reading under
`.agent/selfuse_f290/`. The reviewer's probe answered `SU-044`, generator tier 4.

## Next Steps
1. Register every defect the self-use run surfaced, and book round 7's verdict.
2. The integration gate: the one full suite and its CPU reading against F200's 981.70.
3. The evidence job and the review zip.
4. The ledger rotation, the next paydown's registration with R-1138's owner line, the STATUS flip
   with the README, and the pull request.

## Risks
- R-1138 (Low) stays open, owned by the paydown this closure registers.
- The self-use run spends real money, at most the self_use role's default budget.

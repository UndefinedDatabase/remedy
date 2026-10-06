# Plan — F290 Findings paydown v6

## Goal
Pay down the seven findings open at the claim, `R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
`R-1133` and `R-1137`, each by the repair its own text names, one slice per finding
(docs/roadmap/features/T2_F290.md, DECISION F290 D1).

## Current Step
Session 4, round 5: book round 4's verdict (PASS) and the resolution of R-1117, and land T007
(R-1137) by DECISION F290 D3: the CPU time of the eleven test modules F200 added or changed,
measured and committed as `.agent/authored/f290-r5-cpu.txt`, recorded as the price of F200. Every
slice of the feature is then landed.

## Next Steps
1. The amend0930b-slow-cap hardening stage: an acceptance audit of `docs/roadmap/features/T2_F290.md`
   by a fresh auditor, its report committed, every gap repaired in a reviewed round (at most three).
2. The closure sequence, whose one full suite gives the next CPU reading against F200's 981.70.

## Risks
- R-1138 (Low) stays open, owned by the paydown F290's closure registers.

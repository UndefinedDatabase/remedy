# Plan — F297 Findings paydown v7

## Goal
Pay down the open findings F297 owns, each by the repair its own text names, with the evidence
that discharged it (docs/roadmap/features/T2_F297.md; DECISIONs F297 D1 to D12).

## Current Step
Round 13 on `feature/f297-findings-paydown-v7`, session 2, the closure's evidence round: book
round 12 and register R-1252, the self-use run's one defect, for the next findings paydown; this
round's first commit is the closure's accepted head, on which the evidence job runs and the review
package is built.

## Next Steps
1. The closing round: book round 13, the Built State, the ledger's rotation, R-1235 and R-1246
   re-assigned to the next findings paydown and that paydown registered, the STATUS line with the
   README sync and the self-use entry's `consumed_by`, and the pull request, left unmerged.

## Risks
- R-1235 and R-1246 are carried (the operator allowed R-1246's four reads by DECISION F297 D2,
  and the session's permission settings still refuse them); R-1248 is owned by F305; R-1251 and
  R-1252 by the next findings paydown.
- The evidence job runs one pytest over its own test files; nothing else runs tests this round.

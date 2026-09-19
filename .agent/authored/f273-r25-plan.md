# Plan — F273 Findings paydown v1

Branch: feature/f273-findings-paydown-v1, cut from `main` at `80f7c529`
(the merge commit of pull request 259, F271's closure).

## Goal

Pay down the open findings that describe a real defect, each by the repair
its own text names, with the evidence that discharged it
(`docs/roadmap/features/T2_F273.md`).

## Current Step

Round 25 is closure round B: it books round 24's verdict, registers R-1000,
moves every open finding to F282 by the ownership paragraph, rotates the
ledger, registers F282, flips F273's STATUS line with the README and the
self-use item's `consumed_by`, and opens the pull request into `main`.

## Next Steps

1. The next session's Phase 1: rule 1 (`.agent/STOP`), then rule 2 merges
   F273's pull request at the Open PR Gate once its hosted CI has run.
2. The first round of the next feature books round 25's verdict and reads
   the pull request's 3.12 column for R-0984, which F282 owns.
3. Rule A5 then proposes the next unchecked STATUS line.

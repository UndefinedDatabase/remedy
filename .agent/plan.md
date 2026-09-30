# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 24: the closing round. Round 23 is booked PASS: the evidence job `f293r23e1001`
and the package `remedy-review-20261001-005405-READY_FOR_REVIEW.zip` cover the accepted head
`b59d42cc9`. This round rotates the ledger, flips F293's STATUS line to `[x]` with the README's
counts and Tier 2 paragraph and `SU-040`'s `consumed_by` in the same commit, and opens the pull
request. F293 closes at a 24.5 percent cut; the rest of T002 is F294 (DECISION F293 D15). The
open-findings count is 2 (`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. The next session merges F293's pull request at the Open PR Gate, then claims the next feature by
   Rule A5, which is F294.

## Risks
- None open for F293; operator question Q2 records the split and stands until the operator answers.

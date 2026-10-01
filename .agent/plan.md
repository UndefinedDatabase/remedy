# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 3, round 16: the closing round. Round 15 is booked PASS: the evidence job `f294r15e1001`
and the package `remedy-review-20261001-050249-READY_FOR_REVIEW.zip` cover the accepted head
`5c7006583`. This round hands `R-1127` to F290, records DECISION F294 D13 (the checklist's
consolidation pass), rotates the ledger, flips F294's STATUS line to `[x]` PASS_WITH_RISKS with
the README's counts and Tier 2 paragraph and `SU-041`'s `consumed_by` in the same commit, and
opens the pull request. F294 closes at 865.36 CPU seconds on its Acceptance's second branch
(DECISION F294 D12). The open-findings count is 3 (`R-1117`, `R-1125`, `R-1127`, all owned by
F290).

## Next Steps
1. The next session merges F294's pull request at the Open PR Gate, then claims the next feature
   by Rule A5.

## Risks
- None open for F294; operator question Q3 records the closing ruling and stands until the
  operator answers.

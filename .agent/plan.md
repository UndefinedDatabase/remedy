# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 14: the closure ruling. Book round 13 (PASS: the one full suite read 865.36 CPU
seconds, exit 0), record DECISION F294 D12 (F294 closes on its Acceptance's second branch), add
the closure's reading to the feature file's Built State, and write operator question Q3. The
open-findings count is 3 (`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294 until its
closure hands it to F290).

## Next Steps
1. The evidence job and the review package at the accepted head, with the staging-copy reclaim.
2. The closing round: rotate the ledger, hand `R-1127` to F290, accept F294 PASS_WITH_RISKS in
   STATUS and README, consume `SU-041`, open the pull request.

## Risks
- None for the closure; what remains of the target is a product question, offered to the
  operator as Q3 (DECISION F294 D12).

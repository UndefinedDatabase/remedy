# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 6: book round 5 (PASS), record where the suite's CPU still goes and why the
building rounds end here (DECISION F294 D6), and write F294's Built State. The open-findings
count is 2 (`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. The amend0930b-slow-cap hardening stage: a fresh acceptance audit of F294's Acceptance and
   Goal & Done, and the repairs of any gap it finds.
2. The closure sequence, whose one full suite gives the "after" reading; if it misses 747.65,
   the closure rules with the numbers or splits, and writes the trade-off to the operator.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

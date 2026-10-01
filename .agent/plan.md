# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 7: the first repair round of the amend0930b-slow-cap hardening stage. Book
round 6 (PASS), save the acceptance audit's report, register its two gaps as `R-1126` and
`R-1127`, record DECISION F294 D7, and repair both gaps with tests. The open-findings count is 4
(`R-1117`, `R-1125`, owned by F290; `R-1126`, `R-1127`, owned by F294).

## Next Steps
1. Repeat the acceptance audit for the statements that had gaps.
2. Book round 7, resolve `R-1126` and `R-1127`, and record the hardening stage in the feature
   file's Built State.
3. The closure sequence, whose one full suite gives the "after" reading; if it misses 747.65,
   the closure rules with the numbers or splits, and writes the trade-off to the operator.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 8: the second repair round of the amend0930b-slow-cap hardening stage. Book
round 7 (PASS), save the repeat audit's report, resolve `R-1126`, record DECISION F294 D8, and
make the data-root allocator's test forbid any directory listing (`R-1127`). The open-findings
count is 3 (`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294).

## Next Steps
1. Repeat the acceptance audit for the data-root statement.
2. Book round 8, resolve `R-1127`, and record the hardening stage in the feature file's Built
   State.
3. The closure sequence, whose one full suite gives the "after" reading; if it misses 747.65,
   the closure rules with the numbers or splits, and writes the trade-off to the operator.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

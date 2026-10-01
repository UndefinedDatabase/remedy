# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 9: the third and last repair round of the amend0930b-slow-cap hardening stage.
Book round 8 (PASS), save the second repeat audit's report, record DECISION F294 D9, and make the
data-root allocator's test refuse every directory listing and every started process (`R-1127`).
The open-findings count is 3 (`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294).

## Next Steps
1. Repeat the acceptance audit for the data-root statement.
2. Book round 9, resolve `R-1127` or carry it with its owner, and record the hardening stage in
   the feature file's Built State.
3. The closure sequence, whose one full suite gives the "after" reading; if it misses 747.65,
   the closure rules with the numbers or splits, and writes the trade-off to the operator.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

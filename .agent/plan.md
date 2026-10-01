# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 10: the hardening stage's record. Book round 9 (PASS), save the third repeat
audit's report, record DECISION F294 D10 (the stage ends after three repair rounds, `R-1127`
stays open), and write the stage into the feature file's Built State. The open-findings count is
3 (`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294 until its closure hands it to F290).

## Next Steps
1. The closure sequence (docs/roadmap/STATUS_closure_protocol.md): run the closure's self-use
   item to its approval gate, then the integration gate's one full suite and its cost, then the
   evidence job and the review package, then the closing round.
2. If the full suite misses 747.65 CPU seconds, the closure's DECISION states the remaining cost
   with DECISION F294 D6's readings, and the trade-off goes to the operator.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

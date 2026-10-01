# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 11: the closure sequence's first round. Book round 10 (PASS), then generate the
closure's self-use item and run it to its approval gate, never applying it
(docs/roadmap/STATUS_closure_protocol.md precondition 6). The open-findings count is 3
(`R-1117`, `R-1125`, owned by F290; `R-1127`, owned by F294 until its closure hands it to F290).

## Next Steps
1. Register every defect the self-use run reports, and land the self-use item's repair with its
   red-proof.
2. The integration gate: F294's one full suite and its cost against the 747.65 CPU-second target.
3. The evidence job and the review package, then the closing round.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

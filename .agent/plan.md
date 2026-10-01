# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 2, round 13: the integration gate. Book round 12 (PASS), then run F294's one full suite on
the tree that ships and read its CPU cost against the 747.65 CPU-second target
(docs/agents/integration_gate.md). The open-findings count is 3 (`R-1117`, `R-1125`, owned by
F290; `R-1127`, owned by F294 until its closure hands it to F290).

## Next Steps
1. A green suite: the closure DECISION on the 40 percent target, then the evidence job and the
   review package. A red suite: a repair round naming every bad node id.
2. The closing round.

## Risks
- What remains can only be cut by changing what a job run does (DECISION F294 D6).

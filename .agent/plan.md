# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 3: book round 2 (PASS), and stop a reading from running `git submodule status`
when the index holds no submodule (DECISION F294 D3). On this machine's git that command is a
shell script costing about twenty times any other command of a reading. The open-findings count
is 2 (`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. Cut the rest of the job runner's git work where state provably has not changed, measured in
   two fresh worktrees with Remedy's identity frozen, as round 3 measured.
2. The amend0930b-slow-cap hardening stage: a fresh acceptance audit and its repairs.
3. The closure sequence, whose one full suite gives the "after" reading.

## Risks
- The cuts so far are measured one by one; only the closure's full suite shows their sum.

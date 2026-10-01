# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 4: book round 3 (PASS), and run the golden-path tests' `init`, `do` and `status`
in the test process, keeping every other command of that file a child process (DECISION F294 D4;
at least 12.4 CPU seconds per run of the file, which is also every round's canary). The
open-findings count is 2 (`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. Measure the remaining files that start the command line as a child process where the child
   is not what the test is about, and cut from the top of what remains.
2. The amend0930b-slow-cap hardening stage: a fresh acceptance audit and its repairs.
3. The closure sequence, whose one full suite gives the "after" reading.

## Risks
- The cuts so far are measured one by one; only the closure's full suite shows their sum.

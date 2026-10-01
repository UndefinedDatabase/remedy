# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 5: book round 4 (PASS), move the in-process command line into
`tests/cli/in_process_cli.py`, and run the scoped-listing tests' setup through it while every
listing they assert on stays a child process (DECISION F294 D5). The open-findings count is 2
(`R-1117`, `R-1125`, both owned by F290).

## Next Steps
1. Write the measured cuts into the feature file's Built State, and decide with the numbers
   whether more cuts remain that keep every test's subject intact.
2. The amend0930b-slow-cap hardening stage: a fresh acceptance audit and its repairs.
3. The closure sequence, whose one full suite gives the "after" reading.

## Risks
- The cuts so far are measured one by one; only the closure's full suite shows their sum.

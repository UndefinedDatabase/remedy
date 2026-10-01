# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 2: book round 1 (PASS), and cut the cost every test pays for its data root.
Each test's root now comes from one parent per test process, so no test lists the base temporary
directory to number it (DECISION F294 D2; about 30 CPU seconds of a full suite by the reviewer's
measurement of pytest's own numbering). The open-findings count is 2 (`R-1117`, `R-1125`, both
owned by F290).

## Next Steps
1. Measure what remains of the job runner's git work and of the files that run whole jobs, and
   cut what can be cut without changing what a test proves: `tests/cli/test_golden_path.py`
   starts the command line as a child process in every test, which only some tests are about.
2. The amend0930b-slow-cap hardening stage: a fresh acceptance audit and its repairs.
3. The closure sequence, whose one full suite gives the "after" reading.

## Risks
- The cuts so far are measured one by one; only the closure's full suite shows their sum.

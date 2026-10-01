# Plan — F294 Test load diet, part two

## Goal
Cut the full suite's CPU time to at most 747.65 CPU seconds, 40 percent below F293's T001
baseline, without losing an assertion; or rule with numbers that no more can be cut without
weakening a test (docs/roadmap/features/T2_F294.md).

## Current Step
Session 1, round 1: claim F294, re-head the review record, book F293's round 24, and land the
first cut. A `worktree_identity` reading discovers the repository's configured helpers once
instead of before each of its six git commands (DECISION F294 D1), so one one-task `remedy do`
starts 195 git processes instead of 210. The open-findings count is 2 (`R-1117`, `R-1125`, both
owned by F290).

## Next Steps
1. Cut the job runner's repeated tree snapshots: the back-to-back `write_tree` of the task's
   change set and its safe diff, and the other repeated git readings the reviewer's count names.
2. Measure the files that run whole jobs (`tests/cli/test_do_sequence_cli.py`,
   `tests/cli/test_golden_path.py`, `tests/cli/test_do_commit_flags.py`) before and after, and
   cut from the top of what remains.
3. The amend0930b-slow-cap hardening stage: a fresh acceptance audit and its repairs.
4. The closure sequence, whose one full suite gives the "after" reading.

## Risks
- The git cuts alone may not reach 40 percent; each round's measurement says how far it got.

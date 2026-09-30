# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 5, round 14: the first repair round of the amend0930b-slow-cap hardening stage. Round 13
is booked PASS. The acceptance audit (`.agent/f293_acceptance_audit.md`) found two gaps,
registered as `R-1121` (T001's inventory unguarded) and `R-1122` (no guard that no assertion was
lost); one test file repairs both (DECISION F293 D11). They are resolved only after review and a
repeat of the audit for those two statements. The open-findings count is 3 (`R-1117`, `R-1121`,
`R-1122`).

## Next Steps
1. Repeat the acceptance audit for the two statements that had gaps, by a fresh auditor.
2. Record the stage in the feature file's Built State (statements audited, proven at once, gaps
   found, repaired, remaining), resolve `R-1121` and `R-1122`.
3. The closure sequence, whose integration-gate run supplies T002's after reading and the first
   `Test load:` line from `scripts/closure_suite_cost.py`; below 40 percent, the closure's
   DECISION states the remaining cost with D10's numbers.

## Risks
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- A CPU reading compares only with one taken in the same tree: the job runner file read 41.0 in
  the primary checkout and 70.59 in a disposable worktree on the same code.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite. The leftover-process check first
  meets the whole suite there; T001's run left no process behind.
- A round's selection includes the repository-wide guards over every root it adds a handler, a
  variable read or a module to (`R-1120`).

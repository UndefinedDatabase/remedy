# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 4, round 10. Round 9 is booked PASS. Round 10 builds T004: `remedy doctor core` states how
many test runs and CPU minutes the last 24 hours cost, read from the test load record, as
information only (DECISION F293 D7). T002's cuts so far are rounds 2 to 9; their total is read at
the closure's one full-suite run (DECISION F293 D1). The open-findings count is 2 (`R-1117`,
`R-1118`).

## Next Steps
1. T003 — a test run that leaves a process behind fails (the owner of `R-1118`), and each
   closure's suite transcript records its CPU seconds, a closure costing more than 10% above the
   previous feature's registering a finding owned by the rolling paydown.
2. T002 — further cuts only where the dry run measures a real CPU saving: the mission tests'
   `mission start` setup calls, source scanners that parse the same files in many tests.
3. amend0930b-slow-cap hardening stage: the acceptance audit of every Acceptance and Goal & Done
   statement by a fresh worker, then repair rounds for its gaps.
4. The closure sequence, whose integration-gate run supplies T002's after reading.

## Risks
- "CPU share per test file" in T001 is approximated from wall-clock durations under `-n auto`
  parallelism, not true per-process CPU time; the inventory states this plainly.
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- A CPU reading compares only with one taken in the same tree: the job runner file read 41.0 in
  the primary checkout and 70.59 in a disposable worktree on the same code.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite.

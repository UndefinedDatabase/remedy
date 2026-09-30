# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 5, round 16: the third and last repair round of the amend0930b-slow-cap hardening stage.
Round 15 is booked PASS with the second repeat audit, which left `R-1123` open: a statement placed
before an unchanged assertion can empty it. This round compares every function, method and
assignment that existed where F293 began, with each change F293 made pinned as reviewed (DECISION
F293 D13). The open-findings count is 2 (`R-1117`, `R-1123`).

## Next Steps
1. Repeat the acceptance audit for "without losing a single assertion", by a fresh auditor.
2. Record the stage in the feature file's Built State (statements audited, proven at once, gaps
   found, repaired, remaining), and resolve `R-1123`, or, if the audit still finds a gap, keep it
   open with its owner and close PASS_WITH_RISKS naming it (amend0930b-slow-cap rule 3).
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
- Mutation runs under `-n auto` set `PYTHONDONTWRITEBYTECODE=1`: `-B` does not reach the xdist
  workers, and a same-size mutation restored within a second is otherwise read back stale.

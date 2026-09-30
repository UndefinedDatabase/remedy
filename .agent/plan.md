# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 5, round 13. Round 12 is booked PASS and `R-1120` is resolved. Round 13 is one T002 cut:
the mission command tests start their setup missions in-process, 42.28 to 30.50 CPU seconds for
that file (DECISION F293 D10, which also records what the remaining end-to-end tests spend). The
open-findings count is 1 (`R-1117`, owned by the rolling paydown).

## Next Steps
1. amend0930b-slow-cap hardening stage: the acceptance audit of every Acceptance and Goal & Done
   statement by a fresh worker, then repair rounds for its gaps.
2. The closure sequence, whose integration-gate run supplies T002's after reading and the first
   `Test load:` line from `scripts/closure_suite_cost.py`; below 40 percent, the closure's
   DECISION states the remaining cost with D10's numbers.

## Risks
- "CPU share per test file" in T001 is approximated from wall-clock durations under `-n auto`
  parallelism, not true per-process CPU time; the inventory states this plainly.
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- A CPU reading compares only with one taken in the same tree: the job runner file read 41.0 in
  the primary checkout and 70.59 in a disposable worktree on the same code.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite. The leftover-process check first
  meets the whole suite there; T001's run left no process behind.
- A round's selection includes the repository-wide guards over every root it adds a handler, a
  variable read or a module to (`R-1120`).

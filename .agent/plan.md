# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 5, round 12. Round 11 is booked PASS and `R-1118` is resolved. Round 12 registers and
repairs `R-1120` (round 10's handler raised the blind-handler ratchet to 289 over its frozen 288),
and builds the second half of T003: `scripts/closure_suite_cost.py` puts the closure run's CPU
seconds into the suite transcript and compares them with the previous closure's (DECISION F293
D9). `R-1120` is resolved in the ledger only after this round's review. The open-findings count
is 2 (`R-1117`, `R-1120`).

## Next Steps
1. T002 — one more cut only where the dry run measures a real CPU saving: the mission tests'
   `mission start` setup calls, source scanners that parse the same files in many tests.
2. amend0930b-slow-cap hardening stage: the acceptance audit of every Acceptance and Goal & Done
   statement by a fresh worker, then repair rounds for its gaps.
3. The closure sequence, whose integration-gate run supplies T002's after reading and the first
   `Test load:` line from `scripts/closure_suite_cost.py`.

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

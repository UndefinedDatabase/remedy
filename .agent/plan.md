# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 20: the closure sequence's integration-gate round. Round 19 is booked PASS: the
self-use item `SU-040` landed with two tests (DECISION F293 D14). This round runs F293's one
closure full suite, `python3 -m pytest -n auto -q`, in the primary checkout on the tree that ships,
and `scripts/closure_suite_cost.py`, and commits the transcript
`.agent/authored/f293-closure-suite.txt` with the run's `Test load:` line. The open-findings count
is 1 (`R-1117`, owned by the rolling paydown).

## Next Steps
1. Read the transcript. A red run is repaired under amend0917-throughput rule 2. A green run gives
   T002's after reading against T001's 1,246.09 CPU seconds; the closure's DECISION states whether
   the 40 percent target is met, and when it is missed, the remaining cost with DECISION F293 D10's
   numbers; the Built State takes the reading.
2. The evidence bundle and the review zip.
3. The ledger rotation, `SU-040`'s `consumed_by`, the STATUS flip and the pull request.

## Risks
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- The leftover-process check (DECISION F293 D8) meets the whole suite for the first time in this
  run; a process left behind fails the run and names the process.
- `tests/regression/test_f293_acceptance.py` reads the fork point through `git show` while F293 is
  open; the closure suite runs in the primary checkout, which has that history.

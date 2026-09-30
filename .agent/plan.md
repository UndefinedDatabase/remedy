# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 19: the closure sequence's second round. Round 18 is booked PASS: the self-use
item `SU-040` ran to its approval gate with no run defect. This round lands the job's own change,
the task-progress probe of `remedy dev status` narrowed to the four errors it can meet and
`MAX_EXCUSED` lowered to 287, with two tests through the command line (DECISION F293 D14), and the
Built State records it. The open-findings count is 1 (`R-1117`, owned by the rolling paydown).

## Next Steps
1. The integration-gate round: the one full suite on the tree that ships,
   `scripts/closure_suite_cost.py`, T002's after reading against 1,246.09 CPU seconds, and the
   closure's DECISION on the 40 percent target with DECISION F293 D10's numbers when it is missed;
   the Built State takes the reading.
2. The evidence bundle and the review zip.
3. The ledger rotation, `SU-040`'s `consumed_by`, the STATUS flip and the pull request.

## Risks
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite.
- `tests/regression/test_f293_acceptance.py` reads the fork point through `git show` while F293 is
  open; the closure suite runs in the primary checkout, which has that history.

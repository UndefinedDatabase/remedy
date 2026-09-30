# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 21: the closure's repair round (amend0917-throughput rule 2). Round 20 is booked
PASS; its closure suite read no failed test and exit code 1, because a live UI test left its fake
browser's `sleep` running (R-1124). This round starts the browser in a session of its own and ends
its whole process group on close, with a test, and then re-runs the one full suite on the repaired
tree, replacing `.agent/authored/f293-closure-suite.txt` (amend0921-operator-feedback rule 1). The
open-findings count is 2 (`R-1117`, owned by the rolling paydown, and `R-1124`, this feature's).

## Next Steps
1. Read the new transcript and resolve R-1124 when it reads exit 0 with no process left behind.
2. The closure DECISION on the 40 percent target: round 20's run read 944.99 CPU seconds against
   T001's 1,246.09, 24.2 percent less; the new run's reading decides, and the remaining cost is
   stated with DECISION F293 D10's numbers. The Built State takes the reading.
3. The evidence bundle and the review zip; then the ledger rotation, `SU-040`'s `consumed_by`, the
   STATUS flip and the pull request.

## Risks
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- The real-browser test in the same file runs only in the primary checkout, where the UI's
  dependencies are installed; the reviewer's dry tree skipped it, so the re-run is its proof.

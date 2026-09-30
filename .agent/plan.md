# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 17: the hardening stage is finished. Round 16 is booked PASS with the third repeat
audit (PROVEN), `R-1123` is resolved, the three repeat-audit reports are saved, and the feature file
gains its Built State with the stage's record (amend0930b-slow-cap rule 4). The open-findings count
is 1 (`R-1117`, owned by the rolling paydown).

## Next Steps
1. The self-use item the closure consumes (STATUS_closure_protocol.md precondition 6): read the
   queue first; an item that needs a repair round runs before the integration-gate round.
2. The integration-gate round: the one full suite, `scripts/closure_suite_cost.py`, T002's after
   reading against 1,246.09 CPU seconds, and the closure's DECISION on the 40 percent target with
   DECISION F293 D10's numbers when it is missed; the Built State takes the reading.
3. The evidence bundle, the review zip, the ledger rotation, the STATUS flip and the pull request.

## Risks
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- A CPU reading compares only with one taken in the same tree: the job runner file read 41.0 in
  the primary checkout and 70.59 in a disposable worktree on the same code.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite. The leftover-process check first
  meets the whole suite there; T001's run left no process behind.
- `tests/regression/test_f293_acceptance.py` reads the fork point through `git show` while F293 is
  open; the closure suite runs in the primary checkout, which has that history.

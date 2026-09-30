# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 6, round 18: the closure sequence's first round. Round 17 is booked PASS, which finished
the hardening stage. The self-use item this closure consumes (STATUS_closure_protocol.md
precondition 6) is generated into the queue and run to its approval gate, never applied; its
readings are saved under `.agent/selfuse_f293/`. The reviewer's probe at `a525bfad8` named it:
`SU-040`, narrow the excused blind handler at `apps/cli/commands/dev.py:100` and lower
`MAX_EXCUSED` by one. The open-findings count is 1 (`R-1117`, owned by the rolling paydown).

## Next Steps
1. Register every defect the run reports; land `SU-040`'s repair with its red-proof, before the
   one full suite, so the suite proves the tree that ships.
2. The integration-gate round: the one full suite, `scripts/closure_suite_cost.py`, T002's after
   reading against 1,246.09 CPU seconds, and the closure's DECISION on the 40 percent target with
   DECISION F293 D10's numbers when it is missed; the Built State takes the reading.
3. The evidence bundle, the review zip, the ledger rotation, the STATUS flip and the pull request.

## Risks
- The self-use run spends real provider money, at most the `self_use` role's default budget (8
  provider calls, $6.00).
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite.
- `tests/regression/test_f293_acceptance.py` reads the fork point through `git show` while F293 is
  open; the closure suite runs in the primary checkout, which has that history.

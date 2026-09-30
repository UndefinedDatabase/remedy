# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Session 4, round 7. Round 6 is booked PASS. Round 7 caches each match answer of
`dead_command_ids` per search root and searched words (DECISION F293 D4): the reviewer's dry run
read `tests/cli/test_worker_facade_cmd.py` at 22.04 CPU seconds before and 2.83 after (serial
runs, `-n 0`, test load record). The open-findings count is 2 (`R-1117`, `R-1118`).

## Next Steps
1. T002 — more cuts, ranked by the CPU work they remove rather than by wall time: the mission
   tests' `mission start` setup calls where the start is not what a test checks, source scanners
   that parse the same files in many tests, the two whole-repository collection runs of the CI
   stage tests, UI builds and Chrome starts shared per module; every changed test keeps a mutation
   red-proof. Target: the test load record's `cpu_seconds` at least 40% below 1246.09 (T001's own
   reading), or a dated DECISION with numbers showing no more can be cut.
2. T003 — each closure's suite transcript records CPU seconds; a closure costing >10% more than the
   previous feature's registers a finding owned by the rolling paydown; a run leaving a process
   behind fails.
3. T004 — `remedy doctor core` states the last 24 hours' run count and CPU minutes from the record.
4. amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- "CPU share per test file" in T001 is approximated from wall-clock durations under `-n auto`
  parallelism, not true per-process CPU time; the inventory states this plainly.
- The test load record adds up CPU time (`os.times()`), and a test that sleeps uses none; a cut
  that only removes a sleep shortens the run but moves the 40% target by nothing.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite.

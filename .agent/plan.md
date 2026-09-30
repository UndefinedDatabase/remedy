# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Round 1: claim F293, re-head the ledger, book F044 R15's PASS_WITH_RISKS verdict, and run T001 —
one full-suite measurement run with collection timed separately, ranked into
`.agent/f293_inventory.md`.

## Next Steps
1. T002 — cut from the top of T001's ranking: shared setup per module, in-process CLI calls where
   the child process isn't the point, merged parametrisations; every changed test keeps a
   mutation red-proof.
2. T003 — each closure's suite transcript records CPU seconds; a closure costing >10% more than the
   previous feature's registers a finding owned by the rolling paydown; a run leaving a process
   behind fails.
3. T004 — `remedy doctor core` states the last 24 hours' run count and CPU minutes from the record.
4. amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- "CPU share per test file" in T001 is approximated from wall-clock durations under `-n auto`
  parallelism, not true per-process CPU time; the inventory states this plainly.
- The full-suite run this round is the ONE amend0917-throughput permits this feature; no round
  after this one may run it again.

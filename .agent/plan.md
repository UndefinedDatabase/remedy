# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Rounds 1 to 3 are booked PASS. Round 4 removes the real 30 s backoff sleep from
`test_callback_fires_on_retry`. The open-findings count is 2 (`R-1117`, `R-1118`). MEASURED: the
file's own suite now reads 141 passed with a 0.18s slowest entry (was the retry test's real 30.03s
in T001's ranking); canary `tests/cli/test_golden_path.py` reads 42 passed; `ruff check` on the
file is clean; `integrity check` reads `fail_count` 0; both `cmp` proofs (the saved block copy, the
committed test file against the reviewer's dry-run copy) were silent.

## Next Steps
1. T002 — cut from the top of T001's ranking (`.agent/f293_inventory.md` sections 2 and 3): shared
   setup per module, in-process CLI calls where the child process isn't the point, merged
   parametrisations; every changed test keeps a mutation red-proof. Target: the test load record's
   `cpu_seconds` at least 40% below 1246.09 (T001's own reading), or a dated DECISION with numbers
   showing no more can be cut.
2. T003 — each closure's suite transcript records CPU seconds; a closure costing >10% more than the
   previous feature's registers a finding owned by the rolling paydown; a run leaving a process
   behind fails.
3. T004 — `remedy doctor core` states the last 24 hours' run count and CPU minutes from the record.
4. amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- "CPU share per test file" in T001 is approximated from wall-clock durations under `-n auto`
  parallelism, not true per-process CPU time; the inventory states this plainly.
- T001's run and the closure's integration-gate run are the feature's two full-suite readings
  (DECISION F293 D1); no round in between runs the full suite.

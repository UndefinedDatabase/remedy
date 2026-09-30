# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Round 2 is done, T002's first cut: `dead_command_ids` (`packages/orchestration/dead_command_check.py`)
cached its per-root file scan (module-level `_SCAN_CACHE`, DECISION F293 D2), which T001 ranked as
the #1 CPU-cost driver — every call re-read and re-AST-parsed the whole `tests/`/`scripts/` tree,
~2.4s regardless of call count in the same process. Two new tests prove the cache mechanically
(call-count, per-root isolation); both mutation red-proofs (disable cache, break per-root keying)
confirmed in a disposable worktree, see `.agent/authored/f293-r2-mutations.txt`.

Targeted measurements (not full-suite — DECISION F293 D1 defers the 40%-of-1246.09 Acceptance
check to the closure's own integration-gate run):
- `tests/cli/test_worker_facade_cmd.py`: T001 125.54s/40 lines -> now 22.26s/42 lines, -82.3%.
- The other 4 T001-named files (`test_disk_floor.py`, `test_self_use_generator.py`,
  `test_self_use_runner.py`, `test_dead_command_check.py`): T001 33.53s summed -> now 15.19s, -54.7%.
- `tests/cli/` (whole dir): 2254 passed, fully green, no failures, no new skips.

Next round is T002 continued: more cuts from `.agent/f293_inventory.md` sections 2-3's remaining
top entries (`test_job_task_runner.py`, `test_supervisor_portability.py`, `test_mission_cmd.py`,
`test_do_sequence_cli.py`, etc.), or a DECISION ruling no more can be cut without weakening a test.

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
- The full-suite run this round is the ONE amend0917-throughput permits this feature; no round
  after this one may run it again.

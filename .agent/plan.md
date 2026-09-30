# Plan — F293 Test load diet

## Goal
Cut the full suite's and round selections' CPU cost by at least 40% from T001's baseline, or rule
with numbers that no more can be cut without weakening a test (docs/roadmap/features/T2_F293.md).

## Current Step
Round 3 found and resolved R-1119 in the same round: two tests in `tests/orchestration/
test_job_task_runner.py` (`TestProviderOverrideToFake::test_cli_handler_provider_override`,
`TestCommandPathExplicitOverrides::test_provider_override_to_fake`) made a real, paid subprocess
call to the installed `claude` CLI via `COMMAND_HANDLERS["job.run"]` with no fake installed — the
two single slowest tests in the suite (19.66s/12.77s, T001). Fixed by monkeypatching
`packages/orchestration/pingpong_provider.py`'s `_guarded_cli_run` seam in both tests, returning a
canned JSON response discriminated by "Reviewer" in the prompt text; both roles and the
`--version` probe covered. No production code touched. Confirmed by the same `ps -ef` polling
method that found the defect: zero real `claude` processes spawn now.

Round 2 (prior) cut T002's first item: `dead_command_ids` cached its per-root file scan
(`_SCAN_CACHE`, DECISION F293 D2) — `tests/cli/test_worker_facade_cmd.py` 125.54s -> 22.26s
(-82.3%); four other T001-named files 33.53s -> 15.19s (-54.7%); `tests/cli/` fully green.

Next round is T002 continued: more cuts from `.agent/f293_inventory.md` sections 2-3's remaining
top entries (`test_supervisor_portability.py`, `test_mission_cmd.py`, `test_do_sequence_cli.py`,
etc.), or a DECISION ruling no more can be cut without weakening a test.

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

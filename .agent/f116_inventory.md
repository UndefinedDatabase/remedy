# F116 claim inventory — what Remedy has for a cost anomaly alarm at `e80b95467`

Measured by the planner and reviewer at the F116 claim, 2026-10-07, in the primary checkout on
`main` at `e80b95467` (the merge commit of pull request 312), with
`python3 .agent/authored/f116-r1-measure.py` run from the repository root. The script reads source
text and imports two modules for their constants; it starts no job, calls no provider and writes
nothing. Its output, verbatim:

```
1. the watchdog's burn tripwire (F077)
   signature: evaluate_burn_anomaly(entries: 'Sequence[dict[str, Any]]', *, window: 'int', min_samples: 'int', multiplier: 'float') -> 'Trip | None'
   defaults: WatchdogThresholds(no_progress_repeats=3, burn_window=3, burn_min_samples=5, burn_multiplier=3.0)
   reads measured_tokens: True  reads a clock or a timestamp: False
   callers outside its definition: {'packages/orchestration/watchdog.py': 1}
   tests naming it: {'tests/orchestration/test_watchdog.py': 20}
2. the job runner's safe point
   'def _stop_check(' in pingpong_job.py: 1  calls '_stop_check(': 5
   safe_points.should_stop order: operator stop, then budget: True
3. the F103 ledger as a time series
   timestamp fields, first match wins: ('ts_utc', 'finished_at', 'started_at')
   per-call rows take ONE task-run timestamp: True
   keys of one provider attempt: ['seq', 'round', 'role', 'provider', 'is_retry', 'is_parse_retry', 'stream_call_id', 'stream_artifact_refs', 'error'] plus ['usage', 'total_cost_usd']
   cost bases: ['price_table', 'provider_reported', 'unknown']
4. expectation bands (F074 is unchecked in STATUS)
   modules naming an expectation band: {}
5. unattended mode
   escalation.auto_apply_safe_default defined: True
   commands declaring --unattended: ['job.resume']
   'unattended' in packages/orchestration/pingpong_job.py: 0
   'unattended' in packages/orchestration/long_run_executor.py: 7
   'unattended' in packages/orchestration/orchestrator_loop.py: 5
6. what F116 would add
   packages/orchestration/burn_detector.py exists: False
   tests/orchestration/test_burn_detector.py exists: False
```

## What the readings mean

- The one burn check in the product is the watchdog's, and it is self-relative and counted in
  tokens per mission iteration: no clock, no money, no expectation from outside the run. Its only
  caller is `evaluate_ledger` in the same module, so T003 has one call site to move.
- A job's run-level checks all happen at `_stop_check`, the safe point before each task, where the
  operator stop is read before the budget. T002 adds the detector there and starts no thread.
- The ledger cannot place two calls of one task run apart in time: they share the task run's one
  timestamp, and an attempt records none of its own. A window therefore spans whole task runs,
  which is also the feature file's rule that a window covers at least one full batch.
- A cost figure exists only where a provider reported one; a price table basis is declared but no
  code writes it. A detector stated in dollars must therefore say what it does when a sample has
  no price, and T001 decides that.
- No expectation band exists, so the `class_default` basis reads configuration until F074 lands.
- `pingpong_job.py`, where `remedy job run` executes, has no notion of an unattended run; only
  `remedy job resume --unattended` and the mission loop have one. T002 decides which job runs the
  pause applies to.

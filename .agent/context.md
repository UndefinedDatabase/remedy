# Context — F046 Multi-cycle loop

## Branch
`feature/f046-multi-cycle-loop`
Base commit: `c14a83a2d38cf8b91870f4c7bae225effb26f1af` (main after PR #151 merge)

## Scope
- NEW `packages/orchestration/long_run_executor.py` — the cycle conductor.
- NEW `tests/orchestration/test_long_run_executor.py`.
- T002 additions: cycle evidence records, config keys (`cycles.*`),
  `remedy job run <id> [--cycles N]` CLI.

## Constraints (A6 — reuse, do not reimplement)
- should_stop: `safe_points.should_stop()` (operator + budget in one check)
- task execution: `task_runner.run_next_task()` (rollback stays its concern)
- persistence: `storage.save_job()` — no new persistence paths
- terminal statuses map onto `pingpong_job` JOB_* constants + a ledger event

## Do not touch
`autonomy_loop.run_autonomy_loop`, task-level execution semantics, retry
policy, checkpoint depth, DAG readiness, `run_pingpong` internals.

## Rollout rule
`max_cycles` DEFAULT stays 1 until the F075 milestone gate; the CLI flag
is capped by the same safety default.

# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4869-4878: Job Runner Continuation Config Truth Closure v4.
Fix max_rounds not restored on continuation. Fix explicit --builder fake
ignored after persisted non-fake. Add source/audit fields.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- CLI args default to None (omitted). Resolution: explicit > persisted > default.
- _resolve_cfg() handles all continuation-critical fields consistently
- ExecutionConfig tracks *_source for each field: cli/persisted/default
- run_job() accepts None for builder_name, reviewer_name, max_rounds,
  repair_rounds, test_command, claude_cli_write_mode
- Catalog defaults are None for continuation-critical do.job-run args
- Handler lambda passes raw None through (no or coercion)
- validate_job_task_result() checks 7 conditions independently
- TASK_BLOCKED status for gate failures (not TASK_FAILED)
- Safe next_command for paused jobs — config persisted, report shows it
- repair_rounds=0 truly disables repair
- JOB_PAUSED status for max-tasks partial runs
- do.job-run catalog: may_execute_commands=True
- Target repo mutation blocks job + remaining tasks skipped
- Task prompt bounded (last 5 proof summaries, body truncated at 2000 chars)
- Unsafe paths (traversal, .env, .git, private keys) block workspace apply
- Task IDs deterministic by parse order, not heading number

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

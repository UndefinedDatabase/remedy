# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4845-4856: Job Runner CLI Control + Execution Metadata Closure v2.
Fix repair-round coercion, add source metadata, fix catalog truth,
add paused status, strengthen target mutation guard tests.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- repair_rounds=0 truly disables repair (fixed: `or 2` coercion removed)
- Omitted repair-rounds defaults to 2 via resolve_repair_rounds()
- repair_rounds_source tracks "cli" vs "default" at job level
- JOB_PAUSED status for max-tasks partial runs (not "running")
- do.job-run catalog: may_execute_commands=True (providers + test commands)
- Target repo mutation blocks job + remaining tasks skipped
- Task prompt bounded (last 5 proof summaries, body truncated at 2000 chars)
- Unsafe paths (traversal, .env, .git, private keys) block workspace apply
- Task IDs deterministic by parse order, not heading number

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

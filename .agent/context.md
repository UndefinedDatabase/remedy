# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4887-4895: Job Target Guard Pre-Apply Closure v6.
Move job-level target repo guard before workspace apply. Add post-apply
defense-in-depth guard. No staged files copied after target mutation.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- validate_job_task_result() checks 8 conditions
- Missing reviewer_output blocks with "missing_reviewer_output" reason
- test_passed=None is valid when no test command configured
- CLI args default to None. Resolution: explicit > persisted > default.
- ExecutionConfig tracks *_source for each field
- TASK_BLOCKED status for gate failures
- Safe next_command for paused jobs
- repair_rounds=0 truly disables repair
- JOB_PAUSED status for max-tasks partial runs
- Target repo mutation blocks job
- Task prompt bounded (last 5 summaries, 2000-char body)
- Unsafe paths block workspace apply
- Pre-apply target guard must run before _strict_apply_to_workspace
- Post-apply target guard as defense-in-depth

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4827-4831: Job Task Runner v0.
Sequential multi-task job execution with Builder/Reviewer/Repair gates per task.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- Existing task-file/short-goal flows must not regress
- Failed tests NEVER produce staged_review_passed
- Test failure checked before reviewer verdict (dominance)
- repair_rounds=0 truly disables repair
- review_inconsistent never adjudicates as ready
- Promotion blocked when final tests failed
- All repair loops bounded by hard cap (10)
- Evidence export: no provider calls, no target mutation
- Evidence export: all output (files + API return) recursively redacted
- Job runner: real target repo never mutated
- Job runner: task N+1 starts only after task N passed + applied to workspace
- Job runner: failed/exhausted task blocks job, remaining tasks skipped
- Job runner: task prompt bounded (last 5 summaries, body truncated at 2000 chars)

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

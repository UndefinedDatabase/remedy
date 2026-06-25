# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4706-4723: Scope Plan Approval Gate v0.
Add deterministic scope planning, user decision editing, validated execution,
scope contracts in Builder/Reviewer prompts, scope data in reports.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No provider calls during planning
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- Existing task-file/short-goal flows must not regress

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
- Use scripts/remedy_pytest.sh wrapper for bounded execution

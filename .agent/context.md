# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4799-4806: CLI Repair Default Truth Closure v5.
Fix CLI dispatch so omitted --repair-rounds stays None (default=2), not coerced to 0.

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

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

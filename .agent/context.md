# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4807-4811: Run Evidence Bundle v0.
Export a self-contained, safe proof bundle for any Remedy run.

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
- Evidence export: no raw task body, no secrets/env/keys
- Evidence export: path traversal blocked, output inside requested dir only

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

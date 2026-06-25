# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4773-4787: Repair Governance Correctness Closure v3.
Fix 5 real correctness bugs found by review in repair governance v2.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- Existing task-file/short-goal flows must not regress
- repair_rounds=0 truly disables repair (no legacy fallback)
- CLI default: --repair-rounds omitted → 2 (via resolve_repair_rounds(None))
- review_inconsistent never adjudicates as ready
- All repair loops bounded by hard cap (10)
- Promotion blocked after exhausted/inconsistent repair

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

# Context

## Active Branch
feature/steps-3096-3145-runtime-cleanup-finalization-v0.3
(forked from main at b82d961 after PR #96 merged).

## Scope
Steps 3096-3145: Runtime Lane Process Cleanup + Review Bundle Runtime Finalization v0.3.
Harden subprocess helper with process-group isolation. Add diagnostics to runtime
script. Verify no orphan processes after test runs.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No new feature layer, no provider execution
- No auto-apply/PR/merge, no shell=True, no provider SDK
- Legacy development reads are classified and whitelisted
- New product paths must not introduce live_review.md dependency

## Resource safety
- All pytest tests must run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
- Use scripts/remedy_pytest.sh wrapper for bounded execution

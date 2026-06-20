# Context

## Active Branch
feature/steps-3146-3215-job-centric-core-v0
(forked from main at 462121e after PR #97 merged).

## Scope
Steps 3146-3215: Job-Centric Core Finalization v0.
Make job the primary user-facing concept. Add job status/report facades.
Update docs and Happy Path. Keep mission as advanced/internal.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No new execution capability, no provider SDK, no shell=True
- No auto-apply/PR/merge
- Job facades are read-only wrappers over existing state
- Mission remains as compatibility/advanced facade

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
- Use scripts/remedy_pytest.sh wrapper for bounded execution

# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4906-4916: Job Evidence Bundle v0.
Add remedy do job-evidence command producing redacted, human-readable,
machine-verifiable proof bundle for entire job.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- Job evidence export is read-only
- Export calls no providers
- Export mutates no target repo or job state
- All emitted files redacted
- Output path traversal blocked
- Raw task body not dumped unbounded
- No secrets leaked
- Reuse existing redaction helpers

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

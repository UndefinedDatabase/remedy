# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4917-4926: Job Evidence Nested Path Containment Closure v1.
Close nested task evidence path traversal vulnerability in job evidence export.

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
- Output path traversal blocked (top-level and nested task evidence)
- Nested task evidence paths validated via _task_evidence_dir()
- Raw task body not dumped unbounded
- No secrets leaked
- Reuse existing redaction helpers

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

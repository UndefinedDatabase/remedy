# Context

## Active Branch
feature/steps-3276-3355-job-fulfillment-spine-v0

## Scope
Steps 4927-4936: Job Evidence Symlink Containment Closure v2.
Close symlink escape in nested task evidence paths.

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
- Nested task evidence paths validated via _task_evidence_dir -> _validate_output_path
- _validate_output_path uses .resolve() which follows symlinks
- Raw task body not dumped unbounded
- No secrets leaked
- Reuse existing redaction helpers

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path

# Context

## Active Branch
`feature/f001-adaptive-provider-timeouts` (PR #123 → `main`), closing F001–F003.
Next: `feature/f004-raw-stream-evidence` after #123 merges.

## Scope
F003 — Real token/cost measurement — externally accepted (PASS_WITH_RISKS).
Commit the accepted 22-file source/test change, then build F004 (raw stream
evidence) conventionally.

## Development-only artifacts
`.agent/live_review.md` is a development-time coordination artifact ONLY.
Product code must NOT depend on `.agent/live_review.md`.

## Constraints
- No Fable; no nested Builders/Reviewers/subagents; no `job-flow`/`job-run` for
  implementation. Tier 0 is built conventionally by the operator.
- No auto-execution from plan
- No auto-promotion from run
- No git commit/push/reset in product code
- Job evidence export is read-only
- Export calls no providers
- Export mutates no target repo or job state
- All emitted files redacted
- Output path traversal blocked (top-level and nested task evidence)
- Nested task evidence paths validated via _task_evidence_dir -> _validate_output_path
- Raw task body not dumped unbounded
- No secrets leaked
- Reuse existing redaction helpers
- Verification commands are explicit and actually executed; nothing is claimed
  verified that was not run
- Manual-completion evidence rides existing artifacts only — no new evidence
  file, gate, taxonomy, or schema family
- Provenance hashes are recomputed and verified, never trusted at face value

## F004 constraints (upcoming)
- `--stream-evidence` is opt-in; default remains the F003 JSON mode
- Redact before any raw bytes are persisted
- Bounded raw JSONL (50 MB/task) with honest stop/rotate, never silent truncation
- Every normalized event carries a raw line/byte offset backreference
- `agent_run_trace` prefers normalized `run_events.jsonl`, falls back to legacy
  reconstructed evidence, and records which source it used

## Resource safety
- All pytest tests run within per-test resource limits
- No subprocess spawning, no network calls, no filesystem mutations outside tmp_path
  (the single tiny live smoke is an explicit, separately-evidenced exception)

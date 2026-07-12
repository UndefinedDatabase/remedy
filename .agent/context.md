## Current feature

F007 — Runtime harness (branch `feature/f007-runtime-harness`, base `d969688`).
`remedy runtime serve|probe|stop` over `packages/runtimes/dev_server.py` and
`runtime_config.py`. F006 is merged (PR #126). F008 is NOT in scope.

# Context — Steps 5961-6020

## Active Branch
`feature/f005-structured-outputs` (F005 — enforced structured outputs).
F001–F004 accepted and merged (F004 = PR #124, merge commit `cb55909`).

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

## F005 constraints (current)
- Schemas live in `packages/orchestration/schemas/`; small Pydantic models with a
  compact `schema_v`; `to_json_schema()` export; no mega-schemas, no new taxonomy.
- Every structured provider call: send JSON schema, validate response, invalid =
  error class `parse`, at most ONE parse retry carrying only a concise validation
  hint, never an unbounded repair loop.
- Old free-text parsers stay behind an explicit temporary compatibility flag;
  schema mode never silently falls back to free-text parsing.
- Prompt trace records `schema_v` per structured call; provider-call and token
  accounting stay correct across the one retry.
- Planner compatibility fallback is not removed until >= 5 deterministic green
  planner runs are recorded (feature-document rule).

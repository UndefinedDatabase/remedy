# Live Review — Steps 4807-4811: Run Evidence Bundle v0

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
PENDING

## Commit reviewed
9d1591a — Steps 4807-4811: Run Evidence Bundle v0

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Builder handoff

### What changed
New `remedy do evidence <run_id> --out <dir> --json` command that exports a self-contained, safe proof bundle for any persisted Remedy run.

### Files changed
- `packages/orchestration/pingpong_evidence.py` (new, 420 lines) — evidence bundle builder, redaction, file writer
- `apps/cli/commands/do_cmd.py` (32 lines added) — `_cmd_do_evidence` handler + COMMAND_HANDLERS entry
- `apps/cli/command_catalog.py` (16 lines added) — `do.evidence` CommandEntry
- `tests/orchestration/test_evidence_bundle.py` (new, 415 lines) — 35 tests
- `tests/orchestration/test_repair_loop.py` (3 lines changed) — ruff I001 autofix
- `.agent/plan.md` — updated
- `.agent/context.md` — updated

### Step-by-step results

**Step 4807 — Evidence bundle builder**
`build_evidence_bundle()` loads persisted run JSON + optional promotion JSON, produces deterministic bundle dict. Sections: manifest, summary_md, safe_diff, tests, review, repair_loop, promotion, token_accounting, provider_evidence. No provider calls. No target mutation. No raw task body — only hash/size/excerpt.

**Step 4808 — CLI command**
`remedy do evidence <run_id> --out <dir> --json`. Dispatched via `COMMAND_HANDLERS["do.evidence"]`. Catalog entry: `action_class="read_only"`, `may_mutate_repo=False`, `may_execute_commands=False`. Output files: manifest.json, summary.md, safe.diff, tests.txt, review.json, repair_loop.json, promotion.json, token_accounting.json, provider_evidence.json.

**Step 4809 — Redaction and safe-output**
- `_redact_secrets()`: removes OpenAI/Anthropic/AWS/GitHub/GitLab key patterns, Bearer tokens, env var assignments
- `_sanitize_path()`: replaces `$HOME` prefix with `~`
- `_validate_output_path()`: blocks `..` traversal via `Path.resolve()` check
- No raw `task_body` in output — only `task_input` metadata (hash, size, excerpt)
- No `os.environ`, no `getenv`, no env leakage
- summary.md does not contain `staging_path`
- All file writes validated through `_validate_output_path`

**Step 4810 — Tests (35 total)**
- `TestEvidenceBundleBuilder` (15 tests): no-repair, repair, exhausted, promotion, manifest, summary, diff, tests, review, repair_loop, token_accounting, provider_evidence, missing sections, task input
- `TestEvidenceCli` (5 tests): nonexistent run, no-repair, repair, exhausted, promotion
- `TestRedaction` (8 tests): task body, API keys, env vars, path sanitization, staging paths, path traversal, bundle file redaction
- `TestSafety` (4 tests): no provider call, no target mutation, output confinement, deterministic
- `TestCliDispatch` (3 tests): handler exists, catalog entry, read_only

**Step 4811 — Architecture guard**
All clean:
- No `shell=True` in evidence module
- No provider calls (`create_provider`, `ClaudeCliProvider`, etc.)
- No git mutations (`git commit/push/reset/checkout`)
- No auto-promote, no `--approve`
- No `task_body` access
- No `os.environ` / `getenv`
- No `live_review.md` product dependency
- Writes only inside requested output directory (path traversal blocked)

### Test evidence
- Evidence bundle tests: 35/35 pass
- Repair loop tests: 131/131 pass
- Job fulfillment tests: 109/109 pass (twice, deterministic)
- Fast lane: 571/571 pass
- Runtime lane: 57/57 pass (4/4 suites)
- Lint: ruff clean, mypy clean (199 source files)
- Full suite: 7712 passed, 8 skipped, 1 deselected, 0 failed (266s)

### What this proves
- A human can export a safe proof bundle for any persisted Remedy run
- Bundle answers all required questions (task, providers, tokens, diff, tests, review, repair, promotion, readiness)
- No secrets, env vars, API keys, or raw task body leaked
- Evidence export is deterministic, read-only, and confined to output directory
- Path traversal blocked
- Existing repair/promotion/task-file/scope safety intact

### What this does not prove
- Real Claude CLI dogfood (requires API key + live run)
- UI rendering of evidence bundle
- Multi-run aggregation or comparison
- Streaming evidence for large runs

### Carry-forward
No open findings from previous blocks. All prior reviewer verdicts: PASS.
R-2206 (Low, ruff I001) from v5 resolved by autofix in this commit.

### Review quiet-window
- Final review file check: 2026-06-25 ~14:58 UTC
- live_review.md last modified: ~71 minutes before handoff
- No reviewer activity detected
- No findings requiring Builder action

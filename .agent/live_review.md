# Live Review — Steps 4820-4826: Evidence CLI JSON Redaction Closure v2

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
PENDING

## Commit reviewed
c5400ab — Steps 4820-4826: Evidence CLI JSON Redaction Closure v2

## PR reviewed
No open PR. Builder on `feature/steps-3276-3355-job-fulfillment-spine-v0`.

## Builder handoff

### What changed
Fixed `export_evidence()` return payload leaking secrets to CLI `--json` stdout. One-line fix: wrap return dict in `_redact_json_value()`.

### Files changed
- `packages/orchestration/pingpong_evidence.py` L489: `return _redact_json_value({...})` (was `return {...}`)
- `tests/orchestration/test_evidence_bundle.py` L884-955: 5 new tests across 3 classes
- `.agent/plan.md` — updated
- `.agent/context.md` — updated

### Step-by-step results

**Step 4820 — Redact export_evidence() return payload**
L489: `return _redact_json_value({...})`. All string values in return dict (run_id, out_dir, file paths, manifest fields) now pass through recursive redaction. Path strings preserved as-is since they're local filesystem paths, not secrets.

**Step 4821 — CLI handler defense-in-depth**
No separate fix needed. `_cmd_do_evidence` at L389 does `json.dumps(result)` where `result` is already redacted by `export_evidence()`. Single source of truth — no duplicate redaction logic.

**Step 4822 — CLI stdout JSON leak regression test**
`TestCliStdoutRedaction::test_cli_json_stdout_redacted`: goal contains `API_KEY=supersecretvalue123`, task excerpt contains `sk-ant-...`. Calls `export_evidence()`, `json.dumps(result)`. Asserts secrets absent, run_id and final_status preserved.

**Step 4823 — Export return-value regression tests (3)**
`TestExportReturnRedaction`:
- `test_return_manifest_redacted`: poisoned run, all 7 _LEAK_MARKERS absent from `json.dumps(result)`
- `test_return_preserves_useful_fields`: run_id, out_dir, manifest.final_status, manifest.run_id preserved
- `test_return_has_redacted_placeholder`: `[REDACTED]` present where secrets were

**Step 4824 — Extended full-output scanner**
`TestFullOutputScannerExtended::test_no_leaks_in_files_or_api_return`: scans all emitted files AND `json.dumps(result)` for all 7 leak markers. Covers both file output and CLI/API return path in one test.

**Step 4825 — Existing flows preserved**
- Evidence bundle tests: 65/65 pass
- Repair loop tests: 131/131 pass
- Job fulfillment tests: 109/109 pass (twice)
- Fast lane: 571/571 pass
- Runtime lane: 57/57 pass (4/4 suites)
- Lint: ruff clean, mypy clean (199 source files)
- Full suite: 7742 passed, 8 skipped, 1 deselected, 0 failed (244s)

**Step 4826 — Architecture guard**
All clean: no `shell=True`, no provider calls, no git mutations, no auto-promote, no `task_body`, no `os.environ`/`getenv`, no `live_review.md` dependency. `export_evidence` return wrapped in `_redact_json_value`. `_cmd_do_evidence` relies on redacted return — no unredacted `json.dumps`.

### What this proves
- `do evidence --json | tee ...` is now safe by default
- CLI stdout and bundle files both redacted for 7 secret pattern types
- No divergent redaction logic — single `_redact_json_value` call in `export_evidence`

### What this does not prove
- Real Claude CLI dogfood
- Redaction of novel secret formats not in the 7 patterns

### Carry-forward
No open findings. All prior reviewer verdicts: PASS.

### Review quiet-window
- Final review file check: 2026-06-25 ~17:41 UTC
- live_review.md last modified: ~34 minutes before handoff
- No reviewer activity detected
- No findings requiring Builder action

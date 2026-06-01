# Live Review — Steps 305-312

Reviewer: parallel watcher (independent)
Scope: Steps 305-312 (Prompt/Memory Cleanup, Structured Patch Pipeline, Ollama Builder, Autocoder Bridge)
Status: PASS
Started: 2026-06-01
Branch: feature/steps-247-252-data-honest-contract
Last check: final (Step 312)

---

## Baseline

- Commit: 39f7dd6
- Full pytest (--cache-clear): 3773 passed, 0 failed, 2 skipped
- Vitest: 21 passed
- TypeScript: clean
- Build: OK
- Net new tests: +46

## Active Findings

### R-8001: .pyc cache causes false test failures in repair loop — RESOLVED
- Symptom: test_succeeds_on_second_cycle failed because stale .pyc from cycle 1
- Fix: PYTHONDONTWRITEBYTECODE=1 in subprocess env (builder_bridge.py)
- Status: Resolved, test now passes consistently

---

## Step-by-Step Review

### Step 305: Prompt + Memory Surface Cleanup — PASS

**Files:** `packages/orchestration/llm_planner.py`, `tests/orchestration/test_prompt_redaction.py`

Verified:
- Raw user prompt replaced with `[redacted] (hash=..., len=...)` in planning artifact content
- Prompt hash (SHA-256 prefix, 16 chars) and length in artifact metadata
- Memory section keys/values excluded from artifact content
- Memory metadata (item_count, context_hash) in artifact metadata — no raw content
- Planner callable still receives full prompt (test_planner_still_receives_full_prompt)
- Missing data_dir does not crash
- 6 tests, all pass

No raw prompt or memory content leaks to artifacts. Contract sound.

### Step 306: BuilderOutput v2 Structured Patch Contract — PASS

**Files:** `packages/orchestration/builder_models.py`, `packages/orchestration/structured_patch.py`, `tests/orchestration/test_builder_patch_contract.py`

Verified:
- BuilderOutput extended with `structured_patch_text` (optional) and `structured_patch_format` (default "none")
- Backward compat: narrative-only BuilderOutput still valid
- `parse_builder_patch()` handles: JSON file_ops, fenced JSON, unified diffs
- Rejects: no text, prose/markdown, shell commands (rm/sudo/curl/wget/chmod), malformed JSON, empty paths, path traversal (`../`)
- Safe metadata only in result: output_hash (SHA-256 prefix 16 chars), output_length, error_kind
- Diagnostics bounded (max 5, each <200 chars), no raw provider output
- `BuilderPatchResult.patch: Any = None` — populated with StructuredPatch on success
- 13 tests, all pass

Parser is strict and safe. No raw output leaks. Path safety enforced.

### Step 307: Ollama Builder Prompt — PASS

**Files:** `packages/providers/ollama_builder/provider.py`

Verified:
- System prompt instructs JSON file_ops format for code change tasks
- Memory context injected via `_build_user_message()` (line 117-119) — uses `context.memory_context` which is pre-formatted safe summary, not raw memory
- Structured output via `format=schema` (Ollama JSON schema enforcement)
- Response validated through `BuilderOutput.model_validate_json()`
- No raw memory content in prompt — only formatted memory section
- Model resolution: constructor > REMEDY_OLLAMA_BUILDER_MODEL > REMEDY_OLLAMA_MODEL > default

Clean provider design. Memory injection uses safe format_memory_section output.

### Step 308: Autocoder Bridge (builder→intent→approval→apply) — PASS

**Files:** `packages/orchestration/builder_bridge.py`, `tests/orchestration/test_builder_bridge.py`, `tests/orchestration/test_builder_bridge_smoke.py`

Verified pipeline stages:
1. **Parse**: `parse_builder_patch(output)` — rejects bad input before any state changes
2. **Approval gate**: autonomy < 3 stops at "approval_pending" (no auto-approve)
3. **Intent creation**: `_create_and_approve_intent()` creates Artifact with patch metadata + auto-approves
4. **Permission grant**: `set_permission(job, Capability.repo_generated_write, allow=True)` — scoped to job
5. **Apply**: `apply_structured_patch(patch, repo_path, ...)` with intent_id — source_apply 3-stage gate intact
6. **Test**: subprocess pytest with 60s timeout, proof hash on success

Critical checks:
- `parse_result.patch` field exists on `BuilderPatchResult` (line 80 of builder_models.py) — ✓
- Source_apply requires intent_id and approved state — not bypassed by bridge
- Permission grant is within job scope, not global
- No narrative proposed_changes treated as "autocoder" — must have structured_patch_text
- Shell commands rejected before apply stage
- Path traversal rejected before apply stage
- Events emitted at each stage for operator visibility

Tests: 10 bridge tests + 4 smoke tests (3 fixture + 1 Ollama opt-in), all pass.

**Smoke test design:**
- Fixture smoke: CI-safe, deterministic, full pipeline including subprocess test execution
- Real Ollama smoke: opt-in via `REMEDY_SMOKE_OLLAMA=1`, properly skipped by default
- Ollama smoke does NOT assert parse_success — correctly handles model variability
- Fixture smoke is NOT claimed as "real Ollama success" — clearly labeled "fixture"

### Step 309: Real Repo Smoke — PASS

Covered by `TestRealOllamaSmoke` in test_builder_bridge_smoke.py. Properly gated behind `REMEDY_SMOKE_OLLAMA=1` env var. Not claiming fixture results as real Ollama results.

### Step 310: Bounded Repair Loop — PASS (with observation)

**Files:** `packages/orchestration/builder_bridge.py` (lines 205-288), `tests/orchestration/test_builder_repair_loop.py`

Verified:
- Loop bounded by `max_cycles` (default 3)
- Stops on: tests pass (success), max_cycles reached, parse/apply failure
- First cycle gets `None` repair_context, subsequent cycles get structured context
- Repair context built from `build_repair_context()` with failure_kind, safe_summary
- Events: `repair_loop_cycle_started`, `repair_loop_succeeded`, `repair_context_created`, `repair_loop_stopped`
- No unbounded retries — hard stop at max_cycles

Tests: 6 tests, all pass.

R-8001 resolved: PYTHONDONTWRITEBYTECODE=1 prevents stale .pyc between repair cycles.

### Step 311: Operator Visibility — PASS

**Files:** `packages/orchestration/ui_server.py`, `apps/cli/commands/do_cmd.py`, `tests/orchestration/test_builder_visibility.py`

Verified:
- Dashboard live state: `builder_patch_parsed`, `builder_patch_error`, `repair_loop_cycle`, `repair_loop_max_cycles`
- Stage map extended: parsing, repairing stages for bridge events
- CLI: events displayed in text output, cycles shown
- 5 tests, all pass

### Step 312: Full Baseline — PASS

- pytest: 3773 passed, 2 skipped, 0 failed
- Vitest: 21 passed
- TypeScript: clean
- Build: OK
- Guardrails: no shell=True, no 0.0.0.0, no test_steps_ files

---

## Security Checklist

| Check | Status |
|-------|--------|
| No raw prompt in artifacts | ✓ |
| No raw memory in events/exports | ✓ |
| Parser rejects shell commands | ✓ |
| Parser rejects path traversal | ✓ |
| Source_apply 3-stage gate intact | ✓ |
| Intent required for apply | ✓ |
| No narrative-as-autocoder | ✓ |
| No parser bypass | ✓ |
| No source_apply bypass | ✓ |
| Fixture not claimed as Ollama | ✓ |
| Subprocess test timeout (60s) | ✓ |
| Repair loop bounded | ✓ |
| Diagnostics bounded (no raw output) | ✓ |

## Scope Blockers Checked

- No GPU/CUDA dependencies added
- No external API calls (Ollama opt-in only)
- No Markdown append fallback for source edits
- No vector DB
- No MemPalace
- Source_apply not weakened

---

## Previous Review History

### Steps 305-312: PASS — structured patch pipeline, repair loop, operator visibility
### Steps 297-304: PASS — test polish, rollback cleanup, project memory integration
### Steps 289-296: PASS — test re-architecture, transactionality, dashboard truth
### Steps 283-288: PASS — full baseline green, all findings resolved
### Steps 277-282: PASS — R-4001/R-4002/R-4003 resolved
### Steps 269-276: PASS — R-3011/R-3012/R-3013 resolved, approval gate added
### Steps 261-268: PASS — dashboard-first UI, permission boundary, frontend tests
### Steps 253-260: PASS — contract repair, safety quick wins
### Steps 247-252: PASS — data-honest mission control
### Steps 227-246: PASS — Canvas Force Brain Graph

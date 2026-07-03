# Steps 5481-5510 R2: Review Scope Packet Integration First

## Product goal

Implement Review Scope Packet as an integrated evidence feature, then continue with the remaining core functionality (token-saving reviewer prompts, missing tests gate, final verifier report, token truth).

This is a functionality run. No UX polish.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, no `_pt_check.py`, no temporary Python scripts at repo root. If you need to test something, write the test in the proper test file and run pytest.
- Do NOT change review zip filename pattern.
- Do NOT do UX polish (no CSS, no frontend components, no graph changes).
- Do NOT expose raw prompts, raw diffs, raw stdout/stderr, secrets, or local absolute paths.
- Do NOT use variable names or string literals containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, or strings containing `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings like `marker_string = "SCOPE_PACKET_TEST_BODY_SHOULD_NOT_LEAK"` instead.
- All new test files must use redaction-safe fixture patterns.
- If T001 cannot pass review, STOP. Do not continue to T002-T005.

---

## Task 1: Review Scope Packet — integrated evidence feature

### What to build

Create `packages/orchestration/review_scope.py` with `build_review_scope_packet()` that generates a deterministic review-scope packet for each completed task.

Then integrate it into the job evidence pipeline so packets are written automatically.

### Files allowed

- `packages/orchestration/review_scope.py` (new)
- `packages/orchestration/pingpong_job.py` (modify — integration call)
- `tests/orchestration/test_review_scope.py` (new)

Do NOT create any other files. Do NOT create scratch files at repo root.

### Function signature

```python
def build_review_scope_packet(task, workspace, evidence_dir) -> dict:
```

- `task`: A `TaskEntry` or dict with `task_id`, `title`, `test_passed`, `repair_rounds_used`, `safe_diff_files`
- `workspace`: Path to the job workspace (for related test discovery)
- `evidence_dir`: Path to job evidence dir containing `task_runs/<task_id>/...`

### Packet schema (JSON)

All fields required. Missing values must be explicit (empty list, `false`, `0`), never silently absent.

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "task_title": "...",
  "changed_files": ["packages/orchestration/ui_server.py"],
  "changed_line_ranges": {
    "packages/orchestration/ui_server.py": [[45, 60], [120, 135]]
  },
  "changed_symbols": {
    "packages/orchestration/ui_server.py": ["_build_prompt_trace", "_redact_preview"]
  },
  "risk_tags": {
    "packages/orchestration/ui_server.py": ["security:redaction", "new_function"]
  },
  "prompt_hashes": ["feedface..."],
  "worker_prompt_refs": ["task_runs/T001/prompt_trace.jsonl"],
  "reviewer_prompt_refs": [],
  "evidence_refs": ["task_runs/T001/safe.diff", "task_runs/T001/tests.txt"],
  "related_tests": ["tests/ui_server/test_prompt_trace_payload.py"],
  "test_results": {"ran": false, "passed": 0, "failed": 0, "summary": "tests not run"},
  "open_findings": [],
  "repair_rounds": 0,
  "estimated_review_tokens": 2400,
  "recommended_scope": "hunk_only",
  "scope_reason": "Single file changed, 1 hunk, no cross-file dependencies detected"
}
```

### Risk tags — exact set

Per changed file, assign zero or more tags:

- `new_file` — diff header shows `--- /dev/null` or hunk starts `@@ -0,0 +...`
- `new_function` — added lines contain function/class definitions
- `test_change` — file path starts with `tests/` or contains `/tests/` or filename starts with `test_`
- `config_change` — file extension is `.json`, `.toml`, `.yaml`, or `.yml`
- `security:redaction` — added code contains `_redact`, `_sanitize`, or `_safe_`
- `security:auth` — added code (lowercased) contains `_auth`, `authenticate`, `authorize`, `permission`

### Symbol detection — line-based only

Detect symbols from added diff lines (lines starting with `+` after stripping the `+` prefix). Only match lines whose stripped content starts with one of:

- `def <name>`
- `class <name>`
- `function <name>`
- `const <name> =`
- `export <name>`

Do NOT match symbols inside multi-line strings, docstrings, comments, or embedded diff text in test fixtures. Line-based matching on stripped added lines is sufficient to avoid this.

### New file detection

A file is new if its diff header shows `--- /dev/null` OR its first hunk header is `@@ -0,0 +...`. Tag it `new_file`.

### Open findings — correct collection

Open findings must be collected from multiple sources:

1. `repair_loop.json` field `open_findings`:
   - May be a list of strings like `["F1", "F2"]` — represent each as `{"id": "F1"}`
   - May be a list of dicts like `[{"id": "F1", "severity": "high", "summary": "..."}]` — include as-is
2. `review.json` field `reviews` — the last review entry:
   - If verdict is `needs_repair`, `fail`, or `blocked`, include its findings
   - Do NOT only check for `fail` — `needs_repair` findings are also open

If a task is blocked or repair_exhausted, `open_findings` must NOT be empty unless there truly are no findings.

### Scope recommendation logic

- `hunk_only`: single file, small diff (1 hunk), no cross-file imports changed
- `file_level`: single file with multiple hunks, or symbol renames
- `cross_file`: changes span multiple files with import/call relationships
- `full_job`: security-tagged changes, test failures, or repair rounds > 1

### Test results

- If `tests.txt` is empty or missing: `{"ran": false, "passed": 0, "failed": 0, "summary": "tests not run"}`
- Parse pytest-style output: `N passed`, `N failed`, `N error`
- Use task's `test_passed` field as supplemental signal

### Estimated review tokens

- Prefer `token_accounting.json` field `reviewer_prompt_tokens_estimated` if available and > 0
- Fallback: `200 + len(diff_text) // 4`

### Markdown summary

Also generate a Markdown summary (`review_scope_packet.md`):

```markdown
## Review Scope: T001 — Review Scope Packet

**Scope:** hunk_only
**Reason:** Single file changed, 1 hunk, no cross-file dependencies

### Changed files
| File | Lines | Risk | Symbols |
|------|-------|------|---------|
| packages/orchestration/review_scope.py | 1-446 | new_file, new_function | build_review_scope_packet, _parse_diff |

### Tests
tests not run

### Findings
None
```

### Integration into evidence pipeline

Modify `packages/orchestration/pingpong_job.py`:

After a task's builder-reviewer-repair loop completes (regardless of outcome), call `build_review_scope_packet()` and write the result:

```python
from packages.orchestration.review_scope import build_review_scope_packet

packet = build_review_scope_packet(task_entry, workspace_path, evidence_dir)
# Write JSON
packet_path = evidence_dir / "task_runs" / task_id / "review_scope_packet.json"
packet_path.write_text(json.dumps(packet, indent=2) + "\n")
# Write Markdown
md_path = evidence_dir / "task_runs" / task_id / "review_scope_packet.md"
md_path.write_text(render_scope_markdown(packet) + "\n")
```

Add a `render_scope_markdown(packet) -> str` function to `review_scope.py`.

### Tests

Write `tests/orchestration/test_review_scope.py` with at minimum:

1. `test_single_file_hunk_only` — single-file single-hunk diff → `hunk_only` scope, correct line ranges
2. `test_multi_file_cross_file` — multi-file diff with imports → `cross_file` scope
3. `test_new_file_risk_tag` — `--- /dev/null` diff → `new_file` risk tag
4. `test_test_file_risk_tag` — test file path → `test_change` risk tag
5. `test_config_file_risk_tag` — `.json`/`.toml`/`.yaml`/`.yml` → `config_change` risk tag
6. `test_security_redaction_tag` — file with `_redact` → `security:redaction` tag
7. `test_security_auth_tag` — file with `authenticate` → `security:auth` tag
8. `test_symbol_detection_line_based` — symbols detected from added lines only
9. `test_symbol_detection_ignores_embedded_diffs` — embedded diff strings in test fixtures do not produce false symbols
10. `test_open_findings_from_string_list` — `repair_loop.open_findings: ["F1"]` → findings represented
11. `test_open_findings_from_needs_repair` — `review.json` with `needs_repair` verdict → findings included
12. `test_packet_json_written` — integration: packet file written to evidence dir
13. `test_packet_markdown_written` — integration: markdown file written to evidence dir
14. `test_missing_tests_explicit` — no test output → `test_results.ran` is `false`
15. `test_no_scratch_files` — verify no files created at repo/workspace root

Run: `python3 -m pytest tests/orchestration/test_review_scope.py -q`

All tests must pass. If tests fail, do not continue.

---

## Task 2: Token-saving reviewer prompts

### What to change

Modify `_build_reviewer_prompt()` in `packages/orchestration/pingpong_loop.py` to use the review scope packet when available.

**Current:** Reviewer receives full goal, full builder summary, full diff, full test output.

**New behavior:** If `review_scope_packet.json` exists for this task:
1. Add scope instruction to reviewer prompt: "Focus your review on the changed files and line ranges listed below. Do not review unrelated files unless a risk tag requires cross-file analysis."
2. Include changed line ranges from packet
3. Include risk summary from packet
4. Include related test outputs (not all test outputs)
5. Include prompt trace refs for provenance

**Fallback:** If no scope packet exists, fall back to current behavior (full context).

**Safety preserved:** Reviewer prompt must still include:
- "If you detect a security concern, escalate to full_job scope"
- "If the change modifies imports or exports, check callers"
- All current reviewer instructions remain

### Integration

Pass `review_scope_packet` dict to `_build_reviewer_prompt()` as an optional `scope_packet` kwarg.

### Tests

Add `tests/test_reviewer_prompt_scope.py`:
- Reviewer prompt includes scope instruction when packet exists
- Reviewer prompt falls back to full context when no packet
- Reviewer prompt includes changed line ranges from packet
- Reviewer prompt preserves all safety instructions
- Reviewer prompt includes risk summary

---

## Task 3: Missing Tests Gate

### What to build

Add a check in `pingpong_job.py` final status determination.

After determining all tasks are done, check if any task changed source code but had no tests run.

```python
def _check_missing_tests(job) -> list[str]:
    missing = []
    for task in job.tasks:
        if task.status not in ("applied", "staged_review_pass"):
            continue
        source_changed = any(
            not f.startswith("tests/") and not f.endswith((".md", ".json", ".toml", ".yaml", ".yml", ".css"))
            for f in (task.safe_diff_files or [])
        )
        tests_ran = bool(task.test_passed is not None)
        if source_changed and not tests_ran:
            missing.append(task.task_id)
    return missing
```

If missing tests detected:
- Add `missing_tests_tasks` to job report
- Final audit note: `NEEDS_TESTS` — do not silently say `READY_FOR_APPROVAL`
- Write `missing_tests_report.json` to evidence dir

Do NOT block the job. Human can still approve.

### Tests

Write `tests/test_missing_tests_gate.py`:
- Task with source changes and no tests → flagged
- Task with only test changes → not flagged
- Task with only docs/config changes → not flagged
- Task with source changes AND tests → not flagged
- Multiple tasks, some missing → only missing ones flagged
- Report JSON is written to evidence

---

## Task 4: Final Verifier Report

### What to build

Add `packages/orchestration/final_verifier.py` with:

```python
def build_final_verifier_report(job_id, evidence_dir) -> dict
```

Reads all evidence and produces a deterministic verdict.

**Inputs (from evidence_dir):**
- `job_flow.json`
- `self_run_observability_index.json`
- `task_runs/*/review_scope_packet.json`
- `command_transcript.json`
- `target_guard.json`
- `task_runs/*/review.json`
- `task_runs/*/repair_loop.json`
- `task_runs/*/token_accounting.json`
- `task_runs/*/tests.txt`
- `task_runs/*/manifest.json`

**Verdict logic:**
- `PASS`: all tasks reviewed and passed, all tests pass, no unresolved findings, no missing tests
- `PASS_WITH_RISKS`: all tasks reviewed, tests pass, but some tasks have risk tags or missing tests acknowledged
- `NEEDS_TESTS`: source changed without tests
- `NEEDS_REPAIR`: unresolved findings exist
- `BLOCKED`: critical evidence missing (no review for >50% of tasks), or safety check failed

**Output:** `final_verifier_report.json` with verdict, changed files, unresolved findings, test status, token summary, prompt count, safety status, evidence completeness, recommended action.

### Tests

Write `tests/test_final_verifier.py`:
- All green → PASS
- Missing tests → NEEDS_TESTS
- Unresolved findings → NEEDS_REPAIR
- Missing reviews → BLOCKED
- Token summary aggregation
- Evidence completeness check
- Report has all required schema keys

---

## Task 5: Token truth + verification

### What to build

Enhance `_build_token_accounting_json()` in `packages/orchestration/pingpong_evidence.py`:

New fields:
- `schema_version`: `"1.0.0"`
- `total_estimated_tokens`
- `builder_estimated_tokens`
- `reviewer_estimated_tokens`
- `repair_estimated_tokens`
- `per_task`: breakdown by task ID
- `measurement`: `"estimated"` | `"actual"` | `"unavailable"`
- `measurement_source`: e.g. `"prompt_chars_div_4"`
- `provider`: e.g. `"claude-cli"`
- `missing_data`: list of task IDs without token info
- `actual_tokens`: `null` when not available — do NOT fake

### Verification

After all features are built:
- `review_scope_packet.json` can be generated for a sample diff
- Missing tests gate flags tasks correctly
- `final_verifier_report.json` produces correct verdict
- Token accounting distinguishes estimated vs actual
- No root scratch files exist
- No raw prompts, secrets, or absolute paths leak

### Tests

- Token accounting includes measurement field
- measurement is "estimated" when no actual data
- per_task breakdown sums to total
- missing_data lists tasks without token info
- actual_tokens is null when not available

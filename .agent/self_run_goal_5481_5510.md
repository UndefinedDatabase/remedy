# Steps 5481-5510: Review Scope Packet + Missing Tests Gate + Final Verifier v1

## Product goal

Make Remedy cheaper, safer, and more reviewable by adding four backend features:
1. Review Scope Packet — tells the reviewer exactly what to inspect
2. Token-saving reviewer prompts — reviewer reads only relevant hunks, not full repo
3. Missing Tests Gate — blocks silent approval when tests are absent
4. Final Verifier Report — deterministic pre-approve check
5. Token truth — honest token accounting with estimated vs actual distinction

This is a **functionality** run, not UX polish.

## Hard constraints

- Do NOT change review zip filename pattern.
- Do NOT make `make_review_zip.sh` stricter or annoying.
- Do NOT add memory backends or MemPalace.
- Do NOT add auto-merge or auto-approval.
- Do NOT remove the human final decision.
- Do NOT do UX polish (no CSS, no frontend components, no graph changes).
- Do NOT expose raw prompts, raw diffs, raw stdout/stderr, secrets, or local absolute paths.
- Do NOT use variable names or string literals containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, or strings containing `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings like `marker_string = "SCOPE_PACKET_TEST_BODY_SHOULD_NOT_LEAK"` instead.
- All new test files must use redaction-safe fixture patterns (see prior run `.agent/self_run_goal_5451_5480.md` for examples).

---

## Task 1: Review Scope Packet

### What to build

Add a function that generates `review_scope_packet.json` for each task after the builder completes.

**File:** `packages/orchestration/pingpong_job.py` (or new `packages/orchestration/review_scope.py` if cleaner)

**Function:** `build_review_scope_packet(task, workspace, evidence_dir) -> dict`

The packet must include:

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
  "test_results": {"ran": true, "passed": 18, "failed": 0, "summary": "18 passed in 0.08s"},
  "open_findings": [],
  "repair_rounds": 0,
  "estimated_review_tokens": 2400,
  "recommended_scope": "hunk_only",
  "scope_reason": "Single file changed, 2 hunks, no cross-file dependencies detected"
}
```

**Scope recommendation logic:**
- `hunk_only`: single file, small diff, no cross-file imports changed
- `file_level`: multiple hunks in one file, or symbol renames
- `cross_file`: changes span multiple files with import/call relationships
- `full_job`: security-tagged changes, test failures, or repair rounds > 1

**Symbol detection:** Parse the diff for function/class definitions. Use simple regex: `def (\w+)`, `class (\w+)`, `function (\w+)`, `const (\w+)\s*=`, `export (\w+)`. No AST parsing required.

**Risk tagging per file:**
- `security:redaction` if file touches `_redact`, `_sanitize`, `_safe_`
- `security:auth` if file touches auth/login/session
- `new_file` if file is new
- `new_function` if diff adds a `def` or `function` line
- `test_change` if file is in `tests/`
- `config_change` if file is `.json`, `.toml`, `.yaml`, `.yml`

**Changed line ranges:** Parse unified diff `@@ -a,b +c,d @@` headers to extract target-side ranges.

**Estimated review tokens:** `sum(changed_lines * 4)` as rough char-to-token ratio.

**Write location:** `{evidence_dir}/task_runs/{task_id}/review_scope_packet.json`

Also generate `review_scope_packet.md` with a human-readable summary:
```markdown
## Review Scope: T001 — Backend completion

**Scope:** hunk_only
**Reason:** Single file changed, 2 hunks, no cross-file dependencies

### Changed files
| File | Lines | Risk | Symbols |
|------|-------|------|---------|
| packages/orchestration/ui_server.py | 45-60, 120-135 | security:redaction, new_function | _build_prompt_trace, _redact_preview |

### Tests
18 passed, 0 failed

### Findings
None
```

### Integration point

Call `build_review_scope_packet()` in `pingpong_job.py` after each task's builder run completes, before the reviewer is invoked. Store the result in evidence.

### Tests

Write `tests/test_review_scope_packet.py` with:
- Test: single-file diff produces correct line ranges
- Test: multi-file diff produces cross_file scope
- Test: new file gets `new_file` risk tag
- Test: security-relevant function gets `security:*` risk tag
- Test: test file gets `test_change` risk tag
- Test: empty diff produces empty packet
- Test: symbol extraction from diff
- Test: token estimate is non-negative integer
- Test: packet schema has all required keys
- Test: markdown summary is generated

---

## Task 2: Token-saving reviewer prompts

### What to change

Modify `_build_reviewer_prompt()` in `packages/orchestration/pingpong_loop.py` to use the review scope packet.

**Current state:** Reviewer receives full goal, full builder summary, full diff, full test output.

**New behavior:** If `review_scope_packet.json` exists for this task:
1. Include the recommended scope in the reviewer system prompt
2. Include changed line ranges so the reviewer knows where to focus
3. Include risk summary
4. Include related test outputs (not all test outputs)
5. Include prompt trace refs for provenance
6. Add explicit instruction: "Focus your review on the changed files and line ranges listed below. Do not review unrelated files unless a risk tag requires cross-file analysis."

**Fallback:** If no scope packet exists, fall back to current behavior (full context).

**Do NOT remove safety.** The reviewer prompt must still include:
- "If you detect a security concern, escalate to full_job scope"
- "If the change modifies imports or exports, check callers"
- All current reviewer instructions remain

### Integration

Pass `review_scope_packet` dict to `_build_reviewer_prompt()` as an optional kwarg.

### Tests

Add to `tests/test_pingpong.py` or new `tests/test_reviewer_prompt_scope.py`:
- Test: reviewer prompt includes scope instruction when packet exists
- Test: reviewer prompt falls back to full context when no packet
- Test: reviewer prompt includes changed line ranges from packet
- Test: reviewer prompt preserves all safety instructions
- Test: reviewer prompt includes risk summary

---

## Task 3: Missing Tests Gate

### What to build

Add a check in `pingpong_job.py` final status determination.

**Current logic** (around line 1163-1176):
```python
all_done = all(t.status in (TASK_APPLIED, TASK_SKIPPED) for t in job.tasks)
if all_done:
    job.status = JOB_COMPLETED
```

**New logic:**
After determining all tasks are done, check if any task changed source code but had no tests run:

```python
def _check_missing_tests(job: JobPlan) -> list[str]:
    """Return list of task IDs that changed source but ran no tests."""
    missing = []
    for task in job.tasks:
        if task.status != TASK_APPLIED:
            continue
        # Check if task changed source files (not just tests, configs, docs)
        source_changed = any(
            not f.startswith("tests/") and not f.endswith((".md", ".json", ".toml", ".yaml", ".yml", ".css"))
            for f in task.changed_files
        )
        tests_ran = task.test_result and task.test_result.strip() not in ("", "no tests", "unavailable", "skipped")
        if source_changed and not tests_ran:
            missing.append(task.id)
    return missing
```

**If missing tests detected:**
- Set `job.verification_required = True` (new field on `JobPlan`)
- Set `job.missing_tests_tasks = missing` (new field)
- Final audit status: `NEEDS_TESTS` instead of `READY_FOR_APPROVAL`
- Add warning to job summary

**Do NOT block the job.** The human can still approve. But the status must honestly reflect missing tests.

**Evidence:** Write `missing_tests_report.json` to evidence dir:
```json
{
  "tasks_missing_tests": ["T001"],
  "source_files_changed_without_tests": ["packages/orchestration/ui_server.py"],
  "recommendation": "Run tests for T001 before approving",
  "gate_status": "NEEDS_TESTS"
}
```

### Tests

Write `tests/test_missing_tests_gate.py` with:
- Test: task with source changes and no tests → flagged
- Test: task with only test changes → not flagged
- Test: task with only docs/config changes → not flagged
- Test: task with source changes AND tests → not flagged
- Test: multiple tasks, some missing → only missing ones flagged
- Test: job status becomes NEEDS_TESTS when gate triggers
- Test: missing_tests_report.json is written

---

## Task 4: Final Verifier Report

### What to build

Add `packages/orchestration/final_verifier.py` with:

```python
def build_final_verifier_report(job_id: str, evidence_dir: str) -> dict
```

This function reads all available evidence and produces a deterministic verdict.

**Inputs (read from evidence_dir):**
- `job_flow.json` (if exists)
- `self_run_observability_index.json` (if exists)
- `task_runs/*/review_scope_packet.json` (from T001)
- `command_transcript.json` (if exists)
- `target_guard.json` (if exists)
- `task_runs/*/review.json`
- `task_runs/*/repair_loop.json`
- `task_runs/*/token_accounting.json`
- `task_runs/*/tests.txt`
- `task_runs/*/manifest.json`

**Output:** `final_verifier_report.json`

```json
{
  "schema_version": "1.0.0",
  "job_id": "...",
  "verdict": "PASS_WITH_RISKS",
  "changed_files": ["packages/orchestration/ui_server.py"],
  "changed_line_ranges": {"packages/orchestration/ui_server.py": [[45, 60]]},
  "unresolved_findings": [],
  "test_status": {
    "tasks_with_tests": ["T004"],
    "tasks_without_tests": ["T001", "T002", "T003"],
    "total_passed": 33,
    "total_failed": 0
  },
  "token_summary": {
    "total_estimated": 45000,
    "builder_estimated": 30000,
    "reviewer_estimated": 15000,
    "repair_estimated": 0,
    "measurement": "estimated",
    "provider": "claude-cli"
  },
  "prompt_count": {
    "builder": 4,
    "reviewer": 4,
    "repair": 0,
    "total": 8
  },
  "safety_status": {
    "raw_prompts_exposed": false,
    "absolute_paths_exposed": false,
    "secrets_detected": false,
    "redaction_applied": true
  },
  "evidence_completeness": {
    "total_tasks": 5,
    "tasks_with_review": 4,
    "tasks_with_tests": 1,
    "tasks_with_scope_packet": 4,
    "missing_evidence": ["T005: no review.json"]
  },
  "recommended_action": "Approve after running tests for T001-T003"
}
```

**Verdict logic:**
- `PASS`: all tasks reviewed, all tests pass, no unresolved findings, no missing tests
- `PASS_WITH_RISKS`: all tasks reviewed, tests pass, but some tasks have risk tags or missing tests acknowledged
- `NEEDS_TESTS`: source changed without tests (from missing tests gate)
- `NEEDS_REPAIR`: unresolved findings exist
- `BLOCKED`: critical evidence missing (no review for >50% of tasks), or safety check failed

**Integration:** Call `build_final_verifier_report()` at the end of `run_job_flow()` in `pingpong_job.py`, after all tasks complete. Write result to evidence dir.

### Tests

Write `tests/test_final_verifier.py` with:
- Test: all green → PASS
- Test: missing tests → NEEDS_TESTS
- Test: unresolved findings → NEEDS_REPAIR
- Test: missing reviews → BLOCKED
- Test: token summary aggregation
- Test: evidence completeness check
- Test: safety status check
- Test: changed files aggregation from scope packets
- Test: report has all required schema keys
- Test: recommended_action is non-empty string

---

## Task 5: Token truth + verification

### What to build

Enhance `_build_token_accounting_json()` in `packages/orchestration/pingpong_evidence.py` to produce clearer token data.

**Current:** Passes through `run_data["token_accounting"]` with redaction.

**New fields:**
```json
{
  "schema_version": "1.0.0",
  "total_estimated_tokens": 45000,
  "builder_estimated_tokens": 30000,
  "reviewer_estimated_tokens": 15000,
  "repair_estimated_tokens": 0,
  "per_task": {
    "T001": {"builder": 8000, "reviewer": 4000, "repair": 0},
    "T002": {"builder": 7000, "reviewer": 3500, "repair": 0}
  },
  "measurement": "estimated",
  "measurement_source": "prompt_chars_div_4",
  "provider": "claude-cli",
  "missing_data": [],
  "actual_tokens": null
}
```

**measurement field values:**
- `"estimated"` — derived from `prompt_chars / 4` or similar heuristic
- `"actual"` — from provider API response (if available)
- `"unavailable"` — no data

**If actual token counts are not available, do NOT fake them.** Set `measurement: "estimated"` and `actual_tokens: null`.

**Also:** Update `_build_prompt_trace()` in `ui_server.py` to include per-prompt `measurement` field ("estimated" or "actual").

### Verification

After all features are built, verify:
- `review_scope_packet.json` can be generated for a sample diff
- `_build_reviewer_prompt()` includes scope instructions when packet exists
- Missing tests gate flags tasks correctly
- `final_verifier_report.json` produces correct verdict
- Token accounting distinguishes estimated vs actual
- No raw prompts, secrets, or absolute paths leak into any output
- All new files use redaction-safe test fixtures

### Tests

Add to existing or new test files:
- Test: token accounting includes measurement field
- Test: measurement is "estimated" when no actual data
- Test: per_task breakdown sums to total
- Test: missing_data lists tasks without token info
- Test: actual_tokens is null when not available

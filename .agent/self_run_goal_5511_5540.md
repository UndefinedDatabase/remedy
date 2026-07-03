# Steps 5511-5540: Token-Saving Reviewer Prompts + Self-Verification Gates v1

## Product goal

Use the Review Scope Packet to reduce reviewer token usage. Add self-verification gates so Remedy catches failures that occurred during T001 development: scratch files, missing tests, absent spec items, weak review verdicts.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT make `make_review_zip.sh` stricter or annoying.
- Do NOT do UX work.
- Do NOT fabricate test results.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings instead.

---

## Task 1: Token-saving reviewer prompts

### Files allowed

- `packages/orchestration/pingpong_loop.py` (modify `_build_reviewer_prompt`)
- `tests/orchestration/test_reviewer_prompt_scope.py` (create new)

### What to do

Update `_build_reviewer_prompt()` so it reads `review_scope_packet.json` from the task evidence directory when available.

When the scope packet is available, the reviewer prompt must include:

- Task goal / task title
- Changed files list
- Changed line ranges
- Changed symbols
- Risk tags
- Recommended scope and scope reason
- Related tests
- Open findings (if any)
- Evidence refs
- Prompt hashes
- Estimated review tokens
- Instruction: focus on listed files/hunks unless risk tags or scope reason require escalation

Scope behavior in the prompt:

- `hunk_only` — tell reviewer to focus on listed hunks and tests only
- `file_level` — tell reviewer to inspect changed file(s) fully
- `cross_file` — tell reviewer to inspect related files and imports/callers
- `full_job` — tell reviewer to inspect full task evidence, may escalate

Include: "You may escalate scope if you find evidence of broader issues, but state why."

When scope packet is NOT available, fall back to the current behavior (full diff in prompt).

### Tests

Write `tests/orchestration/test_reviewer_prompt_scope.py`:

1. `test_reviewer_prompt_includes_scope_packet_fields` — when scope packet exists, prompt contains changed files, risk tags, recommended scope
2. `test_reviewer_prompt_hunk_only_focuses_hunks` — `hunk_only` scope → prompt tells reviewer to focus on hunks
3. `test_reviewer_prompt_full_job_escalation` — `full_job` scope → prompt includes full evidence inspection instruction
4. `test_reviewer_prompt_fallback_without_scope_packet` — no scope packet → prompt still works with full diff

---

## Task 2: Spec compliance checklist

### Files allowed

- `packages/orchestration/spec_compliance.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_spec_compliance.py` (create new)

### What to do

Create `packages/orchestration/spec_compliance.py` with:

```python
def build_spec_compliance_checklist(task, goal_text, evidence_dir) -> dict:
    """Build a spec compliance checklist for one task."""
```

The checklist inspects the goal text and evidence to verify:

- Required artifact filenames mentioned in the goal are present in evidence
- Required function/class names mentioned in the goal are present in the diff
- Required test names mentioned in the goal are present in the test file
- Required grep/probe strings are present in changed files

Output schema:

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "checks": [
    {
      "type": "artifact",
      "name": "review_scope_packet.json",
      "required": true,
      "found": true,
      "location": "task_runs/T001/review_scope_packet.json"
    },
    {
      "type": "function",
      "name": "_collect_open_findings",
      "required": true,
      "found": true,
      "location": "packages/orchestration/review_scope.py"
    },
    {
      "type": "test",
      "name": "test_open_findings_from_needs_repair_review",
      "required": true,
      "found": false,
      "location": ""
    }
  ],
  "total_checks": 3,
  "passed": 2,
  "failed": 1,
  "missing_items": ["test_open_findings_from_needs_repair_review"],
  "verdict": "INCOMPLETE"
}
```

Verdicts: `COMPLETE`, `INCOMPLETE`, `SKIPPED` (no goal text available).

Write `spec_compliance_check.json` to `task_runs/<task_id>/` during evidence export.

Integration in `job_evidence.py`: after the review scope packet call, add a spec compliance check call (also wrapped in try/except).

### Tests

Write `tests/orchestration/test_spec_compliance.py`:

1. `test_checklist_detects_present_artifact` — artifact file exists → found=true
2. `test_checklist_detects_missing_artifact` — artifact file missing → found=false
3. `test_checklist_detects_function_in_diff` — function name in diff → found=true
4. `test_checklist_detects_missing_function` — function name not in diff → found=false
5. `test_checklist_detects_test_name_in_test_file` — test function present → found=true
6. `test_checklist_verdict_incomplete_on_missing` — any check failed → INCOMPLETE
7. `test_checklist_verdict_complete_all_present` — all checks pass → COMPLETE

---

## Task 3: Missing tests gate

### Files allowed

- `packages/orchestration/pingpong_job.py` (modify final audit logic)
- `tests/orchestration/test_missing_tests_gate.py` (create new)

### What to do

In the final audit section of `pingpong_job.py` (or wherever `final_audit` dict is built), add a missing tests gate:

If source code changed AND test code changed AND no tests were executed (`test_passed is None` and `tests.txt` is empty or says "not run"):

- Set `final_audit.status` to `NEEDS_TESTS` instead of `READY_FOR_APPROVAL`
- Set `promote_ready` to `false`
- Add `final_audit.missing_tests_reason` explaining what happened
- Add `final_audit.test_commands` with exact commands to run (e.g. `python3 -m pytest tests/orchestration/test_review_scope.py -q`)

If sandbox blocked tests, mark:
- `tests_blocked_by_environment: true`
- Do NOT pretend tests passed

The gate should NOT block when:
- Only non-code files changed (docs, configs without tests)
- Tests actually ran and results are recorded

### Tests

Write `tests/orchestration/test_missing_tests_gate.py`:

1. `test_gate_blocks_when_source_and_tests_changed_but_not_run` — NEEDS_TESTS
2. `test_gate_allows_when_tests_ran` — READY_FOR_APPROVAL allowed
3. `test_gate_allows_when_only_docs_changed` — no block
4. `test_sandbox_blocked_tests_marked_honestly` — `tests_blocked_by_environment: true`

---

## Task 4: Scratch file guard

### Files allowed

- `packages/orchestration/pingpong_job.py` (modify — add guard check)
- `tests/orchestration/test_scratch_file_guard.py` (create new)

### What to do

Before final audit and before review, check the job workspace root for forbidden scratch files:

Patterns:
- `_*.py` at workspace root
- `_run_*.py` at workspace root
- `_pt_check.py` at workspace root
- Any `.py` file at workspace root not in the intended changed files list

If found:
- Add to `final_audit.scratch_files_found: [list of paths]`
- Set `final_audit.status` to `BLOCKED`
- Set `promote_ready` to `false`
- Add reason: "Scratch files found at workspace root: ..."

### Tests

Write `tests/orchestration/test_scratch_file_guard.py`:

1. `test_guard_blocks_root_underscore_py` — `_run_rs.py` at root → BLOCKED
2. `test_guard_allows_intended_files` — files in intended list → no block
3. `test_guard_allows_nested_underscore_files` — `pkg/_internal.py` → no block (not at root)

---

## Task 5: Final verifier report

### Files allowed

- `packages/orchestration/final_verifier.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_final_verifier.py` (create new)

### What to do

Create `packages/orchestration/final_verifier.py` with:

```python
def build_final_verifier_report(evidence_dir) -> dict:
    """Build a deterministic final verifier report from evidence artifacts."""
```

It reads:
- `job_flow.json` or `job_report.json`
- `self_run_observability_index.json`
- `task_runs/<task_id>/review_scope_packet.json`
- `task_runs/<task_id>/spec_compliance_check.json`
- `command_transcript.json`
- `target_guard.json`
- Task reviews, repair loops, test results, token accounting

Output:

```json
{
  "schema_version": "1.0.0",
  "verdict": "PASS",
  "changed_files": ["pkg/review_scope.py"],
  "changed_line_ranges": {"pkg/review_scope.py": [[1, 632]]},
  "unresolved_findings": [],
  "test_status": {"ran": true, "passed": 32, "failed": 0},
  "token_summary": {
    "total_estimated_prompt_tokens": 13496,
    "builder_prompt_tokens": 8573,
    "reviewer_prompt_tokens": 4923
  },
  "prompt_count": 2,
  "safety_status": "clean",
  "evidence_completeness": {
    "review_scope_packet": true,
    "spec_compliance_check": true,
    "safe_diff": true,
    "review_json": true,
    "tests_txt": true
  },
  "missing_spec_items": [],
  "recommended_action": "Approve and promote."
}
```

Verdicts:
- `PASS` — all evidence complete, no findings, tests passed or honestly reported
- `PASS_WITH_RISKS` — complete but has open findings or risks noted
- `NEEDS_TESTS` — tests required but not run
- `NEEDS_REPAIR` — unresolved findings exist
- `BLOCKED` — scratch files, safety issues, or critical evidence missing

Write `final_verifier_report.json` to evidence dir during evidence export.

Integration in `job_evidence.py`: after task-level evidence (scope packet, compliance check), write the final verifier report at job level (also wrapped in try/except).

### Tests

Write `tests/orchestration/test_final_verifier.py`:

1. `test_verifier_pass_with_complete_evidence` — all artifacts present, no findings → PASS
2. `test_verifier_needs_tests_when_absent` — tests not run → NEEDS_TESTS
3. `test_verifier_needs_repair_with_findings` — unresolved findings → NEEDS_REPAIR
4. `test_verifier_blocked_on_missing_evidence` — critical evidence missing → BLOCKED
5. `test_verifier_includes_token_summary` — token summary present in report
6. `test_verifier_includes_changed_files` — changed files from scope packet included

---

## Task 6: Token truth

### Files allowed

- `packages/orchestration/pingpong_evidence.py` (modify `_build_token_accounting_json`)
- `tests/orchestration/test_token_truth.py` (create new)

### What to do

Enhance `_build_token_accounting_json()` to clearly distinguish estimated vs actual token counts.

Output must include:

```json
{
  "total_estimated_prompt_tokens": 13496,
  "builder_prompt_tokens_estimated": 8573,
  "reviewer_prompt_tokens_estimated": 4923,
  "repair_prompt_tokens_estimated": 0,
  "per_task_tokens": {
    "T001": {
      "builder_estimated": 8573,
      "reviewer_estimated": 4923,
      "repair_estimated": 0
    }
  },
  "counts_are_estimated": true,
  "actual_provider_tokens_available": false,
  "actual_provider_input_tokens": null,
  "actual_provider_output_tokens": null,
  "provider": "claude-cli",
  "token_measurement_source": "character_heuristic",
  "missing_token_data": []
}
```

Key requirements:
- Every token field must say whether it is estimated or actual
- If actual provider tokens are unavailable, say so explicitly
- `counts_are_estimated: true` when using heuristics
- `token_measurement_source`: "character_heuristic", "provider_reported", or "unavailable"
- `missing_token_data`: list of what could not be measured

### Tests

Write `tests/orchestration/test_token_truth.py`:

1. `test_token_truth_marks_estimated` — `counts_are_estimated: true` when heuristic
2. `test_token_truth_marks_source` — `token_measurement_source` present
3. `test_token_truth_missing_data_listed` — missing data explicitly listed
4. `test_token_truth_per_task_breakdown` — per-task token breakdown present

---

## What NOT to do

- Do NOT create scratch files at repo root
- Do NOT fabricate test results
- Do NOT pretend tests passed when they did not run
- Do NOT use `finditer(added_text)` for symbol detection
- Do NOT use risk tag names `tests` or `config`
- Do NOT modify `review_scope.py` unless fixing a bug found during this run

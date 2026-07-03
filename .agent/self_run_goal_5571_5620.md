# Steps 5571-5620: Verification Gates + Token Truth v1

## Product goal

Add verification gates (Missing Tests Gate, Scratch File Guard, Final Verifier Report) and honest token accounting (Token Truth) so Remedy catches self-run failures deterministically before final audit says READY_FOR_APPROVAL.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, `_cleanup_*.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT make `make_review_zip.sh` stricter or annoying.
- Do NOT do UX work.
- Do NOT fabricate test results.
- Do NOT fabricate exact token counts.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings instead.
- Do NOT label estimated tokens as exact/actual.
- Do NOT copy estimated values into `actual_*` fields.

---

## Task 1: Missing Tests Gate

### Files allowed

- `packages/orchestration/missing_tests_gate.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_missing_tests_gate.py` (create new)

Do NOT modify other files.

### What to do

Create `packages/orchestration/missing_tests_gate.py` with:

```python
def build_missing_tests_gate(task, evidence_dir: str) -> dict:
    """Check whether tests should have run but didn't."""

def write_missing_tests_gate(task, evidence_dir: str, written: dict) -> None:
    """Build and write missing_tests_gate.json to task evidence."""
```

Logic:
- Read `task_runs/<task_id>/safe.diff` from evidence dir.
- Check if source code files changed (`.py` files not under `tests/`).
- Check if test files changed (files matching `test_*.py` or under `tests/`).
- Read `task_runs/<task_id>/tests.txt` for test execution status.
- If source or tests changed AND tests were not executed:
  - `gate_status`: `NEEDS_TESTS`
  - `tests_blocked_by_environment`: check if tests.txt says "blocked" or "sandbox"
  - `suggested_test_commands`: list of `python3 -m pytest <test_file> -q` for each test file
  - `reason`: why tests are required
- If tests ran and results are recorded:
  - `gate_status`: `PASS`
- If only non-code files changed:
  - `gate_status`: `PASS` (no tests required)

Schema:

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "gate_status": "NEEDS_TESTS",
  "source_files_changed": true,
  "test_files_changed": true,
  "tests_executed": false,
  "tests_blocked_by_environment": true,
  "suggested_test_commands": ["python3 -m pytest tests/orchestration/test_foo.py -q"],
  "reason": "Source and test files changed but no tests were executed",
  "test_result_summary": ""
}
```

Write `task_runs/<task_id>/missing_tests_gate.json` in evidence export.

Integration in `job_evidence.py`:
After the spec compliance check block (around line 152), add:

```python
try:
    from packages.orchestration.missing_tests_gate import write_missing_tests_gate
    write_missing_tests_gate(task, str(out_path), written)
except Exception as exc:
    rel = f"task_runs/{task.task_id}/missing_tests_gate.error.txt"
    err_path = _validate_output_path(str(out_path), rel)
    err_path.write_text(
        f"missing_tests_gate unavailable: {type(exc).__name__}: {exc}\n",
        encoding="utf-8",
    )
    written[rel] = str(err_path)
```

### Tests

Create `tests/orchestration/test_missing_tests_gate.py`:

1. `test_gate_needs_tests_when_source_changed_no_tests_run` — source .py changed, no tests run → `NEEDS_TESTS`
2. `test_gate_pass_when_tests_ran` — tests ran → `PASS`
3. `test_gate_pass_when_only_docs_changed` — only .md changed → `PASS`
4. `test_gate_detects_sandbox_blocked` — tests.txt mentions "blocked" → `tests_blocked_by_environment: true`
5. `test_gate_suggests_test_commands` — test file changed → suggested commands include pytest command
6. `test_gate_writes_to_evidence` — `write_missing_tests_gate` creates JSON file

---

## Task 2: Scratch File Guard

### Files allowed

- `packages/orchestration/scratch_file_guard.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_scratch_file_guard.py` (create new)

Do NOT modify other files.

### What to do

Create `packages/orchestration/scratch_file_guard.py` with:

```python
def build_scratch_file_guard(workspace: str, allowed_files: list[str] | None = None) -> dict:
    """Check workspace root for forbidden scratch files."""

def write_scratch_file_guard(workspace: str, evidence_dir: str, task_id: str, allowed_files: list[str] | None, written: dict) -> None:
    """Build and write scratch_file_guard.json to task evidence."""
```

Forbidden patterns at workspace root:
- `_*.py`
- `_run_*.py`
- `_pt_check.py`
- `_cleanup_*.py`

A file is allowed if it appears in `allowed_files` list or in the review scope packet's `changed_files`.

Schema:

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "guard_status": "PASS",
  "checked_patterns": ["_*.py", "_run_*.py", "_pt_check.py", "_cleanup_*.py"],
  "files_found": [],
  "forbidden_files": [],
  "allowed_files_found": [],
  "suggested_cleanup": []
}
```

If forbidden files found:
- `guard_status`: `BLOCKED`
- `forbidden_files`: list of paths
- `suggested_cleanup`: list of `rm <path>` commands

Write `task_runs/<task_id>/scratch_file_guard.json` or `scratch_file_guard.json` at job level.

Integration in `job_evidence.py`:
After the missing tests gate block, add scratch file guard at job level (not per-task):

```python
try:
    from packages.orchestration.scratch_file_guard import write_scratch_file_guard
    all_allowed = []
    for task in job.tasks:
        if hasattr(task, "safe_diff_files") and task.safe_diff_files:
            all_allowed.extend(task.safe_diff_files)
    write_scratch_file_guard(
        job.job_workspace_path or "",
        str(out_path),
        "",
        all_allowed,
        written,
    )
except Exception as exc:
    rel = "scratch_file_guard.error.txt"
    err_path = _validate_output_path(str(out_path), rel)
    err_path.write_text(
        f"scratch_file_guard unavailable: {type(exc).__name__}: {exc}\n",
        encoding="utf-8",
    )
    written[rel] = str(err_path)
```

### Tests

Create `tests/orchestration/test_scratch_file_guard.py`:

1. `test_guard_pass_clean_workspace` — no scratch files → `PASS`
2. `test_guard_blocks_root_underscore_py` — `_run_test.py` at root → `BLOCKED`
3. `test_guard_allows_intended_files` — file in allowed list → not forbidden
4. `test_guard_allows_nested_underscore_files` — `pkg/_internal.py` → not forbidden (not at root)
5. `test_guard_suggests_cleanup` — forbidden file → suggested cleanup includes rm command
6. `test_guard_writes_to_evidence` — `write_scratch_file_guard` creates JSON

---

## Task 3: Final Verifier Report

### Files allowed

- `packages/orchestration/final_verifier.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_final_verifier.py` (create new)

Do NOT modify other files.

### What to do

Create `packages/orchestration/final_verifier.py` with:

```python
def build_final_verifier_report(evidence_dir: str) -> dict:
    """Build a deterministic final verifier report from evidence artifacts."""

def write_final_verifier_report(evidence_dir: str, written: dict) -> None:
    """Build and write final_verifier_report.json to evidence dir."""
```

The report reads all available evidence:
- `job_report.json` or `job_flow.json`
- `self_run_observability_index.json`
- `task_runs/<task_id>/review_scope_packet.json`
- `task_runs/<task_id>/spec_compliance_check.json`
- `task_runs/<task_id>/missing_tests_gate.json`
- `scratch_file_guard.json`
- `task_runs/<task_id>/review.json`
- `task_runs/<task_id>/repair_loop.json`
- `task_runs/<task_id>/tests.txt`
- `task_runs/<task_id>/token_accounting.json`

Schema:

```json
{
  "schema_version": "1.0.0",
  "verdict": "PASS",
  "changed_files": ["pkg/review_scope.py"],
  "changed_line_ranges": {},
  "unresolved_findings": [],
  "test_status": {"ran": false, "passed": 0, "failed": 0},
  "missing_tests_gate": "PASS",
  "scratch_file_guard": "PASS",
  "spec_compliance": "PASS",
  "token_status": {
    "actual_available": false,
    "estimated_prompt_tokens": 13496
  },
  "evidence_completeness": {
    "review_scope_packet": true,
    "spec_compliance_check": true,
    "missing_tests_gate": true,
    "scratch_file_guard": true,
    "safe_diff": true,
    "review_json": true,
    "tests_txt": true
  },
  "missing_evidence": [],
  "recommended_action": "Approve and promote."
}
```

Verdict logic:
- `PASS` — all gates pass, no unresolved findings, evidence complete
- `PASS_WITH_RISKS` — all gates pass but warnings (missing optional evidence)
- `NEEDS_TESTS` — missing tests gate says NEEDS_TESTS
- `NEEDS_REPAIR` — unresolved findings from review
- `BLOCKED` — scratch file guard BLOCKED, or critical evidence missing

Write `final_verifier_report.json` at evidence root (not per-task).

Integration in `job_evidence.py`:
After the task loop and scratch file guard, before `_write_job_prompt_trace_summary`:

```python
try:
    from packages.orchestration.final_verifier import write_final_verifier_report
    write_final_verifier_report(str(out_path), written)
except Exception as exc:
    rel = "final_verifier_report.error.txt"
    err_path = _validate_output_path(str(out_path), rel)
    err_path.write_text(
        f"final_verifier_report unavailable: {type(exc).__name__}: {exc}\n",
        encoding="utf-8",
    )
    written[rel] = str(err_path)
```

### Tests

Create `tests/orchestration/test_final_verifier.py`:

1. `test_verifier_pass_complete_evidence` — all artifacts present, gates pass → `PASS`
2. `test_verifier_needs_tests` — missing tests gate NEEDS_TESTS → `NEEDS_TESTS`
3. `test_verifier_blocked_scratch_files` — scratch guard BLOCKED → `BLOCKED`
4. `test_verifier_needs_repair_findings` — unresolved findings → `NEEDS_REPAIR`
5. `test_verifier_blocked_missing_evidence` — critical evidence missing → `BLOCKED`
6. `test_verifier_includes_evidence_completeness` — all evidence keys present
7. `test_verifier_writes_to_evidence` — `write_final_verifier_report` creates JSON

---

## Task 4: Token Truth

### Files allowed

- `packages/orchestration/token_truth.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration)
- `tests/orchestration/test_token_truth.py` (create new)

Do NOT modify other files.

### What to do

Create `packages/orchestration/token_truth.py` with:

```python
def build_token_truth(evidence_dir: str) -> dict:
    """Build honest token accounting separating actual from estimated usage."""

def write_token_truth(evidence_dir: str, written: dict) -> None:
    """Build and write token_truth.json to evidence dir."""
```

Read from evidence:
- `task_runs/<task_id>/token_accounting.json` for estimated values
- `task_runs/<task_id>/provider_evidence.json` for actual provider usage
- `prompt_trace_summary.json` for prompt counts

Schema:

```json
{
  "schema_version": "1.0.0",
  "source": "evidence_aggregation",
  "provider": "claude-cli",
  "model": "",
  "actual_available": false,
  "actual_prompt_tokens": null,
  "actual_completion_tokens": null,
  "actual_total_tokens": null,
  "actual_cache_creation_tokens": null,
  "actual_cache_read_tokens": null,
  "estimated_prompt_tokens": 13496,
  "estimated_completion_tokens": 0,
  "estimated_total_tokens": 13496,
  "measurement_source": "character_heuristic",
  "measurement_confidence": "low",
  "missing_reason": "actual token usage unavailable from claude-cli output",
  "per_task": {
    "T001": {
      "builder_estimated": 8573,
      "reviewer_estimated": 4923,
      "repair_estimated": 0,
      "actual_available": false
    }
  },
  "builder_estimated_total": 8573,
  "reviewer_estimated_total": 4923,
  "repair_estimated_total": 0,
  "provider_call_count": 2
}
```

Rules:
- If provider evidence contains actual usage data, populate `actual_*` fields and set `actual_available: true`.
- If not, set `actual_available: false`, `actual_*` to null, and `missing_reason` explaining why.
- Estimated values from token_accounting.json go in `estimated_*` fields only.
- `measurement_source`: `"character_heuristic"`, `"provider_reported"`, or `"unavailable"`.
- `measurement_confidence`: `"high"` if actual, `"low"` if estimated, `"none"` if unavailable.

Write `token_truth.json` at evidence root.

Integration in `job_evidence.py`:
After the final verifier report block, add:

```python
try:
    from packages.orchestration.token_truth import write_token_truth
    write_token_truth(str(out_path), written)
except Exception as exc:
    rel = "token_truth.error.txt"
    err_path = _validate_output_path(str(out_path), rel)
    err_path.write_text(
        f"token_truth unavailable: {type(exc).__name__}: {exc}\n",
        encoding="utf-8",
    )
    written[rel] = str(err_path)
```

### Tests

Create `tests/orchestration/test_token_truth.py`:

1. `test_token_truth_marks_estimated` — no actual data → `actual_available: false`, estimates populated
2. `test_token_truth_marks_source` — `measurement_source` is `"character_heuristic"`
3. `test_token_truth_missing_reason` — `missing_reason` present when actual unavailable
4. `test_token_truth_per_task_breakdown` — per-task builder/reviewer/repair estimates present
5. `test_token_truth_actual_when_available` — mock provider data with usage → `actual_available: true`, actual values populated
6. `test_token_truth_no_cross_contamination` — estimated values never copied to actual fields
7. `test_token_truth_writes_to_evidence` — `write_token_truth` creates JSON

---

## What NOT to do

- Do NOT create scratch files at repo root
- Do NOT fabricate test results
- Do NOT pretend tests passed when they did not run
- Do NOT label estimated tokens as actual/exact
- Do NOT copy estimated values into actual_* fields
- Do NOT modify `review_scope.py` or `spec_compliance.py`
- Do NOT modify `pingpong_loop.py`
- Do NOT modify test files other than those listed in allowed files
- Do NOT modify `do_cmd.py` or `ui_server.py`

# Steps 5541-5570: Spec Compliance Checklist v1

## Product goal

Create a deterministic spec compliance checklist per task so Builder and Reviewer cannot silently miss exact requirements from the goal file. This feature catches the class of bugs where builders skip required tests, miss exact function signatures, omit required constants, or create forbidden scratch files.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT do UX work.
- Do NOT fabricate test results.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings instead.

---

## Task 1: Spec compliance checklist module

### Files allowed

- `packages/orchestration/spec_compliance.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration call)
- `packages/orchestration/pingpong_loop.py` (modify — add checklist summary to reviewer prompt)
- `tests/orchestration/test_spec_compliance.py` (create new)

Do NOT modify other files.
Do NOT create any other files.

### Module: `packages/orchestration/spec_compliance.py`

Create this module with these public functions:

```python
def parse_goal_requirements(goal_text: str) -> dict[str, Any]:
    """Parse explicit requirements from task/goal text using deterministic heuristics."""

def build_spec_compliance_checklist(
    task: Any,
    goal_text: str,
    evidence_dir: str,
    workspace: str = "",
) -> dict[str, Any]:
    """Build a deterministic spec compliance checklist for one task."""

def render_checklist_markdown(checklist: dict[str, Any]) -> str:
    """Render a spec compliance checklist as human-readable Markdown."""

def write_spec_compliance_check(
    task: Any,
    goal_text: str,
    evidence_dir: str,
    workspace: str,
    written: dict[str, str],
) -> None:
    """Build, write JSON + Markdown, and register in written dict."""
```

### Checklist schema — all fields required

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "task_title": "...",
  "required_files": ["packages/orchestration/spec_compliance.py"],
  "allowed_files": ["packages/orchestration/spec_compliance.py", "tests/orchestration/test_spec_compliance.py"],
  "required_artifacts": ["spec_compliance_check.json"],
  "required_functions": ["build_spec_compliance_checklist"],
  "required_constants": ["_REVIEWER_SCOPED_DIFF_CAP"],
  "required_tests": ["test_checklist_detects_present_artifact"],
  "required_strings": ["within review scope"],
  "forbidden_files": ["_run_*.py", "_*.py"],
  "forbidden_strings": [],
  "checks": [
    {
      "type": "file",
      "name": "packages/orchestration/spec_compliance.py",
      "required": true,
      "found": true,
      "location": "packages/orchestration/spec_compliance.py"
    }
  ],
  "total_checks": 5,
  "passed": 4,
  "failed": 1,
  "missing_items": ["test_checklist_detects_missing_function"],
  "verdict": "FAIL"
}
```

### Goal text parsing — `parse_goal_requirements()`

Parse these patterns from goal text:

1. **Allowed files**: lines matching `- \`path/to/file\`` under a heading containing "Files allowed" or "Allowed files". Collect all file paths listed.

2. **Required tests**: lines matching `- \`test_name\`` or `1. \`test_name\`` or numbered items like `1. test_name_here` under a heading containing "Tests" or "### Tests". Also match patterns like `test_something_descriptive` appearing as list items.

3. **Required functions**: lines matching `def function_name` or `function_name()` appearing in code blocks or requirement lists.

4. **Required constants**: lines matching `CONSTANT_NAME = value` in code blocks.

5. **Required artifacts**: filenames like `*.json`, `*.md` mentioned as required outputs.

6. **Forbidden files**: patterns mentioned after "Do NOT create" or listed as forbidden scratch files.

7. **Forbidden strings**: patterns mentioned after "Do NOT use" for variable names/strings.

8. **Required strings**: exact strings that must appear in output (e.g. `"within review scope"`).

Return a dict with keys: `allowed_files`, `required_tests`, `required_functions`, `required_constants`, `required_artifacts`, `forbidden_files`, `forbidden_strings`, `required_strings`.

### Checklist building — `build_spec_compliance_checklist()`

For each parsed requirement, create a check entry:

1. **allowed_files**: verify each file exists in the diff or evidence. Mark `found: true/false`.

2. **required_tests**: read test files from the diff or evidence dir. Check if test function names exist. Mark `found: true/false`.

3. **required_functions**: read the safe.diff or changed files. Check if function definitions exist. Mark `found: true/false`.

4. **required_constants**: read the safe.diff or changed files. Check if constant assignments exist. Mark `found: true/false`.

5. **required_artifacts**: check if artifact files exist in the evidence dir under `task_runs/<task_id>/`. Mark `found: true/false`.

6. **forbidden_files**: check workspace root for matching files. If found, mark as violation.

7. **forbidden_strings**: check the diff for forbidden strings. If found, mark as violation.

8. **required_strings**: check the diff or changed files for required strings. If found, mark `found: true`, else `found: false`.

Verdict logic:
- `PASS` — all required checks pass, no forbidden violations
- `PASS_WITH_RISKS` — all required pass but warnings present (e.g. missing optional items)
- `FAIL` — any required check fails
- `BLOCKED` — forbidden file or forbidden string violation found

### Integration in `packages/orchestration/job_evidence.py`

In `export_job_evidence()`, after the review scope packet loop (around line 136), add a second integration for spec compliance:

```python
for task in job.tasks:
    try:
        from packages.orchestration.spec_compliance import write_spec_compliance_check
        goal_text = _read_goal_text(job)
        write_spec_compliance_check(
            task,
            goal_text,
            str(out_path),
            job.job_workspace_path or "",
            written,
        )
    except Exception as exc:
        rel = f"task_runs/{task.task_id}/spec_compliance_check.error.txt"
        err_path = _validate_output_path(str(out_path), rel)
        err_path.write_text(
            f"spec_compliance_check unavailable: {type(exc).__name__}: {exc}\n",
            encoding="utf-8",
        )
        written[rel] = str(err_path)
```

The `_read_goal_text(job)` helper should read the goal file content from `job.job_file_path` or `job.goal_file` if available. If not available, return empty string.

Requirements:
- Import lazily so evidence export does not crash if spec_compliance is missing.
- Wrap in try/except so a failure does not break the entire evidence bundle.
- Write error artifact on failure, do not silently skip.

### Reviewer prompt integration in `packages/orchestration/pingpong_loop.py`

In `_render_reviewer_scope_section()`, after the estimated review tokens section and before the final focus/escalation instructions, add:

If a `spec_compliance` key is present in the scope packet:

```python
compliance = packet.get("spec_compliance")
if compliance and isinstance(compliance, dict):
    verdict = compliance.get("verdict", "unknown")
    missing = compliance.get("missing_items", [])
    lines.append("")
    lines.append(f"### Spec Compliance: {verdict}")
    if missing:
        lines.append("Missing items:")
        for item in missing:
            lines.append(f"- {item}")
    lines.append(
        "If verdict is FAIL or BLOCKED, you MUST check the missing items "
        "before marking pass."
    )
```

This is optional — if `spec_compliance` is not in the packet, skip silently. This allows the runtime scope packet builder to optionally include compliance data when available.

### Tests

Create `tests/orchestration/test_spec_compliance.py` with these tests:

1. `test_parse_allowed_files_with_test_file` — goal text listing two allowed files including a test file → both files in `allowed_files` list

2. `test_allowed_test_file_not_out_of_scope` — allowed file that is a test file → check entry has `found: true`, not flagged as violation

3. `test_parse_required_test_names` — goal text listing test names under `### Tests` heading → all names in `required_tests`

4. `test_missing_required_test_creates_missing_item` — required test name not found in diff → appears in `missing_items`, verdict is `FAIL`

5. `test_required_artifact_detected` — artifact file exists in evidence dir → check entry `found: true`

6. `test_required_artifact_missing` — artifact file does not exist → `found: false`, in `missing_items`

7. `test_forbidden_root_scratch_file_detected` — `_run_test.py` at workspace root → verdict `BLOCKED`, in `missing_items` as violation

8. `test_required_constant_detected` — constant `_REVIEWER_SCOPED_DIFF_CAP` in diff → `found: true`

9. `test_required_string_detected` — required string "within review scope" in diff → `found: true`

10. `test_forbidden_string_detected` — forbidden string in diff → verdict `BLOCKED`

11. `test_checklist_json_written_to_evidence` — `write_spec_compliance_check` creates `task_runs/<task_id>/spec_compliance_check.json` and registers in `written`

12. `test_checklist_generation_failure_writes_error_artifact` — when `build_spec_compliance_checklist` raises, error artifact is written

13. `test_verdict_pass_all_present` — all checks pass → `PASS`

14. `test_verdict_fail_on_missing_required` — any required check fails → `FAIL`

15. `test_parse_required_functions` — goal text with `def build_spec_compliance_checklist` → function name in `required_functions`

Use `tmp_path` fixture. Create minimal evidence structures with helpers. Use benign marker strings.

Import:

```python
from packages.orchestration.spec_compliance import (
    parse_goal_requirements,
    build_spec_compliance_checklist,
    render_checklist_markdown,
    write_spec_compliance_check,
)
```

### What NOT to do

- Do NOT create scratch files at repo root
- Do NOT fabricate test results
- Do NOT pretend tests passed when they did not run
- Do NOT skip the evidence integration
- Do NOT silently swallow errors — write error artifacts
- Do NOT modify `review_scope.py`
- Do NOT modify test files other than the one listed in allowed files

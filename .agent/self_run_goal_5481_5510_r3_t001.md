# Steps 5481-5510 R3: Review Scope Packet T001 Compliance

## Product goal

Make Review Scope Packet a real evidence artifact that is automatically written by the job evidence export pipeline. This is T001 only — do NOT start T002-T005.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or any temporary Python scripts at repo root. Write tests in `tests/orchestration/test_review_scope.py` and run pytest if the sandbox allows.
- Do NOT change review zip filename pattern.
- Do NOT do UX work.
- Do NOT start T002-T005.
- Do NOT fabricate test results.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings like `marker_string = "SCOPE_PACKET_TEST_BODY"` instead.

---

## Task 1: Review Scope Packet — integrated evidence artifact

### Files allowed

Only these files may be modified or created:

- `packages/orchestration/review_scope.py` (new)
- `packages/orchestration/job_evidence.py` (modify — add review scope packet writing after task evidence)
- `tests/orchestration/test_review_scope.py` (new)

Do NOT modify `packages/orchestration/pingpong_job.py`.
Do NOT create any other files.

### Integration point

In `packages/orchestration/job_evidence.py`, the function `_write_task_run_evidence()` (line ~466) handles per-task evidence. After the call to `write_evidence_bundle(bundle, str(task_out))` returns and the task evidence files are written, add a call to write the review scope packet:

```python
from packages.orchestration.review_scope import write_review_scope_packet
write_review_scope_packet(task, job.job_workspace_path or "", str(out_base), written)
```

The `write_review_scope_packet` function should:
1. Call `build_review_scope_packet(task, workspace, evidence_dir)` to build the packet dict
2. Write `task_runs/<task_id>/review_scope_packet.json` (JSON with indent=2)
3. Call `render_scope_markdown(packet)` and write `task_runs/<task_id>/review_scope_packet.md`
4. Add both paths to the `written` dict

This must run for ANY task that has a task evidence dir and a run_id — including blocked and staged_blocked tasks. Do NOT skip blocked tasks.

For tasks without a run_id (where `_write_unavailable` is called instead), do NOT write a packet — those tasks have no evidence to scope.

### Public API in `packages/orchestration/review_scope.py`

```python
def build_review_scope_packet(task, workspace, evidence_dir) -> dict:
    """Build a deterministic review-scope packet for one task."""

def render_scope_markdown(packet) -> str:
    """Render a review scope packet as human-readable Markdown."""

def write_review_scope_packet(task, workspace, evidence_dir, written) -> None:
    """Build, write JSON + Markdown, and register in written dict."""
```

### Packet schema — all fields required

Every field must always be present. Missing values are explicit (empty list, `false`, `0`), never silently absent.

```json
{
  "schema_version": "1.0.0",
  "task_id": "T001",
  "task_title": "...",
  "changed_files": [],
  "changed_line_ranges": {},
  "changed_symbols": {},
  "risk_tags": {},
  "prompt_hashes": [],
  "worker_prompt_refs": [],
  "reviewer_prompt_refs": [],
  "evidence_refs": [],
  "related_tests": [],
  "test_results": {"ran": false, "passed": 0, "failed": 0, "summary": "tests not run"},
  "open_findings": [],
  "repair_rounds": 0,
  "estimated_review_tokens": 200,
  "recommended_scope": "hunk_only",
  "scope_reason": "..."
}
```

### Risk tags — exact names

Per changed file, assign zero or more of these exact tag strings:

- `new_file` — diff header has `--- /dev/null` or first hunk is `@@ -0,0 +...`
- `new_function` — added lines contain a function/class/const/export definition
- `test_change` — path starts with `tests/`, contains `/tests/`, or filename starts with `test_`
- `config_change` — extension is `.json`, `.toml`, `.yaml`, or `.yml`
- `security:redaction` — added code contains `_redact`, `_sanitize`, or `_safe_`
- `security:auth` — added code (lowercased) contains `_auth`, `authenticate`, `authorize`, or `permission`

Do NOT use `tests` — use `test_change`.
Do NOT use `config` — use `config_change`.

### New file detection

Track per file whether `--- /dev/null` appeared as the old-file header, OR the first hunk header is `@@ -0,0 +...`. If either, tag as `new_file`.

### Symbol detection — line-based only

For each file in the diff, collect symbols only from ADDED lines (lines starting with `+`, after removing the `+` prefix).

After stripping leading whitespace, match lines that START with:
- `def <name>(` or `async def <name>(`
- `class <name>`
- `function <name>`
- `const <name> =`
- `export function <name>`
- `export const <name>`

Use regex patterns like:
```python
_SYM_PATTERNS = [
    re.compile(r"^(?:async\s+)?def\s+([A-Za-z_]\w*)"),
    re.compile(r"^class\s+([A-Za-z_]\w*)"),
    re.compile(r"^(?:export\s+)?function\s+([A-Za-z_]\w*)"),
    re.compile(r"^(?:export\s+)?const\s+([A-Za-z_]\w*)\s*="),
]
```

Only match on stripped content of added lines. Do NOT match symbols in removed lines, context lines, or embedded diff strings in test fixtures.

### Open findings — correct collection

Collect from BOTH sources:

1. `repair_loop.json` → field `open_findings`:
   - If it is a list of strings like `["F1", "F2"]`, convert each to `{"id": "F1"}`, `{"id": "F2"}`
   - If it is a list of dicts like `[{"id": "F1", "severity": "high", "summary": "..."}]`, include as-is
   - If the field is missing or null, skip

2. `review.json` → field `reviews` → last entry:
   - If the last review's `verdict` is `needs_repair`, `fail`, or `blocked`, include its `findings` list
   - If the verdict is `pass` with no findings, skip
   - Deduplicate: if a finding ID already exists from repair_loop, prefer the review.json version (it may have more detail)

If a task is blocked/repair_exhausted AND review findings exist, `open_findings` MUST NOT be empty.

### Recommended scope — exact values

Use exactly these scope values:

- `full_job` — any `security:*` tag exists, OR test failure, OR repair_rounds > 1
- `cross_file` — multiple changed files with import changes detected, OR > 3 changed files
- `file_level` — single file with multiple hunks, OR 2-3 files without import changes
- `hunk_only` — single file, single hunk, no security risk

If no changed files: `hunk_only` with reason `"No changed files detected; verify evidence only."`

### Estimated review tokens

1. Check `task_runs/<task_id>/token_accounting.json` for `reviewer_prompt_tokens_estimated`
2. If available and > 0, use it
3. Fallback: `200 + len(diff_text) // 4`

### Prompt refs

- `worker_prompt_refs`: include `task_runs/<task_id>/prompt_trace.jsonl` if that file exists AND has builder role entries
- `reviewer_prompt_refs`: include `task_runs/<task_id>/prompt_trace.jsonl` if that file exists AND has reviewer role entries
- `prompt_hashes`: all `prompt_sha256` values from prompt_trace.jsonl in first-seen order

### Markdown output

`render_scope_markdown(packet) -> str` must produce:

```markdown
## Review Scope: T001 — <task_title>

**Scope:** hunk_only
**Reason:** Single file, 1 hunk, no security risk.

### Changed files
| File | Lines | Risk | Symbols |
|------|-------|------|---------|
| packages/orchestration/review_scope.py | 1-392 | new_file, new_function | build_review_scope_packet |

### Tests
tests not run

### Findings
None

### Evidence
- task_runs/T001/safe.diff
- task_runs/T001/review.json
```

If no changed files, show "No files changed."
If no findings, show "None".
If no evidence refs, show "No evidence files found."

### Tests

Write `tests/orchestration/test_review_scope.py` with these tests:

1. `test_single_file_hunk_only` — single-file single-hunk diff → `hunk_only`, correct line ranges
2. `test_multi_file_cross_file` — multi-file diff with import change → `cross_file`
3. `test_new_file_risk_tag` — `--- /dev/null` diff → `new_file` in risk_tags
4. `test_test_file_risk_tag` — test file path → `test_change` in risk_tags
5. `test_config_file_risk_tag` — `.toml` file → `config_change` in risk_tags
6. `test_security_redaction_tag` — added code with `_redact` → `security:redaction`
7. `test_security_auth_tag` — added code with `authenticate` → `security:auth`
8. `test_symbol_detection_line_based` — symbols from added `def`/`class`/`const` lines
9. `test_symbol_detection_ignores_embedded_diffs` — diff text embedded in a test fixture string does not produce false symbols
10. `test_open_findings_from_repair_loop_string_list` — `repair_loop.open_findings: ["F1"]` → `[{"id": "F1"}]`
11. `test_open_findings_from_needs_repair_review` — review with `needs_repair` → findings included
12. `test_packet_json_written` — `review_scope_packet.json` written to task evidence dir
13. `test_packet_markdown_written` — `review_scope_packet.md` written to task evidence dir
14. `test_missing_tests_explicit` — no test output → `test_results.ran` is `false`
15. `test_token_estimate_prefers_accounting` — token_accounting value used when available
16. `test_full_job_scope_on_security` — security tag → `full_job` scope
17. `test_render_scope_markdown` — markdown contains title, scope, table headers

Use `tmp_path` fixture. Create minimal evidence structures. Use benign marker strings.

Test the integration by importing `write_review_scope_packet` and calling it with a mock task and evidence dir, then checking the output files exist.

### What NOT to do

- Do NOT create `_run_rs.py` or any scratch files at repo root
- Do NOT create `review_scope.json` — the filename must be `review_scope_packet.json`
- Do NOT use risk tag names `tests` or `config` — use `test_change` and `config_change`
- Do NOT use scope values `file`, `module`, `none` — use `hunk_only`, `file_level`, `cross_file`, `full_job`
- Do NOT import from or modify `pingpong_job.py`
- Do NOT scan removed diff lines for symbols
- Do NOT fabricate test results

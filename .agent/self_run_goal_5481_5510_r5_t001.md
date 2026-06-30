# Steps 5481-5510 R5: Review Scope Packet Final T001 Fix

## Product goal

Create the Review Scope Packet feature: a deterministic per-task evidence artifact that summarises what changed and how much review effort it deserves. Write both the module, its integration into the evidence export pipeline, and comprehensive tests.

This is a surgical T001-only run. Do NOT start T002-T005.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT make `make_review_zip.sh` stricter or annoying.
- Do NOT do UX work.
- Do NOT start T002-T005.
- Do NOT fabricate test results.
- Do NOT auto-approve or auto-merge.
- Do NOT commit or push.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings instead.

---

## Task 1: Review Scope Packet — complete implementation

### Files allowed

Only these files may be modified or created:

- `packages/orchestration/review_scope.py` (create new)
- `packages/orchestration/job_evidence.py` (modify — add integration call)
- `tests/orchestration/test_review_scope.py` (create new)

Do NOT modify `packages/orchestration/pingpong_job.py`.
Do NOT create any other files.

### Module: `packages/orchestration/review_scope.py`

Create this module with three public functions:

```python
def build_review_scope_packet(task, workspace, evidence_dir) -> dict:
    """Build a deterministic review-scope packet for one task."""

def render_scope_markdown(packet) -> str:
    """Render a review scope packet as human-readable Markdown."""

def write_review_scope_packet(task, workspace, evidence_dir, written) -> None:
    """Build, write JSON + Markdown, and register in written dict."""
```

### Packet schema — all 18 fields required

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

### CRITICAL: Symbol detection — line-based ONLY

This is the most important fix. Do NOT use `finditer` on concatenated text. Use `match` on individual stripped lines.

Use EXACTLY this logic:

```python
_SYMBOL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^def\s+(\w+)"),
    re.compile(r"^async\s+def\s+(\w+)"),
    re.compile(r"^class\s+(\w+)"),
    re.compile(r"^function\s+(\w+)"),
    re.compile(r"^const\s+(\w+)\s*="),
    re.compile(r"^export\s+function\s+(\w+)"),
    re.compile(r"^export\s+const\s+(\w+)\s*="),
)


def _detect_symbols(added_lines: list[str]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    in_triple_quote = False

    for line in added_lines:
        stripped = line.strip()

        quote_count = stripped.count('"""') + stripped.count("'''")
        if quote_count:
            if quote_count % 2 == 1:
                in_triple_quote = not in_triple_quote
            continue

        if in_triple_quote:
            continue

        for pattern in _SYMBOL_PATTERNS:
            m = pattern.match(stripped)
            if not m:
                continue
            name = m.group(1)
            if name not in seen:
                seen.add(name)
                found.append(name)
            break

    return found
```

Key requirements:

- Patterns use `^` anchor, NOT `\b` word boundary.
- Includes `async def`, `export function`, `export const`.
- Uses `pattern.match(stripped)`, NOT `pattern.finditer(text)`.
- Skips lines inside triple-quoted strings.
- Input is `list[str]` of added lines, NOT a single joined string.
- The string `finditer(added_text)` must NOT appear anywhere in the file. Final reviewer will grep for it.

### CRITICAL: Diff parsing — store added lines as list

`_parse_diff()` must store added lines in TWO forms:

- `added_lines`: `list[str]` — individual lines (for `_detect_symbols`)
- `added_text`: `str` — joined text (for risk tag security marker detection)

Track `new_file: bool` per file:

- `True` when `--- /dev/null` appears as old-file header
- OR when first hunk header matches `@@ -0,0 +...`

Track `import_change: bool` for cross-file scope detection.

Call symbol detection with the list:

```python
symbols = _detect_symbols(info["added_lines"])
```

### CRITICAL: Open findings — collect from BOTH sources

Use EXACTLY this logic:

```python
_BLOCKING_VERDICTS = {"needs_repair", "fail", "blocked"}


def _finding_id(finding: dict[str, Any]) -> str:
    return str(finding.get("id") or finding.get("finding_id") or "")


def _collect_open_findings(review: Any, repair: Any) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    anonymous: list[dict[str, Any]] = []

    def add_finding(item: Any) -> None:
        if isinstance(item, str):
            item = {"id": item}
        if not isinstance(item, dict):
            return
        fid = _finding_id(item)
        if fid:
            existing = by_id.get(fid, {})
            merged = {**existing, **item}
            by_id[fid] = merged
        else:
            anonymous.append(item)

    if isinstance(repair, dict):
        for item in repair.get("open_findings", []) or []:
            add_finding(item)

    review_findings_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(review, dict):
        for rev in review.get("reviews", []) or []:
            if not isinstance(rev, dict):
                continue
            verdict = str(rev.get("verdict") or "").lower()
            if verdict not in _BLOCKING_VERDICTS:
                continue
            for item in rev.get("findings", []) or []:
                if isinstance(item, dict):
                    fid = _finding_id(item)
                    if fid:
                        review_findings_by_id[fid] = item
                add_finding(item)

    for fid, current in list(by_id.items()):
        richer = review_findings_by_id.get(fid)
        if richer:
            by_id[fid] = {**current, **richer}

    return list(by_id.values()) + anonymous
```

Key requirements:

- Handles string IDs like `["F1"]` by converting to `{"id": "F1"}`.
- Checks verdicts `needs_repair`, `fail`, AND `blocked` — not just `fail`.
- Merges findings from BOTH repair_loop and review sources. Does NOT early-return after repair findings.
- Enriches repair-loop string IDs with matching review finding details.

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

### Fallback risk tags (when diff is missing)

When `build_review_scope_packet()` falls back to `task.safe_diff_files` because no diff is available, risk tags must STILL be assigned:

```python
tags = []
if _is_test_path(path):
    tags.append("test_change")
ext = Path(path).suffix.lower()
if ext in (".json", ".toml", ".yaml", ".yml"):
    tags.append("config_change")
risk_tags[path] = tags
```

Do NOT just do `["test_change"] if _is_test_path(path) else []`. Config files need `config_change` even in the fallback path.

### Recommended scope — exact values

Use exactly these scope values:

- `full_job` — any `security:*` tag exists, OR test failure, OR repair_rounds > 1
- `cross_file` — multiple changed files with import changes detected, OR > 3 changed files
- `file_level` — single file with multiple hunks, OR 2-3 files without import changes
- `hunk_only` — single file, single hunk, no security risk

### Estimated review tokens

1. Check `task_runs/<task_id>/token_accounting.json` for `reviewer_prompt_tokens_estimated`
2. If available and > 0, use it
3. Fallback: `200 + len(diff_text) // 4`

### Prompt refs

- `worker_prompt_refs`: include `task_runs/<task_id>/prompt_trace.jsonl` if that file exists AND has builder role entries
- `reviewer_prompt_refs`: include `task_runs/<task_id>/prompt_trace.jsonl` if that file exists AND has reviewer role entries
- `prompt_hashes`: all `prompt_sha256` values from prompt_trace.jsonl in first-seen order

### Markdown output

`render_scope_markdown(packet) -> str` must produce structured Markdown with:

- Title line: `## Review Scope: <task_id> — <task_title>` (or `# Review Scope — <task_id>: <task_title>`)
- Scope and reason
- Changed files table or per-file sections with line ranges, symbols, risk tags
- Tests section
- Findings section
- Evidence refs section

### Writer

`write_review_scope_packet(task, workspace, evidence_dir, written)` must:

1. Call `build_review_scope_packet(task, workspace, evidence_dir)` to build the packet dict
2. Write `task_runs/<task_id>/review_scope_packet.json` (JSON with indent=2)
3. Call `render_scope_markdown(packet)` and write `task_runs/<task_id>/review_scope_packet.md`
4. Add both paths to the `written` dict
5. No-op if task has no `task_id`

### Integration in `packages/orchestration/job_evidence.py`

In `export_job_evidence()`, the loop at line ~123 calls `_write_task_run_evidence(task, str(out_path), written)` for each task. After this loop (around line 125), add a second loop that writes the review scope packet for each task that has a run_id:

```python
# Write review scope packets for each task
for task in job.tasks:
    if task.run_id:
        try:
            from packages.orchestration.review_scope import write_review_scope_packet
            write_review_scope_packet(
                task,
                job.job_workspace_path or "",
                str(out_path),
                written,
            )
        except Exception:
            pass  # Do not break evidence export if scope packet fails
```

Requirements:

- Import lazily so evidence export does not crash if review_scope is missing.
- Wrap in try/except so a failure does not break the entire evidence bundle.
- Only call for tasks with a `run_id`.
- Pass `job.job_workspace_path or ""` as the workspace parameter.

Final reviewer will grep `job_evidence.py` for `write_review_scope_packet` and fail if not found.

### Tests

Write `tests/orchestration/test_review_scope.py` with ALL these tests:

**Core packet tests (from R4, keep working):**

1. `test_hunk_only_single_file` — single-file single-hunk diff → `hunk_only`, correct line ranges, symbols detected
2. `test_file_level_multiple_hunks` — single file, 2+ hunks → `file_level`
3. `test_cross_file_with_imports` — multi-file diff with import change → `cross_file`
4. `test_full_job_on_security_tag` — security tag → `full_job`
5. `test_full_job_on_test_failure` — test failure → `full_job`
6. `test_prompt_hashes_and_refs` — prompt trace with builder+reviewer → correct hashes and refs
7. `test_token_estimate_prefers_accounting` — token_accounting.json value used when available
8. `test_open_findings_from_repair_loop_dict` — repair_loop.open_findings as dict list
9. `test_missing_diff_falls_back_to_task_files` — no diff → uses task.safe_diff_files
10. `test_related_tests_workspace_scan` — changed file has matching test in workspace

**Risk tag tests:**

11. `test_new_file_via_dev_null` — `--- /dev/null` diff → `new_file` in risk_tags
12. `test_new_file_via_zero_zero_hunk` — `@@ -0,0` → `new_file`
13. `test_modified_file_not_new` — normal diff → no `new_file`
14. `test_test_change_tag_exact_name` — test file → `test_change`, NOT `tests`
15. `test_config_change_tag` — `.json` file → `config_change`
16. `test_config_change_toml_yaml` — `.toml`, `.yaml`, `.yml` → `config_change`
17. `test_security_auth_tag` — added code with `authenticate` → `security:auth`
18. `test_security_redaction_tag` — added code with `_redact` → `security:redaction`
19. `test_only_allowed_risk_tags` — all emitted tags are in the allowed set

**R5 fix validation tests (these MUST be present):**

20. `test_symbol_detection_ignores_embedded_diff_strings` — diff text embedded in a test fixture triple-quoted string does NOT produce false symbols. Use this exact diff:

```python
diff = (
    "--- a/tests/test_parse.py\n+++ b/tests/test_parse.py\n"
    "@@ -0,0 +1,7 @@\n"
    '+FIXTURE = """\n'
    "++def fake_symbol():\n"
    "++    pass\n"
    '+"""\n'
    "+\n"
    "+def real_test():\n"
    "+    pass\n"
)
```

Assert `"real_test"` in symbols, `"fake_symbol"` NOT in symbols.

21. `test_symbol_detection_async_def_and_exports` — added lines with `async def foo()`, `export function bar()`, `export const baz =` → all three detected.

22. `test_open_findings_from_repair_loop_string_list` — `repair_loop.open_findings: ["F1", "F2"]` → returns `[{"id": "F1"}, {"id": "F2"}]`.

23. `test_open_findings_from_needs_repair_review` — review.json with `verdict: "needs_repair"` and findings → findings included.

24. `test_open_findings_from_blocked_review` — review.json with `verdict: "blocked"` and findings → findings included.

25. `test_open_findings_enriches_repair_string_from_review` — repair has `["F1"]`, review has `{"id": "F1", "severity": "high", "summary": "bug"}` → output has `{"id": "F1", "severity": "high", "summary": "bug"}`.

26. `test_fallback_config_change_without_diff` — no diff, `task.safe_diff_files: ["settings.toml"]` → `config_change` in risk_tags.

**Output tests:**

27. `test_render_markdown_has_key_sections` — markdown output contains title, scope, changed files, tests, findings, evidence sections
28. `test_render_markdown_deterministic` — same packet → same markdown
29. `test_render_markdown_empty` — empty packet → "No changed files" text
30. `test_write_creates_json_and_md` — `write_review_scope_packet` creates both files with correct names and registers in written dict

Use `tmp_path` fixture. Create minimal evidence structures with a helper like `_make_run()`. Use benign marker strings.

### Verification: what NOT to do

- Do NOT create scratch files at repo root
- Do NOT use `finditer(added_text)` anywhere in `review_scope.py`
- Do NOT use `\b` word boundary in symbol patterns — use `^` anchors
- Do NOT check only `verdict == "fail"` — check `needs_repair` and `blocked` too
- Do NOT early-return from `_collect_open_findings` after repair findings
- Do NOT drop string IDs from `repair_loop.open_findings`
- Do NOT skip `config_change` in the fallback path
- Do NOT use risk tag `tests` — use `test_change`
- Do NOT use risk tag `config` — use `config_change`
- Do NOT break existing features (scope values, prompt refs, token estimate, writer filenames)

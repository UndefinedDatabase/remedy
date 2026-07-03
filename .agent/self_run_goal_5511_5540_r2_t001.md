# Steps 5511-5540 R2: Runtime Token-Saving Reviewer Prompts

## Product goal

Fix the reviewer prompt so it actually uses a runtime review scope packet at the real call site, reducing token usage for scoped reviews. The scope packet must be built at runtime BEFORE the reviewer prompt is generated — not relying on evidence export which happens AFTER.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT do UX work.
- Do NOT fabricate test results.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures.

---

## Task 1: Runtime token-saving reviewer prompts

### Files allowed

- `packages/orchestration/pingpong_loop.py` (modify)
- `tests/orchestration/test_reviewer_prompt_scope.py` (create new)

Do NOT modify other files.
Do NOT create any other files.

### Context: current code

The real reviewer prompt call site is at line ~1548 of `pingpong_loop.py`:

```python
reviewer_prompt = _build_reviewer_prompt(
    effective_goal,
    builder_out.summary,
    diff_summary=diff_summary,
    safe_diff=reviewer_safe_diff,
    test_result=rd.test_summary,
    files_changed=result.staged_files,
    task_excerpt=task_input.excerpt if task_input else "",
    task_sha256=task_input.sha256 if task_input else "",
    task_tokens_estimated=task_input.tokens_estimated if task_input else 0,
    scope_contract=reviewer_scope_text,
    prior_findings=findings if is_repair else None,
    repair_round=result.repair_rounds_used if is_repair else 0,
)
```

The function `_build_reviewer_prompt()` is defined at line ~788. Current signature:

```python
def _build_reviewer_prompt(
    goal: str,
    builder_summary: str,
    *,
    diff_summary: str = "",
    safe_diff: str = "",
    test_result: str = "",
    files_changed: list[str] | None = None,
    task_excerpt: str = "",
    task_sha256: str = "",
    task_tokens_estimated: int = 0,
    scope_contract: str = "",
    prior_findings: list[ReviewFinding] | None = None,
    repair_round: int = 0,
) -> str:
```

Current diff cap: `_REVIEWER_DIFF_CAP = 30000`

### What to do

#### 1. Build runtime scope packet before reviewer prompt

At the real call site (around line ~1525, in the reviewer phase), BEFORE the `_build_reviewer_prompt(...)` call, build a runtime scope packet dict.

Use the existing `build_review_scope_packet` from `packages.orchestration.review_scope` if it can work with available runtime data. If not, build a lightweight runtime dict directly:

```python
runtime_scope_packet = None
if reviewer_safe_diff and result.staged_files:
    try:
        from packages.orchestration.review_scope import build_review_scope_packet
        runtime_task = {
            "task_id": result.task_id or "",
            "title": task_input.title if task_input else "",
            "test_passed": rd.test_passed if rd else None,
            "repair_rounds_used": result.repair_rounds_used,
        }
        runtime_scope_packet = build_review_scope_packet(
            runtime_task,
            str(staging) if staging else "",
            "",  # no evidence dir at runtime
        )
    except Exception:
        runtime_scope_packet = None
```

If `build_review_scope_packet` requires an evidence dir and can't work without it, build a minimal dict instead:

```python
if runtime_scope_packet is None and reviewer_safe_diff:
    from packages.orchestration.review_scope import _parse_diff, _detect_symbols, _risk_tags_for_file
    parsed = _parse_diff(reviewer_safe_diff)
    changed_files = sorted(parsed.keys())
    risk_tags = {}
    changed_symbols = {}
    changed_line_ranges = {}
    for path in changed_files:
        info = parsed[path]
        added_lines = info.get("added_lines", [])
        symbols = _detect_symbols(added_lines)
        added_text = "\n".join(added_lines)
        tags = _risk_tags_for_file(path, added_text, symbols, info.get("new_file", False))
        risk_tags[path] = tags
        changed_symbols[path] = symbols
        changed_line_ranges[path] = info.get("ranges", [])
    has_security = any(t.startswith("security:") for tags in risk_tags.values() for t in tags)
    runtime_scope_packet = {
        "task_id": result.task_id or "",
        "task_title": task_input.title if task_input else "",
        "changed_files": changed_files,
        "changed_line_ranges": changed_line_ranges,
        "changed_symbols": changed_symbols,
        "risk_tags": risk_tags,
        "recommended_scope": "full_job" if has_security else ("cross_file" if len(changed_files) > 1 else "hunk_only"),
        "scope_reason": "runtime scope from safe diff",
        "related_tests": [f for f in changed_files if "test" in f.lower()],
        "open_findings": [],
    }
```

#### 2. Add `scope_packet` parameter to `_build_reviewer_prompt()`

Add a new keyword parameter:

```python
scope_packet: dict[str, Any] | None = None,
```

#### 3. When `scope_packet` is present, generate a focused prompt

Inside `_build_reviewer_prompt`, when `scope_packet is not None`:

- Include `## Review Scope Packet` section with:
  - Changed files, line ranges, symbols, risk tags
  - Recommended scope and reason
  - Related tests
  - Open findings (if any)
  - "Files listed in changed_files and related_tests are within review scope. Do not flag them as out-of-scope."
  - "You may escalate scope if you find evidence of broader issues, but state why."
- Include `## Focused Staged Diff` section with the diff capped at `_REVIEWER_SCOPED_DIFF_CAP = 12000`
  - If truncated: append `[FOCUSED DIFF TRUNCATED]`
- Do NOT include `## Task Input Summary`
- Do NOT include duplicate `## Files Changed`
- Do NOT include old `## Staged Unified Diff`
- Still include `## Original Goal`, `## Builder Summary`, `## Test Result`, prior findings if repair

When `scope_packet is None`:

- Keep EXACTLY the current behavior unchanged
- Use `## Task Input Summary`, `## Files Changed`, `## Staged Unified Diff` as before
- Use `_REVIEWER_DIFF_CAP = 30000` as before

#### 4. Pass `scope_packet` at the real call site

Change the real call at line ~1548:

```python
reviewer_prompt = _build_reviewer_prompt(
    effective_goal,
    builder_out.summary,
    diff_summary=diff_summary,
    safe_diff=reviewer_safe_diff,
    test_result=rd.test_summary,
    files_changed=result.staged_files,
    task_excerpt=task_input.excerpt if task_input else "",
    task_sha256=task_input.sha256 if task_input else "",
    task_tokens_estimated=task_input.tokens_estimated if task_input else 0,
    scope_contract=reviewer_scope_text,
    prior_findings=findings if is_repair else None,
    repair_round=result.repair_rounds_used if is_repair else 0,
    scope_packet=runtime_scope_packet,
)
```

Final reviewer will grep for `scope_packet=runtime_scope_packet` at the call site and fail if not found.

#### 5. Add the scoped diff cap constant

```python
_REVIEWER_SCOPED_DIFF_CAP = 12000
```

Place it near `_REVIEWER_DIFF_CAP = 30000`.

### Tests

Create `tests/orchestration/test_reviewer_prompt_scope.py` with these tests:

1. `test_scoped_prompt_includes_review_scope_section` — when `scope_packet` is passed, prompt contains `## Review Scope Packet`

2. `test_scoped_prompt_includes_focused_diff` — when `scope_packet` is passed, prompt contains `## Focused Staged Diff`

3. `test_scoped_prompt_omits_task_input_summary` — when `scope_packet` is passed, prompt does NOT contain `## Task Input Summary`

4. `test_scoped_prompt_omits_staged_unified_diff` — when `scope_packet` is passed, prompt does NOT contain `## Staged Unified Diff`

5. `test_scoped_prompt_omits_duplicate_files_changed` — when `scope_packet` is passed, prompt does NOT contain `## Files Changed`

6. `test_scoped_prompt_shorter_than_fallback` — for a large diff (>12000 chars), scoped prompt is shorter than fallback prompt

7. `test_scoped_prompt_truncates_with_marker` — diff exceeding `_REVIEWER_SCOPED_DIFF_CAP` produces `[FOCUSED DIFF TRUNCATED]`

8. `test_fallback_without_scope_packet` — when `scope_packet=None`, prompt uses `## Staged Unified Diff` and `## Task Input Summary`

9. `test_changed_test_file_is_in_scope` — scope packet listing a test file in `changed_files` → prompt includes "Files listed in changed_files and related_tests are within review scope"

10. `test_scope_packet_none_uses_full_diff_cap` — without scope packet, diff up to `_REVIEWER_DIFF_CAP` (30000) is included, not the smaller cap

Tests must directly call `_build_reviewer_prompt(...)` with and without `scope_packet` and assert on the output string.

Import the function:

```python
from packages.orchestration.pingpong_loop import _build_reviewer_prompt
```

### What NOT to do

- Do NOT create scratch files at repo root
- Do NOT only add parameters without wiring them at the real call site
- Do NOT leave the real runtime call without `scope_packet=runtime_scope_packet`
- Do NOT use `finditer(added_text)` anywhere
- Do NOT remove existing behavior when `scope_packet` is None
- Do NOT change `_REVIEWER_DIFF_CAP` value (keep it 30000 for fallback)

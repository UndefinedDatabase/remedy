# Steps 5481-5510 R4: Review Scope Packet Spec Gap Closure

## Product goal

Fix the remaining spec gaps in the Review Scope Packet. This is a surgical repair of `review_scope.py` and its tests. Do NOT rewrite from scratch — fix the specific issues listed below.

## Hard constraints

- Do NOT create scratch files at the repo root. No `_run_rs.py`, `_pt_check.py`, or temporary Python scripts at repo root.
- Do NOT change review zip filename pattern.
- Do NOT do UX work.
- Do NOT start T002-T005.
- Do NOT fabricate test results.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures. Use benign marker strings instead.

---

## Task 1: Review Scope Packet spec gap closure

### Files allowed

Only these files may be modified:

- `packages/orchestration/review_scope.py` (modify)
- `tests/orchestration/test_review_scope.py` (modify)

Do NOT modify `packages/orchestration/job_evidence.py` (integration already works).
Do NOT modify `packages/orchestration/pingpong_job.py`.
Do NOT create any new files.

### What already works (do NOT break)

These features from R3 are correct and must be preserved:

- `build_review_scope_packet()` returns all 18 schema fields
- `render_scope_markdown()` generates Markdown with title, scope, table, tests, findings, evidence
- `write_review_scope_packet()` writes `review_scope_packet.json` and `review_scope_packet.md`
- Scope values: `hunk_only`, `file_level`, `cross_file`, `full_job`
- Prompt hashes and worker/reviewer refs split by role
- Token estimate prefers token_accounting, falls back to heuristic
- Integration via `job_evidence.py` `_write_task_run_evidence()`

### Fix 1: Risk tags — exact names

In `_risk_tags_for_file()`, change the risk tag strings to use exact spec names.

Current code (WRONG):
```python
if _is_test_path(path):
    tags.append("tests")
```

Fix to:
```python
if _is_test_path(path):
    tags.append("test_change")
```

Add config detection:
```python
ext = Path(path).suffix.lower()
if ext in (".json", ".toml", ".yaml", ".yml"):
    tags.append("config_change")
```

These are the ONLY allowed risk tag strings:
- `new_file`
- `new_function`
- `test_change`
- `config_change`
- `security:redaction`
- `security:auth`

### Fix 2: New-file detection

Update `_parse_diff()` to track whether each file is new.

A file is new when:
- Its old-file header is `--- /dev/null`
- OR its first hunk header matches `@@ -0,0 +...`

Track this in the per-file dict: `"new_file": True`

Then in `_risk_tags_for_file()`, accept a `new_file: bool` parameter and if true, add `"new_file"` to tags.

Example diff that must produce `new_file`:
```diff
--- /dev/null
+++ b/pkg/new.py
@@ -0,0 +1,2 @@
+def hello():
+    pass
```

### Fix 3: Symbol detection — line-based only

Current `_detect_symbols()` uses `pat.finditer(added_text)` which searches the entire concatenated added text. This catches symbols inside embedded diff strings in test fixtures.

Fix: Change to line-based detection. Process each added line individually. Only match symbols on lines whose STRIPPED content starts with the pattern.

Replace `_detect_symbols(added_text: str) -> list[str]` with `_detect_symbols(added_lines: list[str]) -> list[str]`:

```python
_SYM_PATTERNS = [
    re.compile(r"^(?:async\s+)?def\s+([A-Za-z_]\w*)"),
    re.compile(r"^class\s+([A-Za-z_]\w*)"),
    re.compile(r"^(?:export\s+)?function\s+([A-Za-z_]\w*)"),
    re.compile(r"^(?:export\s+)?const\s+([A-Za-z_]\w*)\s*="),
]

def _detect_symbols(added_lines: list[str]) -> list[str]:
    found = []
    seen = set()
    for line in added_lines:
        stripped = line.strip()
        for pat in _SYM_PATTERNS:
            m = pat.match(stripped)
            if m:
                name = m.group(1)
                if name not in seen:
                    seen.add(name)
                    found.append(name)
    return found
```

Key change: use `pat.match(stripped)` not `pat.finditer(full_text)`. This way embedded diff strings like `+def fake_symbol():` inside a test string literal are only detected if they appear as actual top-level added lines, not as content within strings.

Also update `_parse_diff()` to store added lines as a list (not joined text) until needed. Pass the list to `_detect_symbols()`.

For `_risk_tags_for_file()`, the `added_text` parameter is still needed for security marker detection. You can join the lines for that purpose, or pass both.

### Fix 4: Open findings — collect from both sources

Replace `_collect_open_findings()` with correct logic:

```python
def _collect_open_findings(review: Any, repair: Any) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    # Source 1: repair_loop.json open_findings
    if isinstance(repair, dict):
        for f in repair.get("open_findings", []) or []:
            if isinstance(f, str):
                findings.append({"id": f})
                seen_ids.add(f)
            elif isinstance(f, dict):
                findings.append(f)
                fid = f.get("id", "")
                if fid:
                    seen_ids.add(fid)

    # Source 2: review.json — last review with non-pass verdict
    if isinstance(review, dict):
        reviews = review.get("reviews", []) or []
        if reviews:
            last = reviews[-1]
            if isinstance(last, dict):
                verdict = last.get("verdict", "")
                if verdict in ("needs_repair", "fail", "blocked"):
                    for f in last.get("findings", []) or []:
                        if isinstance(f, dict):
                            fid = f.get("id", "")
                            if fid and fid in seen_ids:
                                # Enrich: replace string-only entry with full dict
                                for i, existing in enumerate(findings):
                                    if existing.get("id") == fid and len(existing) == 1:
                                        findings[i] = f
                                        break
                            elif fid not in seen_ids:
                                findings.append(f)
                                if fid:
                                    seen_ids.add(fid)

    return findings
```

### Fix 5: Also update the fallback in build_review_scope_packet

In `build_review_scope_packet()`, when building risk_tags for fallback files (no diff available), also use `test_change` and `config_change`:

```python
# Current (WRONG):
risk_tags[path] = ["tests"] if _is_test_path(path) else []

# Fix:
tags = []
if _is_test_path(path):
    tags.append("test_change")
ext = Path(path).suffix.lower()
if ext in (".json", ".toml", ".yaml", ".yml"):
    tags.append("config_change")
risk_tags[path] = tags
```

### Tests to add

Add these new tests to `tests/orchestration/test_review_scope.py`:

```python
def test_new_file_risk_tag(tmp_path):
    """--- /dev/null diff produces new_file risk tag."""
    diff = (
        "--- /dev/null\n+++ b/pkg/brand_new.py\n"
        "@@ -0,0 +1,2 @@\n+def greet():\n+    pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "new_file" in pkt["risk_tags"]["pkg/brand_new.py"]
    assert "new_function" in pkt["risk_tags"]["pkg/brand_new.py"]


def test_test_file_risk_tag(tmp_path):
    """Test file path gets test_change, not 'tests'."""
    diff = (
        "--- a/tests/test_widget.py\n+++ b/tests/test_widget.py\n"
        "@@ -1,0 +2,1 @@\n+def test_widget(): pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    tags = pkt["risk_tags"]["tests/test_widget.py"]
    assert "test_change" in tags
    assert "tests" not in tags


def test_config_file_risk_tag(tmp_path):
    """Config file extension gets config_change."""
    diff = (
        "--- a/pyproject.toml\n+++ b/pyproject.toml\n"
        "@@ -1,0 +2,1 @@\n+name = \"remedy\"\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "config_change" in pkt["risk_tags"]["pyproject.toml"]


def test_security_auth_tag(tmp_path):
    """Added code with authenticate gets security:auth."""
    diff = (
        "--- a/pkg/login.py\n+++ b/pkg/login.py\n"
        "@@ -1,0 +2,2 @@\n+def authenticate(user):\n+    return True\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "security:auth" in pkt["risk_tags"]["pkg/login.py"]


def test_symbol_detection_ignores_embedded_diffs(tmp_path):
    """Embedded diff strings in test fixtures must not produce false symbols."""
    diff = (
        "--- a/tests/test_parse.py\n+++ b/tests/test_parse.py\n"
        "@@ -0,0 +1,5 @@\n"
        "+FIXTURE = \"\"\"\n"
        "++def fake_symbol():\n"
        "++    pass\n"
        "+\"\"\"\n"
        "+def real_test(): pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    syms = pkt["changed_symbols"]["tests/test_parse.py"]
    assert "real_test" in syms
    assert "fake_symbol" not in syms


def test_open_findings_from_repair_loop_string_list(tmp_path):
    """repair_loop.open_findings as string list produces id-only dicts."""
    repair = '{"open_findings": ["F1", "F2"], "repair_rounds_used": 1}'
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", repair=repair)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    ids = [f["id"] for f in pkt["open_findings"]]
    assert "F1" in ids
    assert "F2" in ids


def test_open_findings_from_needs_repair_review(tmp_path):
    """Review with needs_repair verdict includes its findings."""
    review = {
        "total_reviews": 1,
        "final_verdict": "needs_repair",
        "reviews": [{
            "round": 1,
            "verdict": "needs_repair",
            "finding_count": 1,
            "findings": [{"id": "F1", "severity": "high", "summary": "bug found"}]
        }]
    }
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", review=json.dumps(review))
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert len(pkt["open_findings"]) >= 1
    assert pkt["open_findings"][0]["id"] == "F1"
```

Keep ALL existing tests that already pass. Only add new ones and fix tag assertions in existing tests (change `"tests"` to `"test_change"` where needed).

### What NOT to do

- Do NOT create scratch files at repo root
- Do NOT change filenames (`review_scope_packet.json`, `review_scope_packet.md`)
- Do NOT change scope values (`hunk_only`, `file_level`, `cross_file`, `full_job`)
- Do NOT change the integration in `job_evidence.py`
- Do NOT rewrite the whole file from scratch — make targeted fixes
- Do NOT remove existing working tests
- Do NOT use `tests` as a risk tag — use `test_change`
- Do NOT use `config` as a risk tag — use `config_change`

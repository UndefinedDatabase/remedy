"""Tests for review_scope: build packet, render markdown, write artifacts."""
from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.review_scope import (
    SCHEMA_VERSION,
    build_review_scope_packet,
    parse_diff_line_ranges,
    render_scope_markdown,
    split_diff_by_path,
    write_review_scope_packet,
)


def _make_run(evidence_dir: Path, task_id: str, *, diff: str = "", tests: str = "",
              trace: str = "", review: str = "", repair: str = "",
              token_accounting: str = "") -> Path:
    run = evidence_dir / "task_runs" / task_id
    run.mkdir(parents=True, exist_ok=True)
    if diff:
        (run / "safe.diff").write_text(diff, encoding="utf-8")
    if tests:
        (run / "tests.txt").write_text(tests, encoding="utf-8")
    if trace:
        (run / "prompt_trace.jsonl").write_text(trace, encoding="utf-8")
    if review:
        (run / "review.json").write_text(review, encoding="utf-8")
    if repair:
        (run / "repair_loop.json").write_text(repair, encoding="utf-8")
    if token_accounting:
        (run / "token_accounting.json").write_text(token_accounting, encoding="utf-8")
    return run


SINGLE_FILE_DIFF = """--- a/packages/orchestration/ui_server.py
+++ b/packages/orchestration/ui_server.py
@@ -45,0 +46,3 @@
+def _build_prompt_trace():
+    pass
"""


def test_hunk_only_single_file(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, tests="3 passed in 0.05s")
    task = {"task_id": "T001", "title": "Add trace", "test_passed": True}
    pkt = build_review_scope_packet(task, tmp_path, ev)

    assert pkt["schema_version"] == SCHEMA_VERSION
    assert pkt["task_id"] == "T001"
    assert pkt["changed_files"] == ["packages/orchestration/ui_server.py"]
    assert pkt["changed_line_ranges"]["packages/orchestration/ui_server.py"] == [[46, 48]]
    assert "_build_prompt_trace" in pkt["changed_symbols"]["packages/orchestration/ui_server.py"]
    assert pkt["recommended_scope"] == "hunk_only"
    assert pkt["test_results"] == {"ran": True, "passed": 3, "failed": 0,
                                   "summary": "3 passed in 0.05s"}


def test_file_level_multiple_hunks(tmp_path):
    diff = (
        "--- a/pkg/a.py\n+++ b/pkg/a.py\n"
        "@@ -45,0 +46,2 @@\n+x = 1\n+y = 2\n"
        "@@ -120,0 +130,1 @@\n+z = 3\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert pkt["changed_line_ranges"]["pkg/a.py"] == [[46, 47], [130, 130]]
    assert pkt["recommended_scope"] == "file_level"


def test_cross_file_with_imports(tmp_path):
    diff = (
        "--- a/pkg/a.py\n+++ b/pkg/a.py\n@@ -1,0 +2,1 @@\n+from pkg.b import thing\n"
        "--- a/pkg/b.py\n+++ b/pkg/b.py\n@@ -1,0 +2,1 @@\n+def thing():\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert pkt["changed_files"] == ["pkg/a.py", "pkg/b.py"]
    assert pkt["recommended_scope"] == "cross_file"


def test_full_job_on_security_tag(tmp_path):
    diff = (
        "--- a/pkg/secure.py\n+++ b/pkg/secure.py\n"
        "@@ -1,0 +2,2 @@\n+def _redact_preview():\n+    pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "security:redaction" in pkt["risk_tags"]["pkg/secure.py"]
    assert pkt["recommended_scope"] == "full_job"
    assert "security" in pkt["scope_reason"]


def test_full_job_on_test_failure(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, tests="1 failed, 2 passed in 0.1s")
    pkt = build_review_scope_packet(
        {"task_id": "T001", "test_passed": False}, tmp_path, ev
    )
    assert pkt["test_results"]["failed"] == 1
    assert pkt["recommended_scope"] == "full_job"


def test_prompt_hashes_and_refs(tmp_path):
    trace = (
        json.dumps({"role": "builder", "prompt_sha256": "feedface"}) + "\n"
        + json.dumps({"role": "reviewer", "prompt_sha256": "deadbeef"}) + "\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, trace=trace)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert pkt["prompt_hashes"] == ["feedface", "deadbeef"]
    assert pkt["worker_prompt_refs"] == ["task_runs/T001/prompt_trace.jsonl"]
    assert pkt["reviewer_prompt_refs"] == ["task_runs/T001/prompt_trace.jsonl"]
    assert "task_runs/T001/safe.diff" in pkt["evidence_refs"]


def test_token_estimate_prefers_accounting(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF,
              token_accounting=json.dumps({"reviewer_prompt_tokens_estimated": 2400}))
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert pkt["estimated_review_tokens"] == 2400


def test_open_findings_from_repair_loop(tmp_path):
    repair = json.dumps({
        "repair_rounds_used": 2,
        "open_findings": [{"id": "F1", "severity": "high", "summary": "leak"}],
    })
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, repair=repair)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert pkt["open_findings"][0]["id"] == "F1"
    assert pkt["repair_rounds"] == 2
    # repair_rounds > 1 forces full_job
    assert pkt["recommended_scope"] == "full_job"


def test_missing_diff_falls_back_to_task_files(tmp_path):
    ev = tmp_path / "evidence"
    (ev / "task_runs" / "T001").mkdir(parents=True)
    task = {"task_id": "T001", "safe_diff_files": ["pkg/x.py"]}
    pkt = build_review_scope_packet(task, tmp_path, ev)
    assert pkt["changed_files"] == ["pkg/x.py"]
    assert pkt["test_results"]["ran"] is False


def test_related_tests_workspace_scan(tmp_path):
    diff = (
        "--- a/pkg/widget.py\n+++ b/pkg/widget.py\n@@ -1,0 +2,1 @@\n+def go():\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    tests_dir = tmp_path / "tests" / "unit"
    tests_dir.mkdir(parents=True)
    (tests_dir / "test_widget.py").write_text("def test_go(): pass\n", encoding="utf-8")
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "tests/unit/test_widget.py" in pkt["related_tests"]


# ---------------------------------------------------------------------------
# Symbol detection — line-based ONLY (the critical fix)
# ---------------------------------------------------------------------------

def test_symbols_line_based_no_midline_false_positives(tmp_path):
    # ``def`` / ``class`` appearing mid-line (call sites, strings) must NOT
    # be captured. Only lines that *start* with a definition keyword count.
    diff = (
        "--- a/pkg/m.py\n+++ b/pkg/m.py\n@@ -1,0 +2,4 @@\n"
        "+    result = make_def('not_a_symbol')\n"
        "+    note = 'class Fake: pass'\n"
        "+def real_one():\n"
        "+    return define_helper()\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    syms = pkt["changed_symbols"]["pkg/m.py"]
    assert syms == ["real_one"]
    assert "not_a_symbol" not in syms
    assert "Fake" not in syms


def test_symbols_indented_methods_detected(tmp_path):
    # Indented defs/classes are detected after stripping leading whitespace.
    diff = (
        "--- a/pkg/c.py\n+++ b/pkg/c.py\n@@ -1,0 +2,5 @@\n"
        "+class Widget:\n"
        "+    def method_a(self):\n"
        "+        pass\n"
        "+    async def method_b(self):\n"
        "+        pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    syms = pkt["changed_symbols"]["pkg/c.py"]
    assert syms == ["Widget", "method_a", "method_b"]


def test_symbols_js_const_and_function(tmp_path):
    diff = (
        "--- a/web/app.js\n+++ b/web/app.js\n@@ -1,0 +2,2 @@\n"
        "+const router = createRouter();\n"
        "+function handler() {}\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    syms = pkt["changed_symbols"]["web/app.js"]
    assert "router" in syms
    assert "handler" in syms


# ---------------------------------------------------------------------------
# Risk tags — exact spec names
# ---------------------------------------------------------------------------

_ALLOWED_RISK_TAGS = {
    "new_file",
    "new_function",
    "test_change",
    "config_change",
    "security:redaction",
    "security:auth",
}


def test_test_change_tag_exact_name(tmp_path):
    diff = (
        "--- a/tests/test_widget.py\n+++ b/tests/test_widget.py\n"
        "@@ -1,0 +2,1 @@\n+def test_go(): pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    tags = pkt["risk_tags"]["tests/test_widget.py"]
    assert "test_change" in tags
    assert "tests" not in tags


def test_config_change_tag(tmp_path):
    diff = (
        "--- a/pkg/settings.json\n+++ b/pkg/settings.json\n"
        '@@ -1,0 +2,1 @@\n+{"k": 1}\n'
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "config_change" in pkt["risk_tags"]["pkg/settings.json"]


def test_config_change_tag_toml_yaml(tmp_path):
    diff = (
        "--- a/a.toml\n+++ b/a.toml\n@@ -1,0 +2,1 @@\n+x = 1\n"
        "--- a/b.yaml\n+++ b/b.yaml\n@@ -1,0 +2,1 @@\n+x: 1\n"
        "--- a/c.yml\n+++ b/c.yml\n@@ -1,0 +2,1 @@\n+y: 2\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "config_change" in pkt["risk_tags"]["a.toml"]
    assert "config_change" in pkt["risk_tags"]["b.yaml"]
    assert "config_change" in pkt["risk_tags"]["c.yml"]


def test_only_allowed_risk_tags_emitted(tmp_path):
    diff = (
        "--- /dev/null\n+++ b/tests/test_auth.py\n"
        "@@ -0,0 +1,2 @@\n+def authenticate(): pass\n+    _redact_token()\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    for tags in pkt["risk_tags"].values():
        assert set(tags) <= _ALLOWED_RISK_TAGS


# ---------------------------------------------------------------------------
# New-file detection
# ---------------------------------------------------------------------------

def test_new_file_via_dev_null_old_header(tmp_path):
    diff = (
        "--- /dev/null\n+++ b/pkg/new.py\n@@ -0,0 +1,2 @@\n+def hello():\n+    pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "new_file" in pkt["risk_tags"]["pkg/new.py"]


def test_new_file_via_zero_zero_hunk(tmp_path):
    # Old header present (not /dev/null) but first hunk starts at -0,0.
    diff = (
        "--- a/pkg/new2.py\n+++ b/pkg/new2.py\n@@ -0,0 +1,1 @@\n+def hi(): pass\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "new_file" in pkt["risk_tags"]["pkg/new2.py"]


def test_modified_file_not_tagged_new_file(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert "new_file" not in pkt["risk_tags"]["packages/orchestration/ui_server.py"]


# ---------------------------------------------------------------------------
# render_scope_markdown
# ---------------------------------------------------------------------------

def test_render_markdown_contains_key_sections(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, tests="3 passed in 0.05s")
    pkt = build_review_scope_packet(
        {"task_id": "T001", "title": "Add trace"}, tmp_path, ev
    )
    md = render_scope_markdown(pkt)
    assert md.startswith("# Review Scope — T001: Add trace")
    assert "**Recommended scope:** `hunk_only`" in md
    assert "## Changed Files" in md
    assert "`packages/orchestration/ui_server.py`" in md
    assert "`_build_prompt_trace`" in md
    assert "## Related Tests" in md
    assert "## Open Findings" in md
    assert "## Evidence" in md


def test_render_markdown_deterministic(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert render_scope_markdown(pkt) == render_scope_markdown(pkt)


def test_render_markdown_empty_change_set():
    pkt = {
        "schema_version": SCHEMA_VERSION,
        "task_id": "T009",
        "task_title": "",
        "changed_files": [],
        "changed_line_ranges": {},
        "changed_symbols": {},
        "risk_tags": {},
        "prompt_hashes": [],
        "worker_prompt_refs": [],
        "reviewer_prompt_refs": [],
        "evidence_refs": [],
        "related_tests": [],
        "test_results": {"ran": False, "passed": 0, "failed": 0, "summary": "tests not run"},
        "open_findings": [],
        "repair_rounds": 0,
        "estimated_review_tokens": 0,
        "recommended_scope": "hunk_only",
        "scope_reason": "no changes",
    }
    md = render_scope_markdown(pkt)
    assert "# Review Scope — T009" in md
    assert "_No changed files recorded._" in md


# ---------------------------------------------------------------------------
# write_review_scope_packet
# ---------------------------------------------------------------------------

def test_write_creates_json_and_md_and_registers(tmp_path):
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, tests="3 passed in 0.05s")
    written: dict[str, str] = {}
    write_review_scope_packet(
        {"task_id": "T001", "title": "Add trace"}, tmp_path, ev, written
    )

    json_path = ev / "task_runs" / "T001" / "review_scope_packet.json"
    md_path = ev / "task_runs" / "T001" / "review_scope_packet.md"
    assert json_path.exists()
    assert md_path.exists()

    assert written["task_runs/T001/review_scope_packet.json"] == str(json_path)
    assert written["task_runs/T001/review_scope_packet.md"] == str(md_path)

    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["schema_version"] == SCHEMA_VERSION
    assert loaded["task_id"] == "T001"
    # JSON written with indent=2.
    assert "\n  " in json_path.read_text(encoding="utf-8")


def test_write_noop_without_task_id(tmp_path):
    ev = tmp_path / "evidence"
    written: dict[str, str] = {}
    write_review_scope_packet({"task_id": ""}, tmp_path, ev, written)
    assert written == {}


# ---------------------------------------------------------------------------
# All 18 schema fields always present
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {
    "schema_version", "task_id", "task_title", "changed_files",
    "changed_line_ranges", "changed_symbols", "risk_tags", "prompt_hashes",
    "worker_prompt_refs", "reviewer_prompt_refs", "evidence_refs",
    "related_tests", "test_results", "open_findings", "repair_rounds",
    "estimated_review_tokens", "recommended_scope", "scope_reason",
}


def test_all_18_fields_present_even_when_empty(tmp_path):
    ev = tmp_path / "evidence"
    (ev / "task_runs" / "T001").mkdir(parents=True)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert set(pkt.keys()) == _REQUIRED_FIELDS
    assert len(_REQUIRED_FIELDS) == 18
    assert pkt["test_results"] == {"ran": False, "passed": 0, "failed": 0,
                                   "summary": "tests not run"}


# ---------------------------------------------------------------------------
# R5 patch: export symbol detection
# ---------------------------------------------------------------------------

def test_symbol_detection_exports_capture_symbol_names(tmp_path):
    diff = (
        "--- a/web/app.js\n+++ b/web/app.js\n@@ -0,0 +1,3 @@\n"
        "+export function makeThing() {}\n"
        "+export const value = 1\n"
        "+function helper() {}\n"
    )
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=diff)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    syms = pkt["changed_symbols"]["web/app.js"]
    assert "makeThing" in syms
    assert "value" in syms
    assert "helper" in syms
    assert "function" not in syms
    assert "const" not in syms


# ---------------------------------------------------------------------------
# R5 patch: open findings
# ---------------------------------------------------------------------------

def test_open_findings_from_repair_loop_string_list(tmp_path):
    repair = '{"open_findings": ["F1", "F2"], "repair_rounds_used": 1}'
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, repair=repair)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    ids = [f["id"] for f in pkt["open_findings"]]
    assert "F1" in ids
    assert "F2" in ids


def test_open_findings_from_needs_repair_review(tmp_path):
    review = json.dumps({
        "total_reviews": 1,
        "final_verdict": "needs_repair",
        "reviews": [{
            "round": 1,
            "verdict": "needs_repair",
            "finding_count": 1,
            "findings": [{"id": "F2", "severity": "high", "summary": "bug found"}],
        }],
    })
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, review=review)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    assert len(pkt["open_findings"]) >= 1
    assert pkt["open_findings"][0]["id"] == "F2"


def test_open_findings_from_blocked_review(tmp_path):
    review = json.dumps({
        "total_reviews": 1,
        "final_verdict": "blocked",
        "reviews": [{
            "round": 1,
            "verdict": "blocked",
            "finding_count": 1,
            "findings": [{"id": "B1", "severity": "critical", "summary": "blocked"}],
        }],
    })
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, review=review)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    ids = [f["id"] for f in pkt["open_findings"]]
    assert "B1" in ids


def test_open_findings_enriches_repair_string_from_review(tmp_path):
    repair = '{"open_findings": ["F1"], "repair_rounds_used": 1}'
    review = json.dumps({
        "reviews": [{
            "verdict": "needs_repair",
            "findings": [{"id": "F1", "severity": "high", "summary": "real bug"}],
        }],
    })
    ev = tmp_path / "evidence"
    _make_run(ev, "T001", diff=SINGLE_FILE_DIFF, repair=repair, review=review)
    pkt = build_review_scope_packet({"task_id": "T001"}, tmp_path, ev)
    f1 = [f for f in pkt["open_findings"] if f.get("id") == "F1"]
    assert len(f1) == 1
    assert f1[0]["severity"] == "high"
    assert f1[0]["summary"] == "real bug"


# ---------------------------------------------------------------------------
# R5 patch: fallback config_change
# ---------------------------------------------------------------------------

def test_fallback_config_change_without_diff(tmp_path):
    ev = tmp_path / "evidence"
    (ev / "task_runs" / "T001").mkdir(parents=True)
    task = {"task_id": "T001", "safe_diff_files": ["package.json", "tests/test_x.py"]}
    pkt = build_review_scope_packet(task, tmp_path, ev)
    assert "config_change" in pkt["risk_tags"]["package.json"]
    assert "test_change" in pkt["risk_tags"]["tests/test_x.py"]


# ---------------------------------------------------------------------------
# F111 T002b: split_diff_by_path — one standalone diff section per path
# ---------------------------------------------------------------------------

TWO_FILE_DIFF = """--- a/src/a.py
+++ b/src/a.py
@@ -1,2 +1,3 @@
 keep_a
+added_a
--- a/src/b.py
+++ b/src/b.py
@@ -10,2 +10,2 @@
-old_b
+new_b
"""


def test_split_diff_by_path_single_file_round_trip():
    sections = split_diff_by_path(SINGLE_FILE_DIFF)
    path = "packages/orchestration/ui_server.py"
    assert list(sections) == [path]
    # The section is the whole diff back again, minus the trailing newline that
    # ``splitlines`` consumed.
    assert sections[path] == SINGLE_FILE_DIFF.rstrip("\n")


def test_split_diff_by_path_two_files_are_disjoint():
    sections = split_diff_by_path(TWO_FILE_DIFF)
    assert sorted(sections) == ["src/a.py", "src/b.py"]

    assert sections["src/a.py"].startswith("--- a/src/a.py\n")
    assert sections["src/b.py"].startswith("--- a/src/b.py\n")
    assert "src/b.py" not in sections["src/a.py"]
    assert "src/a.py" not in sections["src/b.py"]
    assert "added_a" in sections["src/a.py"]
    assert "new_b" in sections["src/b.py"]
    assert "new_b" not in sections["src/a.py"]


def test_split_diff_by_path_drops_preamble_before_first_header():
    diff = (
        "diff --git a/src/a.py b/src/a.py\n"
        "index 1111111..2222222 100644\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -1,2 +1,3 @@\n"
        " keep_a\n"
        "+added_a\n"
    )
    sections = split_diff_by_path(diff)
    assert list(sections) == ["src/a.py"]
    for section in sections.values():
        assert "diff --git" not in section
        assert "index 1111111" not in section
    assert sections["src/a.py"].startswith("--- a/src/a.py\n")


def test_split_diff_by_path_concatenates_repeated_path():
    diff = (
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -1,2 +1,3 @@\n"
        " keep_a\n"
        "+first\n"
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -40,2 +41,3 @@\n"
        " keep_more\n"
        "+second\n"
    )
    sections = split_diff_by_path(diff)
    assert list(sections) == ["src/a.py"]
    section = sections["src/a.py"]
    assert "@@ -1,2 +1,3 @@" in section
    assert "@@ -40,2 +41,3 @@" in section
    assert section.count("--- a/src/a.py") == 2


def test_split_diff_by_path_keeps_no_newline_marker():
    diff = (
        "--- a/src/a.py\n"
        "+++ b/src/a.py\n"
        "@@ -1 +1 @@\n"
        "-old\n"
        "+new\n"
        "\\ No newline at end of file\n"
    )
    section = split_diff_by_path(diff)["src/a.py"]
    assert section.endswith("\\ No newline at end of file")


def test_split_diff_by_path_empty_input():
    assert split_diff_by_path("") == {}


def test_split_diff_by_path_leaves_line_ranges_unchanged():
    # The added ``lines`` key is additive: the existing reading of hunk headers
    # returns exactly what it returned before the split was introduced.
    assert parse_diff_line_ranges(TWO_FILE_DIFF) == {
        "src/a.py": [[1, 3]],
        "src/b.py": [[10, 11]],
    }

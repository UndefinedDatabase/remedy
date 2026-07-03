"""Tests for missing_tests_gate.py — diff classification + gate status + writer."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.missing_tests_gate import (
    build_missing_tests_gate,
    write_missing_tests_gate,
)

_SOURCE_DIFF = """\
--- a/packages/orchestration/foo.py
+++ b/packages/orchestration/foo.py
@@ -0,0 +1,2 @@
+def foo():
+    return 1
"""

_TEST_DIFF = """\
--- a/tests/orchestration/test_foo.py
+++ b/tests/orchestration/test_foo.py
@@ -0,0 +1,2 @@
+def test_foo():
+    assert True
"""

_DOC_DIFF = """\
--- a/docs/README.md
+++ b/docs/README.md
@@ -0,0 +1,1 @@
+# docs
"""


def _seed(tmp_path: Path, task_id: str, diff: str, tests: str) -> str:
    run = tmp_path / "task_runs" / task_id
    run.mkdir(parents=True)
    (run / "safe.diff").write_text(diff)
    (run / "tests.txt").write_text(tests)
    return str(tmp_path)


def test_source_and_test_changed_no_tests_run_needs_tests(tmp_path):
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF + _TEST_DIFF, "tests_not_run")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["source_files_changed"] is True
    assert gate["test_files_changed"] is True
    assert gate["tests_executed"] is False
    assert gate["suggested_test_commands"] == [
        "python3 -m pytest tests/orchestration/test_foo.py -q"
    ]
    assert gate["schema_version"] == "1.0.0"
    assert gate["task_id"] == "T001"


def test_blocked_environment_flagged(tmp_path):
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF, "tests not run: sandbox blocked")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["tests_blocked_by_environment"] is True


def test_tests_executed_passes(tmp_path):
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF + _TEST_DIFF, "1 passed in 0.01s")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "PASS"
    assert gate["tests_executed"] is True
    assert gate["suggested_test_commands"] == []
    assert gate["test_result_summary"] == "1 passed in 0.01s"


def test_only_docs_changed_passes(tmp_path):
    evidence = _seed(tmp_path, "T001", _DOC_DIFF, "tests_not_run")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "PASS"
    assert gate["source_files_changed"] is False
    assert gate["test_files_changed"] is False
    assert gate["suggested_test_commands"] == []


def test_missing_evidence_files_treated_as_no_change(tmp_path):
    run = tmp_path / "task_runs" / "T001"
    run.mkdir(parents=True)
    gate = build_missing_tests_gate({"task_id": "T001"}, str(tmp_path))

    assert gate["gate_status"] == "PASS"
    assert gate["source_files_changed"] is False
    assert gate["tests_executed"] is False


def test_writer_emits_json_and_registers(tmp_path):
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF, "tests_not_run")
    written: dict[str, str] = {}
    write_missing_tests_gate({"task_id": "T001"}, evidence, written)

    rel = "task_runs/T001/missing_tests_gate.json"
    assert rel in written
    data = json.loads(Path(written[rel]).read_text())
    assert data["gate_status"] == "NEEDS_TESTS"
    assert data["source_files_changed"] is True


def test_writer_noop_on_unsafe_task_id(tmp_path):
    written: dict[str, str] = {}
    write_missing_tests_gate({"task_id": "../evil"}, str(tmp_path), written)
    assert written == {}


_TS_DIFF = """\
--- a/src/components/Widget.ts
+++ b/src/components/Widget.ts
@@ -0,0 +1,2 @@
+export function widget(): string {
+  return "hello";
+}
"""

_TSX_DIFF = """\
--- a/src/components/Widget.tsx
+++ b/src/components/Widget.tsx
@@ -0,0 +1,2 @@
+export function Widget(): JSX.Element {
+  return <div>hello</div>;
+}
"""


def test_ts_source_change_without_tests_needs_tests(tmp_path):
    evidence = _seed(tmp_path, "T001", _TS_DIFF, "tests_not_run")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["source_files_changed"] is True
    assert gate["tests_executed"] is False


def test_tsx_source_change_without_tests_needs_tests(tmp_path):
    evidence = _seed(tmp_path, "T001", _TSX_DIFF, "tests_not_run")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["source_files_changed"] is True
    assert gate["tests_executed"] is False


def test_docs_only_still_pass_with_extended_source(tmp_path):
    evidence = _seed(tmp_path, "T001", _DOC_DIFF, "tests_not_run")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "PASS"
    assert gate["source_files_changed"] is False


def test_sandbox_blocked_error_output_needs_tests(tmp_path):
    """Sandbox-blocked error output must not count as executed tests."""
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF, "pytest error: sandbox blocked")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["tests_executed"] is False
    assert gate["tests_blocked_by_environment"] is True
    assert "blocked" in gate["reason"].lower()


def test_error_sandbox_blocked_output_needs_tests(tmp_path):
    """Bare 'error: sandbox blocked' also must not count as executed."""
    evidence = _seed(tmp_path, "T001", _TS_DIFF, "error: sandbox blocked")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "NEEDS_TESTS"
    assert gate["tests_executed"] is False
    assert gate["tests_blocked_by_environment"] is True


def test_real_failure_without_sandbox_counts_as_executed(tmp_path):
    """Real test failure (no sandbox marker) still counts as executed."""
    evidence = _seed(tmp_path, "T001", _SOURCE_DIFF, "1 failed, 2 error in 0.3s")
    gate = build_missing_tests_gate({"task_id": "T001"}, evidence)

    assert gate["gate_status"] == "PASS"
    assert gate["tests_executed"] is True
    assert gate["tests_blocked_by_environment"] is False

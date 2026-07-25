"""Tests for the deterministic spec compliance checklist module."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.spec_compliance import (
    SCHEMA_VERSION,
    build_spec_compliance_checklist,
    parse_goal_requirements,
    render_checklist_markdown,
    write_spec_compliance_check,
)

GOAL_WITH_EXPLICIT_ARRAYS = """
# Job: Spec Compliance

### Files allowed

- `packages/orchestration/spec_compliance.py` (create new)
- `tests/orchestration/test_spec_compliance.py` (create new)

Schema:

    "required_files": ["packages/orchestration/spec_compliance.py"],
    "allowed_files": ["packages/orchestration/spec_compliance.py", "tests/orchestration/test_spec_compliance.py"],
    "required_artifacts": ["spec_compliance_check.json"],
    "required_functions": ["build_spec_compliance_checklist"],
    "required_constants": ["_REVIEWER_SCOPED_DIFF_CAP"],
    "required_tests": ["test_checklist_detects_present_artifact"],
    "required_strings": ["within review scope"],
    "forbidden_files": ["_run_helper.py"],
    "forbidden_strings": [],
"""


class _Task:
    def __init__(self, task_id: str, title: str, body: str = "") -> None:
        self.task_id = task_id
        self.title = title
        self.body = body


def test_parse_explicit_arrays():
    reqs = parse_goal_requirements(GOAL_WITH_EXPLICIT_ARRAYS)
    assert reqs["required_files"] == ["packages/orchestration/spec_compliance.py"]
    assert "spec_compliance_check.json" in reqs["required_artifacts"]
    assert reqs["required_functions"] == ["build_spec_compliance_checklist"]
    assert reqs["required_constants"] == ["_REVIEWER_SCOPED_DIFF_CAP"]
    assert reqs["required_tests"] == ["test_checklist_detects_present_artifact"]
    assert reqs["required_strings"] == ["within review scope"]
    assert reqs["forbidden_files"] == ["_run_helper.py"]


def test_parse_heuristic_fallbacks():
    goal = (
        "Implement `def widget_count(` and add a test `test_widget_count`.\n"
        "Create `pkg/widget.py` (create new). Use constant `MAX_WIDGETS`.\n"
    )
    reqs = parse_goal_requirements(goal)
    assert "widget_count" in reqs["required_functions"]
    assert "test_widget_count" in reqs["required_tests"]
    assert "pkg/widget.py" in reqs["required_files"]
    assert "pkg/widget.py" in reqs["allowed_files"]
    assert "MAX_WIDGETS" in reqs["required_constants"]


def test_parse_is_deterministic():
    a = parse_goal_requirements(GOAL_WITH_EXPLICIT_ARRAYS)
    b = parse_goal_requirements(GOAL_WITH_EXPLICIT_ARRAYS)
    assert a == b
    # lists are sorted + de-duplicated
    assert a["allowed_files"] == sorted(set(a["allowed_files"]))


def test_checklist_schema_fields_present(tmp_path):
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), workspace=""
    )
    for key in (
        "schema_version", "task_id", "task_title", "required_files",
        "allowed_files", "required_artifacts", "required_functions",
        "required_constants", "required_tests", "required_strings",
        "forbidden_files", "forbidden_strings", "checks", "summary",
        "verdict", "missing_items", "total_checks", "passed", "failed",
    ):
        assert key in checklist, f"missing key: {key}"
    assert checklist["schema_version"] == SCHEMA_VERSION
    assert checklist["task_id"] == "T001"
    assert checklist["verdict"] in ("PASS", "PASS_WITH_RISKS", "FAIL", "BLOCKED")


def test_checklist_detects_missing_file(tmp_path):
    # Empty workspace -> required file is missing.
    workspace = tmp_path / "ws"
    workspace.mkdir()
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), str(workspace)
    )
    file_checks = [c for c in checklist["checks"] if c["type"] == "file"]
    assert file_checks
    assert all(not c["present"] for c in file_checks)
    assert not checklist["summary"]["compliant"]
    assert checklist["verdict"] == "FAIL"
    assert "packages/orchestration/spec_compliance.py" in checklist["missing_items"]
    assert "packages/orchestration/spec_compliance.py" in checklist["summary"]["missing"]


def test_checklist_detects_present_file_and_function(tmp_path):
    workspace = tmp_path / "ws"
    (workspace / "packages" / "orchestration").mkdir(parents=True)
    (workspace / "packages" / "orchestration" / "spec_compliance.py").write_text(
        "def build_spec_compliance_checklist():\n    pass\n", encoding="utf-8"
    )
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), str(workspace)
    )
    by_name = {c["name"]: c for c in checklist["checks"]}
    assert by_name["packages/orchestration/spec_compliance.py"]["present"]
    assert by_name["build_spec_compliance_checklist"]["present"]


def test_checklist_detects_present_artifact(tmp_path):
    evidence_dir = tmp_path / "evidence"
    run_dir = evidence_dir / "task_runs" / "T001"
    run_dir.mkdir(parents=True)
    (run_dir / "spec_compliance_check.json").write_text("{}", encoding="utf-8")

    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(evidence_dir), workspace=""
    )
    artifact_checks = [c for c in checklist["checks"] if c["type"] == "artifact"]
    assert artifact_checks
    present = {c["name"]: c["present"] for c in artifact_checks}
    assert present.get("spec_compliance_check.json") is True


def test_forbidden_file_violation(tmp_path):
    workspace = tmp_path / "ws"
    workspace.mkdir()
    (workspace / "_run_helper.py").write_text("x = 1\n", encoding="utf-8")
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), str(workspace)
    )
    forbidden = [c for c in checklist["checks"] if c["type"] == "forbidden_file"]
    assert forbidden
    violation = forbidden[0]
    assert violation["present"] is True
    assert violation["ok"] is False
    assert checklist["verdict"] == "BLOCKED"
    assert "_run_helper.py" in checklist["summary"]["violations"]


def test_render_markdown_contains_status_and_table(tmp_path):
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), workspace=""
    )
    md = render_checklist_markdown(checklist)
    assert "# Spec Compliance — T001" in md
    assert "**Status:**" in md
    assert "| Result | Type | Requirement | Detail |" in md


def test_write_spec_compliance_check_registers_outputs(tmp_path):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    written: dict[str, str] = {}
    task = _Task("T001", "Spec compliance", GOAL_WITH_EXPLICIT_ARRAYS)

    write_spec_compliance_check(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(evidence_dir), "", written
    )

    assert "task_runs/T001/spec_compliance_check.json" in written
    assert "task_runs/T001/spec_compliance_check.md" in written
    json_path = evidence_dir / "task_runs" / "T001" / "spec_compliance_check.json"
    assert json_path.is_file()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["task_id"] == "T001"
    assert data["schema_version"] == SCHEMA_VERSION


def test_write_spec_compliance_check_rejects_unsafe_task_id(tmp_path):
    written: dict[str, str] = {}
    task = _Task("../evil", "bad", GOAL_WITH_EXPLICIT_ARRAYS)
    write_spec_compliance_check(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), "", written
    )
    assert written == {}


def test_dict_task_supported(tmp_path):
    task = {"task_id": "T002", "title": "Dict task", "body": ""}
    checklist = build_spec_compliance_checklist(
        task, GOAL_WITH_EXPLICIT_ARRAYS, str(tmp_path), workspace=""
    )
    assert checklist["task_id"] == "T002"
    assert checklist["task_title"] == "Dict task"


def test_allowed_test_file_not_flagged_as_out_of_scope():
    goal = (
        "### Files allowed\n\n"
        "- `packages/orchestration/spec_compliance.py` (create new)\n"
        "- `tests/orchestration/test_spec_compliance.py` (create new)\n"
    )
    reqs = parse_goal_requirements(goal)
    assert "tests/orchestration/test_spec_compliance.py" in reqs["allowed_files"]
    assert "packages/orchestration/spec_compliance.py" in reqs["allowed_files"]


def test_missing_required_test_creates_missing_item(tmp_path):
    goal = (
        "### Tests\n\n"
        "1. `test_checklist_detects_present_artifact`\n"
        "2. `test_nonexistent_test_name`\n"
    )
    workspace = tmp_path / "ws"
    workspace.mkdir()
    task = _Task("T001", "Test check")
    checklist = build_spec_compliance_checklist(
        task, goal, str(tmp_path), str(workspace)
    )
    assert "test_nonexistent_test_name" in checklist["missing_items"]
    assert checklist["verdict"] != "PASS"


def test_test_file_path_not_treated_as_required_function():
    goal = (
        "Create the following files:\n"
        "- `tests/orchestration/test_fresh_evidence_gate.py` (create new)\n"
        "- `tests/orchestration/test_artifact_contract_gate.py` (create new)\n"
    )
    reqs = parse_goal_requirements(goal)
    assert "test_fresh_evidence_gate" not in reqs["required_tests"]
    assert "test_artifact_contract_gate" not in reqs["required_tests"]


def test_exact_function_names_still_required():
    goal = (
        "Implement these tests:\n"
        "- `test_matching_job_id_passes`\n"
        "- `test_stale_job_blocks`\n"
    )
    reqs = parse_goal_requirements(goal)
    assert "test_matching_job_id_passes" in reqs["required_tests"]
    assert "test_stale_job_blocks" in reqs["required_tests"]


def test_missing_exact_function_name_creates_missing_item(tmp_path):
    goal = "Add test `test_this_must_exist` to verify behavior."
    workspace = tmp_path / "ws"
    workspace.mkdir()
    task = _Task("T001", "Check test")
    checklist = build_spec_compliance_checklist(
        task, goal, str(tmp_path), str(workspace)
    )
    assert "test_this_must_exist" in checklist["missing_items"]
    assert checklist["verdict"] == "FAIL"


def test_checklist_generation_failure_propagates(tmp_path, monkeypatch):
    """When build_spec_compliance_checklist raises, write_spec_compliance_check
    propagates the error so the caller (job_evidence.py) can write the error
    artifact via its own try/except."""
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    written: dict[str, str] = {}
    task = _Task("T001", "bad")

    import packages.orchestration.spec_compliance as sc
    monkeypatch.setattr(
        sc, "build_spec_compliance_checklist",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    with pytest.raises(RuntimeError, match="boom"):
        write_spec_compliance_check(task, "goal", str(evidence_dir), "", written)
    assert "task_runs/T001/spec_compliance_check.json" not in written


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])

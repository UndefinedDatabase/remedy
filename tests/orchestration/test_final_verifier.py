"""Tests for final_verifier.py — aggregation + verdict logic + writer."""

from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.final_verifier import (
    build_final_verifier_report,
    write_final_verifier_report,
)


def _run_dir(base: Path, task_id: str) -> Path:
    d = base / "task_runs" / task_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _seed_pass_task(base: Path, task_id: str = "T001") -> None:
    """Seed one fully-passing task with complete evidence."""
    d = _run_dir(base, task_id)
    (d / "review_scope_packet.json").write_text(json.dumps({
        "changed_files": ["pkg/review_scope.py"],
        "changed_line_ranges": {"pkg/review_scope.py": [[1, 10]]},
    }))
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "PASS"}))
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "PASS"}))
    (d / "review.json").write_text(json.dumps({"final_verdict": "pass", "reviews": []}))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": []}))
    (d / "tests.txt").write_text("3 passed in 0.1s\n")
    (d / "safe.diff").write_text("--- a/pkg/review_scope.py\n+++ b/pkg/review_scope.py\n")
    (d / "token_accounting.json").write_text(json.dumps({
        "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": 5000,
        "reviewer_prompt_tokens_estimated": 8496,
    }))
    (base / "scratch_file_guard.json").write_text(json.dumps({"guard_status": "PASS"}))
    (base / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": False,
        "estimated_prompt_tokens": 13496,
        "estimated_total_tokens": 13496,
        "measurement_source": "character_heuristic",
        "measurement_confidence": "low",
        "missing_reason": "actual usage unavailable",
        "builder_estimated_total": 5000,
        "reviewer_estimated_total": 8496,
        "repair_estimated_total": 0,
        "provider_call_count": 2,
    }))
    (base / "final_verifier_report.json").write_text(json.dumps({"verdict": "PASS"}))


def test_full_pass(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)

    report = build_final_verifier_report(str(tmp_path))

    assert report["schema_version"] == "1.0.0"
    assert report["verdict"] == "PASS"
    assert report["changed_files"] == ["pkg/review_scope.py"]
    assert report["changed_line_ranges"] == {"pkg/review_scope.py": [[1, 10]]}
    assert report["unresolved_findings"] == []
    assert report["test_status"] == {"ran": True, "passed": 3, "failed": 0}
    assert report["missing_tests_gate"] == "PASS"
    assert report["scratch_file_guard"] == "PASS"
    assert report["spec_compliance"] == "PASS"
    assert report["token_status"]["actual_available"] is False
    assert report["token_status"]["estimated_prompt_tokens"] == 13496
    assert all(report["evidence_completeness"].values())
    assert report["missing_evidence"] == []
    assert report["recommended_action"] == "Approve and promote."


def test_needs_tests(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "NEEDS_TESTS"}))
    (d / "tests.txt").write_text("tests_not_run\n")

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "NEEDS_TESTS"
    assert report["test_status"] == {"ran": False, "passed": 0, "failed": 0}
    assert report["recommended_action"] == "Run the missing tests before promoting."


def test_blocked_by_scratch_guard(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    (tmp_path / "scratch_file_guard.json").write_text(
        json.dumps({"guard_status": "BLOCKED"})
    )

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "BLOCKED"
    assert report["scratch_file_guard"] == "BLOCKED"


def test_blocked_by_spec_compliance(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "BLOCKED"}))

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "BLOCKED"
    assert report["spec_compliance"] == "BLOCKED"


def test_needs_repair_from_open_findings(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "review.json").write_text(json.dumps({
        "final_verdict": "needs_repair",
        "reviews": [{
            "round": 1,
            "findings": [
                {"id": "R1", "severity": "low", "file": "pkg/a.py", "summary": "scope"},
            ],
        }],
    }))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": ["R1"]}))

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "NEEDS_REPAIR"
    assert report["unresolved_findings"] == [{
        "task_id": "T001",
        "finding_id": "R1",
        "severity": "low",
        "file": "pkg/a.py",
        "summary": "scope",
    }]
    assert report["recommended_action"] == "Resolve the open findings before promoting."


def test_needs_repair_from_failed_tests(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "tests.txt").write_text("2 passed, 1 failed in 0.2s\n")

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "NEEDS_REPAIR"
    assert report["test_status"] == {"ran": True, "passed": 2, "failed": 1}


def test_pass_with_risks_missing_optional_evidence(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    # Remove an optional evidence file -> still all gates pass, but incomplete.
    (tmp_path / "task_runs" / "T001" / "review_scope_packet.json").unlink()

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "PASS_WITH_RISKS"
    assert report["evidence_completeness"]["review_scope_packet"] is False
    assert "review_scope_packet" in report["missing_evidence"]
    assert report["recommended_action"].startswith("Approve with risks")


def test_empty_evidence_dir(tmp_path: Path) -> None:
    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "PASS_WITH_RISKS"
    assert report["changed_files"] == []
    assert report["unresolved_findings"] == []
    assert set(report["missing_evidence"]) == set(report["evidence_completeness"])


def test_worst_status_across_tasks(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path, "T001")
    _seed_pass_task(tmp_path, "T002")
    (tmp_path / "task_runs" / "T002" / "missing_tests_gate.json").write_text(
        json.dumps({"gate_status": "NEEDS_TESTS"})
    )

    report = build_final_verifier_report(str(tmp_path))

    assert report["missing_tests_gate"] == "NEEDS_TESTS"
    assert report["verdict"] == "NEEDS_TESTS"


def test_changed_files_merged_across_tasks(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path, "T001")
    d = _run_dir(tmp_path, "T002")
    (d / "review_scope_packet.json").write_text(json.dumps({
        "changed_files": ["pkg/other.py"],
        "changed_line_ranges": {},
    }))
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "PASS"}))
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "PASS"}))
    (d / "review.json").write_text(json.dumps({"final_verdict": "pass", "reviews": []}))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": []}))
    (d / "tests.txt").write_text("1 passed\n")
    (d / "safe.diff").write_text("diff\n")

    report = build_final_verifier_report(str(tmp_path))

    assert report["changed_files"] == ["pkg/other.py", "pkg/review_scope.py"]


def test_writer_creates_report(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    written: dict[str, str] = {}

    write_final_verifier_report(str(tmp_path), written)

    assert "final_verifier_report.json" in written
    data = json.loads((tmp_path / "final_verifier_report.json").read_text())
    assert data["verdict"] == "PASS"


def test_writer_noop_without_evidence_dir(tmp_path: Path) -> None:
    written: dict[str, str] = {}
    write_final_verifier_report("", written)
    assert written == {}


def test_line_ranges_merged_across_tasks(tmp_path: Path) -> None:
    # F1: same file in two tasks -> ranges unioned, not first-wins.
    _seed_pass_task(tmp_path, "T001")  # pkg/review_scope.py ranges [[1, 10]]
    d = _run_dir(tmp_path, "T002")
    (d / "review_scope_packet.json").write_text(json.dumps({
        "changed_files": ["pkg/review_scope.py"],
        "changed_line_ranges": {"pkg/review_scope.py": [[20, 25]]},
    }))
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "PASS"}))
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "PASS"}))
    (d / "review.json").write_text(json.dumps({"final_verdict": "pass", "reviews": []}))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": []}))
    (d / "tests.txt").write_text("1 passed\n")
    (d / "safe.diff").write_text("diff\n")

    report = build_final_verifier_report(str(tmp_path))

    assert report["changed_line_ranges"] == {
        "pkg/review_scope.py": [[1, 10], [20, 25]],
    }


def test_needs_tests_surfaces_repair_signal(tmp_path: Path) -> None:
    # F2: NEEDS_TESTS wins precedence but repair condition must not be masked.
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "NEEDS_TESTS"}))
    (d / "tests.txt").write_text("2 passed, 1 failed in 0.2s\n")

    report = build_final_verifier_report(str(tmp_path))

    assert report["verdict"] == "NEEDS_TESTS"
    assert report["also_needs_repair"] is True
    assert "also present" in report["recommended_action"]


def test_pass_not_flagged_for_repair(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    report = build_final_verifier_report(str(tmp_path))
    assert report["also_needs_repair"] is False


def test_token_status_reads_token_truth_json(tmp_path: Path) -> None:
    """Final verifier reads token_truth.json when present and returns its fields."""
    _seed_pass_task(tmp_path)
    (tmp_path / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": False,
        "actual_prompt_tokens": None,
        "actual_completion_tokens": None,
        "actual_total_tokens": None,
        "estimated_prompt_tokens": 9500,
        "estimated_completion_tokens": 0,
        "estimated_total_tokens": 9500,
        "measurement_source": "character_heuristic",
        "measurement_confidence": "low",
        "missing_reason": "actual usage unavailable from claude-cli output",
        "builder_estimated_total": 5000,
        "reviewer_estimated_total": 4500,
        "repair_estimated_total": 0,
        "provider_call_count": 2,
    }))

    report = build_final_verifier_report(str(tmp_path))
    ts = report["token_status"]

    assert ts["actual_available"] is False
    assert ts["estimated_prompt_tokens"] == 9500
    assert ts["estimated_total_tokens"] == 9500
    assert ts["measurement_source"] == "character_heuristic"
    assert ts["measurement_confidence"] == "low"
    assert ts["builder_estimated_total"] == 5000
    assert ts["reviewer_estimated_total"] == 4500
    assert ts["provider_call_count"] == 2
    assert ts["missing_reason"] is not None


def test_token_status_fallback_without_token_truth(tmp_path: Path) -> None:
    """Without token_truth.json, falls back to per-task token_accounting."""
    _seed_pass_task(tmp_path)
    (tmp_path / "token_truth.json").unlink()

    report = build_final_verifier_report(str(tmp_path))
    ts = report["token_status"]

    assert ts["actual_available"] is False
    assert ts["estimated_prompt_tokens"] == 13496
    assert "measurement_source" not in ts


def test_evidence_completeness_includes_token_truth(tmp_path: Path) -> None:
    """Evidence completeness tracks token_truth (not final_verifier_report —
    the report cannot verify its own existence at build time)."""
    _seed_pass_task(tmp_path)
    (tmp_path / "token_truth.json").unlink()

    report = build_final_verifier_report(str(tmp_path))
    ec = report["evidence_completeness"]

    assert "token_truth" in ec
    assert ec["token_truth"] is False
    assert "final_verifier_report" not in ec

    (tmp_path / "token_truth.json").write_text("{}")
    report2 = build_final_verifier_report(str(tmp_path))
    assert report2["evidence_completeness"]["token_truth"] is True


def test_written_report_does_not_mark_itself_missing(tmp_path: Path) -> None:
    """Freshly written final_verifier_report.json must not list itself as
    missing evidence."""
    _seed_pass_task(tmp_path)
    (tmp_path / "final_verifier_report.json").unlink()
    written: dict[str, str] = {}

    write_final_verifier_report(str(tmp_path), written)

    data = json.loads((tmp_path / "final_verifier_report.json").read_text())
    assert "final_verifier_report" not in data.get("missing_evidence", [])
    assert "final_verifier_report" not in data.get("evidence_completeness", {})

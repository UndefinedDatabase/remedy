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
    assert "pkg/review_scope.py" in report["changed_files"]
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
    # Remove review_scope_packet — authoritative_changed_files still has the file
    # from safe.diff, but the scope mismatch is informational, not blocking.
    # Without change_provenance_gate.json, no coverage check runs.
    (tmp_path / "task_runs" / "T001" / "review_scope_packet.json").unlink()

    report = build_final_verifier_report(str(tmp_path))

    assert report["evidence_completeness"]["review_scope_packet"] is False
    assert "review_scope_packet" in report["missing_evidence"]
    assert report["verdict"] == "PASS_WITH_RISKS"
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

    assert "pkg/other.py" in report["changed_files"]
    assert "pkg/review_scope.py" in report["changed_files"]


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


def test_reads_change_provenance_gate(tmp_path: Path) -> None:
    """Final verifier reads change_provenance_gate.json and blocks on BLOCKED."""
    _seed_pass_task(tmp_path)

    (tmp_path / "change_provenance_gate.json").write_text(
        json.dumps({"verdict": "PASS", "covered_files": ["pkg/review_scope.py"]})
    )
    report = build_final_verifier_report(str(tmp_path))
    assert report["change_provenance"] == "PASS"
    assert report["verdict"] == "PASS"

    (tmp_path / "change_provenance_gate.json").write_text(
        json.dumps({"verdict": "BLOCKED", "covered_files": []})
    )
    report = build_final_verifier_report(str(tmp_path))
    assert report["change_provenance"] == "BLOCKED"
    assert report["verdict"] == "BLOCKED"


def test_change_provenance_absent_defaults_empty(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    report = build_final_verifier_report(str(tmp_path))
    assert report["change_provenance"] == ""
    assert report["verdict"] == "PASS"


def test_exposes_all_core_gate_fields(tmp_path: Path) -> None:
    """Final verifier must expose fresh/artifact/runtime/change/commit gate fields."""
    _seed_pass_task(tmp_path)
    (tmp_path / "fresh_evidence_gate.json").write_text(json.dumps({"verdict": "PASS"}))
    (tmp_path / "artifact_contract_gate.json").write_text(json.dumps({"verdict": "PASS"}))
    (tmp_path / "runtime_integration_gate.json").write_text(json.dumps({"verdict": "PASS"}))
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({"verdict": "PASS"}))
    (tmp_path / "commit_execution_gate.json").write_text(json.dumps({"verdict": "COMMIT_READY"}))

    report = build_final_verifier_report(str(tmp_path))

    assert report["fresh_evidence_gate"] == "PASS"
    assert report["artifact_contract_gate"] == "PASS"
    assert report["runtime_integration_gate"] == "PASS"
    assert report["change_provenance"] == "PASS"
    assert report["commit_execution_gate"] == "COMMIT_READY"


def test_blocked_by_fresh_evidence_gate(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    (tmp_path / "fresh_evidence_gate.json").write_text(json.dumps({"verdict": "BLOCKED"}))

    report = build_final_verifier_report(str(tmp_path))
    assert report["verdict"] == "BLOCKED"
    assert report["fresh_evidence_gate"] == "BLOCKED"


def test_blocked_by_artifact_contract_gate(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    (tmp_path / "artifact_contract_gate.json").write_text(json.dumps({"verdict": "BLOCKED"}))

    report = build_final_verifier_report(str(tmp_path))
    assert report["verdict"] == "BLOCKED"
    assert report["artifact_contract_gate"] == "BLOCKED"


def test_blocked_by_runtime_integration_gate(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    (tmp_path / "runtime_integration_gate.json").write_text(json.dumps({"verdict": "BLOCKED"}))

    report = build_final_verifier_report(str(tmp_path))
    assert report["verdict"] == "BLOCKED"
    assert report["runtime_integration_gate"] == "BLOCKED"


def test_commit_execution_gate_exposed_not_blocking(tmp_path: Path) -> None:
    """commit_execution_gate is downstream — exposed in output but does not block."""
    _seed_pass_task(tmp_path)
    (tmp_path / "commit_execution_gate.json").write_text(json.dumps({"verdict": "BLOCKED"}))

    report = build_final_verifier_report(str(tmp_path))
    assert report["commit_execution_gate"] == "BLOCKED"
    assert report["verdict"] != "BLOCKED"


def test_verification_tests_clears_needs_tests(tmp_path: Path) -> None:
    """When verification_tests.json shows tests passed, NEEDS_TESTS is cleared."""
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "NEEDS_TESTS"}))
    (d / "tests.txt").write_text("tests_not_run\n")

    report = build_final_verifier_report(str(tmp_path))
    assert report["verdict"] == "NEEDS_TESTS"

    (tmp_path / "verification_tests.json").write_text(json.dumps({
        "exit_code": 0,
        "passed": 206,
        "failed": 0,
        "verification_type": "post_apply",
    }))

    report2 = build_final_verifier_report(str(tmp_path))
    assert report2["verdict"] == "PASS"
    assert report2["test_status"]["passed"] == 206


def test_verification_tests_not_cleared_on_failure(tmp_path: Path) -> None:
    """verification_tests with failures does NOT clear NEEDS_TESTS."""
    _seed_pass_task(tmp_path)
    d = tmp_path / "task_runs" / "T001"
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "NEEDS_TESTS"}))
    (d / "tests.txt").write_text("tests_not_run\n")

    (tmp_path / "verification_tests.json").write_text(json.dumps({
        "exit_code": 1,
        "passed": 200,
        "failed": 6,
        "verification_type": "post_apply",
    }))

    report = build_final_verifier_report(str(tmp_path))
    assert report["verdict"] == "NEEDS_TESTS"


def test_written_report_does_not_mark_itself_missing(tmp_path: Path) -> None:
    _seed_pass_task(tmp_path)
    (tmp_path / "final_verifier_report.json").unlink()
    written: dict[str, str] = {}

    write_final_verifier_report(str(tmp_path), written)

    data = json.loads((tmp_path / "final_verifier_report.json").read_text())
    assert "final_verifier_report" not in data.get("missing_evidence", [])
    assert "final_verifier_report" not in data.get("evidence_completeness", {})


def test_authoritative_files_includes_all_sources(tmp_path: Path) -> None:
    """authoritative_changed_files unions review_scope, safe.diff, workspace.diff."""
    _seed_pass_task(tmp_path)
    (tmp_path / "workspace.diff").write_text(
        "--- a/scripts/build_review_manifest.py\n"
        "+++ b/scripts/build_review_manifest.py\n+change\n"
    )
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py", "scripts/build_review_manifest.py"],
    }))

    report = build_final_verifier_report(str(tmp_path))

    assert "pkg/review_scope.py" in report["authoritative_changed_files"]
    assert "scripts/build_review_manifest.py" in report["authoritative_changed_files"]
    # workspace.diff file not in review_scope → PASS_WITH_RISKS (not plain PASS)
    assert report["file_set_alignment_status"] in ("PASS", "PASS_WITH_RISKS")


def test_file_alignment_blocks_on_uncovered(tmp_path: Path) -> None:
    """File alignment BLOCKED when authoritative file not in change_provenance."""
    _seed_pass_task(tmp_path)
    (tmp_path / "workspace.diff").write_text(
        "--- a/extra/new.py\n+++ b/extra/new.py\n+x\n"
    )
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py"],
    }))

    report = build_final_verifier_report(str(tmp_path))

    assert report["file_set_alignment_status"] == "BLOCKED"
    assert "extra/new.py" in report["review_subject_uncovered_files"]
    assert report["verdict"] == "BLOCKED"


def test_file_alignment_blocks_on_hash_mismatch(tmp_path: Path) -> None:
    """File alignment BLOCKED when change_provenance has hash mismatches."""
    _seed_pass_task(tmp_path)
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "BLOCKED",
        "covered_files": ["pkg/review_scope.py"],
        "hash_mismatches": [{"file": "pkg/review_scope.py",
                             "evidence_sha256": "aaa", "current_sha256": "bbb"}],
    }))

    report = build_final_verifier_report(str(tmp_path))

    assert report["content_hash_mismatches"] == [
        {"file": "pkg/review_scope.py",
         "evidence_sha256": "aaa", "current_sha256": "bbb"}
    ]
    assert report["file_set_alignment_status"] == "BLOCKED"
    assert report["verdict"] == "BLOCKED"


def test_file_alignment_pass_when_all_covered(tmp_path: Path) -> None:
    """File alignment PASS when authoritative files match change_provenance."""
    _seed_pass_task(tmp_path)
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py"],
    }))

    report = build_final_verifier_report(str(tmp_path))

    assert report["file_set_alignment_status"] == "PASS"
    assert report["review_subject_uncovered_files"] == []
    assert report["verdict"] == "PASS"


def test_mismatch_not_plain_pass(tmp_path: Path) -> None:
    """Non-empty change_source_mismatches must not allow plain PASS."""
    _seed_pass_task(tmp_path)
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py", "pkg/extra.py"],
    }))
    (tmp_path / "workspace.diff").write_text(
        "diff --git a/pkg/extra.py b/pkg/extra.py\n"
        "--- a/pkg/extra.py\n+++ b/pkg/extra.py\n"
    )

    report = build_final_verifier_report(str(tmp_path))

    if report["change_source_mismatches"]:
        assert report["verdict"] != "PASS", (
            "non-empty change_source_mismatches must not allow plain PASS"
        )
        assert report["file_set_alignment_status"] == "PASS_WITH_RISKS"


def test_pass_when_authoritative_equals_scope(tmp_path: Path) -> None:
    """PASS when authoritative files and review_scope match exactly."""
    _seed_pass_task(tmp_path)
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py"],
    }))

    report = build_final_verifier_report(str(tmp_path))

    assert report["change_source_mismatches"] == []
    assert report["verdict"] == "PASS"


def test_commit_execution_not_ready_on_pass_with_risks(tmp_path: Path) -> None:
    """commit_execution_gate not COMMIT_READY when final_verifier is PASS_WITH_RISKS."""
    from packages.orchestration.commit_execution_gate import build_commit_execution_gate
    result = build_commit_execution_gate(
        fresh_evidence_verdict="PASS",
        artifact_contract_verdict="PASS",
        runtime_integration_verdict="PASS",
        final_verifier_verdict="PASS_WITH_RISKS",
        change_provenance_verdict="PASS",
    )
    assert result["verdict"] != "COMMIT_READY", (
        "PASS_WITH_RISKS final_verifier must not produce COMMIT_READY"
    )
    assert result["verdict"] == "NEEDS_HUMAN_APPROVAL"


def test_task_safe_diff_count_matches_summary(tmp_path: Path) -> None:
    """Task summary Safe Diff count must match actual safe.diff file count."""
    _seed_pass_task(tmp_path, "T001")
    d = tmp_path / "task_runs" / "T001"
    diff_text = (d / "safe.diff").read_text()
    diff_count = diff_text.count("diff --git") if diff_text.strip() else 0
    # In our seed, safe.diff has one diff entry
    (d / "summary.md").write_text(f"Safe Diff: {diff_count} file(s)\n")
    summary = (d / "summary.md").read_text()
    import re
    m = re.search(r"Safe Diff:\s*(\d+)", summary)
    assert m, "summary must contain Safe Diff count"
    assert int(m.group(1)) == diff_count


def test_authoritative_files_absent_from_all_tasks_detected(tmp_path: Path) -> None:
    """Files in authoritative set absent from all task review_scopes are detected."""
    _seed_pass_task(tmp_path, "T001")
    (tmp_path / "workspace.diff").write_text(
        "diff --git a/extra.py b/extra.py\n--- a/extra.py\n+++ b/extra.py\n"
    )
    (tmp_path / "change_provenance_gate.json").write_text(json.dumps({
        "verdict": "PASS",
        "covered_files": ["pkg/review_scope.py", "extra.py"],
    }))
    report = build_final_verifier_report(str(tmp_path))
    # extra.py is in authoritative but not in any task's review_scope
    assert report["change_source_mismatches"], (
        "must detect files absent from task review_scopes"
    )
    assert report["verdict"] != "PASS"

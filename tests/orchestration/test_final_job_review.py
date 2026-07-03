"""Tests for final job-level review (final_job_review)."""
from __future__ import annotations

from packages.orchestration.final_job_review import (
    SCHEMA_VERSION,
    FinalJobVerdict,
    build_final_job_repair_loop,
    build_final_job_review,
)

_GOAL = "Build sticky builder/reviewer repair loop"
_PLAN = [{"id": "T001"}, {"id": "T002"}, {"id": "T003"}]
_SUMMARIES = ["did T001", "did T002", "did T003"]
_DIFFS = ["diff1", "diff2", "diff3"]
_CLEAN_TESTS = {"passed": 30, "failed": 0, "errors": 0}
_CLEAN_GATES = [{"name": "proof_chain", "verdict": "pass"}]


def _pass_verdicts():
    return [
        {"task_id": "T001", "verdict": "pass"},
        {"task_id": "T002", "verdict": "staged_review_passed"},
        {"task_id": "T003", "verdict": "pass"},
    ]


def test_pass_case_no_findings():
    report = build_final_job_review(
        _GOAL, _PLAN, _SUMMARIES, _DIFFS, _pass_verdicts(), _CLEAN_TESTS, _CLEAN_GATES
    )
    expected_keys = {
        "schema_version",
        "job_id",
        "job_goal",
        "verdict",
        "findings",
        "task_count",
        "tasks_reviewed",
        "scope_check",
        "acceptance_criteria_check",
        "changed_files_match",
    }
    assert set(report) == expected_keys
    assert report["schema_version"] == SCHEMA_VERSION
    assert report["verdict"] == FinalJobVerdict.PASS.value
    assert report["findings"] == []
    assert report["task_count"] == 3
    assert report["tasks_reviewed"] == 3
    assert report["changed_files_match"] is True


def test_findings_case_needs_repair():
    verdicts = [
        {"task_id": "T001", "verdict": "pass"},
        {"task_id": "T002", "verdict": "needs_repair"},
        {"task_id": "T003", "verdict": "pass"},
    ]
    report = build_final_job_review(
        _GOAL, _PLAN, _SUMMARIES, _DIFFS, verdicts, _CLEAN_TESTS, _CLEAN_GATES
    )
    assert report["verdict"] == FinalJobVerdict.NEEDS_REPAIR.value
    assert len(report["findings"]) == 1
    assert report["findings"][0]["severity"] == "repairable"


def test_blocker_detection_from_task_verdict():
    verdicts = [
        {"task_id": "T001", "verdict": "pass"},
        {"task_id": "T002", "verdict": "blocked"},
        {"task_id": "T003", "verdict": "pass"},
    ]
    report = build_final_job_review(
        _GOAL, _PLAN, _SUMMARIES, _DIFFS, verdicts, _CLEAN_TESTS, _CLEAN_GATES
    )
    assert report["verdict"] == FinalJobVerdict.BLOCKED.value
    assert report["findings"][0]["severity"] == "critical"


def test_blocker_detection_from_failing_tests():
    report = build_final_job_review(
        _GOAL,
        _PLAN,
        _SUMMARIES,
        _DIFFS,
        _pass_verdicts(),
        {"passed": 28, "failed": 2, "errors": 0},
        _CLEAN_GATES,
    )
    assert report["verdict"] == FinalJobVerdict.BLOCKED.value
    categories = {f["category"] for f in report["findings"]}
    assert "test_evidence" in categories


def test_blocker_detection_from_failing_gate():
    gates = [{"name": "proof_chain", "verdict": "fail"}]
    report = build_final_job_review(
        _GOAL, _PLAN, _SUMMARIES, _DIFFS, _pass_verdicts(), _CLEAN_TESTS, gates
    )
    assert report["verdict"] == FinalJobVerdict.BLOCKED.value
    assert any(f["category"] == "proof_gate" for f in report["findings"])


def test_scope_check_detects_out_of_scope_file():
    report = build_final_job_review(
        _GOAL,
        _PLAN,
        _SUMMARIES,
        _DIFFS,
        _pass_verdicts(),
        _CLEAN_TESTS,
        _CLEAN_GATES,
        expected_changed_files=["a.py", "b.py"],
        actual_changed_files=["a.py", "b.py", "secret.py"],
    )
    assert report["changed_files_match"] is False
    assert report["scope_check"]["in_scope"] is False
    assert report["verdict"] == FinalJobVerdict.NEEDS_REPAIR.value
    assert any(f["category"] == "scope" for f in report["findings"])


def test_scope_check_passes_when_within_plan():
    report = build_final_job_review(
        _GOAL,
        _PLAN,
        _SUMMARIES,
        _DIFFS,
        _pass_verdicts(),
        _CLEAN_TESTS,
        _CLEAN_GATES,
        expected_changed_files=["a.py", "b.py"],
        actual_changed_files=["a.py"],
    )
    assert report["changed_files_match"] is True
    assert report["verdict"] == FinalJobVerdict.PASS.value


def test_acceptance_criteria_check():
    report = build_final_job_review(
        _GOAL,
        _PLAN,
        _SUMMARIES,
        _DIFFS,
        _pass_verdicts(),
        _CLEAN_TESTS,
        _CLEAN_GATES,
        acceptance_criteria=[{"met": True}, {"met": False}, {"met": True}],
    )
    assert report["acceptance_criteria_check"]["total"] == 3
    assert report["acceptance_criteria_check"]["unmet"] == 1
    assert report["acceptance_criteria_check"]["all_met"] is False
    assert report["verdict"] == FinalJobVerdict.NEEDS_REPAIR.value


def test_finding_to_task_routing():
    verdicts = [
        {"task_id": "T001", "verdict": "pass"},
        {"task_id": "T002", "verdict": "needs_repair"},
        {"task_id": "T003", "verdict": "pass"},
    ]
    report = build_final_job_review(
        _GOAL, _PLAN, _SUMMARIES, _DIFFS, verdicts, _CLEAN_TESTS, _CLEAN_GATES
    )
    finding = report["findings"][0]
    assert finding["task_id"] == "T002"


def test_empty_task_list():
    report = build_final_job_review(_GOAL, [], [], [], [], {}, [])
    assert report["task_count"] == 0
    assert report["tasks_reviewed"] == 0
    assert report["findings"] == []
    assert report["verdict"] == FinalJobVerdict.PASS.value


def test_job_id_and_goal_recorded():
    report = build_final_job_review(
        _GOAL,
        _PLAN,
        _SUMMARIES,
        _DIFFS,
        _pass_verdicts(),
        _CLEAN_TESTS,
        _CLEAN_GATES,
        job_id="JOB-5741",
    )
    assert report["job_id"] == "JOB-5741"
    assert report["job_goal"] == _GOAL


# --- repair loop ---------------------------------------------------------


def test_repair_loop_basic_shape():
    loop = build_final_job_repair_loop(
        findings=[{"id": "F-TASK-002"}],
        repair_tasks=[{"id": "R1", "status": "completed"}],
        re_review_verdict="PASS",
    )
    expected_keys = {
        "schema_version",
        "findings_count",
        "repair_tasks_created",
        "repair_tasks_completed",
        "re_review_verdict",
        "rounds",
        "budget",
        "budget_remaining",
        "budget_exhausted",
        "resolved",
    }
    assert set(loop) == expected_keys
    assert loop["findings_count"] == 1
    assert loop["repair_tasks_created"] == 1
    assert loop["repair_tasks_completed"] == 1


def test_re_review_after_repair_passes():
    loop = build_final_job_repair_loop(
        findings=[{"id": "F1"}],
        repair_tasks=[{"id": "R1", "status": "done"}],
        re_review_verdict="pass",
        rounds=1,
        budget=3,
    )
    assert loop["re_review_verdict"] == "PASS"
    assert loop["resolved"] is True
    assert loop["budget_remaining"] == 2
    assert loop["budget_exhausted"] is False


def test_repair_budget_exhaustion():
    loop = build_final_job_repair_loop(
        findings=[{"id": "F1"}, {"id": "F2"}],
        repair_tasks=[{"id": "R1", "status": "pending"}],
        re_review_verdict="NEEDS_REPAIR",
        rounds=3,
        budget=3,
    )
    assert loop["budget_remaining"] == 0
    assert loop["budget_exhausted"] is True
    assert loop["repair_tasks_completed"] == 0
    assert loop["resolved"] is False


def test_repair_loop_counts_completed_only():
    loop = build_final_job_repair_loop(
        findings=[{"id": "F1"}],
        repair_tasks=[
            {"id": "R1", "status": "completed"},
            {"id": "R2", "status": "pending"},
            {"id": "R3", "status": "done"},
        ],
        re_review_verdict="NEEDS_REPAIR",
    )
    assert loop["repair_tasks_created"] == 3
    assert loop["repair_tasks_completed"] == 2

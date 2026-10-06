"""Tests for `packages.orchestration.client_digest` (T002, DECISION F295 D4).

Each test sets `REMEDY_DATA_DIR` to a short directory from
`tmp_path_factory.mktemp`, as `tests/cli/test_serve_cmd.py` does.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration.client_digest import _decision_entry, build_client_digest
from packages.orchestration.decision_queue import HumanDecision
from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
from packages.orchestration.job_apply import job_apply_landed
from packages.orchestration.pingpong_job import JobPlan, save_job_plan

NOW = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture
def root(tmp_path_factory, monkeypatch) -> Path:
    base = tmp_path_factory.mktemp("cd")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(base))
    return base


def _apply_record(root: Path, job_id: str, name: str, body: str) -> None:
    record_dir = root / "job_apply_records" / job_id
    record_dir.mkdir(parents=True, exist_ok=True)
    (record_dir / name).write_text(body)


# ── job_apply_landed ──────────────────────────────────────────────────────


def test_job_apply_landed_is_false_with_no_records_directory(root):
    assert job_apply_landed("no-such-job") is False


@pytest.mark.parametrize("status", ["dry_run", "blocked"])
def test_job_apply_landed_is_false_for_a_status_that_is_not_applied(root, status):
    _apply_record(root, "job-1", "a.json", json.dumps({"status": status}))

    assert job_apply_landed("job-1") is False


def test_job_apply_landed_is_true_when_one_record_reads_applied(root):
    _apply_record(root, "job-2", "a.json", json.dumps({"status": "blocked"}))
    _apply_record(root, "job-2", "b.json", json.dumps({"status": "applied"}))

    assert job_apply_landed("job-2") is True


def test_job_apply_landed_skips_a_file_of_invalid_json_beside_an_applied_record(root):
    _apply_record(root, "job-3", "bad.json", "{not json")
    _apply_record(root, "job-3", "good.json", json.dumps({"status": "applied"}))

    assert job_apply_landed("job-3") is True


# ── build_client_digest ───────────────────────────────────────────────────


def test_build_client_digest_on_an_empty_data_root_equals_the_version_1_frame(root):
    digest = build_client_digest(now=NOW)

    assert digest == {
        "version": 1,
        "read_at": NOW.isoformat(),
        "supervisor": {"answers": False},
        "projects": [],
        "jobs": [],
        "awaiting_apply": [],
        "decisions": [],
        "degraded": False,
        "skipped_files": [],
    }


def test_build_client_digest_names_a_job_file_that_is_not_valid_json_as_degraded(root):
    from packages.orchestration.data_paths import jobs_dir

    bad_dir = jobs_dir(root) / "bad-job-id"
    bad_dir.mkdir(parents=True)
    (bad_dir / "job.json").write_text("not json")

    digest = build_client_digest(now=NOW)

    assert digest["degraded"] is True
    assert "bad-job-id" in digest["skipped_files"]


# ── build_client_digest's decisions key (T002, DECISION F295 D5) ─────────────


def _job_metadata() -> dict:
    """A fresh metadata dict naming a target repo, so `derive_stop_reasons` does
    not add its own `no_target_repo` decision on top of the one each test pins."""
    return {"target_repo": "/tmp/fake-repo"}


def test_a_task_decision_with_a_default_is_listed_as_the_whole_d5_object(root):
    job = JobPlan(job_title="port-job", project_id="proj-1", metadata=_job_metadata())
    record = enqueue_task_decision(
        job, task_id="T001", question="Which port?",
        options=["8080", "9090"], safe_default="8080", now=NOW,
    )
    save_job_plan(job)

    digest = build_client_digest(now=NOW)

    created = datetime.fromisoformat(record["created_at"])
    assert digest["decisions"] == [{
        "job_id": str(job.job_id),
        "project_id": "proj-1",
        "decision_id": record["decision_id"],
        "type": "task_decision",
        "severity": "blocker",
        "question": "Which port?",
        "default": "8080",
        "options": ["8080", "9090"],
        "clarifications": [],
        "created_at": record["created_at"],
        "age_seconds": int((NOW - created).total_seconds()),
    }]


def test_a_task_decision_without_a_default_has_a_null_default(root):
    job = JobPlan(job_title="port-job-2", project_id="proj-1", metadata=_job_metadata())
    enqueue_task_decision(
        job, task_id="T001", question="Which port?",
        options=["8080", "9090"], safe_default="", now=NOW,
    )
    save_job_plan(job)

    digest = build_client_digest(now=NOW)

    [entry] = digest["decisions"]
    assert entry["default"] is None


def test_a_pending_task_plan_approval_carries_its_clarification_and_no_default(root):
    job = JobPlan(
        job_title="plan-job",
        project_id="proj-1",
        metadata=_job_metadata(),
        task_plan={
            "_approval": "pending",
            "clarifications_resolved": [
                {"id": "q1", "question": "Which database?", "default_answer": "sqlite"},
            ],
        },
    )
    save_job_plan(job)

    digest = build_client_digest(now=NOW)

    assert digest["decisions"] == [{
        "job_id": str(job.job_id),
        "project_id": "proj-1",
        "decision_id": "plan:approval",
        "type": "task_plan_approval",
        "severity": "blocker",
        "question": "Task plan awaiting approval (1 open question).",
        "default": None,
        "options": ["approve", "reject"],
        "clarifications": [
            {"id": "q1", "question": "Which database?", "default": "sqlite"},
        ],
        "created_at": "",
        "age_seconds": None,
    }]


def test_an_answered_task_decision_is_not_listed(root):
    job = JobPlan(job_title="answered-job", project_id="proj-1", metadata=_job_metadata())
    record = enqueue_task_decision(
        job, task_id="T001", question="Which port?", options=["8080"], now=NOW,
    )
    answer_task_decision(job, record["decision_id"], answer="8080", now=NOW)
    save_job_plan(job)

    digest = build_client_digest(now=NOW)

    assert digest["decisions"] == []


def test_two_jobs_decisions_are_sorted_by_job_id_then_decision_id(root):
    job_a = JobPlan(job_title="job-a", project_id="proj-1", metadata=_job_metadata())
    first = enqueue_task_decision(job_a, task_id="T001", question="Q1", options=["x"], now=NOW)
    second = enqueue_task_decision(job_a, task_id="T002", question="Q2", options=["y"], now=NOW)
    save_job_plan(job_a)

    job_b = JobPlan(job_title="job-b", project_id="proj-2", metadata=_job_metadata())
    third = enqueue_task_decision(job_b, task_id="T003", question="Q3", options=["z"], now=NOW)
    save_job_plan(job_b)

    digest = build_client_digest(now=NOW)

    actual_keys = [(d["job_id"], d["decision_id"]) for d in digest["decisions"]]
    expected_keys = sorted([
        (str(job_a.job_id), first["decision_id"]),
        (str(job_a.job_id), second["decision_id"]),
        (str(job_b.job_id), third["decision_id"]),
    ])
    assert actual_keys == expected_keys


def test_a_job_whose_decisions_cannot_be_read_marks_degraded_and_skips_only_that_job(
        root, monkeypatch):
    import packages.orchestration.client_digest as client_digest_mod
    from packages.orchestration.decision_queue import list_decisions as real_list_decisions

    bad_job = JobPlan(job_title="bad-job", project_id="proj-1", metadata=_job_metadata())
    enqueue_task_decision(bad_job, task_id="T001", question="Q1", options=["a"], now=NOW)
    save_job_plan(bad_job)

    good_job = JobPlan(job_title="good-job", project_id="proj-2", metadata=_job_metadata())
    good_record = enqueue_task_decision(
        good_job, task_id="T002", question="Q2", options=["b"], now=NOW)
    save_job_plan(good_job)

    def fake_list_decisions(job, events):
        if str(job.job_id) == str(bad_job.job_id):
            raise RuntimeError("boom")
        return real_list_decisions(job, events)

    monkeypatch.setattr(client_digest_mod, "list_decisions", fake_list_decisions)

    digest = build_client_digest(now=NOW)

    assert digest["degraded"] is True
    assert f"decisions of job {bad_job.job_id}" in digest["skipped_files"]
    [entry] = digest["decisions"]
    assert entry["decision_id"] == good_record["decision_id"]


def test_the_age_helper_reads_an_offsetless_created_at_as_utc():
    decision = HumanDecision(
        id="d1", type="stop_reason", status="open", severity="blocker",
        source="s", related_node_id="", related_intent_id="", related_file="",
        safe_summary="s", next_actions=(), created_at="2026-01-01T11:59:00",
        resolved_at=None,
    )

    entry = _decision_entry("job-1", "proj-1", decision, NOW)

    assert entry["age_seconds"] == 60


def test_the_age_helper_reads_a_non_iso8601_created_at_as_null():
    decision = HumanDecision(
        id="d2", type="stop_reason", status="open", severity="blocker",
        source="s", related_node_id="", related_intent_id="", related_file="",
        safe_summary="s", next_actions=(), created_at="not-a-date",
        resolved_at=None,
    )

    entry = _decision_entry("job-1", "proj-1", decision, NOW)

    assert entry["age_seconds"] is None

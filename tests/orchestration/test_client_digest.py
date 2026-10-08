"""Tests for `packages.orchestration.client_digest` (T002, DECISION F295 D4).

Each test sets `REMEDY_DATA_DIR` to a short directory from
`tmp_path_factory.mktemp`, as `tests/cli/test_serve_cmd.py` does.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.client_digest import _decision_entry, build_client_digest
from packages.orchestration.decision_queue import HumanDecision
from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
from packages.orchestration.job_apply import job_apply_landed
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    ApplyManifest,
    ExecutionConfig,
    JobPlan,
    TaskEntry,
    save_job_plan,
)

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
            raise OSError("boom")
        return real_list_decisions(job, events)

    monkeypatch.setattr(client_digest_mod, "list_decisions", fake_list_decisions)

    digest = build_client_digest(now=NOW)

    assert digest["degraded"] is True
    assert f"decisions of job {bad_job.job_id}" in digest["skipped_files"]
    [entry] = digest["decisions"]
    assert entry["decision_id"] == good_record["decision_id"]


@pytest.mark.parametrize("run_log", [
    "[1]\n",
    '{"timestamp": 1}\n{"timestamp": "2026-01-01T00:00:00"}\n',
], ids=["a-line-that-is-json-but-not-an-object", "timestamps-of-mixed-types"])
def test_a_job_whose_run_log_holds_a_malformed_record_marks_degraded_and_skips_only_that_job(
        root, run_log):
    from packages.orchestration.data_paths import run_log_dir

    bad_job = JobPlan(job_title="bad-log-job", project_id="proj-1", metadata=_job_metadata())
    enqueue_task_decision(bad_job, task_id="T001", question="Q1", options=["a"], now=NOW)
    save_job_plan(bad_job)
    log_dir = run_log_dir(bad_job.job_id, root)
    log_dir.mkdir(parents=True)
    (log_dir / "run.jsonl").write_text(run_log, encoding="utf-8")

    good_job = JobPlan(job_title="good-log-job", project_id="proj-2", metadata=_job_metadata())
    good_record = enqueue_task_decision(
        good_job, task_id="T002", question="Q2", options=["b"], now=NOW)
    save_job_plan(good_job)

    digest = build_client_digest(now=NOW)

    assert digest["degraded"] is True
    assert f"decisions of job {bad_job.job_id}" in digest["skipped_files"]
    [entry] = digest["decisions"]
    assert entry["decision_id"] == good_record["decision_id"]


def test_an_error_outside_the_named_read_errors_is_not_hidden_as_degradation(
        root, monkeypatch):
    import packages.orchestration.client_digest as client_digest_mod

    job = JobPlan(job_title="crash-job", project_id="proj-1", metadata=_job_metadata())
    save_job_plan(job)

    def fake_list_decisions(job, events):
        raise RuntimeError("a defect, not a bad record")

    monkeypatch.setattr(client_digest_mod, "list_decisions", fake_list_decisions)

    with pytest.raises(RuntimeError, match="a defect, not a bad record"):
        build_client_digest(now=NOW)


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


# ── each job's cost and evidence, each project's cost of the day (T002, DECISION F295 D7) ──

ACTUALS_STARTED_AT = "2026-01-01T11:00:00+00:00"


def _priced_actuals(*, cost, priced, unpriced) -> dict:
    """A version-2 persisted actuals record that `decode_persisted_budget_actuals` accepts."""
    return {
        "schema_version": "2.0.0", "provider_call_count": 4, "actual_call_count": 3,
        "unmeasured_call_count": 1, "total_tokens": 4200, "started_at": ACTUALS_STARTED_AT,
        "actual_sources": ["pingpong_actuals"], "measured_cost_usd": cost,
        "priced_call_count": priced, "unpriced_call_count": unpriced,
    }


def _git_folder(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    return path


def test_a_job_without_actuals_or_evidence_reads_an_absent_cost_and_null_references(root):
    job = JobPlan(job_title="bare-job", project_id="proj-1")
    save_job_plan(job)

    [entry] = build_client_digest(now=NOW)["jobs"]

    assert entry["cost"] == {"value_usd": None, "basis": "absent"}
    assert entry["evidence"] == {
        "evidence_dir": None, "run_ids": [], "postmortem_path": None,
        "run_manifest_path": None, "result_diff_path": None, "result_diff_sha256": None,
    }


@pytest.mark.parametrize(("cost", "priced", "unpriced", "expected"), [
    (1.25, 3, 0, {"value_usd": 1.25, "basis": "actual"}),
    (0.5, 1, 2, {"value_usd": 0.5, "basis": "lower_bound"}),
    (None, 0, 2, {"value_usd": None, "basis": "absent"}),
], ids=["every-call-priced", "a-call-unpriced", "never-priced"])
def test_a_jobs_persisted_actuals_give_its_cost_and_exactness_basis(
        root, cost, priced, unpriced, expected):
    job = JobPlan(job_title="priced-job", project_id="proj-1",
                  first_running_at=ACTUALS_STARTED_AT,
                  budget_actuals=_priced_actuals(cost=cost, priced=priced, unpriced=unpriced))
    save_job_plan(job)

    [entry] = build_client_digest(now=NOW)["jobs"]

    assert entry["cost"] == expected


def test_a_job_whose_actuals_are_damaged_marks_degraded_and_nulls_only_its_cost(root):
    bad_job = JobPlan(job_title="bad-actuals", project_id="proj-1",
                      budget_actuals={"schema_version": "9.9.9"})
    save_job_plan(bad_job)
    good_job = JobPlan(job_title="good-actuals", project_id="proj-2",
                       first_running_at=ACTUALS_STARTED_AT,
                       budget_actuals=_priced_actuals(cost=1.25, priced=3, unpriced=0))
    save_job_plan(good_job)

    digest = build_client_digest(now=NOW)

    costs = {entry["job_id"]: entry["cost"] for entry in digest["jobs"]}
    assert costs[str(bad_job.job_id)] is None
    assert costs[str(good_job.job_id)] == {"value_usd": 1.25, "basis": "actual"}
    assert digest["degraded"] is True
    assert f"cost of job {bad_job.job_id}" in digest["skipped_files"]


def test_a_jobs_evidence_names_the_files_that_exist_and_nulls_the_one_that_does_not(root):
    from packages.orchestration.data_paths import job_dir, job_evidence_dir

    job = JobPlan(job_title="evidence-job", project_id="proj-1",
                  run_refs=["run-a", "run-b"], postmortem_path="postmortem.json",
                  run_manifest_path="run_manifest.json", result_diff_path="result.diff",
                  result_diff_sha256="ab" * 32)
    save_job_plan(job)
    evidence_dir = job_evidence_dir(str(job.job_id))
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "postmortem.json").write_text("{}", encoding="utf-8")
    (job_dir(str(job.job_id)) / "result.diff").write_text("", encoding="utf-8")

    [entry] = build_client_digest(now=NOW)["jobs"]

    assert entry["evidence"] == {
        "evidence_dir": str(evidence_dir),
        "run_ids": ["run-a", "run-b"],
        "postmortem_path": str(evidence_dir / "postmortem.json"),
        "run_manifest_path": None,
        "result_diff_path": str(job_dir(str(job.job_id)) / "result.diff"),
        "result_diff_sha256": "ab" * 32,
    }


def test_a_projects_cost_today_sums_the_ledgers_calls_of_the_utc_day_of_read_at(
        root, tmp_path):
    from packages.orchestration.project_registry import register_project_repo
    from packages.orchestration.token_ledger import (
        COST_BASIS_PROVIDER_REPORTED,
        CallRecord,
        record_call,
    )

    project = register_project_repo("ledger-project", _git_folder(tmp_path / "ledger-project"))
    for call_id, ts_utc, cost_usd in (("today", "2026-01-01T09:00:00+00:00", 0.25),
                                      ("yesterday", "2025-12-31T23:59:59+00:00", 1.0)):
        assert record_call(CallRecord(call_id=call_id, ts_utc=ts_utc, cost_usd=cost_usd,
                                      cost_basis=COST_BASIS_PROVIDER_REPORTED),
                           project_id=project.id)

    [entry] = build_client_digest(now=NOW)["projects"]

    assert entry["cost_today"] == {
        "day": "2026-01-01", "value_usd": 0.25, "basis": "actual", "calls": 1,
    }


def test_a_project_whose_ledger_cannot_be_read_marks_degraded_and_nulls_its_cost_today(
        root, tmp_path):
    from packages.orchestration.project_registry import register_project_repo
    from packages.orchestration.token_ledger import token_ledger_path_for

    project = register_project_repo("broken-ledger", _git_folder(tmp_path / "broken-ledger"))
    ledger = token_ledger_path_for(project.id)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_bytes(b"this is not an SQLite database, and it is long enough to be read")

    digest = build_client_digest(now=NOW)

    [entry] = digest["projects"]
    assert entry["cost_today"] is None
    assert digest["degraded"] is True
    assert f"cost of the day of project {project.id}" in digest["skipped_files"]


# ── a declined job, and a job of an abandoned mission (F304 T003, DECISION F304 D5) ──


def _completed_job(title: str, project_id: str = "proj-1") -> JobPlan:
    job = JobPlan(job_title=title, project_id=project_id, state=JOB_COMPLETED)
    save_job_plan(job)
    return job


def test_a_declined_job_no_longer_waits_for_its_apply(root):
    from packages.orchestration.job_apply import decline_job_result

    kept, declined = _completed_job("kept"), _completed_job("declined")
    decline_job_result(declined, reason="not needed", source="cli", now=NOW)
    save_job_plan(declined)

    digest = build_client_digest(now=NOW)

    waits = {entry["job_id"]: entry["waits_for_apply"] for entry in digest["jobs"]}
    assert waits == {str(kept.job_id): True, str(declined.job_id): False}
    assert digest["awaiting_apply"] == [str(kept.job_id)]


def test_a_job_of_an_abandoned_mission_no_longer_waits_for_its_apply(root, tmp_path):
    from packages.orchestration.mission_state import (
        MISSION_ROLE_INITIAL,
        MISSION_STATUS_ABANDONED,
        create_mission,
        link_job_to_mission,
        set_mission_status,
    )
    from packages.orchestration.project_registry import register_project_repo

    project_id = str(register_project_repo("abandoning", _git_folder(tmp_path / "abandoning")).id)
    active, abandoned = (create_mission(project_id, goal) for goal in ("Keep this", "Drop this"))
    kept, dropped = _completed_job("kept", project_id), _completed_job("dropped", project_id)
    link_job_to_mission(project_id, active.id, str(kept.job_id), MISSION_ROLE_INITIAL)
    link_job_to_mission(project_id, abandoned.id, str(dropped.job_id), MISSION_ROLE_INITIAL)
    set_mission_status(project_id, abandoned.id, MISSION_STATUS_ABANDONED)

    digest = build_client_digest(now=NOW)

    waits = {entry["job_id"]: entry["waits_for_apply"] for entry in digest["jobs"]}
    assert waits == {str(kept.job_id): True, str(dropped.job_id): False}
    assert digest["awaiting_apply"] == [str(kept.job_id)]


# ── a completed job's approval card (F304 T005, DECISION F304 D10) ──────────


def _task(task_id: str, applied_files: list[str], *, manifest_status: str = "applied",
          **fields) -> TaskEntry:
    manifest = ApplyManifest(task_id=task_id, applied_files=applied_files, status=manifest_status)
    return TaskEntry(task_id=task_id, apply_manifest=manifest, **fields)


def test_a_completed_jobs_card_names_its_changed_files_test_command_and_tasks(root):
    job = JobPlan(job_title="carded", project_id="proj-1", state=JOB_COMPLETED,
                  execution_config=ExecutionConfig(test_command="pytest -q"),
                  tasks=[_task("T001", ["src/b.py", "README.md"], title="Write b",
                               reviewer_verdict="approve", repair_rounds_used=1,
                               test_passed=True),
                         _task("T002", ["src/b.py"], title="Fix b", reviewer_verdict="approve",
                               test_passed=False),
                         _task("T003", ["blocked.py"], manifest_status="blocked",
                               title="Not applied")])
    save_job_plan(job)

    [entry] = build_client_digest(now=NOW)["jobs"]

    assert entry["approval_card"] == {
        "changed_file_count": 2,
        "changed_files": ["README.md", "src/b.py"],
        "test_command": "pytest -q",
        "tasks": [
            {"task_id": "T001", "title": "Write b", "reviewer_verdict": "approve",
             "repair_rounds_used": 1, "test_ran": True, "test_passed": True},
            {"task_id": "T002", "title": "Fix b", "reviewer_verdict": "approve",
             "repair_rounds_used": 0, "test_ran": True, "test_passed": False},
            {"task_id": "T003", "title": "Not applied", "reviewer_verdict": None,
             "repair_rounds_used": 0, "test_ran": False, "test_passed": None},
        ],
    }


def test_a_card_counts_every_changed_file_and_names_only_the_first_by_the_limit(root):
    from packages.orchestration.client_digest import APPROVAL_CARD_FILE_LIMIT

    paths = [f"f{index:03d}.txt" for index in range(APPROVAL_CARD_FILE_LIMIT + 5)]
    job = JobPlan(job_title="many-files", project_id="proj-1", state=JOB_COMPLETED,
                  tasks=[_task("T001", list(reversed(paths)))])
    save_job_plan(job)

    [entry] = build_client_digest(now=NOW)["jobs"]

    card = entry["approval_card"]
    assert card["changed_file_count"] == APPROVAL_CARD_FILE_LIMIT + 5
    assert card["changed_files"] == paths[:APPROVAL_CARD_FILE_LIMIT]
    assert card["test_command"] is None


@pytest.mark.parametrize("state", [state for state in RunState if state != JOB_COMPLETED],
                         ids=lambda state: state.value)
def test_a_job_that_is_not_completed_carries_a_null_card(root, state):
    job = JobPlan(job_title="not-completed", project_id="proj-1", state=state,
                  tasks=[_task("T001", ["a.py"], reviewer_verdict="approve")])
    save_job_plan(job)

    [entry] = build_client_digest(now=NOW)["jobs"]

    assert entry["approval_card"] is None


# ── the digest reads and never writes (R-1144) ──────────────────────────────


def _data_root_snapshot(root: Path) -> dict[str, tuple[bytes, int]]:
    """Every file under *root* with its bytes and its modification time in nanoseconds."""
    return {str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in sorted(root.rglob("*")) if path.is_file()}


def test_reading_the_digest_changes_no_file_under_the_data_root(root, tmp_path):
    from packages.orchestration.data_paths import projects_dir
    from packages.orchestration.project_registry import RemyProject, register_project_repo
    from packages.orchestration.token_ledger import (
        COST_BASIS_PROVIDER_REPORTED,
        CallRecord,
        record_call,
    )

    project = register_project_repo("kept-project", _git_folder(tmp_path / "kept-project"))
    assert record_call(CallRecord(call_id="c1", ts_utc="2026-01-01T09:00:00+00:00", cost_usd=0.25,
                                  cost_basis=COST_BASIS_PROVIDER_REPORTED), project_id=project.id)
    # A record written before slugs existed: `list_projects` would migrate it on read.
    legacy = json.loads(RemyProject(name="Legacy Project").model_dump_json())
    legacy.pop("slug", None)
    (projects_dir() / f"{legacy['id']}.json").write_text(json.dumps(legacy), encoding="utf-8")
    job = JobPlan(job_title="kept-job", project_id=str(project.id), metadata=_job_metadata())
    enqueue_task_decision(job, task_id="T001", question="Q1", options=["a"], now=NOW)
    save_job_plan(job)
    before = _data_root_snapshot(root)

    digest = build_client_digest(now=NOW)

    assert _data_root_snapshot(root) == before
    assert sorted(entry["slug"] for entry in digest["projects"]) == ["kept-project",
                                                                      "legacy-project"]

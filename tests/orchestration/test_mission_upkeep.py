"""F301 T002, DECISION F301 D1 — the project's upkeep ledger and the findings a job leaves open."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_dir, run_dir
from packages.orchestration.mission_state import create_mission, link_job_to_mission
from packages.orchestration.mission_upkeep import (
    LINE_JOB_CLOSED,
    LINE_UPKEEP_SKIPPED,
    UPKEEP_METADATA_KEY,
    append_upkeep_line,
    finding_key,
    job_open_findings,
    open_findings,
    read_upkeep_ledger,
    record_closed_jobs,
    replaced_pairs_from_findings,
    upkeep_ledger_path,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECT = "a" * 32


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """One data root for jobs, runs, missions and projects alike."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


def _final_review(job_id: str, findings: list[dict]) -> None:
    path = job_dir(job_id) / "final_job_review.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"job_id": job_id, "verdict": "NEEDS_REPAIR", "findings": findings}),
                    encoding="utf-8")


def _run_record(run_id: str, findings: list[dict]) -> None:
    path = run_dir(run_id) / "result.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    rounds = [{"round": 1, "reviewer": {"verdict": "fail", "findings": [{"id": "OLD"}]}},
              {"round": 2, "reviewer": {"verdict": "fail", "findings": findings}}]
    path.write_text(json.dumps({"run_id": run_id, "rounds": rounds}), encoding="utf-8")


def _job(state: str, tasks: list[TaskEntry] | None = None, metadata: dict | None = None) -> JobPlan:
    job = JobPlan(job_title="fixture", state=RunState(state), tasks=list(tasks or []),
                  metadata=dict(metadata or {}))
    save_job_plan(job)
    return job


def _mission_of(*jobs: JobPlan) -> str:
    mission = create_mission(PROJECT, "Keep the importer working")
    for index, job in enumerate(jobs):
        link_job_to_mission(PROJECT, mission.id, str(job.job_id), "initial" if index == 0 else "follow_up")
    return mission.id


REVIEW_FINDING = {"id": "F-TASK-001", "severity": "repairable", "category": "task_verdict",
                  "message": "T001 did not pass review", "task_id": "T001"}
BLOCKED_FINDING = {"id": "R1", "severity": "high", "file": "importer.py", "summary": "the CSV path is unread"}


class TestTheLedgerFile:
    def test_it_lives_under_the_project_beside_its_other_records(self, tmp_path):
        assert upkeep_ledger_path("p1", tmp_path) == tmp_path / "projects" / "p1" / "upkeep_ledger.jsonl"

    def test_lines_are_appended_and_read_back_in_order(self, data_root):
        first = append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "one"})
        append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "two"})
        lines = read_upkeep_ledger(PROJECT)
        assert [line["reason"] for line in lines] == ["one", "two"]
        assert first == lines[0]
        assert {k: first[k] for k in ("version", "kind", "mission_id")} == {
            "version": 1, "kind": LINE_UPKEEP_SKIPPED, "mission_id": "m1"}
        assert first["recorded_at"]

    def test_an_unknown_kind_is_refused_and_writes_nothing(self, data_root):
        with pytest.raises(ValueError):
            append_upkeep_line(PROJECT, "m1", "job_opened", {})
        assert not upkeep_ledger_path(PROJECT).exists()

    def test_a_torn_line_and_a_foreign_line_are_skipped(self, data_root):
        append_upkeep_line(PROJECT, "m1", LINE_UPKEEP_SKIPPED, {"reason": "kept"})
        with upkeep_ledger_path(PROJECT).open("a", encoding="utf-8") as fh:
            fh.write('{"kind": "job_closed", "job_id"\n')
            fh.write('{"kind": "something_else"}\n')
            fh.write("[1, 2]\n")
        assert [line["reason"] for line in read_upkeep_ledger(PROJECT)] == ["kept"]

    def test_a_project_without_a_ledger_reads_empty(self, data_root):
        assert read_upkeep_ledger(PROJECT) == []


class TestTheOpenFindingsOfAJob:
    def test_the_final_review_and_the_blocked_tasks_last_round(self, data_root):
        blocked = TaskEntry(task_id="T002", status="blocked", run_id="run-b")
        passed = TaskEntry(task_id="T003", status="completed", run_id="run-p")
        job = _job("completed", [blocked, passed])
        _final_review(str(job.job_id), [REVIEW_FINDING])
        _run_record("run-b", [BLOCKED_FINDING])
        _run_record("run-p", [{"id": "NOT-READ", "severity": "low", "file": "", "summary": "x"}])

        found = job_open_findings(job)

        job_id = str(job.job_id)
        assert found == [
            {"key": f"{job_id}:T001:F-TASK-001", "source": "final_review", "finding_id": "F-TASK-001",
             "severity": "repairable", "file": "", "summary": "T001 did not pass review", "task_id": "T001"},
            {"key": f"{job_id}:T002:R1", "source": "review", "finding_id": "R1", "severity": "high",
             "file": "importer.py", "summary": "the CSV path is unread", "task_id": "T002"},
        ]

    def test_a_job_level_finding_is_keyed_by_job(self):
        assert finding_key("j1", "", "F-SCOPE-001") == "j1:job:F-SCOPE-001"

    def test_a_job_with_no_review_and_no_blocked_task_leaves_nothing(self, data_root):
        assert job_open_findings(_job("failed", [TaskEntry(status="failed")])) == []

    def test_an_unreadable_final_review_is_no_finding_and_no_crash(self, data_root):
        job = _job("completed")
        path = job_dir(str(job.job_id)) / "final_job_review.json"
        path.write_text("{not json", encoding="utf-8")
        assert job_open_findings(job) == []


class TestReplacedPairs:
    def test_the_hygiene_rules_replaced_file_names_its_original(self):
        findings = [
            {"finding_id": "HYG-replaced-src/importer_v2.py", "file": "src/importer_v2.py",
             "summary": "src/importer_v2.py: added beside src/importer.py, which it replaces"},
            {"finding_id": "HYG-unreferenced-src/x.py", "file": "src/x.py",
             "summary": "src/x.py: an added file that no other file references"},
            {"finding_id": "R1", "file": "src/new_y.py", "summary": "added beside src/y.py, which"},
        ]
        assert replaced_pairs_from_findings(findings) == [
            {"path": "src/importer_v2.py", "original": "src/importer.py"}]

    def test_a_summary_naming_no_original_gives_no_pair(self):
        findings = [{"finding_id": "HYG-replaced-a_v2.py", "file": "a_v2.py", "summary": "a_v2.py: odd"}]
        assert replaced_pairs_from_findings(findings) == []


class TestRecordingClosedJobs:
    def test_each_ended_job_gets_one_line_in_link_order(self, data_root):
        done = _job("completed", [TaskEntry(task_id="T001", status="completed")])
        _final_review(str(done.job_id), [REVIEW_FINDING])
        failed = _job("failed")
        running = _job("running")
        cancelled = _job("cancelled")
        mission_id = _mission_of(done, failed, running, cancelled)

        written = record_closed_jobs(PROJECT, mission_id)

        assert [(line["job_id"], line["job_state"]) for line in written] == [
            (str(done.job_id), "completed"), (str(failed.job_id), "failed"),
            (str(cancelled.job_id), "cancelled")]
        assert written[0]["open_findings"][0]["key"] == f"{done.job_id}:T001:F-TASK-001"
        assert all(line["kind"] == LINE_JOB_CLOSED and line["mission_id"] == mission_id
                   and line["resolved"] == [] and line["replaced"] == [] for line in written)
        assert read_upkeep_ledger(PROJECT) == written

    def test_a_job_is_recorded_once_and_a_running_one_when_it_ends(self, data_root):
        done = _job("completed")
        running = _job("running")
        mission_id = _mission_of(done, running)
        record_closed_jobs(PROJECT, mission_id)

        assert record_closed_jobs(PROJECT, mission_id) == []
        running.state = RunState.COMPLETED
        save_job_plan(running)
        assert [line["job_id"] for line in record_closed_jobs(PROJECT, mission_id)] == [str(running.job_id)]
        assert len(read_upkeep_ledger(PROJECT)) == 2

    def test_a_missing_job_record_is_passed_over(self, data_root):
        done = _job("completed")
        mission_id = _mission_of(done)
        (job_dir(str(done.job_id)) / "job.json").unlink()
        assert record_closed_jobs(PROJECT, mission_id) == []

    def test_a_blocked_replacement_is_recorded_as_a_pair(self, data_root):
        task = TaskEntry(task_id="T001", status="blocked", run_id="run-r")
        job = _job("failed", [task])
        _run_record("run-r", [{"id": "HYG-replaced-src/a_new.py", "severity": "high",
                               "file": "src/a_new.py",
                               "summary": "src/a_new.py: added beside src/a.py, which it replaces"}])
        [line] = record_closed_jobs(PROJECT, _mission_of(job))
        assert line["replaced"] == [{"path": "src/a_new.py", "original": "src/a.py"}]


class TestWhatResolvesAFinding:
    def _two_jobs(self, upkeep_state: str) -> tuple[str, str]:
        first = _job("completed")
        _final_review(str(first.job_id), [REVIEW_FINDING])
        key = finding_key(str(first.job_id), "T001", "F-TASK-001")
        upkeep = _job(upkeep_state, metadata={UPKEEP_METADATA_KEY: {"findings": [key]}})
        return _mission_of(first, upkeep), key

    def test_an_upkeep_job_that_completed_resolves_what_it_carried(self, data_root):
        mission_id, key = self._two_jobs("completed")
        lines = record_closed_jobs(PROJECT, mission_id)
        assert lines[1]["resolved"] == [key]
        assert open_findings(read_upkeep_ledger(PROJECT)) == []

    def test_an_upkeep_job_that_failed_resolves_nothing(self, data_root):
        mission_id, key = self._two_jobs("failed")
        lines = record_closed_jobs(PROJECT, mission_id)
        assert lines[1]["resolved"] == []
        assert [f["key"] for f in open_findings(read_upkeep_ledger(PROJECT))] == [key]

    def test_open_findings_are_oldest_first_once_each_and_scoped_to_a_mission(self, data_root):
        mission_id, key = self._two_jobs("failed")
        record_closed_jobs(PROJECT, mission_id)
        lines = read_upkeep_ledger(PROJECT)
        repeated = {**lines[0], "job_id": "other", "mission_id": "m2"}

        found = open_findings([*lines, repeated])

        assert [f["key"] for f in found] == [key]
        assert found[0]["job_id"] == lines[0]["job_id"]
        assert open_findings(lines, mission_id="m2") == []
        assert [f["key"] for f in open_findings(lines, mission_id=mission_id)] == [key]


def test_mission_continue_records_the_ended_jobs_before_the_next_one(tmp_path):
    """The way a user reaches the ledger: `remedy mission continue` on the command line."""
    data_root = tmp_path / "data"
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_root)}
    env.pop("REMEDY_PROJECT", None)
    previous = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_root)
    try:
        from packages.orchestration.config import reset_config
        from packages.orchestration.project_registry import RemyProject, save_project

        reset_config()
        project = RemyProject(name="Upkeep Test", slug="upkeep-test")
        save_project(project)
        project_id = str(project.id)
        mission = create_mission(project_id, "Keep the importer working")
        first = _job("completed")
        _final_review(str(first.job_id), [REVIEW_FINDING])
        link_job_to_mission(project_id, mission.id, str(first.job_id), "initial")
    finally:
        if previous is None:
            os.environ.pop("REMEDY_DATA_DIR", None)
        else:
            os.environ["REMEDY_DATA_DIR"] = previous
        reset_config()

    def run() -> dict:
        proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.grouped", "mission", "continue", mission.id, "Add the CSV path",
             "--project", project_id, "--json"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env)
        assert proc.returncode == 0, proc.stderr
        return json.loads(proc.stdout)

    body = run()
    run()

    lines = read_upkeep_ledger(project_id, data_root)
    assert [(line["kind"], line["job_id"]) for line in lines] == [(LINE_JOB_CLOSED, str(first.job_id))]
    assert lines[0]["open_findings"][0]["key"] == f"{first.job_id}:T001:F-TASK-001"
    assert body["role"] == "follow_up"

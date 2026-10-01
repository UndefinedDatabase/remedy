"""F292 T003 — the hunk decision recorded for the attempt a diff shows (DECISION F292 D6).

A hunk decision REPLACES the whole record for its attempt, so the cockpit's hunk controls must
start from what is recorded. `/api/jobs/<id>/hunk-decisions` and
`/api/jobs/<id>/task-runs/<tid>/hunk-decisions` answer that record, keyed exactly as
`_dispatch_approve_hunks` keys the decision it records, and
`hunk_decision_record.recorded_hunk_decision` reads it, totally.
"""
from __future__ import annotations

import difflib
import json
from datetime import datetime, timezone
from http.client import HTTPConnection

import pytest

from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.diff_view_source import DIFF_JOB_ARTIFACT_NAME, DIFF_SCOPE_JOB, build_diff_view
from packages.orchestration.hunk_decision_record import (
    HUNK_DECISIONS_METADATA_KEY,
    record_hunk_decision_from_view,
    recorded_hunk_decision,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan
from packages.orchestration.ui_server import (
    _build_hunk_decisions_json,
    _build_task_run_hunk_decisions_json,
    _resolve_evidence_dir,
)

_ORIGINAL = "".join(f"line {n}\n" for n in range(1, 41))
_EDITED = _ORIGINAL.replace("line 2\n", "line two\n").replace("line 20\n", "line twenty\n") \
    .replace("line 38\n", "line thirty-eight\n")
NOW = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)


def _diff(original: str, edited: str) -> str:
    return "".join(difflib.unified_diff(original.splitlines(True), edited.splitlines(True),
                                        fromfile="a/f.txt", tofile="b/f.txt"))


@pytest.fixture
def job(tmp_path, monkeypatch) -> JobPlan:
    """A saved job whose evidence holds a three-hunk job diff and a one-hunk diff for T001."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    from packages.orchestration.data_paths import job_evidence_index_dir

    job = JobPlan(job_title="f292 hunk decisions", user_prompt="p", tasks=[TaskEntry(title="t")])
    save_job_plan(job)
    evidence = tmp_path / "evidence"
    (evidence / "task_runs" / "T001").mkdir(parents=True)
    (evidence / DIFF_JOB_ARTIFACT_NAME).write_text(_diff(_ORIGINAL, _EDITED), encoding="utf-8")
    (evidence / "task_runs" / "T001" / "safe.diff").write_text(
        _diff(_ORIGINAL, _ORIGINAL.replace("line 5\n", "line five\n")), encoding="utf-8")
    index = job_evidence_index_dir()
    index.mkdir(parents=True, exist_ok=True)
    (index / f"{job.job_id}.json").write_text(
        json.dumps({"job_id": str(job.job_id), "evidence_dir_local": str(evidence)}), encoding="utf-8")
    return job


def _record(job: JobPlan, task_run: str | None, approved: list[str], rejected: list[dict]) -> None:
    view = build_diff_view(_resolve_evidence_dir(str(job.job_id)), task_id=task_run)
    result = record_hunk_decision_from_view(
        job, task_id=view["task_id"] if view["task_id"] is not None else DIFF_SCOPE_JOB,
        attempt=view["source"], attempt_view=view, approved=approved, rejected=rejected, now=NOW)
    assert not hasattr(result, "code"), result
    save_job_plan(job)


def _job_hunk_ids() -> list[str]:
    return [h["id"] for h in parse_unified_diff_to_view(_diff(_ORIGINAL, _EDITED))["files"][0]["hunks"]]


class TestTheJobRoute:

    def test_nothing_recorded_reads_the_attempt_key_and_no_row(self, job):
        assert _build_hunk_decisions_json(job) == {
            "attempt_key": "job:workspace.diff", "decided_at": "", "hunks": []}

    def test_a_recorded_decision_reads_every_row_in_diff_order(self, job):
        ids = _job_hunk_ids()
        assert len(ids) == 3
        _record(job, None, [ids[0]], [{"id": ids[1], "reason": "too broad"}])
        answer = _build_hunk_decisions_json(load_job_plan(str(job.job_id)))
        assert answer["attempt_key"] == "job:workspace.diff"
        assert datetime.fromisoformat(answer["decided_at"]) == NOW
        assert answer["hunks"] == [
            {"id": ids[0], "state": "approved", "reason": ""},
            {"id": ids[1], "state": "rejected", "reason": "too broad"},
            {"id": ids[2], "state": "pending", "reason": ""},
        ]

    def test_a_record_of_another_attempt_is_not_this_ones(self, job):
        job.metadata[HUNK_DECISIONS_METADATA_KEY] = {"job:older.diff": {
            "task_id": "job", "attempt": "older.diff", "decided_at": NOW.isoformat(),
            "hunks": [{"id": "abc", "state": "approved", "reason": "", "landing": "unattempted"}]}}
        assert _build_hunk_decisions_json(job)["hunks"] == []

    def test_a_job_with_no_evidence_has_no_attempt(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        bare = JobPlan(job_title="no evidence", user_prompt="p", tasks=[TaskEntry(title="t")])
        save_job_plan(bare)
        assert _build_hunk_decisions_json(bare) == {"attempt_key": "", "decided_at": "", "hunks": []}


class TestTheTaskRunRoute:

    def test_a_task_runs_decision_is_its_own_and_not_the_jobs(self, job):
        [hunk] = [h["id"] for h in build_diff_view(
            _resolve_evidence_dir(str(job.job_id)), task_id="T001")["files"][0]["hunks"]]
        _record(job, "T001", [], [{"id": hunk, "reason": "wrong file"}])
        saved = load_job_plan(str(job.job_id))
        assert _build_task_run_hunk_decisions_json(saved, "T001")["hunks"] == [
            {"id": hunk, "state": "rejected", "reason": "wrong file"}]
        assert _build_task_run_hunk_decisions_json(saved, "T001")["attempt_key"] == "T001:task_runs/T001/safe.diff"
        assert _build_hunk_decisions_json(saved)["hunks"] == []

    def test_an_unknown_task_run_has_no_attempt(self, job):
        assert _build_task_run_hunk_decisions_json(job, "T999") == {
            "attempt_key": "", "decided_at": "", "hunks": []}

    def test_both_routes_answer_over_http(self, job, tmp_path):
        from tests.ui_server.test_command_dispatch import _start_ui_server_for_job

        ids = _job_hunk_ids()
        _record(job, None, ids, [])
        port, token = _start_ui_server_for_job(str(job.job_id), tmp_path)
        for path, key in ((f"/api/jobs/{job.job_id}/hunk-decisions?token={token}", "job:workspace.diff"),
                          (f"/api/jobs/{job.job_id}/task-runs/T001/hunk-decisions?token={token}",
                           "T001:task_runs/T001/safe.diff")):
            conn = HTTPConnection("127.0.0.1", port, timeout=10)
            try:
                conn.request("GET", path)
                response = conn.getresponse()
                body = json.loads(response.read())
            finally:
                conn.close()
            assert response.status == 200, body
            assert body["attempt_key"] == key
        assert [row["state"] for row in _build_hunk_decisions_json(load_job_plan(str(job.job_id)))["hunks"]] == [
            "approved", "approved", "approved"]


class TestTheReaderIsTotal:

    @pytest.mark.parametrize("metadata", [None, "x", {}, {HUNK_DECISIONS_METADATA_KEY: "x"},
                                          {HUNK_DECISIONS_METADATA_KEY: {"job:a.diff": "x"}},
                                          {HUNK_DECISIONS_METADATA_KEY: {"job:a.diff": {"hunks": "x"}}}])
    def test_anything_unreadable_reads_as_nothing_recorded(self, metadata):
        assert recorded_hunk_decision(metadata, task_id="job", attempt="a.diff") == {
            "attempt_key": "job:a.diff", "decided_at": "", "hunks": []}

    def test_a_row_without_a_text_id_is_dropped_and_odd_fields_read_as_text(self):
        metadata = {HUNK_DECISIONS_METADATA_KEY: {"T1:x": {"decided_at": 7, "hunks": [
            "x", {"id": 3}, {"id": "h1", "state": "approved"}, {"id": "h2", "state": "rejected", "reason": 5}]}}}
        assert recorded_hunk_decision(metadata, task_id="T1", attempt="x") == {
            "attempt_key": "T1:x", "decided_at": "", "hunks": [
                {"id": "h1", "state": "approved", "reason": ""}, {"id": "h2", "state": "rejected", "reason": "5"}]}

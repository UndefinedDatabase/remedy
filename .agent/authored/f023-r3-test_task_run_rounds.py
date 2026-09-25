"""F023 T002 — the per-round facts route behind the graph's L2 run detail.

`packages/orchestration/run_rounds_view.py` reads ONE task's latest run report and keeps
only numbers, vocabulary words and timestamps (DECISION F023 D3); `ui_server.py` serves it
at `/api/jobs/<job>/task-runs/<task_id>/rounds`. The builder is tested directly for its
shape and its refusals, and the route over a REAL server on a free port, because dispatch
is the thing a direct call cannot prove.
"""
from __future__ import annotations

import json
import threading
from http.client import HTTPConnection
from types import SimpleNamespace

import pytest

from packages.orchestration.run_rounds_view import (
    REASON_NO_RUN,
    REASON_REPORT_MISSING,
    REASON_REPORT_UNREADABLE,
    REASON_UNKNOWN_TASK,
    TASK_RUN_ROUNDS_VERSION,
    build_task_run_rounds,
)
from tests.ui_server.server_start import wait_for_server_info

RUN_ID = "0123456789abcdef"

# One report as `export_pingpong_json` writes it, with the prose a served envelope must
# never carry: summaries, finding texts and a changed file's path.
REPORT = {
    "run_id": RUN_ID,
    "retries_used": 1,
    "rounds": [
        {
            "round": 1, "kind": "initial", "repair_of_round": 0,
            "input_finding_ids": [], "resolved_finding_ids": [], "remaining_finding_ids": ["F1"],
            "started_at": "2026-09-25T10:00:00+00:00", "finished_at": "2026-09-25T10:01:30.250000+00:00",
            "builder": {"summary": "SECRET builder prose", "files_changed": ["secret/path.py"],
                        "provider": "claude-cli", "duration_ms": 61000, "tokens_used": 1834, "error": ""},
            "test_passed": False, "test_summary": "SECRET test output",
            "reviewer": {"verdict": "needs_repair", "confidence": 0.8, "summary": "SECRET review",
                         "finding_count": 1,
                         "findings": [{"id": "F1", "severity": "high", "file": "secret/path.py",
                                       "summary": "SECRET finding"}],
                         "provider": "claude-cli", "duration_ms": 22000, "error": "",
                         "parse_retried": True, "parse_retry_recovered": True},
        },
        {
            "round": 2, "kind": "repair", "started_at": "2026-09-25T10:01:31+00:00",
            "finished_at": "2026-09-25T10:02:00+00:00",
            "builder": {"duration_ms": 20000, "tokens_used": 900},
            "test_passed": True,
            "reviewer": {"verdict": "pass", "duration_ms": 8000, "parse_retried": False},
        },
    ],
}

EXPECTED_ROUNDS = [
    {
        "round": 1, "kind": "initial",
        "started_at": "2026-09-25T10:00:00+00:00", "finished_at": "2026-09-25T10:01:30.250000+00:00",
        "duration_ms": 90250, "test_passed": False,
        "builder": {"duration_ms": 61000, "tokens_used": 1834},
        "reviewer": {"verdict": "needs_repair", "duration_ms": 22000, "parse_retried": True},
    },
    {
        "round": 2, "kind": "repair",
        "started_at": "2026-09-25T10:01:31+00:00", "finished_at": "2026-09-25T10:02:00+00:00",
        "duration_ms": 29000, "test_passed": True,
        "builder": {"duration_ms": 20000, "tokens_used": 900},
        "reviewer": {"verdict": "pass", "duration_ms": 8000, "parse_retried": False},
    },
]


def _job(run_id=RUN_ID):
    return SimpleNamespace(job_id="job-1", tasks=[SimpleNamespace(task_id="T001", run_id=run_id)])


def _reads(report, reason=None):
    seen = []

    def read(run_id):
        seen.append(run_id)
        return report, reason

    return read, seen


class TestTheBuilder:
    def test_the_rounds_are_the_reports_facts_and_nothing_else(self):
        read, seen = _reads(REPORT)
        env = build_task_run_rounds(_job(), "T001", read_report=read)
        assert seen == [RUN_ID]
        assert env == {
            "version": TASK_RUN_ROUNDS_VERSION, "job_id": "job-1", "task_id": "T001",
            "available": True, "reason": None, "run_id": RUN_ID, "retries_used": 1,
            "rounds": EXPECTED_ROUNDS,
        }

    def test_no_prose_from_the_report_reaches_the_envelope(self):
        read, _ = _reads(REPORT)
        text = json.dumps(build_task_run_rounds(_job(), "T001", read_report=read))
        assert "SECRET" not in text
        assert "secret/path.py" not in text
        assert "claude-cli" not in text

    def test_an_unknown_task_is_named_and_reads_nothing(self):
        read, seen = _reads(REPORT)
        env = build_task_run_rounds(_job(), "T404", read_report=read)
        assert (env["available"], env["reason"], env["rounds"], seen) == (False, REASON_UNKNOWN_TASK, [], [])

    @pytest.mark.parametrize("run_id", ["", "../../etc", "0123456789ABCDEF", "abc", None])
    def test_a_task_with_no_valid_run_id_reads_nothing(self, run_id):
        read, seen = _reads(REPORT)
        env = build_task_run_rounds(_job(run_id), "T001", read_report=read)
        assert (env["available"], env["reason"], env["run_id"], seen) == (False, REASON_NO_RUN, None, [])

    @pytest.mark.parametrize("reason", [REASON_REPORT_MISSING, REASON_REPORT_UNREADABLE])
    def test_a_report_that_cannot_be_had_is_named(self, reason):
        read, _ = _reads(None, reason)
        env = build_task_run_rounds(_job(), "T001", read_report=read)
        assert (env["available"], env["reason"], env["run_id"]) == (False, reason, RUN_ID)

    def test_malformed_values_become_none_never_an_exception(self):
        report = {"retries_used": True, "rounds": [
            {"round": -1, "kind": "Initial Round", "started_at": "yesterday",
             "finished_at": "2026-09-25T10:00:00+00:00", "test_passed": "yes",
             "builder": {"duration_ms": "61s", "tokens_used": 3.5},
             "reviewer": {"verdict": "PASS", "duration_ms": None, "parse_retried": "true"}},
            {"round": 3, "started_at": "2026-09-25T10:00:10+00:00", "finished_at": "2026-09-25T10:00:00+00:00"},
            "not a round",
        ]}
        read, _ = _reads(report)
        env = build_task_run_rounds(_job(), "T001", read_report=read)
        assert env["available"] is True
        assert env["retries_used"] is None
        assert env["rounds"] == [
            {"round": None, "kind": None, "started_at": None,
             "finished_at": "2026-09-25T10:00:00+00:00", "duration_ms": None, "test_passed": None,
             "builder": {"duration_ms": None, "tokens_used": None},
             "reviewer": {"verdict": None, "duration_ms": None, "parse_retried": False}},
            {"round": 3, "kind": None, "started_at": "2026-09-25T10:00:10+00:00",
             "finished_at": "2026-09-25T10:00:00+00:00", "duration_ms": None, "test_passed": None,
             "builder": None, "reviewer": None},
        ]


class TestTheRoute:
    """The route over a real server, reading a real report under a temporary data root."""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.data_paths import run_dir
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

        self.job = JobPlan(job_title="rounds-route", user_prompt="p",
                           tasks=[TaskEntry(task_id="T001", title="a", run_id=RUN_ID),
                                  TaskEntry(task_id="T002", title="b")])
        save_job_plan(self.job)
        self.job_id = str(self.job.job_id)
        report_dir = run_dir(RUN_ID)
        report_dir.mkdir(parents=True)
        (report_dir / "result.json").write_text(json.dumps(REPORT), encoding="utf-8")
        self.tmp_path = tmp_path

    def _start_server(self):
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(self.job_id, host="127.0.0.1", port=0, token=token,
                                open_browser=False, info_file=info_file)
            except (SystemExit, KeyboardInterrupt):
                pass

        t = threading.Thread(target=run, daemon=True)
        t.start()
        info = wait_for_server_info(info_file, t)
        return info["port"], token

    @staticmethod
    def _get(port, path):
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            return resp.status, json.loads(resp.read())
        finally:
            conn.close()

    def test_the_route_serves_the_tasks_rounds(self):
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/task-runs/T001/rounds?token={token}")
        assert status == 200, body
        assert (body["available"], body["run_id"], body["retries_used"]) == (True, RUN_ID, 1), body
        assert body["rounds"] == EXPECTED_ROUNDS

    def test_a_task_with_no_run_and_an_unknown_task_are_data_at_200(self):
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/task-runs/T002/rounds?token={token}")
        assert (status, body["available"], body["reason"]) == (200, False, REASON_NO_RUN), body
        status, body = self._get(port, f"/api/jobs/{self.job_id}/task-runs/T404/rounds?token={token}")
        assert (status, body["available"], body["reason"]) == (200, False, REASON_UNKNOWN_TASK), body

    def test_the_route_refuses_a_bad_token(self):
        port, _token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/task-runs/T001/rounds?token=wrong")
        assert (status, body["error"]) == (403, "invalid token"), body

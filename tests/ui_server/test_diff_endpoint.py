"""
Domain tests: ui_server/test_diff_endpoint.py

F037 T001, the read endpoint: the two GET routes that hand `build_diff_view`'s
envelope to a client. The server is a REAL one on a free port — the routes are
the thing under test, so a direct call to the builder would prove nothing about
dispatch.
"""

from __future__ import annotations

import json
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.core.models import Job, Task

# WHY the two diffs name DIFFERENT files: serving the job diff where the task
# run's was asked for — or the reverse — is then a red rather than a shrug.
JOB_DIFF_PATH = "packages/orchestration/job_scope_only.py"
TASK_DIFF_PATH = "packages/orchestration/task_scope_only.py"

JOB_DIFF = f"""diff --git a/{JOB_DIFF_PATH} b/{JOB_DIFF_PATH}
--- a/{JOB_DIFF_PATH}
+++ b/{JOB_DIFF_PATH}
@@ -1,2 +1,2 @@
 a line that did not move
-the old job line
+the new job line
"""

TASK_DIFF = f"""diff --git a/{TASK_DIFF_PATH} b/{TASK_DIFF_PATH}
--- a/{TASK_DIFF_PATH}
+++ b/{TASK_DIFF_PATH}
@@ -1,2 +1,2 @@
 a line that did not move
-the old task line
+the new task line
"""


def _make_job() -> Job:
    return Job(
        name="test-diff-endpoint-job",
        user_prompt="Test prompt for the diff endpoint",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


class TestDiffEndpoint:
    """The job-scope and task-run-scope diff routes, over real HTTP."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _write_evidence(self) -> Path:
        """Build an evidence dir and point the server's resolver at it.

        The index file is the FIRST branch `_resolve_evidence_dir` reads, so
        writing it keeps this test independent of the working directory — the
        fallback branch is a path relative to the CWD.
        """
        evidence = self.tmp_path / "evidence"
        (evidence / "task_runs" / "T001").mkdir(parents=True)
        (evidence / "workspace.diff").write_text(JOB_DIFF, encoding="utf-8")
        (evidence / "task_runs" / "T001" / "safe.diff").write_text(
            TASK_DIFF, encoding="utf-8")

        index_dir = self.tmp_path / "job_evidence_index"
        index_dir.mkdir(parents=True, exist_ok=True)
        (index_dir / f"{self.job_id}.json").write_text(
            json.dumps({"evidence_dir_local": str(evidence)}), encoding="utf-8")
        return evidence

    def _start_server(self):
        """Start the real server in a daemon thread, return (port, token)."""
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                info = json.loads(Path(info_file).read_text())
                return info["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    @staticmethod
    def _get(port, path):
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            raw = resp.read()
            return resp.status, json.loads(raw)
        finally:
            conn.close()

    def test_job_route_serves_the_workspace_diff(self):
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token={token}")
        assert status == 200, body
        assert body["scope"] == "job", body
        assert body["available"] is True, body
        assert body["source"] == "workspace.diff", body
        assert [f["path"] for f in body["files"]] == [JOB_DIFF_PATH], body

    def test_task_run_route_serves_only_that_runs_diff(self):
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T001/diff?token={token}")
        assert status == 200, body
        assert body["scope"] == "task_run", body
        assert body["task_id"] == "T001", body
        assert body["available"] is True, body
        # ONLY the task run's file: the job diff names a different path, so a
        # route that ignored the task id would show up right here.
        assert [f["path"] for f in body["files"]] == [TASK_DIFF_PATH], body

    def test_unknown_task_run_is_a_named_absence_at_status_200(self):
        """An unknown run is DATA, not an HTTP error.

        The status is asserted explicitly because 200-with-a-reason is the
        design decision the route carries: a 404 would make a job with no diff
        indistinguishable from a bad URL, so a later change to 404 must be red.
        """
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T404/diff?token={token}")
        assert status == 200, body
        assert body["available"] is False, body
        assert body["reason"] == "unknown_task_run", body
        assert body["task_run_ids"] == ["T001"], body

    def test_job_route_refuses_a_bad_token(self):
        self._write_evidence()
        port, _token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token=wrong")
        assert status == 403, body
        assert body["error"] == "invalid token", body

    def test_task_run_route_refuses_a_bad_token(self):
        self._write_evidence()
        port, _token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T001/diff?token=wrong")
        assert status == 403, body
        assert body["error"] == "invalid token", body

    def test_job_without_evidence_names_the_absence_at_status_200(self):
        # No `_write_evidence()` call: the index is absent and the CWD-relative
        # fallback directory does not exist for this job's id either.
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token={token}")
        assert status == 200, body
        assert body["available"] is False, body
        assert body["reason"] == "evidence_dir_unavailable", body

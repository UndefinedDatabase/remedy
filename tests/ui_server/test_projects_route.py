"""Route tests for /api/projects and /api/projects/<id>/summary (F042 T001, DECISION F042 D1).

Written by the reviewer as the acceptance of the two routes. Both reach the
server the way the other ui_server tests do — a real server on a free port, a
real token, a real HTTP request — and pin the one property a route here may
have: it composes NOTHING. Each body must equal what `projects_view` and
`project_summary` answer in this process for the same data root, so a route
that filtered, renamed or re-scoped a card would show up as an inequality.
"""

from __future__ import annotations

import json
import subprocess
import threading
from datetime import datetime, timezone
from http.client import HTTPConnection
from uuid import uuid4

import pytest

from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_cockpit import (
    find_project,
    job_project_view,
    project_summary,
    projects_view,
)
from packages.orchestration.project_registry import register_project_repo
from tests.ui_server.server_start import wait_for_server_info


def _git_folder(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    return path


def _utc_day() -> str:
    return datetime.now(timezone.utc).date().isoformat()


class TestProjectRoutes:
    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        self.alpha = register_project_repo("alpha", _git_folder(tmp_path / "alpha"))
        self.beta = register_project_repo("beta", _git_folder(tmp_path / "beta"))
        self.job = JobPlan(job_title="alpha job", project_id=str(self.alpha.id))
        save_job_plan(self.job)
        save_job_plan(JobPlan(job_title="beta job", project_id=str(self.beta.id)))
        self.tmp_path = tmp_path

    def _start_server(self):
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(str(self.job.job_id), host="127.0.0.1", port=0, token=token,
                                open_browser=False, info_file=info_file)
            except (SystemExit, KeyboardInterrupt):
                pass

        t = threading.Thread(target=run, daemon=True)
        t.start()
        info = wait_for_server_info(info_file, t)
        return info["port"], token

    def _get(self, path: str):
        port, token = self._start_server()
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", path.format(token=token))
        resp = conn.getresponse()
        status, content_type, body = resp.status, resp.getheader("Content-Type"), resp.read()
        conn.close()
        return status, content_type, json.loads(body)

    def test_the_project_list_is_a_pass_through_of_projects_view(self):
        status, content_type, body = self._get("/api/projects?token={token}")
        assert (status, content_type) == (200, "application/json")
        assert body == projects_view()
        assert [p["slug"] for p in body["projects"]] == ["alpha", "beta"]

    @pytest.mark.parametrize("selector", ["slug", "uuid"])
    def test_a_summary_is_a_pass_through_of_project_summary(self, selector):
        name = "alpha" if selector == "slug" else str(self.alpha.id)
        before = _utc_day()
        status, content_type, body = self._get(f"/api/projects/{name}/summary?token={{token}}")
        after = _utc_day()
        assert (status, content_type) == (200, "application/json")
        expected = project_summary(find_project("alpha"))
        assert body["cost_today"].pop("day") in {before, after}
        expected["cost_today"].pop("day")
        assert body == expected
        assert body["jobs"] == {"active": 1, "total": 1}
        assert body["last_result"]["job_id"] == str(self.job.job_id)

    def test_a_summary_over_http_keeps_each_project_to_its_own_jobs(self):
        status, _, body = self._get("/api/projects/beta/summary?token={token}")
        assert status == 200
        assert body["slug"] == "beta"
        assert body["last_result"]["title"] == "beta job"
        assert body["jobs"]["total"] == 1

    @pytest.mark.parametrize("name", ["gamma", str(uuid4())])
    def test_an_unknown_project_is_404(self, name):
        status, _, body = self._get(f"/api/projects/{name}/summary?token={{token}}")
        assert (status, body) == (404, {"error": "project not found"})

    @pytest.mark.parametrize("path", ["/api/projects", "/api/projects/alpha/summary"])
    def test_both_routes_refuse_a_request_without_the_token(self, path):
        status, _, body = self._get(path)
        assert (status, body) == (403, {"error": "invalid token"})

    def test_a_jobs_project_is_a_pass_through_of_job_project_view(self):
        status, content_type, body = self._get(f"/api/jobs/{self.job.job_id}/project?token={{token}}")
        assert (status, content_type) == (200, "application/json")
        assert body == job_project_view(self.job)
        assert (body["scope"], body["project"]["slug"]) == ("project", "alpha")


class TestDashboardProjectLine:
    """DECISION F042 D5: the dashboard's project section reads the job's own `project_id` and
    counts `scoped_jobs` over it, so the right panel's "Project: N jobs" line and the project's
    card in the home grid count the same jobs."""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        self.alpha = register_project_repo("alpha", _git_folder(tmp_path / "alpha"))
        self.beta = register_project_repo("beta", _git_folder(tmp_path / "beta"))
        self.jobs = [JobPlan(job_title=f"alpha job {n}", project_id=str(self.alpha.id)) for n in range(2)]
        for job in self.jobs:
            save_job_plan(job)
        save_job_plan(JobPlan(job_title="beta job", project_id=str(self.beta.id)))

    def test_a_job_scoped_by_its_own_field_gets_its_projects_line(self):
        from packages.orchestration.ui_server import _build_project_summary_section

        section = _build_project_summary_section(self.jobs[0])
        assert section is not None
        assert section["project_id"] == str(self.alpha.id)
        assert section["job_count"] == project_summary(self.alpha)["jobs"]["total"] == 2

    def test_the_jobs_own_project_outranks_the_legacy_key(self):
        """R-1111: a job whose own field names alpha while its legacy metadata still names beta
        is alpha's, the order DECISION F042 D5 (2) states."""
        from packages.orchestration.ui_server import _build_project_summary_section

        job = JobPlan(job_title="moved job", project_id=str(self.alpha.id), metadata={"project_id": str(self.beta.id)})
        save_job_plan(job)
        section = _build_project_summary_section(job)
        assert section is not None
        assert section["project_id"] == str(self.alpha.id)
        assert section["job_count"] == project_summary(self.alpha)["jobs"]["total"] == 3

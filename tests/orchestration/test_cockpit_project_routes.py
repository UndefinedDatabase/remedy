"""Tests for `packages.orchestration.cockpit_project_routes` (F305 T001, DECISION F305 D2).

The door is read twice: called directly, for every shape a path below a project can take, and
through a real server on a free port with a real token, where each body must equal what
`mission_cockpit` answers in this process for the same data root.
"""

from __future__ import annotations

import json
import subprocess
import threading
from http.client import HTTPConnection

import pytest

from packages.orchestration.cockpit_project_routes import project_route_answer
from packages.orchestration.mission_cockpit import mission_orders_view, project_missions_view
from packages.orchestration.mission_state import MissionOrder
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_cockpit import find_project, project_summary
from packages.orchestration.project_registry import register_project_repo
from packages.orchestration.repo_mission import accept_order, link_order_job
from tests.ui_server.server_start import wait_for_server_info

NOT_FOUND = (404, {"error": "not found"})


def _repo(path):
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "-c", "user.email=a@b", "-c", "user.name=n",
                    "commit", "-q", "--allow-empty", "-m", "x"], check=True)
    return path


@pytest.fixture
def alpha(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("REMEDY_PROJECT", raising=False)
    project = register_project_repo("alpha", _repo(tmp_path / "alpha"))
    mission, batch = accept_order(project, project.canonical_repo_path, MissionOrder(text="one order"))
    job = JobPlan(job_title="alpha job", project_id=str(project.id), repo_path=project.canonical_repo_path)
    save_job_plan(job)
    link_order_job(str(project.id), mission.id, batch.order_id, str(job.job_id))
    return {"project": project, "mission_id": mission.id, "job": job, "tmp_path": tmp_path}


def _parts(path: str) -> list[str]:
    return path.split("/")


def test_the_summary_keeps_its_answer(alpha):
    status, body = project_route_answer(_parts("/api/projects/alpha/summary"))
    assert status == 200
    assert body["project_id"] == project_summary(find_project("alpha"))["project_id"]


def test_the_missions_route_answers_the_missions_view(alpha):
    assert project_route_answer(_parts("/api/projects/alpha/missions")) == (
        200, project_missions_view(alpha["project"]))


def test_the_orders_route_answers_the_orders_view(alpha):
    path = f"/api/projects/alpha/missions/{alpha['mission_id']}/orders"
    assert project_route_answer(_parts(path)) == mission_orders_view(alpha["project"], alpha["mission_id"])


@pytest.mark.parametrize("path", [
    "/api/projects/gamma/summary", "/api/projects/gamma/missions",
    "/api/projects/gamma/missions/any/orders"])
def test_an_unknown_project_is_404(alpha, path):
    assert project_route_answer(_parts(path)) == (404, {"error": "project not found"})


@pytest.mark.parametrize("path", [
    "/api/projects/alpha/other", "/api/projects/alpha/missions/any",
    "/api/projects/alpha/missions/any/jobs", "/api/projects/alpha/summary/more",
    "/api/projects/alpha/missions/any/orders/more"])
def test_a_path_that_names_no_route_is_the_handlers_own_404(alpha, path):
    assert project_route_answer(_parts(path)) == NOT_FOUND


def _start_server(alpha):
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(alpha["tmp_path"] / "server_info.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(str(alpha["job"].job_id), host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return wait_for_server_info(info_file, thread)["port"], token


def test_the_server_hands_every_path_below_a_project_to_the_door(alpha):
    port, token = _start_server(alpha)
    paths = {
        "/api/projects/alpha/missions": (200, project_missions_view(alpha["project"])),
        f"/api/projects/alpha/missions/{alpha['mission_id']}/orders":
            mission_orders_view(alpha["project"], alpha["mission_id"]),
        "/api/projects/alpha/missions/nope/orders": (404, {"error": "mission not found"}),
        "/api/projects/alpha/nothing": NOT_FOUND,
        "/api/projects/alpha": NOT_FOUND,
    }
    for path, expected in paths.items():
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        conn.request("GET", f"{path}?token={token}")
        response = conn.getresponse()
        got = (response.status, json.loads(response.read()))
        conn.close()
        assert got == expected, path
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    conn.request("GET", "/api/projects/alpha/missions")
    response = conn.getresponse()
    assert (response.status, json.loads(response.read())) == (403, {"error": "invalid token"})
    conn.close()

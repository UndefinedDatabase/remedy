"""F042 T002, DECISION F042 D2 — the client's project seam agrees with the server's envelopes.

Written by the reviewer. `apps/ui/src/api/projectScope.test.ts` pins the client's rules with
envelopes typed by hand; this file closes the other side: every interface the client declares
for a project envelope carries EXACTLY the keys `packages/orchestration/project_cockpit.py`
emits, read from the dicts the module really answers rather than from a list written here, so a
key added on either side without the other fails in the suite that runs in CI.
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.project_cockpit import (
    PROJECT_COCKPIT_VERSION,
    job_project_view,
    project_summary,
    projects_view,
)
from packages.orchestration.project_registry import register_project_repo

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENT = REPO_ROOT / "apps" / "ui" / "src" / "api" / "projectScope.ts"
SERVER = REPO_ROOT / "packages" / "orchestration" / "ui_server.py"


def _interfaces() -> dict[str, set[str]]:
    source = CLIENT.read_text(encoding="utf-8")
    found = {}
    for name, body in re.findall(r"^export interface (\w+) \{\n(.*?)^\}", source, re.MULTILINE | re.DOTALL):
        found[name] = set(re.findall(r"^\s+(?:readonly\s+)?(\w+)\??:", body, re.MULTILINE))
    return found


@pytest.fixture
def envelopes(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("REMEDY_PROJECT", "alpha")
    folder = tmp_path / "alpha"
    folder.mkdir()
    subprocess.run(["git", "init", "-q", str(folder)], check=True)
    alpha = register_project_repo("alpha", folder)
    job = JobPlan(job_title="alpha job", project_id=str(alpha.id))
    save_job_plan(job)
    view = projects_view(str(tmp_path))
    card = project_summary(alpha, now=datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc))
    return {"view": view, "card": card, "job": job_project_view(job)}


def test_every_project_interface_carries_exactly_the_servers_keys(envelopes):
    interfaces = _interfaces()
    view, card, job = envelopes["view"], envelopes["card"], envelopes["job"]
    assert view["default_project"] is not None and card["last_result"] is not None
    expected = {
        "ProjectsView": set(view),
        "ProjectEntry": set(view["projects"][0]),
        "DefaultProject": set(view["default_project"]),
        "ProjectSummary": set(card),
        "ProjectJobCounts": set(card["jobs"]),
        "ProjectLastResult": set(card["last_result"]),
        "ProjectCostToday": set(card["cost_today"]),
        "ProjectDecisions": set(card["decisions"]),
        "JobProject": set(job),
    }
    assert {name: interfaces.get(name) for name in expected} == expected


def test_the_client_understands_the_servers_version():
    source = CLIENT.read_text(encoding="utf-8")
    assert f"export const PROJECT_COCKPIT_VERSION = {PROJECT_COCKPIT_VERSION};" in source


def test_the_client_paths_name_the_routes_the_server_dispatches():
    source = CLIENT.read_text(encoding="utf-8")
    server = SERVER.read_text(encoding="utf-8")
    assert "/api/projects?token=" in source and 'if path == "/api/projects":' in server
    assert "/summary?token=" in source and 'parts[2] == "projects"' in server
    assert "/project?token=" in source and '"project": _build_job_project_json,' in server


def test_the_seam_is_pure():
    """The code, with its comments removed, touches no wire, clock, storage or page."""
    source = CLIENT.read_text(encoding="utf-8")
    code = re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL))
    assert "export function decodeProjectsView" in code
    for forbidden in ("fetch(", "Date", "localStorage", "sessionStorage", "window.", "document."):
        assert forbidden not in code, forbidden

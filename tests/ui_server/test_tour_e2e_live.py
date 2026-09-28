"""F036 R6 S4 — one real job's guided tour, proved end to end through its file,
the browser's route and the command line (DECISION F036 D7 (3)).

Structured like `tests/orchestration/test_resume_kill.py`'s subprocess run: a
fixture job's own copy of the real multi-cycle pipeline (`run_cycles` +
`default_task_step`) runs to `all_green` in a CHILD PROCESS, so the tour this
test reads is the one a real `remedy job run` leaves behind, not a shortcut
built in the test process. The switch stays off throughout (constraint 7):
the child's environment never carries `REMEDY_TOUR_MODEL_WRITTEN`, so the
stored tour is the mechanical one, generator `fallback`, and no test here
reaches a live model.

Three readers of the SAME stored tour, each through its own real door:
  1. the file        — `stored_tour_versions` / `load_result_tour` in this
                        process, against the child's own data root;
  2. the browser      — a real UI server on port 0, `GET /api/jobs/<id>/tour`,
                        exactly `tour_view(job)` (DECISION F036 D5);
  3. the command line — `python3 -m apps.cli.main job show <id> --tour` in a
                        second subprocess, its JSON `tour` section and its
                        stderr's `render_tour_lines` both read back the same
                        tour.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.result_tour import (
    TOUR_GENERATOR_FALLBACK,
    anchor_problem,
    collect_tour_context,
    load_result_tour,
    render_tour_lines,
    stored_tour_versions,
    tour_problems,
    tour_view,
)
from tests.ui_server.server_start import wait_for_server_info

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# The child: a real two-task job, run to `all_green` through `run_cycles` with
# a deterministic fake provider — the same `ProviderCall` shape
# `long_run_executor.default_task_step` expects (`Callable[[TaskExecutionContext],
# BuilderOutput]`), never the ping-pong Builder/Reviewer protocol's own fake.
# ---------------------------------------------------------------------------

CHILD_SOURCE = '''
"""Fixture: a file-based two-task job runs to all_green through run_cycles with
a deterministic fake provider, leaving real evidence (report.md, tour.json)
behind under REMEDY_DATA_DIR. Prints the job id and the terminal status."""
import json

from packages.core.models import RunState
from packages.orchestration.builder_models import BuilderOutput, TaskExecutionContext
from packages.orchestration.long_run_executor import CycleLimits, default_task_step, run_cycles
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan


class FakeProvider:
    """A deterministic builder that always returns verifiable output."""

    def __init__(self):
        self.calls = 0

    def __call__(self, context: TaskExecutionContext) -> BuilderOutput:
        self.calls += 1
        return BuilderOutput(
            summary=f"did {context.task_description}",
            proposed_changes=[f"write docs for {context.task_description}"],
        )


job = JobPlan(
    job_title="f036-tour-e2e-job",
    user_prompt="build two things end to end",
    tasks=[TaskEntry(title="t1", inputs={"task_type": "documentation"}),
           TaskEntry(title="t2", inputs={"task_type": "documentation"})],
    state=RunState.PLANNED,
)
save_job_plan(job)

result = run_cycles(job, CycleLimits(max_cycles=5), FakeProvider(), task_step=default_task_step)
print(json.dumps({"terminal_status": result.terminal_status, "job_id": job.job_id}))
'''


def _child_env(data_dir: Path) -> dict[str, str]:
    """The subprocess environment: a scratch data root, and NEVER the switch
    (constraint 7 — no test may reach a live model)."""
    env = dict(os.environ)
    env.pop("REMEDY_TOUR_MODEL_WRITTEN", None)
    env["REMEDY_DATA_DIR"] = str(data_dir)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONUNBUFFERED"] = "1"
    return env


def _run_the_fixture_job(data_dir: Path, tmp_path: Path) -> str:
    """Run the child to `all_green`, return its job id."""
    script = tmp_path / "tour_e2e_fixture_run.py"
    script.write_text(CHILD_SOURCE, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(REPO_ROOT), env=_child_env(data_dir),
        capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, f"fixture run failed:\n{proc.stdout}\n{proc.stderr}"
    summary = json.loads(proc.stdout.strip().splitlines()[-1])
    assert summary["terminal_status"] == "all_green", summary
    return summary["job_id"]


# ---------------------------------------------------------------------------
# Helpers new to THIS file — a real server on port 0, own copy per the
# `tests/ui_server/*_e2e_live.py` header convention (each file keeps its own
# rather than importing a sibling test file's).
# ---------------------------------------------------------------------------


def _start_server(job_id: str, tmp_path: Path) -> tuple[int, str]:
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / f"server_info_{secrets.token_hex(4)}.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    t = threading.Thread(target=run, daemon=True)
    t.start()
    info = wait_for_server_info(info_file, t)
    return info["port"], token


def _get_tour(port: int, token: str, job_id: str) -> tuple[int, dict]:
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/tour?token={token}")
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# The proof
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestTourE2ELive:
    def test_one_real_jobs_tour_through_its_file_the_route_and_the_command_line(
            self, tmp_path, monkeypatch):
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_id = _run_the_fixture_job(data_dir, tmp_path)

        # --- 1. THE FILE: read back in this process, against the child's own
        #        data root (DECISION F036 D7 (3)) -------------------------------
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        from packages.orchestration.config import reset_config
        reset_config()

        assert stored_tour_versions(job_id) == [1]

        version, tour = load_result_tour(job_id)
        assert version == 1
        assert tour["generator"] == TOUR_GENERATOR_FALLBACK
        assert tour_problems(tour) == []
        assert tour["stops"], "the fallback tour must hold at least one stop"
        assert tour["stops"][0]["anchor"] == {"kind": "evidence", "ref": "report.md"}

        from packages.orchestration.pingpong_job import require_job_plan

        job = require_job_plan(job_id)
        context = collect_tour_context(job)
        for stop in tour["stops"]:
            assert anchor_problem(stop["anchor"], context) == "", stop

        expected_view = tour_view(job)
        assert expected_view == {
            "stored": True, "version": 1, "tour": tour, "error": "",
        }

        # --- 2. THE BROWSER: a real server on port 0, as test_tour_route.py
        #        starts it, serves exactly tour_view(job) at the tour route -------
        port, token = _start_server(job_id, tmp_path)
        status, body = _get_tour(port, token, job_id)
        assert status == 200
        assert body == expected_view
        assert body["stored"] is True
        assert body["version"] == 1

        # --- 3. THE COMMAND LINE: `job show --tour` in its own subprocess -------
        cli = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "show", job_id, "--tour"],
            cwd=str(REPO_ROOT), env=_child_env(data_dir),
            capture_output=True, text=True, timeout=60,
        )
        assert cli.returncode == 0, f"job show --tour failed:\n{cli.stdout}\n{cli.stderr}"

        cli_data = json.loads(cli.stdout)
        tour_section = cli_data["sections"]["tour"]
        assert tour_section["ok"] is True
        assert tour_section["data"]["stored"] is True
        assert tour_section["data"]["version"] == 1
        assert tour_section["data"]["tour"] == tour

        expected_lines = render_tour_lines(tour)
        stderr_lines = cli.stderr.splitlines()
        assert stderr_lines[-len(expected_lines):] == expected_lines

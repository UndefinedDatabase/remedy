"""Tests for the golden-path CLI (F147 T001–T003)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


def _env(tmp_path):
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


def _git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(
        ["git", "init", "-q", str(repo)],
        check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _init_project(repo, env):
    return subprocess.run(
        [*_CLI, "init"],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )


def _run_do(repo, env, mission, extra_args=None):
    return subprocess.run(
        [*_CLI, "do", mission, *(extra_args or [])],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )


# ── T001: remedy do "<mission>" ────────────────────────────────────────


class TestDoMission:
    def test_do_mission_creates_planned_job(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme")
        assert result.returncode == 0, result.stderr

        out = result.stdout
        assert "Job:" in out
        assert "State: planned" in out
        assert "analyze_requirements" in out
        assert "Next: remedy status" in out
        assert "plan: deterministic skeleton (LLM Flight Plan lands with F013/F014)" in out

    def test_do_mission_json(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--json"])
        assert result.returncode == 0, result.stderr

        data = json.loads(result.stdout)
        assert data["state"] == "planned"
        assert data["mission"] == "build a readme"
        assert len(data["tasks"]) == 3
        assert data["next_command"] == "remedy status"
        assert "plan_label" in data

    def test_missing_project_exits_3(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = _run_do(repo, env, "build a readme")
        assert result.returncode == 3
        assert "No project registered for this repo. Run: remedy init" in result.stderr

    def test_empty_mission_exits_2(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "")
        assert result.returncode == 2

    def test_whitespace_mission_exits_2(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "   ")
        assert result.returncode == 2

    def test_label_exact(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "ship it")
        assert result.returncode == 0
        assert "plan: deterministic skeleton (LLM Flight Plan lands with F013/F014)" in result.stdout

    def test_old_job_json_without_mission_loads(self, tmp_path):
        """Pre-F147 job JSON without mission field must still load."""
        from packages.core.models import Job

        old_json = json.dumps({
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "legacy job",
            "user_prompt": "do something",
            "created_at": "2026-01-01T00:00:00Z",
            "tasks": [],
            "state": "pending",
            "artifacts": [],
            "budget": {},
            "metadata": {},
        })
        job = Job.model_validate_json(old_json)
        assert job.mission is None
        assert job.name == "legacy job"

    def test_long_mission_stored_fully(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        long_mission = "x" * 500
        result = _run_do(repo, env, long_mission, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["mission"] == long_mission


# ── T002: remedy status ───────────────────────────────────────────────


def _run_status(repo, env, extra_args=None):
    return subprocess.run(
        [*_CLI, "status", *(extra_args or [])],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )


class TestStatus:
    def test_status_no_project_exits_0(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "No project registered" in result.stderr

    def test_status_empty_project_exits_0(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "No jobs." in result.stdout

    def test_status_shows_planned_job(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "planned" in result.stdout

    def test_status_json_schema(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert "jobs" in data
        assert "decisions_open" in data
        assert isinstance(data["decisions_open"], int)
        assert "runtime" in data
        assert "stops_pending" in data
        assert isinstance(data["stops_pending"], int)
        assert data["project"] is not None

    def test_status_json_no_project(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert data["project"] is None
        assert data["jobs"] == {}

    def test_status_shows_multiple_jobs(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "first task")
        _run_do(repo, env, "second task")

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        planned_jobs = data["jobs"].get("planned", [])
        assert len(planned_jobs) >= 2

    def test_status_corrupt_file_handled(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        jobs_dir = tmp_path / "data" / "jobs"
        jobs_dir.mkdir(parents=True, exist_ok=True)
        (jobs_dir / "bad.json").write_text("{corrupt")

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert data.get("degraded") is True
        assert len(data.get("skipped_files", [])) >= 1

    def test_status_text_sections(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "Decisions:" in result.stdout
        assert "Runtime:" in result.stdout
        assert "Stops:" in result.stdout

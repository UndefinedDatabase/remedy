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

    def test_explicit_do_run_skips_golden_path(self, tmp_path):
        """Explicit `remedy do run "goal"` → legacy path, not golden path."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = subprocess.run(
            [*_CLI, "do", "run", "build a readme"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        # Legacy path runs (may fail due to no builder, but NOT golden-path output)
        assert "Next: remedy status" not in result.stdout

    def test_budget_flag_skips_golden_path(self, tmp_path):
        """Mission + --max-total-tokens → legacy path (budgets honored)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--max-total-tokens", "500"])
        # Legacy path — golden-path marker absent
        assert "Next: remedy status" not in result.stdout

    def test_bare_mission_with_json_uses_golden_path(self, tmp_path):
        """Bare mission + --json → golden path (--json allowed)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["next_command"] == "remedy status"

    def test_explicit_default_flag_skips_golden_path(self, tmp_path):
        """Mission + --autonomy-level 1 (default value) → legacy path."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--autonomy-level", "1"])
        assert "Next: remedy status" not in result.stdout

    def test_bare_mission_with_repo_uses_golden_path(self, tmp_path):
        """Bare mission + --repo . → golden path (--repo allowed)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--repo", str(repo), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["next_command"] == "remedy status"


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

    def test_status_corrupt_runtime_state(self, tmp_path):
        """Corrupt runtime.json → runtime 'unknown' + warning, exit 0."""
        import hashlib

        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        digest = hashlib.sha256(str(repo.resolve()).encode()).hexdigest()[:16]
        rt_dir = tmp_path / "data" / "projects" / digest
        rt_dir.mkdir(parents=True, exist_ok=True)
        (rt_dir / "runtime.json").write_text("{corrupt")

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["runtime"] == "unknown"
        assert "runtime_warning" in data

        text = _run_status(repo, env)
        assert text.returncode == 0
        assert "Warning:" in text.stdout

    def test_status_text_sections(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "Jobs (all projects):" in result.stdout
        assert "Decisions:" in result.stdout
        assert "Runtime:" in result.stdout
        assert "Stops:" in result.stdout
        assert "Next:" in result.stdout

    def test_status_json_scope(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["scope"] == "all projects"

    def test_status_stop_pending(self, tmp_path):
        """F011 stop request via CLI → stops_pending counts it."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do_result = _run_do(repo, env, "build a readme", ["--json"])
        assert do_result.returncode == 0
        job_id = json.loads(do_result.stdout)["job_id"]

        stop = subprocess.run(
            [*_CLI, "job", "stop", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 0, stop.stderr

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["stops_pending"] >= 1

    def test_status_decisions_with_events(self, tmp_path):
        """Event-derived decisions counted when events exist."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do_result = _run_do(repo, env, "build a readme", ["--json"])
        assert do_result.returncode == 0
        job_id = json.loads(do_result.stdout)["job_id"]

        runs_dir = tmp_path / "data" / "runs" / job_id
        runs_dir.mkdir(parents=True, exist_ok=True)
        event = json.dumps({
            "event": "test_run_completed",
            "timestamp": "2026-01-01T00:00:00Z",
            "metadata": {
                "status": "failed",
                "command": "pytest",
                "test_run_id": "tr-001",
            },
        })
        (runs_dir / "run.jsonl").write_text(event + "\n")

        result = _run_status(repo, env, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["decisions_open"] >= 1

    def test_job_stop_golden_path_job(self, tmp_path):
        """remedy job stop <golden-path id> exits 0 and records request."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do_result = _run_do(repo, env, "build a readme", ["--json"])
        assert do_result.returncode == 0
        job_id = json.loads(do_result.stdout)["job_id"]

        stop = subprocess.run(
            [*_CLI, "job", "stop", job_id, "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 0, stop.stderr
        data = json.loads(stop.stdout)
        assert data["ok"] is True
        assert data["job_id"] == job_id
        assert "stop" in data

    def test_job_stop_unknown_id(self, tmp_path):
        """remedy job stop <unknown> exits 3."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        stop = subprocess.run(
            [*_CLI, "job", "stop", "00000000-0000-0000-0000-000000000099"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 3


# ── T003: help pinning + golden-path smoke ────────────────────────────


class TestHelpPinning:
    def test_do_status_decision_pinned_first(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = subprocess.run(
            [*_CLI, "--help"],
            capture_output=True, text=True, timeout=10,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0
        out = result.stdout
        do_pos = out.index("do ")
        status_pos = out.index("status ")
        decision_pos = out.index("decision ")
        init_pos = out.index("init ")
        assert do_pos < status_pos < decision_pos < init_pos


class TestGoldenPathSmoke:
    def test_init_do_status_stop_flow(self, tmp_path):
        """Golden path: init → do → status → stop → status shows stop."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        init = _init_project(repo, env)
        assert init.returncode == 0, init.stderr

        do = _run_do(repo, env, "build a readme", ["--json"])
        assert do.returncode == 0, do.stderr
        do_data = json.loads(do.stdout)
        job_id = do_data["job_id"]
        short_id = do_data["short_id"]

        status = _run_status(repo, env, ["--json"])
        assert status.returncode == 0, status.stderr
        status_data = json.loads(status.stdout)

        planned_ids = [j["job_id"] for j in status_data["jobs"].get("planned", [])]
        assert job_id in planned_ids

        text_status = _run_status(repo, env)
        assert text_status.returncode == 0
        assert short_id in text_status.stdout
        assert "planned" in text_status.stdout

        stop = subprocess.run(
            [*_CLI, "job", "stop", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 0, stop.stderr

        status2 = _run_status(repo, env, ["--json"])
        assert status2.returncode == 0
        status2_data = json.loads(status2.stdout)
        assert status2_data["stops_pending"] >= 1

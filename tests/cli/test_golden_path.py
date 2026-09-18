"""Tests for the golden-path CLI (F147 T001–T003)."""

from __future__ import annotations

import json
import os
import re
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
    """`remedy do` on the fake builder and reviewer, with no model call and no cockpit.

    F268: a bare `do "<order>"` now RUNS the job it plans, so every call names
    the fake providers; without them the run would reach the role config's
    real provider.
    """
    args = list(extra_args or [])
    if "--no-llm" not in args:
        args.append("--no-llm")
    args += ["--builder-provider", "fake", "--reviewer-provider", "fake", "--no-ui"]
    return subprocess.run(
        [*_CLI, "do", mission, *args],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )


def _shape_order(repo, order, **kwargs):
    """The shape step's job planning, called directly (F268 moved it out of `_cmd_do_mission`)."""
    from packages.orchestration.do_sequence import plan_order_job
    from packages.orchestration.project_registry import resolve_project

    return plan_order_job(order, project=resolve_project(repo), repo_path=str(repo), **kwargs)


def _planned_job_id(tmp_path, monkeypatch, repo, order="build a readme"):
    """A job planned by the golden-path planning and NOT run: the only kind `job stop` accepts.

    F268 made bare `do` run its job to completion, and `job stop` refuses a
    completed job, so the stop tests plan their job through the moved planning.
    """
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return str(_shape_order(repo, order, no_llm=True).job.job_id)


def _job_record(tmp_path, job_id):
    return json.loads((tmp_path / "data" / "jobs" / job_id / "job.json").read_text())


# ── T001: remedy do "<mission>" ────────────────────────────────────────


class TestDoMission:
    def test_do_mission_creates_and_runs_one_job(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--no-llm"])
        assert result.returncode == 0, result.stderr

        out = result.stdout
        assert re.search(r"\[done\] shape: one job [0-9a-f]{16} linked to mission", out)
        assert "3 task(s)" in out
        assert "to completed" in out
        assert "intake: heuristic (forced by --no-llm)" in out
        assert "plan: deterministic skeleton" in out
        assert "[stopped] apply: stopped before apply" in out
        assert "Next: remedy job apply " in out

    def test_do_mission_json(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--no-llm", "--json"])
        assert result.returncode == 0, result.stderr

        data = json.loads(result.stdout)
        [job_id] = data["job_ids"]
        job = _job_record(tmp_path, job_id)
        assert job["status"] == "completed"
        assert job["mission"] == "build a readme"
        assert job["intake"]["goal"]
        assert len(job["tasks"]) == 3
        shape = next(s for s in data["steps"] if s["name"] == "shape")
        assert "intake: heuristic (forced by --no-llm)" in shape["detail"]
        assert "plan: deterministic skeleton" in shape["detail"]
        assert data["stopped_before_apply"] is True
        assert data["contract"] is None

    def test_unregistered_repo_is_registered_by_do(self, tmp_path):
        """F268 D2: `do` registers an unregistered repository instead of exiting 3."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = _run_do(repo, env, "build a readme", ["--json"])
        assert result.returncode == 0, result.stderr
        init = json.loads(result.stdout)["steps"][0]
        assert init["name"] == "init"
        assert init["detail"].startswith(f"registered {repo.resolve()} as project ")

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
        assert "plan: deterministic skeleton" in result.stdout

    def test_old_job_json_without_mission_loads(self, tmp_path):
        """Pre-F147 job JSON without mission field must still load."""
        from packages.orchestration.pingpong_job import _import_job

        old_json = json.dumps({
            "job_id": "0000000000000001",
            "job_title": "legacy job",
            "user_prompt": "do something",
            "created_at": "2026-01-01T00:00:00Z",
            "tasks": [],
            "state": "pending",
            "artifacts": [],
            "budget": {},
            "metadata": {},
        })
        job = _import_job(json.loads(old_json))
        assert job.mission == ""
        assert job.job_title == "legacy job"

    def test_long_mission_stored_fully(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        long_mission = "x" * 500
        result = _run_do(repo, env, long_mission, ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert _job_record(tmp_path, data["job_ids"][0])["mission"] == long_mission

    def test_no_llm_flag_uses_golden_path(self, tmp_path):
        """--no-llm is allowed on the golden path (forces heuristic intake)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--no-llm", "--json"])
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        shape = next(s for s in data["steps"] if s["name"] == "shape")
        assert "intake: heuristic (forced by --no-llm)" in shape["detail"]
        assert data["steps"][0]["name"] == "init"

    def test_intake_persisted_on_job(self, tmp_path):
        """Intake dict is persisted on the saved job."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "fix src/main.py and update README.md", ["--json"])
        assert result.returncode == 0, result.stderr
        job_id = json.loads(result.stdout)["job_ids"][0]

        show = subprocess.run(
            [*_CLI, "job", "show", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert show.returncode == 0, show.stderr
        job_data = json.loads(show.stdout)
        assert job_data["intake"] is not None
        assert job_data["intake"]["schema_v"] == "ji1"
        assert job_data["intake"]["goal"]
        assert "src/main.py" in job_data["intake"]["context_refs"]
        assert "--- Intake ---" in show.stderr
        assert "Goal:" in show.stderr
        assert "src/main.py" in show.stderr

    def test_job_show_silent_for_legacy_job(self, tmp_path, monkeypatch):
        """Legacy job without intake → no Intake block."""
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan

        env = _env(tmp_path)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        legacy = JobPlan(
            job_title="legacy",
            user_prompt="do something",
            state="pending",
        )
        save_job_plan(legacy)
        repo = _git_repo(tmp_path)

        show = subprocess.run(
            [*_CLI, "job", "show", str(legacy.job_id)],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert show.returncode == 0
        assert "--- Intake ---" not in show.stderr

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
        # Legacy path runs (may fail due to no builder, but NOT the do sequence's output)
        assert "] shape:" not in result.stdout

    def test_budget_flag_skips_golden_path(self, tmp_path):
        """Mission + --max-total-tokens → legacy path (budgets honored)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--max-total-tokens", "500"])
        # Legacy path — the do sequence's marker absent
        assert "] shape:" not in result.stdout

    def test_bare_mission_with_json_uses_golden_path(self, tmp_path):
        """Bare mission + --json → golden path (--json allowed)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["steps"][0]["name"] == "init"
        assert data["stopped_before_apply"] is True

    def test_explicit_default_flag_skips_golden_path(self, tmp_path):
        """Mission + --autonomy-level 1 (default value) → legacy path."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--autonomy-level", "1"])
        assert "] shape:" not in result.stdout

    def test_bare_mission_with_repo_uses_golden_path(self, tmp_path):
        """Bare mission + --repo . → golden path (--repo allowed)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        result = _run_do(repo, env, "build a readme", ["--repo", str(repo), "--json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["steps"][0]["name"] == "init"
        assert data["stopped_before_apply"] is True


# ── R-0112: LLM intake wiring + evidence ─────────────────────────────


_FAKE_INTAKE_JSON = json.dumps({
    "schema_v": "ji1",
    "goal": "Fake-provider goal for R-0112.",
    "context_refs": [],
    "constraints": [],
    "acceptance_hints": [],
    "truncated_input": False,
    "clarifications": [],
})


class TestLLMIntakeWiring:
    def test_fake_provider_stores_llm_intake_with_evidence(self, tmp_path, monkeypatch):
        """Fake provider → intake.source='llm', goal matches, evidence dir exists."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        def _fake_call_fn(prompt: str, attempt: int) -> str:
            return _FAKE_INTAKE_JSON

        monkeypatch.setattr(
            "packages.orchestration.intake.make_provider_call_fn",
            lambda: _fake_call_fn,
        )

        from packages.orchestration.job_plan import TaskPlanResult
        from packages.orchestration.schemas.models import TaskPlan
        _fp = TaskPlan(
            schema_v="task_plan_v1",
            tasks=[{"id": "T001", "title": "Do thing", "goal": "A goal",
                    "acceptance": ["Done"], "depends_on": [],
                    "est_tokens_band": "M", "files_hint": []}],
            risks=[],
        )
        monkeypatch.setattr(
            "packages.orchestration.job_plan.plan_job_llm",
            lambda intake, call_fn, **kw: TaskPlanResult(
                plan=_fp, source="llm", calls=1),
        )

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.chdir(str(repo))

        data = _shape_order(repo, "build a readme").to_json()
        assert data["intake"]["source"] == "llm"
        assert data["intake"]["fallback_reason"] == ""
        assert data["intake"]["goal"] == "Fake-provider goal for R-0112."

        job_id = data["job_id"]
        runs_dir = tmp_path / "data" / "job_logs" / job_id
        assert runs_dir.exists(), "evidence directory must exist"
        trace_files = list(runs_dir.glob("prompt_trace.jsonl"))
        assert trace_files, "prompt_trace.jsonl must exist in evidence dir"

        show = subprocess.run(
            [*_CLI, "job", "show", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert show.returncode == 0
        job_data = json.loads(show.stdout)
        assert job_data["intake"]["schema_v"] == "ji1"
        assert job_data["intake"]["goal"] == "Fake-provider goal for R-0112."

    def test_no_provider_heuristic_fallback_exit_0(self, tmp_path, monkeypatch):
        """Provider unavailable → heuristic fallback, exit 0."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        monkeypatch.setattr(
            "packages.orchestration.intake.make_provider_call_fn",
            lambda: None,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.chdir(str(repo))

        data = _shape_order(repo, "build a readme").to_json()
        assert data["intake"]["source"] == "heuristic"
        assert data["intake"]["fallback_reason"] == "provider_unavailable"

    def test_no_llm_skips_provider(self, tmp_path, monkeypatch):
        """--no-llm → zero provider attempts even if provider available."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        provider_called = []

        def _tracking_call_fn(prompt: str, attempt: int) -> str:
            provider_called.append(1)
            return _FAKE_INTAKE_JSON

        monkeypatch.setattr(
            "packages.orchestration.intake.make_provider_call_fn",
            lambda: _tracking_call_fn,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.chdir(str(repo))

        data = _shape_order(repo, "build a readme", no_llm=True).to_json()
        assert data["intake"]["source"] == "heuristic"
        assert data["intake"]["fallback_reason"] == "forced"
        assert len(provider_called) == 0, "provider must not be called with --no-llm"

    def test_provider_error_label_distinct_from_unavailable(self, tmp_path, monkeypatch):
        """Provider reachable but returns bad output → 'provider error', not 'unavailable'.

        Intake falls to heuristic; task plan is mocked to succeed so we
        isolate the intake label under test.
        """
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        def _bad_call_fn(prompt: str, attempt: int) -> str:
            return "not valid json"

        monkeypatch.setattr(
            "packages.orchestration.intake.make_provider_call_fn",
            lambda: _bad_call_fn,
        )

        from packages.orchestration.job_plan import TaskPlanResult
        from packages.orchestration.schemas.models import TaskPlan
        _fp = TaskPlan(
            schema_v="task_plan_v1",
            tasks=[{"id": "T001", "title": "Do thing", "goal": "A goal",
                    "acceptance": ["Done"], "depends_on": [],
                    "est_tokens_band": "M", "files_hint": []}],
            risks=[],
        )
        monkeypatch.setattr(
            "packages.orchestration.job_plan.plan_job_llm",
            lambda intake, call_fn, **kw: TaskPlanResult(
                plan=_fp, source="llm", calls=1),
        )

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.chdir(str(repo))

        shaped = _shape_order(repo, "build a readme")
        assert shaped.intake_label == "intake: heuristic fallback (provider error)"


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

    def test_status_shows_the_do_job(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        result = _run_status(repo, env)
        assert result.returncode == 0
        assert "completed" in result.stdout

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
        completed_jobs = data["jobs"].get("completed", [])
        assert len(completed_jobs) >= 2

    def test_status_corrupt_file_handled(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        jobs_dir = tmp_path / "data" / "jobs"
        (jobs_dir / "badjob").mkdir(parents=True, exist_ok=True)
        (jobs_dir / "badjob" / "job.json").write_text("{corrupt")

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
        assert "Jobs (" in result.stdout
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
        assert data["scope"] in ("all projects", data.get("project", "current"))

    def test_status_stop_pending(self, tmp_path, monkeypatch):
        """F011 stop request via CLI → stops_pending counts it."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        job_id = _planned_job_id(tmp_path, monkeypatch, repo)

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
        job_id = json.loads(do_result.stdout)["job_ids"][0]

        runs_dir = tmp_path / "data" / "job_logs" / job_id
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

    def test_job_stop_golden_path_job(self, tmp_path, monkeypatch):
        """remedy job stop <golden-path id> exits 0 and records request."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        job_id = _planned_job_id(tmp_path, monkeypatch, repo)

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
    def test_visible_groups_in_d4_order(self, tmp_path):
        """DECISION amend0905-vocab D4 (binding, complete): the sixteen visible
        groups appear in `remedy --help` in this fixed order, `do` pinned first."""
        from apps.cli.command_catalog import VISIBLE_GROUP_ORDER

        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        result = subprocess.run(
            [*_CLI, "--help"],
            capture_output=True, text=True, timeout=10,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0
        row_gids: list[str] = []
        for line in result.stdout.splitlines():
            if not line.startswith("│  "):
                continue
            rest = line[len("│  "):]
            for gid in VISIBLE_GROUP_ORDER:
                if rest.startswith(gid) and (len(rest) == len(gid) or not rest[len(gid)].isalnum()):
                    row_gids.append(gid)
                    break
        assert row_gids == list(VISIBLE_GROUP_ORDER)


class TestGoldenPathSmoke:
    def test_init_do_status_stop_flow(self, tmp_path):
        """Golden path: init → do → status → stop → status: do ran the job, so stop is refused."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        init = _init_project(repo, env)
        assert init.returncode == 0, init.stderr

        do = _run_do(repo, env, "build a readme", ["--json"])
        assert do.returncode == 0, do.stderr
        do_data = json.loads(do.stdout)
        job_id = do_data["job_ids"][0]
        short_id = job_id[:8]

        status = _run_status(repo, env, ["--json"])
        assert status.returncode == 0, status.stderr
        status_data = json.loads(status.stdout)

        completed_ids = [j["job_id"] for j in status_data["jobs"].get("completed", [])]
        assert job_id in completed_ids

        text_status = _run_status(repo, env)
        assert text_status.returncode == 0
        assert short_id in text_status.stdout
        assert "completed" in text_status.stdout

        stop = subprocess.run(
            [*_CLI, "job", "stop", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 1
        assert f"job {job_id} is already completed" in stop.stderr

        status2 = _run_status(repo, env, ["--json"])
        assert status2.returncode == 0
        status2_data = json.loads(status2.stdout)
        assert status2_data["stops_pending"] == 0


# ── Short-ID resolution (R-0097) ─────────────────────────────────────


class TestShortIdResolution:
    def test_stop_with_screen_displayed_short_id(self, tmp_path):
        """Parse short ID from TEXT output of `remedy do`, stop with it."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do = _run_do(repo, env, "build a readme")
        assert do.returncode == 0, do.stderr
        m = re.search(r"one job ([0-9a-f]{16})", do.stdout)
        assert m, f"no job id in do output: {do.stdout!r}"
        full_id = m.group(1)
        short_id = full_id[:8]

        # The job `do` ran is completed, so the stop is refused — by the FULL id the
        # screen-displayed short id resolved to, which is what this test proves.
        stop = subprocess.run(
            [*_CLI, "job", "stop", short_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 1, (stop.stderr, stop.stdout)
        assert f"job {full_id} is already completed" in stop.stderr

    def test_ambiguous_short_id_exits_2(self, tmp_path):
        """Two jobs sharing a prefix → exit 2 with candidates listed."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do1 = _run_do(repo, env, "first job", ["--json"])
        assert do1.returncode == 0
        id1 = json.loads(do1.stdout)["job_ids"][0]
        do2 = _run_do(repo, env, "second job", ["--json"])
        assert do2.returncode == 0
        id2 = json.loads(do2.stdout)["job_ids"][0]

        # Find shortest common prefix (at least 4 chars).
        common = 0
        for a, b in zip(id1, id2):
            if a == b:
                common += 1
            else:
                break
        if common < 4:
            jobs_dir = tmp_path / "data" / "jobs"
            forced_id = id1[:8] + id2[8:]
            dst = jobs_dir / forced_id
            (jobs_dir / id2).rename(dst)
            record = dst / "job.json"
            record.write_text(record.read_text().replace(str(id2), forced_id))
            prefix = id1[:8]
        else:
            prefix = id1[:common]
            if len(prefix) < 4:
                prefix = id1[:4]

        stop = subprocess.run(
            [*_CLI, "job", "stop", prefix],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 2, (stop.returncode, stop.stderr, stop.stdout)
        assert "ambiguous" in stop.stderr

    def test_unknown_short_id_exits_3(self, tmp_path):
        """Unknown hex prefix → exit 3 (not found)."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        stop = subprocess.run(
            [*_CLI, "job", "stop", "deadbeef"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert stop.returncode == 3

    def test_status_next_line_runs_verbatim(self, tmp_path):
        """Every Next: line printed by `remedy status` runs verbatim as a command."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)
        _run_do(repo, env, "build a readme")

        status = _run_status(repo, env)
        assert status.returncode == 0

        for line in status.stdout.splitlines():
            if "Next:" not in line:
                continue
            cmd_text = line.split("Next:", 1)[1].strip()
            if cmd_text.startswith("remedy do"):
                continue
            parts = cmd_text.replace("remedy ", "").split()
            result = subprocess.run(
                [*_CLI, *parts],
                capture_output=True, text=True, timeout=30,
                cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
            )
            assert result.returncode == 0, (
                f"Next-line command failed: {cmd_text!r}\n"
                f"exit={result.returncode}\nstderr={result.stderr}"
            )

    def test_job_show_accepts_short_id(self, tmp_path):
        """remedy job show <short> resolves to full UUID."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do = _run_do(repo, env, "build a readme", ["--json"])
        assert do.returncode == 0
        job_id = json.loads(do.stdout)["job_ids"][0]
        short = job_id[:8]

        result = subprocess.run(
            [*_CLI, "job", "show", short],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data["job_id"] == job_id

    def test_decision_list_accepts_short_id(self, tmp_path):
        """remedy decision list <short> resolves to full UUID."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        _init_project(repo, env)

        do = _run_do(repo, env, "build a readme", ["--json"])
        assert do.returncode == 0
        job_id = json.loads(do.stdout)["job_ids"][0]
        short = job_id[:8]

        result = subprocess.run(
            [*_CLI, "decision", "list", short],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, result.stderr

"""Tests for flight plan approval gate (F014 T004)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

from packages.core.models import Job
from packages.orchestration.decision_queue import DECISION_TYPES, list_decisions

_CLI = [sys.executable, "-m", "apps.cli.grouped"]


class TestFlightPlanApprovalDecisionType:

    def test_type_registered(self):
        assert "flight_plan_approval" in DECISION_TYPES


class TestFlightPlanApprovalDecision:

    def test_pending_creates_blocker(self):
        job = Job(name="t", flight_plan={"_approval": "pending"})
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"]
        assert len(fp) == 1
        assert fp[0].severity == "blocker"
        assert fp[0].status == "open"
        assert fp[0].id == "fp:approval"

    def test_approved_no_decision(self):
        job = Job(name="t", flight_plan={"_approval": "approved"})
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"]
        assert len(fp) == 0

    def test_rejected_no_decision(self):
        job = Job(name="t", flight_plan={"_approval": "rejected"})
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"]
        assert len(fp) == 0

    def test_no_flight_plan_no_decision(self):
        job = Job(name="t")
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"]
        assert len(fp) == 0

    def test_next_actions(self):
        job = Job(name="t", flight_plan={"_approval": "pending"})
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"][0]
        actions = " ".join(fp.next_actions)
        assert "approve" in actions
        assert "reject" in actions

    def test_safe_summary(self):
        job = Job(name="t", flight_plan={"_approval": "pending"})
        fp = [d for d in list_decisions(job, []) if d.type == "flight_plan_approval"][0]
        assert "awaiting approval" in fp.safe_summary.lower()


def _git_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _env(tmp_path):
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(tmp_path / "data"),
    }


_FAKE_INTAKE_JSON = json.dumps({
    "schema_v": "ji1",
    "goal": "Test goal.",
    "context_refs": [],
    "constraints": [],
    "acceptance_hints": [],
    "truncated_input": False,
    "clarifications": [],
})


def _setup_llm_mocks(monkeypatch, *, plan_succeeds=True):
    """Configure monkeypatches for LLM intake + flight plan path."""
    def _fake_call(prompt: str, attempt: int) -> str:
        return _FAKE_INTAKE_JSON

    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: _fake_call,
    )

    from packages.orchestration.flight_plan import FlightPlanResult
    from packages.orchestration.schemas.models import FlightPlan

    if plan_succeeds:
        _fp = FlightPlan(
            schema_v="flight_plan_v1",
            tasks=[{
                "id": "T001", "title": "Do thing", "goal": "A goal",
                "acceptance": ["Done"], "depends_on": [],
                "est_tokens_band": "M", "files_hint": [],
            }],
            risks=[],
        )
        monkeypatch.setattr(
            "packages.orchestration.flight_plan.plan_job_llm",
            lambda intake, call_fn, **kw: FlightPlanResult(
                plan=_fp, source="llm", calls=1),
        )
    else:
        monkeypatch.setattr(
            "packages.orchestration.flight_plan.plan_job_llm",
            lambda intake, call_fn, **kw: FlightPlanResult(
                plan=None, source="llm", error_hint="parse failure"),
        )


class TestFlightPlanLabel:

    def test_deterministic_fallback_label(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        result = subprocess.run(
            [*_CLI, "do", "test mission", "--no-llm", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert result.returncode == 0, result.stderr
        data = json.loads(result.stdout)
        assert data["plan_label"] == "deterministic skeleton"

    def test_llm_flight_plan_label(self, tmp_path, monkeypatch):
        """Successful LLM flight plan -> label contains 'flight plan' + 'awaiting approval'."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        monkeypatch.chdir(str(repo))

        from io import StringIO
        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)

        from apps.cli.commands.do_cmd import _cmd_do_mission
        _cmd_do_mission("test mission", repo=str(repo), json_output=True)

        data = json.loads(captured.getvalue())
        assert "flight plan" in data["plan_label"].lower()
        assert "awaiting approval" in data["plan_label"].lower()
        assert data["state"] == "planned"

    def test_llm_plan_stores_pending_approval(self, tmp_path, monkeypatch):
        """Successful LLM flight plan -> job.flight_plan._approval == 'pending'."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        monkeypatch.chdir(str(repo))

        from io import StringIO
        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)

        from apps.cli.commands.do_cmd import _cmd_do_mission
        _cmd_do_mission("test mission", repo=str(repo), json_output=True)

        data = json.loads(captured.getvalue())
        job_id = data["job_id"]

        show = subprocess.run(
            [*_CLI, "job", "show", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert show.returncode == 0, show.stderr
        job_data = json.loads(show.stdout)
        assert job_data["flight_plan"] is not None
        assert job_data["flight_plan"]["_approval"] == "pending"

    def test_flight_plan_failure_falls_back(self, tmp_path, monkeypatch):
        """LLM flight plan failure -> deterministic skeleton label."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        _setup_llm_mocks(monkeypatch, plan_succeeds=False)
        monkeypatch.chdir(str(repo))

        from io import StringIO
        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)

        from apps.cli.commands.do_cmd import _cmd_do_mission
        _cmd_do_mission("test mission", repo=str(repo), json_output=True)

        data = json.loads(captured.getvalue())
        assert data["plan_label"] == "deterministic skeleton"
        assert data["state"] == "planned"

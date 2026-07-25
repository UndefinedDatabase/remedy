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
        assert "remedy decision resolve" in actions
        assert "--reason approve" in actions
        assert "--reason reject" in actions

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

    def test_flight_plan_parse_failure_not_planned(self, tmp_path, monkeypatch):
        """LLM flight plan parse failure -> non-zero exit, no tasks, postmortem."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        _setup_llm_mocks(monkeypatch, plan_succeeds=False)
        monkeypatch.chdir(str(repo))

        import pytest
        from apps.cli.commands.do_cmd import _cmd_do_mission
        with pytest.raises(SystemExit) as exc_info:
            _cmd_do_mission("test mission", repo=str(repo), json_output=True)
        assert exc_info.value.code != 0


class TestApprovalGateEnforcement:
    """R-0119: execution refused while approval pending."""

    def test_run_refused_while_pending(self, tmp_path, monkeypatch):
        from packages.orchestration.flight_plan import flight_plan_approval_open
        job = Job(name="t", flight_plan={"_approval": "pending"})
        assert flight_plan_approval_open(job)

    def test_approved_not_blocked(self):
        from packages.orchestration.flight_plan import flight_plan_approval_open
        job = Job(name="t", flight_plan={"_approval": "approved"})
        assert not flight_plan_approval_open(job)

    def test_no_plan_not_blocked(self):
        from packages.orchestration.flight_plan import flight_plan_approval_open
        job = Job(name="t")
        assert not flight_plan_approval_open(job)


class TestDecisionResolve:
    """R-0120: approve/reject via remedy decision resolve."""

    def test_approve_flow(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = Job(name="t", flight_plan={"_approval": "pending"})
        save_job(job)
        short_id = str(job.id)[:8]

        from apps.cli.commands.decision import _cmd_decision_resolve
        _cmd_decision_resolve(short_id, "fp:approval", reason="approve")

        from packages.orchestration.storage import load_job
        updated = load_job(job.id)
        assert updated.flight_plan["_approval"] == "approved"

    def test_reject_flow(self, tmp_path, monkeypatch):
        from packages.orchestration.storage import save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = Job(name="t", flight_plan={"_approval": "pending"})
        save_job(job)
        short_id = str(job.id)[:8]

        from apps.cli.commands.decision import _cmd_decision_resolve
        _cmd_decision_resolve(short_id, "fp:approval", reason="reject")

        from packages.orchestration.storage import load_job
        updated = load_job(job.id)
        assert updated.flight_plan["_approval"] == "rejected"

    def test_bad_reason_exits(self, tmp_path, monkeypatch):
        import pytest
        from packages.orchestration.storage import save_job
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = Job(name="t", flight_plan={"_approval": "pending"})
        save_job(job)
        short_id = str(job.id)[:8]

        from apps.cli.commands.decision import _cmd_decision_resolve
        with pytest.raises(SystemExit) as exc_info:
            _cmd_decision_resolve(short_id, "fp:approval", reason="maybe")
        assert exc_info.value.code == 1


class TestAutoApproval:
    """R-0124: --yes auto-approves with audit trail."""

    def test_yes_auto_approves(self, tmp_path, monkeypatch):
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
        _cmd_do_mission("test mission", repo=str(repo), json_output=True, yes=True)

        data = json.loads(captured.getvalue())
        assert "approved via --yes" in data["plan_label"]

        job_id = data["job_id"]
        show = subprocess.run(
            [*_CLI, "job", "show", job_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        job_data = json.loads(show.stdout)
        assert job_data["flight_plan"]["_approval"] == "approved"
        assert job_data["flight_plan"]["_approval_audit"]["mode"] == "auto_yes"

    def test_yes_not_blocked(self, tmp_path, monkeypatch):
        """--yes approved plan should not be blocked by approval gate."""
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
        _cmd_do_mission("test mission", repo=str(repo), json_output=True, yes=True)

        data = json.loads(captured.getvalue())
        fp_decisions = [
            d for d in list_decisions(Job(name="t",
                flight_plan={"_approval": "approved",
                             "_approval_audit": {"mode": "auto_yes"}}), [])
            if d.type == "flight_plan_approval"
        ]
        assert len(fp_decisions) == 0


class TestReplanApprovalRearm:
    """R-0129: replan re-arms _approval to pending."""

    def test_replan_rearms_approval(self, tmp_path):
        from packages.orchestration.flight_plan import replan
        from packages.orchestration.schemas.models import FlightPlan

        old_plan = {
            "schema_v": "flight_plan_v1",
            "tasks": [{"id": "T001", "title": "X", "goal": "G",
                        "acceptance": ["A"], "depends_on": [],
                        "est_tokens_band": "M", "files_hint": []}],
            "risks": [],
            "_approval": "rejected",
        }
        new_plan = FlightPlan(
            schema_v="flight_plan_v1",
            tasks=[{"id": "T001", "title": "Y", "goal": "G2",
                    "acceptance": ["B"], "depends_on": [],
                    "est_tokens_band": "S", "files_hint": []}],
            risks=[],
        )
        ev_dir = tmp_path / "evidence"
        ev_dir.mkdir()
        result, version = replan(old_plan, new_plan, ev_dir)
        assert result["_approval"] == "pending"
        assert version == 2

    def test_replan_rejected_after_completed_task(self, tmp_path):
        import pytest
        from packages.orchestration.flight_plan import ReplanRejectedError, replan
        from packages.orchestration.schemas.models import FlightPlan

        old_plan = {
            "schema_v": "flight_plan_v1",
            "tasks": [{"id": "T001", "title": "X", "goal": "G",
                        "acceptance": ["A"], "depends_on": [],
                        "est_tokens_band": "M", "files_hint": []}],
            "risks": [],
            "_approval": "approved",
        }
        new_plan = FlightPlan(
            schema_v="flight_plan_v1",
            tasks=[{"id": "T001", "title": "Y", "goal": "G2",
                    "acceptance": ["B"], "depends_on": [],
                    "est_tokens_band": "S", "files_hint": []}],
            risks=[],
        )
        ev_dir = tmp_path / "evidence"
        ev_dir.mkdir()
        with pytest.raises(ReplanRejectedError):
            replan(old_plan, new_plan, ev_dir, any_task_completed=True)

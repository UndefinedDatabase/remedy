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


_FAKE_PLAN_JSON = json.dumps({
    "schema_v": "flight_plan_v1",
    "tasks": [{
        "id": "T001", "title": "Do thing", "goal": "A goal",
        "acceptance": ["Done"], "depends_on": [],
        "est_tokens_band": "M", "files_hint": [],
    }],
    "risks": [],
})


def _setup_llm_mocks(monkeypatch, *, plan_succeeds=True, transformations=None):
    """Configure monkeypatches for LLM intake + flight plan path.

    Both call_fn FACTORIES are mocked, not only the functions behind them.
    `do_cmd` reaches the flight-plan branch solely when
    `intake.make_structured_call_fn` hands back a callable, and the real factory
    decides that by probing a live Ollama server. Leaving it unmocked made these
    tests read the developer machine instead of their own fixtures: green with a
    server up, and on a CI runner silently down the `deterministic skeleton`
    path, where every assertion below is about the plan that never got built.
    """
    def _fake_call(prompt: str, attempt: int) -> str:
        return _FAKE_INTAKE_JSON

    monkeypatch.setattr(
        "packages.orchestration.intake.make_provider_call_fn",
        lambda: _fake_call,
    )

    def _fake_plan_call(prompt: str, attempt: int) -> str:
        return _FAKE_PLAN_JSON

    # Returns a callable for every model_cls it is asked for, so the caller takes
    # the provider branch. The payload is a valid FlightPlan rather than a stub:
    # `plan_job_llm` is replaced below and never invokes it, but a later test that
    # stops replacing it then still drives a mock instead of a live server.
    monkeypatch.setattr(
        "packages.orchestration.intake.make_structured_call_fn",
        lambda model_cls, **kw: _fake_plan_call,
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
                plan=_fp, source="llm", calls=1,
                transformations=list(transformations or [])),
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

    def test_normalization_record_is_persisted_and_rendered(
            self, tmp_path, monkeypatch):
        """F016: the record lands on the job dict and in plan.md."""
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        data_dir = tmp_path / "data"
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        _setup_llm_mocks(monkeypatch, plan_succeeds=True, transformations=[{
            "kind": "split",
            "source_ids": ["T000"],
            "result_ids": ["T001"],
            "reason": "oversized task sliced",
        }])
        monkeypatch.chdir(str(repo))

        from io import StringIO
        captured = StringIO()
        monkeypatch.setattr("sys.stdout", captured)

        from apps.cli.commands.do_cmd import _cmd_do_mission
        _cmd_do_mission("test mission", repo=str(repo), json_output=True)
        job_id = json.loads(captured.getvalue())["job_id"]

        from packages.orchestration.storage import load_job
        saved = load_job(job_id)
        assert saved.flight_plan["_normalization"] == [{
            "kind": "split",
            "source_ids": ["T000"],
            "result_ids": ["T001"],
            "reason": "oversized task sliced",
        }]

        plan_md = data_dir / "evidence_exports" / job_id / "plan.md"
        text = plan_md.read_text()
        assert "## Normalization" in text
        assert "oversized task sliced" in text

    def test_flight_plan_parse_failure_not_planned(self, tmp_path, monkeypatch):
        """LLM flight plan parse failure -> non-zero exit, no tasks, postmortem."""
        from pathlib import Path

        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        data_dir = tmp_path / "data"
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        _setup_llm_mocks(monkeypatch, plan_succeeds=False)
        monkeypatch.chdir(str(repo))

        import pytest
        from apps.cli.commands.do_cmd import _cmd_do_mission
        with pytest.raises(SystemExit) as exc_info:
            _cmd_do_mission("test mission", repo=str(repo), json_output=True)
        assert exc_info.value.code != 0

        # Verify saved job: state != planned, tasks empty
        from packages.orchestration.storage import list_jobs
        jobs = list_jobs()
        assert len(jobs) == 1
        saved_job = jobs[0]
        assert saved_job.state.value != "planned"
        assert saved_job.tasks == []

        # Verify postmortem exists under evidence dir
        ev_dir = data_dir / "evidence_exports" / str(saved_job.id)
        postmortem_files = list(ev_dir.glob("*postmortem*")) if ev_dir.exists() else []
        assert len(postmortem_files) > 0, f"postmortem file must exist in {ev_dir}"


class TestApprovalGateEnforcement:
    """R-0119/R-0130: execution refused while pending or rejected."""

    def test_run_refused_while_pending(self, tmp_path, monkeypatch):
        from packages.orchestration.flight_plan import flight_plan_blocks_execution
        job = Job(name="t", flight_plan={"_approval": "pending"})
        assert flight_plan_blocks_execution(job) == "pending"

    def test_run_refused_while_rejected(self):
        from packages.orchestration.flight_plan import flight_plan_blocks_execution
        job = Job(name="t", flight_plan={"_approval": "rejected"})
        assert flight_plan_blocks_execution(job) == "rejected"

    def test_approved_not_blocked(self):
        from packages.orchestration.flight_plan import flight_plan_blocks_execution
        job = Job(name="t", flight_plan={"_approval": "approved"})
        assert flight_plan_blocks_execution(job) is None

    def test_no_plan_not_blocked(self):
        from packages.orchestration.flight_plan import flight_plan_blocks_execution
        job = Job(name="t")
        assert flight_plan_blocks_execution(job) is None

    def test_rejected_cli_exit_3(self, tmp_path):
        """R-0130: rejected plan refuses execution at CLI level."""
        from packages.core.models import Task, RunState
        from packages.orchestration.storage import save_job
        env = _env(tmp_path)
        repo = _git_repo(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        job = Job(
            name="rejected-test",
            state=RunState.PLANNED,
            flight_plan={"_approval": "rejected"},
            tasks=[Task(description="X")],
        )
        env_with_data = {**env, "REMEDY_DATA_DIR": str(tmp_path / "data")}
        save_result = subprocess.run(
            [sys.executable, "-c", f"""
import os, sys
sys.path.insert(0, os.environ["PYTHONPATH"])
os.environ["REMEDY_DATA_DIR"] = "{tmp_path / 'data'}"
from packages.core.models import Job, Task, RunState
from packages.orchestration.storage import save_job
job = Job(name="rejected-test", state=RunState.PLANNED,
          flight_plan={{"_approval": "rejected"}},
          tasks=[Task(description="X")])
save_job(job)
print(str(job.id))
"""],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env_with_data,
        )
        job_id = save_result.stdout.strip()
        short_id = job_id[:8]

        run = subprocess.run(
            [*_CLI, "job", "run-next", short_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env_with_data, stdin=subprocess.DEVNULL,
        )
        assert run.returncode == 3
        assert "flight plan rejected" in run.stderr
        assert "remedy do replan" in run.stderr


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
                             "_approval_audit": {"mode": "auto_yes",
                                                 "reason": "auto-approved via --yes"}}), [])
            if d.type == "flight_plan_approval"
        ]
        open_decisions = [d for d in fp_decisions if d.status == "open"]
        resolved_decisions = [d for d in fp_decisions if d.status == "resolved"]
        assert len(open_decisions) == 0
        assert len(resolved_decisions) == 1
        assert "auto-approved via --yes" in resolved_decisions[0].safe_summary


class TestConfigBudgetPrecedence:
    """R-0133: config-set budgets win over plan-suggested budgets."""

    def test_config_budget_survives_plan_suggestion(self, tmp_path, monkeypatch):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        # Write config with max_total_tokens = 5000
        config_file = repo / "remedy.toml"
        config_file.write_text(
            "[remedy]\n[remedy.budget]\nmax_total_tokens = 5000\n"
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        # Mock plan suggests max_total_tokens = 99999
        from packages.orchestration.flight_plan import FlightPlanResult
        from packages.orchestration.schemas.models import FlightPlan
        _fp = FlightPlan(
            schema_v="flight_plan_v1",
            tasks=[{
                "id": "T001", "title": "Do thing", "goal": "A goal",
                "acceptance": ["Done"], "depends_on": [],
                "est_tokens_band": "M", "files_hint": [],
            }],
            risks=[],
            budgets={"max_total_tokens": 99999},
        )
        monkeypatch.setattr(
            "packages.orchestration.flight_plan.plan_job_llm",
            lambda intake, call_fn, **kw: FlightPlanResult(
                plan=_fp, source="llm", calls=1),
        )
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        # Override plan_job_llm again since _setup_llm_mocks sets it
        monkeypatch.setattr(
            "packages.orchestration.flight_plan.plan_job_llm",
            lambda intake, call_fn, **kw: FlightPlanResult(
                plan=_fp, source="llm", calls=1),
        )
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
        job_data = json.loads(show.stdout)
        # Config says 5000, plan says 99999 → config wins
        assert job_data["budgets"]["max_total_tokens"] == 5000

    def test_plan_fills_unset_config_field(self, tmp_path, monkeypatch):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)
        subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        # Config sets ONLY max_total_tokens, leaves max_provider_calls unset
        config_file = repo / "remedy.toml"
        config_file.write_text(
            "[remedy]\n[remedy.budget]\nmax_total_tokens = 5000\n"
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

        from packages.orchestration.flight_plan import FlightPlanResult
        from packages.orchestration.schemas.models import FlightPlan
        _fp = FlightPlan(
            schema_v="flight_plan_v1",
            tasks=[{
                "id": "T001", "title": "Do thing", "goal": "A goal",
                "acceptance": ["Done"], "depends_on": [],
                "est_tokens_band": "M", "files_hint": [],
            }],
            risks=[],
            budgets={"max_provider_calls": 42},
        )
        _setup_llm_mocks(monkeypatch, plan_succeeds=True)
        monkeypatch.setattr(
            "packages.orchestration.flight_plan.plan_job_llm",
            lambda intake, call_fn, **kw: FlightPlanResult(
                plan=_fp, source="llm", calls=1),
        )
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
        job_data = json.loads(show.stdout)
        # Plan fills max_provider_calls since config didn't set it
        assert job_data["budgets"]["max_provider_calls"] == 42


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


class TestApprovalGoldenPathCLI:
    """R-0127: full CLI sequence — init → do(seed) → run(blocked) → approve → status.

    Assumption: inline save_job seeds the job with a pending flight plan as the
    provider stand-in, per spec allowance.
    """

    def test_full_approval_sequence(self, tmp_path):
        repo = _git_repo(tmp_path)
        env = _env(tmp_path)

        # 1. init
        init = subprocess.run(
            [*_CLI, "init"], capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert init.returncode == 0, init.stderr

        # 2. seed job with pending flight plan via save_job
        seed = subprocess.run(
            [sys.executable, "-c", """
import os, json, sys
sys.path.insert(0, os.environ["PYTHONPATH"])
os.environ["REMEDY_DATA_DIR"] = os.environ["REMEDY_DATA_DIR"]
from packages.core.models import Job, Task, RunState
from packages.orchestration.storage import save_job
job = Job(
    name="approval-smoke",
    state=RunState.PLANNED,
    flight_plan={
        "schema_v": "flight_plan_v1",
        "tasks": [{"id": "T001", "title": "Do thing", "goal": "G",
                    "acceptance": ["Done"], "depends_on": [],
                    "est_tokens_band": "M", "files_hint": []}],
        "risks": [],
        "_approval": "pending",
    },
    tasks=[Task(description="Do thing")],
)
save_job(job)
print(json.dumps({"job_id": str(job.id)}))
"""],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env,
        )
        assert seed.returncode == 0, seed.stderr
        job_id = json.loads(seed.stdout)["job_id"]
        short_id = job_id[:8]

        # 3. run attempt → expect blocked (exit 3, stderr mentions approval)
        run = subprocess.run(
            [*_CLI, "job", "run-next", short_id],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert run.returncode == 3, f"expected exit 3, got {run.returncode}: {run.stderr}"
        assert "plan awaiting approval" in run.stderr
        assert "remedy decision resolve" in run.stderr

        # 4. approve via CLI
        approve = subprocess.run(
            [*_CLI, "decision", "resolve", short_id, "fp:approval",
             "--reason", "approve"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert approve.returncode == 0, approve.stderr
        assert "approved" in approve.stdout.lower()

        # 5. status shows job
        status = subprocess.run(
            [*_CLI, "job", "status", short_id, "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
        )
        assert status.returncode == 0, status.stderr
        st = json.loads(status.stdout)
        assert st["name"] == "approval-smoke"
        assert st["state"] == "planned"
        assert st["pending_count"] == 1

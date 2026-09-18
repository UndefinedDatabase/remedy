"""F269 T002 — the mission gate: a contract's blocking criteria hold the mission.

The acceptance test DECISION F269 D4 orders, end to end with no double for the
gate: a planned mission carries a three-criterion contract whose checks are
decided by files in a tmp directory — two pass, one cannot.  One job is
dispatched through ``execute_move`` with an ``execute`` seam that runs the REAL
``dod_gate.run_job_gate`` in that directory.  Afterwards the contract reads two
``met`` and one ``unmet``, and ``evaluate_move`` refuses
``declare_mission_achieved`` naming that criterion; once the check can pass
and a job re-runs, the refusal is gone.

``remedy mission achieve`` on such a mission is the operator's override: it
exits 0, names the unmet criteria and sets the status (D4 (5)).

No provider is called: the plan and every check are compiled on F061's
deterministic path.  Missions and job evidence live under ``tmp_path``.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from apps.cli.grouped import main
from packages.orchestration.dod_gate import run_job_gate
from packages.orchestration.mission_compiler import plan_mission
from packages.orchestration.mission_contract import (
    ContractCriterion,
    compile_contract_criteria,
    read_mission_contract,
    write_mission_contract,
)
from packages.orchestration.mission_state import create_mission, load_mission
from packages.orchestration.orchestrator_loop import (
    JobExecution,
    evaluate_move,
    execute_move,
    mark_milestone_done,
)
from packages.orchestration.orchestrator_move_schema import (
    MOVE_DECLARE_MISSION_ACHIEVED,
    MOVE_DISPATCH_JOB,
)
from packages.orchestration.project_registry import RemyProject, save_project

PASSING_TEST = "def test_it():\n    assert True\n"
#: Passes only once ``ready.txt`` exists beside ``tests/``.
GATED_TEST = ("from pathlib import Path\n\n\n"
              "def test_it():\n"
              "    assert (Path(__file__).parent.parent / 'ready.txt').is_file()\n")


@pytest.fixture()
def workdir(tmp_path) -> Path:
    """The directory the job's checks run in: two passing tests, one gated."""
    root = tmp_path / "work"
    (root / "tests").mkdir(parents=True)
    (root / "tests" / "test_a.py").write_text(PASSING_TEST, encoding="utf-8")
    (root / "tests" / "test_b.py").write_text(PASSING_TEST, encoding="utf-8")
    (root / "tests" / "test_c.py").write_text(GATED_TEST, encoding="utf-8")
    return root


@pytest.fixture()
def planned(tmp_path, monkeypatch):
    """A registered project and a planned mission with a three-criterion
    contract: the planner's criterion for M001 names ``tests/test_a.py``, two
    whole-mission template criteria name ``test_b.py`` and ``test_c.py``."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    project = RemyProject(name="Gate", slug="gate")
    save_project(project)
    project_id = str(project.id)
    mission = create_mission(project_id, "make tests/test_a.py pass", root=tmp_path)
    plan_mission(project_id, mission.id, None, root=tmp_path)
    contract = read_mission_contract(load_mission(project_id, mission.id, tmp_path))
    added = compile_contract_criteria([
        ContractCriterion(id="C002", text="tests/test_b.py passes", origin="template"),
        ContractCriterion(id="C003", text="tests/test_c.py passes", origin="template"),
    ])
    write_mission_contract(project_id, mission.id,
                           replace(contract, criteria=contract.criteria + added),
                           tmp_path)
    return project_id, mission.id


def _run_the_real_gate_in(workdir: Path):
    def execute(job):
        result = run_job_gate(str(job.job_id), workdir)
        return JobExecution(terminal_status="all_green", job_status="completed",
                            gate_released=None if result is None else result.released)

    return execute


def _dispatch(project_id: str, mission_id: str, root: Path, workdir: Path):
    move = SimpleNamespace(kind=MOVE_DISPATCH_JOB,
                           payload={"milestone_id": "M001", "step": "build M001"})
    return execute_move(project_id, mission_id, move, root=root,
                        execute=_run_the_real_gate_in(workdir))


def _achieve_refusal(project_id: str, mission_id: str, root: Path) -> str:
    return evaluate_move(load_mission(project_id, mission_id, root),
                         SimpleNamespace(kind=MOVE_DECLARE_MISSION_ACHIEVED, payload={}),
                         observe=lambda *a: None,
                         project_id=project_id, mission_id=mission_id)


def _statuses(project_id: str, mission_id: str, root: Path):
    contract = read_mission_contract(load_mission(project_id, mission_id, root))
    return [(c.id, c.status) for c in contract.criteria]


class TestTheContractHoldsTheMission:
    def test_the_contract_has_three_blocking_criteria_each_with_a_check(
            self, tmp_path, planned):
        project_id, mission_id = planned
        contract = read_mission_contract(load_mission(project_id, mission_id, tmp_path))

        assert [(c.id, c.origin, c.check["spec"]["selector"])
                for c in contract.criteria] == [
            ("C001", "planner", "tests/test_a.py"),
            ("C002", "template", "tests/test_b.py"),
            ("C003", "template", "tests/test_c.py")]
        assert all(c.blocking for c in contract.criteria)

    def test_the_job_gate_decides_two_met_and_one_unmet(self, tmp_path, planned,
                                                       workdir):
        project_id, mission_id = planned

        outcome = _dispatch(project_id, mission_id, tmp_path, workdir)

        assert outcome.status == "dispatched"
        assert "gate=blocked" in outcome.detail
        assert _statuses(project_id, mission_id, tmp_path) == [
            ("C001", "met"), ("C002", "met"), ("C003", "unmet")]
        contract = read_mission_contract(load_mission(project_id, mission_id, tmp_path))
        assert all(c.evidence_ref.startswith(f"{outcome.job_id}:")
                   for c in contract.criteria)

    def test_the_achieve_move_is_refused_naming_the_unmet_criterion(
            self, tmp_path, planned, workdir):
        project_id, mission_id = planned
        _dispatch(project_id, mission_id, tmp_path, workdir)
        mark_milestone_done(project_id, mission_id, "M001", tmp_path)

        reason = _achieve_refusal(project_id, mission_id, tmp_path)

        assert "blocking contract criteria are not met: C003" in reason
        assert "C001" not in reason and "C002" not in reason

    def test_once_the_check_can_pass_a_re_run_lifts_the_refusal(
            self, tmp_path, planned, workdir):
        project_id, mission_id = planned
        _dispatch(project_id, mission_id, tmp_path, workdir)
        mark_milestone_done(project_id, mission_id, "M001", tmp_path)
        assert _achieve_refusal(project_id, mission_id, tmp_path)

        (workdir / "ready.txt").write_text("ready\n", encoding="utf-8")
        _dispatch(project_id, mission_id, tmp_path, workdir)

        assert _statuses(project_id, mission_id, tmp_path) == [
            ("C001", "met"), ("C002", "met"), ("C003", "met")]
        assert _achieve_refusal(project_id, mission_id, tmp_path) == ""


class TestTheOperatorsAchieveIsNotHeld:
    """D4 (5): `mission achieve` names the unmet criteria and is not refused."""

    def _unmet(self, tmp_path, planned, workdir):
        project_id, mission_id = planned
        _dispatch(project_id, mission_id, tmp_path, workdir)
        return project_id, mission_id

    def test_text_names_the_unmet_criteria_before_the_status_line(
            self, tmp_path, planned, workdir, capsys):
        project_id, mission_id = self._unmet(tmp_path, planned, workdir)

        main(["mission", "achieve", mission_id, "--project", project_id])

        lines = capsys.readouterr().out.splitlines()
        [notice] = [line for line in lines if "Unmet blocking criteria" in line]
        assert "C003" in notice and "C001" not in notice
        assert lines.index(notice) < lines.index("  Status: achieved")
        assert load_mission(project_id, mission_id, tmp_path).status == "achieved"

    def test_json_carries_the_unmet_criteria(self, tmp_path, planned, workdir,
                                             capsys):
        project_id, mission_id = self._unmet(tmp_path, planned, workdir)

        main(["mission", "achieve", mission_id, "--project", project_id, "--json"])

        body = json.loads(capsys.readouterr().out)
        assert body["unmet_blocking_criteria"] == ["C003"]
        assert body["mission"]["status"] == "achieved"

    def test_a_met_contract_prints_no_notice_and_an_empty_list(
            self, tmp_path, planned, workdir, capsys):
        project_id, mission_id = planned
        (workdir / "ready.txt").write_text("ready\n", encoding="utf-8")
        _dispatch(project_id, mission_id, tmp_path, workdir)

        main(["mission", "achieve", mission_id, "--project", project_id, "--json"])

        assert json.loads(capsys.readouterr().out)["unmet_blocking_criteria"] == []

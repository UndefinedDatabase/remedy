"""F269 T002 — the mission gate: a contract's blocking criteria hold the mission.

The acceptance test DECISION F269 D4 orders, end to end with no double for the
gate: a planned mission carries a three-criterion contract whose checks are
decided by files in a tmp directory — two pass, one cannot.  One job is
dispatched through ``execute_move`` with an ``execute`` seam that runs the REAL
``dod_gate.run_job_gate`` in that directory.  Afterwards the contract reads two
``met`` and one ``unmet`` — the unmet one whole-mission, so its check is
reported in the job's DoD and the job's gate releases (DECISION F269 D6 (1))
— and ``evaluate_move`` refuses
``declare_mission_achieved`` naming that criterion; once the check can pass
and a job re-runs, the refusal is gone.

``remedy mission achieve`` on such a mission is the operator's override: it
exits 0, names the unmet criteria and sets the status (D4 (5)).

DECISION F269 D9: the same mission run by ``run_mission`` with the real
gate and a three-round budget ends ``iteration_limit`` with one open
remainder decision naming the unmet criterion, and ``yes`` to it at the CLI
starts the follow-up mission holding exactly that criterion.

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
        # DECISION F269 D6 (1): the only red check is C003's, a whole-mission
        # criterion's, so it is reported in the job's DoD and the gate releases.
        assert "gate=released" in outcome.detail
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

    def test_a_red_whole_mission_check_releases_the_job_but_holds_the_mission(
            self, tmp_path, planned, workdir):
        """DECISION F269 D6 (1): reported in the job's DoD, still decided on the contract."""
        from packages.orchestration.dod_gate import load_dod, load_gate_result

        project_id, mission_id = planned
        outcome = _dispatch(project_id, mission_id, tmp_path, workdir)
        mark_milestone_done(project_id, mission_id, "M001", tmp_path)

        # The milestone's own DoD check `acc-001` is C001's check (same kind and
        # spec), so C001's is not added a second time; it stays blocking.
        blocking = {c.id: c.blocking for c in load_dod(outcome.job_id).checks}
        assert blocking == {"acc-001": True, "ctr-C002": False, "ctr-C003": False}
        result = load_gate_result(outcome.job_id)
        assert (result["released"], result["blocking_red"], result["reported_red"]) == (
            True, [], ["ctr-C003"])
        assert _statuses(project_id, mission_id, tmp_path)[2] == ("C003", "unmet")
        assert "blocking contract criteria are not met: C003" in _achieve_refusal(
            project_id, mission_id, tmp_path)

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


class TestTheRemainderAtBudgetEnd:
    """DECISION F269 D9 — T005's Acceptance, end to end with the real job gate.

    `run_mission` with a scripted orchestrator dispatches M001 (the real gate
    runs in the tmp directory), declares M001 done, then claims the mission
    achieved, which the contract refuses on C003; the three-round budget ends
    there.  The run ends `iteration_limit` with one open remainder decision
    naming C003, and `remedy decision resolve ... --reason yes` starts the
    follow-up mission whose contract is exactly C003.
    """

    SCRIPT = (
        {"kind": "dispatch_job", "payload": {"milestone_id": "M001",
                                              "step": "build M001"}},
        {"kind": "declare_milestone_done", "payload": {"milestone_id": "M001"}},
        {"kind": "declare_mission_achieved"},
    )

    def _scripted(self):
        from packages.orchestration.orchestrator_move_schema import (
            ORCHESTRATOR_MOVE_SCHEMA_V,
        )

        answers = [json.dumps({"schema_v": ORCHESTRATOR_MOVE_SCHEMA_V, **move})
                   for move in self.SCRIPT]
        calls: list[str] = []

        def call_fn(prompt: str, attempt: int) -> str:
            calls.append(prompt)
            return answers[min(len(calls), len(answers)) - 1]

        return call_fn

    def _run(self, tmp_path, planned, workdir):
        """The loop with the real gate; its observation is what that gate decided.

        The ``execute`` seam does not move the job record's state, so the
        milestone evidence is read from what the seam ran: before the dispatch
        there is none, after it the job completed with the gate's verdict.
        """
        from packages.orchestration.orchestrator_loop import (
            LoopLimits,
            MilestoneEvidence,
            run_mission,
        )

        project_id, mission_id = planned
        ran: list[JobExecution] = []
        gate = _run_the_real_gate_in(workdir)

        def execute(job):
            ran.append(gate(job))
            return ran[-1]

        def evidence(_project_id, _mission_id, _milestone_id):
            if not ran:
                return MilestoneEvidence()
            return MilestoneEvidence(job_id="gated", job_state="completed",
                                     gate_released=ran[-1].gate_released)

        result = run_mission(
            mission_id, LoopLimits(max_iterations=len(self.SCRIPT)),
            project_id=project_id, call_fn=self._scripted(), root=tmp_path,
            execute=execute, evidence=evidence,
            control_root_path=tmp_path / "control")
        return project_id, mission_id, result

    def _open_remainders(self, project_id, mission_id, root):
        from packages.orchestration.mission_contract import CONTRACT_REMAINDER_MARKER
        from packages.orchestration.orchestrator_loop import open_mission_decisions

        return [r for r in open_mission_decisions(load_mission(project_id, mission_id, root))
                if r["question"].startswith(CONTRACT_REMAINDER_MARKER)]

    def test_the_run_ends_blocked_with_one_remainder_decision_naming_the_criterion(
            self, tmp_path, planned, workdir):
        from packages.orchestration.orchestrator_loop import TERMINAL_ITERATION_LIMIT

        project_id, mission_id, result = self._run(tmp_path, planned, workdir)

        assert result.terminal == TERMINAL_ITERATION_LIMIT
        [refused] = [e for e in result.entries if e.outcome["status"] == "refused"]
        assert refused.move["kind"] == MOVE_DECLARE_MISSION_ACHIEVED
        assert "blocking contract criteria are not met: C003" in refused.outcome["detail"]
        assert _statuses(project_id, mission_id, tmp_path) == [
            ("C001", "met"), ("C002", "met"), ("C003", "unmet")]
        [record] = self._open_remainders(project_id, mission_id, tmp_path)
        assert "C003: tests/test_c.py passes" in record["question"]
        assert "C001" not in record["question"] and "C002" not in record["question"]
        assert f"remainder decision {record['decision_id']} was raised" in result.detail

    def test_yes_at_the_cli_starts_the_follow_up_mission_holding_the_unmet_criterion(
            self, tmp_path, planned, workdir, capsys):
        from packages.orchestration.mission_state import list_missions

        project_id, mission_id, _result = self._run(tmp_path, planned, workdir)
        [record] = self._open_remainders(project_id, mission_id, tmp_path)
        job_id = load_mission(project_id, mission_id, tmp_path).latest_link().job_id
        capsys.readouterr()

        try:
            main(["decision", "resolve", job_id, record["decision_id"], "--reason", "yes"])
            code = 0
        except SystemExit as exc:
            code = exc.code or 0

        assert code == 0
        out = capsys.readouterr().out
        [follow_up] = [m for m in list_missions(project_id, tmp_path) if m.id != mission_id]
        assert f"Follow-up mission {follow_up.id} started" in out
        assert f"remedy mission plan {follow_up.id}" in out
        contract = read_mission_contract(follow_up)
        assert [(c.id, c.text, c.status) for c in contract.criteria] == [
            ("C001", "tests/test_c.py passes", "open")]
        assert follow_up.order.text == record["impact"]
        assert self._open_remainders(project_id, mission_id, tmp_path) == []

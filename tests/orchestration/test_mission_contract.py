"""F269 T001 and T002 — the contract record, its compiled checks, the job's slice.

What DECISIONs F269 D2 and D3 require proof of:

  * a contract round-trips through the mission record unchanged;
  * every D2 rule is refused on WRITE and on READ of a body stored raw
    through ``set_mission_contract``, with an error naming the rule;
  * a job's slice is the whole-mission criteria plus its milestone's own, in
    contract order, and a job with no milestone gets the whole-mission
    criteria alone;
  * the milestone recorder writes onto an existing job record and writes
    nothing for a job that does not exist.

And what DECISION F269 D4 (1) and (2) require:

  * F061's compiler gives every criterion a check ``ctr-<id>`` tracing to
    ``<id>:0`` and carrying the criterion's own ``blocking``;
  * planning a mission writes one planner criterion per milestone, and a
    re-plan keeps every non-planner criterion with its id.

And D4 (3) and (4): a job's DoD gains its slice checks without duplicating
one it already has, and the job's stored gate result decides its slice
criteria.  D6 (1): a whole-mission criterion's check enters the DoD
non-blocking, a milestone-scoped one with the criterion's ``blocking``.
D7: a contract's job, dispatched or made by `remedy do`, is bound to its
repository and granted the three repository capabilities; a mission with no
contract writes nothing, and a binding already set is kept.

D8: every amendment rule is refused on write and on a raw read; amending
adds one compiled ``amendment`` criterion with the next free id and an entry
that applies from the mission's next round, touches nothing already there,
and survives a re-plan; the renderer lists the amendments after the criteria.

Every test writes into ``tmp_path``; no real provider is called — a planned
mission replays a recorded planner answer.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from packages.orchestration.dod_gate import GateResult, load_dod, save_gate_result, store_dod
from packages.orchestration.dod_runners import CheckEvidence
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck
from packages.orchestration.mission_compiler import plan_mission
from packages.orchestration.mission_contract import (
    JOB_MILESTONE_KEY,
    ContractCriterion,
    ContractError,
    MissionContract,
    amend_mission_contract,
    compile_contract_criteria,
    job_contract_slice,
    merge_contract_slice_into_dod,
    read_job_milestone,
    read_mission_contract,
    record_contract_results,
    record_job_milestone,
    render_contract_lines,
    write_mission_contract,
)
from packages.orchestration.mission_state import (
    create_mission,
    load_mission,
    set_mission_contract,
)
from packages.orchestration.pingpong_job import JobPlan, load_job_plan, save_job_plan

PROJECT = "p-f269"


def _body() -> dict[str, Any]:
    """A valid three-criterion body: whole mission, M1, M2."""
    return {
        "schema": "contract_v1",
        "template": "cli-tool",
        "criteria": [
            {"id": "C001", "text": "the suite passes", "blocking": True,
             "origin": "template", "milestones": [], "check": None,
             "status": "open", "evidence_ref": None},
            {"id": "C002", "text": "the parser reads flags", "blocking": True,
             "origin": "planner", "milestones": ["M1"], "check": None,
             "status": "open", "evidence_ref": None},
            {"id": "C003", "text": "help lists every command", "blocking": False,
             "origin": "planner", "milestones": ["M2"], "check": None,
             "status": "met", "evidence_ref": "evidence/help.txt"},
        ],
        "amendments": [],
    }


#: Stands for "remove this key" in a broken-body row.
_DELETE = object()


def _broken(path: tuple[Any, ...], value: Any) -> dict[str, Any]:
    """The valid body with ONE value at ``path`` replaced, or removed."""
    body = _body()
    target: Any = body
    for key in path[:-1]:
        target = target[key]
    if value is _DELETE:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return body


#: (rule named in the error, the broken body) — one row per D2 rule.
BROKEN_BODIES = [
    ("body is an object", ["not", "an", "object"]),
    ("schema is contract_v1", _broken(("schema",), "contract_v0")),
    ("fields are known", _broken(("extra",), 1)),
    ("fields are known", _broken(("criteria", 0, "weight"), 3)),
    ("required fields are present", _broken(("schema",), _DELETE)),
    ("required fields are present", _broken(("criteria", 0, "text"), _DELETE)),
    ("template is a name or null", _broken(("template",), "")),
    ("criteria is a list", _broken(("criteria",), {"C001": "x"})),
    ("criterion is an object", _broken(("criteria", 0), "the suite passes")),
    ("id is C plus three digits", _broken(("criteria", 0, "id"), "C1")),
    ("id is unique in the contract", _broken(("criteria", 1, "id"), "C001")),
    ("text is non-empty", _broken(("criteria", 0, "text"), "   ")),
    ("blocking is a bool", _broken(("criteria", 0, "blocking"), "yes")),
    ("origin is template, planner or amendment",
     _broken(("criteria", 0, "origin"), "operator")),
    ("milestones is a list of distinct milestone ids",
     _broken(("criteria", 0, "milestones"), "M1")),
    ("milestones is a list of distinct milestone ids",
     _broken(("criteria", 0, "milestones"), ["M1", "M1"])),
    ("check is null or an object", _broken(("criteria", 0, "check"), "pytest")),
    ("status is open, met or unmet", _broken(("criteria", 0, "status"), "done")),
    ("evidence_ref is null or a non-empty string",
     _broken(("criteria", 0, "evidence_ref"), "")),
    ("amendments is a list of objects", _broken(("amendments",), ["a note"])),
]


BROKEN_IDS = [f"{i:02d}-{rule}" for i, (rule, _body_) in enumerate(BROKEN_BODIES)]


@pytest.fixture()
def mission(tmp_path):
    return create_mission(PROJECT, "Ship the tool", root=tmp_path)


class TestTheContractRecord:
    def test_a_contract_round_trips_through_the_mission_record(self, tmp_path,
                                                               mission):
        written = write_mission_contract(PROJECT, mission.id, _body(), tmp_path)

        loaded = read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))

        assert loaded == written
        assert loaded.to_json() == _body()
        assert [c.id for c in loaded.criteria] == ["C001", "C002", "C003"]

    def test_the_defaults_are_the_ones_d2_names(self):
        criterion = ContractCriterion.from_json(
            {"id": "C001", "text": "it builds", "origin": "planner"})

        assert criterion.blocking is True
        assert criterion.status == "open"
        assert criterion.milestones == ()
        assert criterion.check is None
        assert criterion.evidence_ref is None

    def test_a_mission_without_a_contract_reads_as_none(self, mission):
        assert read_mission_contract(mission) is None

    @pytest.mark.parametrize(("rule", "body"), BROKEN_BODIES, ids=BROKEN_IDS)
    def test_a_broken_body_is_refused_on_write(self, tmp_path, mission, rule,
                                               body):
        with pytest.raises(ContractError) as caught:
            write_mission_contract(PROJECT, mission.id, copy.deepcopy(body),
                                   tmp_path)

        assert caught.value.rule == rule
        assert rule in str(caught.value)
        assert load_mission(PROJECT, mission.id, tmp_path).contract is None

    @pytest.mark.parametrize(("rule", "body"), BROKEN_BODIES, ids=BROKEN_IDS)
    def test_a_broken_body_stored_raw_is_refused_on_read(self, tmp_path,
                                                         mission, rule, body):
        if not isinstance(body, dict):
            # The storage call refuses a non-object itself; the reader meets
            # such a body only on a record object, so give it one directly.
            with pytest.raises(ContractError) as caught:
                read_mission_contract(SimpleNamespace(contract=body))
        else:
            set_mission_contract(PROJECT, mission.id, copy.deepcopy(body),
                                 tmp_path)
            with pytest.raises(ContractError) as caught:
                read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))

        assert caught.value.rule == rule
        assert rule in str(caught.value)

    def test_a_contract_error_is_a_value_error(self):
        assert issubclass(ContractError, ValueError)


class TestTheJobSlice:
    def test_a_job_of_m1_gets_the_whole_mission_and_m1_criteria_in_order(self):
        contract = MissionContract.from_json(_body())

        assert [c.id for c in job_contract_slice(contract, "M1")] == ["C001", "C002"]

    def test_a_job_with_no_milestone_gets_the_whole_mission_criteria_only(self):
        contract = MissionContract.from_json(_body())

        assert [c.id for c in job_contract_slice(contract, None)] == ["C001"]

    def test_the_slice_is_a_subset_of_the_mission_criteria(self):
        contract = MissionContract.from_json(_body())

        for milestone in ("M1", "M2", "M3", None):
            assert set(job_contract_slice(contract, milestone)) <= set(contract.criteria)


class TestTheJobMilestone:
    def test_the_recorder_writes_the_milestone_on_the_job(self, tmp_path):
        job = JobPlan(job_title="fixture")
        save_job_plan(job, tmp_path)

        assert record_job_milestone(str(job.job_id), "M1", tmp_path) is True

        stored = load_job_plan(str(job.job_id), tmp_path)
        assert stored.metadata[JOB_MILESTONE_KEY] == "M1"
        assert read_job_milestone(str(job.job_id), tmp_path) == "M1"

    def test_an_unknown_job_is_false_and_writes_nothing(self, tmp_path):
        assert record_job_milestone("0123456789abcdef", "M1", tmp_path) is False
        assert not (tmp_path / "jobs").exists()

    def test_a_job_that_records_no_milestone_reads_as_none(self, tmp_path):
        job = JobPlan(job_title="fixture")
        save_job_plan(job, tmp_path)

        assert read_job_milestone(str(job.job_id), tmp_path) is None


def _criterion(ident: str, text: str, **over: Any) -> ContractCriterion:
    return ContractCriterion(id=ident, text=text,
                             origin=over.pop("origin", "template"), **over)


class TestTheCompiledContract:
    """DECISION F269 D4 (1): F061's compiler gives every criterion its check."""

    def test_every_criterion_gets_its_own_check_with_its_own_blocking(self):
        criteria = [_criterion("C001", "the suite passes"),
                    _criterion("C002", "the docs read well", blocking=False),
                    _criterion("C007", "tests/test_cli.py passes")]

        compiled = compile_contract_criteria(criteria)

        assert [c.id for c in compiled] == ["C001", "C002", "C007"]
        for criterion in compiled:
            assert criterion.check["id"] == f"ctr-{criterion.id}"
            assert criterion.check["acceptance_refs"] == [f"{criterion.id}:0"]
        assert [c.check["blocking"] for c in compiled] == [True, False, True]

    def test_a_non_blocking_criterion_stays_non_blocking(self):
        [compiled] = compile_contract_criteria(
            [_criterion("C001", "the docs read well", blocking=False)])

        assert compiled.blocking is False
        assert compiled.check["blocking"] is False

    def test_a_criterion_naming_a_test_path_compiles_to_that_selector(self):
        [compiled] = compile_contract_criteria(
            [_criterion("C001", "tests/test_cli.py::test_help passes")])

        assert compiled.check["kind"] == "pytest"
        assert compiled.check["spec"] == {"selector": "tests/test_cli.py::test_help"}

    def test_the_compiled_check_is_a_valid_dod_check_and_survives_a_write(
            self, tmp_path, mission):
        compiled = compile_contract_criteria([_criterion("C001", "it builds")])
        written = write_mission_contract(
            PROJECT, mission.id, MissionContract(criteria=compiled), tmp_path)

        assert DoDCheck.model_validate(written.criteria[0].check).id == "ctr-C001"

    def test_nothing_to_compile_is_nothing(self):
        assert compile_contract_criteria([]) == ()


class TestThePlannerCriteria:
    """DECISION F269 D4 (2): planning a mission writes its planner criteria."""

    @pytest.fixture()
    def planned(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        fixture = json.loads((Path(__file__).parent / "fixtures" / "mission"
                              / "payments_platform.json").read_text(encoding="utf-8"))
        draft = json.dumps(fixture["provider_draft"])
        m = create_mission(PROJECT, fixture["mission"]["goal"])
        return m, (lambda prompt, attempt: draft)

    def test_a_planned_mission_carries_one_planner_criterion_per_milestone(
            self, planned):
        m, call_fn = planned
        outcome = plan_mission(PROJECT, m.id, call_fn)

        contract = read_mission_contract(load_mission(PROJECT, m.id))
        milestones = outcome.plan.milestones
        assert len(milestones) >= 2
        assert [c.milestones for c in contract.criteria] == [
            (ms.id,) for ms in milestones]
        assert [c.text for c in contract.criteria] == [ms.goal for ms in milestones]
        assert {c.origin for c in contract.criteria} == {"planner"}
        assert all(c.blocking and c.check is not None for c in contract.criteria)
        assert outcome.mission.contract == contract.to_json()

    def test_a_plan_without_a_provider_still_writes_its_planner_criterion(
            self, planned):
        m, _call_fn = planned
        outcome = plan_mission(PROJECT, m.id, None)

        contract = read_mission_contract(outcome.mission)
        assert [(c.id, c.milestones) for c in contract.criteria] == [("C001", ("M001",))]

    def test_a_replan_keeps_a_non_planner_criterion_and_replaces_the_planner_ones(
            self, planned):
        m, call_fn = planned
        write_mission_contract(PROJECT, m.id, MissionContract(criteria=(
            _criterion("C001", "an old planner criterion", origin="planner",
                       milestones=("M009",)),
            _criterion("C004", "the readme names the install command"),
        ), template="cli-tool"))

        plan_mission(PROJECT, m.id, None)

        contract = read_mission_contract(load_mission(PROJECT, m.id))
        assert contract.template == "cli-tool"
        kept, *planner = contract.criteria
        assert (kept.id, kept.text, kept.origin) == (
            "C004", "the readme names the install command", "template")
        assert kept.check is not None
        assert [(c.id, c.origin, c.milestones) for c in planner] == [
            ("C005", "planner", ("M001",))]


JOB = "0123456789abcdef"


def _pytest_check(check_id: str, selector: str) -> DoDCheck:
    return DoDCheck(id=check_id, kind="pytest", spec={"selector": selector},
                    blocking=True, source="plan_acceptance")


@pytest.fixture()
def sliced(tmp_path, monkeypatch):
    """A mission whose compiled contract has a whole-mission, an M1 and an M2
    criterion, each naming its own test file; the data root is ``tmp_path``."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    m = create_mission(PROJECT, "Ship the tool", root=tmp_path)
    write_mission_contract(PROJECT, m.id, MissionContract(
        criteria=compile_contract_criteria([
            _criterion("C001", "tests/test_all.py passes"),
            _criterion("C002", "tests/test_m1.py passes", milestones=("M1",)),
            _criterion("C003", "tests/test_m2.py passes", milestones=("M2",)),
        ])), tmp_path)
    return load_mission(PROJECT, m.id, tmp_path)


class TestTheJobDoDCarriesItsSlice:
    """DECISION F269 D4 (3): the job's DoD carries its contract slice."""

    def test_a_job_with_no_dod_gets_one_holding_its_slice_checks(self, sliced):
        assert merge_contract_slice_into_dod(sliced, "M1", JOB) == 2

        dod = load_dod(JOB)
        assert [(c.id, c.spec["selector"]) for c in dod.checks] == [
            ("ctr-C001", "tests/test_all.py"), ("ctr-C002", "tests/test_m1.py")]
        assert (dod.compiled, dod.origin) == (False, "deterministic")

    def test_a_whole_mission_criterions_check_enters_non_blocking_though_the_criterion_blocks(
            self, sliced):
        """DECISION F269 D6 (1): a whole-mission check is reported, never held on."""
        whole = read_mission_contract(sliced).criteria[0]
        assert (whole.id, whole.milestones, whole.blocking) == ("C001", (), True)
        assert whole.check["blocking"] is True

        merge_contract_slice_into_dod(sliced, "M1", JOB)

        [check] = [c for c in load_dod(JOB).checks if c.id == "ctr-C001"]
        assert check.blocking is False

    def test_a_milestone_scoped_blocking_criterions_check_enters_blocking(self, sliced):
        """DECISION F269 D6 (1): a milestone's own criterion keeps its ``blocking``."""
        merge_contract_slice_into_dod(sliced, "M1", JOB)

        [check] = [c for c in load_dod(JOB).checks if c.id == "ctr-C002"]
        assert check.blocking is True

    def test_a_job_with_no_milestone_gets_only_non_blocking_checks(self, sliced):
        assert merge_contract_slice_into_dod(sliced, None, JOB) == 1

        assert [(c.id, c.blocking) for c in load_dod(JOB).checks] == [("ctr-C001", False)]

    def test_a_job_for_m1_gets_no_m2_scoped_check(self, sliced):
        merge_contract_slice_into_dod(sliced, "M1", JOB)

        selectors = [c.spec["selector"] for c in load_dod(JOB).checks]
        assert "tests/test_m2.py" not in selectors

    def test_a_check_equal_in_kind_and_spec_is_not_added_a_second_time(
            self, sliced):
        store_dod(JOB, DoD(schema_v=DOD_SCHEMA_V, compiled=False,
                           origin="deterministic",
                           checks=[_pytest_check("acc-001", "tests/test_all.py")]))

        assert merge_contract_slice_into_dod(sliced, "M1", JOB) == 1

        dod = load_dod(JOB)
        assert [(c.id, c.spec["selector"]) for c in dod.checks] == [
            ("acc-001", "tests/test_all.py"), ("ctr-C002", "tests/test_m1.py")]

    def test_merging_twice_adds_nothing_the_second_time(self, sliced):
        merge_contract_slice_into_dod(sliced, "M1", JOB)

        assert merge_contract_slice_into_dod(sliced, "M1", JOB) == 0
        assert len(load_dod(JOB).checks) == 2

    def test_a_mission_without_a_contract_stores_nothing(self, tmp_path,
                                                         monkeypatch, mission):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        assert merge_contract_slice_into_dod(mission, "M1", JOB) == 0
        assert load_dod(JOB) is None


def _gate_result(*passed_or_failed: tuple[str, str]) -> GateResult:
    return GateResult(released=all(s == "passed" for _, s in passed_or_failed),
                      evidence=tuple(CheckEvidence(
                          check_id=check_id, kind="pytest", source="plan_acceptance",
                          blocking=True, status=status, reason="", command="",
                          argv=(), cwd="", exit_code=0, duration_ms=0,
                          output_tail="") for check_id, status in passed_or_failed))


class TestTheJobGateDecidesItsCriteria:
    """DECISION F269 D4 (4): statuses are read back from the job's gate."""

    def test_statuses_and_evidence_follow_the_stored_gate_result(self, tmp_path,
                                                                 sliced):
        store_dod(JOB, DoD(schema_v=DOD_SCHEMA_V, compiled=False,
                           origin="deterministic",
                           checks=[_pytest_check("acc-001", "tests/test_all.py")]))
        merge_contract_slice_into_dod(sliced, "M1", JOB)
        save_gate_result(JOB, _gate_result(("acc-001", "passed"),
                                           ("ctr-C002", "failed")))

        record_contract_results(PROJECT, sliced.id, JOB, "M1", tmp_path)

        contract = read_mission_contract(load_mission(PROJECT, sliced.id, tmp_path))
        assert [(c.id, c.status, c.evidence_ref) for c in contract.criteria] == [
            ("C001", "met", f"{JOB}:acc-001"),
            ("C002", "unmet", f"{JOB}:ctr-C002"),
            ("C003", "open", None)]

    def test_no_gate_result_changes_nothing(self, tmp_path, sliced):
        merge_contract_slice_into_dod(sliced, "M1", JOB)

        assert record_contract_results(PROJECT, sliced.id, JOB, "M1", tmp_path) is None

        assert load_mission(PROJECT, sliced.id, tmp_path).contract == sliced.contract


class TestTheRenderer:
    def test_every_criterion_is_rendered_in_order_with_its_scope(self):
        contract = MissionContract.from_json(_body())

        lines = render_contract_lines("Contract of mission m1", contract.template,
                                      contract.criteria)

        text = "\n".join(lines)
        assert lines[0] == "Contract of mission m1"
        assert "Template: cli-tool" in text
        assert text.index("C001") < text.index("C002") < text.index("C003")
        assert "whole mission" in text
        assert "evidence: evidence/help.txt" in text

    def test_no_criteria_says_so(self):
        lines = render_contract_lines("Contract of job j1", None, ())

        assert "  Criteria: (none)" in lines
        assert "  Template: (none)" in lines


# ── DECISION F269 D7: the contract binds each of its jobs and grants it ──

GRANTS = ("repo_test_run", "repo_generated_write", "repo_revert")


def _allowed(job) -> dict[str, bool]:
    from packages.orchestration.permissions import Capability, is_allowed

    return {grant: is_allowed(job, Capability(grant)) for grant in GRANTS}


@pytest.fixture()
def registered(tmp_path, monkeypatch):
    """A registered project whose canonical repository is ``tmp_path/repo``."""
    from packages.orchestration.project_registry import RemyProject, save_project

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    canonical = tmp_path / "repo"
    canonical.mkdir()
    project = RemyProject(name="Bound", slug="bound", canonical_repo_path=str(canonical))
    save_project(project)
    return str(project.id), str(canonical)


def _dispatch_one_job(project_id: str, mission_id: str, root: Path):
    """Dispatch one job through ``execute_move``; return (stored job, job the executor got)."""
    from packages.orchestration.orchestrator_loop import JobExecution, execute_move
    from packages.orchestration.orchestrator_move_schema import MOVE_DISPATCH_JOB

    seen: list[Any] = []

    def execute(job):
        seen.append(job)
        return JobExecution(terminal_status="all_green", job_status="completed")

    move = SimpleNamespace(kind=MOVE_DISPATCH_JOB,
                           payload={"milestone_id": "M1", "step": "build M1"})
    outcome = execute_move(project_id, mission_id, move, root=root, execute=execute)
    assert outcome.status == "dispatched"
    return load_job_plan(outcome.job_id, root), seen[0]


class TestTheContractBindsAndGrantsItsJobs:
    """DECISION F269 D7: the heir of the deleted `attach-repo` and `permit` words of `job`."""

    def test_a_dispatched_job_gets_the_projects_repository_and_the_three_grants(
            self, tmp_path, registered):
        project_id, canonical = registered
        m = create_mission(project_id, "Ship the tool", root=tmp_path)
        write_mission_contract(project_id, m.id, MissionContract(criteria=(
            _criterion("C001", "the tool ships"),)), tmp_path)

        stored, given = _dispatch_one_job(project_id, m.id, tmp_path)

        assert stored.repo_path == ""
        assert stored.metadata["target_repo"] == canonical
        assert _allowed(stored) == dict.fromkeys(GRANTS, True)
        # The executor saves the in-memory job next, so it carries the same values.
        assert given.metadata["target_repo"] == canonical
        assert _allowed(given) == dict.fromkeys(GRANTS, True)

    def test_a_do_job_is_bound_to_its_own_repo_path_and_granted(self, tmp_path,
                                                                monkeypatch, capsys):
        import subprocess

        from apps.cli.grouped import main

        def tripwire(*args, **kwargs):
            raise AssertionError("remedy do reached a model-call factory under --no-llm")

        for factory in ("packages.orchestration.intake.make_provider_call_fn",
                        "packages.orchestration.intake.make_structured_call_fn",
                        "packages.orchestration.study.study_call_fn"):
            monkeypatch.setattr(factory, tripwire)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        target = tmp_path / "target"
        target.mkdir()
        for args in (("init", "-q"), ("config", "user.email", "t@e.com"),
                     ("config", "user.name", "T"), ("config", "commit.gpgsign", "false")):
            subprocess.run(["git", *args], cwd=target, check=True, capture_output=True)
        (target / "README.md").write_text("# target\n")
        subprocess.run(["git", "add", "-A"], cwd=target, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-qm", "init"], cwd=target, check=True,
                       capture_output=True)
        monkeypatch.chdir(target)

        main(["do", "Write a CONTRIBUTING.md", "--no-llm", "--no-ui", "--json",
              "--plan-only", "--builder-provider", "fake", "--reviewer-provider", "fake"])
        data = json.loads(capsys.readouterr().out)

        assert data["contract"]["criteria"]
        [job_id] = data["job_ids"]
        job = load_job_plan(job_id)
        assert job.repo_path == str(target.resolve())
        assert job.metadata["target_repo"] == job.repo_path
        assert _allowed(job) == dict.fromkeys(GRANTS, True)

    def test_a_mission_with_no_contract_writes_nothing(self, tmp_path, registered):
        project_id, _canonical = registered
        m = create_mission(project_id, "Ship the tool", root=tmp_path)

        stored, given = _dispatch_one_job(project_id, m.id, tmp_path)

        for job in (stored, given):
            assert "target_repo" not in job.metadata
            assert "permissions" not in job.metadata
            assert _allowed(job) == dict.fromkeys(GRANTS, False)

    def test_a_target_repo_already_set_is_not_overwritten(self, tmp_path, registered):
        from packages.orchestration.mission_contract import grant_contract_job_repository

        project_id, _canonical = registered
        m = create_mission(project_id, "Ship the tool", root=tmp_path)
        write_mission_contract(project_id, m.id, MissionContract(criteria=(
            _criterion("C001", "the tool ships"),)), tmp_path)
        job = JobPlan(job_title="fixture", repo_path=str(tmp_path / "own"),
                      metadata={"target_repo": str(tmp_path / "elsewhere")})
        save_job_plan(job, tmp_path)

        grant_contract_job_repository(load_mission(project_id, m.id, tmp_path),
                                      str(job.job_id), tmp_path)

        stored = load_job_plan(str(job.job_id), tmp_path)
        assert stored.metadata["target_repo"] == str(tmp_path / "elsewhere")
        assert _allowed(stored) == dict.fromkeys(GRANTS, True)


# ── DECISION F269 D8: an amendment's shape, its round of effect, its criterion ──


def _amendment(**over: Any) -> dict[str, Any]:
    """A valid amendment entry that added C004 and applies from round 2."""
    body = {"id": "A001", "text": "tests/test_login.py passes",
            "received_at": "2026-09-18T10:00:00+00:00", "applies_from": 2,
            "criteria": ["C004"],
            "understood": "adds blocking criterion C004: tests/test_login.py passes",
            "acknowledged_in": None}
    body.update(over)
    return body


def _amended_body() -> dict[str, Any]:
    """The valid three-criterion body plus one amendment and the criterion it added."""
    body = _body()
    body["criteria"].append(
        {"id": "C004", "text": "tests/test_login.py passes", "blocking": True,
         "origin": "amendment", "milestones": [], "check": None,
         "status": "open", "evidence_ref": None})
    body["amendments"] = [_amendment()]
    return body


def _broken_amendment(field: str, value: Any) -> dict[str, Any]:
    """The amended body with ONE amendment field replaced, or removed."""
    body = _amended_body()
    if value is _DELETE:
        del body["amendments"][0][field]
    else:
        body["amendments"][0][field] = value
    return body


def _twice_amended() -> dict[str, Any]:
    body = _amended_body()
    body["amendments"].append(_amendment())
    return body


#: (rule named in the error, the broken body) — one row per D8 (1) rule.
BROKEN_AMENDMENTS = [
    ("fields are known", _broken_amendment("weight", 3)),
    ("required fields are present", _broken_amendment("acknowledged_in", _DELETE)),
    ("amendment id is A plus three digits", _broken_amendment("id", "A1")),
    ("amendment id is unique in the contract", _twice_amended()),
    ("amendment text is non-empty", _broken_amendment("text", "  ")),
    ("received_at is an ISO timestamp", _broken_amendment("received_at", "yesterday")),
    ("applies_from is a round of at least 1", _broken_amendment("applies_from", 0)),
    ("applies_from is a round of at least 1", _broken_amendment("applies_from", True)),
    ("amendment criteria are amendment criteria of the contract",
     _broken_amendment("criteria", "C004")),
    ("amendment criteria are amendment criteria of the contract",
     _broken_amendment("criteria", ["C009"])),
    ("amendment criteria are amendment criteria of the contract",
     _broken_amendment("criteria", ["C001"])),
    ("understood is non-empty", _broken_amendment("understood", "")),
    ("acknowledged_in is null or a round not before applies_from",
     _broken_amendment("acknowledged_in", 1)),
    ("acknowledged_in is null or a round not before applies_from",
     _broken_amendment("acknowledged_in", "2")),
]

AMENDMENT_IDS = [f"{i:02d}-{rule}" for i, (rule, _b) in enumerate(BROKEN_AMENDMENTS)]


class TestTheAmendmentShape:
    """DECISION F269 D8 (1): every rule is refused on write and on a raw read."""

    def test_a_valid_amendment_round_trips(self, tmp_path, mission):
        write_mission_contract(PROJECT, mission.id, _amended_body(), tmp_path)

        loaded = read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))

        assert loaded.to_json() == _amended_body()

    @pytest.mark.parametrize(("rule", "body"), BROKEN_AMENDMENTS, ids=AMENDMENT_IDS)
    def test_a_broken_amendment_is_refused_on_write(self, tmp_path, mission, rule,
                                                    body):
        with pytest.raises(ContractError) as caught:
            write_mission_contract(PROJECT, mission.id, copy.deepcopy(body), tmp_path)

        assert caught.value.rule == rule
        assert rule in str(caught.value)
        assert load_mission(PROJECT, mission.id, tmp_path).contract is None

    @pytest.mark.parametrize(("rule", "body"), BROKEN_AMENDMENTS, ids=AMENDMENT_IDS)
    def test_a_broken_amendment_stored_raw_is_refused_on_read(self, tmp_path,
                                                              mission, rule, body):
        set_mission_contract(PROJECT, mission.id, copy.deepcopy(body), tmp_path)

        with pytest.raises(ContractError) as caught:
            read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))

        assert caught.value.rule == rule
        assert rule in str(caught.value)


def _ledger_rounds(mission_id: str, root: Path, *rounds: int) -> None:
    from packages.orchestration.orchestrator_loop import LedgerEntry, append_ledger_entry

    for number in rounds:
        append_ledger_entry(PROJECT, mission_id, LedgerEntry(
            iteration=number, context_digest="d", move={"kind": "dispatch_job"},
            outcome={"status": "dispatched"}), root)


class TestAmendingAContract:
    """DECISION F269 D8 (2): the amend function."""

    def test_a_mission_with_no_contract_gets_one(self, tmp_path, mission):
        contract = amend_mission_contract(PROJECT, mission.id,
                                          "tests/test_login.py passes", root=tmp_path)

        assert contract.template is None
        assert [(c.id, c.origin) for c in contract.criteria] == [("C001", "amendment")]
        [amendment] = contract.amendments
        assert (amendment["id"], amendment["applies_from"], amendment["criteria"],
                amendment["acknowledged_in"]) == ("A001", 1, ["C001"], None)
        stored = read_mission_contract(load_mission(PROJECT, mission.id, tmp_path))
        assert stored == contract

    def test_the_criterion_is_an_amendment_compiled_with_the_next_free_id(
            self, tmp_path, mission):
        write_mission_contract(PROJECT, mission.id, _body(), tmp_path)

        contract = amend_mission_contract(PROJECT, mission.id,
                                          "tests/test_login.py passes", root=tmp_path)

        added = contract.criteria[-1]
        assert (added.id, added.origin, added.blocking, added.milestones) == (
            "C004", "amendment", True, ())
        assert added.text == "tests/test_login.py passes"
        assert added.check["id"] == "ctr-C004"
        assert added.check["spec"] == {"selector": "tests/test_login.py"}
        assert contract.amendments[0]["understood"] == (
            "adds blocking criterion C004: tests/test_login.py passes")

    def test_an_advisory_milestone_amendment_says_so(self, tmp_path, mission):
        contract = amend_mission_contract(PROJECT, mission.id, "the docs read well",
                                          milestones=("M1",), blocking=False,
                                          root=tmp_path)

        added = contract.criteria[-1]
        assert (added.blocking, added.milestones) == (False, ("M1",))
        assert contract.amendments[0]["understood"] == (
            "adds advisory criterion C001: the docs read well")

    def test_it_applies_from_the_missions_next_round(self, tmp_path, mission):
        _ledger_rounds(mission.id, tmp_path, 1, 2)

        contract = amend_mission_contract(PROJECT, mission.id, "it builds",
                                          root=tmp_path)

        assert contract.amendments[0]["applies_from"] == 3

    def test_a_second_amendment_leaves_the_first_byte_identical(self, tmp_path,
                                                                 mission):
        write_mission_contract(PROJECT, mission.id, _body(), tmp_path)
        amend_mission_contract(PROJECT, mission.id, "it builds", root=tmp_path)
        was = load_mission(PROJECT, mission.id, tmp_path).contract

        amend_mission_contract(PROJECT, mission.id, "tests/test_login.py passes",
                               root=tmp_path)

        body = load_mission(PROJECT, mission.id, tmp_path).contract
        assert [a["id"] for a in body["amendments"]] == ["A001", "A002"]
        assert body["amendments"][1]["criteria"] == ["C005"]
        assert json.dumps(body["criteria"][:4]) == json.dumps(was["criteria"])
        assert json.dumps(body["amendments"][0]) == json.dumps(was["amendments"][0])

    def test_a_replan_keeps_the_amendment_criterion_and_entry(self, tmp_path,
                                                              monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        m = create_mission(PROJECT, "Ship the tool")
        plan_mission(PROJECT, m.id, None)
        amended = amend_mission_contract(PROJECT, m.id, "tests/test_login.py passes")
        [criterion] = [c for c in amended.criteria if c.origin == "amendment"]

        plan_mission(PROJECT, m.id, None)

        contract = read_mission_contract(load_mission(PROJECT, m.id))
        assert [c for c in contract.criteria if c.origin == "amendment"] == [criterion]
        assert contract.amendments == amended.amendments


class TestTheRendererListsAmendments:
    """DECISION F269 D8 (5): amendments follow the criteria."""

    def test_each_amendment_shows_its_round_acknowledgement_and_criteria(self):
        body = _amended_body()
        body["amendments"].append(_amendment(id="A002", acknowledged_in=3))
        contract = MissionContract.from_json(body)

        lines = render_contract_lines("Contract of mission m1", contract.template,
                                      contract.criteria, contract.amendments)

        text = "\n".join(lines)
        assert text.index("C004") < text.index("Amendments: 2")
        assert ("    A001  applies from round 2  not yet acknowledged  adds C004"
                in lines)
        assert ("    A002  applies from round 2  acknowledged in round 3  adds C004"
                in lines)
        assert "          tests/test_login.py passes" in lines

    def test_no_amendments_prints_no_section(self):
        contract = MissionContract.from_json(_body())

        lines = render_contract_lines("t", contract.template, contract.criteria,
                                      contract.amendments)

        assert not any("Amendments" in line for line in lines)

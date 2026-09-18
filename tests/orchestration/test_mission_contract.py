"""F269 T001 — the contract record on the mission and the job's derived slice.

What DECISIONs F269 D2 and D3 require proof of:

  * a contract round-trips through the mission record unchanged;
  * every D2 rule is refused on WRITE and on READ of a body stored raw
    through ``set_mission_contract``, with an error naming the rule;
  * a job's slice is the whole-mission criteria plus its milestone's own, in
    contract order, and a job with no milestone gets the whole-mission
    criteria alone;
  * the milestone recorder writes onto an existing job record and writes
    nothing for a job that does not exist.

Every test writes into ``tmp_path``; no provider is called.
"""
from __future__ import annotations

import copy
from types import SimpleNamespace
from typing import Any

import pytest

from packages.orchestration.mission_contract import (
    JOB_MILESTONE_KEY,
    ContractCriterion,
    ContractError,
    MissionContract,
    job_contract_slice,
    read_job_milestone,
    read_mission_contract,
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

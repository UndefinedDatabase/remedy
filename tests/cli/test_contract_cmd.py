"""CLI tests: `remedy mission contract` and `remedy job contract` (F269 T001).

DECISION F269 D3 (3) is the contract under test: both commands are read-only,
render through one renderer and support `--json`; an id that matches nothing
exits 1; a mission with no contract, and a job in no mission, say so in one
sentence and exit 0 with `"contract": null`; a contract body that breaks a D2
rule exits 1 naming the rule.

Every test runs the real grouped CLI in a subprocess against a tmp_path data
root, through the helpers `tests/cli/test_mission_cmd.py` uses.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.cli.test_mission_cmd import REPO_ROOT, _make_project, _run, _start

#: One criterion for the whole mission, one for M1, one for M2.
CONTRACT = {
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
         "status": "open", "evidence_ref": None},
    ],
    "amendments": [],
}


def _py(data_root: Path, script: str) -> str:
    """Run a setup script against the data root; return its last output line."""
    proc = subprocess.run(
        [sys.executable, "-c", "import sys; sys.path.insert(0, '.');" + script],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
        env={**os.environ, "REMEDY_DATA_DIR": str(data_root)},
    )
    assert proc.returncode == 0, proc.stderr
    return proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""


def _store_contract(data_root: Path, project_id: str, mission_id: str,
                    body: dict) -> None:
    """Store a body RAW, through the storage call, so a broken one lands too."""
    _py(data_root,
        "import json;"
        "from packages.orchestration.mission_state import set_mission_contract;"
        f"set_mission_contract({project_id!r}, {mission_id!r}, "
        f"json.loads({json.dumps(body)!r}))")


def _job(data_root: Path, *, project_id: str | None = None,
         mission_id: str | None = None, milestone: str | None = None) -> str:
    """A job record; linked into the mission and given a milestone when asked."""
    script = ("from packages.orchestration.pingpong_job import JobPlan, save_job_plan;"
              "from packages.orchestration.mission_state import link_job_to_mission;"
              "from packages.orchestration.mission_contract import record_job_milestone;"
              "job = JobPlan(job_title='fixture'); save_job_plan(job);")
    if mission_id is not None:
        script += (f"link_job_to_mission({project_id!r}, {mission_id!r}, "
                   "str(job.job_id), 'initial');")
    if milestone is not None:
        script += f"assert record_job_milestone(str(job.job_id), {milestone!r});"
    return _py(data_root, script + "print(job.job_id)")


@pytest.fixture
def project(tmp_path: Path) -> tuple[Path, str]:
    data_root = tmp_path / "data"
    data_root.mkdir(parents=True)
    return data_root, _make_project(data_root, "Contract Test", "contract-test")


@pytest.fixture
def contracted(project) -> tuple[Path, str, str]:
    """A mission carrying the three-criterion contract."""
    data_root, project_id = project
    mission_id = _start(data_root, project_id, "Ship the tool")
    _store_contract(data_root, project_id, mission_id, CONTRACT)
    return data_root, project_id, mission_id


class TestTheMissionView:
    def test_every_criterion_is_rendered(self, contracted):
        data_root, project_id, mission_id = contracted

        out = _run(["mission", "contract", mission_id, "--project", project_id],
                   data_root).stdout

        assert f"Contract of mission {mission_id}" in out
        for cid in ("C001", "C002", "C003"):
            assert cid in out
        assert "Template: cli-tool" in out

    def test_json_carries_the_stored_body(self, contracted):
        data_root, project_id, mission_id = contracted

        body = json.loads(_run(["mission", "contract", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)

        assert body == {"version": 1, "mission_id": mission_id,
                        "contract": CONTRACT}

    def test_no_contract_is_one_sentence_and_null(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the tool")

        text = _run(["mission", "contract", mission_id, "--project", project_id],
                    data_root)
        body = json.loads(_run(["mission", "contract", mission_id, "--project",
                                project_id, "--json"], data_root).stdout)

        assert text.returncode == 0
        assert text.stdout.strip() == f"Mission {mission_id} has no contract yet."
        assert body["contract"] is None

    def test_an_unknown_mission_exits_1(self, project):
        data_root, project_id = project

        proc = _run(["mission", "contract", "0" * 32, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1

    def test_a_body_breaking_a_rule_exits_1_naming_it(self, project):
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the tool")
        broken = json.loads(json.dumps(CONTRACT))
        broken["criteria"][1]["origin"] = "operator"
        _store_contract(data_root, project_id, mission_id, broken)

        proc = _run(["mission", "contract", mission_id, "--project", project_id],
                    data_root, expect_ok=False)

        assert proc.returncode == 1
        assert "origin is template, planner or amendment" in proc.stderr


class TestTheMissionViewListsAmendments:
    """DECISION F269 D8 (5): `mission contract` shows each amendment."""

    @pytest.fixture
    def amended(self, project) -> tuple[Path, str, str, dict]:
        data_root, project_id = project
        mission_id = _start(data_root, project_id, "Ship the tool")
        body = json.loads(json.dumps(CONTRACT))
        body["criteria"].append(
            {"id": "C004", "text": "tests/test_login.py passes", "blocking": True,
             "origin": "amendment", "milestones": [], "check": None,
             "status": "open", "evidence_ref": None})
        body["amendments"] = [
            {"id": "A001", "text": "tests/test_login.py passes",
             "received_at": "2026-09-18T10:00:00+00:00", "applies_from": 2,
             "criteria": ["C004"],
             "understood": "adds blocking criterion C004: tests/test_login.py passes",
             "acknowledged_in": 2}]
        _store_contract(data_root, project_id, mission_id, body)
        return data_root, project_id, mission_id, body

    def test_text_lists_the_amendment_after_the_criteria(self, amended):
        data_root, project_id, mission_id, _body = amended

        out = _run(["mission", "contract", mission_id, "--project", project_id],
                   data_root).stdout

        assert "  Amendments: 1" in out
        assert ("    A001  applies from round 2  acknowledged in round 2  adds C004"
                in out)
        assert out.index("C004") < out.index("Amendments: 1")

    def test_json_carries_the_amendment(self, amended):
        data_root, project_id, mission_id, body = amended

        shown = json.loads(_run(["mission", "contract", mission_id, "--project",
                                 project_id, "--json"], data_root).stdout)

        assert shown["contract"] == body
        assert shown["contract"]["amendments"][0]["applies_from"] == 2


class TestTheJobView:
    def test_a_job_for_m1_renders_the_whole_mission_and_m1_criteria(
            self, contracted):
        data_root, project_id, mission_id = contracted
        job_id = _job(data_root, project_id=project_id, mission_id=mission_id,
                      milestone="M1")

        out = _run(["job", "contract", job_id], data_root).stdout

        assert "C001" in out
        assert "C002" in out
        assert "C003" not in out
        assert "milestone M1" in out

    def test_every_job_criterion_equals_the_mission_criterion_of_its_id(
            self, contracted):
        data_root, project_id, mission_id = contracted
        job_id = _job(data_root, project_id=project_id, mission_id=mission_id,
                      milestone="M1")

        job_body = json.loads(_run(["job", "contract", job_id, "--json"],
                                   data_root).stdout)
        mission_body = json.loads(_run(["mission", "contract", mission_id,
                                        "--project", project_id, "--json"],
                                       data_root).stdout)

        by_id = {c["id"]: c for c in mission_body["contract"]["criteria"]}
        criteria = job_body["contract"]["criteria"]
        assert [c["id"] for c in criteria] == ["C001", "C002"]
        for criterion in criteria:
            assert criterion == by_id[criterion["id"]]
        assert job_body["mission_id"] == mission_id
        assert job_body["milestone_id"] == "M1"
        assert job_body["contract"]["template"] == "cli-tool"

    def test_a_job_in_no_mission_is_one_sentence_and_null(self, project):
        data_root, _project_id = project
        job_id = _job(data_root)

        text = _run(["job", "contract", job_id], data_root)
        body = json.loads(_run(["job", "contract", job_id, "--json"],
                               data_root).stdout)

        assert text.returncode == 0
        assert text.stdout.strip() == (
            f"Job {job_id} belongs to no mission, so it has no contract.")
        assert body == {"version": 1, "job_id": job_id, "mission_id": None,
                        "milestone_id": None, "contract": None}

    def test_an_unknown_job_exits_1(self, project):
        data_root, _project_id = project

        proc = _run(["job", "contract", "0123456789abcdef"], data_root,
                    expect_ok=False)

        assert proc.returncode == 1


class TestTheCatalog:
    @pytest.mark.parametrize("command_id", ["mission.contract", "job.contract"])
    def test_both_commands_are_read_only_json_commands_with_handlers(
            self, command_id):
        from apps.cli.command_catalog import get_command
        from apps.cli.commands import collect_all_handlers

        entry = get_command(command_id)
        assert entry.action_class == "read_only"
        assert entry.supports_json is True
        assert entry.may_mutate_repo is False
        assert entry.may_execute_commands is False
        assert command_id in collect_all_handlers()

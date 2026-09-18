"""F269 T002 — `run_job` runs the job's DoD gate before its worktree goes (DECISION F269 D6 (2)).

The real `parse_job_file()` → `run_job()` path over a temporary git repository
with one committed file, the fake builder and reviewer (no provider is
called), and the data root under ``tmp_path``.  Each job's checks are
`custom_cmd` checks running ``python3 -c``, so a check's colour is fixed by
the test and not by a test suite:

  * a stored DoD whose BLOCKING check cannot pass blocks the job with
    ``dod_blocking_red:<id>`` and keeps its worktree;
  * a stored DoD whose only red check is non-blocking lets the job complete;
  * a job with no stored DoD completes as before and writes no gate result;
  * a job linked to a mission with a contract has its slice criteria's
    statuses and ``evidence_ref`` written after its run.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from packages.orchestration.dod_gate import load_gate_result, result_path, store_dod
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck
from packages.orchestration.mission_contract import (
    ContractCriterion,
    MissionContract,
    merge_contract_slice_into_dod,
    read_mission_contract,
    record_job_milestone,
    write_mission_contract,
)
from packages.orchestration.mission_state import (
    create_mission,
    link_job_to_mission,
    load_mission,
)
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    parse_job_file,
    run_job,
)

PROJECT = "p-f269-gate"

JOB_TEXT = """# One-task job

## Task 1 — write the readme

Write `docs/README.md`.
"""

PASSES = ["python3", "-c", "pass"]
FAILS = ["python3", "-c", "import sys; sys.exit(1)"]


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _check(check_id: str, argv: list[str], *, blocking: bool = True) -> DoDCheck:
    return DoDCheck(id=check_id, kind="custom_cmd", spec={"argv": argv},
                    blocking=blocking, source="plan_acceptance")


def _store(job_id: str, *checks: DoDCheck) -> None:
    store_dod(job_id, DoD(schema_v=DOD_SCHEMA_V, compiled=False,
                          origin="deterministic", checks=list(checks)))


def _job(repo: Path) -> str:
    return str(parse_job_file(JOB_TEXT, str(repo)).job_id)


def _run(job_id: str):
    return run_job(job_id, builder_name="fake", reviewer_name="fake")


class TestTheGateRunsInsideRunJob:
    def test_a_blocking_check_that_cannot_pass_blocks_the_job_and_keeps_its_worktree(
            self, repo):
        job_id = _job(repo)
        _store(job_id, _check("chk-green", PASSES), _check("chk-red", FAILS))

        done = _run(job_id)

        assert done.state == JOB_BLOCKED
        assert done.error == "dod_blocking_red:chk-red"
        assert done.worktree_cleanup_status == "retained"
        assert Path(done.job_workspace_path).is_dir()
        assert (Path(done.job_workspace_path) / "docs" / "README.md").is_file()
        result = load_gate_result(job_id)
        assert (result["released"], result["blocking_red"]) == (False, ["chk-red"])

    def test_a_job_whose_only_red_check_is_non_blocking_completes(self, repo):
        job_id = _job(repo)
        _store(job_id, _check("chk-green", PASSES),
               _check("chk-reported", FAILS, blocking=False))

        done = _run(job_id)

        assert done.state == JOB_COMPLETED
        assert done.error == ""
        assert done.worktree_cleanup_status == "clean"
        result = load_gate_result(job_id)
        assert (result["released"], result["reported_red"]) == (True, ["chk-reported"])

    def test_a_job_with_no_stored_dod_completes_and_writes_no_gate_result(self, repo):
        job_id = _job(repo)

        done = _run(job_id)

        assert done.state == JOB_COMPLETED
        assert done.error == ""
        assert done.worktree_cleanup_status == "clean"
        assert not result_path(job_id).exists()
        assert load_gate_result(job_id) is None


def _criterion(ident: str, argv: list[str], *milestones: str) -> ContractCriterion:
    """A criterion whose check is its own: the comment keeps every spec distinct,
    so the merge adds each one (it skips a check equal in kind and spec)."""
    return ContractCriterion(
        id=ident, text=f"criterion {ident}", origin="template",
        milestones=milestones,
        check=_check(f"ctr-{ident}", [*argv[:-1], f"{argv[-1]}  # {ident}"]
                     ).model_dump(mode="json"))


class TestTheGateDecidesTheJobsContractSlice:
    def test_the_slice_criteria_carry_the_gates_statuses_after_the_run(self, repo):
        mission = create_mission(PROJECT, "Ship the readme")
        write_mission_contract(PROJECT, mission.id, MissionContract(criteria=(
            _criterion("C001", PASSES),
            _criterion("C002", FAILS),
            _criterion("C003", PASSES, "M1"),
            _criterion("C004", PASSES, "M2"),
        )))
        job_id = _job(repo)
        linked = link_job_to_mission(PROJECT, mission.id, job_id, role="initial")
        assert record_job_milestone(job_id, "M1")
        assert merge_contract_slice_into_dod(linked, "M1", job_id) == 3

        done = _run(job_id)

        # C002 is whole-mission, so its red check is reported, not held on.
        assert done.state == JOB_COMPLETED
        contract = read_mission_contract(load_mission(PROJECT, mission.id))
        assert [(c.id, c.status, c.evidence_ref) for c in contract.criteria] == [
            ("C001", "met", f"{job_id}:ctr-C001"),
            ("C002", "unmet", f"{job_id}:ctr-C002"),
            ("C003", "met", f"{job_id}:ctr-C003"),
            ("C004", "open", None)]

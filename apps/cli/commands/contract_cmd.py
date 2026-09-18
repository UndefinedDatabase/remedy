"""`remedy mission contract` and `remedy job contract` — the two contract views (F269 T001).

A mission's contract is its acceptance criteria, stored on the mission record
in the shape DECISION F269 D2 rules; a job's contract is the slice of it the
job serves, derived from the milestone the job was dispatched for (DECISION
F269 D3).  Both commands are READ-ONLY and print through the one renderer,
``mission_contract.render_contract_lines``.

Exit codes, as D3 (3) rules them: an id that matches nothing exits 1; a mission
with no contract, and a job that belongs to no mission, print one sentence and
exit 0 (``"contract": null`` under ``--json``); a contract body that breaks a
D2 rule exits 1 naming the rule.
"""
from __future__ import annotations

import json as _json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse

EXIT_ERROR = 1


def _read_contract_or_exit(mission: Any) -> Any:
    """The mission's contract or None; a body breaking a D2 rule exits 1."""
    from packages.orchestration.mission_contract import (
        ContractError,
        read_mission_contract,
    )

    try:
        return read_mission_contract(mission)
    except ContractError as exc:
        print(f"Error: mission {mission.id}: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def _cmd_mission_contract(mission_id: str, *, project: str | None = None,
                          json_output: bool = False) -> None:
    """``remedy mission contract <id>`` — every criterion of one mission's contract."""
    from apps.cli.commands.mission_cmd import (
        _load_mission_or_exit,
        _resolve_project_id,
    )
    from packages.orchestration.mission_contract import render_contract_lines

    project_id = _resolve_project_id(project)
    mission = _load_mission_or_exit(project_id, mission_id)
    contract = _read_contract_or_exit(mission)

    if json_output:
        print(_json.dumps({"version": 1, "mission_id": mission.id,
                           "contract": (contract.to_json()
                                        if contract is not None else None)},
                          sort_keys=True))
        return
    if contract is None:
        print(f"Mission {mission.id} has no contract yet.")
        return
    for line in render_contract_lines(f"Contract of mission {mission.id}",
                                      contract.template, contract.criteria):
        print(line)


def _cmd_job_contract(job_id_str: str, *, json_output: bool = False) -> None:
    """``remedy job contract <id>`` — the slice of its mission's contract a job serves."""
    from packages.orchestration.data_paths import resolve_job_id
    from packages.orchestration.mission_contract import (
        job_contract_slice,
        read_job_milestone,
        render_contract_lines,
    )
    from packages.orchestration.mission_state import mission_for_job
    from packages.orchestration.pingpong_job import (
        JobNotFoundError,
        JobStoreError,
        require_job_plan,
    )

    job_id = resolve_job_id(job_id_str)
    try:
        require_job_plan(job_id)
    except (JobNotFoundError, JobStoreError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    milestone_id = read_job_milestone(job_id)
    mission = mission_for_job(job_id)
    contract = _read_contract_or_exit(mission) if mission is not None else None
    criteria = (job_contract_slice(contract, milestone_id)
                if contract is not None else ())

    if json_output:
        print(_json.dumps({
            "version": 1,
            "job_id": job_id,
            "mission_id": mission.id if mission is not None else None,
            "milestone_id": milestone_id,
            "contract": ({"template": contract.template,
                          "criteria": [c.to_json() for c in criteria]}
                         if contract is not None else None),
        }, sort_keys=True))
        return
    if mission is None:
        print(f"Job {job_id} belongs to no mission, so it has no contract.")
        return
    if contract is None:
        print(f"Job {job_id} belongs to mission {mission.id}, which has no "
              f"contract yet.")
        return
    title = (f"Contract of job {job_id} (mission {mission.id}, milestone "
             f"{milestone_id or 'none'})")
    for line in render_contract_lines(title, contract.template, criteria):
        print(line)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "mission.contract": lambda args: _cmd_mission_contract(
        args.mission_id,
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
    ),
    "job.contract": lambda args: _cmd_job_contract(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
}

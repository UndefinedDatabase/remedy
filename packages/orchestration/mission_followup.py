"""A mission's follow-up job: the one work task a step asks for, and the job that carries it.

Moved unchanged out of `packages/orchestration/mission_state.py` as step (2) of that file's
boundary on `docs/system/structure-ledger-v1.md` (F297, DECISION F297 D7), so the follow-up
path can change without growing a file at its limit. `mission_state` imports every name back by
name, so `from packages.orchestration.mission_state import continue_mission` keeps working; the
store's functions are imported inside `continue_mission`, because `mission_state` imports this
module at its end.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import normalize_job_id
from packages.orchestration.mission_record import (
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    MissionError,
    follow_up_target,
)

MISSION_FOLLOW_UP_TASK_TYPE = "mission_follow_up"


def build_follow_up_task(next_step: str) -> Any:
    """The single work task a ``mission continue`` step asks for.

    Deliberately ONE task: planning a follow-up into a DAG is the planner's
    job, not this module's.  What this module owns is that whatever the plan
    turns out to be, verification comes first.
    """
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import TaskEntry

    return TaskEntry(
        title=str(next_step).strip(),
        inputs={"task_type": MISSION_FOLLOW_UP_TASK_TYPE},
        status=RunState.PENDING,
    )


def continue_mission(project_id: str, mission_id: str, next_step: str, *,
                     now: datetime | None = None,
                     root: Path | None = None) -> Any:
    """Create the next job in a mission's chain and link it.

    With a previous job in the chain, the new job's plan is built verify-first
    and then validated as such: the injected verify task is task 0 and the work
    declares it as a dependency, so ``dag_schedule.ready_set`` withholds the
    work until the verification has COMPLETED.

    On an empty mission there is nothing to verify yet, so this creates the
    ``initial`` job with the work alone — an honest plan, not a verify task
    pointed at a job that does not exist. On a mission over several projects
    the job works in the previous job's project and repository (DECISION F205 D5).
    """
    from packages.core.models import RunState
    from packages.orchestration.mission_state import (
        assert_verify_first,
        inject_verify_first,
        link_job_to_mission,
        load_mission,
    )
    from packages.orchestration.pingpong_job import (
        JobNotFoundError,
        JobPlan,
        JobStoreError,
        require_job_plan,
        save_job_plan,
    )

    text = str(next_step).strip()
    if not text:
        raise MissionError("a follow-up needs a step to take")

    mission = load_mission(project_id, mission_id, root)
    previous = mission.latest_link()

    work = build_follow_up_task(text)
    previous_job = None
    if previous is None:
        tasks = [work]
        role = MISSION_ROLE_INITIAL
    else:
        try:
            previous_job = require_job_plan(normalize_job_id(previous.job_id))
        except (ValueError, JobNotFoundError) as exc:
            raise MissionError(
                f"the previous job {previous.job_id} is gone, so its Definition "
                f"of Done cannot be verified — a follow-up would be starting "
                f"blind") from exc
        except JobStoreError as exc:
            raise MissionError(
                f"the previous job {previous.job_id} cannot be read, so its "
                f"Definition of Done cannot be verified: {exc}") from exc
        tasks = inject_verify_first(previous_job, [work])
        role = MISSION_ROLE_FOLLOW_UP

    # Built verify-first above; CHECKED here, so the rule cannot be skipped by
    # a future caller that assembles the plan some other way.
    if role == MISSION_ROLE_FOLLOW_UP:
        assert_verify_first(tasks)

    job = JobPlan(
        job_title=text[:80],
        mission=mission.goal,
        user_prompt=text,
        **{"project_id": str(mission.project_id), **follow_up_target(mission, previous_job)},
        tasks=tasks,
        state=RunState.PLANNED,
        metadata={"mission_id": mission.id, "mission_role": role},
    )
    save_job_plan(job)
    link_job_to_mission(project_id, mission.id, str(job.job_id), role, now=now,
                        root=root)
    return job

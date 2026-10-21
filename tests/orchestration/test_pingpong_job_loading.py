"""The two job loaders of `packages/orchestration/pingpong_job.py` on a damaged record (R-1413)."""

from __future__ import annotations

import json

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_record_path
from packages.orchestration.pingpong_job import JobPlan, load_job_plan_safe, save_job_plan


@pytest.mark.parametrize("tasks", ["not a list", [1], [None]])
def test_the_safe_loader_answers_a_task_list_of_the_wrong_shape_as_damaged(tasks):
    """R-1413, DECISION F307 D8: its docstring says no input makes it raise, and now none does."""
    job = JobPlan(job_title="t", mission="m", user_prompt="m", state=RunState.PLANNED)
    save_job_plan(job)
    path = job_record_path(str(job.job_id))
    record = json.loads(path.read_text())
    record["tasks"] = tasks
    path.write_text(json.dumps(record))

    assert load_job_plan_safe(str(job.job_id)) == (None, True)

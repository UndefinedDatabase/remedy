"""F203 T001 — the failed link to a project is a warning record, not a bare print (DECISION F203 D3).

A parent job whose `project_id` is not a UUID cannot be linked; `continue_from_node` still
answers and saves the child, and the failure is one WARNING record that the terminal shows bare
and the operations log keeps.
"""
from __future__ import annotations

import logging
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.continue_from_node import ContinueResult, continue_from_node
from packages.orchestration.data_paths import mint_job_id, normalize_job_id
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, load_job_plan, save_job_plan
from packages.orchestration.project_brain import build_project_brain
from packages.orchestration.structured_log import (
    LOG_FILE_NAME,
    configure_structured_logging,
    reset_structured_logging,
)

LOGGER_NAME = "packages.orchestration.continue_from_node"
LINK_FAILURE = "WARNING: could not link child job to project not-a-uu"


@pytest.fixture(autouse=True)
def _clean_logging():
    reset_structured_logging()
    yield
    reset_structured_logging()


def _parent_with_bad_project(data_dir: Path) -> JobPlan:
    parent = JobPlan(
        job_id=mint_job_id(),
        job_title="continue-test",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            TaskEntry(
                task_id="T001",
                title="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata={"target_repo": str(data_dir)},
        project_id="not-a-uuid",
    )
    save_job_plan(parent)
    return parent


def _continue(parent: JobPlan) -> ContinueResult:
    graph = build_project_brain(parent, [])
    return continue_from_node(parent, graph, graph.nodes[0].id, "child task")


def test_a_failed_link_still_answers_saves_the_child_and_leaves_one_warning(
    tmp_path, monkeypatch, caplog,
):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    parent = _parent_with_bad_project(tmp_path)
    with caplog.at_level(logging.WARNING):
        result = _continue(parent)

    assert isinstance(result, ContinueResult)
    assert load_job_plan(normalize_job_id(result.child_job_id)).user_prompt == "child task"
    records = [r for r in caplog.records if r.levelno >= logging.WARNING]
    assert len(records) == 1
    assert records[0].name == LOGGER_NAME
    assert records[0].getMessage().startswith(LINK_FAILURE)


def test_the_warning_is_in_the_operations_log_and_bare_on_the_error_stream(
    tmp_path, monkeypatch, capsys,
):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    parent = _parent_with_bad_project(tmp_path)
    root = tmp_path / "data"
    path = configure_structured_logging(root)
    capsys.readouterr()
    _continue(parent)
    for handler in logging.getLogger().handlers:
        handler.flush()

    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if LINK_FAILURE in line]
    assert len(lines) == 1
    assert " WARNING " in lines[0]
    assert path.name == LOG_FILE_NAME
    err_lines = [line for line in capsys.readouterr().err.splitlines() if line.strip()]
    assert len(err_lines) == 1
    assert err_lines[0].startswith(LINK_FAILURE)

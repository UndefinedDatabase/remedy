"""CLI tests for `context inspect` command.

Tests:
- Command catalog entry exists with correct args
- Handler dispatches correctly
- JSON output has required structure
- Text output bounded, no traceback
- Invalid job ID safe
- Invalid task ID safe
- Missing job safe
"""

from __future__ import annotations

import json
from unittest.mock import patch
from uuid import uuid4

import pytest

from packages.core.models import Job, Task


# ---------------------------------------------------------------------------
# Catalog tests
# ---------------------------------------------------------------------------


def test_context_inspect_in_catalog():
    from apps.cli.command_catalog import CATALOG
    cmds = {c.command_id: c for c in CATALOG}
    assert "context.inspect" in cmds
    entry = cmds["context.inspect"]
    assert entry.group_id == "context"
    assert entry.supports_json is True
    arg_names = [a.name for a in entry.args]
    assert "job_id" in arg_names
    assert "task_id" in arg_names
    assert "--json" in arg_names
    assert "--budget" in arg_names


def test_context_inspect_related_commands():
    from apps.cli.command_catalog import CATALOG
    cmds = {c.command_id: c for c in CATALOG}
    entry = cmds["context.inspect"]
    assert "context.pack" in entry.related


# ---------------------------------------------------------------------------
# Handler tests
# ---------------------------------------------------------------------------


def _make_test_job():
    task = Task(description="Fix auth bug")
    job = Job(name="test-job", user_prompt="Fix the bug")
    job.tasks = [task]
    return job, task


def test_handler_text_output(capsys):
    from apps.cli.commands.context import _cmd_context_inspect
    job, task = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
         patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_context_inspect(job_id)

    out = capsys.readouterr().out
    assert "Context Inspection" in out
    assert "Readiness:" in out


def test_handler_json_output(capsys):
    from apps.cli.commands.context import _cmd_context_inspect
    job, task = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
         patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_context_inspect(job_id, json_output=True)

    data = json.loads(capsys.readouterr().out)
    assert data["version"] == 1
    assert "included_paths" in data
    assert "excluded_paths" in data
    assert "budget" in data
    assert "policy_gates" in data
    assert "readiness" in data
    assert "tooling" in data


def test_handler_json_with_task_id(capsys):
    from apps.cli.commands.context import _cmd_context_inspect
    job, task = _make_test_job()
    job_id = str(job.id)
    task_id = str(task.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
         patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_context_inspect(job_id, task_id=task_id, json_output=True)

    data = json.loads(capsys.readouterr().out)
    assert data["task_id"] == task_id


def test_handler_invalid_job_id():
    from apps.cli.commands.context import _cmd_context_inspect
    with pytest.raises(SystemExit) as exc_info:
        _cmd_context_inspect("not-a-uuid")
    assert exc_info.value.code == 1


def test_handler_invalid_task_id():
    from apps.cli.commands.context import _cmd_context_inspect
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         pytest.raises(SystemExit) as exc_info:
        _cmd_context_inspect(job_id, task_id="not-a-uuid")
    assert exc_info.value.code == 1


def test_handler_no_traceback(capsys):
    from apps.cli.commands.context import _cmd_context_inspect
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
         patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_context_inspect(job_id)

    out = capsys.readouterr()
    assert "Traceback" not in out.out
    assert "Traceback" not in out.err


def test_handler_output_bounded(capsys):
    from apps.cli.commands.context import _cmd_context_inspect
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.context.load_job", return_value=job), \
         patch("packages.orchestration.context_inspector._resolve_repo_root", return_value=None), \
         patch("packages.orchestration.data_paths.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_context_inspect(job_id)

    out = capsys.readouterr().out
    assert len(out) < 10000


# ---------------------------------------------------------------------------
# Handler dispatch
# ---------------------------------------------------------------------------


def test_context_inspect_in_handlers():
    from apps.cli.commands.context import COMMAND_HANDLERS
    assert "context.inspect" in COMMAND_HANDLERS

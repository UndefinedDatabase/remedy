"""CLI tests for `change proof` command.

Tests:
- Command catalog entry exists with correct args
- Handler dispatches to proof chain builder
- Path traversal rejection
- JSON output mode
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.approval_queue import make_intent_id


# ---------------------------------------------------------------------------
# Catalog tests
# ---------------------------------------------------------------------------


def test_change_proof_in_catalog():
    from apps.cli.command_catalog import CATALOG
    cmds = {c.command_id: c for c in CATALOG}
    assert "change.proof" in cmds
    entry = cmds["change.proof"]
    assert entry.group_id == "change"
    assert entry.supports_json is True
    arg_names = [a.name for a in entry.args]
    assert "job_id" in arg_names
    assert "--path" in arg_names
    assert "--json" in arg_names


def test_change_proof_related_commands():
    from apps.cli.command_catalog import CATALOG
    cmds = {c.command_id: c for c in CATALOG}
    entry = cmds["change.proof"]
    assert "change.list" in entry.related
    assert "file.why" in entry.related


# ---------------------------------------------------------------------------
# Handler tests
# ---------------------------------------------------------------------------


def _make_test_job():
    task = Task(description="Fix auth bug")
    explanations = [{"file": "src/auth.py", "action": "modify", "risk": "medium", "reason": "", "summary": ""}]
    art = Artifact(
        name="patch-intent", content="", kind=ArtifactKind.PATCH_INTENT,
        task_id=task.id,
        metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
    )
    intent_id = make_intent_id(art.id, 0)
    approvals = {intent_id: {"state": "approved", "decided_at": "", "decided_by": ""}}
    art.metadata["patch_intent_approvals"] = approvals
    job = Job(name="test-job", user_prompt="Fix the bug")
    job.tasks = [task]
    job.artifacts = [art]
    return job, intent_id


def test_handler_text_output(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id)

    out = capsys.readouterr().out
    assert "Proof Chain" in out
    assert "incomplete" in out.lower()


def test_handler_json_output(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id, json_output=True)

    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["version"] == 1
    assert "overall_status" in data
    assert "changes" in data


def test_handler_path_filter(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id, path="src/auth.py", json_output=True)

    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["path_filter"] == "src/auth.py"


def test_handler_path_traversal_rejected():
    from apps.cli.commands.change import _cmd_change_proof
    job_id = str(uuid4())

    with patch("apps.cli.commands.change.load_job"), \
         pytest.raises(SystemExit) as exc_info:
        _cmd_change_proof(job_id, path="../etc/passwd")

    assert exc_info.value.code == 1


def test_handler_absolute_path_rejected():
    from apps.cli.commands.change import _cmd_change_proof
    job_id = str(uuid4())

    with patch("apps.cli.commands.change.load_job"), \
         pytest.raises(SystemExit) as exc_info:
        _cmd_change_proof(job_id, path="/etc/passwd")

    assert exc_info.value.code == 1


def test_handler_invalid_job_id():
    from apps.cli.commands.change import _cmd_change_proof

    with pytest.raises(SystemExit) as exc_info:
        _cmd_change_proof("not-a-uuid")

    assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# Handler dispatch in COMMAND_HANDLERS
# ---------------------------------------------------------------------------


def test_change_proof_in_handlers():
    from apps.cli.commands.change import COMMAND_HANDLERS
    assert "change.proof" in COMMAND_HANDLERS

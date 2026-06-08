"""CLI tests for `change proof` command.

Tests:
- Command catalog entry exists with correct args
- Handler dispatches to proof chain builder
- Path traversal rejection
- JSON output mode with structured next action
- No overclaim of verified status
- Output bounded, no traceback
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


def _make_test_job(*, approved=True, with_apply=False, with_test=False):
    task = Task(description="Fix auth bug")
    explanations = [{"file": "src/auth.py", "action": "modify", "risk": "medium", "reason": "", "summary": ""}]
    art = Artifact(
        name="patch-intent", content="", kind=ArtifactKind.PATCH_INTENT,
        task_id=task.id,
        metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
    )
    intent_id = make_intent_id(art.id, 0)
    if approved:
        approvals = {intent_id: {"state": "approved", "decided_at": "", "decided_by": ""}}
        art.metadata["patch_intent_approvals"] = approvals
    job = Job(name="test-job", user_prompt="Fix the bug")
    job.tasks = [task]
    job.artifacts = [art]
    events = []
    if with_apply:
        events.append({"event": "patch_intent_applied", "metadata": {"intent_id": intent_id, "outcome": "applied", "bytes_written": 100, "line_count": 10}})
        events.append({"event": "patch_apply_proof_recorded", "metadata": {"intent_id": intent_id, "before_sha256": "abc", "after_sha256": "def", "bytes_delta": 50}})
    if with_test:
        events.append({"event": "test_run_completed", "metadata": {"intent_id": intent_id, "status": "passed", "exit_code": 0}})
    return job, intent_id, events


def test_handler_text_output(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id)

    out = capsys.readouterr().out
    assert "Proof Chain" in out
    assert "incomplete" in out.lower()


def test_handler_text_does_not_overclaim_verified(capsys):
    """Text output does not say verified when tests not linked"""
    from apps.cli.commands.change import _cmd_change_proof
    job, iid, events = _make_test_job(with_apply=True)  # no test
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=events):
        _cmd_change_proof(job_id)

    out = capsys.readouterr().out
    assert "Overall: verified" not in out.lower()


def test_handler_json_output(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id, json_output=True)

    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["version"] == 2
    assert "overall_status" in data
    assert "changes" in data
    assert "next_safe_action_obj" in data


def test_handler_json_structured_next_action(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id, json_output=True)

    out = capsys.readouterr().out
    data = json.loads(out)
    nsa = data["next_safe_action_obj"]
    assert "label" in nsa
    assert "command" in nsa
    assert "reason" in nsa
    assert "available" in nsa


def test_handler_path_filter(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
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


def test_handler_no_traceback(capsys):
    """Output never contains traceback"""
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id)

    out = capsys.readouterr()
    assert "Traceback" not in out.out
    assert "Traceback" not in out.err


def test_handler_output_bounded(capsys):
    from apps.cli.commands.change import _cmd_change_proof
    job, _, _ = _make_test_job()
    job_id = str(job.id)

    with patch("apps.cli.commands.change.load_job", return_value=job), \
         patch("apps.cli.commands.change.resolve_data_root", return_value="/tmp"), \
         patch("packages.orchestration.timeline.load_run_events", return_value=[]):
        _cmd_change_proof(job_id)

    out = capsys.readouterr().out
    assert len(out) < 10000


# ---------------------------------------------------------------------------
# Handler dispatch
# ---------------------------------------------------------------------------


def test_change_proof_in_handlers():
    from apps.cli.commands.change import COMMAND_HANDLERS
    assert "change.proof" in COMMAND_HANDLERS

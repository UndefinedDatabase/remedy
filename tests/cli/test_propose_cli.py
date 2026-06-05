"""Contract tests for propose CLI handlers — every catalog command must have a handler."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from apps.cli.command_catalog import CATALOG, get_commands_for_group
from apps.cli.commands import collect_all_handlers
from packages.orchestration.proposed_tasks import (
    ProposedTask,
    ProposedTaskStatus,
    add_proposed_task,
    save_proposed_tasks,
)


@pytest.fixture
def tmp_store(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "packages.orchestration.proposed_tasks._STORE_DIR",
        tmp_path / "proposed_tasks",
    )
    return tmp_path


JOB_ID = "cli-test-job"


class TestCatalogHandlerCoverage:
    def test_all_propose_commands_have_handlers(self):
        handlers = collect_all_handlers()
        propose_cmds = get_commands_for_group("propose")
        assert len(propose_cmds) == 6
        for cmd in propose_cmds:
            assert cmd.command_id in handlers, f"Missing handler for {cmd.command_id}"

    def test_propose_group_exists_in_catalog(self):
        ids = {cmd.command_id for cmd in CATALOG if cmd.group_id == "propose"}
        expected = {"propose.list", "propose.show", "propose.evaluate", "propose.approve", "propose.reject", "propose.defer"}
        assert ids == expected


class TestProposeListHandler:
    def test_list_empty_job(self, tmp_store, capsys):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=False)
        handlers["propose.list"](args)
        assert "No proposed tasks" in capsys.readouterr().out

    def test_list_json_empty(self, tmp_store, capsys):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=True)
        handlers["propose.list"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["count"] == 0
        assert data["tasks"] == []

    def test_list_with_tasks(self, tmp_store, capsys):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", status=ProposedTaskStatus.APPROVED_FOR_BUILD))
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=True)
        handlers["propose.list"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["count"] == 2

    def test_list_filter_by_status(self, tmp_store, capsys):
        add_proposed_task(JOB_ID, ProposedTask(title="A"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", status=ProposedTaskStatus.REJECTED))
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status="proposed", json=True)
        handlers["propose.list"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["count"] == 1

    def test_list_invalid_status(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status="bogus", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)


class TestProposeShowHandler:
    def test_show_existing(self, tmp_store, capsys):
        t = ProposedTask(title="Show me")
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, json=True)
        handlers["propose.show"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["task"]["title"] == "Show me"

    def test_show_missing(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nonexistent", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.show"](args)


class TestProposeEvaluateHandler:
    def test_evaluate_all(self, tmp_store, capsys):
        add_proposed_task(JOB_ID, ProposedTask(title="A", risk="medium"))
        add_proposed_task(JOB_ID, ProposedTask(title="B", risk="medium"))
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=None, json=True)
        handlers["propose.evaluate"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["evaluated_count"] == 2

    def test_evaluate_single(self, tmp_store, capsys):
        t = ProposedTask(title="One", risk="high")
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, json=True)
        handlers["propose.evaluate"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["tasks"][0]["status"] == "evaluated"

    def test_evaluate_missing_task(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nope", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.evaluate"](args)


class TestProposeApproveHandler:
    def test_approve(self, tmp_store, capsys):
        t = ProposedTask(title="Approve me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, json=True)
        handlers["propose.approve"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["approved"] is True

    def test_approve_missing(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nope", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.approve"](args)

    def test_approve_rejected_fails(self, tmp_store):
        t = ProposedTask(title="X", status=ProposedTaskStatus.REJECTED)
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, json=False)
        with pytest.raises(SystemExit):
            handlers["propose.approve"](args)


class TestProposeRejectHandler:
    def test_reject(self, tmp_store, capsys):
        t = ProposedTask(title="Reject me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, reason="bad", json=True)
        handlers["propose.reject"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["rejected"] is True

    def test_reject_missing(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nope", reason="", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.reject"](args)


class TestProposeDeferHandler:
    def test_defer(self, tmp_store, capsys):
        t = ProposedTask(title="Defer me", status=ProposedTaskStatus.EVALUATED)
        add_proposed_task(JOB_ID, t)
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id=t.id, reason="later", json=True)
        handlers["propose.defer"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["deferred"] is True

    def test_defer_missing(self, tmp_store):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nope", reason="", json=False)
        with pytest.raises(SystemExit):
            handlers["propose.defer"](args)


class TestCorruptStoreHandling:
    def test_list_corrupt_store(self, tmp_store, capsys):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("corrupt")
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status=None, json=True)
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["degraded"] is True

    def test_show_corrupt_store(self, tmp_store, capsys):
        path = tmp_store / "proposed_tasks"
        path.mkdir(parents=True, exist_ok=True)
        (path / f"{JOB_ID}.json").write_text("corrupt")
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="any", json=True)
        with pytest.raises(SystemExit):
            handlers["propose.show"](args)
        data = json.loads(capsys.readouterr().out)
        assert data["degraded"] is True


class TestNoTraceback:
    def test_missing_task_no_traceback(self, tmp_store, capsys):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, task_id="nope", json=True)
        with pytest.raises(SystemExit):
            handlers["propose.show"](args)
        out = capsys.readouterr().out
        assert "Traceback" not in out
        data = json.loads(out)
        assert "error" in data

    def test_invalid_status_no_traceback(self, tmp_store, capsys):
        handlers = collect_all_handlers()
        args = SimpleNamespace(job_id=JOB_ID, status="fake", json=True)
        with pytest.raises(SystemExit):
            handlers["propose.list"](args)
        out = capsys.readouterr().out
        assert "Traceback" not in out

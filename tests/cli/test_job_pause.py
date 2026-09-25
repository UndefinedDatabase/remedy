"""F025 T002 — `remedy job pause` / `remedy job unpause`, DECISION F025 D2.

Neither command starts or kills anything: `job.pause` writes a durable
control entry the runner's own safe points read (round 3's `run_cycles`
wiring), and `job.unpause` reads one back, releases it, or reports the
relaunch command for a job an operator pause already parked. This file
proves the CLI's half of D2 — the same effects the write door shares
(`packages/orchestration/pause_control.py`) — through the handler
functions directly and through the real argv dispatcher.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_commands_for_group
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import job_pause_cmd as CMD
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    _persist_job,
    parse_job_file,
)
from packages.orchestration.timeline import load_run_events

_THREE_TASK_JOB = """\
# Job: CLI Pause Test

## Task 1
Do the first thing.

Acceptance:
- it is done

## Task 2
Do the second thing.

Acceptance:
- it is done

## Task 3
Do the third thing.

Acceptance:
- it is done
"""


@pytest.fixture
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def job(data_root, tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    return parse_job_file(_THREE_TASK_JOB, str(repo))


def _task_paused_events(data_root, job_id):
    return [e for e in load_run_events(data_root, job_id) if e["event"] == "task_paused"]


def _task_resumed_events(data_root, job_id):
    return [e for e in load_run_events(data_root, job_id) if e["event"] == "task_resumed"]


class TestJobScopePause:
    def test_it_requests_a_pause_and_says_what_will_happen(self, job, capsys):
        CMD._cmd_job_pause(job.job_id, reason="operator requested pause")

        out = capsys.readouterr().out
        assert "Pause requested — it will take effect at the next safe point." in out
        assert job.job_id in out

    def test_json_output_carries_the_requested_outcome(self, job, capsys):
        CMD._cmd_job_pause(job.job_id, reason="pausing", source="ui", json_output=True)

        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is True and payload["job_id"] == job.job_id
        assert payload["outcome"] == "requested"
        assert payload["scope"] == "job"
        assert payload["request_id"]

    def test_a_second_pause_request_is_idempotent(self, job, capsys):
        CMD._cmd_job_pause(job.job_id, reason="first", json_output=True)
        first = json.loads(capsys.readouterr().out)["request_id"]
        CMD._cmd_job_pause(job.job_id, reason="second", json_output=True)
        second = json.loads(capsys.readouterr().out)["request_id"]

        assert first == second

    def test_a_completed_job_is_refused_with_its_state_named(self, job, capsys):
        job.state = JOB_COMPLETED
        _persist_job(job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause(job.job_id)
        assert exc.value.code == 1
        assert "completed" in capsys.readouterr().err

    def test_a_completed_job_says_so_in_json_too(self, job, capsys):
        job.state = JOB_COMPLETED
        _persist_job(job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause(job.job_id, json_output=True)
        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is False
        assert payload["error"] == "job_not_pausable"
        assert payload["reason"] == "completed"
        assert payload["job_id"] == job.job_id


class TestJobScopeUnpause:
    def test_withdraws_a_pending_pause(self, job, capsys):
        CMD._cmd_job_pause(job.job_id, reason="x", json_output=True)
        capsys.readouterr()

        CMD._cmd_job_unpause(job.job_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["outcome"] == "withdrawn"
        assert payload["request_id"]

    def test_nothing_pending_answers_not_paused(self, job, capsys):
        CMD._cmd_job_unpause(job.job_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["outcome"] == "not_paused"

    def test_human_withdraw_line(self, job, capsys):
        CMD._cmd_job_pause(job.job_id, reason="x")
        capsys.readouterr()
        CMD._cmd_job_unpause(job.job_id)
        out = capsys.readouterr().out
        assert "Pause request withdrawn" in out

    def test_a_parked_job_answers_parked_with_the_relaunch_command(self, job, capsys):
        """A job an operator pause already saved to disk is not withdrawn — the
        door and the CLI alike may start no process, so they name the command
        that does (operator question Q4)."""
        from packages.orchestration.pingpong_job import JOB_PAUSED

        job.state = JOB_PAUSED
        job.pause = {"scope": "job", "request_id": "req-parked"}
        _persist_job(job)

        CMD._cmd_job_unpause(job.job_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["outcome"] == "parked"
        assert payload["next"] == f"remedy job run {job.job_id}"

    def test_a_completed_job_is_refused_with_its_state_named(self, job, capsys):
        job.state = JOB_COMPLETED
        _persist_job(job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_unpause(job.job_id, json_output=True)
        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"] == "job_not_unpausable"
        assert payload["reason"] == "completed"


class TestTaskScopePause:
    def test_pausing_a_task_writes_one_task_paused_event(self, job, data_root, capsys):
        task_id = job.tasks[2].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id, reason="hold task 3", json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["outcome"] == "paused"
        assert payload["scope"] == "task"
        assert payload["task_id"] == task_id
        events = _task_paused_events(data_root, job.job_id)
        assert len(events) == 1
        assert events[0]["task_id"] == task_id
        assert events[0]["metadata"]["request_id"] == payload["request_id"]

    def test_pausing_the_same_task_twice_writes_the_event_exactly_once(
            self, job, data_root, capsys):
        task_id = job.tasks[1].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id, json_output=True)
        capsys.readouterr()
        CMD._cmd_job_pause(job.job_id, task=task_id, json_output=True)
        second = json.loads(capsys.readouterr().out)

        assert second["outcome"] == "paused"
        assert len(_task_paused_events(data_root, job.job_id)) == 1

    def test_human_task_pause_line_names_the_task(self, job, capsys):
        task_id = job.tasks[0].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id)
        out = capsys.readouterr().out
        assert "Task pause requested — it will take effect at the next safe point." in out
        assert task_id in out

    def test_an_unknown_task_is_refused_with_the_task_named(self, job, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause(job.job_id, task="not-a-real-task", json_output=True)
        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"] == "job_not_pausable"
        assert "not-a-real-task" in payload["reason"]
        assert payload["task_id"] == "not-a-real-task"

    def test_an_unknown_task_is_refused_without_json_too(self, job, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause(job.job_id, task="not-a-real-task")
        assert exc.value.code == 1
        assert "not-a-real-task" in capsys.readouterr().err


class TestTaskScopeUnpause:
    def test_releasing_a_paused_task_writes_one_task_resumed_event(
            self, job, data_root, capsys):
        task_id = job.tasks[0].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id, json_output=True)
        capsys.readouterr()

        CMD._cmd_job_unpause(job.job_id, task=task_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["outcome"] == "released"
        assert payload["task_id"] == task_id
        events = _task_resumed_events(data_root, job.job_id)
        assert len(events) == 1
        assert events[0]["task_id"] == task_id
        assert events[0]["metadata"]["request_id"] == payload["request_id"]

    def test_releasing_an_unpaused_task_answers_not_paused_and_writes_nothing(
            self, job, data_root, capsys):
        task_id = job.tasks[0].task_id
        CMD._cmd_job_unpause(job.job_id, task=task_id, json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["outcome"] == "not_paused"
        assert _task_resumed_events(data_root, job.job_id) == []

    def test_releasing_twice_writes_the_event_exactly_once(self, job, data_root, capsys):
        task_id = job.tasks[0].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id, json_output=True)
        capsys.readouterr()
        CMD._cmd_job_unpause(job.job_id, task=task_id, json_output=True)
        capsys.readouterr()
        CMD._cmd_job_unpause(job.job_id, task=task_id, json_output=True)
        second = json.loads(capsys.readouterr().out)

        assert second["outcome"] == "not_paused"
        assert len(_task_resumed_events(data_root, job.job_id)) == 1

    def test_an_unknown_task_is_refused_with_the_task_named(self, job, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_unpause(job.job_id, task="not-a-real-task", json_output=True)
        assert exc.value.code == 1
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"] == "job_not_unpausable"
        assert "not-a-real-task" in payload["reason"]

    def test_human_release_line_names_the_task(self, job, capsys):
        task_id = job.tasks[0].task_id
        CMD._cmd_job_pause(job.job_id, task=task_id)
        capsys.readouterr()
        CMD._cmd_job_unpause(job.job_id, task=task_id)
        out = capsys.readouterr().out
        assert f"Task {task_id} resumed." in out


class TestItRefusesToLie:
    def test_an_unknown_job_pause_exits_3(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause("0123456789abcdef")
        assert exc.value.code == 3
        assert capsys.readouterr().err == "Error: No job matches '0123456789abcdef'. Try: remedy job list.\n"

    def test_an_unknown_job_pause_exits_3_in_json_mode_too(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause("0123456789abcdef", json_output=True)
        assert exc.value.code == 3
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["error"] == "job_not_found"
        assert body["schema_version"] == 1

    def test_an_unknown_job_unpause_exits_3(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_unpause("0123456789abcdef")
        assert exc.value.code == 3

    @pytest.mark.parametrize("bad", ["../etc", "a/b", "", "x" * 65])
    def test_a_malformed_job_id_is_a_usage_error(self, data_root, bad, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause(bad)
        assert exc.value.code == 2
        assert "invalid job id" in capsys.readouterr().err

    def test_a_malformed_job_id_answers_invalid_job_id_under_json(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_pause("../etc", json_output=True)
        assert exc.value.code == 2
        captured = capsys.readouterr()
        assert captured.err == ""
        payload = json.loads(captured.out)
        assert payload["schema_version"] == 1
        assert payload["ok"] is False
        assert payload["error"] == "invalid_job_id"

    def test_a_malformed_job_id_is_a_usage_error_for_unpause_too(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_unpause("../etc")
        assert exc.value.code == 2


class TestJSONThroughTheDispatcher:
    """The same real argv dispatcher `TestJSONThroughTheDispatcher` in
    `test_job_stop.py` proves `job stop` through."""

    def test_pause_answers_the_envelope(self, job, capsys):
        from apps.cli.grouped import main

        main(["job", "pause", job.job_id, "--reason", "dispatched", "--json"])
        payload = json.loads(capsys.readouterr().out)
        assert payload["schema_version"] == 1
        assert payload["ok"] is True
        assert payload["job_id"] == job.job_id
        assert payload["outcome"] == "requested"

    def test_unpause_answers_the_envelope(self, job, capsys):
        from apps.cli.grouped import main

        main(["job", "pause", job.job_id, "--json"])
        capsys.readouterr()
        main(["job", "unpause", job.job_id, "--json"])
        payload = json.loads(capsys.readouterr().out)
        assert payload["schema_version"] == 1
        assert payload["ok"] is True
        assert payload["outcome"] == "withdrawn"

    def test_pause_with_task_answers_the_envelope(self, job, capsys):
        from apps.cli.grouped import main

        task_id = job.tasks[0].task_id
        main(["job", "pause", job.job_id, "--task", task_id, "--json"])
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is True
        assert payload["outcome"] == "paused"
        assert payload["task_id"] == task_id


class TestItIsWiredIntoTheCli:
    def test_pause_is_in_the_catalog_under_job(self):
        entry = next(e for e in CATALOG if e.command_id == "job.pause")
        assert entry.group_id == "job" and entry.subcommand == "pause"
        assert entry.supports_json is True
        assert not entry.may_mutate_repo and not entry.may_execute_commands
        assert {a.name for a in entry.args} >= {
            "job_id", "--task", "--reason", "--source", "--json"}
        assert entry.command_id in {e.command_id for e in get_commands_for_group("job")}

    def test_unpause_is_in_the_catalog_under_job(self):
        entry = next(e for e in CATALOG if e.command_id == "job.unpause")
        assert entry.group_id == "job" and entry.subcommand == "unpause"
        assert entry.supports_json is True
        assert not entry.may_mutate_repo and not entry.may_execute_commands
        assert {a.name for a in entry.args} >= {"job_id", "--task", "--source", "--json"}
        assert entry.command_id in {e.command_id for e in get_commands_for_group("job")}

    def test_both_handlers_are_registered(self):
        handlers = collect_all_handlers()
        assert "job.pause" in handlers
        assert "job.unpause" in handlers

    def test_both_are_exposed_to_the_ui_door(self):
        from apps.cli.command_catalog import UI_EXPOSED_COMMANDS

        assert "job.pause" in UI_EXPOSED_COMMANDS
        assert "job.unpause" in UI_EXPOSED_COMMANDS


class TestTheParserWiresTaskAsAValuedOption:
    """`--task` takes a value — unlike `job stop`'s `--status`, which is a bare
    flag — so a parse that drops the value would silently pause the whole job
    instead of the one task the operator named."""

    def _parse(self, argv: list[str]):
        from apps.cli.grouped import build_parser

        return build_parser().parse_args(argv)

    def test_pause_task_value_reaches_the_namespace(self):
        args = self._parse(["job", "pause", "abc123", "--task", "T2"])
        assert args.task == "T2"

    def test_unpause_task_value_reaches_the_namespace(self):
        args = self._parse(["job", "unpause", "abc123", "--task", "T2"])
        assert args.task == "T2"

    def test_only_declared_flags_are_flags(self):
        flags = {(e.command_id, a.name) for e in CATALOG for a in e.args if a.is_flag}
        assert ("job.pause", "--task") not in flags
        assert ("job.unpause", "--task") not in flags

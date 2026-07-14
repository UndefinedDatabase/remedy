"""F011 T003 — `remedy job stop`, the operator's half of the kill switch.

The command writes a control file and says so. It does not kill a process, it does not
touch the repository, and it never pretends: an unknown job exits 3, an unwritable control
area exits non-zero and says that NO stop was requested, and a finished job is told the
truth instead of being handed a reassuring sentence.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_commands_for_group
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import job_stop_cmd as CMD
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_STOPPED,
    _persist_job,
    parse_job_file,
)
from packages.orchestration.safe_points import (
    consume_stop,
    control_root,
    request_stop,
    stop_requested,
)

_JOB = """\
# Job: CLI Stop Test

## Task 1
Do a thing.

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
    return parse_job_file(_JOB, str(repo))


class TestTheHappyPath:
    def test_it_requests_a_stop_and_says_what_will_happen(self, job, capsys):
        CMD._cmd_job_stop(job.job_id, reason="operator requested stop")

        out = capsys.readouterr().out
        assert "Stop requested — it will take effect at the next safe point." in out
        assert job.job_id in out

        pending = stop_requested(job.job_id)
        assert pending is not None
        assert pending.reason == "operator requested stop" and pending.source == "cli"

    def test_json_output_is_stable_and_carries_the_signal(self, job, capsys):
        CMD._cmd_job_stop(job.job_id, reason="stopping", source="ui", json_output=True)

        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is True and payload["job_id"] == job.job_id
        assert payload["stop"]["reason"] == "stopping"
        assert payload["stop"]["source"] == "ui"
        assert payload["stop"]["stop_signal_v"] == 1
        assert payload["stop"]["request_id"]

    def test_a_second_request_is_idempotent(self, job, capsys):
        CMD._cmd_job_stop(job.job_id, reason="first", json_output=True)
        first = json.loads(capsys.readouterr().out)["stop"]["request_id"]
        CMD._cmd_job_stop(job.job_id, reason="second", json_output=True)
        second = json.loads(capsys.readouterr().out)["stop"]["request_id"]

        assert first == second

    def test_stopping_an_already_stopped_job_creates_no_new_trap_request(self, job, capsys):
        """The reviewed build wrote a NEW pending request here — which would stop the job
        again the moment somebody resumed it. Same stop, same answer, no new episode."""
        job.status = JOB_STOPPED
        job.stop_request_id = "oldrequest123"
        job.stop_reason = "operator requested stop"
        job.stopped_at = "2026-07-14T10:00:00+00:00"
        _persist_job(job)

        CMD._cmd_job_stop(job.job_id, reason="again", json_output=True)
        payload = json.loads(capsys.readouterr().out)

        assert payload["ok"] is True and payload["already_stopped"] is True
        assert payload["stop"]["request_id"] == "oldrequest123"
        assert stop_requested(job.job_id) is None      # NO new pending file

    def test_the_human_already_stopped_message_is_honest(self, job, capsys):
        job.status = JOB_STOPPED
        job.stop_request_id = "oldrequest123"
        _persist_job(job)

        CMD._cmd_job_stop(job.job_id, reason="again")
        out = capsys.readouterr().out
        assert "already stopped" in out and "no new stop was requested" in out
        assert stop_requested(job.job_id) is None

    def test_it_kills_no_process_and_touches_no_repository(self, job, monkeypatch):
        import subprocess

        def _no(*a, **k):
            raise AssertionError("the kill switch shelled out")

        monkeypatch.setattr(subprocess, "run", _no)
        monkeypatch.setattr(subprocess, "Popen", _no)
        monkeypatch.setattr(os, "kill", _no)

        CMD._cmd_job_stop(job.job_id, reason="x")
        assert stop_requested(job.job_id) is not None


class TestStatus:
    def test_status_distinguishes_none_pending_and_consumed(self, job, capsys):
        CMD._cmd_job_stop(job.job_id, status=True, json_output=True)
        empty = json.loads(capsys.readouterr().out)
        assert empty["pending"] is None and empty["consumed_count"] == 0
        assert empty["stopped"] is False

        request_stop(job.job_id, "waiting", "cli")
        CMD._cmd_job_stop(job.job_id, status=True, json_output=True)
        pending = json.loads(capsys.readouterr().out)
        assert pending["pending"]["reason"] == "waiting"
        assert pending["consumed_count"] == 0

        consume_stop(job.job_id)
        job.status = JOB_STOPPED
        _persist_job(job)
        CMD._cmd_job_stop(job.job_id, status=True, json_output=True)
        consumed = json.loads(capsys.readouterr().out)
        assert consumed["pending"] is None and consumed["consumed_count"] == 1
        assert consumed["stopped"] is True and consumed["job_status"] == "stopped"

    def test_status_shows_the_archived_history_of_a_resumed_job(self, job, capsys):
        request_stop(job.job_id, "first", "cli")
        consume_stop(job.job_id)
        job.status = "running"                      # resumed
        _persist_job(job)
        request_stop(job.job_id, "second", "cli")
        consume_stop(job.job_id)

        CMD._cmd_job_stop(job.job_id, status=True, json_output=True)
        payload = json.loads(capsys.readouterr().out)
        assert payload["consumed_count"] == 2
        assert {a["reason"] for a in payload["archived"]} == {"first", "second"}
        assert payload["stopped"] is False           # it is running again

    def test_human_status_is_readable(self, job, capsys):
        request_stop(job.job_id, "operator requested stop", "cli")
        CMD._cmd_job_stop(job.job_id, status=True)
        out = capsys.readouterr().out
        assert "Stop request PENDING" in out
        assert "operator requested stop" in out


class TestItRefusesToLie:
    def test_an_unknown_job_exits_3(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop("0123456789abcdef")
        assert exc.value.code == 3
        assert "job not found" in capsys.readouterr().err

    def test_an_unknown_job_exits_3_in_json_mode_too(self, data_root, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop("0123456789abcdef", json_output=True)
        assert exc.value.code == 3
        assert json.loads(capsys.readouterr().out)["error"] == "job_not_found"

    def test_status_for_an_unknown_job_exits_3(self, data_root):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop("0123456789abcdef", status=True)
        assert exc.value.code == 3

    @pytest.mark.parametrize("bad", ["../etc", "a/b", "", "x" * 65])
    def test_a_malformed_job_id_is_a_usage_error(self, data_root, bad, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop(bad)
        assert exc.value.code == 2
        assert "invalid job id" in capsys.readouterr().err

    def test_a_completed_job_is_not_told_that_work_will_stop(self, job, capsys):
        job.status = JOB_COMPLETED
        _persist_job(job)

        with pytest.raises(SystemExit) as exc:
            CMD._cmd_job_stop(job.job_id)
        assert exc.value.code == 1
        err = capsys.readouterr().err
        assert "no stop was requested" in err or "no work left to stop" in err
        assert stop_requested(job.job_id) is None

    def test_an_unwritable_control_area_is_loud_and_requests_nothing(self, job, capsys):
        root = control_root()
        root.mkdir(parents=True, exist_ok=True)
        os.chmod(root, 0o500)
        try:
            with pytest.raises(SystemExit) as exc:
                CMD._cmd_job_stop(job.job_id, reason="x")
            assert exc.value.code == 1
            assert "no stop was requested" in capsys.readouterr().err
        finally:
            os.chmod(root, 0o700)

    def test_an_unwritable_control_area_says_so_in_json_too(self, job, capsys):
        root = control_root()
        root.mkdir(parents=True, exist_ok=True)
        os.chmod(root, 0o500)
        try:
            with pytest.raises(SystemExit) as exc:
                CMD._cmd_job_stop(job.job_id, reason="x", json_output=True)
            assert exc.value.code == 1
            payload = json.loads(capsys.readouterr().out)
            assert payload["ok"] is False and payload["error"] == "stop_not_requested"
        finally:
            os.chmod(root, 0o700)


class TestItIsWiredIntoTheCli:
    def test_the_command_is_in_the_catalog_under_job(self):
        entry = next(e for e in CATALOG if e.command_id == "job.stop")
        assert entry.group_id == "job" and entry.subcommand == "stop"
        assert entry.supports_json is True
        assert not entry.may_mutate_repo and not entry.may_execute_commands
        assert {a.name for a in entry.args} >= {
            "job_id", "--reason", "--source", "--status", "--json"}
        assert entry.command_id in {e.command_id for e in get_commands_for_group("job")}

    def test_the_handler_is_registered(self):
        handlers = collect_all_handlers()
        assert "job.stop" in handlers

    def test_it_is_not_the_worker_queue_pause_or_cancel(self):
        # F011 stops a PERSISTED PING-PONG JOB. Wiring it to the queue commands would stop
        # the wrong thing entirely.
        assert "job.stop" not in {"job.pause", "job.cancel"}
        entry = next(e for e in CATALOG if e.command_id == "job.stop")
        assert "safe point" in entry.description or "F011" in entry.description


class TestTheParserDoesNotBreakOtherCommands:
    """F011 first added `--status` as a store_true by OPTION NAME, in the shared grouped
    parser. That silently turned `remedy propose list <job> --status pending` into an error:
    the same option name means different things to different commands, so the CATALOG
    decides, per argument, not the parser by spelling."""

    def _parse(self, argv: list[str]):
        from apps.cli.grouped import build_parser

        return build_parser().parse_args(argv)

    def test_job_stop_status_is_a_boolean_flag(self):
        args = self._parse(["job", "stop", "abc123", "--status"])
        assert args.status is True

    def test_job_stop_status_takes_no_value(self):
        with pytest.raises(SystemExit):
            self._parse(["job", "stop", "abc123", "--status", "pending"])

    def test_propose_list_status_still_takes_a_value(self):
        args = self._parse(["propose", "list", "abc123", "--status", "pending"])
        assert args.status == "pending"

    def test_only_declared_flags_are_flags(self):
        from apps.cli.command_catalog import CATALOG

        flags = {(e.command_id, a.name) for e in CATALOG for a in e.args if a.is_flag}
        assert ("job.stop", "--status") in flags
        assert ("propose.list", "--status") not in flags

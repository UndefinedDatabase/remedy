"""Tests for `remedy teach narrate` — the teacher's Stage 1 surface (F255 T002/T003).

The load-bearing property is T003's: the command is READ-ONLY, proven
BEHAVIOURALLY rather than asserted — every file under the data root is hashed
before and after the call and the two maps must be identical.

Deliberately NOT re-asserted here: the sentences themselves, which
tests/orchestration/test_teacher_narration.py pins at module level, and the
parser wiring, which this round's own gate exercises by running the real
`remedy teach narrate` end to end over a run log.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command, get_commands_for_group
from apps.cli.commands.teach_cmd import COMMAND_HANDLERS, _cmd_teach_narrate

_JOB_ID = "3f2b1a90-0000-4000-8000-000000000001"

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
    {"event": "some_unlisted_event", "timestamp": "2026-08-21T00:00:03Z"},
]


def _write_run_log(root: Path, job_id: str, events: list[dict]) -> Path:
    """A run log at the real relative path ``load_run_events`` reads."""
    runs = root / "runs" / job_id
    runs.mkdir(parents=True, exist_ok=True)
    log = runs / "run-1.jsonl"
    log.write_text(
        "\n".join(json.dumps(e, separators=(",", ":")) for e in events) + "\n",
        encoding="utf-8",
    )
    return log


def _hash_tree(root: Path) -> dict[str, str]:
    """Every file under ``root``, mapped to the sha256 of its bytes."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


class TestTeachNarrateIsReadOnly:
    """T003: the run's files are byte-identical before and after the command."""

    def test_narrating_changes_no_byte_under_the_data_root(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = _hash_tree(data_root)
        assert before, "the fixture must put at least one file on disk"

        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()

        assert _hash_tree(data_root) == before

    def test_narrating_creates_and_removes_no_file(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = sorted(p.relative_to(data_root) for p in data_root.rglob("*"))
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert sorted(p.relative_to(data_root) for p in data_root.rglob("*")) == before

    def test_narrating_appends_no_run_log_event(self, data_root, capsys):
        log = _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = log.read_bytes()
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert log.read_bytes() == before

    def test_a_job_with_no_run_log_writes_nothing_and_says_so(self, data_root, capsys):
        _cmd_teach_narrate(_JOB_ID)
        out = capsys.readouterr().out
        assert "no events yet" in out and "(0 events)" in out
        assert _hash_tree(data_root) == {}


class TestTeachCatalogDeclaration:
    def test_the_command_is_declared_read_only(self):
        cmd = get_command("teach.narrate")
        # T003 declares the action class as well as proving the behaviour: the
        # catalog is what a permission layer reads, and the tests above are what
        # make the declaration true rather than merely stated.
        assert cmd.action_class == "read_only"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False
        assert cmd.requires_permission is False

    def test_ask_is_declared_write_metadata_because_it_writes_a_ledger_row(self):
        cmd = get_command("teach.ask")
        # DECISION F255 D10: `ask` writes exactly one token-ledger row, so a
        # read_only declaration here would be false — and a false declaration
        # misleads the permission layer that reads this catalog.
        assert cmd.action_class == "write_metadata"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False
        assert cmd.supports_json is True
        assert cmd.related == ("teach.narrate",)

    def test_the_handler_table_covers_every_declared_teach_command(self):
        # EQUALITY of the two sets, never a subset: a declared command with no
        # handler and a handler with no declaration are both defects, and only
        # equality catches the second one.
        declared = {c.command_id for c in get_commands_for_group("teach")}
        assert declared == {"teach.narrate", "teach.ask"} == set(COMMAND_HANDLERS)

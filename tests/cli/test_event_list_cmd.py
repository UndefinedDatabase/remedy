"""`event list` honours the shared list options (R-0796).

In-process: `_load_job_events` is replaced by a fake that hands the handler a
fixed run log, so no job store and no data root are read.
"""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest

_JOB = "0123456789abcdef0123456789abcdef"
_EVENTS = [
    {"event": "job_created", "timestamp": "2026-09-01T00:00:00Z", "outcome": "ok"},
    {"event": "test_run_completed", "timestamp": "2026-09-02T00:00:00Z", "outcome": "passed"},
    {"event": "job_completed", "timestamp": "2026-09-03T00:00:00Z", "outcome": "ok"},
]


def _event_list(capsys, **flags):
    from apps.cli.commands.event import _cmd_event_list

    with patch("apps.cli.commands.event._load_job_events",
               return_value=(None, list(_EVENTS), _JOB)):
        _cmd_event_list(_JOB, json_output=True, **flags)
    return [e["event_type"] for e in json.loads(capsys.readouterr().out)["events"]]


def test_the_newest_event_leads_by_default(capsys):
    assert _event_list(capsys) == ["job_completed", "test_run_completed", "job_created"]


def test_limit_keeps_the_newest_events(capsys):
    assert _event_list(capsys, limit="2") == ["job_completed", "test_run_completed"]


def test_since_and_until_filter_by_the_events_timestamp(capsys):
    assert _event_list(capsys, since="2026-09-01T12:00:00Z",
                       until="2026-09-02T12:00:00Z") == ["test_run_completed"]


def test_type_still_filters_before_the_list_options(capsys):
    assert _event_list(capsys, event_type="job_created", limit="1") == ["job_created"]


def test_an_unknown_sort_field_exits_nonzero_naming_the_valid_set(capsys):
    with pytest.raises(SystemExit) as exc:
        _event_list(capsys, sort="bogus")
    assert exc.value.code == 1
    assert "valid fields: event_type, outcome, timestamp" in capsys.readouterr().err


def test_the_parsed_command_line_reaches_the_handler(capsys):
    """The catalog's own --limit default and the shared --since/--until/--sort
    arrive through COMMAND_HANDLERS, not only through a direct call."""
    from apps.cli.commands.event import COMMAND_HANDLERS
    from apps.cli.grouped import build_parser

    args = build_parser().parse_args(
        ["event", "list", _JOB, "--json", "--sort", "event_type", "--until", "2026-09-02T12:00:00Z"])
    with patch("apps.cli.commands.event._load_job_events",
               return_value=(None, list(_EVENTS), _JOB)):
        COMMAND_HANDLERS["event.list"](args)
    body = json.loads(capsys.readouterr().out)
    assert [e["event_type"] for e in body["events"]] == ["job_created", "test_run_completed"]

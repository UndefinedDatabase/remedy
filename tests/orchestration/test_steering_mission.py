"""F264 T002, the mission half — a consumed steering message amends its mission's contract.

DECISION amend0905-vocab D9 makes every operator message an amendment "recorded on the mission,
DoD recompiled"; F269 built the amendment, and DECISION F264 D5 routes a consumed message to it,
exactly once, and names the amendment in the consumption marker. No provider is ever called.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packages.orchestration import steering as ST
from packages.orchestration.mission_contract import read_mission_contract
from packages.orchestration.mission_state import (
    MISSION_ROLE_INITIAL,
    create_mission,
    link_job_to_mission,
    load_mission,
)
from packages.orchestration.timeline import load_run_events

PROJECT = "p-f264"
JOB = "0a1b2c3d4e5f6a7b"
NOW = datetime(2026, 9, 24, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def root(tmp_path):
    return tmp_path / "remedy_data"


@pytest.fixture
def mission(root):
    made = create_mission(PROJECT, "Ship the tool", root=root)
    link_job_to_mission(PROJECT, made.id, JOB, MISSION_ROLE_INITIAL, root=root)
    return made


def _send(root, text):
    return ST.record_steering_message(JOB, text, job_state="running", channel="cli",
                                      root=root, now=NOW)


def _consume(root, round_number=2):
    return ST.consume_pending_steering(JOB, task_id="task-1", round_number=round_number,
                                       root=root, now=NOW)


def _contract(root, mission):
    return read_mission_contract(load_mission(PROJECT, mission.id, root))


def test_a_consumed_message_amends_the_mission_and_the_marker_names_it(root, mission):
    _send(root, "Use pnpm, never npm.")
    _consume(root)
    [amendment] = _contract(root, mission).amendments
    assert (amendment["id"], amendment["text"], amendment["criteria"]) == (
        "A001", "Use pnpm, never npm.", ["C001"])
    marker = ST.list_steering_consumptions(JOB, root)["sm-0001"]
    assert (marker["mission_id"], marker["amendment_id"]) == (mission.id, "A001")
    [event] = [e for e in load_run_events(root, JOB)
               if e.get("event") == "steering_message_consumed"]
    assert event["metadata"]["amendment_id"] == "A001"


def test_each_message_is_one_amendment_in_order_and_never_twice(root, mission):
    _send(root, "one")
    _consume(root, round_number=1)
    _send(root, "two")
    _consume(root, round_number=2)
    _consume(root, round_number=3)
    amendments = _contract(root, mission).amendments
    assert [(a["id"], a["text"]) for a in amendments] == [("A001", "one"), ("A002", "two")]
    markers = ST.list_steering_consumptions(JOB, root)
    assert [markers[m]["amendment_id"] for m in ("sm-0001", "sm-0002")] == ["A001", "A002"]


def test_a_job_with_no_mission_amends_nothing(root):
    _send(root, "Use pnpm.")
    _consume(root)
    marker = ST.list_steering_consumptions(JOB, root)["sm-0001"]
    assert (marker["mission_id"], marker["amendment_id"]) == ("", "")


def test_a_failed_amendment_is_loud_and_consumes_nothing(root, mission, monkeypatch):
    def refuse(*args, **kwargs):
        raise OSError("mission record is read-only")

    monkeypatch.setattr("packages.orchestration.mission_contract.amend_mission_contract", refuse)
    _send(root, "Use pnpm.")
    with pytest.raises(OSError, match="read-only"):
        _consume(root)
    assert ST.list_steering_consumptions(JOB, root) == {}
    assert _contract(root, mission) is None

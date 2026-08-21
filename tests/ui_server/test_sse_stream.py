"""
Domain tests: ui_server/test_sse_stream.py

T001's stream reader: frames carry the ledger's own position as the SSE event
id, an idle stream heartbeats with a comment frame, and every collaborator
that touches time is injected so cadence is asserted rather than waited out.
"""

from __future__ import annotations

import json
from typing import Any

from packages.orchestration import ui_server as mod


def _events(count: int) -> list[dict[str, Any]]:
    return [
        {"event": f"e{i}", "timestamp": f"2026-08-21T00:00:{i:02d}Z", "outcome": "ok"}
        for i in range(count)
    ]


# A hand-wound clock: the test decides what time it is.
class _Clock:
    def __init__(self) -> None:
        self.t = 0.0
        self.slept: list[float] = []

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.t += seconds


def _budget(passes: int) -> Any:
    """A `should_continue` that permits exactly `passes` loop passes."""
    left = [passes]

    def should_continue() -> bool:
        if left[0] <= 0:
            return False
        left[0] -= 1
        return True

    return should_continue


def _run(load_events: Any, start: int, passes: int, clock: _Clock) -> list[bytes]:
    return list(mod.iter_sse_frames(
        load_events, start, now=clock.now, sleep=clock.sleep,
        should_continue=_budget(passes),
        heartbeat_seconds=15.0, poll_seconds=1.0,
    ))


def _parse(frame: bytes) -> dict[str, str]:
    """Split one event frame into its SSE fields."""
    assert frame.endswith(b"\n\n")
    fields: dict[str, str] = {}
    for line in frame.decode().rstrip("\n").split("\n"):
        key, _, value = line.partition(": ")
        fields[key] = value
    return fields


class TestFrameShape:
    def test_the_event_id_is_the_ledger_position(self):
        # Not the position within THIS response: a stream that renumbered
        # would say 0 for the first frame it happened to send.
        assert _parse(mod.sse_event_frame(7, {"seq": 7}))["id"] == "7"

    def test_the_data_line_is_the_json_envelope(self):
        payload = {"seq": 3, "event": "task_started", "timestamp": "t", "outcome": "ok"}
        assert json.loads(_parse(mod.sse_event_frame(3, payload))["data"]) == payload

    def test_the_heartbeat_is_a_comment_and_not_an_event(self):
        frame = mod.sse_heartbeat_frame()
        assert frame.startswith(b":")
        assert frame.endswith(b"\n\n")
        # No field a client can surface, so an idle stream stays silent to the
        # consumer and a resuming client never asks to replay a heartbeat.
        for field in (b"data:", b"id:", b"event:"):
            assert field not in frame

    def test_the_envelope_carries_the_safe_fields_only(self):
        summary = mod._safe_event_summary(2, {"event": "x", "timestamp": "t", "outcome": "ok"})
        assert set(summary) == {"seq", "event", "timestamp", "outcome"}

    def test_the_cursor_endpoint_and_the_stream_share_one_envelope(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(3))

        class _Job:
            id = "11111111-2222-3333-4444-555555555555"

        polled = mod._build_events_since_json(_Job(), "0")["events"]
        streamed = [json.loads(_parse(f)["data"])
                    for f in _run(lambda: _events(3), 0, 1, _Clock())]
        # Equal payloads: a field added to one can never be missing from the
        # other, because both come from the one envelope writer.
        assert streamed == polled


class TestStreamFrames:
    def test_every_event_from_the_cursor_is_streamed_in_ledger_order(self):
        frames = _run(lambda: _events(4), 0, 1, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["0", "1", "2", "3"]

    def test_a_cursor_resumes_without_renumbering(self):
        frames = _run(lambda: _events(5), 2, 1, _Clock())
        # First frame after a resume is 2, not 0: the ledger numbers, the
        # stream only carries the numbering.
        assert [_parse(f)["id"] for f in frames] == ["2", "3", "4"]

    def test_a_cursor_past_the_end_streams_no_event(self):
        frames = _run(lambda: _events(3), 9, 1, _Clock())
        assert [f for f in frames if not f.startswith(b":")] == []

    def test_events_appended_during_the_stream_continue_the_numbering(self):
        growing = [_events(2)]
        frames = _run(lambda: growing.pop(0) if growing else _events(4), 0, 2, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["0", "1", "2", "3"]


class TestHeartbeatCadence:
    def test_an_idle_stream_stays_silent_before_the_interval(self):
        clock = _Clock()
        assert _run(lambda: [], 0, 3, clock) == []
        assert clock.slept == [1.0, 1.0, 1.0]

    def test_one_heartbeat_is_sent_once_the_interval_has_passed(self):
        assert _run(lambda: [], 0, 16, _Clock()) == [mod.sse_heartbeat_frame()]

    def test_the_heartbeat_interval_restarts_after_each_frame(self):
        # Cadence, not a count of ticks: 30 slept seconds carry two beats.
        assert _run(lambda: [], 0, 32, _Clock()) == [mod.sse_heartbeat_frame()] * 2

    def test_an_event_defers_the_next_heartbeat(self):
        served = [_events(1)]
        frames = _run(lambda: served.pop(0) if served else _events(1), 0, 15, _Clock())
        # 14 idle seconds after the event is one short of the interval.
        assert [f for f in frames if f.startswith(b":")] == []

    def test_the_default_interval_is_fifteen_seconds(self):
        assert mod.SSE_HEARTBEAT_SECONDS == 15.0

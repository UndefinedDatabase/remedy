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
        assert set(summary) == {"seq", "event", "timestamp", "outcome", "task_id"}
        # No linkage in either place is not an error: the row cannot jump.
        assert summary["task_id"] == ""

    def test_the_envelope_carries_the_linkage_from_both_event_sources(self):
        """DECISION F021 D2's single additive field, resolved from TWO places.

        `load_run_events` yields run-log rows whose `task_id` is TOP-LEVEL,
        while `_load_job_plan_events` nests it under `metadata`. A summary
        reading only the top level would leave jump-to-node dead for every
        trace-driven job while every run-log job worked -- a silent half
        feature, and the failure mode no suite here would have surfaced.
        """
        from_run_log = mod._safe_event_summary(
            1, {"event": "task_started", "task_id": "T-7"})
        assert from_run_log["task_id"] == "T-7"

        from_trace = mod._safe_event_summary(
            2, {"event": "task_started", "metadata": {"task_id": "T-9"}})
        assert from_trace["task_id"] == "T-9"

        # Top level wins when both carry one: the run log is the ledger.
        both = mod._safe_event_summary(3, {
            "event": "x", "task_id": "T-1", "metadata": {"task_id": "T-2"}})
        assert both["task_id"] == "T-1"

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


# A job the route can carry: `_load_job` is stubbed, so only the id is read.
class _Job:
    id = "11111111-2222-3333-4444-555555555555"


class _Socket:
    """A peer that accepts `until` frames and then goes away."""

    def __init__(self, until: int) -> None:
        self.frames: list[bytes] = []
        self.until = until

    def write(self, frame: bytes) -> None:
        if len(self.frames) >= self.until:
            raise BrokenPipeError
        self.frames.append(frame)

    def flush(self) -> None:
        return None


def _dispatch(monkeypatch: Any, path: str, job: Any, err: Any,
              headers: dict[str, str] | None = None) -> tuple[list, list]:
    """Drive `do_GET` on a socketless handler and record what it answered."""
    monkeypatch.setattr(mod, "_load_job", lambda jid: (job, err))
    handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
    handler.server_token = "tok"
    handler.target_job_id = ""
    handler.path = path
    # A real handler always carries `headers`; one built with `__new__` does
    # not, and the stream branch now reads it.
    handler.headers = headers or {}
    answered: list[Any] = []
    streamed: list[Any] = []
    handler._send_json = lambda code, data: answered.append((code, data))
    handler._send_sse_stream = lambda j, cursor: streamed.append((j, cursor))
    handler.do_GET()
    return answered, streamed


class TestFrameDraining:
    def test_every_frame_reaches_the_socket_in_order(self):
        socket = _Socket(3)
        sent = mod.drain_sse_frames(
            iter([b"a", b"b", b"c"]), socket.write, socket.flush, lambda: None)
        assert socket.frames == [b"a", b"b", b"c"]
        assert sent == 3

    def test_a_broken_pipe_stops_the_reader(self):
        stopped: list[bool] = []
        socket = _Socket(0)
        # The generator is suspended in `yield` and cannot see the pipe break,
        # so nothing but this call can end its loop.
        sent = mod.drain_sse_frames(
            iter([b"a", b"b"]), socket.write, socket.flush,
            lambda: stopped.append(True))
        assert sent == 0
        assert stopped == [True]

    def test_a_disconnect_keeps_the_frames_already_written(self):
        socket = _Socket(2)
        sent = mod.drain_sse_frames(
            iter([b"a", b"b", b"c"]), socket.write, socket.flush, lambda: None)
        assert socket.frames == [b"a", b"b"]
        assert sent == 2

    def test_a_closed_socket_ends_the_stream_rather_than_raising(self):
        # A wfile the server has already closed raises ValueError, not OSError.
        def flush() -> None:
            raise ValueError("I/O operation on closed file")

        assert mod.drain_sse_frames(
            iter([b"a"]), lambda frame: None, flush, lambda: None) == 0


class TestStreamRoute:
    def test_the_stream_path_reaches_the_writer_with_its_cursor(self, monkeypatch):
        job = _Job()
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", job, None)
        assert answered == []
        assert streamed == [(job, "7")]

    def test_a_stream_without_a_cursor_starts_at_the_beginning(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert streamed[0][1] == "0"

    def test_an_unknown_job_answers_404_before_one_stream_byte(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/nope/events/stream?token=tok", None,
            (404, {"error": "job not found"}))
        assert streamed == []
        assert answered == [(404, {"error": "job not found"})]

    def test_a_bad_token_never_reaches_the_stream(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=wrong", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 403

    def test_the_cursor_endpoint_still_answers_beside_the_stream(self, monkeypatch):
        # The stream is a SIXTH path part, so the five-part branch is untouched.
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(2))
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events-since?token=tok&cursor=0", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 200
        assert [e["seq"] for e in answered[0][1]["events"]] == [0, 1]


class TestStreamResponse:
    def _handler(self, socket: Any) -> Any:
        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.sent_code = []
        handler.headers_out = []
        handler.send_response = handler.sent_code.append
        handler.send_header = lambda key, value: handler.headers_out.append((key, value))
        handler.end_headers = lambda: None
        handler.wfile = socket
        return handler

    def test_the_response_declares_an_event_stream(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(1))
        handler = self._handler(_Socket(0))
        clock = _Clock()
        handler._send_sse_stream(_Job(), "0", now=clock.now, sleep=clock.sleep)
        assert handler.sent_code == [200]
        assert dict(handler.headers_out)["Content-Type"] == "text/event-stream"
        assert dict(handler.headers_out)["Cache-Control"] == "no-store"

    def test_the_cursor_span_reaches_the_socket_without_renumbering(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(3))
        socket = _Socket(2)
        handler = self._handler(socket)
        clock = _Clock()
        handler._send_sse_stream(_Job(), "1", now=clock.now, sleep=clock.sleep)
        # Resumed at 1, so the ids are the ledger's own and not 0-based.
        assert [_parse(f)["id"] for f in socket.frames] == ["1", "2"]

    def test_a_non_numeric_cursor_streams_from_the_beginning(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(2))
        socket = _Socket(2)
        handler = self._handler(socket)
        clock = _Clock()
        handler._send_sse_stream(_Job(), "junk", now=clock.now, sleep=clock.sleep)
        assert [_parse(f)["id"] for f in socket.frames] == ["0", "1"]

    def test_the_departed_peer_ends_the_loop(self, monkeypatch):
        # Without `stop` this call never returns: the reader would poll the
        # ledger for ever on a socket nobody is reading.
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(1))
        handler = self._handler(_Socket(0))
        clock = _Clock()
        handler._send_sse_stream(_Job(), "0", now=clock.now, sleep=clock.sleep)
        assert handler.wfile.frames == []


#: T001's framing golden: the exact bytes a client parses for a two-event
#: ledger that then goes idle past the heartbeat interval. Field order, the
#: blank-line separator and the comment shape are all pinned here, so any
#: change to the wire format has to be a deliberate edit of this constant.
GOLDEN_STREAM = (
    b'id: 0\ndata: {"seq": 0, "event": "e0", "timestamp": "2026-08-21T00:00:00Z", "outcome": "ok", "task_id": ""}\n\n'
    b'id: 1\ndata: {"seq": 1, "event": "e1", "timestamp": "2026-08-21T00:00:01Z", "outcome": "ok", "task_id": ""}\n\n'
    b": heartbeat\n\n"
)


class TestFramingGolden:
    def test_the_wire_bytes_match_the_golden(self):
        # 17 passes: one drains both events, fifteen sleep out the interval,
        # the last emits the single heartbeat that idling earns.
        joined = b"".join(_run(lambda: _events(2), 0, 17, _Clock()))
        assert joined == GOLDEN_STREAM

    def test_the_golden_is_what_the_frame_builders_produce(self):
        # Not a transcription of the constant above: rebuilt from the writers,
        # so a golden edited without a code change fails here.
        rebuilt = b"".join([
            mod.sse_event_frame(seq, mod._safe_event_summary(seq, _events(2)[seq]))
            for seq in (0, 1)
        ]) + mod.sse_heartbeat_frame()
        assert rebuilt == GOLDEN_STREAM


class TestStreamSlots:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_a_job_holds_slots_up_to_the_cap(self):
        taken = [mod.acquire_sse_slot("j", limit=2) for _ in range(3)]
        assert taken == [True, True, False]

    def test_a_released_slot_can_be_taken_again(self):
        assert mod.acquire_sse_slot("j", limit=1)
        assert not mod.acquire_sse_slot("j", limit=1)
        mod.release_sse_slot("j")
        assert mod.acquire_sse_slot("j", limit=1)

    def test_the_registry_forgets_a_job_at_zero(self):
        mod.acquire_sse_slot("j", limit=1)
        mod.release_sse_slot("j")
        # Not a lingering 0: an idle cockpit must not grow the registry.
        assert "j" not in mod._SSE_SLOTS_PER_JOB

    def test_an_extra_release_never_goes_negative(self):
        mod.release_sse_slot("j")
        mod.release_sse_slot("j")
        assert mod._SSE_SLOTS_PER_JOB.get("j", 0) == 0
        assert mod.acquire_sse_slot("j", limit=1)

    def test_two_jobs_do_not_share_one_cap(self):
        assert mod.acquire_sse_slot("a", limit=1)
        assert mod.acquire_sse_slot("b", limit=1)
        assert not mod.acquire_sse_slot("a", limit=1)

    def test_the_default_cap_is_four(self):
        assert mod.SSE_MAX_STREAMS_PER_JOB == 4


class TestStreamCapRoute:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_the_stream_is_refused_with_429_beyond_the_cap(self, monkeypatch):
        for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
            assert mod.acquire_sse_slot(_Job.id)
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert streamed == []
        assert answered[0][0] == 429

    def test_a_refused_stream_does_not_consume_a_slot(self, monkeypatch):
        for _ in range(mod.SSE_MAX_STREAMS_PER_JOB):
            mod.acquire_sse_slot(_Job.id)
        _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        # Still exactly at the cap: the refusal took nothing.
        assert mod._SSE_SLOTS_PER_JOB[_Job.id] == mod.SSE_MAX_STREAMS_PER_JOB

    def test_a_served_stream_releases_its_slot(self, monkeypatch):
        _dispatch(monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None)
        assert _Job.id not in mod._SSE_SLOTS_PER_JOB

    def test_a_raising_stream_still_releases_its_slot(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_job", lambda jid: (_Job(), None))

        def boom(job, cursor):
            raise RuntimeError("socket died")

        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.server_token = "tok"
        handler.target_job_id = ""
        handler.path = "/api/jobs/J/events/stream?token=tok"
        handler.headers = {}
        handler._send_json = lambda code, data: None
        handler._send_sse_stream = boom
        raised = False
        try:
            handler.do_GET()
        except RuntimeError:
            raised = True
        assert raised
        # The `finally` is the whole point: a crash must not leak capacity.
        assert _Job.id not in mod._SSE_SLOTS_PER_JOB

    def test_an_unknown_job_never_takes_a_slot(self, monkeypatch):
        _dispatch(
            monkeypatch, "/api/jobs/nope/events/stream?token=tok", None,
            (404, {"error": "job not found"}))
        assert mod._SSE_SLOTS_PER_JOB == {}


class TestResumeStart:
    """T002's resolver: the ledger position a reconnecting client resumes at."""

    def test_a_last_event_id_resumes_one_past_the_event_it_names(self):
        # The header names what the client ALREADY has, so starting AT it
        # would hand the same event over twice.
        assert mod.resolve_sse_start("4", "0") == 5

    def test_the_header_beats_the_query_cursor(self):
        # A reconnect carries the stale query string it first connected with
        # and a header the browser keeps current.
        assert mod.resolve_sse_start("9", "3") == 10

    def test_event_id_zero_is_a_position_and_not_an_absence(self):
        # The first event is 0; a truthiness test here would resume at 0 and
        # replay it for ever.
        assert mod.resolve_sse_start("0", "7") == 1

    def test_an_absent_header_falls_back_to_the_cursor(self):
        assert mod.resolve_sse_start(None, "6") == 6

    def test_a_blank_header_falls_back_to_the_cursor(self):
        assert mod.resolve_sse_start("   ", "6") == 6

    def test_a_mangled_header_falls_back_rather_than_refusing(self):
        assert mod.resolve_sse_start("not-a-seq", "6") == 6

    def test_a_negative_header_is_not_a_position(self):
        assert mod.resolve_sse_start("-1", "6") == 6

    def test_the_cursor_is_a_start_and_is_never_incremented(self):
        # Only the header is exclusive; conflating the two is the defect this
        # whole function exists to prevent.
        assert mod.resolve_sse_start(None, "7") == 7

    def test_neither_input_starts_at_the_beginning(self):
        assert mod.resolve_sse_start(None, "junk") == 0

    def test_surrounding_whitespace_is_tolerated(self):
        assert mod.resolve_sse_start(" 4 ", "0") == 5


class TestResumeSpan:
    def test_the_replayed_span_is_exactly_the_events_the_client_missed(self):
        # Six in the ledger and two already delivered: 3, 4 and 5 are owed.
        # Neither a duplicate of 2 nor a gap at 3 is acceptable.
        start = mod.resolve_sse_start("2", "0")
        frames = _run(lambda: _events(6), start, 1, _Clock())
        assert [_parse(f)["id"] for f in frames] == ["3", "4", "5"]

    def test_a_client_that_is_current_is_owed_no_event(self):
        start = mod.resolve_sse_start("5", "0")
        frames = _run(lambda: _events(6), start, 1, _Clock())
        assert [f for f in frames if not f.startswith(b":")] == []


class TestResumeRoute:
    def setup_method(self):
        mod._SSE_SLOTS_PER_JOB.clear()

    def test_the_header_reaches_the_writer_as_the_next_position(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok", _Job(), None,
            headers={"Last-Event-ID": "4"})
        assert streamed[0][1] == "5"

    def test_without_a_header_the_query_cursor_still_decides(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", _Job(), None)
        assert streamed[0][1] == "7"

    def test_the_header_overrides_the_cursor_on_the_wire(self, monkeypatch):
        _answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=7", _Job(), None,
            headers={"Last-Event-ID": "1"})
        assert streamed[0][1] == "2"

    def test_a_mangled_header_still_serves_the_stream(self, monkeypatch):
        answered, streamed = _dispatch(
            monkeypatch, "/api/jobs/J/events/stream?token=tok&cursor=3", _Job(), None,
            headers={"Last-Event-ID": "??"})
        assert answered == []
        assert streamed[0][1] == "3"

    def test_the_header_name_is_the_one_the_browser_sends(self):
        # EventSource sends exactly this spelling; a rename breaks resume in
        # silence, because the fallback path still serves a valid stream.
        assert mod.SSE_LAST_EVENT_ID_HEADER == "Last-Event-ID"


class _FlakyPeer:
    """A socket that accepts `until` frames and then drops the connection."""

    def __init__(self, until: int) -> None:
        self.frames: list[bytes] = []
        self.until = until

    def write(self, frame: bytes) -> None:
        if len(self.frames) >= self.until:
            raise BrokenPipeError
        self.frames.append(frame)

    def flush(self) -> None:
        return None


def _hammer(monkeypatch: Any, events: list, drop_after: int,
            reconnects: int = 40, last_event_id: str | None = None) -> list[bytes]:
    """Reconnect until the ledger is drained, dropping every `drop_after` frames.

    This is the acceptance shape the feature file names: a client that keeps
    losing its connection must end up with the ledger and nothing else. Each
    reconnect carries the id of the last frame it kept, exactly as an
    EventSource sends `Last-Event-ID`, and the server decides the span.
    `last_event_id` seeds that state, so a caller can hand this helper a client
    that ALREADY holds part of the ledger — which is what makes a resume across
    a ledger that grew between connections expressible (finding R-0621).
    """
    monkeypatch.setattr(mod, "_load_events", lambda job: events)
    transcript: list[bytes] = []
    for _ in range(reconnects):
        peer = _FlakyPeer(drop_after)
        handler = mod._RemedyHandler.__new__(mod._RemedyHandler)
        handler.send_response = lambda code: None
        handler.send_header = lambda key, value: None
        handler.end_headers = lambda: None
        handler.wfile = peer
        clock = _Clock()
        start = mod.resolve_sse_start(last_event_id, "0")
        handler._send_sse_stream(_Job(), str(start), now=clock.now, sleep=clock.sleep)
        for frame in peer.frames:
            # A heartbeat carries no id, so a resuming client never asks to
            # replay one and it never enters the transcript.
            if frame.startswith(b":"):
                continue
            transcript.append(frame)
            last_event_id = _parse(frame)["id"]
        if last_event_id is not None and int(last_event_id) == len(events) - 1:
            break
    return transcript


def _ledger_bytes(events: list) -> bytes:
    """The envelope sequence the client's transcript must byte-equal."""
    return b"".join(
        mod.sse_event_frame(seq, mod._safe_event_summary(seq, events[seq]))
        for seq in range(len(events))
    )


class TestDisconnectHammer:
    def test_the_transcript_byte_equals_the_ledger_envelope_sequence(self, monkeypatch):
        # The feature's acceptance heart, verbatim: bytes, not a summary.
        events = _events(12)
        assert b"".join(_hammer(monkeypatch, events, 3)) == _ledger_bytes(events)

    def test_no_event_arrives_twice_and_none_is_missing(self, monkeypatch):
        # Spelled out as ids too: a byte comparison that failed would not say
        # WHICH of the two failure modes happened.
        ids = [_parse(f)["id"] for f in _hammer(monkeypatch, _events(12), 3)]
        assert ids == [str(i) for i in range(12)]

    def test_every_disconnect_cadence_yields_the_same_transcript(self, monkeypatch):
        # One drop per frame is the worst case and a single clean connection
        # the best; the transcript may not depend on which one happened.
        events = _events(12)
        for drop_after in (1, 2, 3, 5, 7, 12):
            got = b"".join(_hammer(monkeypatch, events, drop_after))
            assert got == _ledger_bytes(events), drop_after

    def test_a_resume_crosses_a_ledger_that_grew_between_connections(self, monkeypatch):
        # The stream reads a file that is still being appended to, so the span
        # a client misses can straddle the growth. R-0621: the version of this
        # test written at R14 started its second client from scratch, so the
        # boundary it is named for was never crossed by a resume at all.
        events = _events(6)
        first = _hammer(monkeypatch, events, 2, reconnects=1)
        assert [_parse(f)["id"] for f in first] == ["0", "1"]
        events.extend(_events(10)[6:])
        rest = _hammer(monkeypatch, events, 3,
                       last_event_id=_parse(first[-1])["id"])
        # 2 through 9: everything after the frame the client kept, across the
        # boundary, with no duplicate of 1 and no gap at 6.
        assert [_parse(f)["id"] for f in rest] == [str(i) for i in range(2, 10)]
        assert b"".join(first + rest) == _ledger_bytes(events)

    def test_a_single_clean_connection_needs_no_resume(self, monkeypatch):
        events = _events(4)
        assert b"".join(_hammer(monkeypatch, events, 4)) == _ledger_bytes(events)


class TestResumeStartTypes:
    """R-0620: the guard reads a POSITION, and zero is a position."""

    def test_an_integer_zero_is_a_position_and_not_an_absence(self):
        # The string "0" is truthy and the integer 0 is not, so a truthiness
        # guard passes the string form and silently fails this one.
        assert mod.resolve_sse_start(0, "7") == 1

    def test_an_integer_header_resumes_one_past_it(self):
        assert mod.resolve_sse_start(4, "7") == 5

    def test_none_is_the_only_absence(self):
        # Everything else is data; only a missing header falls back.
        assert mod.resolve_sse_start(None, "7") == 7

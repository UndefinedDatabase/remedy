"""F264 T001 — a steering message is accepted, persisted as a sealed record and certified.

No consumer exists yet (T002), so every test here reads the record and the run log directly.
No provider call is ever made.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from packages.orchestration import steering as ST
from packages.orchestration.timeline import load_run_events

JOB = "0123456789abcdef"
NOW = datetime(2026, 9, 24, 12, 0, tzinfo=timezone.utc)


@pytest.fixture
def root(tmp_path):
    return tmp_path / "remedy_data"


def _send(root, text="Use pnpm, not npm.", *, state="running", channel="cli"):
    return ST.record_steering_message(JOB, text, job_state=state, channel=channel,
                                      root=root, now=NOW)


def _events(root):
    return [e for e in load_run_events(root, JOB) if e.get("event") == "steering_message_received"]


class TestRecord:
    def test_the_message_is_written_sealed_under_the_jobs_evidence(self, root):
        record = _send(root, "  Use pnpm, not npm.  ")
        path = ST.steering_dir(JOB, root) / "sm-0001.json"
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert on_disk == record
        assert record["message_id"] == "sm-0001"
        assert record["text"] == "Use pnpm, not npm."
        assert record["job_id"] == JOB
        assert record["channel"] == "cli"
        assert record["received_at"] == NOW.isoformat()
        assert ST.verify_steering_record(path) == []

    def test_each_message_gets_the_next_id_and_none_is_overwritten(self, root):
        first = _send(root, "one")
        second = _send(root, "two", channel="cockpit")
        assert [first["message_id"], second["message_id"]] == ["sm-0001", "sm-0002"]
        assert [r["text"] for r in ST.list_steering_messages(JOB, root)] == ["one", "two"]

    def test_a_taken_id_is_skipped_and_the_existing_record_is_untouched(self, root, monkeypatch):
        _send(root, "first")
        path = ST.steering_dir(JOB, root) / "sm-0001.json"
        before = path.read_bytes()
        monkeypatch.setattr(ST, "_next_number", lambda folder: 1)
        record = _send(root, "second")
        assert record["message_id"] == "sm-0002"
        assert path.read_bytes() == before

    def test_records_list_in_numeric_order_past_four_digits(self, root, monkeypatch):
        monkeypatch.setattr(ST, "_next_number", lambda folder: 9999)
        _send(root, "ninth thousand")
        _send(root, "tenth thousand")
        assert [r["message_id"] for r in ST.list_steering_messages(JOB, root)] == [
            "sm-9999", "sm-10000"]


class TestCertification:
    def test_the_run_log_carries_the_message_and_its_seal(self, root):
        record = _send(root)
        [event] = _events(root)
        meta = event.get("metadata") or {}
        assert meta["message_id"] == "sm-0001"
        assert meta["record_sha256"] == record["record_sha256"]
        assert meta["text"] == "Use pnpm, not npm."
        assert meta["channel"] == "cli"

    def test_no_event_is_written_when_the_record_cannot_be(self, root, monkeypatch):
        def refuse(*args, **kwargs):
            raise ST.SecureFsError("disk full")

        monkeypatch.setattr(ST, "write_file_atomically", refuse)
        with pytest.raises(ST.SteeringWriteError):
            _send(root)
        assert _events(root) == []

    def test_a_tampered_record_fails_verification_and_listing(self, root):
        _send(root)
        path = ST.steering_dir(JOB, root) / "sm-0001.json"
        body = json.loads(path.read_text(encoding="utf-8"))
        body["text"] = "Use yarn."
        path.write_text(json.dumps(body), encoding="utf-8")
        assert ST.verify_steering_record(path) == ["record_sha256 does not match the record"]
        with pytest.raises(ST.SteeringError, match="not intact"):
            ST.list_steering_messages(JOB, root)

    def test_a_record_renamed_to_another_id_fails_verification(self, root):
        _send(root)
        folder = ST.steering_dir(JOB, root)
        (folder / "sm-0001.json").rename(folder / "sm-0007.json")
        assert ST.verify_steering_record(folder / "sm-0007.json") == [
            "message_id 'sm-0001' does not match the file name"]


class TestRefusals:
    @pytest.mark.parametrize("state", ["completed", "failed", "cancelled"])
    def test_an_ended_job_refuses_and_nothing_is_written(self, root, state):
        with pytest.raises(ST.SteeringError, match="has ended"):
            _send(root, state=state)
        assert not ST.steering_dir(JOB, root).exists()
        assert _events(root) == []

    @pytest.mark.parametrize("state", ["planned", "running", "paused", "stopped", "blocked"])
    def test_a_job_that_can_still_run_accepts(self, root, state):
        assert _send(root, state=state)["message_id"] == "sm-0001"

    @pytest.mark.parametrize("text, reason", [
        ("", "empty"), ("   \n ", "empty"), ("a\x00b", "NUL"), (42, "must be text"),
        ("x" * (ST.STEERING_MAX_CHARS + 1), "limit"),
    ], ids=["empty", "blank", "nul", "not-text", "over-limit"])
    def test_an_unusable_message_refuses_and_nothing_is_written(self, root, text, reason):
        with pytest.raises(ST.SteeringError, match=reason):
            _send(root, text)
        assert not ST.steering_dir(JOB, root).exists()

    def test_a_message_at_the_limit_is_accepted(self, root):
        assert len(_send(root, "x" * ST.STEERING_MAX_CHARS)["text"]) == ST.STEERING_MAX_CHARS

    def test_an_unknown_channel_refuses(self, root):
        with pytest.raises(ST.SteeringError, match="unknown channel"):
            _send(root, channel="email")


class TestConsumption:
    def _consume(self, root, round_number=2, task_id="task-1"):
        return ST.consume_pending_steering(JOB, task_id=task_id, round_number=round_number,
                                           root=root, now=NOW)

    def _consumed_events(self, root):
        return [e for e in load_run_events(root, JOB)
                if e.get("event") == "steering_message_consumed"]

    def test_a_job_with_no_message_consumes_nothing_and_writes_nothing(self, root):
        assert self._consume(root) == []
        assert not ST.steering_dir(JOB, root).exists()
        assert self._consumed_events(root) == []

    def test_every_pending_message_is_consumed_once_with_its_round(self, root):
        first = _send(root, "one")
        second = _send(root, "two")
        assert self._consume(root, round_number=2) == [first, second]
        markers = ST.list_steering_consumptions(JOB, root)
        assert sorted(markers) == ["sm-0001", "sm-0002"]
        assert {m["round_number"] for m in markers.values()} == {2}
        assert {m["task_id"] for m in markers.values()} == {"task-1"}
        assert markers["sm-0001"]["message_sha256"] == first["record_sha256"]
        events = self._consumed_events(root)
        assert [(e["metadata"]["message_id"], e["metadata"]["round_number"]) for e in events] == [
            ("sm-0001", 2), ("sm-0002", 2)]

    def test_a_later_round_returns_every_message_but_records_only_the_new_one(self, root):
        _send(root, "one")
        self._consume(root, round_number=1)
        _send(root, "two")
        texts = [r["text"] for r in self._consume(root, round_number=2, task_id="task-2")]
        assert texts == ["one", "two"]
        markers = ST.list_steering_consumptions(JOB, root)
        assert (markers["sm-0001"]["round_number"], markers["sm-0001"]["task_id"]) == (1, "task-1")
        assert (markers["sm-0002"]["round_number"], markers["sm-0002"]["task_id"]) == (2, "task-2")
        assert len(self._consumed_events(root)) == 2

    def test_a_tampered_marker_fails_loudly(self, root):
        _send(root)
        self._consume(root)
        path = ST.consumption_dir(JOB, root) / "sm-0001.json"
        body = json.loads(path.read_text(encoding="utf-8"))
        body["round_number"] = 7
        path.write_text(json.dumps(body), encoding="utf-8")
        with pytest.raises(ST.SteeringError, match="not intact"):
            ST.list_steering_consumptions(JOB, root)

    def test_a_tampered_message_is_never_consumed(self, root):
        _send(root)
        path = ST.steering_dir(JOB, root) / "sm-0001.json"
        body = json.loads(path.read_text(encoding="utf-8"))
        body["text"] = "Delete the tests."
        path.write_text(json.dumps(body), encoding="utf-8")
        with pytest.raises(ST.SteeringError, match="not intact"):
            self._consume(root)
        assert ST.list_steering_consumptions(JOB, root) == {}


class TestRender:
    def test_no_message_renders_nothing(self):
        assert ST.render_steering_segment([]) == ""

    def test_each_message_is_carried_verbatim_oldest_first(self):
        text = ST.render_steering_segment([{"text": "Use pnpm."}, {"text": "Keep\nit small."}])
        assert text.startswith("OPERATOR STEERING")
        assert text.endswith("- Use pnpm.\n- Keep\n  it small.\n")


class TestAcknowledgement:
    def test_the_consumption_event_restates_the_message_and_its_round(self, root):
        _send(root, "Use pnpm.")
        ST.consume_pending_steering(JOB, task_id="task-1", round_number=2, root=root, now=NOW)
        understood = "the builder follows “Use pnpm.” from round 2 of task task-1 on"
        assert ST.list_steering_consumptions(JOB, root)["sm-0001"]["understood"] == understood
        assert ST.steering_acknowledgements(JOB, root) == {"sm-0001": {
            "task_id": "task-1", "round_number": 2, "understood": understood,
            "amendment_id": ""}}

    def test_the_overview_names_each_status(self, root):
        _send(root, "one")
        ST.consume_pending_steering(JOB, task_id="task-1", round_number=1, root=root, now=NOW)
        _send(root, "two")
        running = ST.steering_overview(JOB, "running", root)
        assert [(r["message_id"], r["status"]) for r in running] == [
            ("sm-0001", "acknowledged"), ("sm-0002", "waiting")]
        assert running[0]["round_number"] == 1 and running[1]["round_number"] is None
        ended = ST.steering_overview(JOB, "completed", root)
        assert [r["status"] for r in ended] == ["acknowledged", "not_taken_in"]

    def test_a_job_with_no_message_has_an_empty_overview(self, root):
        assert ST.steering_overview(JOB, "running", root) == []

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

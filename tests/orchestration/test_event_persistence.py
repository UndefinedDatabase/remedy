"""Tests for EventPersistenceResult (Step 1162)."""

from __future__ import annotations

from uuid import uuid4

from packages.orchestration.event_persistence import (
    emit_important_event,
)


def test_skipped_when_not_eligible():
    r = emit_important_event("/tmp", str(uuid4()), "x", {}, eligible=frozenset({"y"}))
    assert r.status == "skipped"
    assert r.persisted is False


def test_failed_on_invalid_job_id():
    r = emit_important_event("/tmp", "not-a-uuid", "evt", {})
    assert r.status == "failed"
    assert r.degraded is True


def test_complete_on_valid(tmp_path):
    jid = str(uuid4())
    r = emit_important_event(tmp_path, jid, "evt", {"k": "v"})
    assert r.status == "complete"
    assert r.persisted is True
    assert (tmp_path / "job_logs" / jid).exists()


def test_no_raw_exception_text():
    r = emit_important_event("/tmp", "bad", "evt", {})
    assert r.reason in ("invalid_job_id", "append_failed", "unexpected")

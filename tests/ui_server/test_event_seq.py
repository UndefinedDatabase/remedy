"""
Domain tests: ui_server/test_event_seq.py

The cursor-based events payload carries each event's own position in the
ledger as `seq`. F008's stream uses that value as the SSE event id, so it
must be the ledger's position and never a per-response counter — DECISION
F008 D1, "the stream EXPOSES the ledger position as seq and assigns
nothing". Renumbering is the failure this pins against: a client that
resumes from `seq` must land on the same event the server meant.
"""

from __future__ import annotations

from typing import Any

import pytest

from packages.orchestration import ui_server as mod


class _FakeJob:
    id = "11111111-2222-3333-4444-555555555555"


def _events(count: int) -> list[dict[str, Any]]:
    return [
        {"event": f"e{i}", "timestamp": f"2026-08-21T00:00:{i:02d}Z", "outcome": "ok"}
        for i in range(count)
    ]


@pytest.fixture
def ledger(monkeypatch):
    """Install a fixed ledger and hand the test its own length."""

    def install(count: int) -> int:
        monkeypatch.setattr(mod, "_load_events", lambda job: _events(count))
        return count

    return install


class TestEventSeqIsTheLedgerPosition:
    def test_seq_starts_at_zero_for_a_zero_cursor(self, ledger):
        ledger(5)
        payload = mod._build_events_since_json(_FakeJob(), "0")
        assert [e["seq"] for e in payload["events"]] == [0, 1, 2, 3, 4]

    def test_seq_is_absolute_not_relative_to_the_cursor(self, ledger):
        ledger(5)
        payload = mod._build_events_since_json(_FakeJob(), "3")
        # The third event is seq 3 whichever cursor asked for it — a
        # response-relative counter would restart at 0 here.
        assert [e["seq"] for e in payload["events"]] == [3, 4]

    def test_an_event_keeps_one_seq_across_different_cursors(self, ledger):
        ledger(6)
        job = _FakeJob()
        from_zero = mod._build_events_since_json(job, "0")["events"]
        from_four = mod._build_events_since_json(job, "4")["events"]
        by_seq = {e["seq"]: e["event"] for e in from_zero}
        for event in from_four:
            assert by_seq[event["seq"]] == event["event"]

    def test_seq_agrees_with_the_cursor_the_same_payload_returns(self, ledger):
        total = ledger(9)
        payload = mod._build_events_since_json(_FakeJob(), "2")
        assert payload["cursor"] == str(total)
        # The next request starts where this response stopped: the cursor is
        # one past the last seq returned, so no event is skipped or repeated.
        assert payload["events"][-1]["seq"] + 1 == int(payload["cursor"])

    def test_a_non_numeric_cursor_reads_from_the_start(self, ledger):
        ledger(3)
        payload = mod._build_events_since_json(_FakeJob(), "not-a-number")
        assert [e["seq"] for e in payload["events"]] == [0, 1, 2]

    def test_a_cursor_past_the_end_returns_nothing_and_invents_no_seq(self, ledger):
        total = ledger(4)
        payload = mod._build_events_since_json(_FakeJob(), "10")
        assert payload["events"] == []
        assert payload["cursor"] == str(total)

    def test_seq_survives_the_fifty_event_response_cap(self, ledger):
        ledger(140)
        payload = mod._build_events_since_json(_FakeJob(), "60")
        seqs = [e["seq"] for e in payload["events"]]
        # The cap bounds the RESPONSE, never the numbering: the first event
        # is still 60 and the run is consecutive.
        assert len(seqs) == 50
        assert seqs[0] == 60
        assert seqs == list(range(60, 110))

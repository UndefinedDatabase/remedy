"""
Domain tests: ui_server/test_budget_tick_envelope.py

T001's last hop. `_safe_event_summary` drops an event's `metadata`, and every
figure DECISION F022 D1 rules lives there, so a `budget.tick` reached the client
carrying no spend, no limit and no basis. DECISION F022 D3 widens that envelope
for THAT ONE EVENT KIND, through a whitelist copied key by key at both levels.

Both halves are pinned here: the tick gains its figures, and every other kind's
frame stays exactly the five fields it was.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from packages.orchestration import ui_server as mod

#: The envelope's fields before DECISION F022 D3, WRITTEN OUT rather than read
#: back off the code. A derived set would agree with whatever the summary
#: happened to produce, and the whole point of this half is that it cannot move
#: without someone typing it here.
BASE_FIELDS = {"seq", "event", "timestamp", "outcome", "task_id"}

#: One tick's metadata in the shape `safe_points._budget_tick_payload` writes it
#: when every figure exists. `TestTheWhitelistCoversTheEmitter` pins that claim
#: against the live emitter rather than trusting this literal.
FULL_TICK_METADATA: dict[str, Any] = {
    "spent_tokens": 1200,
    "unmeasured_calls": 2,
    "spent_usd": 0.42,
    "limit_tokens": 4000,
    "limit_usd": 1.5,
    "basis": {"tokens": "actual", "cost": "lower_bound"},
}

#: A value that must never reach a subscriber. Distinctive on purpose: the leak
#: assertions search the SERIALISED summary for it, so a substring that also
#: occurs in ordinary field names would make them pass for the wrong reason.
PLAUSIBLE_SECRET = "sk-live-51NEVERSHIPTHIS"


def _event(kind: str, metadata: Any = None, *, with_metadata: bool = True) -> dict:
    """One ledger row as `load_run_events` yields it."""
    event: dict[str, Any] = {
        "event": kind,
        "timestamp": "2026-08-23T00:00:00Z",
        "outcome": "",
    }
    if with_metadata:
        event["metadata"] = metadata
    return event


def _tick(metadata: Any) -> dict:
    return _event("budget.tick", metadata)


def _serialised(summary: dict) -> str:
    """The summary as a client receives it, not as a dict a test can inspect."""
    return mod.sse_event_frame(0, summary).decode()


class _Clock:
    """A hand-wound clock: the test decides what time it is."""

    def __init__(self) -> None:
        self.t = 0.0

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += seconds


def _passes(count: int) -> Any:
    """A `should_continue` that permits exactly `count` loop passes."""
    left = [count]

    def should_continue() -> bool:
        if left[0] <= 0:
            return False
        left[0] -= 1
        return True

    return should_continue


class TestEveryOtherKindIsUntouched:
    """T1 — the byte-compatibility half, and the one a later round will be
    tempted to break."""

    def test_a_non_tick_summary_is_exactly_the_five_fields_it_was(self):
        summary = mod._safe_event_summary(2, _event("task_started"))
        assert set(summary) == {"seq", "event", "timestamp", "outcome", "task_id"}
        assert set(summary) == BASE_FIELDS

    def test_a_non_tick_carrying_tick_shaped_metadata_still_gains_nothing(self):
        # The condition is on the EVENT KIND and not on the metadata's shape:
        # a widening keyed off "does this look like a tick" would be reachable
        # by any writer that happened to name a field `spent_tokens`.
        summary = mod._safe_event_summary(2, _event("task_started", FULL_TICK_METADATA))
        assert set(summary) == BASE_FIELDS
        assert "1200" not in _serialised(summary)


class TestTheTickCarriesItsFigures:
    """T2 — the feature half."""

    def test_a_tick_gains_the_payload_key_and_nothing_else(self):
        summary = mod._safe_event_summary(5, _tick(FULL_TICK_METADATA))
        assert set(summary) == BASE_FIELDS | {"budget"}
        # Discriminator: the five are still the five, unchanged in value too.
        assert summary["event"] == "budget.tick"
        assert summary["seq"] == 5

    def test_the_payload_holds_every_figure_the_metadata_carried(self):
        summary = mod._safe_event_summary(5, _tick(FULL_TICK_METADATA))
        assert summary["budget"] == FULL_TICK_METADATA

    def test_the_figures_survive_serialisation_to_the_wire(self):
        # A dict a test can read is not a frame a client receives.
        summary = mod._safe_event_summary(5, _tick(FULL_TICK_METADATA))
        payload = json.loads(_serialised(summary).split("data: ", 1)[1])
        assert payload["budget"] == FULL_TICK_METADATA


class TestTheWhitelistBlocksWhatItDoesNotName:
    """T3 and T4 — the redaction half, asserted against the SERIALISED text."""

    def test_an_unnamed_outer_field_never_reaches_the_wire(self):
        metadata = dict(FULL_TICK_METADATA, api_key=PLAUSIBLE_SECRET)
        summary = mod._safe_event_summary(5, _tick(metadata))
        text = _serialised(summary)
        # Positive control first: this tick really did carry the secret, so the
        # absence below is redaction and not an empty payload.
        assert PLAUSIBLE_SECRET in json.dumps(metadata)
        assert PLAUSIBLE_SECRET not in text
        assert "api_key" not in text
        assert "budget" in summary

    def test_an_unnamed_key_inside_basis_never_reaches_the_wire(self):
        metadata = dict(
            FULL_TICK_METADATA,
            basis={"tokens": "actual", "cost": "actual", "trace_url": PLAUSIBLE_SECRET},
        )
        summary = mod._safe_event_summary(5, _tick(metadata))
        text = _serialised(summary)
        assert PLAUSIBLE_SECRET in json.dumps(metadata)
        assert PLAUSIBLE_SECRET not in text
        assert "trace_url" not in text
        # The named basis keys DID survive: otherwise this passes because the
        # nested object was dropped whole, which is a different behaviour.
        assert summary["budget"]["basis"] == {"tokens": "actual", "cost": "actual"}


class TestAnAbsentLimitStaysAbsent:
    """T5 — no fabricated denominator survives the last hop either."""

    def test_a_limit_the_tick_never_carried_is_a_missing_key(self):
        metadata = {
            "spent_tokens": 90,
            "unmeasured_calls": 0,
            "basis": {"tokens": "actual", "cost": "absent"},
        }
        payload = mod._safe_event_summary(5, _tick(metadata))["budget"]
        assert "limit_tokens" not in payload
        assert "limit_usd" not in payload
        assert "spent_usd" not in payload
        # Not a null and not a zero: `.get` would hide exactly that failure.
        assert payload == metadata

    def test_the_missing_limit_is_missing_on_the_wire_too(self):
        metadata = {"spent_tokens": 90, "unmeasured_calls": 0}
        text = _serialised(mod._safe_event_summary(5, _tick(metadata)))
        assert "limit_tokens" not in text
        assert "limit_usd" not in text
        assert "null" not in text


class TestAMalformedTickIsNotAnError:
    """T6 — the summary runs for every event on the stream and may not fail."""

    def test_a_tick_with_no_metadata_yields_an_empty_payload(self):
        summary = mod._safe_event_summary(5, _event("budget.tick", with_metadata=False))
        assert summary["budget"] == {}
        assert set(summary) == BASE_FIELDS | {"budget"}

    def test_a_tick_whose_metadata_is_not_a_dict_yields_an_empty_payload(self):
        for junk in (None, "spent_tokens=3", ["spent_tokens", 3], 7):
            summary = mod._safe_event_summary(5, _tick(junk))
            assert summary["budget"] == {}, junk

    def test_a_tick_whose_basis_is_not_a_dict_keeps_the_outer_figures(self):
        metadata = {"spent_tokens": 90, "unmeasured_calls": 0, "basis": "actual"}
        payload = mod._safe_event_summary(5, _tick(metadata))["budget"]
        assert payload == {"spent_tokens": 90, "unmeasured_calls": 0}


class TestBothTransportsCarryTheSameTick:
    """T7 — `_safe_event_summary` has ONE writer and TWO transports, and a tick
    is not an exception to the one-envelope rule `test_sse_stream.py` pins for
    the general case."""

    def test_the_cursor_endpoint_and_the_stream_agree_on_a_tick(self, monkeypatch):
        events = [_event("task_started"), _tick(FULL_TICK_METADATA)]
        monkeypatch.setattr(mod, "_load_events", lambda job: events)

        class _Job:
            id = "11111111-2222-3333-4444-555555555555"

        polled = mod._build_events_since_json(_Job(), "0")["events"]
        clock = _Clock()
        streamed = [
            json.loads(frame.decode().split("data: ", 1)[1])
            for frame in mod.iter_sse_frames(
                lambda: events, 0, now=clock.now, sleep=clock.sleep,
                should_continue=_passes(1),
                heartbeat_seconds=15.0, poll_seconds=1.0,
            )
        ]
        assert streamed == polled
        # Discriminator: the tick's figures are actually in what was compared,
        # so this cannot pass by both transports dropping them together.
        assert polled[1]["budget"] == FULL_TICK_METADATA
        assert "budget" not in polled[0]


class TestTheWhitelistCoversTheEmitter:
    """The drift guard the two whitelists need: a figure DECISION F022 D1 adds
    to the tick and nobody adds here would be written, logged and then silently
    dropped at the envelope — the exact failure this round exists to fix."""

    @staticmethod
    def _emitted_payload() -> dict:
        from packages.orchestration.safe_points import _budget_tick_payload

        evaluation = SimpleNamespace(
            counters=SimpleNamespace(
                measured_token_total=1200,
                unmeasured_call_count=2,
                measured_cost_usd=0.42,
            ),
            configured_limits=SimpleNamespace(max_total_tokens=4000, max_cost_usd=1.5),
            token_lower_bound=False,
            cost_lower_bound=True,
        )
        return _budget_tick_payload(evaluation)

    def test_the_emitter_really_produced_a_populated_payload(self):
        # Premise first: an empty payload would make both subset checks vacuous.
        payload = self._emitted_payload()
        assert len(payload) >= 6, payload

    def test_every_key_the_emitter_writes_is_named_by_a_whitelist(self):
        payload = self._emitted_payload()
        named = set(mod.BUDGET_TICK_SUMMARY_FIELDS) | {"basis"}
        assert set(payload) <= named, sorted(set(payload) - named)
        assert set(payload["basis"]) <= set(mod.BUDGET_TICK_BASIS_FIELDS)

    def test_an_emitted_payload_crosses_the_envelope_unchanged(self):
        payload = self._emitted_payload()
        summary = mod._safe_event_summary(5, _tick(payload))
        assert summary["budget"] == payload

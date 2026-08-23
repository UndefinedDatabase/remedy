"""
Domain tests: ui_server/test_budget_final_section.py

T003b's server half. DECISION F022 D7 rules the run log's LAST `budget.tick` as
the authority for the terminal reconciliation, so the dashboard payload carries
that one tick's whitelisted figures as `budget_final`.

Three properties are pinned here: the LAST tick wins, the payload is
`_budget_tick_summary_payload`'s and nothing wider, and a job that emitted no
tick yields `None` rather than a fabricated empty figure.
"""

from __future__ import annotations

import json
from typing import Any

from packages.core.models import Job
from packages.orchestration import ui_server as mod

#: One tick's metadata in the shape `safe_points._budget_tick_payload` writes
#: it. `test_budget_tick_envelope.py` pins that shape against the live emitter;
#: this file only needs a whitelisted payload it can tell apart from another.
FIRST_TICK_METADATA: dict[str, Any] = {
    "spent_tokens": 100,
    "unmeasured_calls": 0,
    "spent_usd": 0.01,
    "limit_tokens": 4000,
    "limit_usd": 1.5,
    "basis": {"tokens": "actual", "cost": "actual"},
}

#: The job's FINAL tick. Every figure differs from the first tick's, so an
#: assertion cannot pass by reading the wrong end of the list.
LAST_TICK_METADATA: dict[str, Any] = {
    "spent_tokens": 3300,
    "unmeasured_calls": 2,
    "spent_usd": 0.99,
    "limit_tokens": 4000,
    "limit_usd": 1.5,
    "basis": {"tokens": "actual", "cost": "lower_bound"},
}

#: A value that must never reach a dashboard reader. Distinctive on purpose:
#: the leak assertion searches the SERIALISED payload for it, so a substring
#: that also occurs in ordinary field names would pass for the wrong reason.
PLAUSIBLE_SECRET = "sk-live-51NEVERSHIPTHIS"


def _event(kind: str, metadata: Any = None, *, timestamp: str = "2026-08-23T00:00:00Z") -> dict:
    """One ledger row as `load_run_events` yields it, already time-sorted."""
    return {"event": kind, "timestamp": timestamp, "outcome": "", "metadata": metadata}


def _tick(metadata: Any, *, timestamp: str = "2026-08-23T00:00:00Z") -> dict:
    return _event("budget.tick", metadata, timestamp=timestamp)


def _run_of_two_ticks() -> list[dict]:
    """A run whose ticks are separated by unrelated events, in ledger order."""
    return [
        _event("task_started", {}, timestamp="2026-08-23T00:00:00Z"),
        _tick(FIRST_TICK_METADATA, timestamp="2026-08-23T00:00:01Z"),
        _event("source_context_injected", {"estimated_tokens": 500}, timestamp="2026-08-23T00:00:02Z"),
        _tick(LAST_TICK_METADATA, timestamp="2026-08-23T00:00:03Z"),
        _event("job_completed", {}, timestamp="2026-08-23T00:00:04Z"),
    ]


class TestTheLastTickIsTheFinalFigure:
    """T1 — 'final' means the ledger's last word, not its first."""

    def test_the_later_tick_wins_over_the_earlier_one(self):
        final = mod._build_budget_final(_run_of_two_ticks())
        assert final == LAST_TICK_METADATA
        # Discriminator: the earlier tick really was in the list, so this
        # cannot pass because only one tick was ever offered.
        assert final != FIRST_TICK_METADATA
        assert final["spent_tokens"] == 3300

    def test_a_single_tick_is_its_own_final_figure(self):
        assert mod._build_budget_final([_tick(FIRST_TICK_METADATA)]) == FIRST_TICK_METADATA

    def test_events_after_the_last_tick_do_not_displace_it(self):
        events = _run_of_two_ticks() + [_event("test_run_completed", {"exit_code": 0})]
        assert mod._build_budget_final(events) == LAST_TICK_METADATA


class TestThePayloadIsTheEnvelopesOwn:
    """T2 — one whitelist, one redaction boundary, no second projection."""

    def test_the_figures_are_exactly_what_the_whitelist_returns(self):
        expected = mod._budget_tick_summary_payload(LAST_TICK_METADATA)
        assert mod._build_budget_final(_run_of_two_ticks()) == expected
        # Premise: an empty expectation would make the equality vacuous.
        assert len(expected) >= 6, expected

    def test_the_section_adds_no_field_of_its_own(self):
        final = mod._build_budget_final(_run_of_two_ticks())
        named = set(mod.BUDGET_TICK_SUMMARY_FIELDS) | {"basis"}
        assert set(final) <= named, sorted(set(final) - named)

    def test_a_tick_whose_metadata_is_not_a_dict_is_still_a_tick(self):
        # `{}` and `None` are different answers: one job emitted a tick that
        # carried nothing, the other emitted no tick at all.
        assert mod._build_budget_final([_tick("spent_tokens=3")]) == {}
        assert mod._build_budget_final([_tick(None)]) == {}


class TestTheWhitelistBlocksWhatItDoesNotName:
    """T3 — the redaction half, asserted against the SERIALISED payload."""

    def test_an_unnamed_outer_field_never_reaches_the_dashboard(self):
        metadata = dict(LAST_TICK_METADATA, api_key=PLAUSIBLE_SECRET)
        final = mod._build_budget_final([_tick(metadata)])
        text = json.dumps(final, default=str)
        # Positive control first: this tick really did carry the secret, so the
        # absence below is redaction and not an empty payload.
        assert PLAUSIBLE_SECRET in json.dumps(metadata)
        assert PLAUSIBLE_SECRET not in text
        assert "api_key" not in text
        assert final["spent_tokens"] == 3300

    def test_an_unnamed_key_inside_basis_never_reaches_the_dashboard(self):
        metadata = dict(
            LAST_TICK_METADATA,
            basis={"tokens": "actual", "cost": "actual", "trace_url": PLAUSIBLE_SECRET},
        )
        final = mod._build_budget_final([_tick(metadata)])
        text = json.dumps(final, default=str)
        assert PLAUSIBLE_SECRET not in text
        assert "trace_url" not in text
        # The named basis keys DID survive: otherwise this passes because the
        # nested object was dropped whole, which is a different behaviour.
        assert final["basis"] == {"tokens": "actual", "cost": "actual"}


class TestAnAbsentFigureStaysAbsent:
    """T4 — a job with no tick has no final figure, and says so."""

    def test_a_run_with_no_tick_yields_none(self):
        events = [_event("task_started", {}), _event("job_completed", {})]
        assert mod._build_budget_final(events) is None

    def test_an_empty_run_yields_none(self):
        assert mod._build_budget_final([]) is None

    def test_it_is_none_and_not_an_empty_object_or_a_zero(self):
        final = mod._build_budget_final([_event("task_started", {})])
        assert final is None
        assert final != {}
        assert final != 0

    def test_a_tick_shaped_event_of_another_kind_is_not_a_tick(self):
        # The match is on the EVENT KIND: a widening keyed off "does this look
        # like a tick" would be reachable by any writer naming a field.
        events = [_event("token_budget_report", LAST_TICK_METADATA)]
        assert mod._build_budget_final(events) is None


class TestTheDashboardCarriesTheSection:
    """T5 — the payload key itself, because a builder nobody calls ships
    nothing."""

    def test_the_dashboard_carries_the_final_figure(self, monkeypatch):
        events = _run_of_two_ticks()
        monkeypatch.setattr(mod, "_load_events", lambda job: events)
        dash = mod._build_dashboard(Job(name="budget-final"))
        assert dash["budget_final"] == LAST_TICK_METADATA

    def test_the_addition_left_the_estimate_beside_it_alone(self, monkeypatch):
        events = _run_of_two_ticks()
        monkeypatch.setattr(mod, "_load_events", lambda job: events)
        dash = mod._build_dashboard(Job(name="budget-final"))
        # The two are DIFFERENT quantities and the reconciliation authority is
        # the tick: `token_usage` stays the estimate it always was.
        assert dash["token_usage"]["estimated"] is True
        assert dash["token_usage"]["total_tokens"] == 500
        assert dash["budget_final"]["spent_tokens"] == 3300

    def test_a_job_with_no_tick_carries_the_key_holding_none(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: [_event("task_started", {})])
        dash = mod._build_dashboard(Job(name="budget-final"))
        assert "budget_final" in dash
        assert dash["budget_final"] is None

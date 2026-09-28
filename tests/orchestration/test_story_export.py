"""Domain tests: orchestration/test_story_export.py

F039 T003 (DECISION F039 D7) — `build_story_payload` assembles one job's whole
story from the cockpit's own builders and nothing else: `_build_dashboard`,
`_load_events` and `_safe_event_summary` (packages/orchestration/ui_server.py)
and `ownership_view` (packages/orchestration/ownership_phrases.py). `_load_events`
is patched to a fixed three-event stream so the payload is asserted against a
known ledger rather than a live job's own history, and the budget tick carries
a secret-looking field to prove `_safe_event_summary`'s redaction boundary
still applies inside a story.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from packages.orchestration import ui_server as mod
from packages.orchestration.ownership_phrases import ownership_view
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.story_export import (
    STORY_DASHBOARD_SECTIONS,
    STORY_EXPORT_SCHEMA,
    build_story_payload,
)

REPO_ROOT = Path(__file__).resolve().parents[2]

#: A value that must never reach the payload's `repr` — the same discriminator
#: `tests/ui_server/test_budget_final_section.py` uses for the same reason: a
#: substring that also occurs in ordinary field names would pass for the wrong
#: reason.
PLAUSIBLE_SECRET = "sk-secret"


def _event(kind: str, metadata: Any = None, *, task_id: str = "", outcome: str = "",
           timestamp: str = "2026-09-29T00:00:00Z") -> dict:
    return {"event": kind, "timestamp": timestamp, "outcome": outcome, "task_id": task_id,
            "metadata": metadata or {}}


def _three_events() -> list[dict]:
    return [
        _event("task_run_started", {"attempt_id": "attempt-1"}, task_id="t1"),
        _event("budget.tick", {"spent_usd": 0.5, "api_key": PLAUSIBLE_SECRET}),
        _event("task_run_completed", {}, task_id="t1", outcome="pass"),
    ]


def _job() -> JobPlan:
    return JobPlan(job_title="story-export", tasks=[TaskEntry(task_id="t1", title="Deliver the change")])


class TestThePayloadIsTheCockpitsOwnBuilders:
    """T1 — every part of the payload is read from the cockpit's own routes."""

    def test_the_payload_holds_exactly_the_five_keys(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        payload = build_story_payload(_job())
        assert set(payload) == {"schema", "job_id", "dashboard", "frames", "ownership"}

    def test_the_schema_and_job_id(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        job = _job()
        payload = build_story_payload(job)
        assert payload["schema"] == STORY_EXPORT_SCHEMA
        assert payload["job_id"] == str(job.job_id)

    def test_the_dashboard_equals_the_three_sections_of_build_dashboard(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        job = _job()
        payload = build_story_payload(job)
        full = mod._build_dashboard(job)
        assert payload["dashboard"] == {key: full[key] for key in STORY_DASHBOARD_SECTIONS}
        # A LITERAL expectation, never derived from STORY_DASHBOARD_SECTIONS itself:
        # a mutation that widens that tuple must still be caught here, not vacuously
        # agree with the same widened tuple on both sides of the comparison above.
        assert set(payload["dashboard"]) == {"tasks", "live", "story"}

    def test_the_frames_equal_safe_event_summary_of_each_event_seqs_0_1_2(self, monkeypatch):
        events = _three_events()
        monkeypatch.setattr(mod, "_load_events", lambda job: events)
        payload = build_story_payload(_job())
        expected = [{"seq": i, "event": mod._safe_event_summary(i, e)} for i, e in enumerate(events)]
        assert payload["frames"] == expected
        assert [f["seq"] for f in payload["frames"]] == [0, 1, 2]

    def test_the_ownership_matches_ownership_view_and_its_schema(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        job = _job()
        payload = build_story_payload(job)
        assert payload["ownership"] == ownership_view(job)
        assert payload["ownership"]["schema"] == "remedy.ownership.v1"


class TestTheSecretNeverReachesTheStory:
    """T2 — the redaction boundary `_safe_event_summary` already enforces
    survives being read through this module too."""

    def test_the_secret_and_its_field_name_occur_nowhere_in_the_payloads_repr(self, monkeypatch):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        payload = build_story_payload(_job())
        text = repr(payload)
        assert PLAUSIBLE_SECRET not in text
        assert "api_key" not in text


class TestTheTypeScriptConstantMatches:
    """T3 — the guard holding the schema to one string in both languages."""

    def test_storyexport_ts_pins_the_same_schema_string(self):
        source = (REPO_ROOT / "apps/ui/src/components/story/storyExport.ts").read_text(encoding="utf-8")
        match = re.search(r'export const STORY_EXPORT_SCHEMA = "([^"]+)";', source)
        assert match is not None, "STORY_EXPORT_SCHEMA not found in storyExport.ts"
        assert match.group(1) == STORY_EXPORT_SCHEMA

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

import json
import re
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration import ui_server as mod
from packages.orchestration.config import get_key_spec
from packages.orchestration.ownership_phrases import ownership_view
from packages.orchestration.pingpong_job import JobPlan, TaskEntry
from packages.orchestration.story_export import (
    STORY_DASHBOARD_SECTIONS,
    STORY_EXPORT_SCHEMA,
    StoryExportError,
    build_story_payload,
    export_story_html,
    read_story_player,
    render_story_html,
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


def _write_player(directory: Path, *, script: str = "console.log('story player');",
                  style: str = "body { margin: 0; }") -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "story-player.js").write_text(script, encoding="utf-8")
    (directory / "story-player.css").write_text(style, encoding="utf-8")


class TestReadStoryPlayer:
    """S3 (DECISION F039 D8) — the built player is read whole, or refused."""

    def test_a_missing_player_raises_story_player_missing(self, tmp_path):
        with pytest.raises(StoryExportError) as excinfo:
            read_story_player(tmp_path / "absent")
        assert excinfo.value.error == "story_player_missing"
        assert "npm install" in excinfo.value.message
        assert "npm run build" in excinfo.value.message

    def test_a_script_holding_its_own_closing_tag_raises_story_player_unsafe(self, tmp_path):
        _write_player(tmp_path, script="console.log('</SCRIPT>');")
        with pytest.raises(StoryExportError) as excinfo:
            read_story_player(tmp_path)
        assert excinfo.value.error == "story_player_unsafe"

    def test_a_style_holding_its_own_closing_tag_raises_story_player_unsafe(self, tmp_path):
        _write_player(tmp_path, style="/* </STYLE> */")
        with pytest.raises(StoryExportError) as excinfo:
            read_story_player(tmp_path)
        assert excinfo.value.error == "story_player_unsafe"

    def test_a_built_player_reads_back_verbatim(self, tmp_path):
        _write_player(tmp_path, script="const x = 1;", style="body{color:red}")
        script, style = read_story_player(tmp_path)
        assert script == "const x = 1;"
        assert style == "body{color:red}"


def _page_payload(**overrides: Any) -> dict[str, Any]:
    payload = {"schema": "remedy.story.v1", "job_id": "job-1", "dashboard": {}, "frames": [], "ownership": None}
    payload.update(overrides)
    return payload


class TestRenderStoryHtml:
    """S3 (DECISION F039 D8) — the one page around the built player."""

    def test_the_embedded_json_parses_back_to_the_payload(self):
        payload = _page_payload()
        page = render_story_html(payload, "const s = 1;", "body{}")
        match = re.search(
            r'<script type="application/json" id="remedy-story-data">(.*?)</script>', page, re.DOTALL)
        assert match is not None
        assert json.loads(match.group(1)) == payload

    def test_a_payload_string_holding_a_closing_script_tag_never_closes_it_early(self):
        payload = _page_payload(job_id="</script><b>")
        page = render_story_html(payload, "const s = 1;", "body{}")
        assert page.lower().count("</script") == 2

    def test_the_style_and_script_appear_verbatim_inside_their_elements(self):
        script = "const s = window.__never_reached__;"
        style = "body { color: var(--remedy-ink); }"
        page = render_story_html(_page_payload(), script, style)
        assert f"<style>{style}</style>" in page
        assert f'<script type="module">{script}</script>' in page

    def test_the_policy_holds_default_src_none(self):
        page = render_story_html(_page_payload(), "const s = 1;", "body{}")
        assert "default-src 'none'" in page

    def test_a_job_id_with_markup_titles_the_page_escaped(self):
        page = render_story_html(_page_payload(job_id="<j&1>"), "const s = 1;", "body{}")
        assert "<title>Remedy story of job &lt;j&amp;1&gt;</title>" in page


class TestExportStoryHtml:
    """S3 (DECISION F039 D8) — the whole export, budgeted."""

    def test_export_at_exactly_its_own_length_returns_the_same_bytes_and_refuses_one_byte_less(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setattr(mod, "_load_events", lambda job: _three_events())
        _write_player(tmp_path)
        job = _job()
        data = export_story_html(job, max_bytes=10_000_000, player_dir=tmp_path)
        again = export_story_html(job, max_bytes=len(data), player_dir=tmp_path)
        assert again == data
        with pytest.raises(StoryExportError) as excinfo:
            export_story_html(job, max_bytes=len(data) - 1, player_dir=tmp_path)
        assert excinfo.value.error == "story_too_large"
        assert str(len(data)) in excinfo.value.message
        assert str(len(data) - 1) in excinfo.value.message
        assert "story.export_max_bytes" in excinfo.value.message


class TestTheExportMaxBytesKey:
    """S3 — the budget's own registered key."""

    def test_the_default_is_five_million_bytes(self):
        assert get_key_spec("story.export_max_bytes").default == 5_000_000

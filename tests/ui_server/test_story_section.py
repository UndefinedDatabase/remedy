"""
Domain tests: ui_server/test_story_section.py

F039 T002, DECISION F039 D5. The story's autoplay pacing reaches the browser
as the dashboard's `story` section: `_build_story_section` reads the two
configuration keys, `story.step_ms` and `story.chapter_pause_ms`, on every
call from the process's configuration, which `get_config` loads once and
keeps, so a change takes effect when the cockpit restarts (R-1100); and
`_build_dashboard` carries that section under `story`.
"""

from __future__ import annotations

from packages.orchestration import ui_server as mod
from packages.orchestration.config import reset_config
from packages.orchestration.pingpong_job import JobPlan


def test_the_section_reads_the_defaults_with_both_variables_unset(monkeypatch):
    monkeypatch.delenv("REMEDY_STORY_STEP_MS", raising=False)
    monkeypatch.delenv("REMEDY_STORY_CHAPTER_PAUSE_MS", raising=False)
    reset_config()
    try:
        assert mod._build_story_section() == {"step_ms": 420, "chapter_pause_ms": 1600}
    finally:
        reset_config()


def test_the_section_reads_the_configured_values_when_both_are_set(monkeypatch):
    monkeypatch.setenv("REMEDY_STORY_STEP_MS", "300")
    monkeypatch.setenv("REMEDY_STORY_CHAPTER_PAUSE_MS", "2500")
    reset_config()
    try:
        assert mod._build_story_section() == {"step_ms": 300, "chapter_pause_ms": 2500}
    finally:
        reset_config()


def test_the_dashboard_carries_the_section(monkeypatch):
    monkeypatch.setattr(mod, "_load_events", lambda job: [])
    dash = mod._build_dashboard(JobPlan(job_title="story-section"))
    assert dash["story"] == mod._build_story_section()


def test_a_changed_variable_takes_effect_only_after_reset_config_r1100(monkeypatch):
    monkeypatch.delenv("REMEDY_STORY_STEP_MS", raising=False)
    reset_config()
    try:
        assert mod._build_story_section()["step_ms"] == 420
        monkeypatch.setenv("REMEDY_STORY_STEP_MS", "900")
        assert mod._build_story_section()["step_ms"] == 420
        reset_config()
        assert mod._build_story_section()["step_ms"] == 900
    finally:
        monkeypatch.delenv("REMEDY_STORY_STEP_MS", raising=False)
        reset_config()

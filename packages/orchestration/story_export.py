"""F039 T003 (DECISION F039 D7) — the story's DATA half: one job's story payload,
built from the cockpit's own builders and nothing else. Remedy deliberately
exports nothing the cockpit's own routes do not already serve: the dashboard
section, the event frames and the ownership view are each read through the
exact function the browser already calls, so a story file can never diverge
from what the live cockpit would have shown for the same job.

`build_story_payload` is the ONE function here. It imports `ownership_view`
(`packages/orchestration/ownership_phrases.py`) and `_build_dashboard`,
`_load_events` and `_safe_event_summary` (`packages/orchestration/ui_server.py`)
function-scoped, exactly as `ownership_phrases.py`'s own `ownership_view`
imports `build_ownership_ledger` function-scoped — the pattern this module
mirrors rather than reinvents.
"""
from __future__ import annotations

from typing import Any

__all__ = [
    "STORY_EXPORT_SCHEMA",
    "STORY_DASHBOARD_SECTIONS",
    "build_story_payload",
]

#: The one schema string both language halves pin: this module's writer and
#: `apps/ui/src/components/story/storyExport.ts`'s reader
#: (`tests/orchestration/test_story_export.py` guards the two stay equal).
STORY_EXPORT_SCHEMA = "remedy.story.v1"

#: The dashboard keys a story carries — the task list, the live state and the
#: story pacing section — never the whole dashboard, which holds figures (proof
#: chain paths, evidence directories) a self-contained export has no business
#: repeating.
STORY_DASHBOARD_SECTIONS = ("tasks", "live", "story")


def build_story_payload(job: Any) -> dict[str, Any]:
    """S2 — one job's story payload: `{"schema", "job_id", "dashboard", "frames",
    "ownership"}`. `dashboard` is `STORY_DASHBOARD_SECTIONS` of `_build_dashboard(job)`;
    `frames` is every event `_load_events(job)` holds, each through
    `_safe_event_summary`, with `seq` counted from 0; `ownership` is `ownership_view(job)`
    unchanged. Every part comes from the cockpit's own builders, so a story file holds
    nothing the cockpit does not already serve.
    """
    from packages.orchestration.ownership_phrases import ownership_view
    from packages.orchestration.ui_server import _build_dashboard, _load_events, _safe_event_summary

    dashboard = _build_dashboard(job)
    return {
        "schema": STORY_EXPORT_SCHEMA,
        "job_id": str(job.job_id),
        "dashboard": {key: dashboard[key] for key in STORY_DASHBOARD_SECTIONS},
        "frames": [
            {"seq": seq, "event": _safe_event_summary(seq, event)}
            for seq, event in enumerate(_load_events(job))
        ],
        "ownership": ownership_view(job),
    }

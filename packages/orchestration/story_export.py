"""F039 T003 (DECISION F039 D7) — the story's DATA half: one job's story payload,
built from the cockpit's own builders and nothing else. Remedy deliberately
exports nothing the cockpit's own routes do not already serve: the dashboard
section, the event frames and the ownership view are each read through the
exact function the browser already calls, so a story file can never diverge
from what the live cockpit would have shown for the same job.

`build_story_payload` builds the payload (DECISION F039 D7); `export_story_html` writes it
into ONE page around the built player (DECISION F039 D8). `build_story_payload` imports
`ownership_view` (`packages/orchestration/ownership_phrases.py`) and `_build_dashboard`,
`_load_events` and `_safe_event_summary` (`packages/orchestration/ui_server.py`)
function-scoped, exactly as `ownership_phrases.py`'s own `ownership_view`
imports `build_ownership_ledger` function-scoped — the pattern this module
mirrors rather than reinvents.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

__all__ = [
    "STORY_EXPORT_SCHEMA",
    "STORY_DASHBOARD_SECTIONS",
    "STORY_DATA_ELEMENT_ID",
    "STORY_PLAYER_DIR",
    "StoryExportError",
    "build_story_payload",
    "read_story_player",
    "render_story_html",
    "export_story_html",
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

#: The exported page's own element id (F039 T003, DECISION F039 D8): the one place
#: `render_story_html` writes the payload's JSON and the one place
#: `apps/ui/src/storyPlayerMain.tsx` reads it back. Pinned equal in both languages by
#: `tests/orchestration/test_story_export.py`.
STORY_DATA_ELEMENT_ID = "remedy-story-data"

#: Where the story player's second `vite build` (DECISION F039 D8, `apps/ui/vite.config.ts`'s
#: `storyPlayerBuild` plugin) writes `story-player.js` and `story-player.css`. Resolved from
#: `__file__` rather than the process's own cwd, so `read_story_player` finds the built player
#: regardless of where `remedy` is invoked from.
STORY_PLAYER_DIR = Path(__file__).resolve().parents[2] / "apps" / "ui" / "dist" / "story"


class StoryExportError(Exception):
    """The export could not be produced. Nothing was written (DECISION F039 D8).

    `error` is the stable machine token `apps/cli/commands/job_story_cmd.py` maps to an exit
    code; `message` is the sentence a human reads.
    """

    def __init__(self, error: str, message: str) -> None:
        super().__init__(message)
        self.error = error
        self.message = message


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


def read_story_player(player_dir: Path | None = None) -> tuple[str, str]:
    """Read the story player's built script and style sheet (DECISION F039 D8).

    `player_dir` defaults to `STORY_PLAYER_DIR`, read AT CALL TIME (never bound into a
    default parameter value) so a caller — or a test — that patches the module attribute
    is read, not a stale copy taken when this function was defined.

    Raises `StoryExportError("story_player_missing", ...)` when either file is not a
    regular file, naming the build command that produces them, and
    `StoryExportError("story_player_unsafe", ...)` when the script holds its own `</script`
    (any case) or the style holds its own `</style` (any case) — either one would let the
    built player's own text close the element `render_story_html` inlines it into.
    """
    directory = STORY_PLAYER_DIR if player_dir is None else player_dir
    script_path = directory / "story-player.js"
    style_path = directory / "story-player.css"
    if not script_path.is_file() or not style_path.is_file():
        raise StoryExportError(
            "story_player_missing",
            f"The story player is not built at {directory}; run `cd apps/ui && npm install "
            f"&& npm run build` and export again.",
        )
    script = script_path.read_text(encoding="utf-8")
    style = style_path.read_text(encoding="utf-8")
    if "</script" in script.lower():
        raise StoryExportError(
            "story_player_unsafe",
            "The built story player's own script holds a `</script` tag; refusing to "
            "inline it into the exported page.",
        )
    if "</style" in style.lower():
        raise StoryExportError(
            "story_player_unsafe",
            "The built story player's own style holds a `</style` tag; refusing to "
            "inline it into the exported page.",
        )
    return script, style


def render_story_html(payload: dict[str, Any], script: str, style: str) -> str:
    """The exported page of DECISION F039 D8 (3): one HTML document with no request of its
    own. The content security policy allows no `default-src` at all, inline script and style
    only; the payload is written as JSON with every `<` replaced by `\\u003c`, so a story
    string that itself reads `</script>` can never close the element early; the built
    player's script and style are inlined verbatim (`read_story_player` already refused a
    built player carrying its own closing tag).
    """
    job_id = html.escape(str(payload.get("job_id", "")))
    payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True).replace("<", "\\u003c")
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:\">\n"
        f"<title>Remedy story of job {job_id}</title>\n"
        f"<style>{style}</style>\n"
        "</head>\n"
        "<body>\n"
        '<div id="root" data-ui="remedy-story"></div>\n'
        f'<script type="application/json" id="{STORY_DATA_ELEMENT_ID}">{payload_json}</script>\n'
        f'<script type="module">{script}</script>\n'
        "</body>\n"
        "</html>\n"
    )


def export_story_html(job: Any, *, max_bytes: int, player_dir: Path | None = None) -> bytes:
    """The whole export (DECISION F039 D8): `build_story_payload(job)` rendered around the
    built player, as UTF-8 bytes. Refuses whole — never cuts a story — when the page is
    larger than `max_bytes` (`story.export_max_bytes`), naming both numbers, the key and
    that nothing was written.
    """
    script, style = read_story_player(player_dir)
    payload = build_story_payload(job)
    page = render_story_html(payload, script, style)
    data = page.encode("utf-8")
    if len(data) > max_bytes:
        raise StoryExportError(
            "story_too_large",
            f"The story is {len(data)} bytes, over the `story.export_max_bytes` budget of "
            f"{max_bytes} bytes; nothing was written.",
        )
    return data

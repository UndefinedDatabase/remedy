"""F039 T003, DECISION F039 D8 — the story player built a second time, and the page that
reads it back.

`vite.config.ts`'s own build plugin, `storyPlayerMain.tsx` and `StoryPlayerApp.tsx` are never
exercised by vitest — one is a build-time plugin `closeBundle()` runs once the cockpit's own
build closes, and the other two need a mounted DOM this repository's node-environment vitest
config does not provide (the same reason `StoryPanel.tsx` is pinned as source, DECISION F039
D6). Assertions below therefore run against COMMENT-STRIPPED source, exactly as
`test_story_panel_contract.py` reads `StoryPanel.tsx`.
"""
from __future__ import annotations

import re
from pathlib import Path

from packages.orchestration import story_export
from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI = REPO_ROOT / "apps" / "ui"
UI_SRC = UI / "src"
STORY = UI_SRC / "components" / "story"

VITE_CONFIG = UI / "vite.config.ts"
STORY_PLAYER_MAIN = UI_SRC / "storyPlayerMain.tsx"
STORY_PLAYER_APP = STORY / "StoryPlayerApp.tsx"
STORY_PANEL = STORY / "StoryPanel.tsx"
STORY_EXPORT_TS = STORY / "storyExport.ts"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_build_plugin_names_the_second_builds_own_shape():
    source = _source(VITE_CONFIG)
    for literal in (
        'apply: "build"',
        "configFile: false",
        'input: "src/storyPlayerMain.tsx"',
        "inlineDynamicImports: true",
        'entryFileNames: "story-player.js"',
        'assetFileNames: "story-player[extname]"',
        'STORY_PLAYER_OUT_DIR = "dist/story"',
    ):
        assert literal in source, f"vite.config.ts is missing {literal!r}"


def test_story_player_dir_equals_the_out_dir_under_apps_ui():
    assert story_export.STORY_PLAYER_DIR == UI / "dist" / "story"


def test_the_pages_entry_reads_the_page_and_calls_no_network():
    source = _source(STORY_PLAYER_MAIN)
    assert "readEmbeddedStory(" in source
    assert "getElementById(STORY_DATA_ELEMENT_ID)" in source
    for forbidden in ("fetch(", "EventSource", "WebSocket", "XMLHttpRequest"):
        assert forbidden not in source, f"storyPlayerMain.tsx reaches for {forbidden}"


def test_the_player_app_wires_one_scrub_into_the_timeline_and_the_panel():
    source = _source(STORY_PLAYER_APP)
    assert source.count("useTimelineScrub(") == 1
    assert "<PhaseTimeline scrub={scrub} />" in source
    panel_lines = [line for line in source.splitlines() if "<StoryPanel" in line]
    assert len(panel_lines) == 1, "expected exactly one StoryPanel element"
    assert "scrub={scrub}" in panel_lines[0]
    assert "onClose" not in panel_lines[0]


def test_the_panel_takes_onclose_as_optional_with_a_conditional_close_button():
    source = _source(STORY_PANEL)
    assert "onClose?: () => void;" in source
    assert '{onClose && <button type="button" onClick={onClose}>Close story</button>}' in source


def test_the_typescript_element_id_equals_the_python_one():
    source = STORY_EXPORT_TS.read_text(encoding="utf-8")
    match = re.search(r'export const STORY_DATA_ELEMENT_ID = "([^"]+)";', source)
    assert match is not None, "STORY_DATA_ELEMENT_ID not found in storyExport.ts"
    assert match.group(1) == story_export.STORY_DATA_ELEMENT_ID

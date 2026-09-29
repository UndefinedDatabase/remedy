"""F039 T002's in-app story panel, pinned as source (DECISION F039 D6).

`StoryPanel.tsx` cannot be rendered by this repository's vitest config (no DOM harness
exists for it, the reason `TourOverlay.tsx` and `LessonsOverlay.tsx` are pinned this same
way — DECISION F031 D5). Assertions run against COMMENT-STRIPPED source, or prose above a
definition would satisfy a guard meant for the code (finding R-0584, the reason
`test_tour_overlay_contract.py` and `test_main_layout_guard.py` already read this way).
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments
from tests.ui_contracts.test_phase_mapping import ts_import_specifiers

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
STORY = UI_SRC / "components" / "story"
PANEL = STORY / "StoryPanel.tsx"
PANEL_CSS = STORY / "StoryPanel.module.css"
PLAYER = STORY / "storyPlayer.ts"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
RIGHT_PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"

#: storyPlayer.ts's own three specifiers, in S2's own order.
EXPECTED_SPECIFIERS = ["./storyAutoplay", "./storyNarration", "./storyView"]

#: Same set `test_story_view.py` pins for storyView.ts's own purity.
PURITY_WORDS = ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch(", "React")

_RAW_COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(")


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_panel_is_a_region_portaled_to_the_document_body():
    source = _source(PANEL)
    assert "createPortal(" in source
    assert "document.body" in source
    assert 'data-ui="story-panel"' in source
    assert 'role="region"' in source


def test_the_panel_drives_the_real_scrub_and_reads_reduced_motion():
    source = _source(PANEL)
    assert "autoplayStep(" in source
    assert "buildStoryView(" in source
    assert "useReducedMotion()" in source


def test_the_panel_owns_exactly_one_timer_and_reads_no_door():
    source = _source(PANEL)
    assert source.count("window.setTimeout(") == 1
    assert "window.clearTimeout(" in source
    assert "fetch(" not in source


def test_the_timer_reads_the_latest_view_through_a_ref_and_never_scrub_or_view_bare_r1101():
    source = _source(PANEL)
    assert "}, [playing, position, reducedMotion, scrubTo]);" in source
    assert "viewRef.current" in source
    timer = re.search(
        r"if \(!playing\) return;.*?\}, \[playing, position, reducedMotion, scrubTo\]\);",
        source,
        re.DOTALL,
    )
    assert timer is not None, "expected the timer effect's own body"
    body = timer.group(0)
    assert re.search(r"\bscrub\b", body) is None, "the timer's dependency list still names `scrub` bare"
    assert re.search(r"\bview\b", body) is None, "the timer's dependency list still names `view` bare"


def test_the_css_module_names_the_overlay_layer_and_the_replay_violet_with_no_raw_colour():
    css = PANEL_CSS.read_text(encoding="utf-8")
    assert "var(--remedy-z-overlay)" in css
    assert "var(--remedy-purple)" in css
    assert not _RAW_COLOUR.search(css), "StoryPanel.module.css carries a raw colour literal"


def test_story_player_imports_exactly_the_three_of_s2_and_is_pure():
    source = _source(PLAYER)
    assert ts_import_specifiers(source) == EXPECTED_SPECIFIERS
    for word in PURITY_WORDS:
        assert word not in source, f"storyPlayer.ts reaches for {word}"


def test_the_shell_mounts_the_panel_outside_main_with_the_scrub():
    source = _source(SHELL)
    assert source.index("</main>") < source.index("<StoryPanel")
    assert "onOpenStory={() => setStoryOpen(true)}" in source
    element = [line for line in source.splitlines() if "<StoryPanel" in line]
    assert len(element) == 1, "expected exactly one StoryPanel element"
    assert "scrub={scrub}" in element[0]


def test_the_right_panel_holds_the_story_button():
    source = _source(RIGHT_PANEL)
    assert ('{onOpenStory && (<button type="button" className={styles.advancedToggle} '
            'onClick={onOpenStory}>Story</button>)}') in source

"""F039 T002 — the story's whole view, DECISION F039 D5.

`apps/ui/src/components/story/storyView.ts` assembles a job's story from its ledger
rows, its task seeds, its ownership view and the browser's own pacing payload — the
dashboard's `story` section `_build_story_section` in `packages/orchestration/ui_server.py`
serves and `packages/orchestration/config.py` describes through two keys,
`story.step_ms` and `story.chapter_pause_ms`. The vitest goldens in `storyView.test.ts`
cannot read the Python side of that binding, so this guard pins: the section's own two
keys against the literals `storyAutoplay.ts` reads them by, each key's registered
default against the constant `storyAutoplay.ts` falls back to, the module's imports
and its purity, and that `feedRow.ts` reads the budget tick reader this round wires in.
"""
from __future__ import annotations

import re
from pathlib import Path

from packages.orchestration import ui_server as mod
from packages.orchestration.config import get_key_spec
from tests.ui_contracts.test_phase_mapping import ts_import_specifiers

ROOT = Path(__file__).resolve().parent.parent.parent
STORY = ROOT / "apps" / "ui" / "src" / "components" / "story"
MODULE = STORY / "storyView.ts"
AUTOPLAY = STORY / "storyAutoplay.ts"
FEED_ROW = ROOT / "apps" / "ui" / "src" / "api" / "feedRow.ts"

EXPECTED_SPECIFIERS = [
    "../../api/costMetric",
    "../../api/ownership",
    "../graph/brainOntology",
    "../timeline/phaseMapping",
    "./storyAutoplay",
    "./storyChapters",
    "./storyNarration",
]

PURITY_WORDS = ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch(", "React")


def _strip_comments(src: str) -> str:
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.DOTALL)


def _constant(src: str, name: str) -> int:
    match = re.search(rf"^export const {name} = (\d+);$", src, re.MULTILINE)
    assert match, f"storyAutoplay.ts declares no `export const {name}`"
    return int(match.group(1))


def test_the_section_reads_exactly_the_two_keys_storyautoplay_reads_by():
    autoplay_src = _strip_comments(AUTOPLAY.read_text(encoding="utf-8"))
    assert set(mod._build_story_section()) == {"step_ms", "chapter_pause_ms"}
    for literal in ('"step_ms"', '"chapter_pause_ms"'):
        assert literal in autoplay_src, f"storyAutoplay.ts never reads {literal}"


def test_each_keys_default_equals_storyautoplays_own_constant():
    autoplay_src = _strip_comments(AUTOPLAY.read_text(encoding="utf-8"))
    step_spec = get_key_spec("story.step_ms")
    pause_spec = get_key_spec("story.chapter_pause_ms")
    assert step_spec is not None and pause_spec is not None
    assert step_spec.default == _constant(autoplay_src, "STORY_STEP_MS")
    assert pause_spec.default == _constant(autoplay_src, "STORY_CHAPTER_PAUSE_MS")


def test_the_module_imports_exactly_the_seven_specifiers_of_s4_and_is_pure():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    assert ts_import_specifiers(src) == EXPECTED_SPECIFIERS
    for word in PURITY_WORDS:
        assert word not in src, f"storyView.ts reaches for {word}"


def test_feed_row_holds_the_budget_tick_reader():
    src = _strip_comments(FEED_ROW.read_text(encoding="utf-8"))
    assert "budgetTickFiguresOf(frame)" in src

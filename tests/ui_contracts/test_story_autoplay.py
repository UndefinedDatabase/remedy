"""T5_F039.md T002, DECISION F039 D4 — the autoplay module's pacing is bound to the design
reference's motion tokens and its imports stay to the two named modules; the vitest
environment reads neither CSS nor Python, so this guard holds both bindings and the
module's purity, the way `test_timeline_scrub_contract.py` holds them for the scrubber.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_phase_mapping import ts_import_specifiers

ROOT = Path(__file__).resolve().parent.parent.parent
STORY = ROOT / "apps" / "ui" / "src" / "components" / "story"
AUTOPLAY = STORY / "storyAutoplay.ts"
TOKENS = ROOT / "docs" / "ui" / "design_reference" / "tokens.css"


def _code(path: Path) -> str:
    # Comments are stripped first, so a WHY comment naming a word cannot satisfy or
    # trip a guard about the code (finding R-0584).
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)


def test_the_step_is_the_birth_motion_token():
    token = re.search(r"--remedy-dur-birth:\s*(\d+)ms;", TOKENS.read_text(encoding="utf-8"))
    assert token, "the design reference no longer defines --remedy-dur-birth"
    step = re.search(r"^export const STORY_STEP_MS = (\d+);$", _code(AUTOPLAY), re.MULTILINE)
    assert step and step.group(1) == token.group(1)


def test_the_chapter_pause_is_the_pulse_motion_token():
    token = re.search(r"--remedy-dur-pulse:\s*(\d+)ms;", TOKENS.read_text(encoding="utf-8"))
    assert token, "the design reference no longer defines --remedy-dur-pulse"
    pause = re.search(r"^export const STORY_CHAPTER_PAUSE_MS = (\d+);$", _code(AUTOPLAY), re.MULTILINE)
    assert pause and pause.group(1) == token.group(1)


def test_the_module_imports_only_the_two_named_modules():
    assert sorted(set(ts_import_specifiers(_code(AUTOPLAY)))) == ["./storyChapters", "./storyNarration"]


def test_the_module_calls_chapterAt():
    assert "chapterAt(" in _code(AUTOPLAY)


def test_the_module_stays_pure():
    src = _code(AUTOPLAY)
    for word in ("Date", "performance.", "setTimeout", "setInterval", "requestAnimationFrame",
                 "Math.random", "window.", "document.", "fetch("):
        assert word not in src, f"storyAutoplay.ts reaches for {word}"

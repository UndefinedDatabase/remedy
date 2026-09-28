"""F039 T001 — the story's chapters, DECISION F039 D1.

`apps/ui/src/components/story/storyChapters.ts` chapters a job's event ledger by the phase
bar's own reading (`readPhases`, `TIMELINE_PHASES`) and its key events (`extractSubGlyphs`),
both from `apps/ui/src/components/timeline/phaseMapping.ts`. The vitest goldens in
`storyChapters.test.ts` cannot read the phase bar's own table, so this guard pins the title
table to it, and pins the module's imports, its two library calls and its purity — no clock,
no DOM, no invented sentence — the way `test_phase_mapping.py` pins `phaseMapping.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TIMELINE = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "phaseMapping.ts"
MODULE = ROOT / "apps" / "ui" / "src" / "components" / "story" / "storyChapters.ts"

EXPECTED_TITLES = {
    "job": "The start",
    "planning": "The plan",
    "build": "The build",
    "test": "The tests",
    "review": "The review",
    "finalized": "The finish",
}


def _strip_comments(src: str) -> str:
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.DOTALL)


def _phases(src: str, name: str) -> list[str]:
    match = re.search(rf"{name}[^=]*= \[(.*?)\];", src, re.DOTALL)
    assert match, f"no `{name}` list"
    return re.findall(r'"([a-z]+)"', match.group(1))


def _title_table_block(src: str) -> re.Match[str]:
    match = re.search(r"^export const STORY_CHAPTER_TITLES: [^=]+= \{\n(.*?)^\};$", src, re.MULTILINE | re.DOTALL)
    assert match, "storyChapters.ts declares no `export const STORY_CHAPTER_TITLES` table"
    return match


def _title_table(src: str) -> dict[str, str]:
    block = _title_table_block(src)
    entries = re.findall(r'^  ([a-z]+): "([^"]*)",$', block.group(1), re.MULTILINE)
    assert len(entries) == len(block.group(1).strip().splitlines()), "STORY_CHAPTER_TITLES has a line of another shape"
    return dict(entries)


def test_the_title_table_s_keys_are_the_bar_s_phases_in_order():
    module_src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    bar_phases = _phases(TIMELINE.read_text(encoding="utf-8"), "export const TIMELINE_PHASES")
    table = _title_table(module_src)
    assert list(table.keys()) == bar_phases


def test_the_title_table_s_values_are_the_six_titles():
    table = _title_table(_strip_comments(MODULE.read_text(encoding="utf-8")))
    assert table == EXPECTED_TITLES


def test_the_module_imports_exactly_the_two_specifiers_of_s1():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    imports = re.findall(r'^import [^;]*from "([^"]+)";$', src, re.MULTILINE)
    assert sorted(set(imports)) == ["../graph/brainOntology", "../timeline/phaseMapping"]


def test_the_module_calls_readphases_and_extractsubglyphs():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    assert "readPhases(" in src
    assert "extractSubGlyphs(" in src


def test_the_module_is_pure_no_react_no_dom_no_clock():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    for word in ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch("):
        assert word not in src, f"storyChapters.ts reaches for {word}"


def test_the_only_template_literal_is_the_split_title_suffix():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    templates = re.findall(r"`[^`]*`", src)
    assert templates == ["`${title}, part ${part} of ${parts}`"], templates


def test_no_double_quoted_sentence_outside_the_title_table():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    table_block = _title_table_block(src)
    outside = src[: table_block.start()] + src[table_block.end() :]
    for literal in re.findall(r'"([^"]*)"', outside):
        assert not re.search(r"[A-Za-z] [A-Za-z]", literal), f"a sentence outside the title table: {literal!r}"

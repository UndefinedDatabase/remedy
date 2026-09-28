"""F039 T002 — the story's narration cards, DECISION F039 D3.

`apps/ui/src/components/story/storyNarration.ts` words a job's key events into narration
cards: the reviewer's own verdict for a review round (`STORY_VERDICT_LINES`, bound to
`REVIEW_OUTCOME_STATE_TABLE` in `brainOntology.ts`) and the ownership ledger's own action
words (`STORY_ACTOR_ACTIONS`, bound to `SUB_GLYPH_TABLE` in `phaseMapping.ts` and
`OWNERSHIP_CHIP_WORDS` in `ownership.ts`). The vitest goldens in `storyNarration.test.ts`
cannot read those Python-adjacent TypeScript tables against each other's own sources, so this
guard pins both tables, the module's imports, its one library call and its purity — no clock,
no DOM, no invented sentence outside its own verdict table — the way `test_story_chapters.py`
pins `storyChapters.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_phase_mapping import ts_import_specifiers

ROOT = Path(__file__).resolve().parent.parent.parent
STORY = ROOT / "apps" / "ui" / "src" / "components" / "story"
MODULE = STORY / "storyNarration.ts"
BRAIN_ONTOLOGY = ROOT / "apps" / "ui" / "src" / "components" / "graph" / "brainOntology.ts"
PHASE_MAPPING = ROOT / "apps" / "ui" / "src" / "components" / "timeline" / "phaseMapping.ts"
OWNERSHIP = ROOT / "apps" / "ui" / "src" / "api" / "ownership.ts"

EXPECTED_SPECIFIERS = [
    "../../api/costMetric",
    "../../api/ownership",
    "../graph/brainOntology",
    "../timeline/phaseMapping",
    "./storyChapters",
]

EXPECTED_VERDICT_LINES = {
    "pass": "Verdict: pass",
    "fail": "Verdict: fail",
    "needs_repair": "Verdict: needs repair",
    "blocked": "Verdict: blocked",
}

EXPECTED_ACTOR_ACTIONS = {
    "job_stopped": "job_stopped",
    "task_decision_answered": "decision_answered",
}


def _strip_comments(src: str) -> str:
    return re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.DOTALL)


def _table_block(src: str, name: str) -> re.Match[str]:
    match = re.search(rf"^export const {name}: [^=]+= \{{\n(.*?)^\}};$", src, re.MULTILINE | re.DOTALL)
    assert match, f"no `export const {name}` table in the source given"
    return match


def _string_table(block: str) -> dict[str, str]:
    entries = re.findall(r'^  ([A-Za-z_]+): "([^"]*)",$', block, re.MULTILINE)
    assert len(entries) == len(block.strip().splitlines()), "a line of another shape"
    return dict(entries)


def _keys_only(block: str) -> list[str]:
    keys = re.findall(r'^  ([A-Za-z_]+): "[^"]*",$', block, re.MULTILINE)
    assert len(keys) == len(block.strip().splitlines()), "a line of another shape"
    return keys


def test_story_verdict_lines_matches_review_outcome_state_table_in_order():
    module_src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    ontology_src = _strip_comments(BRAIN_ONTOLOGY.read_text(encoding="utf-8"))
    verdict_block = _table_block(module_src, "STORY_VERDICT_LINES")
    outcome_block = _table_block(ontology_src, "REVIEW_OUTCOME_STATE_TABLE")
    verdict_table = _string_table(verdict_block.group(1))
    outcome_keys = re.findall(r"^  ([a-z_]+):", outcome_block.group(1), re.MULTILINE)
    assert list(verdict_table.keys()) == outcome_keys
    assert verdict_table == EXPECTED_VERDICT_LINES


def test_story_actor_actions_is_the_two_pairs_bound_to_their_sources():
    module_src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    phase_src = _strip_comments(PHASE_MAPPING.read_text(encoding="utf-8"))
    ownership_src = _strip_comments(OWNERSHIP.read_text(encoding="utf-8"))
    actor_block = _table_block(module_src, "STORY_ACTOR_ACTIONS")
    actor_table = _string_table(actor_block.group(1))
    assert actor_table == EXPECTED_ACTOR_ACTIONS
    sub_glyph_block = _table_block(phase_src, "SUB_GLYPH_TABLE")
    sub_glyph_keys = set(re.findall(r"^  ([a-z_]+):", sub_glyph_block.group(1), re.MULTILINE))
    assert set(actor_table.keys()) <= sub_glyph_keys
    chip_block = _table_block(ownership_src, "OWNERSHIP_CHIP_WORDS")
    chip_keys = set(_keys_only(chip_block.group(1)))
    assert set(actor_table.values()) <= chip_keys


def test_the_module_imports_exactly_the_five_specifiers_of_s4():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    assert ts_import_specifiers(src) == EXPECTED_SPECIFIERS


def test_the_module_calls_costmetricof_and_is_pure():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    assert "costMetricOf(" in src
    for word in ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch(", "React"):
        assert word not in src, f"storyNarration.ts reaches for {word}"


def test_no_double_quoted_sentence_outside_the_verdict_table_and_the_one_template_literal():
    src = _strip_comments(MODULE.read_text(encoding="utf-8"))
    verdict_block = _table_block(src, "STORY_VERDICT_LINES")
    outside = src[: verdict_block.start()] + src[verdict_block.end() :]
    for literal in re.findall(r'"([^"]*)"', outside):
        assert not re.search(r"[A-Za-z] [A-Za-z]", literal), f"a sentence outside the verdict table: {literal!r}"
    templates = re.findall(r"`[^`]*`", src)
    assert len(templates) == 1, templates
    assert templates[0].startswith("`Cost so far: ${"), templates[0]

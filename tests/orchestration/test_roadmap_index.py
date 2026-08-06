"""Tests for the machine-readable roadmap mirror (F080 T001).

Two fixture kinds, per the feature's acceptance:

* THIS repository — the index must round-trip the real roadmap: every
  feature file present, STATUS order preserved, `plan next` target
  correct against Rule A5.
* One broken-grammar fixture per violation class — each must fail with
  the exact ``<file>:<line>: <what>`` so a fix is mechanical.

The mirror is one-way: nothing here writes markdown, and the generated
index goes under the data root, never into the repo.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.roadmap_index import (
    STATUS_GLYPHS,
    GrammarViolation,
    RoadmapGrammarError,
    active_feature,
    blocker_states,
    build_index,
    next_feature,
    proposed_feature,
    roadmap_index_path,
    write_index,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Fixture repo helpers — a minimal but grammar-valid roadmap
# ---------------------------------------------------------------------------

VALID_FEATURE = """# T{tier}_F{fid} — {title}
**Tier {tier} · Depends on: {depends} · Blocks/used by: {blocks}**

## Goal & Done
Fixture feature.
"""

VALID_STATUS = """# REMEDY STATUS — Execution-Order Truth

> Grammar: see ROADMAP.md Part C.

## Tier 0 — Foundation

- [x] F001 — First feature (PR #1)
- [ ] F002 — Second feature
"""

VALID_ROADMAP = """# REMEDY ROADMAP

## PART G — MILESTONES

| # | Name | Features | Proof |
|---|---|---|---|
| M1 | "Solid ground" | Tier 0 | ten clean runs |
"""


def _make_repo(tmp_path: Path) -> Path:
    """A tiny repository whose roadmap satisfies every grammar rule."""
    root = tmp_path / "repo"
    features = root / "docs" / "roadmap" / "features"
    features.mkdir(parents=True)
    (features / "T0_F001.md").write_text(
        VALID_FEATURE.format(tier=0, fid="001", title="First feature", depends="none", blocks="F002"),
        encoding="utf-8")
    (features / "T0_F002.md").write_text(
        VALID_FEATURE.format(tier=0, fid="002", title="Second feature", depends="F001", blocks="nothing yet"),
        encoding="utf-8")
    (root / "docs" / "roadmap" / "STATUS.md").write_text(VALID_STATUS, encoding="utf-8")
    (root / "docs" / "roadmap" / "ROADMAP.md").write_text(VALID_ROADMAP, encoding="utf-8")
    return root


def _violations(root: Path) -> list[GrammarViolation]:
    with pytest.raises(RoadmapGrammarError) as excinfo:
        build_index(root)
    return excinfo.value.violations


# ---------------------------------------------------------------------------
# This repository as the fixture
# ---------------------------------------------------------------------------


class TestThisRepository:
    def test_index_complete(self):
        """Every feature file and every STATUS entry is in the index."""
        index = build_index(REPO_ROOT)
        files = sorted(p.name for p in (REPO_ROOT / "docs/roadmap/features").glob("*.md"))
        assert len(index.features) >= len(files)
        assert len(index.order) == len(files)
        by_id = {f.id for f in index.features}
        for name in files:
            assert name.split("_")[1].removesuffix(".md") in by_id

    def test_order_is_status_order(self):
        """The index order is STATUS.md top-to-bottom — the execution truth."""
        index = build_index(REPO_ROOT)
        status_lines = [f.status_line for f in index.ordered_features() if f.status_line]
        assert status_lines == sorted(status_lines)

    def test_feature_round_trips(self):
        """A known feature keeps id, tier, title, deps and file path."""
        index = build_index(REPO_ROOT)
        f080 = index.by_id("F080")
        assert f080 is not None
        assert f080.tier == 1
        assert f080.title == "Machine-readable roadmap mirror & STATUS.md"
        assert f080.file == "docs/roadmap/features/T1_F080.md"
        assert "F070" in f080.depends_on
        assert "F248" in f080.blocks

    def test_every_status_glyph_maps_to_a_known_state(self):
        index = build_index(REPO_ROOT)
        known = set(STATUS_GLYPHS.values()) | {"not_scheduled"}
        assert {f.status for f in index.features} <= known

    def test_plan_next_target_matches_rule_a5(self):
        """Rule A5: the `[~]` line is active; otherwise the first `[ ]`."""
        index = build_index(REPO_ROOT)
        feature, reason = proposed_feature(index)
        assert feature is not None
        if reason == "in_progress":
            assert feature is active_feature(index)
        else:
            assert reason == "next_unchecked"
            assert feature is next_feature(index)

    def test_next_unchecked_is_the_first_todo_in_file_order(self):
        index = build_index(REPO_ROOT)
        todo = [f for f in index.ordered_features() if f.status == "todo"]
        assert next_feature(index) is todo[0]

    def test_blockers_carry_their_states(self):
        index = build_index(REPO_ROOT)
        f080 = index.by_id("F080")
        states = blocker_states(index, f080)
        assert [s["id"] for s in states] == list(f080.depends_on)
        assert all(s["status"] != "unknown" for s in states)

    def test_milestones_parsed_and_attached(self):
        index = build_index(REPO_ROOT)
        assert len(index.milestones) >= 10
        assert index.by_id("F080").milestone == "M2"

    def test_index_json_round_trips(self, tmp_path):
        """The written index is JSON and carries the same features."""
        index = build_index(REPO_ROOT)
        path = write_index(index, tmp_path / "data")
        assert path == roadmap_index_path(tmp_path / "data")
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["schema"] == "roadmap_index/v1"
        assert len(payload["features"]) == len(index.features)
        assert payload["order"] == list(index.order)

    def test_index_is_written_under_the_data_root_only(self, tmp_path):
        """One-way mirror: writing the index touches nothing in the repo."""
        before = sorted(p.name for p in (REPO_ROOT / "docs/roadmap").iterdir())
        index = build_index(REPO_ROOT)
        path = write_index(index, tmp_path / "data")
        assert str(path).startswith(str(tmp_path))
        assert sorted(p.name for p in (REPO_ROOT / "docs/roadmap").iterdir()) == before


# ---------------------------------------------------------------------------
# Grammar violations — one fixture per class, exact file:line
# ---------------------------------------------------------------------------


class TestGrammarViolations:
    def test_valid_fixture_repo_parses(self, tmp_path):
        index = build_index(_make_repo(tmp_path))
        assert [f.id for f in index.ordered_features()] == ["F001", "F002"]
        assert next_feature(index).id == "F002"

    def test_missing_title_line(self, tmp_path):
        root = _make_repo(tmp_path)
        target = root / "docs/roadmap/features/T0_F002.md"
        target.write_text("Second feature\n" + target.read_text(encoding="utf-8").split("\n", 1)[1],
                          encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/features/T0_F002.md:1: missing title line: "
            "expected '# T<tier>_F<id> — <title>'")

    def test_malformed_dependency_line(self, tmp_path):
        root = _make_repo(tmp_path)
        target = root / "docs/roadmap/features/T0_F001.md"
        lines = target.read_text(encoding="utf-8").split("\n")
        lines[1] = "Tier 0 - depends on nothing"
        target.write_text("\n".join(lines), encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/features/T0_F001.md:2: malformed dependency line: "
            "expected '**Tier <n> · Depends on: … · Blocks/used by: …**'")

    def test_unclosed_dependency_block(self, tmp_path):
        root = _make_repo(tmp_path)
        target = root / "docs/roadmap/features/T0_F001.md"
        lines = target.read_text(encoding="utf-8").split("\n")
        lines[1] = "**Tier 0 · Depends on: none · Blocks/used by: F002"
        target.write_text("\n".join(lines), encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/features/T0_F001.md:2: malformed dependency line: "
            "bold block is not closed with '**'")

    def test_tier_mismatch_between_title_and_dependency_line(self, tmp_path):
        root = _make_repo(tmp_path)
        target = root / "docs/roadmap/features/T0_F001.md"
        lines = target.read_text(encoding="utf-8").split("\n")
        lines[1] = lines[1].replace("**Tier 0", "**Tier 3")
        target.write_text("\n".join(lines), encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/features/T0_F001.md:2: dependency line says tier 3, "
            "title line says tier 0")

    def test_duplicate_id_across_files(self, tmp_path):
        root = _make_repo(tmp_path)
        duplicate = root / "docs/roadmap/features/T0_F002.md"
        duplicate.write_text(
            VALID_FEATURE.format(tier=0, fid="001", title="Cloned first feature",
                                 depends="none", blocks="none"),
            encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/features/T0_F002.md:1: title line F001 (tier 0) does not "
            "match file name 'T0_F002.md'")
        assert str(found[1]) == (
            "docs/roadmap/features/T0_F002.md:1: duplicate feature id F001 — "
            "already defined in docs/roadmap/features/T0_F001.md")

    def test_unknown_status_glyph(self, tmp_path):
        root = _make_repo(tmp_path)
        status = root / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace(
            "- [ ] F002", "- [?] F002"), encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/STATUS.md:8: unknown status glyph '?' — expected one of "
            "[' ', '!', 'x', '~']")

    def test_status_line_without_checkbox_grammar(self, tmp_path):
        root = _make_repo(tmp_path)
        status = root / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace(
            "- [ ] F002 — Second feature", "- F002 — Second feature"), encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/STATUS.md:8: status line without checkbox grammar: "
            "expected '- [<glyph>] F<id> — <title>'")

    def test_duplicate_status_line(self, tmp_path):
        root = _make_repo(tmp_path)
        status = root / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8") + "- [ ] F001 — First feature again\n",
                          encoding="utf-8")
        found = _violations(root)
        assert str(found[0]) == (
            "docs/roadmap/STATUS.md:9: duplicate feature id F001 — already listed on line 7")

    def test_all_violations_reported_in_one_pass(self, tmp_path):
        """A fix round is mechanical: every violation is collected, not just the first."""
        root = _make_repo(tmp_path)
        (root / "docs/roadmap/features/T0_F001.md").write_text("broken\n", encoding="utf-8")
        status = root / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace("- [ ] F002", "- [?] F002"),
                          encoding="utf-8")
        found = _violations(root)
        assert len(found) == 2
        assert {v.file for v in found} == {
            "docs/roadmap/features/T0_F001.md", "docs/roadmap/STATUS.md"}

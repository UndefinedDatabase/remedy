"""Tests for the feature→mission adapter (F080 T003).

Three things are proven here, in the feature's own words:

* **Mapping** — each of the four seeded parts comes from its section and
  says which heading and line it came from.
* **End to end on a real file** — T2_F103.md compiles into a prepared
  mission whose parts are all present and traceable, approval left open.
* **No execution side effects** — zero jobs, zero runs, repo unchanged,
  and a file that breaks the roadmap grammar is refused outright.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.feature_mission_adapter import (
    PreparedMission,
    dod_compiler_input,
    parse_task_slices,
    prepare_feature_mission,
    prepared_mission_path,
    read_feature_sections,
    write_prepared_mission,
)
from packages.orchestration.roadmap_index import RoadmapGrammarError

REPO_ROOT = Path(__file__).resolve().parents[2]

FIXTURE_FEATURE = """# T0_F002 — Second feature
**Tier 0 · Depends on: F001 · Blocks/used by: nothing yet**

## Goal & Done
The widget becomes queryable. DONE when the reader answers from the
store and every figure names its basis.

## How it fits (inspect current shape before building)
The capture path already exists; this adds the store, not a second
capture path.

## Design (suggested shape)
- One store per project under the data root.

## Task slicing
- **T001** schema + writer + unit tests.
- **T002** backfill command + idempotence tests.

## Acceptance
- A fake-provider job yields exactly its calls as rows.
- Rerunning the backfill adds nothing.

## Do not touch
Estimation, provider parsing, docs/roadmap/STATUS.md semantics.
Suggested tests: tests/orchestration/test_widget.py.
"""

FIXTURE_STATUS = """# REMEDY STATUS — Execution-Order Truth

## Tier 0 — Foundation

- [x] F001 — First feature (PR #1)
- [ ] F002 — Second feature
"""

MINIMAL_FEATURE = """# T0_F001 — First feature
**Tier 0 · Depends on: none · Blocks/used by: F002**

## Goal & Done
The ground is solid.
"""


@pytest.fixture
def fixture_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    features = root / "docs" / "roadmap" / "features"
    features.mkdir(parents=True)
    (features / "T0_F001.md").write_text(MINIMAL_FEATURE, encoding="utf-8")
    (features / "T0_F002.md").write_text(FIXTURE_FEATURE, encoding="utf-8")
    (root / "docs" / "roadmap" / "STATUS.md").write_text(FIXTURE_STATUS, encoding="utf-8")
    return root


def _snapshot(root: Path) -> dict[str, tuple[int, float]]:
    return {str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime)
            for p in sorted(root.rglob("*")) if p.is_file()}


# ---------------------------------------------------------------------------
# Section reading
# ---------------------------------------------------------------------------


class TestSections:
    def test_sections_carry_their_heading_line(self):
        sections = read_feature_sections(FIXTURE_FEATURE)
        by_heading = {s.heading: s.line for s in sections}
        assert by_heading["Goal & Done"] == 4
        assert by_heading["Task slicing"] == 15
        assert by_heading["Acceptance"] == 19

    def test_roles_ignore_parenthesised_qualifiers(self):
        sections = read_feature_sections(FIXTURE_FEATURE)
        roles = {s.heading: s.role() for s in sections}
        assert roles["How it fits (inspect current shape before building)"] == "context"
        assert roles["Task slicing"] == "plan"
        assert roles["Acceptance"] == "acceptance"
        assert roles["Do not touch"] == "fences"
        assert roles["Design (suggested shape)"] == ""

    def test_bullet_task_slices(self):
        slices = parse_task_slices("- **T001** parser + tests.\n- **T002** the CLI.")
        assert [(s.id, s.text) for s in slices] == [
            ("T001", "parser + tests."), ("T002", "the CLI.")]

    def test_prose_task_slices(self):
        """Older feature files write the slicing as one paragraph."""
        slices = parse_task_slices("T001 module + unit tests. T002 provider integration.")
        assert [s.id for s in slices] == ["T001", "T002"]
        assert slices[0].text == "module + unit tests"


# ---------------------------------------------------------------------------
# Section -> draft part mapping
# ---------------------------------------------------------------------------


class TestSectionMapping:
    @pytest.fixture
    def prepared(self, fixture_repo) -> PreparedMission:
        return prepare_feature_mission("F002", fixture_repo)

    def test_context_section_becomes_intake_context(self, prepared):
        refs = " ".join(prepared.intake.context_refs)
        assert "How it fits" in refs
        assert "T0_F002.md" in refs

    def test_goal_carries_the_feature_identity_and_goal_section(self, prepared):
        assert prepared.goal.startswith("F002 — Second feature.")
        assert "becomes queryable" in prepared.goal

    def test_task_slicing_becomes_the_plan_seed(self, prepared):
        assert [t.id for t in prepared.plan.tasks] == ["T001", "T002"]
        assert prepared.plan.tasks[0].goal == "schema + writer + unit tests."
        assert prepared.plan.tasks[0].files_hint == ["docs/roadmap/features/T0_F002.md"]

    def test_task_slicing_becomes_the_milestone_draft(self, prepared):
        goals = [m.goal for m in prepared.mission_plan.milestones]
        assert [m.id for m in prepared.mission_plan.milestones] == ["T001", "T002"]
        assert goals[0].startswith("T001 of F002 is complete:")
        assert prepared.mission_plan.compiled is False
        assert prepared.mission_plan.origin == "deterministic"

    def test_acceptance_becomes_the_dod_seed(self, prepared):
        assert prepared.dod_seed == (
            "A fake-provider job yields exactly its calls as rows.",
            "Rerunning the backfill adds nothing.")
        assert list(prepared.intake.acceptance_hints) == list(prepared.dod_seed)
        assert prepared.plan.tasks[0].acceptance == list(prepared.dod_seed)

    def test_do_not_touch_becomes_fences(self, prepared):
        assert prepared.fence_globs == ("docs/roadmap/STATUS.md",)
        assert prepared.plan.fences == {"deny": ["docs/roadmap/STATUS.md"]}
        assert any("Estimation" in note for note in prepared.fence_notes)

    def test_suggested_tests_are_not_fences(self, prepared):
        """"Suggested tests:" names where proof lives — the opposite of a fence."""
        assert not any("test_widget" in glob for glob in prepared.fence_globs)
        assert not any("Suggested tests" in note for note in prepared.fence_notes)

    def test_every_part_records_its_source_heading_and_line(self, prepared):
        assert prepared.sources["plan"] == {"heading": "Task slicing", "line": 15}
        assert prepared.sources["dod"] == {"heading": "Acceptance", "line": 19}
        assert prepared.sources["fences"] == {"heading": "Do not touch", "line": 23}
        assert prepared.sources["goal"] == {"heading": "Goal & Done", "line": 4}
        assert "How it fits (inspect current shape before building)" in \
            prepared.sources["context"]["headings"]

    def test_feature_without_sections_still_compiles(self, fixture_repo):
        """A sparse file yields one slice and the Goal & Done fallback seed."""
        prepared = prepare_feature_mission("F001", fixture_repo)
        assert [t.id for t in prepared.plan.tasks] == ["T001"]
        assert prepared.plan.tasks[0].acceptance  # never empty — schema requires one

    def test_dod_compiler_input_is_the_pair_the_compiler_consumes(self, prepared):
        from packages.orchestration.dod_compiler import deterministic_dod
        from packages.orchestration.dod_schema import TRACEABILITY_RULE

        intake, plan = dod_compiler_input(prepared)
        assert intake["goal"] == prepared.goal
        dod = deterministic_dod(plan, intake=intake)
        assert dod.checks and TRACEABILITY_RULE
        assert dod.compiled is False


# ---------------------------------------------------------------------------
# End to end on a real feature file of this repository
# ---------------------------------------------------------------------------


class TestRealFeatureFileEndToEnd:
    @pytest.fixture
    def prepared(self) -> PreparedMission:
        return prepare_feature_mission("F103")

    def test_compiles_t2_f103(self, prepared):
        assert prepared.feature_id == "F103"
        assert prepared.tier == 2
        assert prepared.feature_file == "docs/roadmap/features/T2_F103.md"
        assert "Token ledger" in prepared.title

    def test_all_four_seeded_parts_are_present(self, prepared):
        assert prepared.intake.context_refs          # context input
        assert len(prepared.plan.tasks) == 3         # plan seed: T001-T003
        assert prepared.dod_seed                     # DoD input
        assert prepared.fence_notes                  # fences

    def test_parts_are_traceable_to_their_sections(self, prepared):
        text = (REPO_ROOT / prepared.feature_file).read_text(encoding="utf-8").split("\n")
        for part in ("goal", "plan", "dod", "fences"):
            line = prepared.sources[part]["line"]
            assert text[line - 1].startswith("## ")
            assert prepared.sources[part]["heading"] in text[line - 1]

    def test_slices_match_the_files_task_slicing(self, prepared):
        assert [t.id for t in prepared.plan.tasks] == ["T001", "T002", "T003"]
        assert "schema" in prepared.plan.tasks[0].goal
        assert "backfill" in prepared.plan.tasks[1].goal

    def test_approval_is_left_open(self, prepared):
        assert prepared.approval_required is True
        assert prepared.started is False
        assert prepared.mission_plan.milestones_without_dod == ("T001", "T002", "T003")

    def test_draft_round_trips_as_json(self, prepared, tmp_path):
        path = write_prepared_mission(prepared, tmp_path / "data")
        assert path == prepared_mission_path("F103", tmp_path / "data")
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["schema"] == "prepared_feature_mission/v1"
        assert payload["started"] is False
        assert payload["approval_required"] is True
        assert [t["id"] for t in payload["plan"]["tasks"]] == ["T001", "T002", "T003"]

    def test_every_feature_file_in_this_repo_compiles(self):
        """The grammar the parser enforces is enough to compile the roadmap."""
        from packages.orchestration.roadmap_index import build_index

        index = build_index(REPO_ROOT)
        sample = [f for f in index.features if f.file][:12]
        for feature in sample:
            prepared = prepare_feature_mission(feature.id)
            assert prepared.plan.tasks
            assert prepared.started is False


# ---------------------------------------------------------------------------
# No execution side effects — an acceptance criterion, not a nicety
# ---------------------------------------------------------------------------


class TestNoExecutionSideEffects:
    def test_no_jobs_and_no_runs_are_created(self, fixture_repo, tmp_path):
        data_root = tmp_path / "data"
        prepared = prepare_feature_mission("F002", fixture_repo)
        write_prepared_mission(prepared, data_root)
        assert not (data_root / "jobs").exists()
        assert not (data_root / "runs").exists()
        assert not (data_root / "missions").exists()

    def test_only_the_draft_is_written_under_the_data_root(self, fixture_repo, tmp_path):
        data_root = tmp_path / "data"
        write_prepared_mission(prepare_feature_mission("F002", fixture_repo), data_root)
        written = sorted(str(p.relative_to(data_root)) for p in data_root.rglob("*") if p.is_file())
        assert written == ["roadmap/missions/F002.json"]

    def test_preparing_alone_writes_nothing(self, fixture_repo, tmp_path):
        data_root = tmp_path / "data"
        data_root.mkdir()
        prepare_feature_mission("F002", fixture_repo)
        assert list(data_root.rglob("*")) == []

    def test_the_feature_repo_is_left_untouched(self, fixture_repo, tmp_path):
        before = _snapshot(fixture_repo)
        write_prepared_mission(prepare_feature_mission("F002", fixture_repo), tmp_path / "data")
        assert _snapshot(fixture_repo) == before

    def test_this_repository_is_left_untouched(self):
        roadmap = REPO_ROOT / "docs" / "roadmap"
        before = _snapshot(roadmap)
        prepare_feature_mission("F103")
        assert _snapshot(roadmap) == before


# ---------------------------------------------------------------------------
# A broken file is refused
# ---------------------------------------------------------------------------


class TestGrammarRefusal:
    def test_broken_feature_file_raises_grammar_error(self, fixture_repo):
        (fixture_repo / "docs/roadmap/features/T0_F002.md").write_text(
            "Second feature\n\nno header at all\n", encoding="utf-8")
        with pytest.raises(RoadmapGrammarError) as excinfo:
            prepare_feature_mission("F002", fixture_repo)
        assert "T0_F002.md:1: missing title line" in str(excinfo.value)

    def test_a_broken_neighbour_also_stops_the_compile(self, fixture_repo):
        """One parser, one verdict: the adapter compiles only a trusted roadmap."""
        (fixture_repo / "docs/roadmap/features/T0_F001.md").write_text(
            "First feature\n", encoding="utf-8")
        with pytest.raises(RoadmapGrammarError):
            prepare_feature_mission("F002", fixture_repo)

    def test_unknown_feature_id_is_a_value_error(self, fixture_repo):
        with pytest.raises(ValueError, match="F999"):
            prepare_feature_mission("F999", fixture_repo)

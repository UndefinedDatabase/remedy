"""Source guard for T002 part one (DECISION F019 D3): the stage mounts the
live force-graph renderer by default and keeps `BrainGraphCanvas.tsx` (the SVG
view) mounted as the explicit "Simple view" fallback — kept in the tree.
This module reads source text only; it makes no claim about runtime
behaviour, which is vitest's job (brainView.test.ts).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH_DIR = REPO_ROOT / "apps" / "ui" / "src" / "components" / "graph"
STAGE_TSX = GRAPH_DIR / "BrainGraphStage.tsx"
STAGE_CSS = GRAPH_DIR / "BrainGraphStage.module.css"
RENDERER_TSX = GRAPH_DIR / "ForceBrainGraph.tsx"


class TestStageMountsBothRenderers:
    def test_stage_imports_force_brain_graph(self):
        src = STAGE_TSX.read_text()
        assert "ForceBrainGraph" in src

    def test_stage_imports_brain_graph_canvas(self):
        src = STAGE_TSX.read_text()
        assert "BrainGraphCanvas" in src

    def test_stage_mounts_force_brain_graph_element(self):
        src = STAGE_TSX.read_text()
        assert "<ForceBrainGraph" in src

    def test_stage_mounts_brain_graph_canvas_element(self):
        src = STAGE_TSX.read_text()
        assert "<BrainGraphCanvas" in src


class TestStageMapsLiveClicksToTheShellsSelectionId:
    def test_stage_calls_shell_selection_id_of(self):
        src = STAGE_TSX.read_text()
        assert "shellSelectionIdOf(" in src


class TestStageBuildsTheRealLayout:
    def test_stage_seeds_from_the_dashboard(self):
        src = STAGE_TSX.read_text()
        assert "dashboardBrainSeeds(" in src

    def test_stage_folds_the_ledgers_prefix_into_the_reducer_model(self):
        """R5 T003: the stage now REBUILDS from the ledger's contiguous prefix
        rather than seeding once from the dashboard alone (DECISION F019 D5) —
        `test_brain_live_wiring.py` pins the rest of the wiring."""
        src = STAGE_TSX.read_text()
        assert "rebuildBrainModel(" in src

    def test_stage_lays_out_the_model(self):
        src = STAGE_TSX.read_text()
        assert "buildBrainLayout(" in src

    def test_stage_filters_the_layout(self):
        src = STAGE_TSX.read_text()
        assert "filterBrainLayout(" in src

    def test_stage_counts_tasks_to_pick_a_renderer(self):
        src = STAGE_TSX.read_text()
        assert "brainTaskCount(" in src


class TestStageCarriesTheSimpleViewToggle:
    def test_simple_view_text_present(self):
        src = STAGE_TSX.read_text()
        assert "Simple view" in src

    def test_live_view_text_present(self):
        src = STAGE_TSX.read_text()
        assert "Live view" in src

    def test_view_dock_and_toggle_classes_defined(self):
        css = STAGE_CSS.read_text()
        assert ".viewDock" in css
        assert ".viewToggle" in css


class TestForceBrainGraphNoLongerPaintsTheDecorativeDashboardGraph:
    """ForceBrainGraph.tsx paints buildBrainLayout's REAL layout now, not the
    dashboard-polling decorative graph (DECISION F019 D1) — so it must not
    import the function or the type that built the old one."""

    def test_does_not_reference_build_force_brain_model(self):
        """The module PATH "./buildForceBrainModel" is fine — `seededRng` is
        re-exported from there (design item 6); the demoted decorative
        BUILDER function itself must not be imported or called."""
        src = RENDERER_TSX.read_text()
        without_module_path = src.replace('"./buildForceBrainModel"', "")
        assert "buildForceBrainModel" not in without_module_path

    def test_does_not_reference_remedy_dashboard(self):
        src = RENDERER_TSX.read_text()
        assert "RemedyDashboard" not in src

    def test_references_schedule_brain_births(self):
        src = RENDERER_TSX.read_text()
        assert "scheduleBrainBirths" in src

    def test_references_node_painters_table(self):
        src = RENDERER_TSX.read_text()
        assert "NODE_PAINTERS" in src

    def test_container_is_aria_hidden(self):
        """graph_spec.md §14: the canvas is not the accessible surface."""
        src = RENDERER_TSX.read_text()
        assert 'aria-hidden="true"' in src

    def test_particle_expression_reads_active_and_reduced_motion(self):
        src = RENDERER_TSX.read_text()
        assert "linkDirectionalParticles" in src
        particle_line_start = src.index("linkDirectionalParticles")
        particle_expr = src[particle_line_start:particle_line_start + 200]
        assert "active" in particle_expr
        assert "reducedMotion" in particle_expr

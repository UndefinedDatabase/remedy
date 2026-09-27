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
PROMPT_LIST_TSX = GRAPH_DIR / "PromptNodeList.tsx"
PROMPT_LIST_CSS = GRAPH_DIR / "PromptNodeList.module.css"


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


class TestStageComposesThePromptTraceOntoTheLiveModelOnly:
    """F288 T003 (DECISION F288 D5): `withPromptNodes` composes the dashboard's
    prompt trace onto the LIVE model exactly once, inside the `liveModel` line
    only — a scrubbed model stays `rebuildBrainModel`'s own history, drawing no
    prompt — and a click on a synapse selects the prompt item itself."""

    def test_with_prompt_nodes_appears_exactly_once_inside_the_live_model_line(self):
        src = STAGE_TSX.read_text()
        assert src.count("withPromptNodes(") == 1
        assert "const liveModel = useMemo(() => withPromptNodes(" in src

    def test_the_scrubbed_model_still_wins_over_the_composed_live_model(self):
        src = STAGE_TSX.read_text()
        assert "const model = scrub.scrubbedModel ?? liveModel;" in src

    def test_a_click_selects_the_prompt_item_itself_not_only_the_task(self):
        src = RENDERER_TSX.read_text()
        body = src[src.index("const handleNodeClick = useCallback("):src.index("}, [onSelectNode, onZoomEvent]);")]
        assert "selectionIdOf(n)" in body
        assert "selectionTaskIdOf(n)" not in body


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


class TestPromptNodeListMountsInTheLiveBranchOnly:
    """F288 T003 second half (DECISION F288 D6, graph_spec.md §14): the
    keyboard's parallel list of the live picture's prompt nodes mounts
    beside the aria-hidden canvas in the live branch only — the simple
    branch is the SVG picture's own keyboard surface and stays untouched."""

    def test_the_live_branch_holds_the_prompt_node_list(self):
        src = STAGE_TSX.read_text()
        live = src[src.index("{showLiveGraph ? ("):src.index(") : (")]
        assert "<PromptNodeList" in live

    def test_the_simple_branch_does_not(self):
        src = STAGE_TSX.read_text()
        simple = src[src.index(") : ("):]
        assert "<PromptNodeList" not in simple


class TestPromptNodeListIsTheAccessibleSurfaceForTheCanvassSynapses:
    """graph_spec.md §14 pairs the `aria-hidden` canvas with this list as the
    accessible surface for its prompt nodes."""

    def test_buttons_are_native_and_type_button(self):
        src = PROMPT_LIST_TSX.read_text()
        assert 'type="button"' in src

    def test_pressed_state_is_wired(self):
        src = PROMPT_LIST_TSX.read_text()
        assert "aria-pressed={" in src

    def test_a_click_selects_the_prompt_item(self):
        src = PROMPT_LIST_TSX.read_text()
        assert "onSelect(entry.promptId)" in src

    def test_carries_its_own_data_ui_marker(self):
        src = PROMPT_LIST_TSX.read_text()
        assert 'data-ui="prompt-node-list"' in src

    def test_is_not_aria_hidden(self):
        src = PROMPT_LIST_TSX.read_text()
        assert "aria-hidden" not in src

    def test_style_module_shows_on_focus_within_and_never_display_none_or_visibility_hidden(self):
        css = PROMPT_LIST_CSS.read_text()
        assert ":focus-within" in css
        assert "display: none" not in css
        assert "visibility: hidden" not in css

    def test_the_canvas_still_stays_aria_hidden(self):
        src = RENDERER_TSX.read_text()
        assert 'aria-hidden="true"' in src

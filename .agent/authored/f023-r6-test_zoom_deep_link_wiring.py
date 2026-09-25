"""F023 T003 — deep links and cluster expansion are wired as DECISION F023 D6 rules.

`useZoomDeepLink.ts` reads the zoom's link from the page's URL once, replays it through the
machine when the graph holds its node, and then keeps the URL in step with
`history.replaceState`; `BrainGraphStage.tsx` checks focus against the unexpanded layout
and renders the layout with the focused task's cluster chip expanded
(`clusterExpansion.ts` through `buildBrainLayout`). The pure halves are goldened by
`zoomDeepLink.test.ts` and `clusterExpansion.test.ts`; the vitest environment renders no
React and has no `window`, so the binding is pinned from source here.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
UI = ROOT / "apps" / "ui"
GRAPH = UI / "src" / "components" / "graph"
STAGE = GRAPH / "BrainGraphStage.tsx"
HOOK = GRAPH / "useZoomDeepLink.ts"
LAYOUT = GRAPH / "buildForceBrainModel.ts"


def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_the_stage_restores_and_follows_the_link_against_the_unexpanded_graph():
    src = _src(STAGE)
    assert "const baseLayout = useMemo(() => buildBrainLayout(model), [model]);" in src
    assert "const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, baseLayout.nodes), [model, baseLayout]);" in src
    assert "useZoomDeepLink(zoomGraph, zoom.state, zoom.dispatch);" in src
    assert src.index("const zoom = useSemanticZoom(zoomGraph);") < src.index("useZoomDeepLink(")


def test_the_stage_expands_the_focused_tasks_cluster_and_nothing_else():
    src = _src(STAGE)
    assert "const expandTaskId = zoomCrumbs.find((c) => c.level === 1)?.nodeId ?? null;" in src
    assert "(expandTaskId === null ? baseLayout : buildBrainLayout(model, expandTaskId))" in src
    assert "filterBrainLayout(layout, filter)" in src
    layout = _src(LAYOUT)
    assert "export function buildBrainLayout(model: BrainModel, expandTaskId: string | null = null): BrainLayoutData {" in layout
    assert ": expandClusterOf(clusterBrainModel(model), model, expandTaskId);" in layout


def test_the_link_is_read_once_and_written_without_a_router_or_a_history_entry():
    src = _src(HOOK)
    assert "useState(() => zoomLinkFromSearch(window.location.search))" in src
    assert "window.history.replaceState(" in src
    assert "pushState" not in src
    assert "react-router" not in _src(UI / "package.json")


def test_a_level_restored_before_the_canvas_existed_still_gets_its_camera():
    # Measured headless before this round: a deep link restored L3 while the canvas had
    # no size yet, the camera effect found no graph and never ran again, and the
    # one-time fit then forced the organism's camera over the restored level.
    src = (GRAPH / "ForceBrainGraph.tsx").read_text(encoding="utf-8")
    assert "const graphReady = size.width > 0;" in src
    camera = src[src.index("const camera = zoomCamera(layoutRef.current, zoom);"):]
    assert camera.index("}, [zoom, graphReady]);") < camera.index("// Initial fit")
    fit = src[src.index("// Initial fit"):]
    assert "zoomCamera(layoutRef.current, zoomRef.current) ?? { x: 0, y: 0, k: ZOOM_HOME_CAMERA }" in fit
    assert fit.index("}, [graphReady]);") < fit.index("\n  return (\n")


def test_a_pending_link_waits_for_its_node_and_gives_way_to_the_reader():
    src = _src(HOOK)
    replay = src[src.index("const link = pendingRef.current;"):]
    assert replay.index("if (!link || !graph.has(link.focusId)) return;") < replay.index("zoomLinkEvents(link).forEach(dispatch);")
    assert "if (state === ZOOM_HOME) return;" in src

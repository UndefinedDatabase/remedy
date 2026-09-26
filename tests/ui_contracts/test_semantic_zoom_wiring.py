"""F023 T002 — the stage drives the live canvas from the semantic-zoom machine.

`BrainGraphStage.tsx` holds the zoom state through `useSemanticZoom.ts`, checks focus
against the model plus its clustered view, and hands the canvas the render effects
`zoomView.ts` computes; `ForceBrainGraph.tsx` paints them, sends clicks and wheel
crossings to the machine, and moves the camera per level without mistaking its own
camera move for a wheel (graph_spec.md §10, DECISIONS F023 D1 and D2). The vitest
environment renders no `.tsx`, so the wiring is pinned from source here; the effects
themselves are goldened by `zoomView.test.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
CANVAS = GRAPH / "ForceBrainGraph.tsx"
STAGE = GRAPH / "BrainGraphStage.tsx"
HOOK = GRAPH / "useSemanticZoom.ts"
VIEW = GRAPH / "zoomView.ts"
SHIM = ROOT / "apps" / "ui" / "src" / "types" / "react-force-graph-2d.d.ts"
REFERENCE_TOKENS = ROOT / "docs" / "ui" / "design_reference" / "tokens.css"


def _src(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_the_stage_checks_focus_against_the_model_and_its_clustered_view():
    src = _src(STAGE)
    # From F023 D6 the graph reads the UNEXPANDED layout, so an expanded chip never
    # moves the graph the focus is checked against.
    assert "const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, baseLayout.nodes), [model, baseLayout]);" in src
    assert "const zoom = useSemanticZoom(zoomGraph);" in src
    assert "zoomEmphasis(visible, zoom.state)" in src


def test_the_stage_hands_the_canvas_the_state_and_mounts_the_breadcrumbs_with_it():
    src = _src(STAGE)
    live = src[src.index("{showLiveGraph ? ("):src.index(") : (")]
    for prop in ("zoom={zoom.state}", "emphasis={emphasis}", "onZoomEvent={zoom.dispatch}"):
        assert prop in live, f"<ForceBrainGraph> lacks {prop}"
    assert '<ZoomBreadcrumbs items={crumbs} onJump={(level) => zoom.dispatch({ type: "crumb", level })} />' in live


def test_a_click_is_the_machines_click():
    src = _src(CANVAS)
    body = src[src.index("const handleNodeClick = useCallback("):src.index("}, [onSelectNode, onZoomEvent]);")]
    assert 'onZoomEvent({ type: "click", nodeId: n.id });' in body


def test_the_wheel_reads_every_zoom_frame_but_never_the_components_own_camera_move():
    src = _src(CANVAS)
    assert "onZoom={handleZoom}" in src
    assert "onNodeHover={handleNodeHover}" in src
    body = src[src.index("const handleZoom = useCallback("):src.index("}, [onZoomEvent]);")]
    lock = body.index("if (performance.now() < cameraLockUntilRef.current) return;")
    assert lock < body.index("wheelZoomEvent(previous, k, hoveredIdRef.current)")
    assert body.index("lastZoomRef.current = k;") < lock, "a locked frame must still record the factor"
    camera = src[src.index("const camera = zoomCamera(layoutRef.current, zoom);"):]
    assert camera.index("cameraLockUntilRef.current = performance.now() + ms + 100;") < camera.index(
        "fg.zoom(camera.k, ms);"
    )
    shim = _src(SHIM)
    assert "onZoom?: (transform: { k: number; x: number; y: number }) => void;" in shim


def test_the_painter_dims_labels_and_rings_from_the_emphasis():
    src = _src(CANVAS)
    assert "const dim = emphasis.dimmed.has(n.id) ? ZOOM_DIM_ALPHA : 1;" in src
    assert "if (n.id === selectedId || n.id === emphasis.ringId) {" in src
    assert "(globalScale > 1.4 || emphasis.labelled.has(n.id))" in src
    label = src[src.index("(globalScale > 1.4 || emphasis.labelled.has(n.id))"):]
    assert label.index("ctx.globalAlpha = dim * vetoFade;") < label.index("ctx.fillText(n.label")
    assert "(emphasis.dimmed.has(target.id) ? ZOOM_DIM_ALPHA : 1)" in src


def test_the_branch_glow_is_painted_in_the_in_progress_token():
    src = _src(CANVAS)
    assert 'const glow = resolvedPalette.palette["--remedy-state-current"];' in src
    assert "if (emphasis.glowing.has(l.id) && glow) {" in src
    assert '"--remedy-state-current"' in _src(GRAPH / "renderers" / "nodeStates.ts")


def test_escape_and_reconcile_live_in_the_hook():
    src = _src(HOOK)
    assert "escapeWalksBack(target, document.querySelector('[role=\"dialog\"]') !== null)" in src
    effect = src[src.index('dispatch({ type: "reconcile" });'):]
    assert effect.index("}, [graph, dispatch]);") < 60


def test_the_camera_moves_over_the_reference_slow_duration():
    ref = re.search(r"--remedy-dur-slow:\s*(\d+)ms;", _src(REFERENCE_TOKENS))
    assert ref, "the reference token sheet no longer declares --remedy-dur-slow"
    assert f"export const ZOOM_CAMERA_MS = {ref.group(1)};" in _src(VIEW)

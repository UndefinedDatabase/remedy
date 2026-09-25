"""F020 T003 — the brain graph's canvas animates state changes and pauses when hidden.

`apps/ui/src/components/graph/ForceBrainGraph.tsx` schedules a crossfade for every
state change through `renderers/stateMotion.ts`, paints each non-core node through
the motion-aware painter with its pulse, and asks for animation frames only when
`brainNeedsAnimationFrames` says so, which it never does while `usePageVisible`
reports the page hidden (graph_spec.md §12, motion_spec.md; DECISION F020 D4). The
vitest environment renders no `.tsx`, so the wiring is pinned from source here; the
decisions themselves are pinned by `stateMotion.test.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
CANVAS = GRAPH / "ForceBrainGraph.tsx"
VISIBLE = GRAPH / "usePageVisible.ts"


def test_the_canvas_redraws_only_when_the_animation_rule_says_so():
    src = CANVAS.read_text(encoding="utf-8")
    assert "const pageVisible = usePageVisible();" in src
    call = re.search(r"const animating = brainNeedsAnimationFrames\(\{([^}]*)\}\);", src)
    assert call, "ForceBrainGraph.tsx does not compute `animating` from brainNeedsAnimationFrames"
    assert {p.strip() for p in call.group(1).split(",")} == {
        "pageVisible", "reducedMotion", "birthsInFlight", "transitionsInFlight", "pulsing",
    }
    assert "autoPauseRedraw={!animating}" in src
    # A particle keeps force-graph drawing whatever autoPauseRedraw says, so it
    # must stop with the page: measured at F020 R4, 61 frames a second hidden.
    assert "(l as BrainLayoutLink).active && !reducedMotion && pageVisible ? 1 : 0" in src
    assert "const pulsing = useMemo(() => layoutHasPulse(layout), [layout]);" in src


def test_every_state_change_is_scheduled_before_the_next_paint():
    src = CANVAS.read_text(encoding="utf-8")
    effect = src.index("scheduleStateTransitions(transitionsPreviousLayoutRef.current, layout, now, reducedMotion)")
    assert src.rfind("useLayoutEffect(() => {", 0, effect) > src.rfind("useEffect(() => {", 0, effect)
    assert "transitionsPreviousLayoutRef.current = layout;" in src[effect:]


def test_each_node_is_painted_with_its_change_and_its_pulse():
    src = CANVAS.read_text(encoding="utf-8")
    assert "transition: record ? transitionFrameAt(record, now) : null," in src
    assert "pulseScale: pulseScaleAt(n.state, now, reducedMotion)," in src
    assert "NODE_PAINTERS[n.kind](n, ctx, globalScale, paint, resolvedPalette.palette, motionOf(n));" in src


def test_visibility_is_read_from_the_document_and_nothing_ticks_on_a_timer():
    hook = VISIBLE.read_text(encoding="utf-8")
    assert 'document.addEventListener("visibilitychange", onChange);' in hook
    assert 'document.removeEventListener("visibilitychange", onChange);' in hook
    assert 'document.visibilityState !== "hidden"' in hook
    for path in (CANVAS, VISIBLE):
        assert "setInterval" not in path.read_text(encoding="utf-8"), f"{path.name} animates on a timer"

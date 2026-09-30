import { createRoot } from "react-dom/client";
import { useMemo, useState } from "react";
import "../src/styles/globals.css";
import { ForceBrainGraph } from "../src/components/graph/ForceBrainGraph";
import { buildBrainLayout } from "../src/components/graph/buildForceBrainModel";
import {
  BRAIN_PERF_STAGE1_NODES,
  BRAIN_PERF_STAGE6_NODES,
  brainPerfModel,
} from "../src/components/graph/brainPerfFixture";
import { ZOOM_HOME } from "../src/components/graph/semanticZoom";
import { zoomEmphasis } from "../src/components/graph/zoomView";

// F044 T003's frame-pipeline trace stage mounts this harness and measures it over CDP
// (`tests/orchestration/test_ci_budgets.py`'s
// `test_this_repositorys_shell_sustains_60fps_at_200_nodes`), never a JS-side
// `requestAnimationFrame` timer: headless Chrome paces `requestAnimationFrame` at a fixed 60 Hz
// regardless of the real work a frame costs, so a timer read from inside the page can only show
// whether a frame was scheduled, never whether it was actually delivered on time (DECISION
// F044 D10). This harness therefore does nothing but mount the real graph, at the same root
// zoom level `BrainGraphStage.tsx` opens on, over the committed fixture (DECISION F019 D6), and
// let it settle; every number this stage reports comes from Chrome's own compositor, read from
// outside the page.
//
// No vetoes exist in this static fixture, so `vetoFaded`/`vetoHover` are the same empty values
// `BrainGraphStage.tsx` would compute for a dashboard with none; `onZoomEvent` is a no-op
// because this harness never dispatches a zoom interaction of its own.
//
// `../src/styles/globals.css` is imported for the same reason `apps/ui/src/main.tsx` imports it:
// the node painter's `resolvedPalette` reads design tokens through `getComputedStyle` on
// `document.documentElement` (`tokens_rules.md`, "a 2D canvas cannot read var()"), and without
// this stylesheet every token resolves to an empty string, which crashes `CanvasGradient.
// addColorStop` on the first paint — measured directly, by this round's reviewer, from a version
// of this harness that omitted the import.

function Harness() {
  const params = new URLSearchParams(window.location.search);
  const n = params.get("n") === String(BRAIN_PERF_STAGE6_NODES) ? BRAIN_PERF_STAGE6_NODES : BRAIN_PERF_STAGE1_NODES;
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const layout = useMemo(() => buildBrainLayout(brainPerfModel(n)), [n]);
  const emphasis = useMemo(() => zoomEmphasis(layout, ZOOM_HOME), [layout]);

  return (
    <div style={{ width: 1280, height: 800, position: "fixed", top: 0, left: 0 }}>
      <ForceBrainGraph
        layout={layout}
        selectedId={selectedId}
        onSelectNode={setSelectedId}
        zoom={ZOOM_HOME}
        emphasis={emphasis}
        onZoomEvent={() => {}}
        vetoFaded={new Set()}
        vetoHover={new Map()}
      />
    </div>
  );
}

const container = document.getElementById("root")!;
createRoot(container).render(<Harness />);

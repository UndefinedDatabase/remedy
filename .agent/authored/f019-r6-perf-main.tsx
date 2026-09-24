import { createRoot } from "react-dom/client";
import { useEffect, useMemo, useState } from "react";
import { ForceBrainGraph } from "../../apps/ui/src/components/graph/ForceBrainGraph";
import { buildBrainLayout } from "../../apps/ui/src/components/graph/buildForceBrainModel";
import {
  BRAIN_PERF_STAGE1_NODES,
  BRAIN_PERF_STAGE6_NODES,
  brainPerfModel,
} from "../../apps/ui/src/components/graph/brainPerfFixture";

// F019 R6 perf harness: the input is `brainPerfModel(n)` (the committed
// fixture, `apps/ui/src/components/graph/brainPerfFixture.ts`) laid out
// through the real `buildBrainLayout` — no generator of this harness's own.
//
// Headless Chrome still paces `requestAnimationFrame` at 60 Hz (its
// compositor runs off-screen but on the same vsync-driven loop as a headed
// browser), so this reading shows whether a frame was ever DROPPED
// (p95/meanFps falling under budget), not how much headroom remains above
// 60 fps — there is no "faster than 60" to observe here.

const WARMUP_MS = 2000;
const MEASURE_MS = 8000;

declare global {
  interface Window {
    __brainPerfResult?: {
      n: number;
      nodeCount: number;
      linkCount: number;
      frames: number;
      meanFps: number;
      p50Ms: number;
      p95Ms: number;
      totalMeasureMs: number;
      done: boolean;
    };
  }
}

function Harness() {
  const params = new URLSearchParams(window.location.search);
  const n = params.get("n") === String(BRAIN_PERF_STAGE6_NODES) ? BRAIN_PERF_STAGE6_NODES : BRAIN_PERF_STAGE1_NODES;
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const layout = useMemo(() => buildBrainLayout(brainPerfModel(n)), [n]);

  useEffect(() => {
    window.__brainPerfResult = {
      n,
      nodeCount: layout.nodes.length,
      linkCount: layout.links.length,
      frames: 0,
      meanFps: 0,
      p50Ms: 0,
      p95Ms: 0,
      totalMeasureMs: 0,
      done: false,
    };

    let raf = 0;
    let measuring = false;
    let startedAt = 0;
    const timestamps: number[] = [];

    function finish() {
      cancelAnimationFrame(raf);
      const frames = timestamps.length;
      const deltas: number[] = [];
      for (let i = 1; i < timestamps.length; i++) deltas.push(timestamps[i] - timestamps[i - 1]);
      deltas.sort((a, b) => a - b);
      const totalMs = frames > 0 ? timestamps[frames - 1] - timestamps[0] : 0;
      const meanFps = totalMs > 0 ? ((frames - 1) / (totalMs / 1000)) : 0;
      const pct = (p: number) => (deltas.length ? deltas[Math.min(deltas.length - 1, Math.floor(p * deltas.length))] : 0);
      window.__brainPerfResult = {
        n,
        nodeCount: layout.nodes.length,
        linkCount: layout.links.length,
        frames,
        meanFps: Number(meanFps.toFixed(2)),
        p50Ms: Number(pct(0.5).toFixed(3)),
        p95Ms: Number(pct(0.95).toFixed(3)),
        totalMeasureMs: Number(totalMs.toFixed(1)),
        done: true,
      };
    }

    function loop(ts: number) {
      if (measuring) {
        timestamps.push(ts);
        if (ts - startedAt >= MEASURE_MS) {
          finish();
          return;
        }
      }
      raf = requestAnimationFrame(loop);
    }

    const warmupTimer = setTimeout(() => {
      measuring = true;
      startedAt = performance.now();
    }, WARMUP_MS);
    raf = requestAnimationFrame(loop);

    return () => {
      clearTimeout(warmupTimer);
      cancelAnimationFrame(raf);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layout]);

  return (
    <div style={{ width: 1280, height: 800, position: "fixed", top: 0, left: 0 }}>
      <ForceBrainGraph layout={layout} selectedId={selectedId} onSelectNode={setSelectedId} />
    </div>
  );
}

const container = document.getElementById("root")!;
createRoot(container).render(<Harness />);

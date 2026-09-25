import "../../apps/ui/src/styles/tokens.css";
import { createRoot } from "react-dom/client";
import { useEffect, useMemo } from "react";
import { ForceBrainGraph } from "../../apps/ui/src/components/graph/ForceBrainGraph";
import { EvidencePanel } from "../../apps/ui/src/components/graph/EvidencePanel";
import { RunDetailPopover } from "../../apps/ui/src/components/graph/RunDetailPopover";
import { ZoomBreadcrumbs } from "../../apps/ui/src/components/graph/ZoomBreadcrumbs";
import { buildBrainLayout } from "../../apps/ui/src/components/graph/buildForceBrainModel";
import { BRAIN_PERF_STAGE6_NODES, brainPerfModel } from "../../apps/ui/src/components/graph/brainPerfFixture";
import { zoomBreadcrumbs, zoomGraphOf } from "../../apps/ui/src/components/graph/semanticZoom";
import type { ZoomEvent } from "../../apps/ui/src/components/graph/semanticZoom";
import { useSemanticZoom } from "../../apps/ui/src/components/graph/useSemanticZoom";
import { zoomCrumbLabel, zoomEmphasis } from "../../apps/ui/src/components/graph/zoomView";

// F023 R7 perf harness: the committed 500-node fixture (`brainPerfFixture.ts`)
// wired exactly as `BrainGraphStage.tsx` wires the zoom — the unexpanded layout
// for the zoom graph, the focused task's cluster expanded, the render effects,
// the breadcrumbs, the L2 run detail and the L3 evidence panel — and driven to
// the level the URL's `level` names before the frames are sampled. Headless
// Chrome paces requestAnimationFrame at 60 Hz, so this shows whether a frame
// was dropped, not the headroom above 60 fps (DECISION F019 D6).

const SETTLE_MS = 3000;
const MEASURE_MS = 8000;

// No server behind the harness: the doors answer null, and the run detail and
// the panel render their honest "could not be read" text.
window.fetch = (async () => new Response("null", { status: 200 })) as typeof window.fetch;

declare global {
  interface Window {
    __zoomPerfResult?: {
      level: number;
      reachedLevel: number;
      nodeCount: number;
      frames: number;
      meanFps: number;
      p50Ms: number;
      p95Ms: number;
      done: boolean;
    };
  }
}

function Harness() {
  const level = Number(new URLSearchParams(window.location.search).get("level") ?? "0");
  const model = useMemo(() => brainPerfModel(BRAIN_PERF_STAGE6_NODES), []);
  const baseLayout = useMemo(() => buildBrainLayout(model), [model]);
  const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, baseLayout.nodes), [model, baseLayout]);
  const zoom = useSemanticZoom(zoomGraph);
  const zoomCrumbs = zoomBreadcrumbs(zoomGraph, zoom.state);
  const expandTaskId = zoomCrumbs.find((c) => c.level === 1)?.nodeId ?? null;
  const layout = useMemo(
    () => (expandTaskId === null ? baseLayout : buildBrainLayout(model, expandTaskId)),
    [baseLayout, model, expandTaskId],
  );
  const emphasis = useMemo(() => zoomEmphasis(layout, zoom.state), [layout, zoom.state]);
  const crumbs = zoomCrumbs.map((c) => ({ level: c.level, current: c.current, label: zoomCrumbLabel(c, layout) }));
  const focusedRun = zoom.state.level >= 2 ? model.nodes.find((n) => n.id === zoom.state.focusId) ?? null : null;

  // Drive to the asked level through the machine's own events: the first
  // task that has runs, then its first run, then the diff tab.
  useEffect(() => {
    const task = model.nodes.find((n) => n.kind === "task" && model.nodes.some((r) => r.parentId === n.id));
    const run = task ? model.nodes.find((r) => r.parentId === task.id && r.kind.endsWith("_run")) : undefined;
    const events: ZoomEvent[] = [];
    if (level >= 1 && task) events.push({ type: "click", nodeId: task.id });
    if (level >= 2 && run) events.push({ type: "click", nodeId: run.id });
    if (level >= 3) events.push({ type: "open_evidence", tab: "diff" });
    events.forEach(zoom.dispatch);
  }, [level, model, zoom.dispatch]);

  const reachedLevel = zoom.state.level;
  useEffect(() => {
    let raf = 0;
    let measuring = false;
    let startedAt = 0;
    const stamps: number[] = [];
    window.__zoomPerfResult = { level, reachedLevel, nodeCount: layout.nodes.length, frames: 0, meanFps: 0, p50Ms: 0, p95Ms: 0, done: false };
    function finish() {
      cancelAnimationFrame(raf);
      const deltas: number[] = [];
      for (let i = 1; i < stamps.length; i++) deltas.push(stamps[i] - stamps[i - 1]);
      deltas.sort((a, b) => a - b);
      const total = stamps.length > 1 ? stamps[stamps.length - 1] - stamps[0] : 0;
      const pct = (p: number) => (deltas.length ? deltas[Math.min(deltas.length - 1, Math.floor(p * deltas.length))] : 0);
      window.__zoomPerfResult = {
        level, reachedLevel, nodeCount: layout.nodes.length, frames: stamps.length,
        meanFps: Number((total > 0 ? (stamps.length - 1) / (total / 1000) : 0).toFixed(2)),
        p50Ms: Number(pct(0.5).toFixed(3)), p95Ms: Number(pct(0.95).toFixed(3)), done: true,
      };
    }
    function loop(ts: number) {
      if (measuring) {
        stamps.push(ts);
        if (ts - startedAt >= MEASURE_MS) { finish(); return; }
      }
      raf = requestAnimationFrame(loop);
    }
    const timer = setTimeout(() => { measuring = true; startedAt = performance.now(); }, SETTLE_MS);
    raf = requestAnimationFrame(loop);
    return () => { clearTimeout(timer); cancelAnimationFrame(raf); };
  }, [level, reachedLevel, layout]);

  return (
    <section style={{ width: 1280, height: 800, position: "fixed", top: 0, left: 0 }}>
      <ForceBrainGraph layout={layout} selectedId={null} onSelectNode={() => {}}
        zoom={zoom.state} emphasis={emphasis} onZoomEvent={zoom.dispatch} />
      <ZoomBreadcrumbs items={crumbs} onJump={(l) => zoom.dispatch({ type: "crumb", level: l })} />
      {focusedRun && zoom.state.level === 2 && (
        <RunDetailPopover node={focusedRun} rows={[]} promptItems={[]} jobId="perf" token="t"
          onOpenEvidence={(tab) => zoom.dispatch({ type: "open_evidence", tab })}
          onClose={() => zoom.dispatch({ type: "escape" })} />
      )}
      {focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (
        <EvidencePanel node={focusedRun} tab={zoom.state.tab} rows={[]} promptItems={[]} jobId="perf" token="t"
          onTab={(tab) => zoom.dispatch({ type: "open_evidence", tab })}
          onClose={() => zoom.dispatch({ type: "escape" })} />
      )}
    </section>
  );
}

createRoot(document.getElementById("root")!).render(<Harness />);

import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { createRoot } from "react-dom/client";
import { useEffect, useRef } from "react";
import type { RemedyDashboard, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { BrainGraphStage } from "../../apps/ui/src/components/graph/BrainGraphStage";
import { BRAIN_PERF_STAGE6_NODES, brainPerfLedger } from "../../apps/ui/src/components/graph/brainPerfFixture";
import { buildBrainLayout } from "../../apps/ui/src/components/graph/buildForceBrainModel";
import { ReducedMotionProvider } from "../../apps/ui/src/components/shell/ReducedMotionProvider";
import { PhaseTimeline } from "../../apps/ui/src/components/timeline/PhaseTimeline";
import { extractSubGlyphs } from "../../apps/ui/src/components/timeline/phaseMapping";
import { createScrubMemo } from "../../apps/ui/src/components/timeline/scrubSnapshots";
import { buildTimelineIndex, phasesAt } from "../../apps/ui/src/components/timeline/timelineIndex";
import { buildTimelineView } from "../../apps/ui/src/components/timeline/timelineView";
import { useTimelineScrub } from "../../apps/ui/src/components/timeline/useTimelineScrub";

// F024 R5 scrub budget harness (DECISION F024 D5): the committed 500-node fixture's LEDGER
// (`brainPerfLedger`) mounted as the shell mounts it — one scrubber handed to the real stage and
// the real bar — then (1) every scrub position timed through the modules the hook calls, cold
// and warm, and (2) the handle swept one event per frame while the frames are sampled. Headless
// Chrome paces requestAnimationFrame at 60 Hz, so a frame reading shows whether a frame was
// dropped, not the headroom above it (DECISION F019 D6).

const SETTLE_MS = 3000;
const MEASURE_MS = 8000;
const SLOW_MS = Number(new URLSearchParams(window.location.search).get("slow") ?? "0");
const JOB = `perf-${BRAIN_PERF_STAGE6_NODES}`;
const { seeds, rows } = brainPerfLedger(BRAIN_PERF_STAGE6_NODES);
const TASKS = seeds.map((s) => ({ id: s.id, label: s.id, state: "pending", kind: "task" })) as unknown as RemedyTaskItem[];
const DASHBOARD = { jobId: JOB, tasks: TASKS, promptTrace: { items: [] } } as unknown as RemedyDashboard;
const HEAD = rows[rows.length - 1].seq;

function busyWait(ms: number) {
  const until = performance.now() + ms;
  while (performance.now() < until) { /* the red control's cost */ }
}

function pct(sorted: number[], p: number) {
  return sorted.length ? sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))] : 0;
}

// Every position, through the modules the hook calls per scrub step: the memo's state, the
// prefix's phases and the bar's view. The cold pass builds the snapshots on the way; the warm
// pass runs the positions again in reverse, as a drag back would.
function benchPositions() {
  const t0 = performance.now();
  const index = buildTimelineIndex(JOB, seeds, rows);
  const indexMs = performance.now() - t0;
  const glyphs = extractSubGlyphs(rows);
  const whole = phasesAt(index, HEAD);
  const memo = createScrubMemo(JOB, seeds);
  memo.append(rows);
  const time = (s: number) => {
    const start = performance.now();
    memo.stateAt(s);
    buildTimelineView({ whole, at: phasesAt(index, s), glyphs, position: s, elapsed: null });
    return performance.now() - start;
  };
  const cold: number[] = [];
  for (let s = -1; s <= HEAD; s += 1) cold.push(time(s));
  const warm: number[] = [];
  for (let s = HEAD; s >= -1; s -= 1) warm.push(time(s));
  cold.sort((a, b) => a - b);
  warm.sort((a, b) => a - b);
  const r3 = (v: number) => Number(v.toFixed(3));
  return {
    positions: cold.length,
    indexMs: r3(indexMs),
    coldP95Ms: r3(pct(cold, 0.95)), coldMaxMs: r3(cold[cold.length - 1]),
    warmP95Ms: r3(pct(warm, 0.95)), warmMaxMs: r3(warm[warm.length - 1]),
    snapshots: memo.stats().snapshots, reductions: memo.stats().reductions,
  };
}

declare global {
  interface Window { __scrubPerfResult?: Record<string, unknown> }
}

function Harness() {
  const scrub = useTimelineScrub(JOB, TASKS, rows);
  const scrubRef = useRef(scrub);
  scrubRef.current = scrub;

  useEffect(() => {
    const bench = benchPositions();
    const nodeCount = buildBrainLayout(brainPerfLedgerModel()).nodes.length;
    let raf = 0;
    let measuring = false;
    let startedAt = 0;
    let position = HEAD;
    let step = -1;
    const stamps: number[] = [];
    window.__scrubPerfResult = { done: false, bench, nodeCount, slowMs: SLOW_MS };
    function finish() {
      cancelAnimationFrame(raf);
      const deltas: number[] = [];
      for (let i = 1; i < stamps.length; i++) deltas.push(stamps[i] - stamps[i - 1]);
      deltas.sort((a, b) => a - b);
      const total = stamps.length > 1 ? stamps[stamps.length - 1] - stamps[0] : 0;
      window.__scrubPerfResult = {
        done: true, bench, nodeCount, rows: rows.length, slowMs: SLOW_MS,
        frames: stamps.length,
        meanFps: Number((total > 0 ? (stamps.length - 1) / (total / 1000) : 0).toFixed(2)),
        p50Ms: Number(pct(deltas, 0.5).toFixed(3)), p95Ms: Number(pct(deltas, 0.95).toFixed(3)),
        endedAt: position, mode: scrubRef.current.state.mode,
      };
    }
    function loop(ts: number) {
      if (measuring) {
        stamps.push(ts);
        if (ts - startedAt >= MEASURE_MS) { finish(); return; }
        // One event per frame, back and forth across the whole ledger: a drag.
        if (position + step < -1 || position + step > HEAD) step = -step;
        position += step;
        if (SLOW_MS > 0) busyWait(SLOW_MS);
        scrubRef.current.scrubTo(position);
      }
      raf = requestAnimationFrame(loop);
    }
    const timer = setTimeout(() => { measuring = true; startedAt = performance.now(); }, SETTLE_MS);
    raf = requestAnimationFrame(loop);
    return () => { clearTimeout(timer); cancelAnimationFrame(raf); };
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 12, padding: 12, width: 1256, height: 776, boxSizing: "border-box" }}>
      <div style={{ flex: 1, minHeight: 0, display: "flex" }}>
        <BrainGraphStage dashboard={DASHBOARD} onSelectNode={() => {}} rows={rows} scrub={scrub} serverToken="" />
      </div>
      <PhaseTimeline scrub={scrub} />
    </div>
  );
}

// The fixture's model at its head, laid out, for the node count the reading names.
function brainPerfLedgerModel() {
  const memo = createScrubMemo(JOB, seeds);
  memo.append(rows);
  return memo.stateAt(HEAD);
}

createRoot(document.getElementById("root")!).render(<ReducedMotionProvider><Harness /></ReducedMotionProvider>);

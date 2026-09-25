// The React half of the scrubber, deliberately thin (DECISION F024 D4): every rule
// — the machine, the keyboard, the catch-up plan, the phases of a prefix, the
// bar's view, the track's geometry — is pure and lives in scrubState.ts,
// timelineIndex.ts, timelineView.ts and scrubSnapshots.ts, where the
// node-environment vitest reaches it. What is left here is state, the timers of
// LIVE's fast-forward, and the one place the scrubbed graph state is read.
import { useCallback, useEffect, useMemo, useReducer, useRef, useState } from "react";
import type { RemedyTaskItem } from "../../api/types";
import type { BrainEventRow, BrainModel } from "../graph/brainOntology";
import { dashboardBrainSeeds } from "../graph/brainView";
import { useReducedMotion } from "../shell/ReducedMotionProvider";
import { extractSubGlyphs } from "./phaseMapping";
import type { PhaseReading } from "./phaseMapping";
import { createScrubMemo } from "./scrubSnapshots";
import {
  catchUpPlan,
  initialScrubState,
  scrubKeyEvent,
  scrubOverflowed,
  scrubReduce,
} from "./scrubState";
import type { ScrubState } from "./scrubState";
import { buildTimelineIndex, indexHead, phasesAt, phaseStops } from "./timelineIndex";
import { buildTimelineView, elapsedLabel } from "./timelineView";
import type { TimelineView } from "./timelineView";

export interface TimelineScrub {
  state: ScrubState;
  view: TimelineView;
  whole: PhaseReading;
  stops: number[];
  /** The reducer state at the handle while scrubbed; null while LIVE. */
  scrubbedModel: BrainModel | null;
  /** What LIVE's last return had to say, when it rebuilt instead of replaying. */
  notice: string | null;
  scrubTo: (seq: number) => void;
  onKey: (key: string, shiftKey: boolean) => boolean;
  goLive: () => void;
}

// A row's ledger timestamp, when the row carries one: the ledger's rows are
// feed rows (`feedRowOf`), which add it to the reducer's own shape.
function stampOf(row: BrainEventRow | undefined): string {
  const stamp = (row as { timestamp?: unknown } | undefined)?.timestamp;
  return typeof stamp === "string" ? stamp : "";
}

export function useTimelineScrub(
  jobId: string,
  tasks: readonly RemedyTaskItem[],
  rows: readonly BrainEventRow[],
): TimelineScrub {
  const reducedMotion = useReducedMotion();
  const seeds = useMemo(() => dashboardBrainSeeds(tasks), [tasks]);
  const index = useMemo(() => buildTimelineIndex(jobId, seeds, rows), [jobId, seeds, rows]);
  const glyphs = useMemo(() => extractSubGlyphs(rows), [rows]);
  const memo = useMemo(() => createScrubMemo(jobId, seeds), [jobId, seeds]);
  const fed = useMemo(() => {
    memo.append(rows);
    return memo;
  }, [memo, rows]);

  const head = indexHead(index) ?? -1;
  const [state, dispatch] = useReducer(scrubReduce, head, initialScrubState);
  useEffect(() => { dispatch({ type: "ingest", head }); }, [head]);

  // LIVE's fast-forward: one timer per frame, all cancelled by any new move.
  const timers = useRef<number[]>([]);
  const cancelCatchUp = useCallback(() => {
    for (const id of timers.current) window.clearTimeout(id);
    timers.current = [];
  }, []);
  useEffect(() => cancelCatchUp, [cancelCatchUp]);

  const [notice, setNotice] = useState<string | null>(null);

  const scrubTo = useCallback((seq: number) => {
    cancelCatchUp();
    setNotice(null);
    dispatch({ type: "scrub_to", seq });
  }, [cancelCatchUp]);

  const goLive = useCallback(() => {
    cancelCatchUp();
    if (state.mode === "live") return;
    if (scrubOverflowed(state)) {
      fed.reset(rows);
      setNotice(`${state.queued} events arrived while you looked back, so the view was rebuilt from the ledger.`);
      dispatch({ type: "go_live" });
      return;
    }
    setNotice(null);
    const frames = catchUpPlan(state.position, state.head, reducedMotion);
    for (const frame of frames) {
      timers.current.push(window.setTimeout(() => dispatch({ type: "scrub_to", seq: frame.seq }), frame.atMs));
    }
    const lastMs = frames.length > 0 ? frames[frames.length - 1].atMs : 0;
    timers.current.push(window.setTimeout(() => dispatch({ type: "go_live" }), lastMs));
  }, [cancelCatchUp, fed, reducedMotion, rows, state]);

  const stops = useMemo(() => phaseStops(index), [index]);
  const onKey = useCallback((key: string, shiftKey: boolean) => {
    const event = scrubKeyEvent(key, shiftKey, stops);
    if (event === null) return false;
    if (event.type === "go_live") {
      goLive();
    } else {
      cancelCatchUp();
      setNotice(null);
      dispatch(event);
    }
    return true;
  }, [cancelCatchUp, goLive, stops]);

  const whole = useMemo(() => phasesAt(index, head), [index, head]);
  const view = useMemo(() => {
    const at = phasesAt(index, state.position);
    const first = rows[0];
    const shown = state.position >= 0 ? rows[Math.min(state.position, rows.length - 1)] : undefined;
    const elapsed = shown ? elapsedLabel(stampOf(first), stampOf(shown)) : null;
    return buildTimelineView({ whole, at, glyphs, position: state.position, elapsed });
  }, [glyphs, index, rows, state.position, whole]);

  const scrubbedModel = useMemo(
    () => (state.mode === "scrubbed" ? fed.stateAt(state.position) : null),
    [fed, state.mode, state.position],
  );

  return { state, view, whole, stops, scrubbedModel, notice, scrubTo, onKey, goLive };
}

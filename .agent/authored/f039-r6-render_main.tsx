// F039 R6 T002's render harness (evidence, not product): mounts the real `useTimelineScrub`,
// the real `PhaseTimeline` and the real `StoryPanel` from `apps/ui/src` over the demo
// recording's own ledger and tasks (DECISION F039 D6), the way
// `.agent/authored/f036-r7-render_main.tsx` mounts the real `TourOverlay` over one fixed tour
// view. No door is read here: the panel and the scrub take only the props this harness hands
// them, built once from `normalizeApiFailure` the same way a dashboard that could not load
// still carries a shape every reader can hold. `window.__storyPositions` records every scrub
// position an effect on the position appends to, and `window.__storyClosed` records the
// panel's own close — never a second copy of the DOM's own state retyped into the driver
// script. The `running` query parameter (`?running=1`) sets `dashboard.live.running`, and the
// pacing is fast (`step_ms: 60, chapter_pause_ms: 150`) so `drive.mjs` never waits long for a
// walk to finish. R-1101's own churn proof: the `churn` query parameter (`?churn=1`) re-renders
// this host every 50 ms (a plain tick counter, unread by any child, so the re-render itself is
// the whole point) and appends one `feedRowOf` row of a `budget.tick` frame at the next seq
// every 200 ms, handing the growing `rows` array to both `useTimelineScrub` and `StoryPanel` the
// same way the streaming app does — the two rates R-1101's registration measured a stall at.
import { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { ReducedMotionProvider } from "../../apps/ui/src/components/shell/ReducedMotionProvider";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import { feedRowOf } from "../../apps/ui/src/api/feedRow";
import {
  BRAIN_DEMO_JOB_ID,
  BRAIN_DEMO_TASKS,
  brainDemoRows,
} from "../../apps/ui/src/components/graph/brainDemoRecording";
import { useTimelineScrub } from "../../apps/ui/src/components/timeline/useTimelineScrub";
import { PhaseTimeline } from "../../apps/ui/src/components/timeline/PhaseTimeline";
import { StoryPanel } from "../../apps/ui/src/components/story/StoryPanel";

const QUERY = new URLSearchParams(window.location.search);
const RUNNING = QUERY.get("running") === "1";
const CHURN = QUERY.get("churn") === "1";

(window as unknown as { __storyPositions: number[] }).__storyPositions = [];
(window as unknown as { __storyClosed: boolean }).__storyClosed = false;

function nextTickRow(rows: ReturnType<typeof brainDemoRows>) {
  const nextSeq = rows.reduce((max, row) => Math.max(max, row.seq), 0) + 1;
  return feedRowOf(
    { seq: nextSeq, event: { seq: nextSeq, event: "budget.tick", budget: { spent_usd: 0.01 * nextSeq } } },
    0,
  );
}

function Harness() {
  const [open, setOpen] = useState(true);
  const [rows, setRows] = useState(() => brainDemoRows());
  const [, setChurnTick] = useState(0);

  // Re-renders the host every 50 ms under `?churn=1` — the tick itself is read by nothing;
  // the re-render is the whole point (R-1101).
  useEffect(() => {
    if (!CHURN) return undefined;
    const id = window.setInterval(() => setChurnTick((tick) => tick + 1), 50);
    return () => window.clearInterval(id);
  }, []);

  // Appends one budget.tick row at the next seq every 200 ms under `?churn=1` (R-1101).
  useEffect(() => {
    if (!CHURN) return undefined;
    const id = window.setInterval(() => {
      setRows((current) => [...current, nextTickRow(current)]);
    }, 200);
    return () => window.clearInterval(id);
  }, []);

  const dashboard = useMemo(() => {
    const base = normalizeApiFailure(BRAIN_DEMO_JOB_ID, []);
    return {
      ...base,
      tasks: BRAIN_DEMO_TASKS,
      live: { ...base.live, running: RUNNING },
      story: { step_ms: 60, chapter_pause_ms: 150 },
    };
  }, []);
  const scrub = useTimelineScrub(dashboard.jobId, dashboard.tasks, rows);

  useEffect(() => {
    (window as unknown as { __storyPositions: number[] }).__storyPositions.push(scrub.state.position);
  }, [scrub.state.position]);

  return (
    <>
      <PhaseTimeline scrub={scrub} />
      {open && (
        <StoryPanel
          dashboard={dashboard}
          rows={rows}
          ownership={null}
          scrub={scrub}
          onClose={() => {
            (window as unknown as { __storyClosed: boolean }).__storyClosed = true;
            setOpen(false);
          }}
        />
      )}
    </>
  );
}

const container = document.getElementById("app");
if (container) {
  createRoot(container).render(
    <ReducedMotionProvider>
      <Harness />
    </ReducedMotionProvider>,
  );
}

// F039 R5 T002's render harness (evidence, not product): mounts the real `useTimelineScrub`,
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
// walk to finish.
import { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { ReducedMotionProvider } from "../../apps/ui/src/components/shell/ReducedMotionProvider";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import {
  BRAIN_DEMO_JOB_ID,
  BRAIN_DEMO_TASKS,
  brainDemoRows,
} from "../../apps/ui/src/components/graph/brainDemoRecording";
import { useTimelineScrub } from "../../apps/ui/src/components/timeline/useTimelineScrub";
import { PhaseTimeline } from "../../apps/ui/src/components/timeline/PhaseTimeline";
import { StoryPanel } from "../../apps/ui/src/components/story/StoryPanel";

const RUNNING = new URLSearchParams(window.location.search).get("running") === "1";

(window as unknown as { __storyPositions: number[] }).__storyPositions = [];
(window as unknown as { __storyClosed: boolean }).__storyClosed = false;

function Harness() {
  const [open, setOpen] = useState(true);
  const rows = useMemo(() => brainDemoRows(), []);
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

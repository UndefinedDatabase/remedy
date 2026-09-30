// F043 R1's render harness (evidence, not product): mounts the REAL `LiveStatusPill` and the
// REAL `PhaseTimeline` from `apps/ui/src` with the app's own token and global sheets. The pill
// sits in a small glass card pinned to the top right corner that clips its overflow, which is the
// trap a tooltip must escape (a `backdrop-filter` ancestor confines a fixed descendant and
// `overflow: hidden` clips an absolute one); the timeline's labels sit 56 pixels above the bottom
// edge, where a tooltip has no room below its term. Nothing here reads a door.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { LiveStatusPill } from "../../apps/ui/src/components/panels/LiveStatusPill";
import { PhaseTimeline } from "../../apps/ui/src/components/timeline/PhaseTimeline";
import { TIMELINE_PHASES } from "../../apps/ui/src/components/timeline/phaseMapping";
import { PHASE_LABELS } from "../../apps/ui/src/components/timeline/timelineView";
import type { TimelineScrub } from "../../apps/ui/src/components/timeline/useTimelineScrub";

const EMPTY_SCRUB: TimelineScrub = {
  state: { mode: "live", position: -1, head: -1, queued: 0 },
  view: {
    segments: TIMELINE_PHASES.map((phase) => ({
      phase, label: PHASE_LABELS[phase], state: "future", compact: false, fill: 0,
    })),
    glyphs: [],
    readout: "No events yet",
  },
  whole: { current: "job", spans: [], lastSeq: null },
  stops: [],
  scrubbedModel: null,
  notice: null,
  scrubTo: () => {},
  onKey: () => false,
  goLive: () => {},
};

function Harness() {
  return (
    <>
      <div
        className="remedy-glass-card"
        data-ui="clip-card"
        style={{ position: "fixed", top: 8, right: 4, width: 110, height: 44, overflow: "hidden", padding: 6 }}
      >
        <LiveStatusPill live={true} />
      </div>
      <div data-ui="bottom-dock" style={{ position: "fixed", left: 0, right: 0, top: "calc(100vh - 56px)" }}>
        <PhaseTimeline scrub={EMPTY_SCRUB} />
      </div>
    </>
  );
}

createRoot(document.getElementById("root")!).render(<Harness />);

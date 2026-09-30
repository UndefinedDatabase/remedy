// F043 R2's render harness (evidence, not product): mounts the REAL `TopMetricsBar`, the REAL
// `BrainGraphStage` held scrubbed, and the REAL `RightLivePanel` from `apps/ui/src` with the
// app's own token and global sheets, over a
// fixed running job: a task in each state the task list words differently, one open decision,
// and an action a moment ago, so the NowCard's Live badge shows. The panel sits against the
// right edge, as it does in the shell. Nothing here reads a door; a `window.fetch` stand-in
// answers every request with a 500 so no card waits on the network.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { buildDecisionCardModel } from "../../apps/ui/src/api/decisionCard";
import type { FeedRow } from "../../apps/ui/src/api/feedRow";
import { normalizeApiFailure } from "../../apps/ui/src/api/remedyApi";
import type { RemedyMetric, RemedyState, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { BrainGraphStage } from "../../apps/ui/src/components/graph/BrainGraphStage";
import { TopMetricsBar } from "../../apps/ui/src/components/metrics/TopMetricsBar";
import { RightLivePanel } from "../../apps/ui/src/components/panels/RightLivePanel";
import { TIMELINE_PHASES } from "../../apps/ui/src/components/timeline/phaseMapping";
import { PHASE_LABELS } from "../../apps/ui/src/components/timeline/timelineView";
import type { TimelineScrub } from "../../apps/ui/src/components/timeline/useTimelineScrub";

window.fetch = async (): Promise<Response> => new Response("{}", { status: 500 });

function task(id: string, state: RemedyState, applyStatus?: string): RemedyTaskItem {
  return {
    id, label: `Task ${id}`, state, kind: "task", checked: state === "done", muted: false, nodeId: `node-${id}`,
    ...(applyStatus === undefined ? {} : { applyStatus }),
  };
}

const base = normalizeApiFailure("job-1", []);
const dashboard = {
  ...base,
  live: { ...base.live, running: true },
  tasks: [task("a", "done"), task("b", "current"), task("c", "blocked"), task("d", "pending"), task("e", "done", "partial")],
  decisionInbox: [buildDecisionCardModel({ id: "d-1", status: "open", type: "clarification", age_seconds: 60, blocked_count: 1 })],
};
const recent: FeedRow[] = [{
  seq: 1, receivedAtMs: Date.now(), kind: "builder_started", line: "The builder started.", known: true,
  timestamp: "", outcome: "", taskId: "",
}];
const METRICS: RemedyMetric[] = [
  { key: "open", label: "Open", value: 1 },
  { key: "planned", label: "Planned", value: 1 },
  { key: "done", label: "Done", value: 2 },
  { key: "progress", label: "Progress", value: 40, suffix: "%" },
  { key: "tests", label: "Tests", value: 3, state: "pass" },
  { key: "proof", label: "Proof", value: 1, suffix: "/2" },
  { key: "tokens", label: "Tokens", value: 1200, tooltip: { builder: 1200 } },
];

/** A scrubber held back from the head, which is what makes the stage draw its SCRUBBED banner. */
const SCRUBBED: TimelineScrub = {
  state: { mode: "scrubbed", position: -1, head: -1, queued: 0 },
  view: {
    segments: TIMELINE_PHASES.map((phase) => ({
      phase, label: PHASE_LABELS[phase], state: "future", compact: false, fill: 0,
    })),
    glyphs: [],
    readout: "Before the first event",
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
    <div style={{ display: "flex", gap: 16, padding: 12, alignItems: "flex-start" }}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <TopMetricsBar metrics={METRICS} />
        <div style={{ position: "relative", height: 420, marginTop: 12 }}>
          <BrainGraphStage dashboard={dashboard} onSelectNode={() => {}} rows={[]} scrub={SCRUBBED} serverToken="token" />
        </div>
      </div>
      <div style={{ width: 372, flex: "none" }}>
        <RightLivePanel dashboard={dashboard} serverToken="token" onSelectNode={() => {}} recent={recent} />
      </div>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(<Harness />);

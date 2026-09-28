// F035 R7 T003, R-1083's repair — the render harness (evidence, not product):
// paints three mounts of `DetailPopover` and, once opened, one of
// `EvidencePanel` on its ownership tab, all reading ONE fixed `OwnershipView`
// through a `window.fetch` this page replaces (DECISION F035 D6). The task
// list is the demo recording's own two tasks (`brainDemoRecording.ts`) plus
// one synthetic third task no entry names and one vetoing task, so the
// popover's own "Unreachable" section (read from `dashboard.vetoes`, a
// structure entirely separate from the ownership ledger) and the ownership
// section can be proved sitting together in the order `DetailPopover.tsx`
// writes them. R-1083's repair: the evidence panel is NOT mounted at first
// paint, so `render-detail.png` shows the task detail with entries alone;
// `window.__openPanel()` (called by drive.mjs between screenshots) mounts it
// for `render-tab.png` and the checks that read it.
import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import type { RemedyDashboard, RemedyGraphNode, RemedyTaskItem } from "../../apps/ui/src/api/types";
import { decodeOwnershipView, ownershipViewPath } from "../../apps/ui/src/api/ownership";
import type { EvidenceTab } from "../../apps/ui/src/components/graph/semanticZoom";
import { isZoomRunKind } from "../../apps/ui/src/components/graph/semanticZoom";
import { BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "../../apps/ui/src/components/graph/brainDemoRecording";
import { rebuildBrainModel } from "../../apps/ui/src/components/graph/brainReducer";
import { dashboardBrainSeeds } from "../../apps/ui/src/components/graph/brainView";
import { DetailPopover } from "../../apps/ui/src/components/detail/DetailPopover";
import { EvidencePanel } from "../../apps/ui/src/components/graph/EvidencePanel";

const JOB_ID = BRAIN_DEMO_JOB_ID;
const TOKEN = "harness-token";

// The recording's own two tasks — never retyped, read off it.
const [TASK_A, TASK_B] = BRAIN_DEMO_TASKS.map((t) => t.id);
// A third task no ownership entry names, and the task whose OWN veto (read
// through `dashboard.vetoes`, not the ownership ledger) makes task A
// unreachable — this popover's "Unreachable" section is a different data
// model from the ownership ledger's own ("Who did what") section, and this
// harness proves the two sit together in one render.
const TASK_C = "9c00000000000003";
const TASK_X = "9c00000000000099";

const TASK_C_ITEM: RemedyTaskItem = {
  id: TASK_C, label: "Deliver docs/notes.md", state: "pending", kind: "task",
  checked: false, muted: true, nodeId: TASK_C,
  testStatus: "none", proofStatus: "none", applyStatus: "not_applied",
};
const TASK_X_ITEM: RemedyTaskItem = {
  id: TASK_X, label: "Deliver the auth check", state: "blocked", kind: "task",
  checked: false, muted: true, nodeId: TASK_X,
  testStatus: "none", proofStatus: "none", applyStatus: "not_applied",
};

function graphNodeOf(task: RemedyTaskItem): RemedyGraphNode {
  return {
    id: task.id, label: task.label, kind: "task", state: task.state,
    nodeId: task.nodeId, visibleFromZoom: 0, showLabelFromZoom: 0,
  };
}
const NODE_A = graphNodeOf(BRAIN_DEMO_TASKS[0]);
const NODE_C = graphNodeOf(TASK_C_ITEM);

const DASHBOARD: RemedyDashboard = {
  jobId: JOB_ID,
  title: "Harness job",
  description: "",
  conceptLabel: "",
  metrics: [],
  budgetFinal: null,
  phases: [],
  tasks: [...BRAIN_DEMO_TASKS, TASK_C_ITEM, TASK_X_ITEM],
  activity: [],
  graph: { nodes: [], edges: [] },
  nextAction: { label: "", command: "", risk: "low", requiresHuman: false },
  live: { running: false, stage: "", activeTaskLabel: "", latestMessage: "", latestActor: "System" },
  apiHealth: { degraded: false, failedEndpoints: [] },
  pipeline: null,
  resume: null,
  pause: { record: {}, requested: false, pausedTaskIds: [], error: "" },
  taskSpecs: { tasks: {}, error: "" },
  // DECISION F027 D7 (1) — task X's own veto names task A as unreachable;
  // task A carries no veto of its OWN here, so the popover's "Unreachable"
  // section renders for it rather than "Veto" (the two are mutually
  // exclusive in `DetailPopover.tsx`).
  vetoes: {
    tasks: [{
      taskId: TASK_X,
      reason: "the auth check underneath it is broken",
      actor: "operator (command line)",
      requestedAt: "2026-09-27T00:55:00+00:00",
      requestId: "req-1",
      statusAtVeto: "planned",
      unreachableTaskIds: [TASK_A],
      answer: "",
    }],
    vetoableTaskIds: [],
    unreachableTaskIds: [TASK_A],
    error: "",
  },
  projectSummary: null,
  snapshot: null,
  continuation: null,
  decisionInbox: [],
};

// The ownership ledger's own fixed view (DECISION F035 D6): a task veto of
// task A with a two-line reason, a note to task A, a pause of task B, and a
// job stop naming no task (task_id "", consequence.task_ids []) — the four
// entries S4 orders. The wire shape `decodeOwnershipView` reads, never
// retyped from a Python source: this harness authors the already-rendered
// sentences directly, exactly as the server's own view arrives over the
// wire.
const OWNERSHIP_WIRE = {
  schema: "remedy.ownership.v1",
  job_id: JOB_ID,
  error: "",
  entries: [
    {
      record_ref: "rec-veto-1",
      ts: "2026-09-27T00:55:01+00:00",
      actor: { kind: "operator", door: "cli", recorded_as: "cli", token_number: 3, auto_approved: false },
      action: "task_vetoed",
      task_id: TASK_A,
      text: "known-bad approach\nit splits the auth check across two files",
      consequence: { kind: "", task_ids: [], ref: "" },
      detail: {},
      sentence: "You (command line) vetoed Task A: known-bad approach\nit splits the auth check across two files.",
    },
    {
      record_ref: "rec-note-1",
      ts: "2026-09-27T00:55:05+00:00",
      actor: { kind: "operator", door: "cli", recorded_as: "cli", token_number: 4, auto_approved: false },
      action: "note_sent",
      task_id: TASK_A,
      text: "check the migration order before rerunning",
      consequence: { kind: "", task_ids: [], ref: "" },
      detail: {},
      sentence: "You (command line) sent a note to Task A: “check the migration order before rerunning”. The task has not taken it in.",
    },
    {
      record_ref: "rec-pause-1",
      ts: "2026-09-27T00:55:10+00:00",
      actor: { kind: "operator", door: "cli", recorded_as: "cli", token_number: 5, auto_approved: false },
      action: "task_paused",
      task_id: TASK_B,
      text: "",
      consequence: { kind: "", task_ids: [], ref: "" },
      detail: {},
      sentence: "You (command line) paused Task B.",
    },
    {
      record_ref: "rec-stop-1",
      ts: "2026-09-27T00:55:15+00:00",
      actor: { kind: "operator", door: "cli", recorded_as: "cli", token_number: 6, auto_approved: false },
      action: "job_stopped",
      task_id: "",
      text: "",
      consequence: { kind: "", task_ids: [], ref: "" },
      detail: {},
      sentence: "You (command line) stopped the job.",
    },
  ],
};
const OWNERSHIP_VIEW = decodeOwnershipView(OWNERSHIP_WIRE)!;
const OWNERSHIP_ERRORED = decodeOwnershipView({ ...OWNERSHIP_WIRE, entries: [], error: "boom: secret" })!;

// Exposed for drive.mjs, which cross-checks the rendered chips and sentences
// against the SAME decoded view and task id — never a second copy retyped
// into the driver script.
(window as unknown as { __ownershipView: typeof OWNERSHIP_VIEW }).__ownershipView = OWNERSHIP_VIEW;
(window as unknown as { __taskA: string }).__taskA = TASK_A;

// The run node (iv)'s `EvidencePanel` opens on: any run of task A the demo
// recording's own frames produced, read off the SAME model
// `rebuildBrainModel` builds elsewhere in the app — never invented here.
const seeds = dashboardBrainSeeds(BRAIN_DEMO_TASKS);
const rows = brainDemoRows();
const model = rebuildBrainModel(JOB_ID, seeds, rows);
const runNode = model.nodes.find((n) => isZoomRunKind(n.kind) && n.parentId === `task:${TASK_A}`);
if (!runNode) throw new Error("no run node for task A in the demo recording");

const OWNERSHIP_URL = ownershipViewPath({ jobId: JOB_ID, token: TOKEN });

// The window.fetch replacement (DECISION F035 D6's S4): the evidence panel's
// ownership tab reaches the network through `loadOwnershipView`, which
// defaults to the real `fetch`; this is the ONE seam the harness uses to
// hand it the fixed view instead of a live server. Installed at MODULE LOAD,
// before `createRoot(...).render(...)` below runs a single React commit —
// `OwnershipTab`'s own effect, nested under it, would otherwise fire before
// a patch installed in `Harness`'s effect (children's effects run before
// their parent's in the same commit) and reach the real network first.
const originalFetch = window.fetch.bind(window);
window.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
  if (url === OWNERSHIP_URL) {
    return new Response(JSON.stringify(OWNERSHIP_WIRE), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }
  return originalFetch(input, init);
}) as typeof window.fetch;

function Harness() {
  const [tab, setTab] = useState<EvidenceTab>("ownership");
  // R-1083's repair: the panel starts UNMOUNTED, so render-detail.png shows
  // the task detail alone; drive.mjs calls window.__openPanel() between the
  // two screenshots to mount it for render-tab.png.
  const [panelOpen, setPanelOpen] = useState(false);
  useEffect(() => {
    (window as unknown as { __openPanel: () => void }).__openPanel = () => setPanelOpen(true);
  }, []);

  return (
    <div style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
      <div id="popover-a" style={{ position: "relative", width: 820, height: 700 }}>
        <DetailPopover dashboard={DASHBOARD} selectedNode={NODE_A} onClose={() => {}} ownership={OWNERSHIP_VIEW} />
      </div>
      <div id="popover-c" style={{ position: "relative", width: 820, height: 700 }}>
        <DetailPopover dashboard={DASHBOARD} selectedNode={NODE_C} onClose={() => {}} ownership={OWNERSHIP_VIEW} />
      </div>
      <div id="popover-a-error" style={{ position: "relative", width: 820, height: 700 }}>
        <DetailPopover dashboard={DASHBOARD} selectedNode={NODE_A} onClose={() => {}} ownership={OWNERSHIP_ERRORED} />
      </div>
      {panelOpen && (
        <EvidencePanel
          node={runNode}
          tab={tab}
          rows={rows}
          promptItems={[]}
          jobId={JOB_ID}
          token={TOKEN}
          onTab={setTab}
          onClose={() => {}}
        />
      )}
    </div>
  );
}

const container = document.getElementById("app");
if (container) createRoot(container).render(<Harness />);

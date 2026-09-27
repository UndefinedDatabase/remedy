// F288 R6 T003 second half — the render harness (evidence, not product):
// paints the stage's LIVE wiring, without the stage component itself, from
// the demo recording (brainDemoRecording.ts) plus a four-item prompt trace
// — a builder item and a reviewer item of round 1 for each of the two
// recorded tasks, `runId` each task's own recorded attempt id — through
// `rebuildBrainModel`, `withPromptNodes`, `buildBrainLayout`, the semantic
// zoom exactly as the stage wires it, `<ForceBrainGraph>` and
// `<PromptNodeList>` with `promptListEntries` (DECISION F288 D6). The page
// renders nothing focusable before the list, so Tab's first stop is the
// list's own first button. A selection is kept in React state and mirrored
// to `window.__selected`; `window.__layout` holds the built layout, for
// `drive.mjs` to read both without a second source of truth.
import { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import type { RemedyPromptTraceItem } from "../../apps/ui/src/api/types";
import { BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "../../apps/ui/src/components/graph/brainDemoRecording";
import { rebuildBrainModel } from "../../apps/ui/src/components/graph/brainReducer";
import { dashboardBrainSeeds, promptListEntries } from "../../apps/ui/src/components/graph/brainView";
import { buildBrainLayout } from "../../apps/ui/src/components/graph/buildForceBrainModel";
import { ForceBrainGraph } from "../../apps/ui/src/components/graph/ForceBrainGraph";
import { promptNodeId, withPromptNodes } from "../../apps/ui/src/components/graph/promptNodes";
import { PromptNodeList } from "../../apps/ui/src/components/graph/PromptNodeList";
import { zoomGraphOf } from "../../apps/ui/src/components/graph/semanticZoom";
import { useSemanticZoom } from "../../apps/ui/src/components/graph/useSemanticZoom";
import { zoomEmphasis } from "../../apps/ui/src/components/graph/zoomView";

function promptItem(id: string, taskId: string, runId: string, role: "builder" | "reviewer"): RemedyPromptTraceItem {
  return {
    id, taskId, runId, round: 1, role, promptKind: "initial",
    provider: "fake", providerKind: "fake", promptSha256: "", promptChars: 0,
    promptTokensEstimated: 0, contextCategories: [], changedFilesSafe: [],
    safeDiffFiles: [], evidenceRef: "", redactedPreview: "", redactedPreviewTruncated: false,
  };
}

// The recording's own two tasks and their recorded attempt ids
// (brainDemoRecording.ts's BRAIN_DEMO_FRAMES) — never retyped, read off it.
const [TASK_A, TASK_B] = BRAIN_DEMO_TASKS.map((t) => t.id);
const RUN_A = brainDemoRows().find((r) => r.taskId === TASK_A)!.attemptId!;
const RUN_B = brainDemoRows().find((r) => r.taskId === TASK_B)!.attemptId!;

const PROMPT_TRACE: RemedyPromptTraceItem[] = [
  promptItem("p-a-builder", TASK_A, RUN_A, "builder"),
  promptItem("p-a-reviewer", TASK_A, RUN_A, "reviewer"),
  promptItem("p-b-builder", TASK_B, RUN_B, "builder"),
  promptItem("p-b-reviewer", TASK_B, RUN_B, "reviewer"),
];

const seeds = dashboardBrainSeeds(BRAIN_DEMO_TASKS);
const rows = brainDemoRows();
const baseModel = rebuildBrainModel(BRAIN_DEMO_JOB_ID, seeds, rows);
const model = withPromptNodes(baseModel, PROMPT_TRACE);

function Harness() {
  const layout = useMemo(() => buildBrainLayout(model), []);
  const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, layout.nodes), [layout]);
  const zoom = useSemanticZoom(zoomGraph);
  const entries = useMemo(() => promptListEntries(model, layout), [layout]);
  const emphasis = useMemo(() => zoomEmphasis(layout, zoom.state), [layout, zoom.state]);
  const [selectedPromptId, setSelectedPromptId] = useState<string | null>(null);
  const selectedNodeId = selectedPromptId === null ? null : promptNodeId(selectedPromptId);

  (window as unknown as { __layout: unknown }).__layout = layout;
  (window as unknown as { __selected: string | null }).__selected = selectedPromptId;

  return (
    <div style={{ position: "relative", width: 1280, height: 800 }}>
      <ForceBrainGraph
        layout={layout}
        selectedId={selectedNodeId}
        onSelectNode={() => {}}
        zoom={zoom.state}
        emphasis={emphasis}
        onZoomEvent={zoom.dispatch}
        vetoFaded={new Set()}
        vetoHover={new Map()}
      />
      <PromptNodeList entries={entries} selectedId={selectedNodeId} onSelect={(promptId) => setSelectedPromptId(promptId)} />
    </div>
  );
}

const container = document.getElementById("app");
if (container) createRoot(container).render(<Harness />);

import type { RemedyDashboard } from "../../api/types";
import { LeftBrandRail } from "../rail/LeftBrandRail";
import { TopMetricsBar } from "../metrics/TopMetricsBar";
import { CommandBar } from "../command/CommandBar";
import { BrainGraphStage } from "../graph/BrainGraphStage";
import { RightLivePanel } from "../panels/RightLivePanel";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { DetailPopover } from "../detail/DetailPopover";
import { DegradedBanner } from "./DegradedBanner";
import styles from "./RemedyShell.module.css";
import { browserBrainStreamEnv, createBrainStreamHostDeps } from "../../api/brainStreamDeps";
import { useBrainStream } from "../../api/useBrainStream";
import { metricsWithCostTicker } from "../../api/costTicker";

export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  // The cockpit subscribes HERE rather than in RemedyApp: the shell renders
  // only once a dashboard has loaded, so `dashboard.jobId` is always a real
  // job, where RemedyApp would have to open a stream against an empty id on
  // every URL that carries none (DECISION F008 D3).
  const stream = useBrainStream(dashboard.jobId, (jobId) =>
    createBrainStreamHostDeps(jobId, browserBrainStreamEnv(window)));
  let selectedNode = selectedNodeId ? (dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? null) : null;
  // Prompt satellite nodes carry the prompt item id as their node id. Resolve
  // such a selection to its owning task node so the popover (and its Prompt
  // Trace panel) opens with the prompt highlighted.
  let selectedPromptId: string | null = null;
  if (!selectedNode && selectedNodeId) {
    const promptItem = dashboard.promptTrace?.items.find(p => p.id === selectedNodeId);
    if (promptItem) {
      selectedPromptId = promptItem.id;
      const owningTask = dashboard.tasks.find(t => t.id === promptItem.taskId);
      if (owningTask) {
        selectedNode = dashboard.graph.nodes.find(n => n.nodeId === owningTask.nodeId) ?? null;
      }
    }
  }
  // Jump-to: case-insensitive match over real task labels; focus the first match's node.
  const handleJump = (query: string) => {
    const q = query.toLowerCase();
    const match = dashboard.tasks.find(t => t.label.toLowerCase().includes(q));
    if (match) onSelectNode(match.nodeId);
  };
  return (
    <div className={styles.viewport}>
      <DegradedBanner apiHealth={dashboard.apiHealth} />
      <div className={`${styles.shell} remedy-journey-shell`} data-ui="remedy-visual-v2">
        <LeftBrandRail dashboard={dashboard} />
        <main className={styles.main} data-testid="main-column">
          <TopMetricsBar metrics={metricsWithCostTicker(dashboard.metrics, stream.budget)} />
          <CommandBar nextAction={dashboard.nextAction} onJump={handleJump} />
          <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
          <PhaseTimeline phases={dashboard.phases} timelineEvents={dashboard.timelineEvents} />
        </main>
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} streamStatus={stream.status} recent={stream.recent} recentDropped={stream.recentDropped} />
      </div>
      {selectedNode && <DetailPopover dashboard={dashboard} selectedNode={selectedNode} selectedPromptId={selectedPromptId} onClose={() => onSelectNode(null)} />}
    </div>
  );
}

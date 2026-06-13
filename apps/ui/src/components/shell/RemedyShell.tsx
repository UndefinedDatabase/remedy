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

export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  const selectedNode = selectedNodeId ? (dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? null) : null;
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
          <TopMetricsBar metrics={dashboard.metrics} />
          <CommandBar nextAction={dashboard.nextAction} onJump={handleJump} />
          <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
          <PhaseTimeline phases={dashboard.phases} timelineEvents={dashboard.timelineEvents} />
        </main>
        <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} />
      </div>
      {selectedNode && <DetailPopover dashboard={dashboard} selectedNode={selectedNode} onClose={() => onSelectNode(null)} />}
    </div>
  );
}

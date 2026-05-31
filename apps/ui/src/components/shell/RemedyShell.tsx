import type { RemedyDashboard } from "../../api/types";
import { LeftBrandRail } from "../rail/LeftBrandRail";
import { TopMetricsBar } from "../metrics/TopMetricsBar";
import { CommandBar } from "../command/CommandBar";
import { BrainGraphStage } from "../graph/BrainGraphStage";
import { RightLivePanel } from "../panels/RightLivePanel";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { DetailPopover } from "../detail/DetailPopover";
import { LayerSwitcher } from "../layers/LayerSwitcher";
import styles from "./RemedyShell.module.css";

export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  const selectedNode = selectedNodeId ? (dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? null) : null;
  return (
    <div className={styles.viewport}>
      <div className={`${styles.frame} remedy-journey-shell remedy-visual-v2`} data-ui="remedy-shell" data-ui-v2="remedy-visual-v2">
        <div className={styles.leftRail}>
          <LeftBrandRail dashboard={dashboard} />
        </div>
        <div className={styles.centerStage}>
          <div className={styles.topMetricsSlot}>
            <TopMetricsBar metrics={dashboard.metrics} />
          </div>
          <div className={styles.commandSlot}>
            <CommandBar nextAction={dashboard.nextAction} />
          </div>
          <div className={styles.graphSlot}>
            <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
          </div>
          <div className={styles.timelineSlot}>
            <PhaseTimeline phases={dashboard.phases} />
          </div>
        </div>
        <div className={styles.rightPanelSlot}>
          <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} />
        </div>
        <LayerSwitcher />
        {selectedNode && <DetailPopover dashboard={dashboard} selectedNode={selectedNode} onClose={() => onSelectNode(null)} />}
      </div>
    </div>
  );
}

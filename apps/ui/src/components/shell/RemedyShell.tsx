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

export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void }) {
  const selectedNode = dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? dashboard.graph.nodes[0];
  return (
    <div className={`${styles.shell} remedy-journey-shell`} data-ui="remedy-shell">
      <div className={styles.backgroundAura} aria-hidden="true" />
      <LeftBrandRail dashboard={dashboard} />
      <main className={styles.mainStage}>
        <TopMetricsBar metrics={dashboard.metrics} />
        <CommandBar nextAction={dashboard.nextAction} />
        <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNode?.id ?? null} onSelectNode={onSelectNode} />
        <PhaseTimeline phases={dashboard.phases} />
      </main>
      <RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} />
      <LayerSwitcher />
      <DetailPopover dashboard={dashboard} selectedNode={selectedNode} />
    </div>
  );
}

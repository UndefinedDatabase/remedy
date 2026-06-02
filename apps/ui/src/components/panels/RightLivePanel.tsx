import type { RemedyDashboard } from "../../api/types";
import { PipelinePanel } from "../pipeline/PipelinePanel";
import { ActivityFeedCard } from "./ActivityFeedCard";
import { AgentNowCard } from "./AgentNowCard";
import { LiveStatusPill } from "./LiveStatusPill";
import { TaskChecklistCard } from "./TaskChecklistCard";
import styles from "./RightLivePanel.module.css";

export function RightLivePanel({ dashboard, onSelectNode }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void }) {
  return (
    <aside className={styles.panel} data-ui="right-live-panel">
      <LiveStatusPill live={dashboard.live.running} />
      <AgentNowCard dashboard={dashboard} />
      <PipelinePanel pipeline={dashboard.pipeline} resume={dashboard.resume} />
      <ActivityFeedCard activity={dashboard.activity} />
      <TaskChecklistCard tasks={dashboard.tasks} onSelectNode={onSelectNode} />
    </aside>
  );
}

import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { BrainStreamStatus } from "../../api/brainStream";
import type { FeedRow } from "../../api/feedRow";
import { liveIsActive } from "../../cockpitLogic";
import { NeedsAttentionCard } from "./NeedsAttentionCard";
import { DecisionInboxCard } from "./DecisionInboxCard";
import { ActivityFeedCard } from "./ActivityFeedCard";
import { AgentNowCard } from "./AgentNowCard";
import { LiveStatusPill } from "./LiveStatusPill";
import { TaskChecklistCard } from "./TaskChecklistCard";
import styles from "./RightLivePanel.module.css";

export function RightLivePanel({ dashboard, onSelectNode, streamStatus, recent, recentDropped }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null; recent?: readonly FeedRow[]; recentDropped?: number }) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  return (
    <aside className={styles.panel} data-ui="right-live-panel">
      <LiveStatusPill live={liveIsActive(dashboard)} streamStatus={streamStatus} />
      <AgentNowCard dashboard={dashboard} recent={recent} />
      <NeedsAttentionCard dashboard={dashboard} />
      <DecisionInboxCard decisions={dashboard.decisionInbox} />
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} tasks={dashboard.tasks} onSelectNode={onSelectNode} />
      <TaskChecklistCard tasks={dashboard.tasks} jobId={dashboard.jobId} onSelectNode={onSelectNode} />
      <button
        type="button"
        className={styles.advancedToggle}
        onClick={() => setShowAdvanced(!showAdvanced)}
        aria-expanded={showAdvanced}
      >
        {showAdvanced ? "Hide system details" : "System details"}
      </button>
      {showAdvanced && (
        <div className={styles.advancedSection} data-testid="advanced-details">
          {dashboard.workerStatus && (
            <div className={styles.advancedItem}>
              <strong>Worker:</strong> {dashboard.workerStatus.lifecycle_state}
              {dashboard.workerStatus.why_it_stopped && ` — ${dashboard.workerStatus.why_it_stopped.replace(/_/g, " ")}`}
            </div>
          )}
          {dashboard.pipeline && (
            <div className={styles.advancedItem}>
              <strong>Pipeline:</strong> {dashboard.pipeline.stop_reason || "running"}
            </div>
          )}
          {dashboard.projectSummary && (
            <div className={styles.advancedItem}>
              <strong>Project:</strong> {dashboard.projectSummary.job_count} jobs, {dashboard.projectSummary.current_focus || "idle"}
            </div>
          )}
        </div>
      )}
    </aside>
  );
}

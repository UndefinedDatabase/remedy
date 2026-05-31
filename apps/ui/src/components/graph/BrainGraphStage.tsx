import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { RemedyBrainFlow } from "./RemedyBrainFlow";
import { ConstellationBackdrop } from "./ConstellationBackdrop";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  return (
    <section className={styles.stage} aria-label="Growing brain graph" data-ui="brain-graph-stage">
      <div className={styles.haloA} aria-hidden="true" />
      <div className={styles.haloB} aria-hidden="true" />
      <ConstellationBackdrop jobId={dashboard.jobId || "default"} />
      <RemedyBrainFlow dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} filter={filter} />
      <GraphFilterChips value={filter} onChange={setFilter} />
    </section>
  );
}

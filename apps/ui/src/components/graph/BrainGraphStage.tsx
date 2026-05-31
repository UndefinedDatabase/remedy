import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { RemedyBrainFlow } from "./RemedyBrainFlow";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void }) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  return (
    <section className={styles.stage} aria-label="Growing brain graph" data-ui="brain-graph">
      <div className={styles.glassFog} aria-hidden="true" />
      <RemedyBrainFlow dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} filter={filter} />
      <GraphFilterChips value={filter} onChange={setFilter} />
    </section>
  );
}

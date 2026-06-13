import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { BrainGraphCanvas } from "./BrainGraphCanvas";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId?: string | null; onSelectNode: (nodeId: string | null) => void }) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  return (
    <section className={styles.stage} aria-label="Task brain graph" data-ui="brain-graph-stage">
      <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
      <div className={styles.chipsDock}>
        <GraphFilterChips value={filter} onChange={setFilter} />
      </div>
    </section>
  );
}

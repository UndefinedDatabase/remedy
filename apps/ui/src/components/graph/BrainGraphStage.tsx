import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { ForceBrainGraph } from "./ForceBrainGraph";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({ dashboard, onSelectNode }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string | null) => void }) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  return (
    <section className={styles.stage} aria-label="Growing brain graph" data-ui="brain-graph-stage">
      <div className={styles.haloA} aria-hidden="true" />
      <div className={styles.haloB} aria-hidden="true" />
      <ForceBrainGraph dashboard={dashboard} filter={filter} onSelectNode={onSelectNode} />
      <GraphFilterChips value={filter} onChange={setFilter} />
    </section>
  );
}

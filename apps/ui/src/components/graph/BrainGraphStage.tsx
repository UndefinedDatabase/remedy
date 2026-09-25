import { useMemo, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { rebuildBrainModel } from "./brainReducer";
import type { BrainEventRow } from "./brainOntology";
import { brainLedgerPrefix } from "./brainLedger";
import { useBrainLedger } from "./useBrainLedger";
import { buildBrainLayout } from "./buildForceBrainModel";
import { brainTaskCount, dashboardBrainSeeds, filterBrainLayout, selectedBrainNodeId, shellSelectionIdOf } from "./brainView";
import { ForceBrainGraph } from "./ForceBrainGraph";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { GraphLegend } from "./GraphLegend";
import { BrainGraphCanvas } from "./BrainGraphCanvas";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({
  dashboard,
  selectedNodeId,
  onSelectNode,
  recent,
  readEventsPage,
}: {
  dashboard: RemedyDashboard;
  selectedNodeId?: string | null;
  onSelectNode: (nodeId: string | null) => void;
  recent: readonly BrainEventRow[];
  readEventsPage: (cursor: number) => Promise<unknown>;
}) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  // Live is the default renderer (this round); Simple is the SVG picture
  // with prompt dots and keyboard focus (graph_spec.md §14; DECISION F019
  // D3) — the operator's choice; the stage also mounts it on its own
  // whenever no task is visible.
  const [view, setView] = useState<"live" | "simple">("live");

  const seeds = useMemo(() => dashboardBrainSeeds(dashboard.tasks), [dashboard.tasks]);
  const ledger = useBrainLedger(dashboard.jobId, recent, readEventsPage);
  // The graph folds only the COMPLETE, CONTIGUOUS prefix of the ledger: a
  // hole from a live gap, a mid-ledger join, or a sleeping tab holds the
  // model at the state before it, never a ghost past it (DECISION F019 D5).
  const rows = useMemo(() => brainLedgerPrefix(ledger), [ledger]);
  const layout = useMemo(
    () => buildBrainLayout(rebuildBrainModel(dashboard.jobId, seeds, rows)),
    [dashboard.jobId, seeds, rows],
  );
  const visible = useMemo(() => filterBrainLayout(layout, filter), [layout, filter]);
  const selectedId = selectedBrainNodeId(dashboard.tasks, selectedNodeId ?? null);
  const showLiveGraph = view === "live" && brainTaskCount(visible) > 0;

  return (
    <section className={styles.stage} aria-label="Task brain graph" data-ui="brain-graph-stage">
      {showLiveGraph ? (
        <ForceBrainGraph
          layout={visible}
          selectedId={selectedId}
          onSelectNode={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))}
        />
      ) : (
        // No tasks, an empty filter, or the operator pressed "Simple view":
        // BrainGraphCanvas owns its own empty and filter-empty messages.
        <BrainGraphCanvas dashboard={dashboard} filter={filter} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
      )}
      <div className={styles.chipsDock}>
        <GraphFilterChips value={filter} onChange={setFilter} />
      </div>
      <div className={styles.viewDock}>
        <GraphLegend />
        <button
          type="button"
          className={styles.viewToggle}
          aria-pressed={view === "simple"}
          onClick={() => setView(view === "live" ? "simple" : "live")}
        >
          {view === "live" ? "Simple view" : "Live view"}
        </button>
      </div>
    </section>
  );
}

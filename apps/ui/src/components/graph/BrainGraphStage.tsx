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
import { zoomBreadcrumbs, zoomGraphOf } from "./semanticZoom";
import { useSemanticZoom } from "./useSemanticZoom";
import { ZoomBreadcrumbs } from "./ZoomBreadcrumbs";
import { RunDetailPopover } from "./RunDetailPopover";
import { EvidencePanel } from "./EvidencePanel";
import { zoomCrumbLabel, zoomEmphasis } from "./zoomView";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({
  dashboard,
  selectedNodeId,
  onSelectNode,
  recent,
  readEventsPage,
  serverToken,
}: {
  dashboard: RemedyDashboard;
  selectedNodeId?: string | null;
  onSelectNode: (nodeId: string | null) => void;
  recent: readonly BrainEventRow[];
  readEventsPage: (cursor: number) => Promise<unknown>;
  serverToken: string;
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
  const model = useMemo(() => rebuildBrainModel(dashboard.jobId, seeds, rows), [dashboard.jobId, seeds, rows]);
  const layout = useMemo(() => buildBrainLayout(model), [model]);
  const visible = useMemo(() => filterBrainLayout(layout, filter), [layout, filter]);
  const selectedId = selectedBrainNodeId(dashboard.tasks, selectedNodeId ?? null);
  const showLiveGraph = view === "live" && brainTaskCount(visible) > 0;

  // Semantic zoom (graph_spec §10): focus is checked against the model, which
  // keeps every run, and the laid-out view, which adds the clusters
  // (DECISION F023 D1); what the state means on the canvas is zoomView.ts's.
  const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, layout.nodes), [model, layout]);
  const zoom = useSemanticZoom(zoomGraph);
  const emphasis = useMemo(() => zoomEmphasis(visible, zoom.state), [visible, zoom.state]);
  const crumbs = zoomBreadcrumbs(zoomGraph, zoom.state).map((c) => ({
    level: c.level, current: c.current, label: zoomCrumbLabel(c, layout),
  }));
  // L2's run detail and L3's evidence panel, for the focused run read from the
  // model, which keeps a run a cluster hides (DECISIONS F023 D4 and D5).
  const focusedRun = zoom.state.level >= 2 ? model.nodes.find((n) => n.id === zoom.state.focusId) ?? null : null;

  return (
    <section
      className={styles.stage}
      aria-label="Task brain graph"
      data-ui="brain-graph-stage"
      data-zoom-level={zoom.state.level}
      data-zoom-note={zoom.note ?? undefined}
    >
      {showLiveGraph ? (
        <>
          <ForceBrainGraph
            layout={visible}
            selectedId={selectedId}
            onSelectNode={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))}
            zoom={zoom.state}
            emphasis={emphasis}
            onZoomEvent={zoom.dispatch}
          />
          <ZoomBreadcrumbs items={crumbs} onJump={(level) => zoom.dispatch({ type: "crumb", level })} />
          {focusedRun && zoom.state.level === 2 && (
            <RunDetailPopover
              node={focusedRun}
              rows={rows}
              promptItems={dashboard.promptTrace?.items ?? []}
              jobId={dashboard.jobId}
              token={serverToken}
              onOpenEvidence={(tab) => zoom.dispatch({ type: "open_evidence", tab })}
              onClose={() => zoom.dispatch({ type: "escape" })}
            />
          )}
          {focusedRun && zoom.state.level === 3 && zoom.state.tab !== null && (
            <EvidencePanel
              node={focusedRun}
              tab={zoom.state.tab}
              rows={rows}
              promptItems={dashboard.promptTrace?.items ?? []}
              jobId={dashboard.jobId}
              token={serverToken}
              onTab={(tab) => zoom.dispatch({ type: "open_evidence", tab })}
              onClose={() => zoom.dispatch({ type: "escape" })}
            />
          )}
        </>
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

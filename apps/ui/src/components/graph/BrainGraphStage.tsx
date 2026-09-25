import { useMemo, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { rebuildBrainModel } from "./brainReducer";
import type { BrainEventRow } from "./brainOntology";
import { buildBrainLayout } from "./buildForceBrainModel";
import { brainTaskCount, dashboardBrainSeeds, filterBrainLayout, selectedBrainNodeId, shellSelectionIdOf } from "./brainView";
import { ForceBrainGraph } from "./ForceBrainGraph";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { GraphLegend } from "./GraphLegend";
import { BrainGraphCanvas } from "./BrainGraphCanvas";
import { zoomBreadcrumbs, zoomGraphOf } from "./semanticZoom";
import { useSemanticZoom } from "./useSemanticZoom";
import { useZoomDeepLink } from "./useZoomDeepLink";
import { ZoomBreadcrumbs } from "./ZoomBreadcrumbs";
import { RunDetailPopover } from "./RunDetailPopover";
import { EvidencePanel } from "./EvidencePanel";
import { zoomCrumbLabel, zoomEmphasis } from "./zoomView";
import { pauseBanner } from "../../api/pauseView";
import type { TimelineScrub } from "../timeline/useTimelineScrub";
import styles from "./BrainGraphStage.module.css";

export function BrainGraphStage({
  dashboard,
  selectedNodeId,
  onSelectNode,
  rows,
  scrub,
  serverToken,
}: {
  dashboard: RemedyDashboard;
  selectedNodeId?: string | null;
  onSelectNode: (nodeId: string | null) => void;
  rows: readonly BrainEventRow[];
  scrub: TimelineScrub;
  serverToken: string;
}) {
  const [filter, setFilter] = useState<GraphFilter>("all");
  // Live is the default renderer (this round); Simple is the SVG picture
  // with prompt dots and keyboard focus (graph_spec.md §14; DECISION F019
  // D3) — the operator's choice; the stage also mounts it on its own
  // whenever no task is visible.
  const [view, setView] = useState<"live" | "simple">("live");

  const seeds = useMemo(
    () => dashboardBrainSeeds(dashboard.tasks, dashboard.pause.pausedTaskIds),
    [dashboard.tasks, dashboard.pause.pausedTaskIds],
  );
  // `rows` is the ledger's COMPLETE, CONTIGUOUS prefix, read once by the shell for
  // the graph and the timeline alike: a hole holds the model at the state before
  // it, never a ghost past it (DECISIONS F019 D5 and F024 D4).
  const liveModel = useMemo(() => rebuildBrainModel(dashboard.jobId, seeds, rows), [dashboard.jobId, seeds, rows]);
  // While the timeline is scrubbed the stage draws the reducer state of the
  // prefix at the handle, and the live model waits behind LIVE (DECISION F024 D4).
  const model = scrub.scrubbedModel ?? liveModel;
  // Every cluster chip in place, whatever the focus: the graph the zoom checks
  // its focus against, so moving the focus never moves that graph.
  const baseLayout = useMemo(() => buildBrainLayout(model), [model]);

  // Semantic zoom (graph_spec §10): focus is checked against the model, which
  // keeps every run, and the laid-out view, which adds the clusters
  // (DECISION F023 D1); what the state means on the canvas is zoomView.ts's.
  // The URL's deep link restores it and then follows it (DECISION F023 D6).
  const zoomGraph = useMemo(() => zoomGraphOf(model.nodes, baseLayout.nodes), [model, baseLayout]);
  const zoom = useSemanticZoom(zoomGraph);
  useZoomDeepLink(zoomGraph, zoom.state, zoom.dispatch);
  const zoomCrumbs = zoomBreadcrumbs(zoomGraph, zoom.state);
  // The focused task's cluster chip gives way to its runs; unfocused, the
  // chip returns (DECISION F023 D6).
  const expandTaskId = zoomCrumbs.find((c) => c.level === 1)?.nodeId ?? null;
  const layout = useMemo(
    () => (expandTaskId === null ? baseLayout : buildBrainLayout(model, expandTaskId)),
    [baseLayout, model, expandTaskId],
  );
  const visible = useMemo(() => filterBrainLayout(layout, filter), [layout, filter]);
  const selectedId = selectedBrainNodeId(dashboard.tasks, selectedNodeId ?? null);
  const showLiveGraph = view === "live" && brainTaskCount(visible) > 0;
  const emphasis = useMemo(() => zoomEmphasis(visible, zoom.state), [visible, zoom.state]);
  const crumbs = zoomCrumbs.map((c) => ({
    level: c.level, current: c.current, label: zoomCrumbLabel(c, layout),
  }));
  // L2's run detail and L3's evidence panel, for the focused run read from the
  // model, which keeps a run a cluster hides (DECISIONS F023 D4 and D5).
  const focusedRun = zoom.state.level >= 2 ? model.nodes.find((n) => n.id === zoom.state.focusId) ?? null : null;
  // The pause banner (DECISION F025 D4), a pure read of the dashboard's own
  // pause state — no seam of its own, unlike the scrub banner above it.
  const banner = pauseBanner(dashboard);

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
      {scrub.state.mode === "scrubbed" && (
        <div className={styles.scrubBanner} role="status" data-ui="scrub-banner">
          <span className={styles.scrubBadge}>SCRUBBED</span>
          <span>{scrub.view.readout} · live updates wait behind LIVE</span>
          <button type="button" className={styles.scrubLive} onClick={scrub.goLive}>Back to LIVE</button>
        </div>
      )}
      {banner && (
        <div className={styles.pauseBanner} role="status" data-ui="pause-banner">
          <span className={styles.pauseBadge}>{banner.badge}</span>
          <span>{banner.text}</span>
          {banner.command !== "" && <code>{banner.command}</code>}
        </div>
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

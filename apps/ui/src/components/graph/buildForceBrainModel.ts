import type { RemedyDashboard } from "../../api/types";
import type { BrainNodeKind, BrainNodeState, ForceBrainGraphData, ForceBrainLink, ForceBrainNode } from "./forceBrainTypes";

type SizeClass = "small" | "medium" | "large";
type FilterMode = "all" | "open" | "planned" | "done";

function seededRng(seed: string) {
  let h = 0;
  for (let i = 0; i < seed.length; i++) { h = ((h << 5) - h + seed.charCodeAt(i)) | 0; }
  let s = h >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

const BRANCH_COLORS: string[] = ["#4c83ff", "#4cc681", "#a78bfa", "#67e8f9", "#91b8ff", "#5eead4"];

function particleCount(size: SizeClass): number {
  if (size === "small") return 4;
  if (size === "medium") return 8;
  return 14;
}

export function buildForceBrainModel(
  dashboard: RemedyDashboard,
  size: SizeClass = "medium",
  filter: FilterMode = "all",
): ForceBrainGraphData {
  const rng = seededRng(dashboard.jobId || "default");
  const nodes: ForceBrainNode[] = [];
  const links: ForceBrainLink[] = [];

  const root: ForceBrainNode = {
    id: "root", nodeId: dashboard.jobId, kind: "root", state: "current",
    label: "Project", sourceKind: "layout_only", depth: 0, value: 18, fx: 0, fy: 0,
    clickable: false, visibleLabel: false, alpha: 1, color: "#3478ff",
  };
  nodes.push(root);

  const realNodes = dashboard.graph.nodes.slice(0, 60);
  const branchCount = Math.max(3, Math.min(6, Math.ceil(realNodes.length / 4)));
  const baseLen = size === "small" ? 90 : size === "medium" ? 130 : 170;

  // Build organic branches radiating from root
  for (let b = 0; b < branchCount; b++) {
    const baseAngle = (b / branchCount) * Math.PI * 2 - Math.PI / 2 + (rng() - 0.5) * 0.4;
    const color = BRANCH_COLORS[b % BRANCH_COLORS.length];
    const armLen = baseLen + (rng() * 40 - 20);
    const segCount = 2 + Math.floor(rng() * 2);
    let prevId = "root";
    let cx = 0, cy = 0;

    for (let s = 0; s < segCount; s++) {
      const angle = baseAngle + (rng() - 0.5) * 0.6;
      const dist = armLen / segCount * (0.8 + rng() * 0.4);
      cx += Math.cos(angle) * dist;
      cy += Math.sin(angle) * dist;

      const branchId = `branch-${b}-${s}`;
      const branchNode: ForceBrainNode = {
        id: branchId, kind: "cluster", state: "planned", label: "",
        sourceKind: "layout_only", depth: 1, value: 4,
        fx: cx, fy: cy,
        clickable: false, visibleLabel: false, alpha: 0.3, color,
      };
      nodes.push(branchNode);
      links.push({
        source: prevId, target: branchId,
        strength: 0.6, curvature: 0.05 + rng() * 0.1, alpha: 0.25, width: 1.2 - s * 0.3,
      });
      prevId = branchId;
    }
  }

  // Distribute real nodes along branches
  const branchIds = nodes.filter(n => n.kind === "cluster").map(n => n.id);
  realNodes.forEach((gn, idx) => {
    const state: BrainNodeState = gn.state === "done" ? "done" : gn.state === "current" ? "current" : gn.state === "blocked" ? "blocked" : gn.state === "suggested" ? "suggested" : "planned";
    const kind: BrainNodeKind = gn.kind === "root" ? "task" : (gn.kind as BrainNodeKind) || "task";
    const branchTarget = branchIds[idx % branchIds.length];
    const anchor = nodes.find(n => n.id === branchTarget)!;
    const angle = rng() * Math.PI * 2;
    const dist = 15 + rng() * 35;

    const node: ForceBrainNode = {
      id: gn.id || `real-${idx}`, nodeId: gn.nodeId, kind, state, label: gn.label,
      sourceKind: "real_brain", clusterId: branchTarget, depth: 2, value: 5,
      x: (anchor.fx ?? 0) + Math.cos(angle) * dist,
      y: (anchor.fy ?? 0) + Math.sin(angle) * dist,
      clickable: true, visibleLabel: idx < 6, alpha: 0.85,
      color: anchor.color,
    };
    nodes.push(node);
    links.push({
      source: branchTarget, target: node.id, clusterId: branchTarget,
      strength: 0.4, curvature: 0.03 + rng() * 0.08, alpha: 0.2, width: 0.6,
    });
  });

  // Ambient particles — sparse, along branches.
  // Hard cap: total decorative (layout_only) nodes must never exceed 90; they
  // are purely visual, never interactive, never counted in any UI total.
  const LAYOUT_ONLY_CAP = 90;
  const pCount = particleCount(size);
  branchIds.forEach((bid) => {
    const anchor = nodes.find(n => n.id === bid)!;
    for (let p = 0; p < pCount; p++) {
      if (nodes.filter(n => n.sourceKind === "layout_only").length >= LAYOUT_ONLY_CAP) break;
      const angle = rng() * Math.PI * 2;
      const dist = 10 + rng() * 50;
      const pid = `${bid}-p${p}`;
      nodes.push({
        id: pid, kind: "particle", state: "planned", label: "",
        sourceKind: "layout_only", depth: 3, value: 1.5,
        x: (anchor.fx ?? 0) + Math.cos(angle) * dist,
        y: (anchor.fy ?? 0) + Math.sin(angle) * dist,
        clickable: false, visibleLabel: false,
        alpha: 0.12 + rng() * 0.2, color: anchor.color,
      });
      links.push({
        source: bid, target: pid, strength: 0.15,
        curvature: rng() * 0.15, alpha: 0.08, width: 0.3,
      });
    }
  });

  // Apply filter
  if (filter !== "all") {
    const allowedStates: BrainNodeState[] =
      filter === "done" ? ["done"] :
      filter === "open" ? ["current", "blocked"] :
      ["planned", "suggested"];
    nodes.forEach(n => {
      if (n.kind === "root" || n.kind === "cluster") return;
      if (!allowedStates.includes(n.state)) { n.alpha = 0.04; }
    });
    links.forEach(l => {
      const targetNode = typeof l.target === "string" ? nodes.find(n => n.id === l.target) : l.target;
      if (targetNode && (targetNode as ForceBrainNode).alpha < 0.1) { l.alpha = 0.02; }
    });
  }

  return { nodes, links };
}

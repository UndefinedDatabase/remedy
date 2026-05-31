import type { RemedyDashboard } from "../../api/types";
import type { BrainNodeKind, BrainNodeState, ForceBrainGraphData, ForceBrainLink, ForceBrainNode } from "./forceBrainTypes";

type SizeClass = "small" | "medium" | "large";
type FilterMode = "all" | "open" | "planned" | "done";

// Seeded PRNG (deterministic per jobId)
function seededRng(seed: string) {
  let h = 0;
  for (let i = 0; i < seed.length; i++) { h = ((h << 5) - h + seed.charCodeAt(i)) | 0; }
  let s = h >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

const CLUSTER_DEFS: { id: string; kind: BrainNodeKind; state: BrainNodeState; color: string; label: string }[] = [
  { id: "c-open", kind: "task", state: "current", color: "#4c83ff", label: "Active work" },
  { id: "c-planned", kind: "task", state: "planned", color: "#91b8ff", label: "Planned work" },
  { id: "c-done", kind: "proof", state: "done", color: "#4cc681", label: "Completed" },
  { id: "c-review", kind: "review", state: "suggested", color: "#a78bfa", label: "Review" },
  { id: "c-proof", kind: "proof", state: "done", color: "#67e8f9", label: "Verified" },
  { id: "c-memory", kind: "memory", state: "idle", color: "#5eead4", label: "Memory" },
  { id: "c-blocker", kind: "task", state: "blocked", color: "#fb923c", label: "Blockers" },
];

function particleCount(size: SizeClass): number {
  if (size === "small") return 12;
  if (size === "medium") return 28;
  return 48;
}

export function buildForceBrainModel(
  dashboard: RemedyDashboard,
  size: SizeClass = "medium",
  filter: FilterMode = "all",
): ForceBrainGraphData {
  const rng = seededRng(dashboard.jobId || "default");
  const nodes: ForceBrainNode[] = [];
  const links: ForceBrainLink[] = [];

  // Root node — fixed center
  const root: ForceBrainNode = {
    id: "root", nodeId: dashboard.jobId, kind: "root", state: "current",
    label: "Project", sourceKind: "layout_only", depth: 0, value: 28, fx: 0, fy: 0,
    clickable: false, visibleLabel: true, alpha: 1, color: "#3478ff",
  };
  nodes.push(root);

  // Cluster anchors — radially placed
  const clusterCount = CLUSTER_DEFS.length;
  const clusterAnchors: ForceBrainNode[] = [];
  const baseRadius = size === "small" ? 140 : size === "medium" ? 200 : 260;

  CLUSTER_DEFS.forEach((def, i) => {
    const angle = (i / clusterCount) * Math.PI * 2 - Math.PI / 2;
    const r = baseRadius + (rng() * 40 - 20);
    const anchor: ForceBrainNode = {
      id: def.id, kind: "cluster", state: def.state, label: def.label,
      sourceKind: "layout_only", clusterId: def.id, depth: 1, value: 14,
      fx: Math.cos(angle) * r, fy: Math.sin(angle) * r,
      clickable: false, visibleLabel: false, alpha: 0.7, color: def.color,
    };
    nodes.push(anchor);
    clusterAnchors.push(anchor);
    links.push({ source: "root", target: def.id, strength: 0.8, curvature: 0.1 + rng() * 0.15, alpha: 0.4, width: 1.5 });
  });

  // Assign real graph nodes to clusters
  const realNodes = dashboard.graph.nodes.slice(0, 80);
  realNodes.forEach((gn, idx) => {
    const state: BrainNodeState = gn.state === "done" ? "done" : gn.state === "current" ? "current" : gn.state === "blocked" ? "blocked" : gn.state === "suggested" ? "suggested" : "planned";
    const cluster = state === "done" ? "c-done" : state === "current" ? "c-open" : state === "blocked" ? "c-blocker" : state === "suggested" ? "c-review" : "c-planned";
    const clusterAnchor = clusterAnchors.find(a => a.id === cluster)!;
    const kind: BrainNodeKind = gn.kind === "root" ? "task" : (gn.kind as BrainNodeKind) || "task";
    const angle = rng() * Math.PI * 2;
    const dist = 30 + rng() * 60;

    const node: ForceBrainNode = {
      id: gn.id || `real-${idx}`, nodeId: gn.nodeId, kind, state, label: gn.label,
      sourceKind: "real_brain", clusterId: cluster, depth: 2, value: 6,
      x: (clusterAnchor.fx ?? 0) + Math.cos(angle) * dist,
      y: (clusterAnchor.fy ?? 0) + Math.sin(angle) * dist,
      clickable: true, visibleLabel: false, alpha: 0.9, color: clusterAnchor.color,
    };
    nodes.push(node);
    links.push({ source: cluster, target: node.id, clusterId: cluster, strength: 0.5, curvature: 0.05 + rng() * 0.2, alpha: 0.3, width: 0.8 });
  });

  // Particle nodes — fill for visual density
  const pCount = particleCount(size);
  CLUSTER_DEFS.forEach((def) => {
    const anchor = clusterAnchors.find(a => a.id === def.id)!;
    for (let p = 0; p < pCount; p++) {
      const angle = rng() * Math.PI * 2;
      const dist = 20 + rng() * 90;
      const particleId = `${def.id}-p${p}`;
      const particle: ForceBrainNode = {
        id: particleId, kind: "particle", state: def.state, label: "",
        sourceKind: "layout_only", clusterId: def.id, depth: 3, value: 2,
        x: (anchor.fx ?? 0) + Math.cos(angle) * dist,
        y: (anchor.fy ?? 0) + Math.sin(angle) * dist,
        clickable: false, visibleLabel: false,
        alpha: 0.2 + rng() * 0.4, color: def.color,
      };
      nodes.push(particle);
      links.push({ source: def.id, target: particleId, clusterId: def.id, strength: 0.2, curvature: rng() * 0.3, alpha: 0.15, width: 0.4 });
    }
  });

  // Cross-links between adjacent clusters
  for (let i = 0; i < clusterCount; i++) {
    const next = (i + 1) % clusterCount;
    links.push({
      source: CLUSTER_DEFS[i].id, target: CLUSTER_DEFS[next].id,
      strength: 0.15, curvature: 0.2 + rng() * 0.3, alpha: 0.12, width: 0.5,
    });
    if (rng() > 0.5) {
      const skip = (i + 2) % clusterCount;
      links.push({
        source: CLUSTER_DEFS[i].id, target: CLUSTER_DEFS[skip].id,
        strength: 0.08, curvature: 0.3 + rng() * 0.2, alpha: 0.08, width: 0.3,
      });
    }
  }

  // Apply filter
  if (filter !== "all") {
    const allowedStates: BrainNodeState[] =
      filter === "done" ? ["done"] :
      filter === "open" ? ["current", "blocked"] :
      ["planned", "suggested"];
    nodes.forEach(n => {
      if (n.kind === "root" || n.kind === "cluster") return;
      if (!allowedStates.includes(n.state)) { n.alpha = 0.05; }
    });
    links.forEach(l => {
      const targetNode = typeof l.target === "string" ? nodes.find(n => n.id === l.target) : l.target;
      if (targetNode && (targetNode as ForceBrainNode).alpha < 0.1) { l.alpha = 0.02; }
    });
  }

  return { nodes, links };
}

import type { Edge, Node } from "@xyflow/react";
import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";

function hash(input: string): number {
  let v = 2166136261;
  for (let i = 0; i < input.length; i++) {
    v ^= input.charCodeAt(i);
    v += (v << 1) + (v << 4) + (v << 7) + (v << 8) + (v << 24);
  }
  return Math.abs(v >>> 0);
}

function seededOffset(id: string, scale: number): number {
  return ((hash(id) % 1000) / 1000 - .5) * scale;
}

function stateToBranch(node: RemedyGraphNode, index: number): number {
  if (node.state === "done") return .34;
  if (node.state === "current") return -.1;
  if (node.state === "suggested") return .68;
  return index % 2 === 0 ? -.52 : .52;
}

export function buildReactFlowGraph(dashboard: RemedyDashboard): { nodes: Node[]; edges: Edge[] } {
  const meaningful = dashboard.graph.nodes.slice(0, 120);
  const root = meaningful[0];

  const nodes: Node[] = meaningful.map((node, i) => {
    if (i === 0) return { id: node.id, type: "root", position: { x: 0, y: 0 }, data: { ...node, zoomLabel: true }, draggable: false };
    const branch = stateToBranch(node, i);
    const radius = 160 + Math.floor(i / 8) * 74 + seededOffset(node.id, 40);
    const angle = branch * Math.PI + seededOffset(node.id + "angle", .42);
    const x = Math.cos(angle) * radius + seededOffset(node.id + "x", 90);
    const y = Math.sin(angle) * radius * .62 + seededOffset(node.id + "y", 120);
    return { id: node.id, type: i < 22 ? "work" : "tiny", position: { x, y }, data: { ...node, index: i }, draggable: false };
  });

  const edges: Edge[] = [];
  dashboard.graph.edges.forEach(e => {
    if (nodes.some(n => n.id === e.source) && nodes.some(n => n.id === e.target)) {
      edges.push({ id: e.id, source: e.source, target: e.target, type: "soft", data: { meaning: e.meaning, state: e.state } });
    }
  });

  if (root?.id) {
    nodes.slice(1, 80).forEach((n, i) => {
      if (edges.some(e => e.target === n.id)) return;
      const anchor = i < 12 ? root.id : nodes[Math.max(1, Math.floor(i / 2))]?.id || root.id;
      edges.push({ id: `organic-${anchor}-${n.id}`, source: anchor, target: n.id, type: "soft", data: { meaning: "branches to", state: n.data.state } });
    });
  }

  return { nodes, edges };
}

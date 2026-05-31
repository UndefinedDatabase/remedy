import { useMemo } from "react";
import { ReactFlow, type EdgeTypes, type NodeTypes, useEdgesState, useNodesState } from "@xyflow/react";
import type { RemedyDashboard } from "../../api/types";
import { buildReactFlowGraph } from "./organicLayout";
import { RootNode, HotspotNode } from "./GraphNodes";
import { SoftGlowEdge } from "./SoftGlowEdge";
import styles from "./RemedyBrainFlow.module.css";

const nodeTypes: NodeTypes = { root: RootNode, work: HotspotNode, tiny: HotspotNode };
const edgeTypes: EdgeTypes = { soft: SoftGlowEdge };

const reducedMotion = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function RemedyBrainFlow({ dashboard, onSelectNode, filter }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void; filter: "all" | "open" | "planned" | "done" }) {
  const graph = useMemo(() => {
    const built = buildReactFlowGraph(dashboard);
    if (filter === "all") return built;
    const allowed = new Set(built.nodes.filter(n => {
      const s = n.data?.state;
      if (filter === "done") return s === "done";
      if (filter === "open") return s === "current" || s === "blocked";
      if (filter === "planned") return s === "pending" || s === "suggested";
      return true;
    }).map(n => n.id));
    const root = built.nodes[0];
    if (root) allowed.add(root.id);
    return { nodes: built.nodes.filter(n => allowed.has(n.id)), edges: built.edges.filter(e => allowed.has(e.source) && allowed.has(e.target)) };
  }, [dashboard, filter]);

  const [nodes, , onNodesChange] = useNodesState(graph.nodes);
  const [edges, , onEdgesChange] = useEdgesState(graph.edges);

  return (
    <div className={`${styles.flowWrap} remedy-brain-canvas`} data-ui="react-flow">
      <ReactFlow
        nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
        fitView fitViewOptions={{ duration: reducedMotion ? 0 : 400 }} minZoom={.25} maxZoom={2.4} nodesDraggable={false} nodesConnectable={false}
        elementsSelectable panOnDrag zoomOnScroll
        proOptions={{ hideAttribution: true }}
        onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => onSelectNode(String(node.data?.nodeId || node.id))}
        className={styles.reactFlow}
      />
    </div>
  );
}

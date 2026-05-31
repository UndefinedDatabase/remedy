import { useMemo } from "react";
import { ReactFlow, Background, type EdgeTypes, type NodeTypes, useEdgesState, useNodesState } from "@xyflow/react";
import type { RemedyDashboard } from "../../api/types";
import { useReducedMotion } from "../shell/ReducedMotionProvider";
import { buildReactFlowGraph } from "./organicLayout";
import { RootNode, TinyNode, WorkNode } from "./GraphNodes";
import { SoftGlowEdge } from "./SoftGlowEdge";
import styles from "./RemedyBrainFlow.module.css";

const nodeTypes: NodeTypes = { root: RootNode, work: WorkNode, tiny: TinyNode };
const edgeTypes: EdgeTypes = { soft: SoftGlowEdge };

export function RemedyBrainFlow({ dashboard, onSelectNode, filter }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void; filter: "all" | "open" | "planned" | "done" }) {
  const reducedMotion = useReducedMotion();
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
      {!reducedMotion && <div className={styles.particleVeil} aria-hidden="true" />}
      <ReactFlow
        nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
        fitView minZoom={.25} maxZoom={2.4} nodesDraggable={false} nodesConnectable={false}
        elementsSelectable panOnDrag zoomOnScroll
        proOptions={{ hideAttribution: true }}
        onNodesChange={onNodesChange} onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => onSelectNode(String(node.data?.nodeId || node.id))}
        className={styles.reactFlow}
      >
        <Background color="rgba(95,132,190,.12)" gap={32} size={1} />
      </ReactFlow>
      <div className={styles.softCenterGlow} aria-hidden="true" />
    </div>
  );
}

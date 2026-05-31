export type BrainNodeKind = "root" | "cluster" | "task" | "proof" | "review" | "memory" | "particle";
export type BrainNodeState = "done" | "current" | "planned" | "blocked" | "suggested" | "idle";
export type BrainSourceKind = "real_brain" | "layout_only" | "demo_fixture";

export interface ForceBrainNode {
  id: string;
  nodeId?: string;
  kind: BrainNodeKind;
  state: BrainNodeState;
  label: string;
  sourceKind: BrainSourceKind;
  clusterId?: string;
  depth: number;
  value: number;
  fx?: number | null;
  fy?: number | null;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  clickable: boolean;
  visibleLabel: boolean;
  alpha: number;
  color: string;
}

export interface ForceBrainLink {
  source: string | ForceBrainNode;
  target: string | ForceBrainNode;
  clusterId?: string;
  strength: number;
  curvature: number;
  alpha: number;
  width: number;
}

export interface ForceBrainGraphData {
  nodes: ForceBrainNode[];
  links: ForceBrainLink[];
}

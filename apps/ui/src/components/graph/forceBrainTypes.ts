import type { NodeKind, NodeState } from "./brainOntology";

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

// --- buildBrainLayout's own shapes -------------------------------------------
// ForceBrainNode/Link above paint the polled-dashboard decorative graph;
// these paint the reducer's REAL model 1:1 (graph_spec §8 truth: every
// rendered real node maps 1:1 to a view-model entity, no decor node counted
// as one; DECISION F019 D1). Both live in this file because both are "the
// types the graph module hands its renderer."

/** One positioned real node — WHY a separate shape from ForceBrainNode: this
 *  one is a 1:1 projection of a BrainNode (graph_spec §4 sizes, §6 layout),
 *  never a decorative dot, so it carries no sourceKind/alpha/color at all. */
export interface BrainLayoutNode {
  id: string;
  kind: NodeKind;
  state: NodeState;
  parentId?: string;
  seq: number;
  depth: 0 | 1 | 2;
  radius: number;
  x: number;
  y: number;
  fx?: number;
  fy?: number;
  label: string;
}

/** One positioned parent edge — WHY it carries `depth`/`width`/`active`
 *  already resolved: the renderer paints trunk decay (§6) and particle flow
 *  (§7, §8) without re-deriving either from the node list on every frame. */
export interface BrainLayoutLink {
  id: string;
  source: string;
  target: string;
  depth: 1 | 2;
  width: number;
  active: boolean;
}

/** The whole positioned graph one buildBrainLayout call returns — WHY one
 *  value: brainMotion.ts diffs two of these, previous vs next, to find births. */
export interface BrainLayoutData {
  nodes: BrainLayoutNode[];
  links: BrainLayoutLink[];
}

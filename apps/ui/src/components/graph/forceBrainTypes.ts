import type { NodeKind, NodeState } from "./brainOntology";

// --- the graph module's own shapes -------------------------------------------
// These paint the reducer's REAL model 1:1 (graph_spec §8 truth: every
// rendered node maps 1:1 to a view-model entity, no decor node counted as
// one; DECISION F019 D1). They live in this file because they are "the types
// the graph module hands its renderer."

/** One positioned real node — a 1:1 projection of a BrainNode (graph_spec §4
 *  sizes, §6 layout); never a decorative dot, so it carries no color/alpha
 *  or any other paint-only field. */
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
  /** DECISION F026 D3 clause 2 — a task node's version chip text (`v<n>`),
   *  present ONLY when the task was edited at runtime. Absent otherwise. */
  chip?: string;
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

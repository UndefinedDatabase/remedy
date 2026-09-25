// The ONE state language for brain-graph nodes: for every node state, which
// token colours it, how large it is drawn, which marks it adds and whether it
// pulses. This module names tokens and never colour values; the renderer
// resolves each token once per mount, because a 2D canvas cannot read var()
// (tokens_rules.md). tests/ui_contracts/test_node_glyph_tokens.py checks that
// every token named here resolves, and that the four state colours T5_F020.md
// fixes are the values those tokens carry.
//
// Precedence, quoted verbatim from docs/ui/design_reference/assets_spec.md §4:
// "This is the codified form of `graph_spec.md` §5; on conflict, graph_spec §5
// + this table win over any feature-file prose."
//
// State is never carried by colour alone: failure adds a status dot and a veto
// adds a strike (graph_spec §5, §7), and planned nodes are smaller and ringed.
import type { NodeState } from "../brainOntology";
import type { StateMark } from "./glyphPaths";

/** A design token's name. The renderer resolves it; this module never holds
 *  the value. */
export type RemedyToken = `--remedy-${string}`;

/** In-progress pulse period, `--remedy-dur-pulse` (motion_spec.md "active
 *  pulse"); tests/ui_contracts/test_node_glyph_tokens.py pins it to the token. */
export const NODE_PULSE_MS = 1600;

/** In-progress pulse depth: ±8% scale (graph_spec §12 "Active pulse"). */
export const NODE_PULSE_AMPLITUDE = 0.08;

/** One mark a state adds, and the tokens that paint it. */
export interface StateMarkPaint {
  mark: StateMark;
  token: RemedyToken;
  outlineToken: RemedyToken | null;
}

/** How one state is drawn. `halo` is the soft ring at 35–40% alpha behind the
 *  node (graph_spec §5), or null where the state has none. `branchGlowAlpha`
 *  is the edge glow this state asks of its branch (graph_spec §7: on while
 *  active, 25% once done, off for planned and failed). `downstreamAlpha` dims
 *  what hangs below the node (graph_spec §7: 40% below a veto). */
export interface NodeStateTreatment {
  name: string;
  fillToken: RemedyToken;
  halo: { token: RemedyToken; alpha: number } | null;
  sizeFactor: number;
  marks: readonly StateMarkPaint[];
  pulse: boolean;
  branchGlowAlpha: number;
  downstreamAlpha: number;
}

/** One treatment per node state, in legend order. */
export const NODE_STATE_TREATMENTS: Readonly<Record<NodeState, NodeStateTreatment>> = {
  open: {
    name: "Suggested",
    fillToken: "--remedy-state-open",
    halo: { token: "--remedy-state-open", alpha: 0.4 },
    sizeFactor: 1,
    marks: [],
    pulse: false,
    branchGlowAlpha: 0,
    downstreamAlpha: 1,
  },
  planned: {
    name: "Planned",
    fillToken: "--remedy-state-planned",
    halo: null,
    sizeFactor: 0.9,
    marks: [{ mark: "ring", token: "--remedy-state-planned-ring", outlineToken: null }],
    pulse: false,
    branchGlowAlpha: 0,
    downstreamAlpha: 1,
  },
  in_progress: {
    name: "In progress",
    fillToken: "--remedy-state-current",
    halo: { token: "--remedy-state-current", alpha: 0.4 },
    sizeFactor: 1,
    marks: [],
    pulse: true,
    branchGlowAlpha: 1,
    downstreamAlpha: 1,
  },
  pass: {
    name: "Passed",
    fillToken: "--remedy-state-done",
    halo: { token: "--remedy-state-done", alpha: 0.35 },
    sizeFactor: 1,
    marks: [],
    pulse: false,
    branchGlowAlpha: 0.25,
    downstreamAlpha: 1,
  },
  fail: {
    name: "Failed",
    fillToken: "--remedy-state-blocked",
    halo: { token: "--remedy-state-blocked", alpha: 0.4 },
    sizeFactor: 1,
    marks: [{ mark: "status_dot", token: "--remedy-state-blocked", outlineToken: "--remedy-graph-node-ring" }],
    pulse: false,
    branchGlowAlpha: 0,
    downstreamAlpha: 1,
  },
  blocked: {
    name: "Blocked",
    fillToken: "--remedy-state-blocked",
    halo: { token: "--remedy-state-blocked", alpha: 0.4 },
    sizeFactor: 1,
    marks: [{ mark: "status_dot", token: "--remedy-state-blocked", outlineToken: "--remedy-graph-node-ring" }],
    pulse: false,
    branchGlowAlpha: 0,
    downstreamAlpha: 1,
  },
  vetoed: {
    name: "Vetoed",
    fillToken: "--remedy-state-vetoed",
    halo: { token: "--remedy-state-vetoed", alpha: 0.4 },
    sizeFactor: 1,
    marks: [{ mark: "strike", token: "--remedy-state-vetoed", outlineToken: "--remedy-graph-node-ring" }],
    pulse: false,
    branchGlowAlpha: 0,
    downstreamAlpha: 0.4,
  },
};

/** Every node state, in legend order — read from NODE_STATE_TREATMENTS
 *  itself, so a state removed there leaves every consumer of this list. */
export function nodeStateOrder(): NodeState[] {
  return Object.keys(NODE_STATE_TREATMENTS) as NodeState[];
}

/** Every token this module names, each once, in first-use order: the list
 *  the renderer resolves at mount. */
export function nodeStateTokens(): RemedyToken[] {
  const seen = new Set<RemedyToken>();
  for (const treatment of Object.values(NODE_STATE_TREATMENTS)) {
    seen.add(treatment.fillToken);
    if (treatment.halo) seen.add(treatment.halo.token);
    for (const paint of treatment.marks) {
      seen.add(paint.token);
      if (paint.outlineToken) seen.add(paint.outlineToken);
    }
  }
  return [...seen];
}

/** The scale factor a node of `state` is drawn at, `elapsedMs` into its
 *  pulse: the state's size factor, times a sine of ±NODE_PULSE_AMPLITUDE over
 *  NODE_PULSE_MS for a pulsing state. Reduced motion holds every node still
 *  at its size factor (graph_spec §12: "no pulse"). */
export function nodeScaleAt(state: NodeState, elapsedMs: number, reducedMotion: boolean): number {
  const treatment = NODE_STATE_TREATMENTS[state];
  if (!treatment.pulse || reducedMotion) return treatment.sizeFactor;
  const phase = (2 * Math.PI * elapsedMs) / NODE_PULSE_MS;
  return treatment.sizeFactor * (1 + NODE_PULSE_AMPLITUDE * Math.sin(phase));
}

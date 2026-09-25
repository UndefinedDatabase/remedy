// The conformance assertions over the matrix fixture: where, in the painted
// kind-by-state matrix, each discriminating detail must be — the status dot
// and its outline, the strike and its outline, the planned ring — and where
// the dot and the strike must NOT be, with the rule that judges one pixel
// (T5_F020.md, Acceptance: "Matrix fixture matches references (regions
// asserted)"; state is never colour alone). Pure: a harness paints
// glyphMatrix.ts on a real canvas, reads each probe's pixel and hands it to
// judgeProbe; the probes and the judge are unit-tested here without one.
import type { NodeKind, NodeState } from "../brainOntology";
import { glyphTransform } from "./glyphPaths";
import type { StateMark } from "./glyphPaths";
import { glyphMatrixCells } from "./glyphMatrix";
import { NODE_STATE_TREATMENTS } from "./nodeStates";
import type { RemedyToken } from "./nodeStates";
import type { BrainPalette } from "./palette";

/** Device pixels per world unit the harness paints the matrix at: wide enough
 *  that the thinnest probed stroke, a run's strike, spans several pixels. */
export const CONFORMANCE_SCALE = 8;

/** Largest per-channel difference, 0 to 255, at which a pixel still counts as
 *  a colour. Planned-ring blue and the veto's grey, the closest pair a probe
 *  must tell apart, differ by 41 in their blue channel. */
export const CONFORMANCE_TOLERANCE = 24;

/** Lowest alpha, 0 to 255, at which a pixel counts as painted at all. */
export const CONFORMANCE_MIN_ALPHA = 180;

/** Where, in a glyph's 24-unit box, each detail is probed: the centre of the
 *  status dot (centre 20,4.5, radius 3) and the middle of its outline band
 *  (radius 3 to 4.5); a point on the strike's line (x + y = 24) and the
 *  middle of its outline band beside it; and the top of the ring (radius 11). */
export const PROBE_POINTS: Readonly<Record<StateMark, { mark: [number, number]; outline: [number, number] | null }>> = {
  status_dot: { mark: [20, 4.5], outline: [20, 8.25] },
  strike: { mark: [6, 18], outline: [6.8, 18.8] },
  ring: { mark: [12, 1], outline: null },
  // The centre of the left bar (fill x 17-19, y 1.5-7.5), and a point on its
  // left edge's outline band (stroke centred at x 17, half-width 1.5) that
  // falls outside the fill.
  pause: { mark: [18, 4.5], outline: [16.3, 4.5] },
};

/** One pixel to read and what it must show. */
export interface ConformanceProbe {
  kind: NodeKind;
  state: NodeState;
  mark: StateMark;
  part: "mark" | "outline";
  expect: "present" | "absent";
  token: RemedyToken;
  x: number;
  y: number;
}

/** The binding spec's marks per state: the status dot on a failed or blocked
 *  node, the strike on a veto, the ring on a planned node, and none on any
 *  other (graph_spec.md §5 and §7, assets_spec.md §4, T5_F020.md). Written out
 *  here and NOT read from nodeStates.ts, so the harness judges the render
 *  against the spec rather than against the table the painter itself reads. */
export const BINDING_STATE_MARKS: Readonly<Record<NodeState, readonly StateMark[]>> = {
  open: [],
  planned: ["ring"],
  // DECISION F025 D3 clause 3: the planned ring PLUS the new pause mark. Keyed
  // here right after `planned`, matching `nodeStateOrder()`'s own order.
  paused: ["ring", "pause"],
  in_progress: [],
  pass: [],
  fail: ["status_dot"],
  blocked: ["status_dot"],
  vetoed: ["strike"],
};

/** The binding spec's colour for each mark and its outline: the dot in the
 *  failure red, the strike in the veto's grey, each outlined in the white node
 *  ring, and the ring in the planned ring's blue (DECISION F020 D1); the
 *  pause mark in the same orange the treatment paints it, also outlined in
 *  the white node ring (DECISION F025 D3 clause 3). */
export const BINDING_MARK_TOKENS: Readonly<Record<StateMark, { mark: RemedyToken; outline: RemedyToken | null }>> = {
  status_dot: { mark: "--remedy-state-blocked", outline: "--remedy-graph-node-ring" },
  strike: { mark: "--remedy-state-vetoed", outline: "--remedy-graph-node-ring" },
  ring: { mark: "--remedy-state-planned-ring", outline: null },
  pause: { mark: "--remedy-orange-400", outline: "--remedy-graph-node-ring" },
};

/** Every probe over the matrix, in device pixels at `scale`. A cell whose
 *  state the spec gives a mark is probed for the mark and for its outline; a
 *  cell whose state it does not is probed for the ABSENCE of the dot and of the
 *  strike. The ring is probed where present only: an in-progress halo seen
 *  through a planned ring's position is too close in colour to tell apart.
 *  Only the geometry comes from the painter's side: each cell's radius at its
 *  state's size factor, as the painter draws it. */
export function conformanceProbes(scale: number = CONFORMANCE_SCALE): ConformanceProbe[] {
  const probes: ConformanceProbe[] = [];
  for (const cell of glyphMatrixCells()) {
    const { kind, state } = cell.node;
    const t = glyphTransform(cell.node.x, cell.node.y, cell.node.radius * NODE_STATE_TREATMENTS[state].sizeFactor);
    const at = ([bx, by]: [number, number]) => ({ x: (t.offsetX + bx * t.scale) * scale, y: (t.offsetY + by * t.scale) * scale });
    for (const mark of Object.keys(PROBE_POINTS) as StateMark[]) {
      const points = PROBE_POINTS[mark];
      const tokens = BINDING_MARK_TOKENS[mark];
      if (BINDING_STATE_MARKS[state].includes(mark)) {
        probes.push({ kind, state, mark, part: "mark", expect: "present", token: tokens.mark, ...at(points.mark) });
        if (tokens.outline && points.outline) {
          probes.push({ kind, state, mark, part: "outline", expect: "present", token: tokens.outline, ...at(points.outline) });
        }
      } else if (mark !== "ring") {
        probes.push({ kind, state, mark, part: "mark", expect: "absent", token: tokens.mark, ...at(points.mark) });
      }
    }
  }
  return probes;
}

/** An 8-bit RGBA colour. */
export interface Rgba {
  r: number;
  g: number;
  b: number;
  a: number;
}

/** A resolved token value as RGBA, from three- or six-digit hex or from the
 *  rgb and rgba function notations; null for anything else, which the judge
 *  then fails. */
export function parseCssColour(value: string): Rgba | null {
  const v = value.trim().toLowerCase();
  const hex = /^#([0-9a-f]{3}|[0-9a-f]{6})$/.exec(v);
  if (hex) {
    const h = hex[1].length === 3 ? hex[1].split("").map((c) => c + c).join("") : hex[1];
    return { r: parseInt(h.slice(0, 2), 16), g: parseInt(h.slice(2, 4), 16), b: parseInt(h.slice(4, 6), 16), a: 255 };
  }
  const fn = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/.exec(v);
  if (fn) {
    const alpha = fn[4] === undefined ? 1 : Number(fn[4]);
    return { r: Number(fn[1]), g: Number(fn[2]), b: Number(fn[3]), a: Math.round(alpha * 255) };
  }
  return null;
}

/** Whether a painted pixel shows `colour`: painted (alpha at least
 *  CONFORMANCE_MIN_ALPHA) and within CONFORMANCE_TOLERANCE on every channel. */
export function pixelShows(pixel: Rgba, colour: Rgba): boolean {
  if (pixel.a < CONFORMANCE_MIN_ALPHA) return false;
  const d = Math.max(Math.abs(pixel.r - colour.r), Math.abs(pixel.g - colour.g), Math.abs(pixel.b - colour.b));
  return d <= CONFORMANCE_TOLERANCE;
}

/** One probe's verdict over the pixel the harness read for it. */
export function judgeProbe(probe: ConformanceProbe, pixel: Rgba, palette: BrainPalette): { ok: boolean; why: string } {
  const colour = parseCssColour(palette[probe.token] ?? "");
  if (colour === null) return { ok: false, why: `${probe.token} does not resolve to a colour` };
  const shows = pixelShows(pixel, colour);
  const ok = probe.expect === "present" ? shows : !shows;
  const seen = `[${pixel.r}, ${pixel.g}, ${pixel.b}, ${pixel.a}]`;
  return { ok, why: `${probe.expect} ${probe.token}: pixel ${seen}` };
}

// The graph legend's rows, enumerated from the two sources the canvas paints
// from, so the legend can never list a kind or a state the graph does not
// draw, or draw one differently (T5_F020.md, "the legend is generated from
// the same paths"; assets_spec.md §8 check 9, glyph parity). No row is
// written by hand: remove a kind from GLYPHS and the legend loses its row.
import type { NodeKind, NodeState } from "../brainOntology";
import { GLYPHS, STATE_MARK_PATHS } from "./glyphPaths";
import type { GlyphGeometry, StateMark } from "./glyphPaths";
import { NODE_STATE_TREATMENTS } from "./nodeStates";
import type { NodeStateTreatment, RemedyToken } from "./nodeStates";

/** One node kind as the legend shows it: its name and the very path strings
 *  the canvas builds its Path2D from. */
export interface LegendKindRow {
  kind: NodeKind;
  name: string;
  strokePath: string;
  fillPath: string;
}

/** One mark on a state's swatch, with the paths and tokens the canvas uses. */
export interface LegendMark {
  mark: StateMark;
  strokePath: string;
  fillPath: string;
  token: RemedyToken;
  outlineToken: RemedyToken | null;
}

/** One node state as the legend shows it: a swatch in the state's own fill,
 *  line and size, carrying the same marks the canvas draws. */
export interface LegendStateRow {
  state: NodeState;
  name: string;
  fillToken: RemedyToken;
  lineToken: RemedyToken;
  sizeFactor: number;
  marks: LegendMark[];
}

/** The kind rows, in the glyph module's own order. */
export function legendKindRows(glyphs: Readonly<Record<string, GlyphGeometry>> = GLYPHS): LegendKindRow[] {
  return Object.entries(glyphs).map(([kind, g]) => ({
    kind: kind as NodeKind, name: g.name, strokePath: g.strokePath, fillPath: g.fillPath,
  }));
}

/** The state rows, in the state module's own order. */
export function legendStateRows(
  treatments: Readonly<Record<string, NodeStateTreatment>> = NODE_STATE_TREATMENTS,
): LegendStateRow[] {
  return Object.entries(treatments).map(([state, t]) => ({
    state: state as NodeState,
    name: t.name,
    fillToken: t.fillToken,
    lineToken: t.lineToken,
    sizeFactor: t.sizeFactor,
    marks: t.marks.map((m) => ({
      mark: m.mark,
      strokePath: STATE_MARK_PATHS[m.mark].strokePath,
      fillPath: STATE_MARK_PATHS[m.mark].fillPath,
      token: m.token,
      outlineToken: m.outlineToken,
    })),
  }));
}

/** A token as a CSS value: the DOM legend paints through `var()`, which a
 *  canvas cannot, so it needs no palette bridge. */
export function tokenVar(token: RemedyToken): string {
  return `var(${token})`;
}

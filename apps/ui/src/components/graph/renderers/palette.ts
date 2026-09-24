// The palette bridge tokens_rules.md names: a 2D canvas cannot read var(), so
// the renderer resolves every token it paints with ONCE per mount, from the
// document's computed style, into this object. The token list comes from
// nodeStates.ts, so a token the state table names can never be missing here.
import { nodeStateTokens } from "./nodeStates";
import type { RemedyToken } from "./nodeStates";

/** The white that glosses every sphere and strokes a glyph drawn on one
 *  (graph_spec §5: "radial gradient white-highlight → state fill"). */
export const BRAIN_HIGHLIGHT_TOKEN: RemedyToken = "--remedy-graph-node-ring";

/** The font family a count is written in on the canvas (assets_spec.md §4:
 *  "cluster | circle + centered count text"), resolved like a colour because a
 *  canvas `font` cannot read var() either. */
export const BRAIN_LABEL_FONT_TOKEN: RemedyToken = "--remedy-font-ui";

/** Every token the brain graph's node painter reads, each once. */
export function brainPaletteTokens(): RemedyToken[] {
  return [...new Set<RemedyToken>([...nodeStateTokens(), BRAIN_HIGHLIGHT_TOKEN, BRAIN_LABEL_FONT_TOKEN])];
}

/** Resolved token values, keyed by token name. */
export type BrainPalette = Readonly<Record<RemedyToken, string>>;

/** The resolved palette, and every token that resolved to nothing. A missing
 *  token paints nothing rather than a guessed colour, and the renderer names
 *  it on its container so a test or a reviewer can see it. */
export interface ResolvedBrainPalette {
  palette: BrainPalette;
  missing: RemedyToken[];
}

/** Resolve every painter token through `read`, which returns a token's value
 *  or an empty string when the token is not declared. */
export function resolveBrainPalette(read: (token: RemedyToken) => string): ResolvedBrainPalette {
  const palette: Record<RemedyToken, string> = {};
  const missing: RemedyToken[] = [];
  for (const token of brainPaletteTokens()) {
    const value = read(token).trim();
    palette[token] = value;
    if (!value) missing.push(token);
  }
  return { palette, missing };
}

/** The palette as the document's stylesheet declares it right now. */
export function readDocumentPalette(): ResolvedBrainPalette {
  const style = getComputedStyle(document.documentElement);
  return resolveBrainPalette((token) => style.getPropertyValue(token));
}

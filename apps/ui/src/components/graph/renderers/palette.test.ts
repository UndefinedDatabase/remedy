import { describe, expect, it } from "vitest";
import { nodeStateTokens } from "./nodeStates";
import { BRAIN_HIGHLIGHT_TOKEN, BRAIN_LABEL_FONT_TOKEN, brainPaletteTokens, resolveBrainPalette } from "./palette";

describe("brainPaletteTokens", () => {
  it("covers every token the state table names, plus the highlight and the count's font, each once", () => {
    const tokens = brainPaletteTokens();
    expect(new Set(tokens).size).toBe(tokens.length);
    for (const token of nodeStateTokens()) expect(tokens).toContain(token);
    expect(tokens).toContain(BRAIN_HIGHLIGHT_TOKEN);
    expect(tokens).toContain(BRAIN_LABEL_FONT_TOKEN);
    expect(BRAIN_LABEL_FONT_TOKEN).toBe("--remedy-font-ui");
  });
});

describe("resolveBrainPalette", () => {
  it("resolves every token through the reader, trimmed", () => {
    const { palette, missing } = resolveBrainPalette((token) => `  value-of${token} `);
    expect(missing).toEqual([]);
    for (const token of brainPaletteTokens()) expect(palette[token]).toBe(`value-of${token}`);
  });

  it("names every token that resolves to nothing, and never invents a colour for it", () => {
    const { palette, missing } = resolveBrainPalette((token) => (token === "--remedy-state-vetoed" ? " " : "x"));
    expect(missing).toEqual(["--remedy-state-vetoed"]);
    expect(palette["--remedy-state-vetoed"]).toBe("");
  });
});

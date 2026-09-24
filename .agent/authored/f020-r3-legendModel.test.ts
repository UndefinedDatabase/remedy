import { describe, expect, it } from "vitest";
import { GLYPHS, STATE_MARK_PATHS, glyphKinds } from "./glyphPaths";
import { NODE_STATE_TREATMENTS, nodeStateOrder } from "./nodeStates";
import { legendKindRows, legendStateRows, tokenVar } from "./legendModel";

describe("legendKindRows", () => {
  it("lists every glyph kind, in the glyph module's order", () => {
    expect(legendKindRows().map((r) => r.kind)).toEqual(glyphKinds());
  });

  it("carries the very path strings and names the canvas paints from", () => {
    for (const row of legendKindRows()) {
      const glyph = GLYPHS[row.kind];
      expect(row.strokePath, row.kind).toBe(glyph.strokePath);
      expect(row.fillPath, row.kind).toBe(glyph.fillPath);
      expect(row.name, row.kind).toBe(glyph.name);
    }
  });

  it("loses a kind's row when the kind leaves the glyph module", () => {
    const { cluster: _dropped, ...withoutCluster } = GLYPHS;
    const kinds = legendKindRows(withoutCluster).map((r) => r.kind);
    expect(kinds).not.toContain("cluster");
    expect(kinds).toEqual(glyphKinds().filter((k) => k !== "cluster"));
  });
});

describe("legendStateRows", () => {
  it("lists every node state, in the state module's order", () => {
    expect(legendStateRows().map((r) => r.state)).toEqual(nodeStateOrder());
  });

  it("carries each state's fill, line, size and name as the canvas uses them", () => {
    for (const row of legendStateRows()) {
      const t = NODE_STATE_TREATMENTS[row.state];
      expect([row.name, row.fillToken, row.lineToken, row.sizeFactor], row.state)
        .toEqual([t.name, t.fillToken, t.lineToken, t.sizeFactor]);
    }
  });

  it("draws each state's marks from the canvas's own mark paths and tokens", () => {
    for (const row of legendStateRows()) {
      const t = NODE_STATE_TREATMENTS[row.state];
      expect(row.marks.map((m) => [m.mark, m.token, m.outlineToken]), row.state)
        .toEqual(t.marks.map((m) => [m.mark, m.token, m.outlineToken]));
      for (const m of row.marks) {
        expect([m.strokePath, m.fillPath], `${row.state}:${m.mark}`)
          .toEqual([STATE_MARK_PATHS[m.mark].strokePath, STATE_MARK_PATHS[m.mark].fillPath]);
      }
    }
  });

  it("loses a state's row when the state leaves the state module", () => {
    const { vetoed: _dropped, ...withoutVeto } = NODE_STATE_TREATMENTS;
    expect(legendStateRows(withoutVeto).map((r) => r.state)).toEqual(nodeStateOrder().filter((s) => s !== "vetoed"));
  });
});

describe("tokenVar", () => {
  it("writes a token as a CSS var() reference", () => {
    expect(tokenVar("--remedy-state-done")).toBe("var(--remedy-state-done)");
  });
});

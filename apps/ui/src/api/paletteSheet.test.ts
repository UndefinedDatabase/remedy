// F044 T001 — the bar's dropdown sheet, its pure rules (DECISION F044 D2).
import { describe, expect, it } from "vitest";
import type { JumpTarget } from "./paletteJump";
import {
  PALETTE_HELP_ROWS,
  PALETTE_RECENTS_KEY,
  PALETTE_RECENT_LIMIT,
  PALETTE_SECTION_ORDER,
  PROJECT_RESULT_LIMIT,
  buildPaletteRows,
  highlightPieces,
  movePaletteCursor,
  readPaletteRecents,
  rememberPaletteRef,
  writePaletteRecents,
} from "./paletteSheet";
import type { PaletteInput, PaletteRecentsStorage } from "./paletteSheet";

const TARGETS: JumpTarget[] = [
  { id: "t1", nodeId: "task:t1", label: "Fix error handling", kind: "task" },
  { id: "t2", nodeId: "task:t2", label: "Write tests", kind: "test" },
];

const PROJECTS = [
  { slug: "remedy", name: "Remedy" },
  { slug: "shop", name: "Shop front" },
  { slug: "docs", name: "Docs site" },
];

function input(over: Partial<PaletteInput>): PaletteInput {
  return { query: "", targets: TARGETS, projects: PROJECTS, activeSlug: "remedy", recents: [], ...over };
}

describe("the sheet's constants", () => {
  it("orders the sections, and bounds projects and recents", () => {
    expect(PALETTE_SECTION_ORDER).toEqual(["Recent", "Jump", "Projects", "Help"]);
    expect(PROJECT_RESULT_LIMIT).toBe(5);
    expect(PALETTE_RECENT_LIMIT).toBe(5);
    expect(PALETTE_RECENTS_KEY).toBe("remedy:palette-recent");
  });

  it("offers two help rows", () => {
    expect(PALETTE_HELP_ROWS.map((row) => [row.key, row.ref, row.section, row.label, row.hint, row.action])).toEqual([
      ["help:terms", "help:terms", "Help", "Show every term", "?", { kind: "terms" }],
      ["help:tour", "help:tour", "Help", "Take the tour", "Help", { kind: "tour" }],
    ]);
  });
});

describe("buildPaletteRows for a blank query", () => {
  it("lists every jump, every other project and both help rows, in section order", () => {
    const rows = buildPaletteRows(input({ query: "  " }));
    expect(rows.map((row) => [row.key, row.section, row.label, row.hint])).toEqual([
      ["jump:t1", "Jump", "Fix error handling", "task"],
      ["jump:t2", "Jump", "Write tests", "test"],
      ["project:docs", "Projects", "Docs site", "docs"],
      ["project:shop", "Projects", "Shop front", "shop"],
      ["help:terms", "Help", "Show every term", "?"],
      ["help:tour", "Help", "Take the tour", "Help"],
    ]);
    expect(rows[0].action).toEqual({ kind: "jump", nodeId: "task:t1" });
    expect(rows[2].action).toEqual({ kind: "project", slug: "docs" });
  });

  it("puts the remembered rows first, newest first, and drops a ref that reaches nothing", () => {
    const rows = buildPaletteRows(input({ recents: ["help:tour", "project:remedy", "jump:gone", "jump:t2"] }));
    expect(rows.slice(0, 2).map((row) => [row.key, row.ref, row.section, row.label])).toEqual([
      ["recent:help:tour", "help:tour", "Recent", "Take the tour"],
      ["recent:jump:t2", "jump:t2", "Recent", "Write tests"],
    ]);
    expect(rows[1].action).toEqual({ kind: "jump", nodeId: "task:t2" });
    expect(new Set(rows.map((row) => row.key)).size).toBe(rows.length);
  });

  it("lists no project row while there is only one project", () => {
    const rows = buildPaletteRows(input({ projects: [{ slug: "remedy", name: "Remedy" }] }));
    expect(rows.filter((row) => row.section === "Projects")).toEqual([]);
  });
});

describe("buildPaletteRows for a query", () => {
  it("ranks each section by the fuzzy rule and highlights what matched", () => {
    const rows = buildPaletteRows(input({ query: "s" }));
    expect(rows.map((row) => [row.key, row.ranges])).toEqual([
      ["jump:t2", []],
      ["jump:t1", []],
      ["project:shop", [[0, 1]]],
      ["project:docs", [[5, 6]]],
      ["help:terms", [[0, 1]]],
    ]);
    expect(buildPaletteRows(input({ query: "hand" })).map((row) => [row.key, row.ranges])).toEqual([
      ["jump:t1", [[10, 14]]],
    ]);
  });

  it("highlights nothing on a jump row whose id or kind matched rather than its label", () => {
    const rows = buildPaletteRows(input({ query: "t1" }));
    expect(rows.map((row) => [row.key, row.ranges])).toEqual([["jump:t1", []]]);
  });

  it("lists no recent row once there is a query", () => {
    const rows = buildPaletteRows(input({ query: "tour", recents: ["help:tour"] }));
    expect(rows.map((row) => row.key)).toEqual(["help:tour"]);
  });

  it("stops at the project limit", () => {
    const many = Array.from({ length: 8 }, (_, i) => ({ slug: `p${i}`, name: `Project ${i}` }));
    const rows = buildPaletteRows(input({ query: "project", projects: many, activeSlug: "p0" }));
    expect(rows.filter((row) => row.section === "Projects").map((row) => row.key)).toEqual([
      "project:p1", "project:p2", "project:p3", "project:p4", "project:p5",
    ]);
  });
});

describe("the remembered rows", () => {
  it("puts the chosen ref first, once, and keeps at most five", () => {
    expect(rememberPaletteRef(["a", "b", "c"], "b")).toEqual(["b", "a", "c"]);
    expect(rememberPaletteRef(["a", "b", "c", "d", "e"], "f")).toEqual(["f", "a", "b", "c", "d"]);
  });

  function memory(initial: string | null): PaletteRecentsStorage & { value: string | null } {
    const store = {
      value: initial,
      getItem: (key: string) => (key === PALETTE_RECENTS_KEY ? store.value : null),
      setItem: (key: string, value: string) => { if (key === PALETTE_RECENTS_KEY) store.value = value; },
    };
    return store;
  }

  const broken: PaletteRecentsStorage = {
    getItem: () => { throw new Error("storage is off"); },
    setItem: () => { throw new Error("storage is off"); },
  };

  it("reads the stored array's strings, at most five", () => {
    expect(readPaletteRecents(memory('["jump:t1", 3, "help:tour"]'))).toEqual(["jump:t1", "help:tour"]);
    expect(readPaletteRecents(memory('["a","b","c","d","e","f"]'))).toEqual(["a", "b", "c", "d", "e"]);
  });

  it("reads nothing stored, anything not an array, bad JSON and a broken storage as none", () => {
    expect(readPaletteRecents(memory(null))).toEqual([]);
    expect(readPaletteRecents(memory('{"a":1}'))).toEqual([]);
    expect(readPaletteRecents(memory("not json"))).toEqual([]);
    expect(readPaletteRecents(broken)).toEqual([]);
  });

  it("writes the refs as a JSON array, and survives a broken storage", () => {
    const store = memory(null);
    writePaletteRecents(store, ["help:tour", "jump:t1"]);
    expect(store.value).toBe('["help:tour","jump:t1"]');
    expect(() => writePaletteRecents(broken, ["x"])).not.toThrow();
  });
});

describe("movePaletteCursor", () => {
  it("answers -1 over no rows", () => {
    expect(movePaletteCursor(0, -1, 1)).toBe(-1);
    expect(movePaletteCursor(0, 3, -1)).toBe(-1);
  });

  it("enters at the first row going down and at the last going up", () => {
    expect(movePaletteCursor(3, -1, 1)).toBe(0);
    expect(movePaletteCursor(3, -1, -1)).toBe(2);
    expect(movePaletteCursor(3, 7, 1)).toBe(0);
  });

  it("steps and wraps", () => {
    expect(movePaletteCursor(3, 0, 1)).toBe(1);
    expect(movePaletteCursor(3, 2, 1)).toBe(0);
    expect(movePaletteCursor(3, 0, -1)).toBe(2);
  });
});

describe("highlightPieces", () => {
  it("cuts the label at the ranges", () => {
    expect(highlightPieces("Fix error handling", [[4, 7]])).toEqual([
      { text: "Fix ", hit: false },
      { text: "err", hit: true },
      { text: "or handling", hit: false },
    ]);
    expect(highlightPieces("abc", [[0, 1], [2, 3]])).toEqual([
      { text: "a", hit: true },
      { text: "b", hit: false },
      { text: "c", hit: true },
    ]);
  });

  it("answers the whole label for no range, and clips a range outside it", () => {
    expect(highlightPieces("abc", [])).toEqual([{ text: "abc", hit: false }]);
    expect(highlightPieces("abc", [[2, 9]])).toEqual([{ text: "ab", hit: false }, { text: "c", hit: true }]);
    expect(highlightPieces("", [[0, 1]])).toEqual([]);
  });
});

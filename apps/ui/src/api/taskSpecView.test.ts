import { describe, expect, it } from "vitest";
import { specVersionRows, versionChipLabel } from "./taskSpecView";
import type { RemedyTaskSpec, RemedyTaskSpecFields } from "./types";

function fields(overrides: Partial<RemedyTaskSpecFields> = {}): RemedyTaskSpecFields {
  return {
    title: "Build T1", goal: "goal of T1", acceptance: ["T1 works"],
    estTokensBand: "S", filesHint: ["src/t1.py"],
    ...overrides,
  };
}

function spec(overrides: Partial<RemedyTaskSpec> = {}): RemedyTaskSpec {
  return {
    plannedId: "T1",
    specVersion: 1,
    editState: "waiting",
    notEditableBecause: "",
    current: fields(),
    versions: [],
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// versionChipLabel
// ---------------------------------------------------------------------------

describe("versionChipLabel", () => {
  it("is null for spec version 1", () => {
    expect(versionChipLabel(spec({ specVersion: 1 }))).toBeNull();
  });

  it("is v2 for spec version 2", () => {
    expect(versionChipLabel(spec({ specVersion: 2 }))).toBe("v2");
  });

  it("is null for an undefined spec", () => {
    expect(versionChipLabel(undefined)).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// specVersionRows
// ---------------------------------------------------------------------------

describe("specVersionRows", () => {
  it("is empty for spec version 1", () => {
    expect(specVersionRows(spec({ specVersion: 1 }))).toEqual([]);
  });

  it("is empty for an undefined spec", () => {
    expect(specVersionRows(undefined)).toEqual([]);
  });

  it("one row per archived version, ascending, then the current row last", () => {
    const s = spec({
      specVersion: 3,
      current: fields({ title: "Build T1, v3" }),
      versions: [
        { ...fields({ title: "Build T1, v1" }), specVersion: 1, state: "waiting", archivedAt: "2026-01-01T00:00:00Z" },
        { ...fields({ title: "Build T1, v2" }), specVersion: 2, state: "waiting", archivedAt: "2026-01-02T00:00:00Z" },
      ],
    });

    const rows = specVersionRows(s);
    expect(rows).toHaveLength(3);
    expect(rows.map(r => r.specVersion)).toEqual([1, 2, 3]);
    expect(rows.map(r => r.current)).toEqual([false, false, true]);
    expect(rows[2].archivedAt).toBe("");
    expect(rows[2].state).toBe(s.editState);
  });

  it("the first row changed nothing", () => {
    const s = spec({
      specVersion: 2,
      current: fields({ title: "Build T1, renamed" }),
      versions: [
        { ...fields(), specVersion: 1, state: "waiting", archivedAt: "2026-01-01T00:00:00Z" },
      ],
    });
    const rows = specVersionRows(s);
    expect(rows[0].changes).toEqual([]);
  });

  it("reports every field that differs from the row before it", () => {
    const s = spec({
      specVersion: 2,
      current: {
        title: "Build T1, renamed",
        goal: "a new goal",
        acceptance: ["T1 works", "and is fast"],
        estTokensBand: "M",
        filesHint: ["src/t1.py", "src/t1_helpers.py"],
      },
      versions: [
        { ...fields(), specVersion: 1, state: "waiting", archivedAt: "2026-01-01T00:00:00Z" },
      ],
    });
    const rows = specVersionRows(s);
    const changes = rows[1].changes;
    expect(changes.map(c => c.field)).toEqual(["title", "goal", "acceptance", "estTokensBand", "filesHint"]);
    const acceptance = changes.find(c => c.field === "acceptance")!;
    expect(acceptance.before).toBe("T1 works");
    expect(acceptance.after).toBe("T1 works; and is fast");
    const files = changes.find(c => c.field === "filesHint")!;
    expect(files.before).toBe("src/t1.py");
    expect(files.after).toBe("src/t1.py; src/t1_helpers.py");
  });

  it("compares each row to the one before it, not to the first row", () => {
    const s = spec({
      specVersion: 3,
      // Same title as v2 — differs from v1, so a "compare to the first row"
      // bug would wrongly report a change here.
      current: fields({ title: "Build T1, v2" }),
      versions: [
        { ...fields({ title: "Build T1, v1" }), specVersion: 1, state: "waiting", archivedAt: "2026-01-01T00:00:00Z" },
        { ...fields({ title: "Build T1, v2" }), specVersion: 2, state: "waiting", archivedAt: "2026-01-02T00:00:00Z" },
      ],
    });
    const rows = specVersionRows(s);
    expect(rows[1].changes.map(c => c.field)).toEqual(["title"]);
    expect(rows[2].changes).toEqual([]);
  });

  it("reports no changes when nothing differs from the row before it", () => {
    const s = spec({
      specVersion: 2,
      current: fields(),
      versions: [
        { ...fields(), specVersion: 1, state: "waiting", archivedAt: "2026-01-01T00:00:00Z" },
      ],
    });
    const rows = specVersionRows(s);
    expect(rows[1].changes).toEqual([]);
  });
});

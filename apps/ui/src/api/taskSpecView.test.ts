import { describe, expect, it } from "vitest";
import { changedTaskFields, specVersionRows, taskEditAction, versionChipLabel } from "./taskSpecView";
import type { RemedyDashboard, RemedyTaskSpec, RemedyTaskSpecFields } from "./types";

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

// ---------------------------------------------------------------------------
// taskEditAction
// ---------------------------------------------------------------------------

function dashboardWithSpec(spec: RemedyTaskSpec | undefined): RemedyDashboard {
  return {
    taskSpecs: { tasks: spec ? { t1: spec } : {}, error: "" },
  } as RemedyDashboard;
}

describe("taskEditAction", () => {
  it.each(["waiting", "paused", "failed"] as const)(
    "an editState of %s answers the action",
    (editState) => {
      const dashboard = dashboardWithSpec(spec({ editState, specVersion: 3 }));
      const action = taskEditAction(dashboard, "t1");
      expect(action).toEqual({
        taskId: "t1",
        plannedId: "T1",
        specVersion: 3,
        editState,
        current: fields(),
      });
    },
  );

  it("is null for an editState of \"\"", () => {
    const dashboard = dashboardWithSpec(spec({ editState: "" }));
    expect(taskEditAction(dashboard, "t1")).toBeNull();
  });

  it("is null for a missing spec", () => {
    const dashboard = dashboardWithSpec(undefined);
    expect(taskEditAction(dashboard, "t1")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// changedTaskFields
// ---------------------------------------------------------------------------

describe("changedTaskFields", () => {
  function draft(overrides: Partial<{
    title: string; goal: string; band: string; acceptance: string; files: string;
  }> = {}) {
    return {
      title: "Build T1",
      goal: "goal of T1",
      band: "S",
      acceptance: "T1 works",
      files: "src/t1.py",
      ...overrides,
    };
  }

  it("is {} for an unchanged draft", () => {
    expect(changedTaskFields(fields(), draft())).toEqual({});
  });

  it("carries only title when title alone changed", () => {
    expect(changedTaskFields(fields(), draft({ title: "Renamed" })))
      .toEqual({ title: "Renamed" });
  });

  it("carries only goal when goal alone changed", () => {
    expect(changedTaskFields(fields(), draft({ goal: "new goal" })))
      .toEqual({ goal: "new goal" });
  });

  it("carries only acceptance when acceptance alone changed", () => {
    expect(changedTaskFields(fields(), draft({ acceptance: "a\nb" })))
      .toEqual({ acceptance: ["a", "b"] });
  });

  it("carries only est_tokens_band when band alone changed", () => {
    expect(changedTaskFields(fields(), draft({ band: "L" })))
      .toEqual({ est_tokens_band: "L" });
  });

  it("carries only files_hint when files alone changed", () => {
    expect(changedTaskFields(fields(), draft({ files: "a.py\nb.py" })))
      .toEqual({ files_hint: ["a.py", "b.py"] });
  });

  it("trims each line and drops blank lines for acceptance", () => {
    expect(changedTaskFields(
      fields({ acceptance: ["a", "b"] }),
      draft({ acceptance: "  a  \n\nb\n  \n" }),
    )).toEqual({});
  });

  it("trims each line and drops blank lines for files", () => {
    expect(changedTaskFields(
      fields({ filesHint: ["a.py", "b.py"] }),
      draft({ files: "  a.py \n\n b.py\n\n" }),
    )).toEqual({});
  });

  it("a real change survives the trim", () => {
    expect(changedTaskFields(
      fields({ acceptance: ["a"] }),
      draft({ acceptance: "  a  \n\n  c  \n" }),
    )).toEqual({ acceptance: ["a", "c"] });
  });
});

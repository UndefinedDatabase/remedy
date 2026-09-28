import { describe, it, expect } from "vitest";
import {
  OWNERSHIP_CHIP_WORDS,
  OWNERSHIP_EMPTY_LINE,
  OWNERSHIP_REFRESH_EVENTS,
  OWNERSHIP_UNREADABLE_LINE,
  decodeOwnershipView,
  ownershipChipWord,
  ownershipEntriesForTask,
  ownershipPanelState,
  ownershipRefreshKey,
  ownershipViewPath,
} from "./ownership";
import { loadOwnershipView } from "./remedyApi";

function entry(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    record_ref: "veto:1",
    ts: "2026-09-28T00:00:00+00:00",
    actor: { kind: "operator", door: "cli", recorded_as: "cli", token_number: 0, auto_approved: false },
    action: "task_vetoed",
    task_id: "T1",
    text: "known-bad approach",
    consequence: { kind: "unreachable", task_ids: ["T2", "T3"], ref: "" },
    detail: { status_at_veto: "planned" },
    sentence: "You (command line) vetoed task T1.",
    ...overrides,
  };
}

const VIEW = { schema: "remedy.ownership.v1", job_id: "job-1", entries: [entry()], error: "" };

describe("decodeOwnershipView", () => {
  it("reads a wire-shaped view", () => {
    const view = decodeOwnershipView(VIEW);
    expect(view?.jobId).toBe("job-1");
    expect(view?.error).toBe("");
    expect(view?.entries).toEqual([{
      recordRef: "veto:1", ts: "2026-09-28T00:00:00+00:00",
      actor: { kind: "operator", door: "cli", recordedAs: "cli", tokenNumber: 0, autoApproved: false },
      action: "task_vetoed", taskId: "T1", text: "known-bad approach",
      consequence: { kind: "unreachable", taskIds: ["T2", "T3"], ref: "" },
      sentence: "You (command line) vetoed task T1.",
    }]);
  });

  it.each([
    ["no object", null],
    ["a list", []],
    ["the wrong schema", { ...VIEW, schema: "remedy.ownership.v2" }],
    ["entries that are not a list", { ...VIEW, entries: {} }],
    ["an error that is not a string", { ...VIEW, error: null }],
    ["an entry that is not an object", { ...VIEW, entries: [3] }],
    ["an entry with no record_ref", { ...VIEW, entries: [entry({ record_ref: undefined })] }],
    ["an entry whose actor is not an object", { ...VIEW, entries: [entry({ actor: "cli" })] }],
    ["an actor with a non-number token_number", { ...VIEW,
      entries: [entry({ actor: { kind: "operator", door: "cli", recorded_as: "cli",
        token_number: "1", auto_approved: false } })] }],
    ["an actor with a non-boolean auto_approved", { ...VIEW,
      entries: [entry({ actor: { kind: "operator", door: "cli", recorded_as: "cli",
        token_number: 0, auto_approved: "yes" } })] }],
    ["a consequence that is not an object", { ...VIEW, entries: [entry({ consequence: "x" })] }],
    ["a consequence whose task_ids is not a list", { ...VIEW,
      entries: [entry({ consequence: { kind: "unreachable", task_ids: "T2", ref: "" } })] }],
    ["a consequence whose task_ids holds a non-string", { ...VIEW,
      entries: [entry({ consequence: { kind: "unreachable", task_ids: [3], ref: "" } })] }],
    ["a sentence that is not a string", { ...VIEW, entries: [entry({ sentence: 7 })] }],
  ])("refuses the whole view for %s", (_label, raw) => {
    expect(decodeOwnershipView(raw)).toBeNull();
  });
});

describe("the section's rules", () => {
  it("builds the route with the job id and token encoded", () => {
    expect(ownershipViewPath({ jobId: "a/b", token: "t&k" }))
      .toBe("/api/jobs/a%2Fb/ownership?token=t%26k");
  });

  it("answers the entries for a task by its own id and by a consequence, in order, none for \"\"", () => {
    const view = decodeOwnershipView({
      schema: "remedy.ownership.v1", job_id: "job-1", error: "",
      entries: [
        entry({ record_ref: "a", task_id: "T1", consequence: { kind: "", task_ids: [], ref: "" } }),
        entry({ record_ref: "b", task_id: "T9", consequence: { kind: "unreachable", task_ids: ["T1"], ref: "" } }),
        entry({ record_ref: "c", task_id: "T2", consequence: { kind: "", task_ids: [], ref: "" } }),
      ],
    })!;
    expect(ownershipEntriesForTask(view, "T1").map((e) => e.recordRef)).toEqual(["a", "b"]);
    expect(ownershipEntriesForTask(view, "T2").map((e) => e.recordRef)).toEqual(["c"]);
    expect(ownershipEntriesForTask(view, "")).toEqual([]);
  });

  it("labels every chip word and falls back for an unknown action", () => {
    for (const [action, word] of Object.entries(OWNERSHIP_CHIP_WORDS)) {
      expect(ownershipChipWord(action)).toBe(word);
    }
    expect(ownershipChipWord("teleported_the_task")).toBe("Action");
  });

  it("reads the refresh key over mixed frames", () => {
    expect(ownershipRefreshKey([])).toBe(0);
    expect(ownershipRefreshKey([
      { seq: 4, kind: OWNERSHIP_REFRESH_EVENTS[0] },
      { seq: 9, kind: "task_run_completed" },
      { seq: 7, kind: OWNERSHIP_REFRESH_EVENTS[1] },
    ])).toBe(7);
  });

  it("names the unreadable line", () => {
    expect(OWNERSHIP_UNREADABLE_LINE).toBe("Who did what could not be read for this job.");
  });
});

describe("ownershipPanelState", () => {
  const readableView = decodeOwnershipView(VIEW)!;
  const emptyView = decodeOwnershipView({ ...VIEW, entries: [] })!;
  const erroredView = decodeOwnershipView({ ...VIEW, entries: [], error: "boom" })!;

  it("reads loading while not loaded, whatever the view", () => {
    expect(ownershipPanelState(null, false)).toEqual({ kind: "loading" });
    expect(ownershipPanelState(readableView, false)).toEqual({ kind: "loading" });
  });

  it("reads unreadable for a loaded null view", () => {
    expect(ownershipPanelState(null, true)).toEqual({ kind: "unreadable", line: OWNERSHIP_UNREADABLE_LINE });
  });

  it("reads unreadable for a loaded view whose error is not \"\"", () => {
    expect(ownershipPanelState(erroredView, true)).toEqual({ kind: "unreadable", line: OWNERSHIP_UNREADABLE_LINE });
  });

  it("reads empty for a loaded, readable view with no entry", () => {
    expect(ownershipPanelState(emptyView, true)).toEqual({ kind: "empty", line: OWNERSHIP_EMPTY_LINE });
  });

  it("reads entries, in the view's own order, for a loaded readable view with entries", () => {
    expect(ownershipPanelState(readableView, true)).toEqual({ kind: "entries", entries: readableView.entries });
  });
});

describe("loadOwnershipView", () => {
  it("reads the route through the injected fetcher", async () => {
    const asked: string[] = [];
    const view = await loadOwnershipView({ jobId: "j1", token: "tok" }, async (path) => {
      asked.push(path);
      return VIEW;
    });
    expect(asked).toEqual(["/api/jobs/j1/ownership?token=tok"]);
    expect(view?.entries.length).toBe(1);
  });

  it("answers null, never throws, when the read fails", async () => {
    const view = await loadOwnershipView({ jobId: "j1", token: "tok" }, async () => {
      throw new Error("offline");
    });
    expect(view).toBeNull();
  });
});

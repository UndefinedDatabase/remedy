// T5_F292 T003 — the rules of the hunk controls (DECISION F292 D6).
import { describe, expect, it } from "vitest";
import type { DiffEnvelope } from "./diffViewModel";
import type { HunkDecisions } from "./hunkDecisions";
import {
  decidableHunkIds,
  hunkControlsBlocked,
  hunkDecisionArgs,
  hunkDraftChanged,
  hunkDraftOf,
  hunkIsDecidable,
  hunkTally,
} from "./hunkDecisionView";

function envelope(files: string[][], overrides: Partial<DiffEnvelope> = {}): DiffEnvelope {
  return {
    version: 1, scope: "job", taskId: "", source: "workspace.diff", available: true, reason: null,
    truncated: false, taskRunIds: [],
    files: files.map((ids, n) => ({
      path: `f${n}.txt`, oldPath: null, status: "modified", stats: { added: 1, deleted: 1 }, note: null,
      hunks: ids.map((id) => ({ id, header: "@@ -1 +1 @@", oldStart: 1, newStart: 1, lines: [] })),
    })),
    ...overrides,
  };
}

const ENV = envelope([["h1", "h2"], ["unidentified:file1:hunk0", "h3"]]);

function recorded(rows: [string, "approved" | "rejected" | "pending", string][]): HunkDecisions {
  return { attemptKey: "job:workspace.diff", decidedAt: "2026-10-01T09:00:00+00:00",
    hunks: rows.map(([id, state, reason]) => ({ id, state, reason })) };
}

const NOTHING: HunkDecisions = { attemptKey: "", decidedAt: "", hunks: [] };

describe("hunkControlsBlocked and hunkIsDecidable", () => {
  it("lets an available whole diff be decided", () => {
    expect(hunkControlsBlocked(ENV)).toBeNull();
  });
  it("says why an absent or cut-short diff cannot be decided", () => {
    expect(hunkControlsBlocked(envelope([], { available: false }))).toBe("No change is available to decide.");
    expect(hunkControlsBlocked(envelope([["h1"]], { truncated: true }))).toBe(
      "This change was cut short, so not every hunk can be named; it cannot be decided hunk by hunk.");
  });
  it("never offers a hunk the server sent no id for", () => {
    expect(hunkIsDecidable("h1")).toBe(true);
    expect(hunkIsDecidable("unidentified:file0:hunk0")).toBe(false);
    expect(decidableHunkIds(ENV)).toEqual(["h1", "h2", "h3"]);
  });
});

describe("hunkDraftOf and hunkDraftChanged", () => {
  it("starts every decidable hunk from its record, or pending", () => {
    expect(hunkDraftOf(ENV, recorded([["h2", "rejected", "too broad"], ["h1", "approved", ""]]))).toEqual({
      h1: { state: "approved", reason: "" }, h2: { state: "rejected", reason: "too broad" },
      h3: { state: "pending", reason: "" },
    });
  });
  it("leaves out a recorded hunk this diff does not show", () => {
    expect(Object.keys(hunkDraftOf(ENV, recorded([["gone", "approved", ""]])))).toEqual(["h1", "h2", "h3"]);
  });
  it("sees a changed state or a changed reason of a rejection, and nothing else", () => {
    const start = recorded([["h1", "rejected", "too broad"]]);
    const draft = hunkDraftOf(ENV, start);
    expect(hunkDraftChanged(ENV, start, draft)).toBe(false);
    expect(hunkDraftChanged(ENV, start, { ...draft, h1: { state: "rejected", reason: " too broad " } })).toBe(false);
    expect(hunkDraftChanged(ENV, start, { ...draft, h1: { state: "rejected", reason: "wrong file" } })).toBe(true);
    expect(hunkDraftChanged(ENV, start, { ...draft, h2: { state: "approved", reason: "" } })).toBe(true);
    expect(hunkDraftChanged(ENV, NOTHING, { ...hunkDraftOf(ENV, NOTHING), h3: { state: "pending", reason: "x" } })).toBe(false);
  });
});

describe("hunkDecisionArgs", () => {
  it("records the approved and rejected hunks in the diff's order, the reasons trimmed", () => {
    const draft = { h3: { state: "approved" as const, reason: "" }, h1: { state: "approved" as const, reason: "" },
      h2: { state: "rejected" as const, reason: "  too broad " } };
    expect(hunkDecisionArgs(ENV, draft)).toEqual({ args: {
      approved: ["h1", "h3"], rejected: [{ id: "h2", reason: "too broad" }] } });
  });
  it("names the task run for a task run's diff, and none for the job's own", () => {
    const draft = { h1: { state: "approved" as const, reason: "" } };
    expect(hunkDecisionArgs({ ...ENV, taskId: "T001" }, draft)).toEqual(
      { args: { approved: ["h1"], rejected: [], task_run: "T001" } });
    expect("task_run" in (hunkDecisionArgs(ENV, draft) as { args: object }).args).toBe(false);
  });
  it("refuses a decision that decides nothing", () => {
    expect(hunkDecisionArgs(ENV, hunkDraftOf(ENV, NOTHING))).toEqual({ problem: "Decide at least one hunk before recording." });
  });
  it("refuses a rejection without a reason", () => {
    expect(hunkDecisionArgs(ENV, { h1: { state: "rejected", reason: "  " } })).toEqual(
      { problem: "Give each rejected hunk a reason." });
  });
});

describe("hunkTally", () => {
  it("counts the decidable hunks by state", () => {
    expect(hunkTally(ENV, { h1: { state: "approved", reason: "" }, h2: { state: "rejected", reason: "x" },
      h3: { state: "pending", reason: "" } })).toBe("1 approved, 1 rejected, 1 pending");
  });
});

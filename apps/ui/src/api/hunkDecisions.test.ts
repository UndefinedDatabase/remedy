// T5_F292 T003 — the recorded hunk decision's path and decoder (DECISION F292 D6).
import { describe, expect, it } from "vitest";
import { HUNK_STATES, NO_HUNK_DECISIONS, hunkDecisionsPath, readHunkDecisions } from "./hunkDecisions";

describe("hunkDecisionsPath", () => {
  it("names the job's own diff when the task is blank, and the task run's otherwise", () => {
    expect(hunkDecisionsPath("0123456789abcdef", "t k", "")).toBe("/api/jobs/0123456789abcdef/hunk-decisions?token=t%20k");
    expect(hunkDecisionsPath("0123456789abcdef", "tok", "  ")).toBe("/api/jobs/0123456789abcdef/hunk-decisions?token=tok");
    expect(hunkDecisionsPath("0123456789abcdef", "tok", "T001")).toBe(
      "/api/jobs/0123456789abcdef/task-runs/T001/hunk-decisions?token=tok");
  });
  it("encodes the job and the task run", () => {
    expect(hunkDecisionsPath("a/b", "tok", "c d")).toBe("/api/jobs/a%2Fb/task-runs/c%20d/hunk-decisions?token=tok");
  });
});

describe("readHunkDecisions", () => {
  it("reads every field the route serves, rows in order", () => {
    expect(readHunkDecisions({
      attempt_key: "job:workspace.diff", decided_at: "2026-10-01T09:00:00+00:00",
      hunks: [{ id: "h1", state: "approved", reason: "" }, { id: "h2", state: "rejected", reason: "too broad" },
        { id: "h3", state: "pending", reason: "" }],
    })).toEqual({
      attemptKey: "job:workspace.diff", decidedAt: "2026-10-01T09:00:00+00:00",
      hunks: [{ id: "h1", state: "approved", reason: "" }, { id: "h2", state: "rejected", reason: "too broad" },
        { id: "h3", state: "pending", reason: "" }],
    });
  });
  it("drops a row without a text id or with an unknown state, and reads a missing reason as empty", () => {
    expect(readHunkDecisions({ attempt_key: "k", decided_at: "", hunks: [
      null, "x", { id: 3, state: "approved" }, { id: "h1", state: "landed" }, { id: "h2", state: "rejected" }] }).hunks)
      .toEqual([{ id: "h2", state: "rejected", reason: "" }]);
  });
  it.each([null, undefined, "x", 3, []])("reads %j as nothing recorded", (raw) => {
    expect(readHunkDecisions(raw)).toEqual(NO_HUNK_DECISIONS);
  });
  it("reads fields of the wrong type as empty", () => {
    expect(readHunkDecisions({ attempt_key: 1, decided_at: null, hunks: "x" })).toEqual(NO_HUNK_DECISIONS);
  });
  it("names the three states the ledger writes", () => {
    expect(HUNK_STATES).toEqual(["approved", "rejected", "pending"]);
  });
});

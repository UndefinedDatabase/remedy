// T5_F292 T001 — the plan view's rules (DECISION F292 D2).
import { describe, expect, it } from "vitest";
import {
  PLAN_ABSENT_TEXT,
  PLAN_UNREADABLE_TEXT,
  planApprovalText,
  planBody,
  planDependencyText,
  planEntryText,
  planHeadline,
  planWindowText,
} from "./planView";
import type { RemedyPlan, RemedyPlanTask } from "./types";

function task(overrides: Partial<RemedyPlanTask> = {}): RemedyPlanTask {
  return {
    id: "T1", title: "Build T1", goal: "goal of T1", dependsOn: [], estTokensBand: "S",
    filesHint: [], acceptance: ["T1 works"], jobTaskId: "entry-1", status: "pending",
    specVersion: 1, ...overrides,
  };
}

function plan(overrides: Partial<RemedyPlan> = {}): RemedyPlan {
  return {
    available: true, version: 2, approval: "pending", editable: true, notEditableBecause: "",
    tasks: [task()], error: "", ...overrides,
  };
}

describe("planBody", () => {
  it("is the plan when one is available and nothing failed", () => {
    expect(planBody(plan())).toBe("ready");
  });
  it("is absent when the job has no stored plan", () => {
    expect(planBody(plan({ available: false, tasks: [] }))).toBe("absent");
  });
  it("is unreadable when the section's read failed, whatever else it says", () => {
    expect(planBody(plan({ available: false, error: "bad version" }))).toBe("unreadable");
    expect(planBody(plan({ error: "bad version" }))).toBe("unreadable");
  });
  it("names its two quiet lines", () => {
    expect(PLAN_ABSENT_TEXT).toBe("This job has no stored plan yet.");
    expect(PLAN_UNREADABLE_TEXT).toBe("This job's plan could not be read.");
  });
});

describe("planApprovalText and planHeadline", () => {
  it.each([
    ["pending", "waiting for approval"],
    ["approved", "approved"],
    ["rejected", "rejected"],
    ["", "no approval recorded"],
    ["held", "held"],
    ["toString", "toString"],
  ])("the approval %j reads %j", (approval, text) => {
    expect(planApprovalText(approval)).toBe(text);
  });
  it("puts the version before the approval", () => {
    expect(planHeadline(plan())).toBe("Version 2 · waiting for approval");
    expect(planHeadline(plan({ version: 5, approval: "approved" }))).toBe("Version 5 · approved");
  });
});

describe("planWindowText", () => {
  it("says an editable plan is open", () => {
    expect(planWindowText(plan())).toBe("Open for editing while its approval is open.");
  });
  it("carries the server's reason when the plan is closed", () => {
    expect(planWindowText(plan({
      editable: false,
      notEditableBecause: "the plan is approved; a plan is edited only while its approval is open",
    }))).toBe(
      "Not open for editing: the plan is approved; a plan is edited only while its approval is open.");
  });
  it("says only that it is closed when no reason came", () => {
    expect(planWindowText(plan({ editable: false }))).toBe("Not open for editing.");
  });
});

describe("planDependencyText", () => {
  it.each([
    [[], "Waits for nothing"],
    [["T1"], "Waits for T1"],
    [["T2", "T1"], "Waits for T2 and T1"],
    [["T1", "T2", "T3"], "Waits for T1, T2 and T3"],
  ])("%j reads %j, in the plan's own order", (dependsOn, text) => {
    expect(planDependencyText(task({ dependsOn }))).toBe(text);
  });
});

describe("planEntryText", () => {
  it("names the entry's status and spec version", () => {
    expect(planEntryText(task({ status: "passed", specVersion: 3 }))).toBe("passed · spec version 3");
  });
  it("says so when no task runs the planned task", () => {
    expect(planEntryText(task({ jobTaskId: "", status: "" }))).toBe("No task runs it yet");
  });
  it("says the status is unknown rather than leaving a hole", () => {
    expect(planEntryText(task({ status: "" }))).toBe("status unknown · spec version 1");
  });
});

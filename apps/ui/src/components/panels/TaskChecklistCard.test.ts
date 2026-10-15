// amend1015 P3: the task list, its check mark and its count agree; a finished job adds no task.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { normalizeDashboardPayload } from "../../api/remedyApi";
import { TaskChecklistCard } from "./TaskChecklistCard";

const dashboard = (task: Record<string, unknown>) => normalizeDashboardPayload("j1", {
  job_id: "j1", live: { running: false, state: "completed" }, metrics: {}, phases: [], activity: [],
  tasks: [{ id: "t1", title: "Deliver README.md", ...task }],
});

const card = (props: Partial<Parameters<typeof TaskChecklistCard>[0]> & { tasks: Parameters<typeof TaskChecklistCard>[0]["tasks"] }) =>
  renderToStaticMarkup(createElement(TaskChecklistCard, { jobId: "j1", serverToken: "tok", onSelectNode: () => {}, ...props }));

describe("a done task is checked and counted (amend1015 P3.1)", () => {
  it("verified false does not override the done state", () => {
    const [task] = dashboard({ status: "applied_to_job_workspace", state: "done", verified: false, accepted: false }).tasks;
    expect(task.state).toBe("done");
    expect(task.checked).toBe(true);
    expect(card({ tasks: [task] })).toContain("1 of 1 completed");
  });

  it("a planned task is neither checked nor counted", () => {
    const [task] = dashboard({ status: "pending", state: "planned", verified: false }).tasks;
    expect(task.checked).toBe(false);
    expect(card({ tasks: [task] })).toContain("0 of 1 completed");
  });
});

describe("+ Add Task on a finished job (amend1015 P3.3)", () => {
  it("is disabled and says why", () => {
    const [task] = dashboard({ status: "applied_to_job_workspace", state: "done" }).tasks;
    const html = card({ tasks: [task], finished: true });
    expect(html).toMatch(/<button[^>]*disabled=""[^>]*title="This job has already finished\."[^>]*>\+ Add Task/);
    expect(html).toContain("This job has already finished.");
  });

  it("stays available on a job that is still open", () => {
    const [task] = dashboard({ status: "pending" }).tasks;
    expect(card({ tasks: [task], finished: false })).not.toContain("This job has already finished.");
  });
});

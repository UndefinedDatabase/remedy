// T5_F292 T001 — the plan view's markup, rendered with `renderToStaticMarkup` (DECISION F292 D2).
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { PLAN_ABSENT_TEXT, PLAN_UNREADABLE_TEXT } from "../../api/planView";
import type { RemedyPlan } from "../../api/types";
import { PlanView } from "./PlanView";

const PLAN: RemedyPlan = {
  available: true, version: 3, approval: "pending", editable: true, notEditableBecause: "",
  error: "",
  tasks: [
    { id: "T1", title: "Read the file", goal: "parse it", dependsOn: [], estTokensBand: "S",
      filesHint: [], acceptance: ["reads a file", "reports errors"], jobTaskId: "e1",
      status: "pending", specVersion: 1 },
    { id: "T2", title: "Write tests", goal: "", dependsOn: ["T1"], estTokensBand: "",
      filesHint: [], acceptance: [], jobTaskId: "", status: "", specVersion: 1 },
  ],
};

function render(plan: RemedyPlan): string {
  return renderToStaticMarkup(createElement(PlanView, { plan, onClose: () => {} }));
}

describe("the plan view", () => {
  it("is a dialog named Plan with a close button", () => {
    const markup = render(PLAN);
    expect(markup).toMatch(/^<section [^>]*role="dialog"[^>]*aria-label="Plan"[^>]*data-ui="plan-view"/);
    expect(markup).toMatch(/<button type="button"[^>]*>Close plan<\/button>/);
  });

  it("shows the version, the approval and the open edit window", () => {
    const markup = render(PLAN);
    expect(markup).toMatch(/data-ui="plan-headline">Version 3 · waiting for approval</);
    expect(markup).toMatch(/data-ui="plan-window">Open for editing while its approval is open\.</);
  });

  it("shows a closed window with the server's reason", () => {
    const markup = render({ ...PLAN, editable: false, notEditableBecause: "the job is running" });
    expect(markup).toMatch(/data-ui="plan-window">Not open for editing: the job is running\.</);
  });

  it("lists every planned task in plan order with its title and what it waits for", () => {
    const markup = render(PLAN);
    expect([...markup.matchAll(/data-plan-task="([^"]+)"/g)].map((m) => m[1])).toEqual(["T1", "T2"]);
    expect(markup).toContain("Read the file");
    expect(markup).toContain("Waits for nothing · pending · spec version 1");
    expect(markup).toContain("Waits for T1 · No task runs it yet");
    expect(markup).toContain(">Size S<");
    expect(markup).not.toContain("Size <");
  });

  it("numbers each acceptance criterion from 0, the index the plan edits take", () => {
    const markup = render(PLAN);
    const criteria = [...markup.matchAll(/<li [^>]*><span [^>]*>(\d+)<\/span><span>([^<]*)<\/span><\/li>/g)];
    expect(criteria.map((m) => [m[1], m[2]])).toEqual([["0", "reads a file"], ["1", "reports errors"]]);
    expect(markup).toContain('aria-label="Acceptance criteria of T1"');
  });

  it("says so quietly when the job has no plan, and lists nothing", () => {
    const markup = render({ ...PLAN, available: false, tasks: [] });
    expect(markup).toContain(PLAN_ABSENT_TEXT);
    expect(markup).not.toContain("data-plan-task");
    expect(markup).not.toContain("plan-headline");
  });

  it("says so quietly when the plan could not be read, never the raw error", () => {
    const markup = render({ ...PLAN, error: "invalid literal for int()" });
    expect(markup).toContain(PLAN_UNREADABLE_TEXT.replace(/'/g, "&#x27;"));
    expect(markup).not.toContain("invalid literal");
    expect(markup).not.toContain("data-plan-task");
  });
});

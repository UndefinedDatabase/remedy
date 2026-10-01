// T5_F292 T001 — the plan view's markup, rendered with `renderToStaticMarkup` (DECISION F292 D2).
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { PLAN_ABSENT_TEXT, PLAN_UNREADABLE_TEXT } from "../../api/planView";
import type { RemedyPlan } from "../../api/types";
import { PlanCriteria } from "./PlanCriteria";
import { PlanMergeForm } from "./PlanMergeForm";
import { PlanSplitForm } from "./PlanSplitForm";
import { PlanTaskEditForm } from "./PlanTaskEditForm";
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
  return renderToStaticMarkup(createElement(PlanView, {
    plan, target: { jobId: "0123456789abcdef", serverToken: "token" }, onClose: () => {} }));
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
    const criteria = [...markup.matchAll(/<li [^>]*><span [^>]*>(\d+)<\/span><span>([^<]*)<\/span>/g)];
    expect(criteria.map((m) => [m[1], m[2]])).toEqual([["0", "reads a file"], ["1", "reports errors"]]);
    expect(markup).toContain('aria-label="Acceptance criteria of T1"');
  });

  it("offers each task's Edit and Delete while the plan is open, and an empty outcome line", () => {
    const markup = render(PLAN);
    const buttons = [...markup.matchAll(/<button type="button"[^>]*>(Edit|Delete)<\/button>/g)].map((m) => m[1]);
    expect(buttons).toEqual(["Edit", "Delete", "Edit", "Delete"]);
    expect(markup).not.toMatch(/<button[^>]*disabled[^>]*>(Edit|Delete)</);
    expect(markup).toMatch(/<p [^>]*role="status"[^>]*data-ui="plan-edit-message"[^>]*><\/p>/);
    expect(markup).not.toContain("plan-task-form");
    expect(markup).not.toContain("plan-delete-confirm");
  });

  it("offers no edit control on a plan that is not open for editing", () => {
    const markup = render({ ...PLAN, editable: false, notEditableBecause: "the plan is approved" });
    expect(markup).not.toMatch(/>(Edit|Delete|Move up|Move down|Change|Remove|Add a criterion)<\/button>/);
    expect(markup).toContain("reads a file");
  });

  it("offers Change and Remove on each criterion and Add a criterion on each task", () => {
    const markup = render(PLAN);
    const labels = [...markup.matchAll(/aria-label="((?:Change|Remove) criterion \d+ of T\d)"[^>]*>(Change|Remove)</g)]
      .map((m) => m[1]);
    expect(labels).toEqual(["Change criterion 0 of T1", "Remove criterion 0 of T1", "Change criterion 1 of T1",
      "Remove criterion 1 of T1"]);
    expect([...markup.matchAll(/>Add a criterion<\/button>/g)]).toHaveLength(2);
  });

  it("disables Remove on a task's only criterion, with the reason", () => {
    const markup = render({ ...PLAN, tasks: [{ ...PLAN.tasks[1], acceptance: ["one"] }] });
    expect(markup).toMatch(/<button type="button"[^>]*disabled=""[^>]*title="A task keeps at least one criterion\."[^>]*aria-label="Remove criterion 0 of T2"/);
    expect(markup).not.toMatch(/disabled=""[^>]*aria-label="Change criterion 0 of T2"/);
  });

  it("disables each move a task cannot make, with the reason", () => {
    const markup = render(PLAN);
    const moves = [...markup.matchAll(/<button type="button"[^>]*?(?: disabled="" title="([^"]*)")?>(Move up|Move down)<\/button>/g)]
      .map((m) => [m[2], m[1] ?? null]);
    expect(moves).toEqual([
      ["Move up", "T1 is already first."], ["Move down", "T2 waits for T1, so T1 cannot come after it."],
      ["Move up", "T2 waits for T1, so it cannot come before it."], ["Move down", "T2 is already last."],
    ]);
  });

  it("offers Merge and Split, each disabled with its reason when it cannot start", () => {
    const markup = render(PLAN);
    const regroup = [...markup.matchAll(/<button type="button"[^>]*?(?: disabled="" title="([^"]*)")?>(Merge|Split)<\/button>/g)]
      .map((m) => [m[2], m[1] ?? null]);
    expect(regroup).toEqual([
      ["Merge", null], ["Split", null], ["Merge", null], ["Split", "A task with one criterion cannot be split."],
    ]);
    const alone = render({ ...PLAN, tasks: [PLAN.tasks[0]] });
    expect(alone).toMatch(/disabled="" title="There is no other task to merge with\."[^>]*>Merge<\/button>/);
  });

  it("lets a free task move both ways", () => {
    const free = { ...PLAN, tasks: [PLAN.tasks[0], { ...PLAN.tasks[1], id: "X", dependsOn: [] }, { ...PLAN.tasks[1], id: "Y", dependsOn: [] }] };
    expect(render(free)).toMatch(/data-plan-task="X"[\s\S]*?<button type="button" class="[^"]*">Move up<\/button><button type="button" class="[^"]*">Move down<\/button>/);
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

describe("the task edit form", () => {
  function renderForm(blockedReason: string | null): string {
    return renderToStaticMarkup(createElement(PlanTaskEditForm, {
      task: { ...PLAN.tasks[0], estTokensBand: "L" }, blockedReason, onSave: () => {}, onCancel: () => {} }));
  }

  it("is a form named for its task with the title, goal and size prefilled", () => {
    const markup = renderForm(null);
    expect(markup).toMatch(/^<form [^>]*aria-label="Edit T1"[^>]*data-ui="plan-task-form"/);
    expect(markup).toMatch(/<span>Title<\/span><input type="text" value="Read the file"\/>/);
    expect(markup).toMatch(/<span>Goal<\/span><textarea>parse it<\/textarea>/);
    const options = [...markup.matchAll(/<option value="([^"]+)"( selected="")?>/g)].map((m) => [m[1], m[2] !== undefined]);
    expect(options).toEqual([["S", false], ["M", false], ["L", true], ["XL", false]]);
  });

  it("offers Save and Cancel, Save disabled with the reason while the controls are blocked", () => {
    expect(renderForm(null)).toMatch(/<button type="submit"[^>]*>Save<\/button><button type="button"[^>]*>Cancel<\/button>/);
    expect(renderForm(null)).not.toMatch(/disabled[^>]*>Save</);
    expect(renderForm("An edit is being saved.")).toMatch(
      /<button type="submit"[^>]*disabled=""[^>]*title="An edit is being saved\."[^>]*>Save<\/button>/);
  });
});

describe("the criteria forms (DECISION F292 D4)", () => {
  function renderCriteria(open: number | null | undefined): string {
    return renderToStaticMarkup(createElement(PlanCriteria, {
      task: PLAN.tasks[0], editable: true, open, blockedReason: null, onOpen: () => {}, onSubmit: () => {} }));
  }

  it("opens a criterion's form on its own line, prefilled, in place of its text and its buttons", () => {
    const markup = renderCriteria(1);
    expect(markup).toMatch(/<span [^>]*>1<\/span><form [^>]*aria-label="Change criterion 1 of T1"[^>]*data-ui="plan-criterion-form"><input type="text" aria-label="Change criterion 1 of T1" value="reports errors"\/>/);
    expect(markup).not.toContain('aria-label="Remove criterion 1 of T1"');
    expect(markup).toContain('aria-label="Remove criterion 0 of T1"');
  });

  it("opens an empty add form in place of the Add a criterion button", () => {
    const markup = renderCriteria(null);
    expect(markup).toMatch(/<form [^>]*aria-label="Add a criterion to T1"[^>]*><input type="text" aria-label="Add a criterion to T1" value=""\/>/);
    expect(markup).not.toContain(">Add a criterion</button>");
  });

  it("shows no form when none is open", () => {
    expect(renderCriteria(undefined)).not.toContain("plan-criterion-form");
  });
});

describe("the merge and split forms (DECISION F292 D5)", () => {
  it("the merge form lists every other task to choose, none chosen and nothing previewed yet", () => {
    const markup = renderToStaticMarkup(createElement(PlanMergeForm, {
      plan: PLAN, task: PLAN.tasks[0], blockedReason: null, onMerge: () => {}, onCancel: () => {} }));
    expect(markup).toMatch(/^<form [^>]*aria-label="Merge T1"[^>]*data-ui="plan-merge-form"/);
    expect(markup).toContain("<legend>Merge T1 with</legend>");
    expect([...markup.matchAll(/<input type="checkbox"\/><span>([^<]*)<\/span>/g)].map((m) => m[1]))
      .toEqual(["T2 — Write tests"]);
    expect(markup).not.toContain("plan-merge-preview");
    expect(markup).toMatch(/<button type="submit"[^>]*>Merge tasks<\/button>/);
  });

  it("the split form opens with the last criterion in part 2 and says what the split will do", () => {
    const markup = renderToStaticMarkup(createElement(PlanSplitForm, {
      plan: PLAN, task: PLAN.tasks[0], blockedReason: null, onSplit: () => {}, onCancel: () => {} }));
    expect(markup).toMatch(/^<form [^>]*aria-label="Split T1"[^>]*data-ui="plan-split-form"/);
    const selected = [...markup.matchAll(/aria-label="Part of criterion (\d)">[\s\S]*?<option value="(\d)" selected="">/g)]
      .map((m) => [m[1], m[2]]);
    expect(selected).toEqual([["0", "1"], ["1", "2"]]);
    expect(markup).toMatch(/data-ui="plan-split-preview">T1 becomes 2 tasks run one after the other, each with its part of the criteria\. T2 will wait for the last part\.</);
    expect(markup).toMatch(/<button type="submit"[^>]*>Split task<\/button>/);
  });

  it("disables Merge tasks and Split task with the reason while the controls are blocked", () => {
    const merge = renderToStaticMarkup(createElement(PlanMergeForm, {
      plan: PLAN, task: PLAN.tasks[0], blockedReason: "An edit is being saved.", onMerge: () => {}, onCancel: () => {} }));
    const split = renderToStaticMarkup(createElement(PlanSplitForm, {
      plan: PLAN, task: PLAN.tasks[0], blockedReason: "An edit is being saved.", onSplit: () => {}, onCancel: () => {} }));
    expect(merge).toMatch(/disabled="" title="An edit is being saved\.">Merge tasks</);
    expect(split).toMatch(/disabled="" title="An edit is being saved\.">Split task</);
  });
});

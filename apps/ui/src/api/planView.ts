// T5_F292 T001, DECISION F292 D2: the plan view's rules. Every sentence the plan view shows is
// decided here, over the dashboard's `plan` section, the read `remedy job plan-show --json`
// prints. Nothing here reaches a fetch, a clock, storage or a DOM.
import type { RemedyPlan, RemedyPlanTask } from "./types";

/** Which body the plan view shows: the section's own read failed, the job has no stored plan,
 *  or the plan itself. */
export type PlanBody = "unreadable" | "absent" | "ready";

/** What the view says when the job has no stored plan. */
export const PLAN_ABSENT_TEXT = "This job has no stored plan yet.";
/** What it says when the section's own read failed. */
export const PLAN_UNREADABLE_TEXT = "This job's plan could not be read.";

/** The approvals a stored plan carries (`job_plan.py` writes these three), in plain words. */
const APPROVAL_WORDS: Readonly<Record<string, string>> = {
  pending: "waiting for approval",
  approved: "approved",
  rejected: "rejected",
};

export function planBody(plan: RemedyPlan): PlanBody {
  if (plan.error !== "") return "unreadable";
  return plan.available ? "ready" : "absent";
}

/** The approval in plain words. An approval this table does not know is shown as stored, never
 *  hidden; no stored approval reads "no approval recorded". */
export function planApprovalText(approval: string): string {
  if (approval === "") return "no approval recorded";
  return Object.prototype.hasOwnProperty.call(APPROVAL_WORDS, approval) ? APPROVAL_WORDS[approval] : approval;
}

/** The plan's version and approval in one line: "Version 2 · waiting for approval". */
export function planHeadline(plan: RemedyPlan): string {
  return `Version ${plan.version} · ${planApprovalText(plan.approval)}`;
}

/** Whether the plan is open for editing, in one sentence that carries the server's reason. */
export function planWindowText(plan: RemedyPlan): string {
  if (plan.editable) return "Open for editing while its approval is open.";
  return plan.notEditableBecause === ""
    ? "Not open for editing."
    : `Not open for editing: ${plan.notEditableBecause}.`;
}

/** What a planned task waits for: "Waits for nothing", "Waits for T1", "Waits for T1 and T2",
 *  "Waits for T1, T2 and T3" — in the plan's own order. */
export function planDependencyText(task: RemedyPlanTask): string {
  const ids = task.dependsOn;
  if (ids.length === 0) return "Waits for nothing";
  if (ids.length === 1) return `Waits for ${ids[0]}`;
  return `Waits for ${ids.slice(0, -1).join(", ")} and ${ids[ids.length - 1]}`;
}

/** The task entry that runs a planned task: its status and spec version, or that none does. */
export function planEntryText(task: RemedyPlanTask): string {
  if (task.jobTaskId === "") return "No task runs it yet";
  return `${task.status === "" ? "status unknown" : task.status} · spec version ${task.specVersion}`;
}

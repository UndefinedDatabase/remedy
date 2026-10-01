// T5_F292 T002, DECISION F292 D3: the rules of the plan view's edit controls — when they may be
// used, what a task's edit form sends, and what deleting a task will do to the tasks that wait
// for it. Nothing here reaches a fetch, a clock, storage or a DOM.
import type { PlanTaskFields } from "./planEditSend";
import { planWindowText } from "./planView";
import type { RemedyPlan, RemedyPlanTask } from "./types";

/** The size bands a planned task may carry, in the order the planner's schema lists them
 *  (`TokenBand` in `packages/orchestration/schemas/models.py`). */
export const PLAN_TOKEN_BANDS = ["S", "M", "L", "XL"] as const;

/** What the edit controls wait for: nothing, an edit in flight, or the plan version an accepted
 *  edit landed as, until the dashboard serves it. */
export interface PlanEditGate {
  sending: boolean;
  awaitingVersion: number | null;
}

/** Why the edit controls cannot be used right now, or `null` when they can. A closed plan gives
 *  the plan view's own window sentence (`normalizePlan` never reads a plan that is not available
 *  as editable); the controls also wait while an edit is in flight and until the version an
 *  accepted edit landed as has arrived, because an edit made against the version still shown
 *  would only be refused as stale. */
export function planEditBlockedReason(plan: RemedyPlan, gate: PlanEditGate): string | null {
  if (!plan.editable) return planWindowText(plan);
  if (gate.sending) return "An edit is being saved.";
  if (gate.awaitingVersion !== null && plan.version < gate.awaitingVersion) {
    return `Waiting for version ${gate.awaitingVersion} of the plan to arrive.`;
  }
  return null;
}

/** The edit form's own state: the three fields it shows, as typed. */
export interface PlanTaskDraft {
  title: string;
  goal: string;
  band: string;
}

export function planTaskDraftOf(task: RemedyPlanTask): PlanTaskDraft {
  return { title: task.title, goal: task.goal, band: task.estTokensBand };
}

/** What is wrong with a draft, in one sentence, or `null` when it can be sent. */
export function planTaskDraftProblem(draft: PlanTaskDraft): string | null {
  if (draft.title.trim() === "") return "Give the task a title.";
  if (draft.goal.trim() === "") return "Give the task a goal.";
  if (!(PLAN_TOKEN_BANDS as readonly string[]).includes(draft.band)) return "Choose a size.";
  return null;
}

/** Only the fields the draft changed, the title and goal trimmed; empty when nothing changed,
 *  which the form reports instead of sending an edit the backend refuses as changing nothing. */
export function changedPlanTaskFields(task: RemedyPlanTask, draft: PlanTaskDraft): PlanTaskFields {
  const fields: PlanTaskFields = {};
  const title = draft.title.trim();
  const goal = draft.goal.trim();
  if (title !== task.title) fields.title = title;
  if (goal !== task.goal) fields.goal = goal;
  if (draft.band !== task.estTokensBand) fields.est_tokens_band = draft.band;
  return fields;
}

function joinIds(ids: readonly string[]): string {
  if (ids.length === 1) return ids[0];
  return `${ids.slice(0, -1).join(", ")} and ${ids[ids.length - 1]}`;
}

/** The question a delete asks before it is sent, saying what happens to the tasks that wait
 *  for the task: `plan_delete_task` makes each of them wait for what the deleted task waited
 *  for instead, so a task that waited for nothing simply leaves their waits. */
export function planDeleteQuestion(plan: RemedyPlan, task: RemedyPlanTask): string {
  const dependents = plan.tasks.filter((other) => other.id !== task.id && other.dependsOn.includes(task.id))
    .map((other) => other.id);
  if (dependents.length === 0) return `Delete ${task.id}? No task waits for it.`;
  const waits = dependents.length === 1 ? "waits" : "wait";
  if (task.dependsOn.length === 0) {
    return `Delete ${task.id}? ${joinIds(dependents)} ${waits} for it; that wait will be dropped.`;
  }
  return `Delete ${task.id}? ${joinIds(dependents)} ${waits} for it and will wait for ${joinIds(task.dependsOn)} instead.`;
}

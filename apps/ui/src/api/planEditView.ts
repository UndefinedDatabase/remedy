// T5_F292 T002, DECISIONS F292 D3 to D5: the rules of the plan view's edit controls — when they
// may be used, what a task's edit form sends, what deleting a task will do to the tasks that wait
// for it, when a criterion may be written or removed, where a task may move, and what a merge or
// a split will do. Nothing here reaches a fetch, a clock, storage or a DOM.
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

/** What is wrong with a criterion as typed, or `null` when it can be sent: the planner refuses
 *  an empty criterion. */
export function planCriterionProblem(text: string): string | null {
  return text.trim() === "" ? "Write the criterion." : null;
}

/** Why a criterion cannot be removed, or `null` when it can: the planner refuses a task with no
 *  criterion at all. */
export function planCriterionRemoveBlocked(task: RemedyPlanTask): string | null {
  return task.acceptance.length <= 1 ? "A task keeps at least one criterion." : null;
}

/** Moving a task one place up (-1) or down (1): the whole new order `plan_reorder` takes, or the
 *  reason it cannot move — it is already at that end, or the task it would pass is one it waits
 *  for (up) or one that waits for it (down), which the planner refuses because a job runs its
 *  tasks in plan order. */
export function planMove(plan: RemedyPlan, taskId: string, step: -1 | 1): { order: string[] } | { blocked: string } {
  const ids = plan.tasks.map((task) => task.id);
  const at = ids.indexOf(taskId);
  const to = at + step;
  if (at < 0 || to < 0 || to >= ids.length) {
    return { blocked: step < 0 ? `${taskId} is already first.` : `${taskId} is already last.` };
  }
  const moving = plan.tasks[at];
  const passed = plan.tasks[to];
  if (step < 0 && moving.dependsOn.includes(passed.id)) {
    return { blocked: `${moving.id} waits for ${passed.id}, so it cannot come before it.` };
  }
  if (step > 0 && passed.dependsOn.includes(moving.id)) {
    return { blocked: `${passed.id} waits for ${moving.id}, so ${moving.id} cannot come after it.` };
  }
  const order = [...ids];
  order[at] = passed.id;
  order[to] = moving.id;
  return { order };
}

/** Why no merge can start from this plan, or `null`: a merge needs a second task. */
export function planMergeBlocked(plan: RemedyPlan): string | null {
  return plan.tasks.length < 2 ? "There is no other task to merge with." : null;
}

/** The tasks a merge names, in plan order: the task it started from and the ones chosen. The
 *  planner merges them at the first one's place, under the first one's id. */
export function planMergeIds(plan: RemedyPlan, taskId: string, chosen: readonly string[]): string[] {
  return plan.tasks.map((task) => task.id).filter((id) => id === taskId || chosen.includes(id));
}

/** What a merge will do, said before it is sent, or the reason it cannot be sent: the planner's
 *  `plan_merge_tasks` joins the tasks into the first, with every criterion of each, and every
 *  other task that waited for one of them waits for the first instead. */
export function planMergeSummary(plan: RemedyPlan, ids: readonly string[]): { text: string } | { problem: string } {
  if (ids.length < 2) return { problem: "Choose at least one task to merge with." };
  const members = plan.tasks.filter((task) => ids.includes(task.id));
  const criteria = members.reduce((count, task) => count + task.acceptance.length, 0);
  const first = ids[0];
  const rewired = plan.tasks.filter((task) => !ids.includes(task.id)
    && task.dependsOn.some((dep) => dep !== first && ids.includes(dep))).map((task) => task.id);
  const text = `${joinIds(ids)} become one task, ${first}, with all ${criteria} of their criteria.`;
  return { text: rewired.length === 0 ? text : `${text} ${joinIds(rewired)} will wait for ${first} instead.` };
}

/** Why a task cannot be split, or `null`: a split gives each part at least one criterion. */
export function planSplitBlocked(task: RemedyPlanTask): string | null {
  return task.acceptance.length < 2 ? "A task with one criterion cannot be split." : null;
}

/** The part each criterion starts in: the first part, but the last criterion in the second, so
 *  the form opens on a split the planner would take. */
export function planSplitDefaultParts(task: RemedyPlanTask): number[] {
  return task.acceptance.map((_, index) => (index === task.acceptance.length - 1 ? 2 : 1));
}

/** The partition `plan_split_task` takes: one group of criterion indexes per part that holds
 *  any, in part order, each group in criterion order. */
export function planSplitPartition(parts: readonly number[]): number[][] {
  const numbers = [...new Set(parts)].sort((a, b) => a - b);
  return numbers.map((part) => parts.flatMap((p, index) => (p === part ? [index] : [])));
}

/** What a split will do, said before it is sent, or the reason it cannot be sent: the planner
 *  runs the parts one after the other, the first waiting for what the task waited for, and every
 *  task that waited for the task waits for the last part. */
export function planSplitSummary(plan: RemedyPlan, task: RemedyPlanTask, partition: readonly (readonly number[])[]):
    { text: string } | { problem: string } {
  if (partition.length < 2) return { problem: "Put the criteria into at least two parts." };
  const dependents = plan.tasks.filter((other) => other.id !== task.id && other.dependsOn.includes(task.id))
    .map((other) => other.id);
  const text = `${task.id} becomes ${partition.length} tasks run one after the other, each with its part of the criteria.`;
  if (dependents.length === 0) return { text };
  return { text: `${text} ${joinIds(dependents)} will wait for the last part.` };
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

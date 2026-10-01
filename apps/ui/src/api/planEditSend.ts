// THE PLAN EDIT REQUEST, END TO END (T5_F292 T002, DECISION F292 D3): the six edits the write
// door accepts for a plan waiting for approval (DECISION F015 D3), as pure builders plus the one
// flow that sends. It composes `taskEditSend.ts` and `pauseSend.ts` rather than copying them: the
// token headers, the nonce class, the job-commands path, the one submit and every status that
// carries no plan-edit meaning are theirs, called through.
//
// WHAT IS ITS OWN: the six command ids in the door's spelling, the `args` each one reads (the
// backend's own argument object plus `expected_version`, the plan version the view shows), and
// the sentences specific to a plan edit — an accepted edit naming the plan's new version, a
// refusal that carries the backend's reason, and a stale version. `plan_edit_refusal` in
// `ui_server.py` answers a stale version as 409 with `current_version` and no `detail`, and a
// plan that fails revalidation as 409 with BOTH, so the reason is read first and the stale
// sentence is said only when no reason came.
//
// THE DELIBERATE ABSENCES: it opens no socket of its own, never retries, never throws, mints no
// nonce itself and reads no clock except `taskEditSend.ts`'s own deadline bound.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import { describePauseSendResult } from "./pauseSend";
import { submitTaskEditRequest } from "./taskEditSend";
import type { TaskEditSubmitResult } from "./taskEditSend";

/** The six command ids, in the door's own spelling and the feature file's order
 *  (`PLAN_EDIT_COMMAND_IDS` in `ui_server.py`). */
export const PLAN_EDIT_COMMANDS = [
  "job.plan-edit-task",
  "job.plan-delete-task",
  "job.plan-reorder",
  "job.plan-merge-tasks",
  "job.plan-split-task",
  "job.plan-edit-acceptance",
] as const;

export type PlanEditCommand = (typeof PLAN_EDIT_COMMANDS)[number];

/** One plan edit: its command and the backend's own argument object for it. */
export interface PlanEdit {
  command: PlanEditCommand;
  args: Readonly<Record<string, unknown>>;
}

/** The fields `plan_edit_task` may change that the plan view edits (`EDITABLE_TASK_FIELDS` in
 *  `plan_editing.py` less `files_hint`, which the view does not show, and `acceptance`, which
 *  has its own edit). */
export interface PlanTaskFields {
  title?: string;
  goal?: string;
  est_tokens_band?: string;
}

export function planEditTaskEdit(taskId: string, fields: PlanTaskFields): PlanEdit {
  return { command: "job.plan-edit-task", args: { task_id: taskId, fields } };
}

export function planDeleteTaskEdit(taskId: string): PlanEdit {
  return { command: "job.plan-delete-task", args: { task_id: taskId } };
}

export function planReorderEdit(order: readonly string[]): PlanEdit {
  return { command: "job.plan-reorder", args: { order: [...order] } };
}

export function planMergeTasksEdit(taskIds: readonly string[]): PlanEdit {
  return { command: "job.plan-merge-tasks", args: { task_ids: [...taskIds] } };
}

export function planSplitTaskEdit(taskId: string, partition: readonly (readonly number[])[]): PlanEdit {
  return { command: "job.plan-split-task", args: { task_id: taskId, partition: partition.map((group) => [...group]) } };
}

export type PlanAcceptanceOp = "add" | "edit" | "remove";

/** `index` is left out of the arguments when it is null, which `plan_edit_acceptance` reads as
 *  "at the end" for an add; `text` is left out for a remove, which takes none. */
export function planEditAcceptanceEdit(taskId: string, op: PlanAcceptanceOp, index: number | null, text: string): PlanEdit {
  const args: Record<string, unknown> = { task_id: taskId, op };
  if (index !== null) args.index = index;
  if (op !== "remove") args.text = text;
  return { command: "job.plan-edit-acceptance", args };
}

function isUsablePlanVersion(candidate: number): boolean {
  return Number.isInteger(candidate) && candidate >= 1;
}

/** THE BUILDER: the exact request the commands endpoint accepts for one edit made against
 *  `expectedVersion`, or `null` whenever it would be unsendable — an empty job id or token, a
 *  nonce outside the door's class, a version that is not a whole number of at least 1, or a
 *  command that is not one of the six. */
export function buildPlanEditRequest(
  target: DecisionSendTarget,
  edit: PlanEdit,
  expectedVersion: number,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || !isUsableCommandNonce(clientNonce)
      || !isUsablePlanVersion(expectedVersion)
      || !(PLAN_EDIT_COMMANDS as readonly string[]).includes(edit.command)) {
    return null;
  }
  return {
    path: jobCommandsPath(target.jobId),
    method: "POST",
    headers: {
      Authorization: `Bearer ${target.serverToken}`,
      "X-Remedy-CSRF": target.serverToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      command: edit.command,
      client_nonce: clientNonce,
      args: { ...edit.args, expected_version: expectedVersion },
    }),
  };
}

const STALE_PLAN_SENTENCE = "Not saved: the plan changed since you opened it. Look at it again and redo the edit.";

/** One send's answer in words, and the plan version an accepted edit landed as (`null` for
 *  every other answer, and for an accepted answer that names no version). */
export interface PlanEditOutcome {
  message: DecisionOutcomeMessage;
  version: number | null;
}

/** THE MAPPING. An accepted edit names the plan's new version; a refusal that carries the
 *  backend's reason — a 409 for a closed or invalid plan, a 400 on `args` for an edit the plan
 *  cannot take — says that reason; a 409 with only `current_version` is a stale version; every
 *  other status is worded as `describePauseSendResult` words it. */
export function describePlanEditResult(result: TaskEditSubmitResult): PlanEditOutcome {
  const body = result.body;
  if (result.outcome === "accepted") {
    const version = typeof body?.version === "number" ? body.version : null;
    return { message: { tone: "ok", sentence: `Saved as version ${version ?? "?"}.` }, version };
  }
  if (result.outcome === "refused" && (result.status === 409 || (result.status === 400 && body?.field === "args"))) {
    if (typeof body?.detail === "string" && body.detail !== "") {
      return { message: { tone: "error", sentence: `Not saved: ${body.detail}.` }, version: null };
    }
    if (result.status === 409 && typeof body?.current_version === "number") {
      return { message: { tone: "error", sentence: STALE_PLAN_SENTENCE }, version: null };
    }
  }
  return { message: describePauseSendResult(result), version: null };
}

const PLAN_EDIT_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;
const UNREACHABLE: TaskEditSubmitResult = { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null };

/** Every seam optional and defaulting to the shipped function, as `taskEditSend.ts` takes. */
export interface PlanEditSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<TaskEditSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForPlanEditDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, PLAN_EDIT_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first step that answers
 *  `null`. Neither `null` path touches the network. */
export async function sendPlanEdit(
  target: DecisionSendTarget,
  edit: PlanEdit,
  expectedVersion: number,
  deps: PlanEditSendDeps = {},
): Promise<PlanEditOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitTaskEditRequest(request));
  const deadline = deps.deadline ?? waitForPlanEditDeadline;
  const unsendable: PlanEditOutcome = {
    message: { tone: "warn", sentence: "This edit cannot be sent as it stands." }, version: null };

  const clientNonce = mintNonce();
  if (clientNonce === null) return unsendable;
  const request = buildPlanEditRequest(target, edit, expectedVersion, clientNonce);
  if (request === null) return unsendable;
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describePlanEditResult(settled ?? UNREACHABLE);
  } catch {
    return describePlanEditResult(UNREACHABLE);
  }
}

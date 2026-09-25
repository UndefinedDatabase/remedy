// THE TASK EDIT REQUEST, END TO END (DECISION F026 D4): everything the detail
// popover's "Edit task" form decides, as pure functions plus the one flow that
// sends. It is modelled on `pauseSend.ts` and reuses its helpers rather than
// copying them — `isUsableCommandNonce`, `jobCommandsPath`, `mintDecisionClientNonce`,
// the `DecisionSendRequest`/`DecisionSendTarget` types and, for every refusal this
// module does not need to word for itself, `describePauseSendResult` — for the
// same reason `pauseSend.ts` gives: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so a rule written inside a
// component would ship untested.
//
// IT COMPOSES, IT DOES NOT RETYPE. The two token headers, the nonce class, the
// job-commands path and every status this door can answer that carries no
// task-edit-specific meaning are `pauseSend.ts`'s own, called through, never
// restated. Only what a runtime task edit adds lives here: the one command id,
// the `args` shape `job.edit-task` reads (`task_id`, `fields`,
// `expected_version`), and the sentences that ARE specific to an edit — an
// accepted save naming its new version, and a 409 the two other refusals do
// not carry: a stale `expected_version` and the task-state refusal
// `task_edit_refusal` answers alongside every plan-edit refusal it inherits.
//
// UNLIKE `pauseSend.ts`, THIS MODULE NEVER READS BACK A `body.outcome` WORD.
// `_dispatch_edit_task` answers a fixed shape on 200 — `task_id`, `state`,
// `spec_version`, `version`, `restored` — not the closed vocabulary
// (`requested`/`paused`/`released`/...) `pause_job_command` answers, so this
// module's own acceptance reader is its own, reading `spec_version` and `state`.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. It opens no socket of its own:
// the network is reached only through the injected submit. It never retries
// and never throws; every path answers one sentence. It mints no nonce itself
// and reads no clock except the one deadline, `pauseSend.ts`'s own bound, for
// the same reason. It does NOT decide which fields changed — `changedTaskFields`
// in `taskSpecView.ts` is the one place that reduces a draft to what to send,
// and this module's caller is the one that calls it.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describePauseSendResult } from "./pauseSend";
import type { TaskEditFields } from "./taskSpecView";

/** The command id the door dispatches (DECISION F026 D2), in the door's OWN
 *  spelling — `JOB_EDIT_TASK_COMMAND_ID` in `ui_server.py` — mirrored here
 *  rather than renamed on the way out, the same rule `pauseSend.ts`'s own two
 *  command ids follow. */
export const JOB_EDIT_TASK_COMMAND_ID = "job.edit-task";

/** How long one send may stay unanswered before the operator is told nothing
 *  came back, in milliseconds — `pauseSend.ts`'s own bound, so every send in
 *  this cockpit agrees on what "too long" means. */
const TASK_EDIT_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;

/** Whether a candidate spec version is one the door would accept as
 *  `expected_version`: `_read_command_payload` requires "a whole number of at
 *  least 1" (the comment above `_dispatch_edit_task` states it in those
 *  words), so this mirror is exactly that reading and nothing more. */
function isUsableSpecVersion(candidate: number): boolean {
  return Number.isInteger(candidate) && candidate >= 1;
}

/** THE BUILDER: a target, a task id, the changed fields and the spec version
 *  the form was opened at become the exact request the commands endpoint
 *  accepts, or `null` whenever that request would be UNSENDABLE — an empty
 *  job id or token, an empty task id, a nonce outside the door's class, a
 *  version that is not a whole number of at least 1, or `fields` with
 *  nothing in it, because a save with nothing changed is not an edit at all. */
export function buildTaskEditRequest(
  target: DecisionSendTarget,
  taskId: string,
  fields: TaskEditFields,
  expectedVersion: number,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || taskId === ""
      || !isUsableCommandNonce(clientNonce) || !isUsableSpecVersion(expectedVersion)
      || Object.keys(fields).length === 0) {
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
      command: JOB_EDIT_TASK_COMMAND_ID,
      client_nonce: clientNonce,
      args: { task_id: taskId, fields, expected_version: expectedVersion },
    }),
  };
}

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request — `pauseSend.ts`'s
 *  own `PauseSendReply` shape, restated under this feature's own name because
 *  the two doors answer different bodies and a shared name would invite a
 *  reader to assume a shared shape. */
export interface TaskEditSendReply {
  ok: boolean;
  status: number;
  json(): Promise<unknown>;
}

export type TaskEditSendFunction = (request: DecisionSendRequest) => Promise<TaskEditSendReply>;

/** THE THREE OUTCOMES, mirroring `pauseSend.ts`'s own closed union. */
export type TaskEditSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, the status that says which refusal it
 *  was, and the parsed body — `null` when the reply carried no usable JSON
 *  object. Structurally identical to `pauseSend.ts`'s `PauseSubmitResult`, so
 *  `describeTaskEditResult` below can hand a refusal or an unreachable result
 *  straight to `describePauseSendResult` without a conversion step. */
export interface TaskEditSubmitResult {
  outcome: TaskEditSubmitOutcome;
  status: number;
  body: Record<string, unknown> | null;
}

function parsedObjectOrNull(candidate: unknown): Record<string, unknown> | null {
  if (candidate === null || typeof candidate !== "object" || Array.isArray(candidate)) {
    return null;
  }
  return candidate as Record<string, unknown>;
}

/** THE SUBMIT: send one already-built request, once, read its body, and map
 *  what comes back to the closed result. Never throws and never retries: a
 *  rejected send becomes `unreachable`, and a body that is not JSON or not an
 *  object becomes `null` rather than propagating a parse error. */
export async function submitTaskEditRequest(
  request: DecisionSendRequest,
  send: TaskEditSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<TaskEditSubmitResult> {
  let reply: TaskEditSendReply;
  try {
    reply = await send(request);
  } catch {
    return { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null };
  }
  let parsed: unknown = null;
  try {
    parsed = await reply.json();
  } catch {
    parsed = null;
  }
  return { outcome: reply.ok ? "accepted" : "refused", status: reply.status,
           body: parsedObjectOrNull(parsed) };
}

const STALE_VERSION_SENTENCE =
  "Not saved: this task changed since you opened it. Close it and edit again.";

/** THE RELAUNCH SENTENCE (R-1061): names the job's real id, in the exact shape
 *  the operator would type it at the command line, when a `jobId` is known;
 *  with no `jobId` (the caller could not supply one) it drops the command
 *  entirely rather than print a placeholder nobody could paste. */
function relaunchSentence(jobId: string): string {
  if (jobId === "") {
    return "Relaunch the job to run it.";
  }
  return `Relaunch the job to run it: remedy job run ${jobId}.`;
}

/** What a 200 reply means: `_dispatch_edit_task`'s own fixed shape, never the
 *  pause door's `outcome` vocabulary. `spec_version` names the version the
 *  edit landed as, and a `state` of `failed` — the task was blocked or failed
 *  when the edit was made — earns the relaunch sentence, because saving alone
 *  never restarts the job. */
function describeTaskEditAcceptance(
  body: Record<string, unknown> | null,
  jobId: string,
): DecisionOutcomeMessage {
  const version = body?.spec_version;
  const sentence = `Saved as v${typeof version === "number" ? version : "?"}.`;
  if (body?.state === "failed") {
    return { tone: "ok", sentence: `${sentence} ${relaunchSentence(jobId)}` };
  }
  return { tone: "ok", sentence };
}

/** What a 409 means, DECISION F026 D2's two shapes: `task_edit_refusal`
 *  answers `current_version` for a stale `expected_version` (the SAME body
 *  shape `plan_edit_refusal`'s own version conflict carries) and `detail` for
 *  every other refusal — the task's own state gate, a closed plan, or a
 *  failed revalidation. Every other status is worded exactly as
 *  `describePauseSendResult` words its own, because none of them carries any
 *  task-edit-specific meaning. */
function describeTaskEditConflict(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  if (typeof body?.current_version === "number") {
    return { tone: "error", sentence: STALE_VERSION_SENTENCE };
  }
  const detail = body?.detail;
  if (typeof detail === "string") {
    return { tone: "error", sentence: `Not saved: ${detail}.` };
  }
  return describePauseSendResult({ outcome: "refused", status: 409, body });
}

/** THE MAPPING: one send's result becomes the one thing to say about it. A
 *  fresh object every call, `pauseSend.ts`'s own rule. `jobId` (R-1061) names
 *  the job the relaunch sentence of an accepted, now-`failed`-state edit
 *  offers to restart; it defaults to empty for a caller with no job id at
 *  hand, which drops the command from that sentence rather than fake one. */
export function describeTaskEditResult(
  result: TaskEditSubmitResult,
  jobId: string = "",
): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return describeTaskEditAcceptance(result.body, jobId);
  }
  if (result.outcome === "refused" && result.status === 409) {
    return describeTaskEditConflict(result.body);
  }
  return describePauseSendResult(result);
}

/** The edit that never reached the wire: no nonce could be minted, or the
 *  builder refused the request outright. */
function describeUnsendableTaskEdit(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: "This edit cannot be sent as it stands." };
}

/** Every seam optional and defaulting to the shipped function, the same shape
 *  `pauseSend.ts`'s `PauseSendDeps` takes. */
export interface TaskEditSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<TaskEditSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForTaskEditDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, TASK_EDIT_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first
 *  step that answers `null`. Neither `null` path touches the network. */
export async function sendTaskEdit(
  target: DecisionSendTarget,
  taskId: string,
  fields: TaskEditFields,
  expectedVersion: number,
  deps: TaskEditSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitTaskEditRequest(request));
  const deadline = deps.deadline ?? waitForTaskEditDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendableTaskEdit();
  }
  const request = buildTaskEditRequest(target, taskId, fields, expectedVersion, clientNonce);
  if (request === null) {
    return describeUnsendableTaskEdit();
  }
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describeTaskEditResult(
      settled ?? { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null },
      target.jobId,
    );
  } catch {
    return describeTaskEditResult(
      { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null }, target.jobId);
  }
}

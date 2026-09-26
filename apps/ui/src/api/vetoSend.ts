// THE VETO REQUEST, END TO END (DECISION F027 D8 (5)): everything the "Veto
// task" form decides, as pure functions plus the one flow that sends. It is
// built exactly as `taskEditSend.ts` is built, and for the same reason: the
// shipped vitest config collects `src/**/*.test.ts` only and no DOM harness
// exists, so a rule written inside a component would ship untested.
//
// IT COMPOSES, IT DOES NOT RETYPE. The two token headers, the nonce class, the
// job-commands path and every status this door can answer that carries no
// veto-specific meaning are `pauseSend.ts`'s and `decisionAnswer.ts`'s own,
// called through, never restated. Only what a veto adds lives here: the one
// command id, the `args` shape `job.veto-task` reads (`task_id`, `reason`),
// and the sentences that ARE specific to a veto — an accepted veto naming how
// many tasks it takes down with it, and the four refusal codes
// `task_veto.veto_task_command` answers that no other command carries.
//
// UNLIKE `pauseSend.ts`, THIS MODULE READS A 409's `error` STRING RATHER THAN
// A BODY FIELD. `_dispatch_veto_task`'s caller in `ui_server.py` puts the
// refused command's own `code` and `detail` on the wire as ONE string, `"<code>:
// <detail>"` (`_safe_error(409, f"{code}: {detail}")`) — unlike `job.pause`'s
// generic 409, which names no code at all. This module reads that prefix back
// off to choose the sentence, and falls back to the raw string, verbatim,
// for a code this page does not name one by one.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. It opens no socket of its own:
// the network is reached only through the injected submit. It never retries
// and never throws; every path answers one sentence. It mints no nonce itself
// and reads no clock except the one deadline, `pauseSend.ts`'s own bound, for
// the same reason. It does NOT decide whether a task may be vetoed at all —
// `vetoView.ts`'s `taskVetoAction` is the one place that reduces the
// dashboard's `vetoes` section to that eligibility, and this module's caller
// is the one that calls it.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describePauseSendResult } from "./pauseSend";

/** The command id the door dispatches (DECISION F027 D5), in the door's OWN
 *  spelling — `JOB_VETO_TASK_COMMAND_ID` in `ui_server.py` — mirrored here
 *  rather than renamed on the way out, the same rule `taskEditSend.ts`'s own
 *  command id follows. */
export const JOB_VETO_TASK_COMMAND_ID = "job.veto-task";

/** How long one send may stay unanswered before the operator is told nothing
 *  came back, in milliseconds — `pauseSend.ts`'s own bound, so every send in
 *  this cockpit agrees on what "too long" means. */
const VETO_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;

/** THE BUILDER: a target, a task id, a reason and a nonce become the exact
 *  request the commands endpoint accepts, or `null` whenever that request
 *  would be UNSENDABLE — an empty task id, a reason blank once trimmed, or a
 *  nonce outside the door's class. The reason itself travels UNCHANGED: the
 *  door's own `validate_veto_reason` is the one place that judges its shape,
 *  and a client-side rewrite would only invite the two to disagree. */
export function buildVetoTaskRequest(
  target: DecisionSendTarget,
  taskId: string,
  reason: string,
  clientNonce: string,
): DecisionSendRequest | null {
  if (taskId === "" || reason.trim() === "" || !isUsableCommandNonce(clientNonce)) {
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
      command: JOB_VETO_TASK_COMMAND_ID,
      client_nonce: clientNonce,
      args: { task_id: taskId, reason },
    }),
  };
}

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request — `pauseSend.ts`'s
 *  own `PauseSendReply` shape, restated under this feature's own name because
 *  the two doors answer different bodies and a shared name would invite a
 *  reader to assume a shared shape. */
export interface VetoTaskSendReply {
  ok: boolean;
  status: number;
  json(): Promise<unknown>;
}

export type VetoTaskSendFunction = (request: DecisionSendRequest) => Promise<VetoTaskSendReply>;

/** THE THREE OUTCOMES, mirroring `pauseSend.ts`'s own closed union. */
export type VetoTaskSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, the status that says which refusal it
 *  was, and the parsed body — `null` when the reply carried no usable JSON
 *  object. */
export interface VetoTaskSubmitResult {
  outcome: VetoTaskSubmitOutcome;
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
export async function submitVetoTaskRequest(
  request: DecisionSendRequest,
  send: VetoTaskSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<VetoTaskSubmitResult> {
  let reply: VetoTaskSendReply;
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

const REPLAN_WAITING_SENTENCE = "A replan proposal is waiting in the decision inbox.";
const UNCONFIRMED_SENTENCE = "The job answered, but did not confirm the veto.";

/** What a 200 reply means: `veto_task_command`'s own `outcome` word, checked
 *  before anything else is read, because a body this browser does not
 *  recognise names no `unreachable` list worth counting. `unreachable` is
 *  read defensively (an array or nothing) — a body this shape-loose earns the
 *  same honest fallback a missing field would. */
function describeVetoAcceptance(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  if (body?.outcome !== "vetoed") {
    return { tone: "warn", sentence: UNCONFIRMED_SENTENCE };
  }
  const unreachable = Array.isArray(body.unreachable) ? body.unreachable : [];
  const count = unreachable.length;
  if (count === 0) {
    return { tone: "ok", sentence: `Vetoed. No other task depended on it. ${REPLAN_WAITING_SENTENCE}` };
  }
  if (count === 1) {
    return { tone: "ok", sentence: `Vetoed. 1 task that depends on it will not run. ${REPLAN_WAITING_SENTENCE}` };
  }
  return { tone: "ok", sentence: `Vetoed. ${count} tasks that depend on it will not run. ${REPLAN_WAITING_SENTENCE}` };
}

/** THE FOUR REFUSAL CODES `veto_task_command` answers, and no others — read
 *  off the `<code>: <detail>` string `_dispatch_veto_task`'s caller puts on
 *  the wire (see the header). A code this table does not name falls through
 *  to the raw string, verbatim, so an operator is never told less than the
 *  door actually said. */
const VETO_REFUSAL_SENTENCES: Readonly<Record<string, string>> = {
  job_not_vetoable: "Not vetoed: this job has already finished.",
  task_already_vetoed: "Not vetoed: this task is already vetoed.",
  task_not_vetoable: "Not vetoed: this task can no longer be vetoed.",
  unknown_task: "Not vetoed: this job has no such task.",
};

/** What a 409 means: the refusal `code` prefixing the wire's `error` string,
 *  looked up in the table above, or the raw string echoed back when the code
 *  is not one of the four. A body with no string `error` at all carries no
 *  code to read, so it falls through to `describePauseSendResult`'s own
 *  generic 409 sentence rather than guessing one. */
function describeVetoConflict(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const error = body?.error;
  if (typeof error !== "string") {
    return describePauseSendResult({ outcome: "refused", status: 409, body });
  }
  const separator = error.indexOf(": ");
  const code = separator === -1 ? "" : error.slice(0, separator);
  const sentence = VETO_REFUSAL_SENTENCES[code];
  return { tone: "warn", sentence: sentence ?? `Not vetoed: ${error}.` };
}

/** What a 400 on field `reason` means — `validate_veto_reason`'s own refusal,
 *  whose `detail` string rides as this body's `error` (`_command_field_error`,
 *  the same shape `job.edit-task`'s argument refusals share). Any OTHER 400
 *  falls through to `describePauseSendResult`'s own generic sentence, since
 *  this module names only the reason's own shape errors. */
function describeVetoBadReason(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const error = body?.error;
  if (typeof error !== "string") {
    return describePauseSendResult({ outcome: "refused", status: 400, body });
  }
  return { tone: "warn", sentence: `Not vetoed: ${error}.` };
}

/** THE MAPPING: one send's result becomes the one thing to say about it. A
 *  fresh object every call, `pauseSend.ts`'s own rule. */
export function describeVetoTaskResult(result: VetoTaskSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return describeVetoAcceptance(result.body);
  }
  if (result.outcome === "refused" && result.status === 409) {
    return describeVetoConflict(result.body);
  }
  if (result.outcome === "refused" && result.status === 400 && result.body?.field === "reason") {
    return describeVetoBadReason(result.body);
  }
  return describePauseSendResult(result);
}

/** The veto that never reached the wire: no nonce could be minted, or the
 *  builder refused the request outright. */
function describeUnsendableVeto(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: "This veto cannot be sent as it stands." };
}

/** Every seam optional and defaulting to the shipped function, the same shape
 *  `pauseSend.ts`'s `PauseSendDeps` takes. */
export interface VetoTaskSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<VetoTaskSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForVetoDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, VETO_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first
 *  step that answers `null`. Neither `null` path touches the network. */
export async function sendVetoTask(
  target: DecisionSendTarget,
  taskId: string,
  reason: string,
  deps: VetoTaskSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitVetoTaskRequest(request));
  const deadline = deps.deadline ?? waitForVetoDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendableVeto();
  }
  const request = buildVetoTaskRequest(target, taskId, reason, clientNonce);
  if (request === null) {
    return describeUnsendableVeto();
  }
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describeVetoTaskResult(settled ?? { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null });
  } catch {
    return describeVetoTaskResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null });
  }
}

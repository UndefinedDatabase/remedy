// THE RERUN REQUEST, END TO END (DECISION F029 D6 (1)): everything the run
// detail's Rerun control decides for `job.rerun-subtree`, as pure functions
// plus the one flow that sends. It is built exactly as `injectSend.ts` is
// built, and for the same reason: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so a rule written inside
// a component would ship untested.
//
// IT COMPOSES, IT DOES NOT RETYPE. The two token headers, the nonce class, the
// job-commands path and every status this door can answer that carries no
// rerun-specific meaning are `pauseSend.ts`'s and `decisionAnswer.ts`'s own,
// called through, never restated. Only what a rerun adds lives here: the one
// command id, the `args` shape `job.rerun-subtree` reads (`task_id`, `model`,
// `confirm_cost`), and the one sentence that IS specific to a rerun's
// refusal.
//
// UNLIKE `vetoSend.ts` AND `injectSend.ts`, A REFUSAL'S SENTENCE NEEDS NO
// LOOKUP TABLE. `rerun_subtree_command`'s own `detail` (DECISION F029 D4) is
// ALREADY a plain sentence — unlike `job.veto-task`'s and `job.inject`'s
// codes, which this cockpit still translates one by one — so this module
// reads the `<code>: <detail>` string `_dispatch_rerun_subtree`'s caller puts
// on the wire and echoes the detail back, verbatim, for every code.
//
// THE 200 BODY IS NOT DESCRIBED HERE. A `needs_confirmation` or a `prepared`
// answer is read into sentences by `rerunView.ts`'s `rerunAnswerView`, not by
// this module's own `describeRerunResult` — that function speaks only for a
// refusal or an unreachable server, which `rerunView.ts` never sees.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. It opens no socket of its own:
// the network is reached only through the injected submit. It never retries
// and never throws; every path answers one sentence. It mints no nonce itself
// and reads no clock except `RERUN_DEADLINE_MS`, longer than every other send
// in this cockpit because a subtree rerun's own preparation walks the job's
// worktree before it answers. It does NOT decide whether a task may be
// rerun at all, and it does not decide what a good model override looks
// like — the server's own refusal is the one place that judges either, and
// this module's caller is the one that calls it.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describePauseSendResult } from "./pauseSend";

/** The command id the door dispatches (DECISION F029 D4), in the door's OWN
 *  spelling — `JOB_RERUN_SUBTREE_COMMAND_ID` in `ui_server.py` — mirrored
 *  here rather than renamed on the way out, the same rule `injectSend.ts`'s
 *  own command ids follow. */
export const JOB_RERUN_SUBTREE_COMMAND_ID = "job.rerun-subtree";

/** How long one send may stay unanswered before the operator is told nothing
 *  came back, in milliseconds. Longer than every other send in this cockpit
 *  because a subtree rerun's own preparation walks the job's worktree under
 *  its lock before it answers (DECISION F029 D2). */
export const RERUN_DEADLINE_MS = 60000;

const NO_RESPONSE_STATUS = 0;

/** What the Rerun control's own state decides, beyond the task it targets. */
export interface RerunSubtreeOptions {
  model?: string;
  confirmCost?: boolean;
}

/** THE BUILDER: a target, a task id and the control's own options become the
 *  exact request the commands endpoint accepts, or `null` whenever that
 *  request would be UNSENDABLE — an empty task id, or a nonce outside the
 *  door's class. `model` rides only when it is non-blank once trimmed — the
 *  TRIMMED value, since the record is durable and edge space is noise no
 *  later reader asked for — and `confirm_cost` rides only when it is `true`;
 *  an absent or `false` value degrades to "not sent" rather than `false`,
 *  the same optional-field shape D14 rules for every other command. */
export function buildRerunSubtreeRequest(
  target: DecisionSendTarget,
  taskId: string,
  options: RerunSubtreeOptions,
  clientNonce: string,
): DecisionSendRequest | null {
  if (taskId === "" || !isUsableCommandNonce(clientNonce)) {
    return null;
  }
  const trimmedModel = (options.model ?? "").trim();
  return {
    path: jobCommandsPath(target.jobId),
    method: "POST",
    headers: {
      Authorization: `Bearer ${target.serverToken}`,
      "X-Remedy-CSRF": target.serverToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      command: JOB_RERUN_SUBTREE_COMMAND_ID,
      client_nonce: clientNonce,
      args: {
        task_id: taskId,
        ...(trimmedModel !== "" ? { model: trimmedModel } : {}),
        ...(options.confirmCost === true ? { confirm_cost: true } : {}),
      },
    }),
  };
}

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request — `injectSend.ts`'s
 *  own `InjectSendReply` shape, restated under this feature's own name
 *  because a shared name would invite a reader to assume a shared shape. */
export interface RerunSubtreeSendReply {
  ok: boolean;
  status: number;
  json(): Promise<unknown>;
}

export type RerunSubtreeSendFunction =
  (request: DecisionSendRequest) => Promise<RerunSubtreeSendReply>;

/** THE THREE OUTCOMES, mirroring `injectSend.ts`'s own closed union. */
export type RerunSubtreeSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, the status that says which refusal it
 *  was, and the parsed body — `null` when the reply carried no usable JSON
 *  object. */
export interface RerunSubtreeSubmitResult {
  outcome: RerunSubtreeSubmitOutcome;
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
 *  what comes back to the closed result — `submitInjectRequest`'s own
 *  contract. Never throws and never retries: a rejected send becomes
 *  `unreachable`, and a body that is not JSON or not an object becomes `null`
 *  rather than propagating a parse error. */
export async function submitRerunSubtreeRequest(
  request: DecisionSendRequest,
  send: RerunSubtreeSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<RerunSubtreeSubmitResult> {
  let reply: RerunSubtreeSendReply;
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

/** THE 200 BODY, or `null` for anything that is not an accepted reply — the
 *  one place `rerunView.ts`'s `rerunAnswerView` reaches for a
 *  `needs_confirmation` or a `prepared` answer. */
export function rerunAnswerOf(result: RerunSubtreeSubmitResult): Record<string, unknown> | null {
  return result.outcome === "accepted" ? result.body : null;
}

const UNRECOGNISED_ACCEPTANCE_SENTENCE = "The job answered, but not in a way this page understands.";

/** What a 409 means: the refusal `code` prefixing the wire's `error` string —
 *  `_dispatch_rerun_subtree`'s caller puts `"<code>: <detail>"` on the wire
 *  (see the header) and `detail` is ALREADY a plain sentence, so this module
 *  echoes it back verbatim rather than keeping a second table that could
 *  drift from the server's own words. A body with no string `error` at all
 *  carries nothing to split, so it falls through to `describePauseSendResult`'s
 *  own generic 409 sentence rather than guessing one. */
function describeRerunConflict(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const error = body?.error;
  if (typeof error !== "string") {
    return describePauseSendResult({ outcome: "refused", status: 409, body });
  }
  const separator = error.indexOf(": ");
  const sentence = separator === -1 ? error : error.slice(separator + 2);
  return { tone: "warn", sentence };
}

/** THE MAPPING: one send's result becomes the one thing to say about it, for
 *  the two cases the Rerun control reaches for it — a refusal or an
 *  unreachable server (`rerunView.ts`'s `rerunAnswerView` already speaks for
 *  an accepted reply). An accepted result still answers something rather
 *  than throwing, for a caller that reaches this function anyway. */
export function describeRerunResult(result: RerunSubtreeSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "refused" && result.status === 409) {
    return describeRerunConflict(result.body);
  }
  if (result.outcome === "accepted") {
    return { tone: "warn", sentence: UNRECOGNISED_ACCEPTANCE_SENTENCE };
  }
  // Reused, not reworded: pauseSend.ts's own unreachable sentence, and its
  // generic refusal sentences for every status other than 409.
  return describePauseSendResult(result);
}

/** THE FLOW'S OWN ANSWER: the sentence to show for a refusal or an
 *  unreachable server, and the 200 body a caller reads through
 *  `rerunView.ts`'s `rerunAnswerView` for everything else. */
export interface RerunSubtreeSendOutcome {
  message: DecisionOutcomeMessage;
  answer: Record<string, unknown> | null;
}

/** The send that never reached the wire: no nonce could be minted, or the
 *  builder refused the request outright. */
function describeUnsendableRerun(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: "This rerun cannot be sent as it stands." };
}

/** Every seam optional and defaulting to the shipped function, the same shape
 *  `injectSend.ts`'s `InjectSendDeps` takes. */
export interface RerunSubtreeSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<RerunSubtreeSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForRerunDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, RERUN_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, waiting up to
 *  `RERUN_DEADLINE_MS`. Neither `null` path touches the network. */
export async function sendRerunSubtree(
  target: DecisionSendTarget,
  taskId: string,
  options: RerunSubtreeOptions,
  deps: RerunSubtreeSendDeps = {},
): Promise<RerunSubtreeSendOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitRerunSubtreeRequest(request));
  const deadline = deps.deadline ?? waitForRerunDeadline;

  const clientNonce = mintNonce();
  const request = clientNonce === null
    ? null
    : buildRerunSubtreeRequest(target, taskId, options, clientNonce);
  if (request === null) {
    return { message: describeUnsendableRerun(), answer: null };
  }
  let settled: RerunSubtreeSubmitResult | null;
  try {
    settled = await Promise.race([submit(request), deadline().then(() => null)]);
  } catch {
    settled = null;
  }
  const result = settled ?? { outcome: "unreachable" as const, status: NO_RESPONSE_STATUS, body: null };
  return { message: describeRerunResult(result), answer: rerunAnswerOf(result) };
}

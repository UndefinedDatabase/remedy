// THE PAUSE REQUEST, END TO END (DECISION F025 D4): everything the job's and a
// task's pause/resume controls decide, as pure functions plus the one flow that
// sends. It is built exactly as `steeringSend.ts` is built, and for the same
// reason: the shipped vitest config collects `src/**/*.test.ts` only and no DOM
// harness exists, so a rule written inside a component would ship untested.
//
// IT COMPOSES THE DECISION INBOX'S CHAIN, IT DOES NOT COPY IT. The path and the
// nonce rule are `decisionAnswer.ts`'s, the nonce minter is `decisionNonce.ts`'s,
// and unreachable's tone and sentence are `steeringSend.ts`'s OWN — reused by
// calling `describeChatSendResult`, never retyped, so the two can never drift
// apart on what "no answer came back" says. Only what differs lives here: the
// two command ids, the `args` shape a pause command takes, and the sentences an
// operator reads about a pause rather than about a message.
//
// UNLIKE `decisionSubmit.ts`, THIS MODULE READS THE BODY. `pause_job_command`
// and `unpause_job_command` in `packages/orchestration/pause_control.py` answer
// a JSON body whose `outcome` word — `requested`, `paused`, `released`,
// `withdrawn`, `parked` with `next`, or `not_paused` — decides the sentence, so
// the submit below reads it where `decisionSubmit.ts` deliberately does not.
//
// THE DELIBERATE ABSENCES. It opens no socket of its own: the network is
// reached only through the injected submit. It never retries and never throws;
// every path answers one sentence. It mints no nonce itself and reads no clock
// except the one deadline, the same bound `steeringSend.ts` uses, for the same
// reason.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describeChatSendResult } from "./steeringSend";

/** The two command ids the door dispatches (DECISION F025 D2), in the door's
 *  OWN spelling — `JOB_PAUSE_COMMAND_ID` and `JOB_UNPAUSE_COMMAND_ID` in
 *  `ui_server.py` — mirrored here rather than renamed on the way out, the same
 *  rule `decisionAnswer.ts`'s `DECISION_RESOLVE_COMMAND_ID` follows. */
export const JOB_PAUSE_COMMAND_ID = "job.pause";
export const JOB_UNPAUSE_COMMAND_ID = "job.unpause";

/** The one command a pause/resume control ever sends. */
export type PauseCommand = typeof JOB_PAUSE_COMMAND_ID | typeof JOB_UNPAUSE_COMMAND_ID;

/** How long one send may stay unanswered before the operator is told nothing
 *  came back, in milliseconds — `steeringSend.ts`'s own bound, so the two agree. */
const PAUSE_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;

/** THE BUILDER: a target, a command, an optional task id and a nonce become the
 *  exact request the commands endpoint accepts, or `null` whenever that
 *  request is UNSENDABLE. `taskId` is `undefined` for a job-scope command and a
 *  non-empty string for a task-scope one; `""` is refused rather than treated
 *  as "no task", because a caller that meant the job passes `undefined`, and a
 *  `""` reaching here is a bug this function refuses to paper over. */
export function buildPauseSendRequest(
  target: DecisionSendTarget,
  command: PauseCommand,
  taskId: string | undefined,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || taskId === ""
      || !isUsableCommandNonce(clientNonce)) {
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
      command,
      client_nonce: clientNonce,
      args: taskId === undefined ? {} : { task: taskId },
    }),
  };
}

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request. Unlike
 *  `decisionSubmit.ts`'s `DecisionSendReply`, `json()` is part of the shape:
 *  the door's outcome word lives in the body, and this feature reads it. */
export interface PauseSendReply {
  ok: boolean;
  status: number;
  json(): Promise<unknown>;
}

export type PauseSendFunction = (request: DecisionSendRequest) => Promise<PauseSendReply>;

/** THE THREE OUTCOMES, mirroring `decisionSubmit.ts`'s own closed union. */
export type PauseSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, the status that says which refusal it
 *  was, and the parsed body — `null` when the reply carried no usable JSON
 *  object, which the mapping below reads as "not a way this page understands". */
export interface PauseSubmitResult {
  outcome: PauseSubmitOutcome;
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
export async function submitPauseSendRequest(
  request: DecisionSendRequest,
  send: PauseSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<PauseSubmitResult> {
  let reply: PauseSendReply;
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

const REQUESTED_SENTENCE =
  "Pause requested. The job stops before its next step; the step that is running finishes first.";
const PAUSED_SENTENCE =
  "This task is paused. It will not start until you resume it, and the rest of the job keeps going.";
const RELEASED_SENTENCE = "This task is released. The job picks it up at its next safe point.";
const WITHDRAWN_SENTENCE = "The pause was taken back before the job reached it.";
const PARKED_SENTENCE_PREFIX = "This job is paused and saved. To continue it, run: ";
const NOT_PAUSED_SENTENCE = "Nothing was paused, so nothing changed.";
const UNRECOGNISED_OUTCOME_SENTENCE = "The job answered, but not in a way this page understands.";

const ENDED_SENTENCE = "This job has ended, so it cannot be paused or resumed.";
const MALFORMED_SENTENCE = "This request could not be read, so nothing was paused or resumed.";
const CREDENTIAL_SENTENCE =
  "This dashboard was not allowed to pause or resume this job, so nothing was recorded. Open the dashboard again from a fresh link.";
const RATE_LIMITED_SENTENCE = "Too many requests arrived at once. Wait a moment, then try again.";
const SERVER_FAILED_SENTENCE = "The job could not record this request. Try again in a moment.";
const UNRECOGNISED_REFUSAL_SENTENCE = "The job refused this request, so nothing was recorded.";
const UNSENDABLE_SENTENCE = "This action cannot be sent as the page stands.";

/** What a 200 reply means, chosen by the body's OWN outcome word — the closed
 *  set `pause_job_command` and `unpause_job_command` produce. `parked` names
 *  the relaunch command the body's `next` carries; anything else, including a
 *  missing or non-string `next`, still gets the honest fallback sentence. */
function describePauseAcceptance(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const outcome = body?.outcome;
  switch (outcome) {
    case "requested":
      return { tone: "ok", sentence: REQUESTED_SENTENCE };
    case "paused":
      return { tone: "ok", sentence: PAUSED_SENTENCE };
    case "released":
      return { tone: "ok", sentence: RELEASED_SENTENCE };
    case "withdrawn":
      return { tone: "ok", sentence: WITHDRAWN_SENTENCE };
    case "parked": {
      const next = body?.next;
      return { tone: "ok", sentence: `${PARKED_SENTENCE_PREFIX}${typeof next === "string" ? next : ""}` };
    }
    case "not_paused":
      return { tone: "ok", sentence: NOT_PAUSED_SENTENCE };
    default:
      return { tone: "warn", sentence: UNRECOGNISED_OUTCOME_SENTENCE };
  }
}

/** What a REFUSAL means, chosen by the status alone — the SAME status-to-tone
 *  mapping `describeChatSendResult` uses, composed rather than re-derived, with
 *  sentences about a pause rather than a message. */
function describePauseRefusal(status: number): DecisionOutcomeMessage {
  const { tone } = describeChatSendResult({ outcome: "refused", status });
  switch (status) {
    case 400:
      return { tone, sentence: MALFORMED_SENTENCE };
    case 403:
      return { tone, sentence: CREDENTIAL_SENTENCE };
    case 409:
      return { tone, sentence: ENDED_SENTENCE };
    case 429:
      return { tone, sentence: RATE_LIMITED_SENTENCE };
    case 500:
      return { tone, sentence: SERVER_FAILED_SENTENCE };
    default:
      return { tone, sentence: UNRECOGNISED_REFUSAL_SENTENCE };
  }
}

/** THE MAPPING: one send's result becomes the one thing to say about it. A
 *  fresh object every call. */
export function describePauseSendResult(result: PauseSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "unreachable") {
    // Reused, not reworded: steering's own unreachable sentence names no
    // message and no pause, so it reads true for either.
    return describeChatSendResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS });
  }
  if (result.outcome === "refused") {
    return describePauseRefusal(result.status);
  }
  return describePauseAcceptance(result.body);
}

/** The action that never reached the wire: no nonce could be minted, or the
 *  builder refused the request outright. */
function describeUnsendablePauseCommand(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: UNSENDABLE_SENTENCE };
}

/** Every seam optional and defaulting to the shipped function, the same shape
 *  `steeringSend.ts`'s `SteeringSendDeps` takes. */
export interface PauseSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<PauseSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForPauseDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, PAUSE_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first
 *  step that answers `null`. Neither `null` path touches the network. */
export async function sendPauseCommand(
  target: DecisionSendTarget,
  command: PauseCommand,
  taskId: string | undefined,
  deps: PauseSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitPauseSendRequest(request));
  const deadline = deps.deadline ?? waitForPauseDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendablePauseCommand();
  }
  const request = buildPauseSendRequest(target, command, taskId, clientNonce);
  if (request === null) {
    return describeUnsendablePauseCommand();
  }
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describePauseSendResult(settled ?? { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null });
  } catch {
    return describePauseSendResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null });
  }
}

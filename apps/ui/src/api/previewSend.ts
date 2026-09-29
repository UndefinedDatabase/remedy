// THE PREVIEW PAIR, END TO END (F041 T003, DECISION F041 D5): everything the app card decides
// about starting or stopping a job's preview, as pure functions plus the one flow that sends. It
// is built exactly as `pauseSend.ts` is built, and for the same reason: the shipped vitest config
// collects `src/**/*.test.ts` only and no DOM harness exists, so a rule written inside a
// component would ship untested.
//
// IT COMPOSES `pauseSend.ts`'S OWN GENERIC SUBMIT, IT DOES NOT COPY IT. `submitPauseSendRequest`
// already sends one already-built request once, reads its body, and maps a rejected send or a
// non-JSON reply to the same closed shape this feature needs — nothing about that function is
// specific to a pause, so this module imports it and `PauseSendDeps` directly rather than
// retyping a `PreviewSubmitResult` and a `PreviewSendDeps` that would say the same thing in
// different words. The path and the nonce rule are `decisionAnswer.ts`'s, the nonce minter is
// `decisionNonce.ts`'s, and unreachable's tone and sentence are `steeringSend.ts`'s own —
// composed, never retyped, so the two doors can never drift apart on what "no answer came back"
// says.
//
// THE REQUEST CARRIES NO ARGS: `job.preview-start` and `job.preview-stop` in
// `packages/orchestration/ui_server.py`'s `_dispatch_job_preview` read only `command` and
// `client_nonce`; `args` is sent empty for the reason `buildPauseSendRequest`'s own job-scope
// request is.
//
// THE DELIBERATE ABSENCES. It opens no socket of its own: the network is reached only through the
// injected submit. It never retries and never throws; every path answers one sentence. It mints
// no nonce itself and reads no clock except the one deadline, the same bound `pauseSend.ts` uses,
// for the same reason.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describeChatSendResult } from "./steeringSend";
import { submitPauseSendRequest } from "./pauseSend";
import type { PauseSendDeps, PauseSubmitResult } from "./pauseSend";

/** The two command ids the door dispatches (DECISION F041 D4), in the door's OWN spelling —
 *  `JOB_PREVIEW_START_COMMAND_ID` and `JOB_PREVIEW_STOP_COMMAND_ID` in `ui_server.py` — mirrored
 *  here rather than renamed on the way out, `pauseSend.ts`'s own rule. */
export const JOB_PREVIEW_START_COMMAND_ID = "job.preview-start";
export const JOB_PREVIEW_STOP_COMMAND_ID = "job.preview-stop";

/** The one command the app card ever sends. */
export type PreviewCommand = typeof JOB_PREVIEW_START_COMMAND_ID | typeof JOB_PREVIEW_STOP_COMMAND_ID;

/** How long one send may stay unanswered before the operator is told nothing came back, in
 *  milliseconds — `pauseSend.ts`'s own bound, so every door in this cockpit agrees. */
const PREVIEW_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;

/** THE BUILDER: a target, a command and a nonce become the exact request the commands endpoint
 *  accepts, or `null` whenever that request is UNSENDABLE: an empty job id, an empty token, or a
 *  nonce `isUsableCommandNonce` refuses. */
export function buildPreviewSendRequest(
  target: DecisionSendTarget,
  command: PreviewCommand,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || !isUsableCommandNonce(clientNonce)) {
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
    body: JSON.stringify({ command, client_nonce: clientNonce, args: {} }),
  };
}

const START_ACCEPTED_SENTENCE = "Starting the app. The link appears once the app answers.";
const STOP_ACCEPTED_SENTENCE = "Stopping the app.";
const UNRECOGNISED_OUTCOME_SENTENCE = "The job answered, but not in a way this page understands.";
const MALFORMED_SENTENCE =
  "This request could not be read, so the app was neither started nor stopped.";
const CREDENTIAL_SENTENCE =
  "This dashboard was not allowed to start or stop the app. Open the dashboard again from a fresh link.";
const RATE_LIMITED_SENTENCE = "Too many requests arrived at once. Wait a moment, then try again.";
const SERVER_FAILED_SENTENCE = "The job could not record this request. Try again in a moment.";
const UNRECOGNISED_REFUSAL_SENTENCE = "The job refused this request, so nothing was recorded.";
const UNSENDABLE_SENTENCE = "This action cannot be sent as the page stands.";

/** What a 200 reply means, chosen by which command was sent and the body's own `outcome`
 *  word — `_dispatch_job_preview` never declines, so `accepted` is the only outcome the door
 *  ever answers, and anything else is a shape this page does not recognise. */
function describePreviewAcceptance(
  command: PreviewCommand, body: Record<string, unknown> | null,
): DecisionOutcomeMessage {
  if (body?.outcome === "accepted") {
    return {
      tone: "ok",
      sentence: command === JOB_PREVIEW_START_COMMAND_ID ? START_ACCEPTED_SENTENCE : STOP_ACCEPTED_SENTENCE,
    };
  }
  return { tone: "warn", sentence: UNRECOGNISED_OUTCOME_SENTENCE };
}

/** What a REFUSAL means, chosen by the status alone — the SAME status-to-tone mapping
 *  `describeChatSendResult` uses, composed rather than re-derived, with sentences about the app
 *  rather than about a message. */
function describePreviewRefusal(status: number): DecisionOutcomeMessage {
  const { tone } = describeChatSendResult({ outcome: "refused", status });
  switch (status) {
    case 400:
      return { tone, sentence: MALFORMED_SENTENCE };
    case 403:
      return { tone, sentence: CREDENTIAL_SENTENCE };
    case 429:
      return { tone, sentence: RATE_LIMITED_SENTENCE };
    case 500:
      return { tone, sentence: SERVER_FAILED_SENTENCE };
    default:
      return { tone, sentence: UNRECOGNISED_REFUSAL_SENTENCE };
  }
}

/** THE MAPPING: one send's result becomes the one thing to say about it. A fresh object every
 *  call. */
export function describePreviewSendResult(
  command: PreviewCommand, result: PauseSubmitResult,
): DecisionOutcomeMessage {
  if (result.outcome === "unreachable") {
    // Reused, not reworded: steering's own unreachable sentence names no message and no preview,
    // so it reads true for either.
    return describeChatSendResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS });
  }
  if (result.outcome === "refused") {
    return describePreviewRefusal(result.status);
  }
  return describePreviewAcceptance(command, result.body);
}

/** The action that never reached the wire: no nonce could be minted, or the builder refused the
 *  request outright. */
function describeUnsendablePreviewCommand(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: UNSENDABLE_SENTENCE };
}

function waitForPreviewDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, PREVIEW_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first step that answers
 *  `null`. Neither `null` path touches the network. `deps` is `pauseSend.ts`'s own
 *  `PauseSendDeps` shape, composed rather than retyped. */
export async function sendPreviewCommand(
  target: DecisionSendTarget,
  command: PreviewCommand,
  deps: PauseSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitPauseSendRequest(request));
  const deadline = deps.deadline ?? waitForPreviewDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendablePreviewCommand();
  }
  const request = buildPreviewSendRequest(target, command, clientNonce);
  if (request === null) {
    return describeUnsendablePreviewCommand();
  }
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describePreviewSendResult(
      command, settled ?? { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null },
    );
  } catch {
    return describePreviewSendResult(
      command, { outcome: "unreachable", status: NO_RESPONSE_STATUS, body: null },
    );
  }
}

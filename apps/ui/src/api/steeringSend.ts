// ONE STEERING MESSAGE, END TO END (T5_F264 T001, DECISION F264 D3): everything the
// cockpit's steering input decides, as pure functions plus the one sequence that
// sends. The input field itself only holds what the operator typed and renders the
// sentence this module answers. DECISION F031 D5's rule applies unchanged: the
// shipped vitest config collects `src/**/*.test.ts` only and no DOM harness exists,
// so a rule written inside a component would ship untested.
//
// IT COMPOSES THE DECISION INBOX'S CHAIN, IT DOES NOT COPY IT. The path and the
// nonce rule are `decisionAnswer.ts`'s, the nonce minter is `decisionNonce.ts`'s,
// and the one network call is `decisionSubmit.ts`'s, because none of the three
// knows anything about decisions. Only what differs lives here: the body
// `chat.send` takes, the refusals a message can earn, and the sentences an
// operator reads about a message rather than about an answer.
//
// THE TWO RULES THE SERVER ALSO ENFORCES are mirrored as constants and pinned to
// their Python originals by `tests/ui_contracts/test_steering_send_contract.py`:
// the message limit is `steering.STEERING_MAX_CHARS`, and the ended states are
// `pingpong_job.JOB_TERMINAL_STATES`. The server's answer stays final; the mirror
// only saves the operator a round trip.
//
// THE DELIBERATE ABSENCES. It opens no socket of its own: the network is reached
// only through the injected submit. It never retries and never throws; every path
// answers one sentence. It mints no nonce itself and reads no clock except the one
// deadline, which is the same bound the decision inbox uses, for the same reason.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import { submitDecisionSendRequest } from "./decisionSubmit";
import type { DecisionSubmitResult } from "./decisionSubmit";
import type { DecisionOutcomeMessage } from "./decisionOutcome";

/** The catalog id of the cockpit's steering route (DECISION F264 D2). */
export const CHAT_SEND_COMMAND = "chat.send";

/** The longest message the server records, in characters, after trimming. */
export const STEERING_MAX_CHARS = 2000;

/** The job states in which no run will ever read a message again. */
export const STEERING_ENDED_STATES: readonly string[] = ["completed", "failed", "cancelled"];

/** The sentence under a steering input that cannot send because the job has ended. */
export const STEERING_ENDED_REASON = "This job has ended, so it takes no more steering.";

/** How long one send may stay unanswered before the operator is told nothing came
 *  back, in milliseconds — the decision inbox's bound, so the two agree. */
const STEERING_DEADLINE_MS = 20000;
const NO_RESPONSE_STATUS = 0;

/** Whether a job in `stage` can still be steered. An unknown stage stays open: the
 *  server's 409 is the final word, and a wrongly closed field would hide a channel
 *  that works. */
export function steeringIsOpen(stage: string): boolean {
  return !STEERING_ENDED_STATES.includes(stage.trim().toLowerCase());
}

/** The message as it will be sent, or `null` when the server would refuse it. The
 *  length is counted in code points, as Python's `len` counts it, so a message with
 *  an emoji is judged here exactly as the server judges it. */
export function normalizeSteeringMessage(message: string): string | null {
  const cleaned = message.trim();
  if (cleaned === "" || cleaned.includes("\u0000")
      || Array.from(cleaned).length > STEERING_MAX_CHARS) {
    return null;
  }
  return cleaned;
}

/** THE BUILDER: a job, its token, a message and a nonce become the exact request
 *  the commands endpoint accepts, or `null` whenever that request is unsendable. */
export function buildChatSendRequest(
  target: DecisionSendTarget,
  message: string,
  clientNonce: string,
): DecisionSendRequest | null {
  const cleaned = normalizeSteeringMessage(message);
  if (target.jobId === "" || target.serverToken === "" || cleaned === null
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
      command: CHAT_SEND_COMMAND,
      client_nonce: clientNonce,
      args: { message: cleaned },
    }),
  };
}

const ACCEPTED_SENTENCE =
  "Your message was recorded. The job reads it at its next safe point.";
const UNREACHABLE_SENTENCE =
  "No answer came back, so this may not have reached the job. You can send it again.";
const MALFORMED_SENTENCE =
  `The job could not take this message. Keep it to one message of at most ${STEERING_MAX_CHARS} characters.`;
const CREDENTIAL_SENTENCE =
  "This dashboard was not allowed to steer the job, so nothing was recorded. Open the dashboard again from a fresh link.";
const ENDED_SENTENCE = "This job has ended, so the message was not recorded.";
const RATE_LIMITED_SENTENCE =
  "Too many messages arrived at once. Wait a moment, then send this one again.";
const SERVER_FAILED_SENTENCE =
  "The job could not record this message. Try again in a moment.";
const UNRECOGNISED_REFUSAL_SENTENCE = "The job refused this message, so nothing was recorded.";
const UNSENDABLE_SENTENCE =
  `This message cannot be sent as it stands: it must not be empty and must be at most ${STEERING_MAX_CHARS} characters.`;

/** THE MAPPING: one send's result becomes the one thing to say about it, read by
 *  status NAME. A fresh object every call. */
export function describeChatSendResult(result: DecisionSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return { tone: "ok", sentence: ACCEPTED_SENTENCE };
  }
  if (result.outcome === "unreachable") {
    return { tone: "warn", sentence: UNREACHABLE_SENTENCE };
  }
  switch (result.status) {
    case 400:
      return { tone: "error", sentence: MALFORMED_SENTENCE };
    case 403:
      return { tone: "error", sentence: CREDENTIAL_SENTENCE };
    case 409:
      return { tone: "error", sentence: ENDED_SENTENCE };
    case 429:
      return { tone: "warn", sentence: RATE_LIMITED_SENTENCE };
    case 500:
      return { tone: "warn", sentence: SERVER_FAILED_SENTENCE };
    default:
      return { tone: "error", sentence: UNRECOGNISED_REFUSAL_SENTENCE };
  }
}

/** The message that never reached the wire. `warn`: the operator can edit it. */
export function describeUnsendableChatMessage(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: UNSENDABLE_SENTENCE };
}

/** Every seam optional and defaulting to the shipped function, so a click site
 *  passes nothing and a test replaces any subset without touching a global. */
export interface SteeringSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<DecisionSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitForDefaultDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, STEERING_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened, stopping at the first step
 *  that answers `null`. Neither `null` path touches the network. */
export async function sendSteeringMessage(
  target: DecisionSendTarget,
  message: string,
  deps: SteeringSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitDecisionSendRequest(request));
  const deadline = deps.deadline ?? waitForDefaultDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendableChatMessage();
  }
  const request = buildChatSendRequest(target, message, clientNonce);
  if (request === null) {
    return describeUnsendableChatMessage();
  }
  try {
    const settled = await Promise.race([submit(request), deadline().then(() => null)]);
    return describeChatSendResult(settled ?? { outcome: "unreachable", status: NO_RESPONSE_STATUS });
  } catch {
    return describeChatSendResult({ outcome: "unreachable", status: NO_RESPONSE_STATUS });
  }
}

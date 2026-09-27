// THE INJECTION REQUEST, END TO END (DECISION F028 D6 (3)): everything the "Add
// Task" affordance decides for its three commands, as pure functions plus the
// flows that send. It is built exactly as `vetoSend.ts` is built, and for the
// same reason: the shipped vitest config collects `src/**/*.test.ts` only and
// no DOM harness exists, so a rule written inside a component would ship
// untested.
//
// IT COMPOSES, IT DOES NOT RETYPE. The two token headers, the nonce class, the
// job-commands path and every status this door can answer that carries no
// injection-specific meaning are `pauseSend.ts`'s and `decisionAnswer.ts`'s
// own, called through, never restated. Only what an injection adds lives
// here: the three command ids, the `args` shape each one reads, and the
// sentences that ARE specific to an injection — the four 200 outcomes a draft,
// a confirm or an answer can settle into, and the sixteen refusal codes
// `_dispatch_injection` answers that no other command carries.
//
// UNLIKE `decisionSubmit.ts`, THIS MODULE READS THE BODY, exactly as
// `vetoSend.ts` does and for the same reason: `_dispatch_injection`'s caller in
// `ui_server.py` puts the refused command's own `code` and `detail` on the
// wire as ONE string, `"<code>: <detail>"` (`_safe_error(409, f"{code}:
// {detail}")`) — unlike `job.pause`'s generic 409, which names no code at all.
// This module reads that prefix back off to choose the sentence, and falls
// back to the raw string, verbatim, for a code this page does not name one by
// one.
//
// THE DRAFT'S OWN DEADLINE IS LONGER THAN EVERY OTHER SEND IN THIS COCKPIT,
// because `job.inject` is the one command whose effect calls the planner
// before it answers (DECISION F028 D5's own header notes the server is a
// `ThreadingHTTPServer`, so this call does not hold the stream, but the
// browser still waits on it) — `INJECT_DRAFT_DEADLINE_MS` names that wait.
// `job.inject-confirm` and `job.inject-answer` call no planner, so they take
// `INJECT_STEP_DEADLINE_MS`, `pauseSend.ts`'s own bound.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. It opens no socket of its own:
// the network is reached only through the injected submit. It never retries
// and never throws; every path answers one sentence. It mints no nonce itself
// and reads no clock except the two deadlines above. It does NOT decide
// whether the "Add Task" affordance may open at all, and it does not decide
// what the operator typed is a good idea — the planner's own draft, read back
// through `describeInjectResult`, is the one place that judges the text, and
// this module's caller is the one that calls it.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import type { DecisionOutcomeMessage } from "./decisionOutcome";
import { describePauseSendResult } from "./pauseSend";

/** The three command ids the door dispatches (DECISION F028 D5), in the
 *  door's OWN spelling — `JOB_INJECT_COMMAND_ID`, `JOB_INJECT_CONFIRM_COMMAND_ID`
 *  and `JOB_INJECT_ANSWER_COMMAND_ID` in `ui_server.py` — mirrored here rather
 *  than renamed on the way out, the same rule `vetoSend.ts`'s own command id
 *  follows. */
export const JOB_INJECT_COMMAND_ID = "job.inject";
export const JOB_INJECT_CONFIRM_COMMAND_ID = "job.inject-confirm";
export const JOB_INJECT_ANSWER_COMMAND_ID = "job.inject-answer";

/** The closed set `job.inject-answer` accepts for `option` — `task_injection
 *  .SHORTFALL_OPTIONS` in the server's own order, mirrored here rather than
 *  renamed on the way out. */
export const INJECT_SHORTFALL_OPTIONS = ["extend_budget", "shrink_task", "drop"] as const;

/** One option `job.inject-answer` accepts. */
export type InjectShortfallOption = (typeof INJECT_SHORTFALL_OPTIONS)[number];

/** How long a DRAFT may stay unanswered before the operator is told nothing
 *  came back, in milliseconds. Longer than every other send in this cockpit
 *  because `job.inject`'s effect calls the planner before it answers. */
export const INJECT_DRAFT_DEADLINE_MS = 120000;

/** How long a CONFIRM or an ANSWER may stay unanswered — `pauseSend.ts`'s own
 *  bound, since neither command calls the planner. */
export const INJECT_STEP_DEADLINE_MS = 20000;

const NO_RESPONSE_STATUS = 0;

function isUsableAfter(after: string | undefined): after is string {
  return typeof after === "string" && after !== "";
}

/** THE DRAFT BUILDER: a target, the operator's text, an optional placement ref
 *  and a caller-supplied nonce become the exact request the commands endpoint
 *  accepts, or `null` whenever that request would be UNSENDABLE — text blank
 *  after trimming, or a nonce outside the door's class. The text itself
 *  travels UNCHANGED: the door's own `validate_injection_text` is the one
 *  place that judges its shape, and a client-side rewrite would only invite
 *  the two to disagree. `after` rides only when it is a non-empty string —
 *  an absent placement ref means "wherever the planner sees fit", which is
 *  what `resolve_after_ref` reads a missing key as. */
export function buildInjectDraftRequest(
  target: DecisionSendTarget,
  text: string,
  after: string | undefined,
  clientNonce: string,
): DecisionSendRequest | null {
  if (text.trim() === "" || !isUsableCommandNonce(clientNonce)) {
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
      command: JOB_INJECT_COMMAND_ID,
      client_nonce: clientNonce,
      args: isUsableAfter(after) ? { text, after } : { text },
    }),
  };
}

/** THE CONFIRM BUILDER: a target, a draft's confirm token and a nonce become
 *  the exact request, or `null` for an empty token or an unusable nonce. */
export function buildInjectConfirmRequest(
  target: DecisionSendTarget,
  confirmToken: string,
  clientNonce: string,
): DecisionSendRequest | null {
  if (confirmToken === "" || !isUsableCommandNonce(clientNonce)) {
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
      command: JOB_INJECT_CONFIRM_COMMAND_ID,
      client_nonce: clientNonce,
      args: { confirm_token: confirmToken },
    }),
  };
}

/** THE ANSWER BUILDER: a target, a shortfall draft's id, the operator's chosen
 *  option and a nonce become the exact request, or `null` for an empty draft
 *  id, an option outside `INJECT_SHORTFALL_OPTIONS` or an unusable nonce. */
export function buildInjectAnswerRequest(
  target: DecisionSendTarget,
  draftId: string,
  option: string,
  clientNonce: string,
): DecisionSendRequest | null {
  if (
    draftId === "" ||
    !(INJECT_SHORTFALL_OPTIONS as readonly string[]).includes(option) ||
    !isUsableCommandNonce(clientNonce)
  ) {
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
      command: JOB_INJECT_ANSWER_COMMAND_ID,
      client_nonce: clientNonce,
      args: { draft_id: draftId, option },
    }),
  };
}

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request — `vetoSend.ts`'s
 *  own `VetoTaskSendReply` shape, restated under this feature's own name
 *  because a shared name would invite a reader to assume a shared shape. */
export interface InjectSendReply {
  ok: boolean;
  status: number;
  json(): Promise<unknown>;
}

export type InjectSendFunction = (request: DecisionSendRequest) => Promise<InjectSendReply>;

/** THE THREE OUTCOMES, mirroring `vetoSend.ts`'s own closed union. */
export type InjectSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, the status that says which refusal it
 *  was, and the parsed body — `null` when the reply carried no usable JSON
 *  object. */
export interface InjectSubmitResult {
  outcome: InjectSubmitOutcome;
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
 *  what comes back to the closed result — `submitVetoTaskRequest`'s own
 *  contract. Never throws and never retries: a rejected send becomes
 *  `unreachable`, and a body that is not JSON or not an object becomes `null`
 *  rather than propagating a parse error. */
export async function submitInjectRequest(
  request: DecisionSendRequest,
  send: InjectSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<InjectSubmitResult> {
  let reply: InjectSendReply;
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

const DRAFTED_SENTENCE =
  "Drafted. Review it, then confirm to add this task to the plan.";
const SHORTFALL_SENTENCE =
  "This draft would put the job over budget. Choose how to proceed before it can be confirmed.";
const CONFIRMED_SENTENCE = "Added. This task joins the plan and the job may start it next.";
const DROPPED_SENTENCE = "Dropped. This draft will not be added.";
const UNCONFIRMED_SENTENCE = "The job answered, but did not confirm the injection.";

/** What a 200 reply means: the body's own `outcome` word, checked before
 *  anything else is read. Any outcome this table does not name — including a
 *  missing one — reads as unconfirmed rather than guessing which of the four
 *  it might have meant. */
function describeInjectAcceptance(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  switch (body?.outcome) {
    case "drafted":
      return { tone: "ok", sentence: DRAFTED_SENTENCE };
    case "shortfall":
      return { tone: "warn", sentence: SHORTFALL_SENTENCE };
    case "confirmed":
      return { tone: "ok", sentence: CONFIRMED_SENTENCE };
    case "dropped":
      return { tone: "ok", sentence: DROPPED_SENTENCE };
    default:
      return { tone: "warn", sentence: UNCONFIRMED_SENTENCE };
  }
}

/** THE SIXTEEN REFUSAL CODES `_dispatch_injection` answers, and no others —
 *  read off the `<code>: <detail>` string its caller puts on the wire (see the
 *  header). A code this table does not name falls through to the raw string,
 *  verbatim, so an operator is never told less than the door actually said. */
const INJECT_REFUSAL_SENTENCES: Readonly<Record<string, string>> = {
  job_terminal: "Not added: this job has already finished.",
  no_task_plan: "Not added: this job has no task plan to add a task to.",
  plan_full: "Not added: the plan is already at its task cap.",
  planner_unavailable: "Not drafted: no planner is available right now.",
  budget_unreadable: "Not drafted: this job's budget state cannot be read.",
  draft_unparseable: "Not drafted: the planner's reply could not be read as a task.",
  draft_invalid: "Not drafted: the drafted task cannot be added to this job's plan.",
  unknown_task: "Not added: this job has no such task.",
  draft_unknown: "Not confirmed: this draft no longer exists.",
  draft_expired: "Not confirmed: this draft has expired.",
  draft_needs_decision: "Not confirmed: this draft is over budget and needs a decision first.",
  already_confirmed: "Not confirmed: this draft has already been confirmed.",
  draft_stale: "Not confirmed: this draft no longer matches the job's plan.",
  draft_not_in_shortfall: "Not answered: this draft is not waiting on a shortfall decision.",
  already_answered: "Not answered: this draft's shortfall has already been answered.",
  cannot_shrink: "Not answered: this draft cannot be shrunk any further.",
};

/** What a 409 means: the refusal `code` prefixing the wire's `error` string,
 *  looked up in the table above, or the raw string echoed back when the code
 *  is not one of the sixteen. A body with no string `error` at all carries no
 *  code to read, so it falls through to `describePauseSendResult`'s own
 *  generic 409 sentence rather than guessing one. */
function describeInjectConflict(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const error = body?.error;
  if (typeof error !== "string") {
    return describePauseSendResult({ outcome: "refused", status: 409, body });
  }
  const separator = error.indexOf(": ");
  const code = separator === -1 ? "" : error.slice(0, separator);
  const sentence = INJECT_REFUSAL_SENTENCES[code];
  return { tone: "warn", sentence: sentence ?? `Not done: ${error}.` };
}

/** What a 400 on field `text` means — `validate_injection_text`'s own
 *  refusal, whose `detail` string rides as this body's `error`
 *  (`_command_field_error`, the same shape `job.veto-task`'s reason refusals
 *  share). Any OTHER 400 falls through to `describePauseSendResult`'s own
 *  generic sentence, since this module names only the text's own shape
 *  errors. */
function describeInjectBadText(body: Record<string, unknown> | null): DecisionOutcomeMessage {
  const error = body?.error;
  if (typeof error !== "string") {
    return describePauseSendResult({ outcome: "refused", status: 400, body });
  }
  return { tone: "warn", sentence: `Not drafted: ${error}.` };
}

/** THE MAPPING: one send's result becomes the one thing to say about it. A
 *  fresh object every call, `vetoSend.ts`'s own rule. */
export function describeInjectResult(result: InjectSubmitResult): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return describeInjectAcceptance(result.body);
  }
  if (result.outcome === "refused" && result.status === 409) {
    return describeInjectConflict(result.body);
  }
  if (result.outcome === "refused" && result.status === 400 && result.body?.field === "text") {
    return describeInjectBadText(result.body);
  }
  return describePauseSendResult(result);
}

/** THE 200 BODY, or `null` for anything that is not an accepted reply — the
 *  one place a caller reaches for a draft's `confirm_token`, a shortfall's
 *  `decision_seed` or a confirm's `placement`, none of which this module
 *  interprets itself. */
export function injectAnswerOf(result: InjectSubmitResult): Record<string, unknown> | null {
  return result.outcome === "accepted" ? result.body : null;
}

/** The send that never reached the wire: no nonce could be minted, or the
 *  builder refused the request outright. */
function describeUnsendableInject(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: "This cannot be sent as it stands." };
}

/** THE FLOW'S OWN ANSWER: the sentence to show and the 200 body a caller may
 *  still want to read, e.g. a draft's `confirm_token`. */
export interface InjectSendOutcome {
  message: DecisionOutcomeMessage;
  answer: Record<string, unknown> | null;
}

/** Every seam optional and defaulting to the shipped function, the same shape
 *  `vetoSend.ts`'s `VetoTaskSendDeps` takes. */
export interface InjectSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<InjectSubmitResult>;
  deadline?: () => Promise<void>;
}

function waitFor(ms: number): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, ms);
  });
}

async function runInjectSend(
  request: DecisionSendRequest | null,
  deps: InjectSendDeps,
  defaultDeadlineMs: number,
): Promise<InjectSendOutcome> {
  if (request === null) {
    return { message: describeUnsendableInject(), answer: null };
  }
  const submit = deps.submit ?? ((sent) => submitInjectRequest(sent));
  const deadline = deps.deadline ?? (() => waitFor(defaultDeadlineMs));
  let settled: InjectSubmitResult | null;
  try {
    settled = await Promise.race([submit(request), deadline().then(() => null)]);
  } catch {
    settled = null;
  }
  const result = settled ?? { outcome: "unreachable" as const, status: NO_RESPONSE_STATUS, body: null };
  return { message: describeInjectResult(result), answer: injectAnswerOf(result) };
}

/** THE DRAFT FLOW: mint, build, send, and say what happened, waiting up to
 *  `INJECT_DRAFT_DEADLINE_MS` — the planner's own call rides inside this send.
 *  Neither `null` path touches the network. */
export async function sendInjectDraft(
  target: DecisionSendTarget,
  text: string,
  after: string | undefined,
  deps: InjectSendDeps = {},
): Promise<InjectSendOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const clientNonce = mintNonce();
  const request = clientNonce === null
    ? null
    : buildInjectDraftRequest(target, text, after, clientNonce);
  return runInjectSend(request, deps, INJECT_DRAFT_DEADLINE_MS);
}

/** THE CONFIRM FLOW: mint, build, send, and say what happened, waiting up to
 *  `INJECT_STEP_DEADLINE_MS`. Neither `null` path touches the network. */
export async function sendInjectConfirm(
  target: DecisionSendTarget,
  confirmToken: string,
  deps: InjectSendDeps = {},
): Promise<InjectSendOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const clientNonce = mintNonce();
  const request = clientNonce === null
    ? null
    : buildInjectConfirmRequest(target, confirmToken, clientNonce);
  return runInjectSend(request, deps, INJECT_STEP_DEADLINE_MS);
}

/** THE ANSWER FLOW: mint, build, send, and say what happened, waiting up to
 *  `INJECT_STEP_DEADLINE_MS`. Neither `null` path touches the network. */
export async function sendInjectAnswer(
  target: DecisionSendTarget,
  draftId: string,
  option: string,
  deps: InjectSendDeps = {},
): Promise<InjectSendOutcome> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const clientNonce = mintNonce();
  const request = clientNonce === null
    ? null
    : buildInjectAnswerRequest(target, draftId, option, clientNonce);
  return runInjectSend(request, deps, INJECT_STEP_DEADLINE_MS);
}

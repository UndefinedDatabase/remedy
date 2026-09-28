// ONE CHAT TURN, END TO END (F038 T003, DECISION F038 D12): the pure half of the evidence
// panel's Chat tab. It decodes the chat route's one wire shape — `chat_turn_view` in
// `packages/orchestration/chat_turn.py`, the SAME shape `remedy chat ask --json` emits
// (DECISION F038 D11) — builds the route's path, marks each answer sentence cited,
// unsupported or absent, names the answer's scope, and builds, sends and describes the one
// request a confirmed card sends. `EvidenceChatTab.tsx` renders what this module decides and
// decides nothing itself: the shipped vitest config collects `src/**/*.test.ts` only and no DOM
// harness exists, so a rule written inside a component would ship untested (DECISION F031 D5,
// followed here for the same reason).
//
// IT COMPOSES THE DECISION INBOX'S CHAIN, IT DOES NOT COPY IT, exactly as `pauseSend.ts` and
// `steeringSend.ts` do: the path and the nonce rule are `decisionAnswer.ts`'s, the nonce minter
// is `decisionNonce.ts`'s, and the one network call is `decisionSubmit.ts`'s submit, because
// none of the three knows anything about chat. Only what differs lives here: the shape of a
// turn, the `args` a confirmed card carries verbatim, and the sentence naming what was sent.
//
// THE DECODER REFUSES WHOLE, exactly as `resultTour.ts` and `ownership.ts` refuse whole: a
// key missing, mistyped or a citation naming no evidence item makes the whole view `null`
// rather than a partial one a card could act on with a number that resolves to nothing.
//
// IT OPENS NO SOCKET OF ITS OWN: `loadChatTurn` in `remedyApi.ts` is the one read, and the
// send below goes out through the injected submit exactly as `sendSteeringMessage` does.
import { isUsableCommandNonce, jobCommandsPath } from "./decisionAnswer";
import { mintDecisionClientNonce } from "./decisionNonce";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import { submitDecisionSendRequest } from "./decisionSubmit";
import type { DecisionSubmitResult } from "./decisionSubmit";
import { describeDecisionSubmitResult } from "./decisionOutcome";
import type { DecisionOutcomeMessage } from "./decisionOutcome";

/** The one sentence an answer gives when nothing in its evidence answers the question,
 *  spelled exactly as `CHAT_NOT_IN_EVIDENCE` in `packages/orchestration/chat_answer.py`. */
export const CHAT_NOT_IN_EVIDENCE = "Not in evidence.";

/** The two kinds `chat_turn_view` answers, in that module's own spelling — `CHAT_TURN_ANSWER`
 *  and `CHAT_TURN_CARD` in `packages/orchestration/chat_turn.py`. */
const CHAT_TURN_ANSWER_KIND = "answer";
const CHAT_TURN_CARD_KIND = "card";

/** One numbered evidence item an answer may cite, as `chat_turn_view` numbers it. */
export interface ChatEvidenceItemView {
  number: number;
  kind: string;
  ref: string;
  text: string;
}

/** One sentence of an answer, checked against its evidence. */
export interface ChatAnswerSentenceView {
  text: string;
  citations: number[];
  supported: boolean;
  problem: string;
}

/** A checked answer to one question, over one evidence set. */
export interface ChatAnswerView {
  kind: "answer";
  scope: string;
  subject: string;
  question: string;
  generator: string;
  sentences: ChatAnswerSentenceView[];
  evidence: ChatEvidenceItemView[];
  omitted: number;
}

/** What a person confirms, exactly as `chat_turn_view` shapes a `ChatActionCard`. */
export interface ChatCardView {
  kind: "card";
  verb: string;
  title: string;
  lines: string[];
  args: Record<string, string>;
  missing: string[];
  confirmable: boolean;
}

/** A turn the route could not run: an empty line, or a task id naming no task of the job. */
export interface ChatUnavailableView {
  kind: "unavailable";
  reason: string;
}

/** The chat route's whole envelope, or the reason it has nothing to answer. */
export type ChatTurnView = ChatAnswerView | ChatCardView | ChatUnavailableView;

function recordOf(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>) : null;
}

function textOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function chatAnswerSentenceViewOf(value: unknown, itemCount: number): ChatAnswerSentenceView | null {
  const sentence = recordOf(value);
  if (sentence === null) return null;
  const text = textOf(sentence["text"]);
  const rawCitations = sentence["citations"];
  const supported = sentence["supported"];
  const problem = textOf(sentence["problem"]);
  if (text === null || !Array.isArray(rawCitations) || typeof supported !== "boolean" || problem === null) {
    return null;
  }
  const citations: number[] = [];
  for (const raw of rawCitations) {
    if (typeof raw !== "number" || !Number.isInteger(raw) || raw < 1 || raw > itemCount) return null;
    citations.push(raw);
  }
  return { text, citations, supported, problem };
}

function chatEvidenceItemViewOf(value: unknown, expectedNumber: number): ChatEvidenceItemView | null {
  const item = recordOf(value);
  if (item === null) return null;
  const number = item["number"];
  const kind = textOf(item["kind"]);
  const ref = textOf(item["ref"]);
  const text = textOf(item["text"]);
  if (typeof number !== "number" || number !== expectedNumber
      || kind === null || ref === null || text === null) {
    return null;
  }
  return { number, kind, ref, text };
}

function chatAnswerViewOf(payload: Record<string, unknown>): ChatAnswerView | null {
  const scope = textOf(payload["scope"]);
  const subject = textOf(payload["subject"]);
  const question = textOf(payload["question"]);
  const generator = textOf(payload["generator"]);
  const rawEvidence = payload["evidence"];
  const omitted = payload["omitted"];
  const rawSentences = payload["sentences"];
  if (scope === null || subject === null || question === null || generator === null
      || !Array.isArray(rawEvidence) || typeof omitted !== "number" || !Number.isInteger(omitted)
      || !Array.isArray(rawSentences) || rawSentences.length === 0) {
    return null;
  }
  const evidence: ChatEvidenceItemView[] = [];
  for (let index = 0; index < rawEvidence.length; index += 1) {
    const item = chatEvidenceItemViewOf(rawEvidence[index], index + 1);
    if (item === null) return null;
    evidence.push(item);
  }
  const sentences: ChatAnswerSentenceView[] = [];
  for (const rawSentence of rawSentences) {
    const sentence = chatAnswerSentenceViewOf(rawSentence, evidence.length);
    if (sentence === null) return null;
    sentences.push(sentence);
  }
  return {
    kind: "answer", scope, subject, question, generator, sentences, evidence, omitted,
  };
}

function chatCardViewOf(payload: Record<string, unknown>): ChatCardView | null {
  const verb = textOf(payload["verb"]);
  const title = textOf(payload["title"]);
  const rawLines = payload["lines"];
  const rawArgs = payload["args"];
  const rawMissing = payload["missing"];
  const confirmable = payload["confirmable"];
  if (verb === null || title === null || !Array.isArray(rawLines) || !Array.isArray(rawMissing)
      || typeof confirmable !== "boolean") {
    return null;
  }
  const lines: string[] = [];
  for (const rawLine of rawLines) {
    const line = textOf(rawLine);
    if (line === null) return null;
    lines.push(line);
  }
  const missing: string[] = [];
  for (const rawEntry of rawMissing) {
    const entry = textOf(rawEntry);
    if (entry === null) return null;
    missing.push(entry);
  }
  const argsRecord = recordOf(rawArgs);
  if (argsRecord === null) return null;
  const args: Record<string, string> = {};
  for (const [key, value] of Object.entries(argsRecord)) {
    if (typeof value !== "string") return null;
    args[key] = value;
  }
  return { kind: "card", verb, title, lines, args, missing, confirmable };
}

/** The chat route's whole answer, or `null` when any part of it cannot be read. NEVER a
 *  partial view and NEVER throws: `available` false becomes the unavailable kind with its
 *  reason; `available` true becomes an answer or a card only when every key of the view is
 *  present with its own type, the evidence is numbered 1 to n in order, every citation is an
 *  integer from 1 to n, at least one sentence exists, and every card argument is a string. */
export function decodeChatTurn(raw: unknown): ChatTurnView | null {
  const payload = recordOf(raw);
  if (payload === null) return null;
  const available = payload["available"];
  if (typeof available !== "boolean") return null;
  if (!available) {
    const reason = textOf(payload["reason"]);
    return reason === null ? null : { kind: "unavailable", reason };
  }
  const kind = payload["kind"];
  if (kind === CHAT_TURN_ANSWER_KIND) return chatAnswerViewOf(payload);
  if (kind === CHAT_TURN_CARD_KIND) return chatCardViewOf(payload);
  return null;
}

/** The job's chat route, with the token the cockpit already carries and the line to ask. No
 *  `task` parameter when `taskId` is `""`, which the route reads as the project scope. */
export function chatTurnPath(request: {
  jobId: string; token: string; text: string; taskId: string; baseUrl?: string;
}): string {
  const base = request.baseUrl ?? "";
  let path = `${base}/api/jobs/${encodeURIComponent(request.jobId)}/chat`
    + `?token=${encodeURIComponent(request.token)}`
    + `&text=${encodeURIComponent(request.text)}`;
  if (request.taskId !== "") {
    path += `&task=${encodeURIComponent(request.taskId)}`;
  }
  return path;
}

/** One `[n]` citation marker, with the space before it, so `chatSentenceText` can drop it. */
const CITATION_MARKER_RE = / ?\[\d+\]/g;

/** A sentence's text with every inline `[n]` citation marker removed: the chips beside it
 *  carry those numbers instead, so the words never say a number twice. */
export function chatSentenceText(sentence: ChatAnswerSentenceView): string {
  return sentence.text.replace(CITATION_MARKER_RE, "");
}

/** The three marks a sentence can carry: `cited` when it is supported by a citation,
 *  `absence` only for `CHAT_NOT_IN_EVIDENCE` with none, and `unsupported` otherwise —
 *  including a sentence that cites something but is not itself supported. */
export function chatSentenceMark(sentence: ChatAnswerSentenceView): "cited" | "unsupported" | "absence" {
  if (!sentence.supported) return "unsupported";
  if (sentence.citations.length > 0) return "cited";
  if (sentence.text === CHAT_NOT_IN_EVIDENCE) return "absence";
  return "unsupported";
}

/** The sentence the scope chip shows: the focused task, the registered project, or that no
 *  project is registered — `subject` is `""` exactly when `run_chat_turn` found no project
 *  owning the job's repository. */
export function chatScopeLabel(answer: ChatAnswerView): string {
  if (answer.scope === "node") return `About task ${answer.subject}`;
  if (answer.subject === "") return "No project is registered for this job.";
  return `About project ${answer.subject}`;
}

/** Which existing tab an evidence item opens: `diff` for a diff item, `prompt` for a prompt
 *  item, `null` for every other kind, which the tab renders as plain text. */
export function chatEvidenceTab(kind: string): "diff" | "prompt" | null {
  if (kind === "diff") return "diff";
  if (kind === "prompt") return "prompt";
  return null;
}

/** THE BUILDER: an addressed job with its token, one card and a caller-supplied nonce become
 *  the exact request the commands endpoint accepts, or `null` whenever that request would be
 *  UNSENDABLE — an empty job id or token, a card that is not confirmable, a card with a
 *  `missing` entry, an empty verb, or a nonce outside the server's class. */
export function buildChatCardSendRequest(
  target: DecisionSendTarget,
  card: ChatCardView,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "" || target.serverToken === "" || !card.confirmable
      || card.missing.length > 0 || card.verb === "" || !isUsableCommandNonce(clientNonce)) {
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
    body: JSON.stringify({ command: card.verb, client_nonce: clientNonce, args: card.args }),
  };
}

/** THE MAPPING: one card send's result becomes the one thing to say about it. `accepted`
 *  names the verb that was sent; every refusal and the unreachable outcome reuse
 *  `describeDecisionSubmitResult`'s own sentence rather than a second copy of it, because
 *  both doors are the same commands endpoint answering the same statuses. */
export function describeChatCardResult(result: DecisionSubmitResult, verb: string): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return { tone: "ok", sentence: `Sent: ${verb}.` };
  }
  return describeDecisionSubmitResult(result);
}

/** The card that never reached the wire: no nonce could be minted, or the builder refused the
 *  request outright. `warn`, because the operator can still press Confirm again. */
export function describeUnsendableChatCard(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: "This card cannot be sent as it stands." };
}

/** Every seam optional and defaulting to the shipped function, `SteeringSendDeps`'s own shape
 *  restated over a card send. */
export interface ChatCardSendDeps {
  mintNonce?: () => string | null;
  submit?: (request: DecisionSendRequest) => Promise<DecisionSubmitResult>;
}

/** THE FLOW: mint, build, submit once and describe, stopping at the first step that answers
 *  `null`. Neither `null` path touches the network. */
export async function sendChatCard(
  target: DecisionSendTarget,
  card: ChatCardView,
  deps: ChatCardSendDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const submit = deps.submit ?? ((request) => submitDecisionSendRequest(request));

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendableChatCard();
  }
  const request = buildChatCardSendRequest(target, card, clientNonce);
  if (request === null) {
    return describeUnsendableChatCard();
  }
  const result = await submit(request);
  return describeChatCardResult(result, card.verb);
}

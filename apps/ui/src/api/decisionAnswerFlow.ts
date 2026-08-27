// ONE ANSWER, END TO END: the single place the decision inbox's four T003
// modules are sequenced, and the only module in this chain that creates a timer
// (T5_F031 T003). `decisionNonce.ts` mints, `decisionSend.ts` builds,
// `decisionSubmit.ts` sends and `decisionOutcome.ts` says what happened — each
// of them pure or single-purpose, none of them aware of the others' refusals.
// This module owns the ORDER and nothing else, so a click handler calls one
// function and renders one sentence. DECISION F031 D5 rules the logic into this
// layer: the shipped vitest config collects `src/**/*.test.ts` only and no DOM
// harness exists, so a sequence written inside a component would ship untested.
//
// EVERY DEPENDENCY IS AN INJECTED SEAM WITH A DEFAULT. A caller passes nothing
// and gets the shipped chain; a test passes everything and touches no global —
// no test under `apps/ui/src` patches one today, and a leaked global is a
// failure that surfaces in an unrelated file. That is the same shape DECISION
// F031 D16 fixed for the send and DECISION F031 D17 for the nonce.
//
// THE DEADLINE IS THE ONLY CLOCK IN THE CHAIN, and DECISION F031 D18 rules it.
// `submitDecisionSendRequest` sets no timeout by design, and `decisionAnswer.ts`,
// `decisionSend.ts` and `decisionNonce.ts` each state in their own headers that
// they read no clock, so a send that never settles had no bound anywhere. The
// bound lands here, behind one seam, which is what keeps every other module's
// no-clock claim true. When the deadline wins, the flow answers the message for
// an `unreachable` result at the status `decisionSubmit.ts` fixes for "no
// response": from the operator's seat "we never heard back" and "we could not
// reach it" are one sentence, so no fourth outcome was invented to say it.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// THE SEND IS NOT CANCELLED WHEN THE DEADLINE WINS. The flow stops WAITING; the
// request may still arrive and still be written. There is no `AbortController`
// here, because aborting would promise a withdrawal the server never agreed to,
// and judging when a write may be abandoned belongs to whoever knows what the
// write meant — which is not this layer.
// IT NEVER RETRIES. One mint, one build, one send. The operator decides whether
// to send again, and the sentence they read tells them whether that could help.
// IT NEVER THROWS AND ALWAYS ANSWERS A MESSAGE, including for a seam that
// rejects: a promise that rejects inside a click handler is an unhandled
// rejection and a card that renders nothing.
// IT OPENS NO SOCKET OF ITS OWN and touches no storage. The network is reached
// only through the injected submit, which is still `decisionSubmit.ts`.
// IT RENDERS NOTHING AND KNOWS NO COMPONENT. It answers a value; the card that
// shows it is `DecisionInboxCard.tsx`.
// IT NEITHER READS NOR VALIDATES THE CLARIFICATION ANSWERS. The map is DATA
// this module forwards to the builder and nothing more: it is not trimmed, not
// filtered against blanks, not checked against the card's own questions. Every
// refusal it can earn belongs to `decisionAnswer.ts`, which is where the
// `answers` key of the args is built, so a reader looking here for that rule is
// looking one module too far down the chain. DECISION F031 D26 rules the form.
import type { DecisionCardModel } from "./decisionCard";
import { mintDecisionClientNonce } from "./decisionNonce";
import { buildDecisionSendRequest } from "./decisionSend";
import type { DecisionSendRequest, DecisionSendTarget } from "./decisionSend";
import { submitDecisionSendRequest } from "./decisionSubmit";
import type { DecisionSubmitResult } from "./decisionSubmit";
import {
  describeDecisionSubmitResult,
  describeUnsendableDecisionAnswer,
} from "./decisionOutcome";
import type { DecisionOutcomeMessage } from "./decisionOutcome";

/** How long one answer may stay unanswered before the operator is told nothing
 *  came back, in milliseconds. It is generous on purpose: this bound exists so a
 *  button cannot stay disabled forever, not to second-guess a slow run. */
const ANSWER_DEADLINE_MS = 20000;

/** The status `decisionSubmit.ts` fixes as the one number no door answers, so a
 *  deadline win reuses that module's closed vocabulary instead of adding to it. */
const NO_RESPONSE_STATUS = 0;

/** What the race answers when the DEADLINE got there first. A named sentinel
 *  rather than a bare `null` at the comparison, so the branch below reads as the
 *  question it asks. */
const DEADLINE_REACHED = null;

/** THE FOUR SEAMS, every one optional and every one defaulting to the shipped
 *  function, so `answerDecisionCard(target, model, text)` is the whole call at a
 *  click site and a test can replace any subset. */
export interface DecisionAnswerFlowDeps {
  /** Mints the client nonce, or answers `null` when none can be built. */
  mintNonce?: () => string | null;
  /** Builds the request, or answers `null` when the answer is unsendable. */
  buildRequest?: (
    target: DecisionSendTarget,
    model: DecisionCardModel,
    answerText: string,
    clientNonce: string,
    clarificationAnswers?: Record<string, string>,
  ) => DecisionSendRequest | null;
  /** The one call that crosses the wire. */
  submit?: (request: DecisionSendRequest) => Promise<DecisionSubmitResult>;
  /** Answers a promise that settles when the wait is over. The default below is
   *  the ONLY place in this chain where a timer is created. */
  deadline?: () => Promise<void>;
}

/** The default deadline: one timer, created here and nowhere else. It is not
 *  cleared when the submit wins — the promise it settles is simply one nobody is
 *  listening to any more, and a seam that answers a promise has no handle to
 *  cancel. */
function waitForDefaultDeadline(): Promise<void> {
  return new Promise((settle) => {
    setTimeout(settle, ANSWER_DEADLINE_MS);
  });
}

/** THE FLOW: mint, build, send, and say what happened — in that order, and
 *  stopping at the first step that answers `null`. Neither `null` path touches
 *  the network, which is the whole reason the refusals live one round trip
 *  earlier than the door. The clarification answers are DATA and the deps are
 *  SEAMS, so the data sits BEFORE the seams — the same order
 *  `buildDecisionResolveCommand` already uses, and the one that keeps
 *  `answerDecisionCard(target, model, text)` the whole call at a click site. */
export async function answerDecisionCard(
  target: DecisionSendTarget,
  model: DecisionCardModel,
  answerText: string,
  clarificationAnswers?: Record<string, string>,
  deps: DecisionAnswerFlowDeps = {},
): Promise<DecisionOutcomeMessage> {
  const mintNonce = deps.mintNonce ?? mintDecisionClientNonce;
  const buildRequest = deps.buildRequest ?? buildDecisionSendRequest;
  const submit = deps.submit ?? ((request) => submitDecisionSendRequest(request));
  const deadline = deps.deadline ?? waitForDefaultDeadline;

  const clientNonce = mintNonce();
  if (clientNonce === null) {
    return describeUnsendableDecisionAnswer();
  }
  const request = buildRequest(target, model, answerText, clientNonce, clarificationAnswers);
  if (request === null) {
    return describeUnsendableDecisionAnswer();
  }

  try {
    // The race BOUNDS THE WAIT, not the request: the send is still in flight
    // when the deadline wins, and nothing here withdraws it.
    const sent = submit(request);
    const settled = await Promise.race([sent, deadline().then(() => DEADLINE_REACHED)]);
    if (settled === DEADLINE_REACHED) {
      return describeDecisionSubmitResult({
        outcome: "unreachable",
        status: NO_RESPONSE_STATUS,
      });
    }
    return describeDecisionSubmitResult(settled);
  } catch {
    // `submitDecisionSendRequest` never rejects, but a seam a caller injects
    // might, and a click handler must still get a sentence rather than an
    // unhandled rejection.
    return describeDecisionSubmitResult({
      outcome: "unreachable",
      status: NO_RESPONSE_STATUS,
    });
  }
}

// The decision inbox's OUTCOME SENTENCE: every word an operator reads about an
// answer they already sent, and nothing else (T5_F031 T003). It is the last PURE
// step of the answer chain — `decisionAnswer.ts` builds the body,
// `decisionNonce.ts` mints the nonce, `decisionSend.ts` builds the request,
// `decisionSubmit.ts` moves it, and this module turns what came back into one
// tone and one sentence a card renders without a branch of its own. DECISION
// F031 D5 rules that split: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so a sentence chosen inside
// a click handler would ship untested.
//
// THE TONE IS NOT THE OUTCOME RESTATED. `decisionSubmit.ts` answers WHAT
// happened; the tone answers WHETHER SENDING AGAIN COULD PLAUSIBLY HELP, which
// is the only question the operator actually has in front of them. A
// rate-limited refusal and a rejected credential are both `refused` there, and
// are `warn` and `error` here.
//
// THE STATUS IS READ AS A NAME, NEVER AS A NUMBER. Each status named below is
// one `packages/orchestration/ui_server.py` really answers, listed in
// `decisionSubmit.ts`'s own header. There is no range arithmetic and no
// server-error branch, so a status that door never sends cannot acquire a
// confident sentence by accident: it takes the one sentence that admits the
// refusal was not recognised.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// NO INPUT MAKES IT THROW. Every function here is total over the type it takes,
// because a sentence chooser that throws inside a click handler leaves a card
// with nothing at all to say.
// IT READS NO CLOCK, OPENS NO SOCKET, STORES NOTHING AND MINTS NOTHING. No
// sentence names an elapsed time, no retry is scheduled, and no earlier send is
// remembered: an answer here is a function of one result and of nothing else.
// NO SENTENCE CARRIES A STATUS NUMBER, A HEADER NAME OR A URL. The number rides
// in the `DecisionSubmitResult` the caller already holds, and a sentence that
// leaked it would turn a card into a console.
// IT DOES NOT DECIDE WHAT TO RENDER. Colour, icon and placement belong to the
// component; this module hands it a tone to key off and a sentence to show.
import type { DecisionSubmitResult } from "./decisionSubmit";

/** HOW LOUD THE CARD SHOULD BE, as a closed union rather than a boolean pair, so
 *  a component keys off one value. `ok` is the door accepting; `warn` is a state
 *  where sending again could plausibly help; `error` is one where it could not,
 *  and the sentence names what would. */
export type DecisionOutcomeTone = "ok" | "warn" | "error";

/** ONE THING TO SAY ABOUT ONE SENT ANSWER: the tone a card keys off and the
 *  sentence it shows. Both fields are plain values, so a component projects them
 *  and branches on nothing. */
export interface DecisionOutcomeMessage {
  tone: DecisionOutcomeTone;
  sentence: string;
}

/** The statuses `packages/orchestration/ui_server.py` really answers on this
 *  door, named one by one because this module reads a status as a NAME. Nothing
 *  below compares, ranges over or does arithmetic on these numbers. */
const REFUSED_MALFORMED_STATUS = 400;
const REFUSED_CREDENTIAL_STATUS = 403;
const REFUSED_CLOSED_STATUS = 409;
const REFUSED_RATE_LIMITED_STATUS = 429;
const REFUSED_UNDISPATCHED_STATUS = 501;

/** THE WHOLE VOCABULARY, in one place, as the constants
 *  `DecisionInboxCard.tsx` keeps its own labels in. Every sentence is the
 *  OPERATOR'S: it says what became of their answer and, where that is true,
 *  what they can do next. */
const ACCEPTED_SENTENCE = "Your answer was recorded.";
const UNREACHABLE_SENTENCE =
  "No answer came back, so this may not have reached the run. You can send it again.";
const RATE_LIMITED_SENTENCE =
  "Too many answers arrived at once. Wait a moment, then send this one again.";
const CREDENTIAL_SENTENCE =
  "This dashboard was not allowed to answer, so nothing was recorded. Open the dashboard again from a fresh link.";
const MALFORMED_SENTENCE = "The run could not read this answer, so nothing was recorded.";
const CLOSED_SENTENCE =
  "This decision is no longer open. It may already have been answered.";
const UNDISPATCHED_SENTENCE = "This run cannot take answers from the dashboard.";
const UNRECOGNISED_REFUSAL_SENTENCE =
  "The run refused this answer, so nothing was recorded.";
const UNSENDABLE_SENTENCE =
  "This answer cannot be sent as it stands. Check it, then try again.";

/** What a REFUSAL means, chosen by the status alone. `default` is the honest
 *  branch: an unlisted status is a refusal this browser cannot name, so it gets
 *  the sentence that claims nothing about which refusal it was. */
function describeRefusedStatus(status: number): DecisionOutcomeMessage {
  switch (status) {
    case REFUSED_RATE_LIMITED_STATUS:
      return { tone: "warn", sentence: RATE_LIMITED_SENTENCE };
    case REFUSED_CREDENTIAL_STATUS:
      return { tone: "error", sentence: CREDENTIAL_SENTENCE };
    case REFUSED_MALFORMED_STATUS:
      return { tone: "error", sentence: MALFORMED_SENTENCE };
    case REFUSED_CLOSED_STATUS:
      return { tone: "error", sentence: CLOSED_SENTENCE };
    case REFUSED_UNDISPATCHED_STATUS:
      return { tone: "error", sentence: UNDISPATCHED_SENTENCE };
    default:
      return { tone: "error", sentence: UNRECOGNISED_REFUSAL_SENTENCE };
  }
}

/** THE MAPPING: one send's closed result becomes the one thing to say about it.
 *  A FRESH OBJECT every call, never a shared constant, so no caller can mutate
 *  the vocabulary for every other caller. */
export function describeDecisionSubmitResult(
  result: DecisionSubmitResult,
): DecisionOutcomeMessage {
  if (result.outcome === "accepted") {
    return { tone: "ok", sentence: ACCEPTED_SENTENCE };
  }
  if (result.outcome === "unreachable") {
    // Nothing was heard back, so nobody knows whether the request arrived —
    // which is exactly the state where sending again is worth trying.
    return { tone: "warn", sentence: UNREACHABLE_SENTENCE };
  }
  return describeRefusedStatus(result.status);
}

/** THE ANSWER THAT NEVER REACHED THE WIRE, which has no `DecisionSubmitResult`
 *  to map: `mintDecisionClientNonce` or `buildDecisionSendRequest` answered
 *  `null` and nothing was sent. It lives here rather than as a fourth member of
 *  `decisionSubmit.ts`'s closed outcome union, because that union describes what
 *  a door answered and this case never reached a door. `warn`, because the
 *  operator can edit what they typed and send again. A FRESH OBJECT, for the
 *  reason above. */
export function describeUnsendableDecisionAnswer(): DecisionOutcomeMessage {
  return { tone: "warn", sentence: UNSENDABLE_SENTENCE };
}

// The decision inbox's ONE NETWORK CALL, alone in its own module (T5_F031
// T003). It takes the request `decisionSend.ts` already built AS A VALUE, sends
// it exactly once, and answers a closed three-value result. Nothing else in this
// feature opens a socket, and this module is the whole of what "impure" means
// here. DECISION F031 D16 rules its shape; DECISION F031 D5 is why the edge is a
// module with an injected send rather than a `fetch` call inside a component —
// the shipped vitest config reaches this file and reaches no component, so a
// mapping that lived in a click handler would ship untested.
//
// THE RESULT IS A VOCABULARY, NOT A RESPONSE. A caller learns three things and
// no more: the door ACCEPTED the answer, REFUSED it, or could not be REACHED.
// The numeric status rides beside the outcome so a card can say WHICH refusal.
// `packages/orchestration/ui_server.py` answers 403 for a bad token and for a
// bad double-submit header, 400 for a malformed body, 409 when the decision is
// absent or no longer open, 429 over the rate budget, 501 for an id it does not
// dispatch, and 200 on success — a credential problem and a stale decision are
// different sentences on a card, and only the status tells them apart. A
// `Response` is deliberately NOT handed out: this feature has no use for a body,
// and returning one would invite a caller to read one.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT NEVER THROWS. A rejected send — offline, a refused connection, an aborted
// request — becomes the unreachable result, because a promise that rejects
// inside a click handler is an unhandled rejection and a card that renders
// nothing.
// IT NEVER RETRIES. One attempt. Judging when replaying a write is safe belongs
// to whoever knows what the write meant, and that is not this module.
// IT SETS NO TIMEOUT, reads no clock, and mints no nonce: the request arrives
// complete, and this module adds no header, no credential and no query to it.
// IT KNOWS NOTHING ABOUT WHAT A DECISION IS. It moves a request and reports what
// came back; every rule about cards, answers and open state stays one layer up.
import type { DecisionSendRequest } from "./decisionSend";

/** EXACTLY WHAT THIS MODULE READS BACK off a sent request, declared as its own
 *  narrow type on purpose. Naming the DOM `Response` here would drag a body, a
 *  header map and a stream into a seam that reads two fields, and would force
 *  every test to construct one. The global `fetch` satisfies this structurally,
 *  so the default below is an adapter over the request's four values and nothing
 *  more. */
export interface DecisionSendReply {
  ok: boolean;
  status: number;
}

/** THE TESTING SEAM: the one function that actually touches the network, passed
 *  IN rather than reached for. A test supplies its own and never patches a
 *  global — no test under `apps/ui/src` patches one today, and a leaked global is
 *  a failure that surfaces in an unrelated file. */
export type DecisionSendFunction = (
  request: DecisionSendRequest,
) => Promise<DecisionSendReply>;

/** THE THREE OUTCOMES, as a union of string literals rather than a pair of
 *  booleans, so a fourth can be added without changing anyone's arity and so no
 *  caller has to decode a flag combination. */
export type DecisionSubmitOutcome = "accepted" | "refused" | "unreachable";

/** ONE SEND'S ANSWER: what happened, and the status that says which refusal it
 *  was. `status` is 0 exactly when the outcome is `unreachable`, because there
 *  was no response and 0 is the one number no door answers. */
export interface DecisionSubmitResult {
  outcome: DecisionSubmitOutcome;
  status: number;
}

/** THE SUBMIT: send one already-built request, once, and map what comes back to
 *  the closed result. The send function defaults to the global `fetch` and is a
 *  parameter so that a test can pass its own without touching a global. */
export async function submitDecisionSendRequest(
  request: DecisionSendRequest,
  send: DecisionSendFunction = (sent) =>
    fetch(sent.path, { method: sent.method, headers: sent.headers, body: sent.body }),
): Promise<DecisionSubmitResult> {
  try {
    const reply = await send(request);
    // A refusal and a success are BOTH answers and neither throws, so the
    // door's own verdict is the only thing that separates them.
    return { outcome: reply.ok ? "accepted" : "refused", status: reply.status };
  } catch {
    return { outcome: "unreachable", status: 0 };
  }
}

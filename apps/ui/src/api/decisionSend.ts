// The decision inbox's SEND REQUEST, as ONE PURE function over the command body
// `decisionAnswer.ts` already builds (T5_F031 T003). It turns a job's identity
// and its per-run token, a card, the answer the operator chose and a
// caller-supplied nonce into the exact request `/api/jobs/<job_id>/commands`
// accepts — as a VALUE, never as a call. DECISION F031 D5 rules F031's logic
// into this layer, and DECISION F031 D13 rules the credential this module
// spends.
//
// IT COMPOSES, IT DOES NOT RE-DERIVE. The body is whatever
// `buildDecisionResolveCommand` answers, serialised; the path is whatever
// `jobCommandsPath` answers. Both come from `./decisionAnswer`, so the four
// refusals that door would answer 400 or 409 stay defined in exactly ONE place
// and this module adds only the two a missing credential earns.
//
// THE TWO TOKEN HEADERS CARRY ONE SECRET, NOT TWO. In
// `packages/orchestration/ui_server.py` the bearer check and the double-submit
// check both compare against the same `self.server_token`, and DECISION F009
// D11 rules that the double-submit header carries the server token ITSELF,
// because there is no cookie to double-submit against. A reader looking here
// for a second, distinct CSRF secret is looking for something Remedy
// deliberately does not mint. The browser has held that one token since F008:
// `RemedyApp` reads it out of the URL and refuses to render without it.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. This module opens no socket and
// calls no `fetch` — the caller issues the request and therefore owns the
// ORIGIN this path is resolved against. It mints no nonce and reads no clock,
// exactly as `decisionAnswer.ts` does not: the caller supplies both, which is
// what keeps every answer here a value a test can assert. It retries nothing,
// stores nothing and logs nothing. The token reaches the request through the
// headers ALONE — never in the path and never in a query string, because a
// query string is the part of a URL that reaches logs.
import type { DecisionCardModel } from "./decisionCard";
import { buildDecisionResolveCommand, jobCommandsPath } from "./decisionAnswer";

/** One HTTP request, flattened into exactly the four values a caller hands to
 *  the browser's own request function: a path with no origin, a method, a
 *  COMPLETE header map, and a body already serialised. Every field is a plain
 *  string, so a test can compare the whole request rather than inspect an
 *  opaque request object it would first have to construct. */
export interface DecisionSendRequest {
  path: string;
  method: "POST";
  headers: Record<string, string>;
  body: string;
}

/** THE BUILDER: a job, its token, one card, one answer and one caller-supplied
 *  nonce become the exact request the commands endpoint accepts — or `null`
 *  whenever that request would be UNSENDABLE. It answers `null` for the four
 *  bodies `buildDecisionResolveCommand` already refuses, and for two more of
 *  its own: an empty job id addresses no job, and an empty token is a request
 *  the door answers 403. Both are refused one round trip earlier, where the
 *  operator is still looking. */
export function buildDecisionSendRequest(
  jobId: string,
  serverToken: string,
  model: DecisionCardModel,
  answerText: string,
  clientNonce: string,
): DecisionSendRequest | null {
  if (jobId === "") {
    return null;
  }
  if (serverToken === "") {
    return null;
  }
  const commandBody = buildDecisionResolveCommand(model, answerText, clientNonce);
  if (commandBody === null) {
    return null;
  }
  return {
    path: jobCommandsPath(jobId),
    method: "POST",
    headers: {
      Authorization: `Bearer ${serverToken}`,
      "X-Remedy-CSRF": serverToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(commandBody),
  };
}

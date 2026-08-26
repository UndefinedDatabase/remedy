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
// `jobCommandsPath` answers. Both come from `./decisionAnswer`, so every refusal
// that door owes — a card with no id, a blank answer, a nonce outside the
// server's class, a decision that is not open — stays defined in exactly ONE
// place, NAMED rather than counted so the sentence cannot go stale, and this
// module adds only what a missing credential earns.
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

/** THE ADDRESSED JOB AND THE CREDENTIAL THAT OPENS ITS DOOR, as ONE value with
 *  NAMED fields. They travelled as two adjacent bare `string` parameters until
 *  finding R-0684: both are opaque ids of the same type, so transposing them at
 *  a call site type-checked, and the swap spent the token as the job id — which
 *  writes the credential into the request PATH, the one thing this module's
 *  header forbids. Named fields make that transposition inexpressible, which is
 *  AGENTS.md's "use distinct ID/value types where an argument swap is plausible"
 *  applied at the cheapest moment: before the first call site exists. */
export interface DecisionSendTarget {
  jobId: string;
  serverToken: string;
}

/** THE BUILDER: an addressed job with its token, one card, one answer and one
 *  caller-supplied nonce become the exact request the commands endpoint accepts
 *  — or `null` whenever that request would be UNSENDABLE. It answers `null` for
 *  every body `buildDecisionResolveCommand` already refuses, and for what a
 *  missing credential earns it: an empty job id addresses no job, and an empty
 *  token is a request the door answers 403. Both are refused one round trip
 *  earlier, where the operator is still looking. */
export function buildDecisionSendRequest(
  target: DecisionSendTarget,
  model: DecisionCardModel,
  answerText: string,
  clientNonce: string,
): DecisionSendRequest | null {
  if (target.jobId === "") {
    return null;
  }
  if (target.serverToken === "") {
    return null;
  }
  const commandBody = buildDecisionResolveCommand(model, answerText, clientNonce);
  if (commandBody === null) {
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
    body: JSON.stringify(commandBody),
  };
}

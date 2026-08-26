// The decision inbox's ANSWER COMMAND, as PURE functions over the models
// `decisionCard.ts` builds (T5_F031 T003). It turns a card plus the answer the
// operator chose into the exact request body `/api/jobs/<job_id>/commands`
// already accepts, and returns `null` for the four bodies that door would refuse
// anyway — refused one round trip earlier, where the operator is still looking.
//
// DECISION F031 D5 rules F031's logic into this layer: the shipped vitest config
// collects `src/**/*.test.ts` only and no DOM harness exists, so everything that
// can be a value is made one and the untested remainder shrinks to the call that
// crosses the wire. DECISION F031 D11 rules that split.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. This module does NOT issue the
// request: it opens no socket, and the sender round owns that call. It does NOT
// mint the nonce either — the caller supplies one, which is precisely what keeps
// this module free of a clock, of a random source and of any injection seam, so
// every one of its answers is a value a test can assert. It reads no clock at
// all. A reader searching this file for a request, a retry, a header or a token
// is searching for something this module refuses to have.
//
// THE DUPLICATION IS DELIBERATE AND IS NOT AN AUTHORITY. Every refusal below is
// a SECOND copy of a rule `packages/orchestration/ui_server.py` already
// enforces. The server's check stays the only authority; this one exists to
// spare the operator a round trip, never to replace it.
import type { DecisionCardModel } from "./decisionCard";

/** The command id the server routes a decision answer by, in the server's OWN
 *  spelling — `DECISION_RESOLVE_COMMAND_ID` in `ui_server.py`. DECISION F031 D1
 *  rules that the browser and the CLI describe one thing one way, so the literal
 *  is not renamed on the way out. */
export const DECISION_RESOLVE_COMMAND_ID = "decision.resolve";

/** The nonce's character class, mirroring `safe_points._ID_RE` on the server —
 *  reached there through `nonce_is_valid` -> `is_safe_id`. It is a guard rather
 *  than a formality: the nonce becomes a FILENAME in the job's control
 *  directory, so a value outside this class is a path, not an id. */
const COMMAND_NONCE_PATTERN = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;

/** The `args` object the decision-resolve command carries, in the server's own
 *  key spellings: `_dispatch_decision_resolve` reads exactly these two and
 *  nothing else. Remedy deliberately does NOT send `source` here — DECISION F009
 *  D22 rules that omission, which lets the record take the `human` default;
 *  passing one would land it in neither tally. */
export interface DecisionResolveArgs {
  decision_id: string;
  answer: string;
}

/** The whole request body the commands endpoint accepts, in that endpoint's own
 *  key spellings — `_read_command_payload` requires a JSON object carrying
 *  exactly `command`, `client_nonce` and an optional `args` object. No key this
 *  interface names is invented, and it names no key the server does not read. */
export interface DecisionResolveCommandBody {
  command: string;
  client_nonce: string;
  args: DecisionResolveArgs;
}

/** Whether a candidate value is a nonce the commands endpoint would accept.
 *  Total over `unknown` on purpose: the candidate reaches this predicate from
 *  wherever the caller minted it, so a number, a null or an absent value is
 *  answered `false` rather than throwing. */
export function isUsableCommandNonce(candidate: unknown): boolean {
  return typeof candidate === "string" && COMMAND_NONCE_PATTERN.test(candidate);
}

/** Where a job's commands are posted, as a PATH and nothing more: no host, no
 *  query, one leading slash. The caller owns the origin and the token, so this
 *  function stays a value a test can compare with `toBe`. */
export function jobCommandsPath(jobId: string): string {
  return `/api/jobs/${jobId}/commands`;
}

/** THE BUILDER: one card, one answer and one caller-supplied nonce become the
 *  exact body the commands endpoint accepts — or `null`, for exactly four
 *  reasons, each of them a body the server would refuse anyway. The model has no
 *  `id`, so no record could match it; the answer text is empty, so the decision
 *  would resolve with nothing; the nonce is outside the class the server
 *  enforces; or the decision is NOT open, which the server answers 409 because
 *  the record is absent or already resolved. */
export function buildDecisionResolveCommand(
  model: DecisionCardModel,
  answerText: string,
  clientNonce: string,
): DecisionResolveCommandBody | null {
  if (model.id === "") {
    return null;
  }
  if (answerText === "") {
    return null;
  }
  if (!isUsableCommandNonce(clientNonce)) {
    return null;
  }
  if (!model.isOpen) {
    return null;
  }
  return {
    command: DECISION_RESOLVE_COMMAND_ID,
    client_nonce: clientNonce,
    args: {
      decision_id: model.id,
      answer: answerText,
    },
  };
}

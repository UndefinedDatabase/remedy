// The completion digest's CLIENT SEAM (T5_F040 T002). This is the browser half
// of the envelope `packages/orchestration/job_digest.py` composes and
// `GET /api/jobs/<job_id>/digest` serves: it DECODES that envelope, NAMES the
// endpoint's path, and turns the cost section into the hero card's cost line as
// a RULE rather than as copy. Every decidable behaviour of the card lives here
// so it can be tested without a renderer this repository does not have —
// DECISION F040 D7 rules that reading of "component tests", and the `.tsx` that
// comes later keeps only wiring.
//
// THE EXACTNESS STRING HAS ONE HOME AND THIS FILE IS NOT IT. `costMetric.ts`
// defines ACTUAL_BASIS and this module imports it, so the metrics bar and the
// hero card cannot disagree about what an exact figure is. A second copy of
// that literal here would be exactly the drift DECISION F040 D2 already spent a
// round preventing for the urgency formula, one layer up.
//
// THIS MODULE WRITES NO PRESENTATION COPY EITHER. `digestCostLine` answers a
// BOOLEAN, the way `costMetricOf` answers one; the marker and the phrase that
// render it live in `apps/ui/src/components/metrics/TopMetricsBar.tsx` as
// ESTIMATE_MARK and ESTIMATE_PHRASE, and the card reads them from there. Copying
// either one down here would be a second home for the words, which is the same
// defect as a second home for the basis, one layer up again.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK. Nothing here calls Date.now, constructs a date or measures
// elapsed time. The trigger rule that WILL need a clock — show the card at job
// end, or on the first open after an absence — is a later round and takes its
// `nowMs` as a parameter, the shape `recency.ts` established, so the rule stays
// testable without waiting and without faking time.
// IT KEEPS NO STORAGE. No localStorage key, no sessionStorage key, no
// module-level mutable, nothing remembered between calls. WHERE a dismissal
// persists is an open DECISION and is deliberately not answered here rather
// than answered by accident.
// IT OPENS NO SOCKET. No fetch, no XMLHttpRequest, no loader of any kind.
// `jobDigestPath` builds the URL and hands it back; whoever touches the wire
// does it elsewhere, the way `loadDiffEnvelope` sits beside `diffEnvelopePath`
// rather than inside it.
// IT MINTS NOTHING. No crypto, no id and no nonce of its own: every value the
// card shows is the server's, carried verbatim.
//
// `tests/ui_contracts/test_job_digest_card_contract.py` pins those four
// absences over this file's source, and `jobDigest.test.ts` pins the rules.
import { ACTUAL_BASIS } from "./costMetric";

/** The envelope version this client understands. A payload carrying any other
 *  number is not decoded at all: `job_digest.py` states that the eight-key set
 *  IS the contract and that a key added to it is a version bump, so a different
 *  version is a different contract rather than a superset of this one. */
export const JOB_DIGEST_VERSION = 1;

/** The cost figure and how EXACT it is (DECISION F040 D4). `value` is the
 *  server's own already-formatted text, carried verbatim — the backend is the
 *  single arithmetic home for money and this module re-derives nothing. `basis`
 *  is the exactness word, and the only one meaning "not an estimate" is the
 *  ACTUAL_BASIS imported above, never a literal restated here. */
export interface JobDigestCost {
  value: string;
  basis: string;
}

/** How much is still waiting for an answer. `peak_urgency` is the most urgent
 *  OPEN card's score on the decision inbox's own formula, computed on the
 *  server and never recomputed here. */
export interface JobDigestDecisions {
  open_count: number;
  peak_urgency: number;
}

/** The ONE call to action, taken verbatim from the run report's recommendation
 *  so the hero card and the report are incapable of disagreeing. `rule_id`
 *  names the RULE rather than carrying a link, because DECISION F040 D5 keeps
 *  routing out of the envelope: the client decides the affordance. */
export interface JobDigestPrimaryAction {
  label: string;
  rule_id: string;
}

/** The whole envelope. All eight keys are always present — the server builds
 *  them that way on purpose, so no reader has to branch on a missing one — and
 *  the field names are the wire's snake_case rather than the client's camel,
 *  the same choice `BudgetTickFigures` makes in `costMetric.ts`.
 *
 *  `ownership` ships EMPTY and that is DECISION F040 D3, not a bug: F035 owns
 *  the ownership sentences and is unbuilt, so the key is present and empty from
 *  the first version and F035 fills it without a version bump. */
export interface JobDigest {
  version: number;
  job_id: string;
  state: string;
  headline: string;
  cost: JobDigestCost;
  ownership: string[];
  decisions: JobDigestDecisions;
  primary_action: JobDigestPrimaryAction;
}

/** Read any value as an object. `null`, an array, a string, a number and
 *  `undefined` all read as the empty payload rather than throwing, which is how
 *  a missing section becomes a complete one full of absences. */
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

/** Read one value as a string, or the empty string. Nothing is coerced: a
 *  number stringified into a headline would be a sentence the server never
 *  wrote. */
function stringOf(value: unknown): string {
  return typeof value === "string" ? value : "";
}

/** Read one value as a usable non-negative finite count, or zero. A NaN, an
 *  infinity, a negative and a string all read as zero, because a fabricated
 *  count is worse than a missing one and this field is only ever a tally. */
function countOf(value: unknown): number {
  const usable = typeof value === "number" && Number.isFinite(value) && value >= 0;
  return usable ? (value as number) : 0;
}

/** Read the ownership section as the sentences it is meant to hold, dropping
 *  every entry that is not a string. A non-array reads as no sentences at all,
 *  which is the shape the server ships today. */
function sentencesOf(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((entry): entry is string => typeof entry === "string");
}

/** The defensive decode: one payload of unknown provenance becomes either a
 *  complete `JobDigest` or `null`, and never a half-shape a caller must check
 *  field by field. This is the answer `normalizePipeline` and
 *  `normalizePromptTrace` already give for their own payloads.
 *
 *  IT NEVER THROWS. Three refusals and three only — a payload that is not a
 *  plain object, a `version` that is not the one this client understands, and a
 *  `job_id` that is missing or not a string. Everything else is read leniently,
 *  because a card that renders "not recorded" is more useful than no card.
 *
 *  UNKNOWN EXTRA KEYS ARE IGNORED, NOT REJECTED. DECISION F040 D3's own
 *  reasoning is that an additive field needs no version bump, so a server that
 *  has learned a new key must still be readable by a client that has not.
 *
 *  AN EMPTY `job_id` IS DECODED rather than refused: `build_job_digest` really
 *  emits one for a job whose id was never recorded, and turning that legitimate
 *  envelope into "no digest at all" would hide the very state the digest exists
 *  to report. Missing and non-string are the refusals, exactly as ordered. */
export function decodeJobDigest(raw: unknown): JobDigest | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) {
    return null;
  }
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== JOB_DIGEST_VERSION) {
    return null;
  }
  const jobId = payload["job_id"];
  if (typeof jobId !== "string") {
    return null;
  }
  const cost = objectOf(payload["cost"]);
  const decisions = objectOf(payload["decisions"]);
  const action = objectOf(payload["primary_action"]);
  return {
    version: JOB_DIGEST_VERSION,
    job_id: jobId,
    state: stringOf(payload["state"]),
    headline: stringOf(payload["headline"]),
    cost: {
      value: stringOf(cost["value"]),
      basis: stringOf(cost["basis"]),
    },
    ownership: sentencesOf(payload["ownership"]),
    decisions: {
      open_count: countOf(decisions["open_count"]),
      peak_urgency: countOf(decisions["peak_urgency"]),
    },
    primary_action: {
      label: stringOf(action["label"]),
      rule_id: stringOf(action["rule_id"]),
    },
  };
}

/** The card's cost line, decided here so the component decides nothing.
 *
 *  `value` is the figure's own text, unchanged. The flag is TRUE for every
 *  basis that is not the imported ACTUAL_BASIS — an unknown word is not an
 *  actual, and the marker is cheap while a false claim of exactness is not,
 *  which is the same reading `isEstimated` applies in `costMetric.ts`.
 *
 *  It answers a BOOLEAN and no words. The component renders the marker and the
 *  phrase from the constants it already owns; see this module's header. */
export function digestCostLine(cost: JobDigestCost): { value: string; estimated: boolean } {
  return {
    value: cost.value,
    estimated: cost.basis !== ACTUAL_BASIS,
  };
}

/** The URL of one job's digest. PURE: no fetch, no state, no throw.
 *
 *  Built the way `diffEnvelopePath` builds the diff's, because the route sits
 *  in the same per-job handler dictionary in `packages/orchestration/ui_server.py`
 *  and is dispatched on the same segment positions. The job id and the token are
 *  percent-encoded for the two reasons that door already documents: an
 *  unencoded slash in the id would not be a bad request but a DIFFERENT route,
 *  and an `&` in the token would end the parameter and start another.
 *
 *  `baseUrl` is optional and absent means relative, so the browser addresses
 *  its own origin and a test can address a fixture server by naming one. */
export function jobDigestPath(request: { jobId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  const q = `token=${encodeURIComponent(request.token)}`;
  const job = encodeURIComponent(request.jobId);
  return `${base}/api/jobs/${job}/digest?${q}`;
}

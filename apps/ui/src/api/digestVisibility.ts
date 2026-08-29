// WHEN the completion digest's hero card appears, as a PURE TOTAL RULE over
// values that are handed to it (T5_F040 T002). `jobDigest.ts` is the browser
// half of the ENVELOPE; this module is the browser half of the TRIGGER, and the
// two are deliberately separate files: `recency.ts`, `actionClass.ts` and
// `feedFocus.ts` each own exactly one rule, and a trigger bolted onto a decoder
// would be a second concern in a module whose purity guard is already written.
//
// The feature file's Acceptance is "Dismissal persists; new activity re-arms",
// and its trigger rules say a terminal event while the UI is open shows the
// hero — dismissible, remembered per job — while a first open with activity
// since last-seen shows the hero for the most significant job. Each of those is
// ONE comparison, and both comparisons are here.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it.
// IT READS NO CLOCK. Nothing here calls Date.now, constructs a date or measures
// elapsed time. `nowMs` arrives as a parameter — the shape `recency.ts`
// established and `AgentNowCard.tsx` binds under the comment "The clock, bound
// HERE because this is the edge that has one" — so the trigger is testable
// without waiting and without faking time.
// IT KEEPS NO STORAGE. No localStorage key, no sessionStorage key, no
// module-level mutable, nothing remembered between calls. WHERE a dismissal
// persists is settled by DECISION F040 D8 — browser-local, keyed per job,
// reached only through the port declared below — and that port is DECLARED here
// and IMPLEMENTED at the edge. A module that reached for storage in this file
// could not be tested without faking a global, and no test under `apps/ui/src`
// patches one today.
// IT OPENS NO SOCKET. No fetch, no XMLHttpRequest, no loader: every value the
// rule needs is already in the caller's hands when it is called.
// IT MINTS NOTHING. No crypto, no id, no nonce; it reads the digest it is given
// and invents no part of it.
// IT WRITES NO PRESENTATION COPY. Not one user-facing sentence, and in
// particular neither of the two phrases the Acceptance audits. This rule answers
// a boolean and a `reason` the card branches on; the WORDS belong to the card,
// the same split `digestCostLine` and `TopMetricsBar.tsx` already make one layer
// down.
//
// `tests/ui_contracts/test_job_digest_card_contract.py` pins those absences over
// this file's source, and `digestVisibility.test.ts` pins the rules.
import type { JobDigest } from "./jobDigest";

/** The states in which the run has not begun. A hero card announcing a job that
 *  has not started would be the overclaiming the Acceptance's copy audit exists
 *  to prevent, so these VETO the card outright rather than merely failing the
 *  settled test. */
const NOT_YET_STARTED_STATES: readonly string[] = ["pending", "planned"];

/** The state in which the run is still working. It does not show on SETTLED
 *  grounds, but the absence rule may still show it: activity since the operator
 *  was last here is real news whether or not the run has finished. */
const IN_FLIGHT_STATES: readonly string[] = ["running"];

/** The states in which the run has come to rest and there is something to
 *  report. `paused` sits here rather than with `running` on purpose — a paused
 *  job is waiting for the operator, which is the most report-worthy rest of the
 *  four. */
const SETTLED_STATES: readonly string[] = ["paused", "completed", "failed", "cancelled"];

/** The THREE-WAY partition over `RunState`, plus the honest fourth answer for a
 *  word this client has never heard of. Two-way would be the real defect: read
 *  as "terminal means not running" it collapses the not-yet-started group into
 *  the settled one and announces a job that never began. */
type DigestStateClass = "not-yet-started" | "in-flight" | "settled" | "unknown";

/** Which of the four a state string belongs to. The seven members of `RunState`
 *  in `packages/core/models.py` are partitioned by the three tuples above; an
 *  UNKNOWN string falls through to `unknown` and is NOT treated as settled,
 *  because claiming a run finished on the strength of a word you cannot read is
 *  exactly the false claim this feature refuses everywhere else. */
function digestStateClass(state: string): DigestStateClass {
  if (NOT_YET_STARTED_STATES.includes(state)) {
    return "not-yet-started";
  }
  if (IN_FLIGHT_STATES.includes(state)) {
    return "in-flight";
  }
  if (SETTLED_STATES.includes(state)) {
    return "settled";
  }
  return "unknown";
}

/** The per-job remembered state: the instant a dismissal was made, or `null`
 *  for never dismissed. Named rather than left a bare `number | null` because
 *  four instants of that exact shape meet in this module and a swap between two
 *  of them would be silent — the objection DECISION F040 D2's own reasoning
 *  makes about restating a rule in a second place. */
export type DigestDismissal = number | null;

/** THE STORAGE PORT, DECLARED HERE AND IMPLEMENTED NOWHERE IN THIS FILE.
 *  DECISION F040 D8 rules that a dismissal persists browser-locally, keyed per
 *  job, and that the implementation is bound at the EDGE — the card — exactly as
 *  `AgentNowCard.tsx` binds the clock `recency.ts` refuses to read. A module
 *  that reached for real storage here could not be tested without faking a
 *  global, and keeping the port a type is what lets every rule below be a pure
 *  function of values. */
export interface DigestVisibilityPort {
  readDismissal(jobId: string): DigestDismissal;
  writeDismissal(jobId: string, dismissedAtMs: number): void;
}

/** WHY the card is or is not showing, from a CLOSED set of string literals. The
 *  card branches on this, so a typo must be a type error rather than a branch
 *  that silently never runs. */
export type DigestVisibilityReason =
  | "no-digest"
  | "dismissed"
  | "not-yet-started"
  | "settled"
  | "activity-since-last-seen"
  | "nothing-new";

/** What the rule answers: whether to show the hero card, and the reason it
 *  decided so. The reason is part of the answer and not a debug aid — a rule
 *  that shows for the wrong reason is a rule the card will branch on wrongly. */
export interface DigestVisibility {
  show: boolean;
  reason: DigestVisibilityReason;
}

/** Everything the rule needs, as VALUES, in one named-argument object. Every
 *  instant is `number | null` because absence is meaningful in each of them:
 *  never dismissed, never seen, nothing has happened yet. The digest is `null`
 *  when none has loaded, which is a state and not an error. */
export interface DigestVisibilityInput {
  digest: JobDigest | null;
  lastSeenMs: number | null;
  dismissedAtMs: DigestDismissal;
  latestActivityMs: number | null;
  nowMs: number;
}

/** THE RULE: total, pure, and it never throws. Every input combination answers,
 *  absences included — a missing stamp is a STATE here, not an error.
 *
 *  The ORDER of the questions is the rule:
 *  1. NO DIGEST NEVER SHOWS, whatever the instants say: there is nothing to put
 *     in the card.
 *  2. A DISMISSAL HOLDS until something NEWER than it happens. Activity strictly
 *     after the dismissal RE-ARMS the card; activity at exactly the dismissal
 *     instant does not, because that is activity the operator was already
 *     looking at when the card was dismissed. That single comparison IS the
 *     Acceptance clause "Dismissal persists; new activity re-arms".
 *  3. A NOT-YET-STARTED RUN VETOES the card. Nothing has happened to this job,
 *     so neither the settled route nor the absence route may announce it.
 *  4. A SETTLED RUN SHOWS, no dismissal being in force.
 *  5. ABSENCE: activity strictly after `lastSeenMs` shows. A `lastSeenMs` of
 *     `null` means never seen, so any activity at all shows. This is the route
 *     that stays open for `running` and for an unknown state — neither shows on
 *     settled grounds, and both may still carry news.
 *  6. NOTHING NEW is the DEFAULT and not a fallback a reader has to infer.
 *
 *  CLOCK SKEW IS ANSWERED BY NOT ASKING. `nowMs` is taken so the rule is total
 *  and so the card's edge has exactly one place to bind a clock, but no branch
 *  above compares any stamp against it: every comparison is between two stamps
 *  the same host took, the way `AgentNowCard.tsx` keeps `receivedAtMs` and its
 *  own `Date.now` on one clock. A `latestActivityMs` in the FUTURE relative to
 *  `nowMs` is therefore still activity and still shows the card. That is the
 *  posture `recency.ts` takes at its own skew comment: under disagreeing clocks
 *  the honest failure is to over-report life, never to declare a working agent
 *  dead. Showing a digest the operator can dismiss costs a click; hiding one
 *  costs the news. */
export function digestVisibility(input: DigestVisibilityInput): DigestVisibility {
  if (input.digest === null) {
    return { show: false, reason: "no-digest" };
  }
  const activityMs = input.latestActivityMs;
  const dismissedAtMs = input.dismissedAtMs;
  const reArmed = activityMs !== null && dismissedAtMs !== null && activityMs > dismissedAtMs;
  if (dismissedAtMs !== null && !reArmed) {
    return { show: false, reason: "dismissed" };
  }
  const stateClass = digestStateClass(input.digest.state);
  if (stateClass === "not-yet-started") {
    return { show: false, reason: "not-yet-started" };
  }
  if (stateClass === "settled") {
    return { show: true, reason: "settled" };
  }
  const lastSeenMs = input.lastSeenMs;
  if (activityMs !== null && (lastSeenMs === null || activityMs > lastSeenMs)) {
    return { show: true, reason: "activity-since-last-seen" };
  }
  return { show: false, reason: "nothing-new" };
}

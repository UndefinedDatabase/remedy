// The decision inbox's card MODEL, as PURE functions over the JSON that
// `/api/jobs/<job_id>/decisions` already returns (T5_F031 T002a). DECISION F031
// D5 rules F031's logic into this layer: the shipped vitest config collects
// `src/**/*.test.ts` only and no DOM harness exists, so every branch a card
// needs lives here and the `.tsx` that projects it stays a thin projection with
// no branching of its own.
//
// The architecture line is `decisionAnswers`. It derives a decision's
// affordances from the decision's OWN payload and never from its `type`, so a
// decision type this repository has not produced yet renders generically on the
// day some producer first emits it. Remedy deliberately does NOT keep a
// per-type form registry, a type-to-widget map, or any `switch` over a decision
// type here — a reader searching for one is searching for something this module
// refuses to have, and `decisionCard.test.ts` measures that refusal rather than
// trusting this comment.
//
// Remedy also deliberately does NOT sort or filter here, and a reader searching
// this file for either is told WHERE it lives rather than which future slice
// owns it: the ordering rule over age and blocked size is `./decisionOrder.ts`,
// the type filter is `./decisionFilter.ts`, and `decisionCardModels` preserves
// the endpoint's order exactly for both of them. COUNTING is neither absent nor
// elsewhere any more: `countOpenDecisions` at the foot of this module answers
// how many cards are still waiting, and the badge that shows that number is
// rendered by `../components/panels/DecisionInboxCard`. ANSWERING is not
// missing everywhere any more either: the command body an answer becomes is
// built by `./decisionAnswer.ts`. What is still genuinely absent is the SEND —
// nothing in this browser posts that body to the command endpoint yet, and that
// is T003's sender round. This module reads no clock either — an age arrives as
// the endpoint's own `age_seconds`, exactly as `recency.ts` takes `nowMs`.

/** What kind of affordance a card offers. `free_text` is the fallback the
 *  producer never has to ask for: a question is never shown without some way to
 *  answer it. */
export type DecisionAnswerKind = "option" | "command" | "free_text";

/** One answer affordance on a card. `label` is what the operator reads, `value`
 *  is what T003's write channel will later send back. */
export interface DecisionAnswer {
  kind: DecisionAnswerKind;
  label: string;
  value: string;
}

/** One decision card, flattened into exactly the fields a renderer projects.
 *  Every field is already a string or a number here, so the component that
 *  displays it needs no formatting rule and therefore no branch of its own. */
export interface DecisionCardModel {
  id: string;
  /** The id of the task this decision is about, taken from the payload's own
   *  `task_id`. The EMPTY STRING when the payload names none, so the deep-link
   *  resolver `./decisionFocus.ts` has a total input and no card has to test
   *  for `undefined`. */
  taskId: string;
  type: string;
  status: string;
  severity: string;
  title: string;
  ageLabel: string;
  /** The raw age the label above formats, carried so that a comparator has a
   *  NUMBER to order by — `orderDecisionInbox` needs one and a formatted label
   *  is not one. `null` is the endpoint's own answer for an unreadable stamp. */
  ageSeconds: number | null;
  blockedLabel: string;
  blockedCount: number;
  isOpen: boolean;
  answers: DecisionAnswer[];
}

/** One entry of the endpoint's `decisions` array, in the endpoint's OWN key
 *  spellings — `export_decision_json` plus the two keys `build_decision_inbox`
 *  adds. DECISION F031 D1 rules that the browser and the CLI describe one thing
 *  one way, so no key is renamed on the way in. Every field is optional and the
 *  untrusted ones are `unknown`, because the payload comes from a producer this
 *  module does not control and must still type-check. */
export interface DecisionInboxEntry {
  id?: string;
  type?: string;
  status?: string;
  severity?: string;
  safe_summary?: string;
  next_actions?: unknown;
  payload?: unknown;
  age_seconds?: number | null;
  blocked_count?: number;
}

/** The endpoint's inbox document. `decisions` is `unknown` for the same reason
 *  the card's payload is: `decisionCardModels` narrows it at runtime rather
 *  than trusting a producer to have sent an array. */
export interface DecisionInboxDocument {
  decisions?: unknown;
}

/** How long the question has been waiting, as the largest whole unit. A null
 *  age is the endpoint's own answer for an unreadable `created_at` stamp
 *  (`_decision_age_seconds` returns None there), and the card must still
 *  render, so this reports `unknown age` rather than inventing a number. */
export function decisionAgeLabel(ageSeconds: number | null): string {
  if (ageSeconds === null || !Number.isFinite(ageSeconds)) {
    return "unknown age";
  }
  // A negative age means the clocks disagree, not that the question is old. The
  // endpoint already clamps at 0; clamping again keeps this honest when the
  // function is called with a raw number rather than an endpoint one.
  const seconds = Math.max(0, Math.trunc(ageSeconds));
  if (seconds < 60) {
    return `${seconds}s`;
  }
  if (seconds < 3600) {
    return `${Math.trunc(seconds / 60)}m`;
  }
  if (seconds < 86400) {
    return `${Math.trunc(seconds / 3600)}h`;
  }
  return `${Math.trunc(seconds / 86400)}d`;
}

/** How much downstream work waits behind this decision. The singular is
 *  deliberate: "blocks 1 tasks" is the kind of detail that makes a surface look
 *  untended, and the inbox is meant to read as a calm place. */
export function decisionBlockedLabel(blockedCount: number): string {
  const count = Number.isFinite(blockedCount) ? Math.trunc(blockedCount) : 0;
  if (count <= 0) {
    return "blocks nothing";
  }
  if (count === 1) {
    return "blocks 1 task";
  }
  return `blocks ${count} tasks`;
}

/** The entries of a value that really is a non-empty array, else no entries. A
 *  missing, null or non-array value falls through here rather than throwing. */
function nonEmptyEntries(value: unknown): unknown[] {
  return Array.isArray(value) && value.length > 0 ? value : [];
}

/** `payload.options` when the payload is an object carrying it, else undefined.
 *  A missing, null or non-object payload is not an error: losing the question
 *  would be worse than showing an odd label. */
function payloadOptions(payload: unknown): unknown {
  if (typeof payload !== "object" || payload === null) {
    return undefined;
  }
  return (payload as { options?: unknown }).options;
}

/** `payload.task_id` when the payload is an object carrying it, else undefined.
 *  Same tolerance as `payloadOptions`: a missing, null or non-object payload is
 *  not an error, it is simply a decision with no task linkage. */
function payloadTaskId(payload: unknown): unknown {
  if (typeof payload !== "object" || payload === null) {
    return undefined;
  }
  return (payload as { task_id?: unknown }).task_id;
}

/** Entries rendered as answers of one kind. A non-string entry goes through
 *  `String` rather than being dropped, for the same reason. */
function entriesAsAnswers(entries: unknown[], kind: DecisionAnswerKind): DecisionAnswer[] {
  return entries.map((entry) => {
    const text = String(entry);
    return { kind, label: text, value: text };
  });
}

/** THE ARCHITECTURE LINE: the affordances a card offers, derived from the
 *  decision's own payload. Options win, then next actions, then a free-text
 *  answer. This function MUST NOT branch on `card.type` — the type is data
 *  here, never control flow — which is exactly what lets a decision type this
 *  repository has never produced render generically. */
export function decisionAnswers(card: DecisionInboxEntry): DecisionAnswer[] {
  const options = nonEmptyEntries(payloadOptions(card.payload));
  if (options.length > 0) {
    return entriesAsAnswers(options, "option");
  }
  const commands = nonEmptyEntries(card.next_actions);
  if (commands.length > 0) {
    return entriesAsAnswers(commands, "command");
  }
  return [{ kind: "free_text", label: "Answer", value: "" }];
}

/** A string field of the endpoint's card, or the empty string when it is absent
 *  or not a string, so no input makes the model throw. */
function cardText(value: unknown): string {
  return typeof value === "string" ? value : "";
}

/** One endpoint card as the model a renderer projects. Total by construction:
 *  every field has a fallback, so a half-written card still renders. */
export function buildDecisionCardModel(card: DecisionInboxEntry): DecisionCardModel {
  const blockedCount =
    typeof card.blocked_count === "number" && Number.isFinite(card.blocked_count)
      ? card.blocked_count
      : 0;
  const ageSeconds = typeof card.age_seconds === "number" ? card.age_seconds : null;
  return {
    id: cardText(card.id),
    // WHY here: the payload's `task_id` is the ONLY linkage on the wire from a
    // decision to the task it is about — `decision_inbox._blocked_subtree_size`
    // reads that same spelling on the server — and `./decisionFocus.ts` turns it
    // into the graph node the card jumps to.
    taskId: cardText(payloadTaskId(card.payload)),
    type: cardText(card.type),
    status: cardText(card.status),
    severity: cardText(card.severity),
    title: cardText(card.safe_summary),
    ageLabel: decisionAgeLabel(ageSeconds),
    ageSeconds,
    blockedLabel: decisionBlockedLabel(blockedCount),
    blockedCount,
    isOpen: card.status === "open",
    answers: decisionAnswers(card),
  };
}

/** Every card of one inbox document, in the order the endpoint sent them.
 *  Remedy deliberately imposes NO ordering here: the rule over age and blocked
 *  size lives in `./decisionOrder.ts`, and a model that quietly re-sorted would
 *  make that rule impossible to see. An absent or non-array `decisions` gives no
 *  cards. */
export function decisionCardModels(inbox: DecisionInboxDocument): DecisionCardModel[] {
  if (!Array.isArray(inbox.decisions)) {
    return [];
  }
  return inbox.decisions.map((card) => buildDecisionCardModel(card as DecisionInboxEntry));
}

/** How many of the inbox's cards are still waiting on an answer — the number the
 *  card header's badge shows. It reads each model's own `isOpen`, which
 *  `buildDecisionCardModel` already derived from the endpoint's `status`, so the
 *  status string is compared in exactly ONE place in this layer and a producer
 *  renaming it breaks one line rather than two. Total by construction: an empty
 *  inbox answers 0 and no input makes this throw. It counts and does nothing
 *  else — the order is `./decisionOrder.ts`'s and the type filter is
 *  `./decisionFilter.ts`'s. */
export function countOpenDecisions(models: readonly DecisionCardModel[]): number {
  return models.reduce((total, model) => (model.isOpen ? total + 1 : total), 0);
}

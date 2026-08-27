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
// built by `./decisionAnswer.ts`, and the SEND is `./decisionAnswerFlow.ts` —
// mint, build, post and one sentence — which `DecisionInboxCard` calls on a
// click, so a card built here is answerable end to end. This module reads no
// clock either — an age arrives as the endpoint's own `age_seconds`, exactly as
// `recency.ts` takes `nowMs`.

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
  /** WHETHER PRESSING THIS AFFORDANCE MAY POST. False when the write door would
   *  refuse the decision — `decision.resolve` answers exactly one of the eight
   *  producing types — and a renderer shows the `value` as PASTEABLE TEXT there
   *  instead of a control, so the affordance never claims a send that the door
   *  would turn away (finding R-0693). */
  posts: boolean;
}

/** One still-open question the flight plan is waiting on, in the model's own
 *  camel case. The endpoint sends `id`, `question`, `default_answer` and
 *  `impact` — `packages/orchestration/flight_plan.py::open_clarification_questions`
 *  builds every record with exactly those four keys and `str()`-coerces each —
 *  so the two spellings differ ONLY in case convention, exactly as the model's
 *  `taskId` below already differs from the payload's own `task_id`. */
export interface DecisionClarification {
  id: string;
  question: string;
  defaultAnswer: string;
  impact: string;
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
  /** The camel-case projection of the endpoint's own
   *  `answerable_by_decision_resolve`, carried on the model so the component
   *  that projects it never has to read a raw endpoint entry. */
  answerableByDecisionResolve: boolean;
  answers: DecisionAnswer[];
  /** The plan's still-open questions, projected from `payload.clarifications`.
   *  EMPTY for every card that carries none — which is every card but a pending
   *  flight-plan approval — so a renderer needs no branch of its own and the
   *  model stays as total as every other field here. */
  clarifications: DecisionClarification[];
}

/** One entry of the endpoint's `decisions` array, in the endpoint's OWN key
 *  spellings — `export_decision_json` plus the three keys `build_decision_inbox`
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
  /** WHETHER THE WRITE DOOR CAN REALLY ANSWER THIS CARD, as the server derived
   *  it in `decision_inbox._answerable_by_decision_resolve`. Optional because a
   *  server older than R43 does not send it, and the readings below are strict
   *  so that its absence never renders a posting control. */
  answerable_by_decision_resolve?: boolean;
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

/** `payload.clarifications` when the payload is an object carrying it, else
 *  undefined. The SAME tolerance as `payloadOptions` and `payloadTaskId`: a
 *  payload that is missing, null or not an object is not an error, it is simply
 *  a decision with no open questions attached. */
function payloadClarifications(payload: unknown): unknown {
  if (typeof payload !== "object" || payload === null) {
    return undefined;
  }
  return (payload as { clarifications?: unknown }).clarifications;
}

/** Entries rendered as answers of one kind. A non-string entry goes through
 *  `String` rather than being dropped, for the same reason. `posts` is handed
 *  in rather than derived here: it is one card-wide reading, so computing it
 *  per entry would let two answers of one card disagree. */
function entriesAsAnswers(
  entries: unknown[],
  kind: DecisionAnswerKind,
  posts: boolean,
): DecisionAnswer[] {
  return entries.map((entry) => {
    const text = String(entry);
    return { kind, label: text, value: text, posts };
  });
}

/** THE ARCHITECTURE LINE: the affordances a card offers, derived from the
 *  decision's own payload. Options win, then next actions, then a free-text
 *  answer. This function MUST NOT branch on `card.type` — the type is data
 *  here, never control flow — which is exactly what lets a decision type this
 *  repository has never produced render generically. */
export function decisionAnswers(card: DecisionInboxEntry): DecisionAnswer[] {
  // ONE READING, STAMPED ON EVERY BRANCH BELOW. The comparison is strict
  // `=== true` on purpose: an ABSENT key must give false, so a payload from a
  // server older than R43 renders no posting control at all. This is still not
  // a branch on `card.type` — it is a boolean the SERVER derived, data here in
  // exactly the way `blocked_count` is data.
  const posts = card.answerable_by_decision_resolve === true;
  const options = nonEmptyEntries(payloadOptions(card.payload));
  if (options.length > 0) {
    return entriesAsAnswers(options, "option", posts);
  }
  const commands = nonEmptyEntries(card.next_actions);
  if (commands.length > 0) {
    return entriesAsAnswers(commands, "command", posts);
  }
  return [{ kind: "free_text", label: "Answer", value: "", posts }];
}

/** A string field of the endpoint's card, or the empty string when it is absent
 *  or not a string, so no input makes the model throw. */
function cardText(value: unknown): string {
  return typeof value === "string" ? value : "";
}

/** AN ENTRY WHOSE `id` IS BLANK AFTER TRIMMING IS DROPPED, because R51's
 *  `_validated_clarification_answers` refuses the WHOLE request when any
 *  answered id is unknown to the plan, so a field the operator can fill but
 *  never submit would cost them every OTHER answer in the same post. Dropping is
 *  not losing the question: `decision_queue.py` writes the open-question COUNT
 *  into the card's own `safe_summary`, so the card still says one is missing.
 *  The id that survives is carried EXACTLY as the endpoint sent it, untrimmed,
 *  because the server compares it by equality against the plan's own ids. Total
 *  like every reader above — a non-array value, a non-object entry and a
 *  non-string field each fall back rather than raise. */
function cardClarifications(payload: unknown): DecisionClarification[] {
  const entries = payloadClarifications(payload);
  if (!Array.isArray(entries)) {
    return [];
  }
  const questions: DecisionClarification[] = [];
  entries.forEach((entry) => {
    if (typeof entry !== "object" || entry === null) {
      return;
    }
    const record = entry as {
      id?: unknown;
      question?: unknown;
      default_answer?: unknown;
      impact?: unknown;
    };
    const id = cardText(record.id);
    if (id.trim() === "") {
      return;
    }
    questions.push({
      id,
      question: cardText(record.question),
      defaultAnswer: cardText(record.default_answer),
      impact: cardText(record.impact),
    });
  });
  return questions;
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
    // The SAME strict reading `decisionAnswers` makes above, so a card and each
    // of its answers can never disagree about whether the door would take them.
    answerableByDecisionResolve: card.answerable_by_decision_resolve === true,
    answers: decisionAnswers(card),
    // WHY here: `payload.clarifications` is the ONLY place the plan's open
    // questions reach the browser — `decision_queue.py` writes them onto the
    // pending approval card — and the write door takes them back as
    // `args.answers`, so the form cannot exist until the model carries them.
    clarifications: cardClarifications(card.payload),
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

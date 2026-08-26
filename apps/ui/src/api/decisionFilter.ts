// The decision inbox's TYPE FILTER, as PURE functions over the models
// `decisionCard.ts` builds (T5_F031 T002b). DECISION F031 D5 keeps it in this
// layer because the shipped vitest config collects `src/**/*.test.ts` and
// reaches no markup: every branch the control needs is decided here, so the
// `.tsx` that draws the chips stays a projection with no branching of its own.
//
// THE ARCHITECTURE LINE, the same one `decisionCard.ts` states one module over:
// the offered types are DERIVED from the models present and from nothing else.
// Remedy deliberately keeps NO hardcoded type list here, no per-type branch and
// no producer enum import — a reader searching this module for one is searching
// for something it refuses to have — so a decision type this repository has
// never produced appears in the control on the day some producer first emits
// it. `decisionFilter.test.ts` measures that refusal rather than trusting this
// comment.
//
// Remedy deliberately does NOT order or count here either: the rule over age
// and blocked size lives in `./decisionOrder.ts`, and the inbox badge's count
// lives in `./decisionCard.ts` as `countOpenDecisions`. THE SEAM IS WIRED —
// commit `6147efc4` gave this module its caller, and that caller is
// `../components/panels/DecisionInboxCard.tsx`, which imports
// `DECISION_FILTER_ALL` and `decisionInboxView` and calls the view once per
// render — while `RightLivePanel.tsx` still hands `orderDecisionInbox(...)`
// straight to that card, which is the ORDERING seam and deliberately unchanged.
import type { DecisionCardModel } from "./decisionCard";

/** The filter value that means "no filter", and the value the control's first
 *  chip carries. A nullable filter would push that branch up into the markup,
 *  which under DECISION F031 D5 no test reaches. */
export const DECISION_FILTER_ALL = "all";

/** One chip the control offers: `value` is what `filterDecisionsByType` takes
 *  back, `label` is what the operator reads, and `count` is how many cards the
 *  chip leaves visible — the number a badge or a chip caption projects without
 *  computing anything of its own. */
export interface DecisionTypeChoice {
  value: string;
  label: string;
  count: number;
}

/** Everything one render pass of the inbox needs: the chips, the cards that
 *  survive the chosen chip, and the single line to show when none do. */
export interface DecisionInboxView {
  choices: DecisionTypeChoice[];
  visible: DecisionCardModel[];
  emptyMessage: string | null;
}

/** A model's type, defaulted exactly as `buildDecisionCardModel` defaults it,
 *  so a half-written model is grouped rather than dropped. */
function modelType(model: DecisionCardModel): string {
  return typeof model.type === "string" ? model.type : "";
}

/** What the operator reads on a chip. The empty type is the one label this
 *  module invents: `buildDecisionCardModel` defaults a missing `type` there,
 *  and a card no chip can reach is a card the operator loses. */
function decisionTypeLabel(type: string): string {
  return type === "" ? "Untyped" : type;
}

/** The same type as it reads INSIDE a sentence, where a capitalised chip label
 *  would shout in the middle of a quiet line. */
function decisionTypePhrase(type: string): string {
  return type === "" ? "untyped" : type;
}

/** The quiet one line a panel shows instead of an empty list, per
 *  `docs/ui/design_reference/ux_spec.md` §14 — panels show quiet one-line
 *  empties, never illustrations. The two cases read DIFFERENTLY on purpose: an
 *  operator who filtered the list down to nothing must read why it is empty
 *  rather than conclude the queue is clear. */
function decisionEmptyMessage(filter: string): string {
  if (filter === DECISION_FILTER_ALL) {
    return "No decisions are waiting.";
  }
  return `No ${decisionTypePhrase(filter)} decisions are waiting.`;
}

/** The chips the control offers, derived from the models it is handed. Total by
 *  construction: no input makes this throw, and an inbox with no models still
 *  offers the "All" chip so the control never renders empty. */
export function decisionTypeChoices(models: readonly DecisionCardModel[]): DecisionTypeChoice[] {
  const counts = new Map<string, number>();
  for (const model of models) {
    const type = modelType(model);
    counts.set(type, (counts.get(type) ?? 0) + 1);
  }
  const choices: DecisionTypeChoice[] = [
    { value: DECISION_FILTER_ALL, label: "All", count: models.length },
  ];
  // WHY THE SENTINEL IS EXCLUDED, which a reader standing at this expression
  // will not have: `DECISION_FILTER_ALL` is an ordinary string, so a producer
  // emitting a decision whose type is literally "all" would otherwise put a
  // SECOND chip with the SAME `value` into the control — two chips one key, and
  // picking either shows everything. Those cards are never lost; the "All" chip
  // counts and shows them. The concrete chips are sorted ASCENDING by `value`
  // under the default string comparison so the control does not reshuffle
  // itself every time the inbox refetches.
  const types = Array.from(counts.keys())
    .filter((type) => type !== DECISION_FILTER_ALL)
    .sort();
  for (const type of types) {
    choices.push({ value: type, label: decisionTypeLabel(type), count: counts.get(type) ?? 0 });
  }
  return choices;
}

/** The cards one chip leaves visible, as a NEW array in the order it was given.
 *  This never mutates or reorders its input: `orderDecisionInbox` fixes the
 *  order upstream and `Array.prototype.filter` preserves it, so a filter that
 *  re-sorted would break DECISION F031 D6's rule from a distance. A value no
 *  model carries yields nothing, which is an answer and not an error. */
export function filterDecisionsByType(
  models: readonly DecisionCardModel[],
  filter: string,
): DecisionCardModel[] {
  if (filter === DECISION_FILTER_ALL) {
    return models.slice();
  }
  return models.filter((model) => modelType(model) === filter);
}

/** One render pass of the inbox: the chips, the visible cards and the empty
 *  line. Total by construction — no input makes this throw — and `emptyMessage`
 *  is `null` exactly when there is something to show, so the caller needs no
 *  test of its own to decide between a list and a line. */
export function decisionInboxView(
  models: readonly DecisionCardModel[],
  filter: string,
): DecisionInboxView {
  const visible = filterDecisionsByType(models, filter);
  return {
    choices: decisionTypeChoices(models),
    visible,
    emptyMessage: visible.length > 0 ? null : decisionEmptyMessage(filter),
  };
}

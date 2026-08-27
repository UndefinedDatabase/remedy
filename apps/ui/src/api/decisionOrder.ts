// The decision inbox's ORDER, as PURE functions over the models
// `decisionCard.ts` builds (T5_F031 T002b). The rule is DECISION F031 D6's and
// is written down nowhere else: a card's urgency is
// `(blockedCount + 1) * ageSeconds`, and the inbox reads open cards first, then
// by urgency descending, then by `id` ascending.
//
// Remedy deliberately does NOT sort in `decisionCardModels`, nor in the
// `decisionInbox` projection in `remedyApi.ts`, nor inside `DecisionInboxCard`
// — a reader searching any of those for a comparator is searching for
// something they refuse to have, because a rule split across four files is a
// rule nobody can see. It lives here alone and is applied in one place, where
// `RightLivePanel` hands the inbox to the card. DECISION F031 D5 keeps it in
// this layer because the shipped vitest config collects `src/**/*.test.ts` and
// reaches no markup.
import type { DecisionCardModel } from "./decisionCard";

/** How urgent one card is, as the single number the inbox sorts by. Total by
 *  construction: no input makes this throw, and an age or a blocked size this
 *  module cannot trust scores as nothing rather than sorting ahead of a real
 *  one. */
export function decisionUrgency(model: DecisionCardModel): number {
  // A card whose label reads "blocks nothing" must SCORE as blocking nothing:
  // `decisionBlockedLabel` already clamps a negative count to that label, so
  // clamping here too keeps the number and the words the operator reads
  // agreeing, and keeps every urgency at or above the 0 a null age scores.
  const blockedCount = Number.isFinite(model.blockedCount) ? Math.max(0, model.blockedCount) : 0;
  // A null age is the endpoint's own answer for an unreadable `created_at`,
  // which is not evidence of urgency; a negative one means the clocks disagree.
  const rawAge = model.ageSeconds;
  const age = rawAge !== null && Number.isFinite(rawAge) && rawAge > 0 ? rawAge : 0;
  // WHY THE `+ 1`, which a reader standing at this expression will not have:
  // DECISION F031 D6 records that a literal `blockedCount * ageSeconds`
  // collapses every card that blocks NOTHING to exactly 0 whatever its age, so
  // a question asked a week ago and one asked a second ago tie and their order
  // becomes whatever the endpoint happened to send. Adding one keeps blocked
  // size dominant — one blocked task doubles a card's score — and leaves age as
  // the total order among the cards that block nothing.
  return (blockedCount + 1) * age;
}

/** The inbox in the order the operator reads it, as a NEW array. This never
 *  mutates or reorders the array it is given: the endpoint's order is what
 *  `decisionCardModels` and the `remedyApi.ts` projection pin, and a comparator
 *  that sorted its input in place would break both from a distance. The order
 *  is TOTAL — `buildDecisionCardModel` defaults `id` to the empty string — so a
 *  shuffled inbox has exactly one answer. */
export function orderDecisionInbox(models: readonly DecisionCardModel[]): DecisionCardModel[] {
  return models.slice().sort((left, right) => {
    // Key 1: a resolved decision is not urgent at any age or blocked size, and
    // a separate boolean key says that without picking a constant large enough
    // to dominate every possible product.
    if (left.isOpen !== right.isOpen) {
      return left.isOpen ? -1 : 1;
    }
    // Key 2: urgency DESCENDING, compared rather than subtracted so that two
    // scores which are both infinite cannot produce a NaN comparator.
    const leftUrgency = decisionUrgency(left);
    const rightUrgency = decisionUrgency(right);
    if (leftUrgency !== rightUrgency) {
      return leftUrgency > rightUrgency ? -1 : 1;
    }
    // Key 3: `id` ASCENDING under the default string comparison, which is what
    // makes the result independent of the order the endpoint happened to send.
    if (left.id !== right.id) {
      return left.id < right.id ? -1 : 1;
    }
    return 0;
  });
}

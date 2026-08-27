// The clarification form's FORM RULES, as PURE functions over the
// `DecisionClarification` entries `decisionCard.ts` projects: what a single
// field is KEYED by while the operator types, and how one decision's fields are
// COLLECTED into the `Record<string, string>` map `answerDecisionCard` has
// accepted since R61. It is the form's arithmetic, not its markup.
//
// DECISION F031 D5 is why these rules live here rather than inside
// `DecisionInboxCard.tsx`: the shipped `vitest.config.ts` collects
// `src/**/*.test.ts` only and this repository has no DOM harness, so a key rule
// or a collection rule written in the component would ship untested. The card
// keeps the field markup and the input state; every rule that can be a value is
// one, here, where a test can pin it.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the
// missing code will search this file for it. Remedy deliberately does NOT trim
// a collected value, does NOT drop a blank one, does NOT omit an empty map and
// does NOT substitute a question's default answer — not one of those rules is
// missing, and every one of them already has an owner. `decisionAnswer.ts`'s
// `clarificationAnswersArg` trims each value, drops the ones blank after
// trimming, and omits the `answers` key entirely when nothing is left; the
// server's `_validated_clarification_answers` then reads an ABSENT `answers` as
// "accept every default", which is DECISION F031 D24's original contract. A
// second copy of those rules here would be the defect rather than the safety:
// two owners of one rule drift, and the trimming would then happen twice with
// only one of the two visible to a reader. This module answers the operator's
// text RAW and hands the deciding to the module that already owns it.
//
// Remedy deliberately keeps no clock, no fetch, no React state and no component
// in this module. A reader searching it for an input, a change handler or a
// request is searching for something it refuses to have.
import type { DecisionCardModel } from "./decisionCard";

/** WHERE ONE CLARIFICATION FIELD'S TEXT IS STORED WHILE THE OPERATOR TYPES.
 *
 *  TWO CARDS MAY CARRY ONE ID, which is why the decision's POSITION is half of
 *  this key — the same reason `decisionAnswerKey` in `DecisionInboxCard.tsx`
 *  pairs a position with an id rather than trusting the id alone. A key built
 *  from the decision id alone would let one card's field hold another card's
 *  answer the moment the inbox carries a duplicate, and the operator would post
 *  text they typed into a different question. The question's own id completes
 *  the key, so one card's two questions can never share a field either. */
export function decisionClarificationFieldKey(
  decisionIndex: number,
  decisionId: string,
  questionId: string,
): string {
  return `${decisionIndex}-${decisionId}-${questionId}`;
}

/** ONE DECISION'S FIELDS AS THE MAP THE WRITE DOOR TAKES: one entry per
 *  clarification the decision carries, keyed by that clarification's OWN id —
 *  which is the spelling `_validated_clarification_answers` compares against the
 *  plan's questions — and valued by the text stored under this decision's field
 *  key for it, or the EMPTY STRING when no field was touched.
 *
 *  IT READS NO KEY IT DID NOT COMPUTE. The store is flat and holds every card's
 *  fields at once, so a collector that iterated the STORE rather than this
 *  decision's questions would carry another card's text into this card's post.
 *  Iterating the decision's own `clarifications` makes that impossible: the only
 *  keys ever read are the ones `decisionClarificationFieldKey` builds from this
 *  decision's position and id.
 *
 *  A decision carrying no clarification collects an empty object, which is the
 *  normal case — every card but a pending flight-plan approval — and NOT a
 *  failure. The empty map is what `clarificationAnswersArg` turns into an absent
 *  `answers` key, so an untouched form posts exactly what a client written
 *  before this form posts. */
export function collectDecisionClarificationAnswers(
  fieldValues: Readonly<Record<string, string>>,
  decisionIndex: number,
  decision: Pick<DecisionCardModel, "id" | "clarifications">,
): Record<string, string> {
  const collected: Record<string, string> = {};
  decision.clarifications.forEach((clarification) => {
    const fieldKey = decisionClarificationFieldKey(
      decisionIndex,
      decision.id,
      clarification.id,
    );
    // `hasOwnProperty` rather than a truthiness test: the store reaches this
    // rule as a plain object, so an untouched field must miss rather than
    // resolve against something on the prototype.
    collected[clarification.id] = Object.prototype.hasOwnProperty.call(fieldValues, fieldKey)
      ? fieldValues[fieldKey]
      : "";
  });
  return collected;
}

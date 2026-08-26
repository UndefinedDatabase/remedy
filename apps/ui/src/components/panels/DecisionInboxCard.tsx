// The decision inbox's CARD, as a pure PROJECTION of the models `decisionCard.ts`
// builds (T5_F031 T002a, DECISION F031 D4). It reads `dashboard.decisionInbox`
// through its one prop and adds nothing of its own: every string it displays is
// a FIELD of a model, never a value this file chose.
//
// THE ARCHITECTURE LINE, written down here because a reader looking for the
// missing code will search this file for it: Remedy deliberately does NOT
// dispatch on a decision's `type` or `status` anywhere in this component — no
// per-type registry, no type-to-widget map, no comparison against either field.
// Both are DATA here and never control flow, which is what lets a decision type
// this repository has not produced yet render on the day some producer first
// emits it. DECISION F031 D5 keeps every real branch in `decisionCard.ts`, where
// the shipped vitest config can reach it; one migrating into this file would
// leave the tested region silently, because no test reaches this markup.
//
// Remedy also deliberately does NOT sort, filter, count or answer here: ordering
// over age and blocked size and the inbox badge are T002b's subject, and the
// write path behind the answer buttons is T003's — which is why those buttons
// ship DISABLED rather than looking live while doing nothing.
import type { DecisionCardModel } from "../../api/decisionCard";
import styles from "./RightLivePanel.module.css";

/** Why answering does nothing yet, said on the control itself rather than left
 *  for the operator to discover by clicking. */
const ANSWER_PENDING_TITLE = "Answering arrives with T003";

/** Every open question in one calm place. With no models this renders nothing at
 *  all — an empty inbox is not news, exactly as `NeedsAttentionCard` shows
 *  nothing when it has no item. */
export function DecisionInboxCard({ decisions }: { decisions: DecisionCardModel[] }) {
  if (decisions.length === 0) return null;

  return (
    <section className={styles.card} data-ui="decision-inbox-card">
      <header className={styles.cardHeader}><h2>Decision inbox</h2></header>
      {decisions.map((decision, decisionIndex) => (
        // The key pairs a model's POSITION with its id, so two cards carrying the
        // same id still get distinct keys and a card with an empty id still gets
        // a stable one.
        <article key={`${decisionIndex}-${decision.id}`} className={styles.decisionRow}>
          <strong className={styles.decisionTitle}>{decision.title}</strong>
          <div className={styles.decisionChips}>
            <span className={styles.decisionChip}>{decision.ageLabel}</span>
            <span className={styles.decisionChip}>{decision.blockedLabel}</span>
            <span className={styles.decisionChip}>{decision.type}</span>
          </div>
          <div className={styles.decisionAnswers}>
            {decision.answers.map((answer, answerIndex) => (
              <button
                key={`${answerIndex}-${answer.value}`}
                type="button"
                className={styles.decisionAnswer}
                disabled
                title={ANSWER_PENDING_TITLE}
              >
                {answer.label}
              </button>
            ))}
          </div>
        </article>
      ))}
    </section>
  );
}

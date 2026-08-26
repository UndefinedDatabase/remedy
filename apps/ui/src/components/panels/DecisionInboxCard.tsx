// The decision inbox's CARD, as a pure PROJECTION of the models `decisionCard.ts`
// builds (T5_F031 T002a, DECISION F031 D4). It reads `dashboard.decisionInbox`
// through its one prop and adds nothing of its own: every string it displays is
// a FIELD — of a model, or of a chip `decisionFilter.ts` derived — never a value
// this file chose.
//
// THE ARCHITECTURE LINE, written down here because a reader looking for the
// missing code will search this file for it: Remedy deliberately does NOT
// dispatch on a decision's `type` or `status` anywhere in this component — no
// per-type registry, no type-to-widget map, no comparison against either field.
// Both are DATA here and never control flow, which is what lets a decision type
// this repository has not produced yet render on the day some producer first
// emits it. DECISION F031 D5 keeps every real branch in `decisionCard.ts`, where
// the shipped vitest config can reach it; one migrating into this file would
// leave the tested region silently, because no test reaches this markup. THE
// FILTER BELOW DOES NOT BREAK THAT: it compares the chosen value against a
// chip's own `value`, which is state against derived data, and never against a
// type this file names.
//
// Remedy deliberately does NOT decide here WHICH cards survive, in WHAT ORDER
// they arrive, or HOW MANY there are. The chosen type is the one piece of state
// this component owns; the RULES that turn it into chips, a visible list and a
// quiet empty line live in `../../api/decisionFilter`, the ordering rule lives
// in `../../api/decisionOrder`, and the header badge's count is
// `countOpenDecisions` in `../../api/decisionCard` — every one of them a module
// the shipped vitest config reaches, which this markup is not. ANSWERING is no
// longer wholly absent — this round added `../../api/decisionAnswer`, which
// builds the exact command body `/api/jobs/<job_id>/commands` accepts, and that
// module is what falsified the sentence that stood here. What is still absent is
// the SEND: nothing in this browser posts that body yet, which is why the answer
// buttons still ship DISABLED rather than looking live while doing nothing.
import { useState } from "react";
import { countOpenDecisions } from "../../api/decisionCard";
import type { DecisionCardModel } from "../../api/decisionCard";
import { DECISION_FILTER_ALL, decisionInboxView } from "../../api/decisionFilter";
import styles from "./RightLivePanel.module.css";

/** Why answering does nothing yet, said on the control itself rather than left
 *  for the operator to discover by clicking. */
const ANSWER_PENDING_TITLE = "Answering arrives with T003";

/** What the chip strip is called for a reader who cannot see it grouped. It is
 *  announced, never displayed, so the projection rule above still holds. */
const FILTER_CHIPS_LABEL = "Filter decisions by type";

/** What the header's number counts, said in words for a reader who meets it
 *  without the heading beside it. It PREFIXES the number rather than standing in
 *  for it: an `aria-label` REPLACES an element's content in the accessibility
 *  tree, so a label naming only the word would hide the very digit it explains.
 *  The colon form is used because it stays grammatical at every count and so
 *  needs no plural branch in this markup, which no test reaches. */
const OPEN_COUNT_LABEL = "Open decisions waiting";

/** Every open question in one calm place. With no models this renders nothing at
 *  all — an empty inbox is not news, exactly as `NeedsAttentionCard` shows
 *  nothing when it has no item. */
export function DecisionInboxCard({ decisions }: { decisions: DecisionCardModel[] }) {
  const [chosenType, setChosenType] = useState<string>(DECISION_FILTER_ALL);

  // THE EMPTY-STATE TRAP, guarded here rather than explained after someone falls
  // into it: this test reads the UNFILTERED prop on purpose. Reading the filtered
  // list instead would unmount the card together with the control inside it the
  // moment a chip matched nothing, stranding the operator with no way back —
  // which is exactly why `decisionInboxView` hands back a quiet line for that
  // case rather than an empty list.
  if (decisions.length === 0) return null;

  // THE BADGE COUNTS THE PROP, NEVER `view.visible`: it says how many questions
  // the job is waiting on, which is not the same number as how many the chosen
  // chip left on screen. Counting the view instead would shrink the badge every
  // time the operator narrowed the list and report a queue draining that had not.
  const openCount = countOpenDecisions(decisions);
  const view = decisionInboxView(decisions, chosenType);

  return (
    <section className={styles.card} data-ui="decision-inbox-card">
      <header className={styles.cardHeader}>
        <h2>Decision inbox</h2>
        {/* An `output` rather than a `span`: a bare `div`/`span` maps to the ARIA
            `generic` role, which prohibits an accessible name, so the label would
            be computed and dropped (finding R-0682). The word ships in the
            VISIBLE text too, because a lone digit beside a heading reads as
            nothing in particular either way. */}
        <output
          className={styles.decisionOpenCount}
          aria-label={`${OPEN_COUNT_LABEL}: ${openCount}`}
        >
          {openCount} open
        </output>
      </header>
      <div className={styles.decisionFilterRow} role="group" aria-label={FILTER_CHIPS_LABEL}>
        {view.choices.map((choice) => (
          <button
            key={choice.value}
            type="button"
            className={
              choice.value === chosenType
                ? `${styles.decisionFilterChip} ${styles.decisionFilterChipOn}`
                : styles.decisionFilterChip
            }
            aria-pressed={choice.value === chosenType}
            onClick={() => setChosenType(choice.value)}
          >
            {choice.label}
            <span className={styles.decisionFilterCount}>{choice.count}</span>
          </button>
        ))}
      </div>
      {/* The list ANNOUNCES itself when a chip changes it, rather than reflowing
          in silence under a control the operator just pressed. */}
      <div aria-live="polite">
        {view.emptyMessage === null ? (
          view.visible.map((decision, decisionIndex) => (
            // The key pairs a model's POSITION with its id, so two cards carrying
            // the same id still get distinct keys and a card with an empty id
            // still gets a stable one.
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
          ))
        ) : (
          <p className={styles.emptyState}>{view.emptyMessage}</p>
        )}
      </div>
    </section>
  );
}

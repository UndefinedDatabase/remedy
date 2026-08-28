// The decision inbox's CARD, as a PROJECTION of the models `decisionCard.ts`
// builds (T5_F031 T002a, DECISION F031 D4). It reads `dashboard.decisionInbox`
// through its own prop, and takes the dashboard's task list, its job id, the
// per-run server token and the node-selecting callback beside it. The two halves
// of what a reader sees are
// split on purpose: the CONTENT of a card is always a FIELD — of a model, or of
// a chip `decisionFilter.ts` derived — and no string this file invented ever
// reaches it, while the FIXED AFFORDANCE LABELS are this file's own and every
// one of them is declared as a `const` directly below rather than written
// inline at its control, so the whole vocabulary this component adds is
// readable in one place.
//
// THE ARCHITECTURE LINE, written down here because a reader looking for the
// missing code will search this file for it: Remedy deliberately does NOT
// dispatch on a decision's `type` or `status` anywhere in this component — no
// per-type registry, no type-to-widget map, no comparison against either field.
// Both are DATA here and never control flow, which is what lets a decision type
// this repository has not produced yet render on the day some producer first
// emits it. DECISION F031 D5 keeps every real branch in `decisionCard.ts`, where
// the shipped vitest config can reach it; one migrating into this file would
// leave the tested region silently. THE FILTER BELOW DOES NOT BREAK THAT: it
// compares the chosen value against a chip's own `value`, which is state against
// derived data, and never against a type this file names. THE OUTCOME MAP DOES
// NOT BREAK IT EITHER: it is a `Record` lookup keyed by a tone
// `decisionOutcome.ts` already chose, which is a projection and not a branch.
// NOR DOES THE CLARIFICATION BLOCK: it tests how MANY questions the model
// carries, which is a length and not a kind, and every question it then renders
// is a field of that model.
//
// NO DOM TEST REACHES THIS MARKUP. The shipped vitest config collects
// `src/**/*.test.ts` and this repository has no DOM environment, so nothing here
// is ever rendered by a suite. What guards this file instead is
// `tests/ui_contracts/test_decision_answer_wiring.py`, which reads the
// COMMENT-STRIPPED source of the whole prop chain and of this component, and
// `tsc --noEmit`, which is why every hop declares `serverToken` in its own props
// type. A reader changing the answer wiring changes that test with it.
//
// Remedy deliberately does NOT decide here WHICH cards survive, in WHAT ORDER
// they arrive, or HOW MANY there are. The chosen type is the one piece of state
// this component owns; the RULES that turn it into chips, a visible list and a
// quiet empty line live in `../../api/decisionFilter`, the ordering rule lives
// in `../../api/decisionOrder`, and the header badge's count is
// `countOpenDecisions` in `../../api/decisionCard` — every one of them a module
// the shipped vitest config reaches, which this markup is not. ANSWERING IS NO
// LONGER ABSENT ANYWHERE: `../../api/decisionAnswerFlow` mints the nonce, builds
// the request, posts it and says what happened, all behind the one call
// `answerDecisionCard` below makes on a click.
//
// ONLY AN ANSWER WHOSE `posts` IS TRUE SHIPS AS A BUTTON, and for that answer
// the press really does reach `/api/jobs/<job_id>/commands`. An answer whose
// `posts` is false ships as PASTEABLE TEXT carrying the command instead, because
// the write door `decision.resolve` would refuse it and an enabled control that
// cannot post is the dishonest affordance finding R-0693 registered
// (DECISION F031 D22). Remedy deliberately does NOT read a decision's `type` or
// its `status` to decide which of the two it renders — a reader searching this
// file for that comparison is searching for something this component refuses to
// have. It projects `answer.posts`, a per-answer boolean `decisionCard.ts`
// already derived from the endpoint's own `answerable_by_decision_resolve`, so
// DECISION F031 D5's rule stands and the guard that pins it stays green. This
// component owns only WHICH answers are in flight, WHERE their sentences appear,
// WHAT COLOUR each one takes and WHAT THE OPERATOR HAS TYPED into each open
// clarification field. It owns no RULE about that typing:
// `../../api/decisionClarificationForm` names a field's key and collects one
// card's fields into the map the write door takes, and `decisionAnswer.ts`'s
// `clarificationAnswersArg` decides what a blank value means — the same D5
// reason keeps both of those out of this file.
import { Fragment, useState } from "react";
import { countOpenDecisions } from "../../api/decisionCard";
import type { DecisionCardModel, DecisionEvidenceRef } from "../../api/decisionCard";
import { answerDecisionCard } from "../../api/decisionAnswerFlow";
import { collectDecisionClarificationAnswers, decisionClarificationFieldKey } from "../../api/decisionClarificationForm";
import { DECISION_FILTER_ALL, decisionInboxView } from "../../api/decisionFilter";
import { nodeIdForDecisionCard } from "../../api/decisionFocus";
import type { DecisionOutcomeMessage, DecisionOutcomeTone } from "../../api/decisionOutcome";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { FocusableTask } from "../../api/feedFocus";
import styles from "./RightLivePanel.module.css";

/** COLOUR AND PLACEMENT ARE THIS COMPONENT'S; THE SENTENCE NEVER IS. Every word
 *  an operator reads about a sent answer comes from `decisionOutcome.ts`, and
 *  this map only says how loud each of its three tones looks. A `Record` lookup
 *  rather than a branch, so no rule about an outcome can drift into markup no
 *  vitest reaches (DECISION F031 D5). */
const DECISION_OUTCOME_CLASS: Record<DecisionOutcomeTone, string> = {
  ok: styles.decisionOutcomeOk,
  warn: styles.decisionOutcomeWarn,
  error: styles.decisionOutcomeError,
};

/** TWO CARDS MAY CARRY ONE ID, so a model's POSITION is half of every key this
 *  card computes: the row key pairs the position with the id, and an answer's
 *  key extends it by that answer's own position. Written once, here, so the
 *  `article` React key and the key an outcome sentence is stored under can never
 *  drift apart and let one card's answer speak in another's row. */
function decisionRowKey(decisionIndex: number, decisionId: string): string {
  return `${decisionIndex}-${decisionId}`;
}

function decisionAnswerKey(decisionIndex: number, decisionId: string, answerIndex: number): string {
  return `${decisionRowKey(decisionIndex, decisionId)}-${answerIndex}`;
}

/** ONE PRESS TOUCHES ONLY ITS OWN KEY, and that is the whole point of these two
 *  (finding R-0687). Each copies the in-flight set before changing it, so React
 *  sees a new identity and no press can add, clear or re-enable another answer's
 *  button; mutating the set in place would both skip the re-render and make one
 *  press the owner of every other answer's disabled state. */
function withAnswerKey(sending: ReadonlySet<string>, answerKey: string): ReadonlySet<string> {
  const next = new Set(sending);
  next.add(answerKey);
  return next;
}

function withoutAnswerKey(sending: ReadonlySet<string>, answerKey: string): ReadonlySet<string> {
  const next = new Set(sending);
  next.delete(answerKey);
  return next;
}

/** What the chip strip is called for a reader who cannot see it grouped. It is
 *  announced, never displayed, so the projection rule above still holds. */
const FILTER_CHIPS_LABEL = "Filter decisions by type";

/** What the header's number counts, said in words for a reader who meets it
 *  without the heading beside it. It PREFIXES the number rather than standing in
 *  for it: an `aria-label` REPLACES an element's content in the accessibility
 *  tree, so a label naming only the word would hide the very digit it explains.
 *  The colon form is used because it stays grammatical at every count and so
 *  needs no plural branch in this markup, which no rendering test reaches. */
const OPEN_COUNT_LABEL = "Open decisions waiting";

/** The jump control's own word, kept chip-row short because it rides in the
 *  strip beside the age, blocked-size and type chips. */
const DECISION_JUMP_LABEL = "In graph";

/** Where that control goes, said on the control itself rather than left for the
 *  operator to discover by clicking. A `title` rather than an `aria-label`: an
 *  `aria-label` REPLACES the button's content in the accessibility tree, and the
 *  visible word would then be missing from the accessible name it explains. */
const DECISION_JUMP_TITLE = "Show this decision's task in the graph";

/** What the strip of receipt chips IS, for a reader who meets it without the
 *  card around it. It rides on a `role="group"`, never on a bare `div`: a
 *  `div`/`span` maps to the ARIA `generic` role, which prohibits an accessible
 *  name, so the label would be computed and dropped (finding R-0682) — the same
 *  reason the filter row above carries one. It names what the chips ARE and
 *  never how many there are or whether any exist: a present/missing signal is
 *  exactly what §17 of docs/ui/design_reference/ux_spec.md keeps out of the
 *  default UI, and the model's own note already says the honest sentence when a
 *  card carries none. */
const DECISION_EVIDENCE_LABEL = "What this decision is based on";

/** What the plan will take for a question the operator leaves alone. It
 *  PREFIXES the model's own `defaultAnswer` and never replaces it: the value is
 *  the question's and only this noun is the card's. It is a WORD BESIDE AN EMPTY
 *  FIELD rather than the field's own value on purpose — the server reads a blank
 *  or absent answer as "accept this question's default" (DECISION F031 D24), so
 *  a prefilled input would post the default as though it had been typed, and an
 *  operator who only glanced at the form would have answered it. */
const DECISION_CLARIFICATION_DEFAULT_LABEL = "Default";

/** What changes depending on how the question is answered. It PREFIXES the
 *  model's own `impact`, which `open_clarification_questions` already wrote —
 *  this card supplies the noun and never the sentence. Both nouns ride in ONE
 *  meta line joined by a middle dot; the dot is punctuation between two labelled
 *  values, and the two labels above are the only words this block adds. */
const DECISION_CLARIFICATION_IMPACT_LABEL = "Impact";

/** Every open question in one calm place. With no models this renders nothing at
 *  all — an empty inbox is not news, exactly as `NeedsAttentionCard` shows
 *  nothing when it has no item. */
export function DecisionInboxCard({ decisions, tasks, jobId, serverToken, onSelectNode, onOpenEvidence }: {
  decisions: DecisionCardModel[];
  tasks: readonly FocusableTask[];
  /** The job every answer from this card addresses — `dashboard.jobId`, the same
   *  value the brain stream is opened against (DECISION F008 D3). */
  jobId: string;
  /** THE PER-RUN CREDENTIAL, and it NEVER REACHES A URL PATH. `decisionSend.ts`
   *  spends it in the `Authorization` and `X-Remedy-CSRF` headers alone, because
   *  a path or a query string is the part of a URL that reaches logs. It arrives
   *  as a prop from `RemedyApp`'s `readUrlState`, threaded through `RemedyShell`
   *  and `RightLivePanel` under this one spelling at every hop. */
  serverToken: string;
  onSelectNode: (nodeId: string | null) => void;
  /** WHERE A RECEIPT GOES WHEN THERE IS SOMEWHERE TO GO — the evidence panel's
   *  ENTRY POINT, and nothing supplies it today (DECISION F032 D8). The panel
   *  itself is `docs/roadmap/features/T5_F023.md` T003, which is unclaimed, so
   *  every card in this release renders its receipts as plain chips; F023
   *  supplies this handler and the panel together and the wiring is one prop at
   *  one call site. It takes the WHOLE ref rather than a field of it, so the
   *  panel that finally arrives gets `kind` and `target` without this component
   *  ever reading either — passing a ref on is not rendering it. */
  onOpenEvidence?: (evidenceRef: DecisionEvidenceRef) => void;
}) {
  const [chosenType, setChosenType] = useState<string>(DECISION_FILTER_ALL);
  // WHICH answers are waiting on the wire, as a SET of keys rather than one key
  // (finding R-0687). The guarantee this shape makes, and the weaker one a
  // single key made, are not the same sentence: a button stays disabled until
  // ITS OWN send settles, because membership is tested per answer key and each
  // press adds and removes only its own. A single key held only "no other button
  // is disabled at this instant", so a second press re-enabled the first
  // answer's button while its request was still on the wire and the operator
  // could send it twice — a 409 and a sentence about a decision they had just
  // answered.
  const [sendingKeys, setSendingKeys] = useState<ReadonlySet<string>>(new Set());
  // Keyed per ANSWER, never per decision: a row's key already carries the
  // model's position, so an id two cards share cannot make them speak as one.
  const [outcomes, setOutcomes] = useState<Record<string, DecisionOutcomeMessage | undefined>>({});
  // WHAT THE OPERATOR HAS TYPED INTO EVERY CLARIFICATION FIELD ON SCREEN, as ONE
  // FLAT STORE keyed by `decisionClarificationFieldKey` rather than as a map per
  // card. That flatness is exactly why `collectDecisionClarificationAnswers`
  // iterates a DECISION'S OWN questions instead of walking this store: the store
  // holds every card's fields at once, so a collector that read its keys would
  // carry one card's text into another card's post. A field nobody touched is
  // simply ABSENT here, and absent is what that collector answers as the empty
  // string — which is the blank the server reads as "accept this default".
  const [clarificationValues, setClarificationValues] = useState<Record<string, string>>({});

  // NAMED FIELDS, never a bare pair of strings: both are opaque ids of the same
  // type, so a positional call would let the token be spent as the job id and
  // written into the request path (finding R-0684).
  const target: DecisionSendTarget = { jobId, serverToken };

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
          view.visible.map((decision, decisionIndex) => {
            // Resolved ONCE per decision, beside the badge and the view above.
            // A null is not a failure: it is a decision naming no task, or one
            // this dashboard does not carry, and that card must not OFFER the
            // jump — the resolver's own contract.
            const jumpNodeId = nodeIdForDecisionCard(decision, tasks);
            // ONE MAP PER ROW, collected here beside the jump target rather than
            // inside a click handler, so every answer on this card sends the
            // same answers and the rule that builds them stays in a module the
            // shipped vitest config reaches (DECISION F031 D5). This card owns
            // no rule about what an empty map, a blank value or an untyped
            // field MEANS — `clarificationAnswersArg` in decisionAnswer.ts owns
            // the trimming and the omission, and the collector owns the keys.
            const clarificationAnswers = collectDecisionClarificationAnswers(
              clarificationValues,
              decisionIndex,
              decision,
            );
            return (
              // The key pairs a model's POSITION with its id, so two cards carrying
              // the same id still get distinct keys and a card with an empty id
              // still gets a stable one.
              <article key={decisionRowKey(decisionIndex, decision.id)} className={styles.decisionRow}>
                <strong className={styles.decisionTitle}>{decision.title}</strong>
                <div className={styles.decisionChips}>
                  <span className={styles.decisionChip}>{decision.ageLabel}</span>
                  <span className={styles.decisionChip}>{decision.blockedLabel}</span>
                  <span className={styles.decisionChip}>{decision.type}</span>
                  {/* Only a decision that can really jump gets the control, so the
                      affordance never lies. That is ActivityFeedCard's rule, but
                      NOT its shape: a decision row already contains the answer
                      buttons, so making the row itself the button would nest
                      interactive controls (DECISION F031 D15). */}
                  {jumpNodeId ? (
                    <button
                      type="button"
                      className={styles.decisionJumpChip}
                      title={DECISION_JUMP_TITLE}
                      onClick={() => onSelectNode(jumpNodeId)}
                    >
                      {DECISION_JUMP_LABEL}
                    </button>
                  ) : null}
                </div>
                {/* THE RECEIPTS, ABOVE EVERYTHING THE OPERATOR CAN PRESS
                    (T5_F032 T003b). A chip shows the ref's `label` and NOTHING
                    ELSE. The label reaches the model already scrubbed, and it
                    is the only one of a ref's three fields a renderer may show:
                    §17 of docs/ui/design_reference/ux_spec.md forbids the
                    default UI to show raw ids, and a ref's `target` is
                    frequently exactly one — a test run id, an escalation id
                    like `td:1` — so it is carried on the model for the deep
                    link, travels to `onOpenEvidence` as a field of the ref it
                    is part of, and appears here in no text, no `title` and no
                    other attribute a browser shows.
                    BOTH REGIONS RENDER UNCONDITIONALLY, and that is the model's
                    doing rather than this markup's luck: `evidenceRefs` is an
                    EMPTY ARRAY and `evidenceNote` the EMPTY STRING on a card
                    with no receipts, so the map yields no nodes, the note
                    yields no text, and RightLivePanel.module.css collapses each
                    empty one OUT OF FLOW rather than removing it. */}
                <div className={styles.decisionEvidence} role="group" aria-label={DECISION_EVIDENCE_LABEL}>
                  {decision.evidenceRefs.map((evidenceRef, evidenceIndex) => (
                    // A RECEIPT IS A CONTROL ONLY WHEN THERE IS SOMEWHERE TO GO
                    // (T5_F032 T003c, DECISION F032 D8). That is the jump chip's
                    // rule one row above, for the same stated reason — the
                    // affordance never lies — and the discriminator is the
                    // PRESENCE of the handler rather than anything this file
                    // reads off the ref. The whole ref travels to it, so the
                    // panel F023 builds receives `kind` and `target` while this
                    // component still shows neither.
                    // THE KEY PAIRS THE RECEIPT'S POSITION WITH ITS LABEL, by
                    // the rule every other key on this card follows: nothing
                    // between the endpoint and the model deduplicates refs, so
                    // two receipts carrying one label still get distinct keys.
                    // It rides on the outer element of BOTH arms, because React
                    // keys the node the map yields and not the branch above it.
                    onOpenEvidence ? (
                      <button
                        key={`${evidenceIndex}-${evidenceRef.label}`}
                        type="button"
                        className={styles.decisionEvidenceChip}
                        onClick={() => onOpenEvidence(evidenceRef)}
                      >
                        {evidenceRef.label}
                      </button>
                    ) : (
                      <span key={`${evidenceIndex}-${evidenceRef.label}`} className={styles.decisionEvidenceChip}>
                        {evidenceRef.label}
                      </span>
                    )
                  ))}
                </div>
                {/* WHY A CARD HAS NO RECEIPTS, in the model's own sentence and
                    never in a status word. `evidence_status` IS the
                    present/missing signal §17 excludes, so it never reaches the
                    model at all; what arrives here is prose, or the empty
                    string when there is nothing to explain. */}
                <p className={styles.decisionEvidenceNote}>{decision.evidenceNote}</p>
                {/* THE STILL-OPEN QUESTIONS, ABOVE THE ANSWER STRIP: the
                    operator reads what the plan is waiting on before pressing
                    the control that resolves it. A card carrying none renders
                    nothing here at all, which is every card but a pending
                    flight-plan approval. */}
                {decision.clarifications.length > 0 ? (
                  <div className={styles.decisionClarifications}>
                    {decision.clarifications.map((clarification, clarificationIndex) => {
                      const fieldKey = decisionClarificationFieldKey(
                        decisionIndex,
                        decision.id,
                        clarification.id,
                      );
                      const defaultText = `${DECISION_CLARIFICATION_DEFAULT_LABEL}: ${clarification.defaultAnswer}`;
                      const impactText = `${DECISION_CLARIFICATION_IMPACT_LABEL}: ${clarification.impact}`;
                      return (
                        // THE KEY PAIRS THE QUESTION'S POSITION WITH ITS FIELD
                        // KEY, because the endpoint does not guarantee distinct
                        // question ids: neither `open_clarification_questions`
                        // in packages/orchestration/flight_plan.py nor
                        // `cardClarifications` in decisionCard.ts deduplicates
                        // them, so a key built from the id alone would let React
                        // reuse ONE node for TWO questions and the operator's
                        // typing would appear under the wrong one. The collected
                        // MAP still collapses a duplicate id to one entry, and
                        // that is not this component's to change: the write
                        // door's contract is keyed by question id.
                        <div key={`${clarificationIndex}-${fieldKey}`} className={styles.decisionClarification}>
                          <label className={styles.decisionClarificationQuestion} htmlFor={fieldKey}>
                            {clarification.question}
                          </label>
                          {/* THE FIELD STARTS EMPTY AND STAYS THE OPERATOR'S.
                              Its value is read from the flat store under this
                              field's own key and falls back to the EMPTY STRING
                              — never to `clarification.defaultAnswer`, which is
                              shown as text below instead: a blank answer is what
                              the server reads as "accept this default"
                              (DECISION F031 D24), so prefilling it would post
                              the default as though it had been typed. */}
                          <input
                            id={fieldKey}
                            type="text"
                            className={styles.decisionClarificationInput}
                            value={clarificationValues[fieldKey] ?? ""}
                            onChange={(event) => {
                              const typed = event.target.value;
                              // ONE FIELD'S KEY AND NO OTHER, by the same rule
                              // the in-flight set follows: the store is copied
                              // and exactly this key is written, so typing in
                              // one question can never edit another's text.
                              setClarificationValues((sofar) => ({ ...sofar, [fieldKey]: typed }));
                            }}
                          />
                          <p className={styles.decisionClarificationMeta}>{`${defaultText} · ${impactText}`}</p>
                        </div>
                      );
                    })}
                  </div>
                ) : null}
                <div className={styles.decisionAnswers}>
                  {decision.answers.map((answer, answerIndex) => {
                    const answerKey = decisionAnswerKey(decisionIndex, decision.id, answerIndex);
                    const outcome = outcomes[answerKey] ?? null;
                    // THE REGION EXISTS BEFORE IT HAS ANYTHING TO SAY, so only
                    // its CLASS is chosen here (finding R-0686). Quiet is the
                    // empty state's collapse, and RightLivePanel.module.css
                    // says there why it is done out of flow rather than with
                    // display: none, visibility: hidden or the hidden
                    // attribute — each of those would take the region out of
                    // the accessibility tree and silence it again.
                    const outcomeClass = outcome === null
                      ? `${styles.decisionOutcome} ${styles.decisionOutcomeQuiet}`
                      : `${styles.decisionOutcome} ${DECISION_OUTCOME_CLASS[outcome.tone]}`;
                    return (
                      <Fragment key={answerKey}>
                        {/* THE CHOICE IS MADE BEFORE THE BUTTON, NEVER AFTER IT.
                            `posts` is the discriminator and the button is the
                            FIRST arm on purpose: the guard in
                            tests/ui_contracts/test_decision_answer_wiring.py
                            reads everything between the LAST `</button>` and the
                            outcome `<p` and rejects `?`, `&&` and `||` there
                            (finding R-0690), so writing this ternary the other
                            way round would put its `?` inside that region and
                            fail a check about the live region for a reason that
                            has nothing to do with one. A refused answer renders
                            as TEXT rather than as a disabled control: a disabled
                            button keeps the shape R-0693 called dishonest and is
                            skipped by keyboard navigation, which would put the
                            command out of reach of the operators most likely to
                            want to paste it (DECISION F031 D22). */}
                        {answer.posts ? (
                          <button
                            type="button"
                            className={styles.decisionAnswer}
                            disabled={sendingKeys.has(answerKey)}
                            onClick={async () => {
                              setSendingKeys((sofar) => withAnswerKey(sofar, answerKey));
                              const message = await answerDecisionCard(target, decision, answer.value, clarificationAnswers);
                              setSendingKeys((sofar) => withoutAnswerKey(sofar, answerKey));
                              setOutcomes((sofar) => ({ ...sofar, [answerKey]: message }));
                            }}
                          >
                            {answer.label}
                          </button>
                        ) : (
                          <code className={styles.decisionAnswerText}>{answer.value}</code>
                        )}
                        {/* It ANNOUNCES itself, which is why the paragraph is
                            rendered EMPTY from this row's first render and
                            filled in later: a screen reader registers a live
                            region when the node enters the accessibility tree
                            and announces later MUTATIONS of it, so a region
                            created together with its first sentence would leave
                            the operator on the button with nothing said. */}
                        <p className={outcomeClass} aria-live="polite">
                          {outcome === null ? "" : outcome.sentence}
                        </p>
                        {/* WHAT THIS ANSWER IS EXPECTED TO DO AND WHAT IT
                            COSTS, under the answer they belong to — the whole
                            reason F032 hangs both on the ANSWER rather than on
                            the card, so consent is informed by the option
                            actually being pressed. THEY SIT AFTER THE OUTCOME
                            PARAGRAPH IN SOURCE ORDER ON PURPOSE: the guard in
                            tests/ui_contracts/test_decision_answer_wiring.py
                            reads the LAST `aria-live` in this file and requires
                            a `<p` to open it (finding R-0690), so a region
                            added above it would aim that reader at the wrong
                            node. Neither carries an `aria-live` of its own: the
                            text is there from the row's first render and never
                            mutates, so announcing it would interrupt rather
                            than inform. BOTH RENDER UNCONDITIONALLY and under
                            no conditional operator at all — decisionCard.ts
                            guarantees each is a string, EMPTY rather than
                            absent, and the stylesheet collapses an empty one
                            out of flow. */}
                        <p className={styles.decisionExpectedOutcome}>{answer.expectedOutcome}</p>
                        <p className={styles.decisionDownside}>{answer.downside}</p>
                      </Fragment>
                    );
                  })}
                </div>
              </article>
            );
          })
        ) : (
          <p className={styles.emptyState}>{view.emptyMessage}</p>
        )}
      </div>
    </section>
  );
}

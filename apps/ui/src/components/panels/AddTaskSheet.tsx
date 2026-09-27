import { useEffect, useState, type ChangeEvent } from "react";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { InjectSendOutcome } from "../../api/injectSend";
import { sendInjectAnswer, sendInjectConfirm, sendInjectDraft } from "../../api/injectSend";
import { injectDraftView } from "../../api/injectView";
import type { RemedyTaskItem } from "../../api/types";
import styles from "./AddTaskSheet.module.css";

/** The text area's own cap — `task_injection.MAX_INJECTION_TEXT_CHARS`'s
 *  mirror in this browser, the same rule `TaskVetoForm.tsx`'s `MAX_REASON_CHARS`
 *  follows: a second copy kept here so the field's own `maxLength` agrees with
 *  what the door would refuse anyway. */
const MAX_TASK_TEXT_CHARS = 2000;

/** The "must follow" select's own default — an absent `after` ref, which
 *  `resolve_after_ref` reads as "wherever the planner sees fit". */
const PLANNER_PLACEMENT_VALUE = "";
const PLANNER_PLACEMENT_LABEL = "Let the planner place it";

/** DECISION F028 D7 (2) — a Discard on a plain (non-shortfall) draft never
 *  reaches the door: `answer_injection_shortfall` refuses `draft_not_in_shortfall`
 *  for a draft whose own `status` is `confirmable`, so a confirmable draft has
 *  no server-side "drop" to answer, only its own TTL
 *  (`INJECTION_DRAFT_TTL_SECONDS`) to expire by. This sentence is the client's
 *  own words for that outcome, deliberately NOT imported from
 *  `injectSend.ts`'s own `DROPPED_SENTENCE` — this round's tracked path set
 *  does not open that file, so the two are two words that happen to agree
 *  rather than one shared constant. */
const DISCARD_SENTENCE = "Dropped. This draft will not be added.";

/** DECISION F028 D7 — the "Add Task" sheet: shaped as `LessonsOverlay.tsx` is,
 *  a right-anchored glass dialog that drafts a task from the operator's own
 *  words, shows the draft as sentences through `injectDraftView` alone,
 *  confirms or discards it, and answers a cost shortfall. It reaches the
 *  network only through `api/injectSend.ts`'s three flows — never `fetch(`
 *  itself, the same rule every sending component in this cockpit follows.
 *
 *  ONE RESULT SENTENCE, ALWAYS MOUNTED (finding R-0686's own mechanism, as
 *  `TaskVetoForm.tsx`'s `.editResult` and this panel's `.pauseOutcome` are
 *  mounted): the `<p aria-live="polite">` below is rendered from the very
 *  first paint, empty, so assistive technology registers the live region
 *  before it ever has anything to announce. */
export function AddTaskSheet({ target, tasks, onClose }: {
  target: DecisionSendTarget;
  tasks: readonly RemedyTaskItem[];
  onClose: () => void;
}) {
  const [text, setText] = useState("");
  const [afterId, setAfterId] = useState(PLANNER_PLACEMENT_VALUE);
  const [sending, setSending] = useState(false);
  const [answer, setAnswer] = useState<Record<string, unknown> | null>(null);
  const [resultSentence, setResultSentence] = useState("");
  const [discarded, setDiscarded] = useState(false);

  // Esc closes the sheet, as the reference's sheets and popovers do.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  const view = discarded ? null : injectDraftView(answer);
  const outcomeWord = answer !== null && typeof answer.outcome === "string" ? answer.outcome : "";
  // A confirmed or a dropped body — including this sheet's own client-side
  // Discard, DECISION F028 D7 (2) — ends the flow: the sheet shows only its
  // sentence and the Close button above, never the form or the review again.
  const done = discarded || outcomeWord === "confirmed" || outcomeWord === "dropped";

  async function runSend(sent: Promise<InjectSendOutcome>) {
    setSending(true);
    const outcome = await sent;
    setSending(false);
    setAnswer(outcome.answer);
    setResultSentence(outcome.message.sentence);
  }

  function handleDraft() {
    if (sending || text.trim() === "") return;
    void runSend(sendInjectDraft(target, text, afterId === PLANNER_PLACEMENT_VALUE ? undefined : afterId));
  }

  function handleConfirm() {
    if (sending || view === null || !view.confirmToken) return;
    void runSend(sendInjectConfirm(target, view.confirmToken));
  }

  function handleAnswer(option: string) {
    if (sending || view === null) return;
    void runSend(sendInjectAnswer(target, view.draftId, option));
  }

  function handleDiscard() {
    setDiscarded(true);
    setResultSentence(DISCARD_SENTENCE);
  }

  return (
    <section className={styles.sheet} role="dialog" aria-label="Add a task" data-ui="add-task-sheet">
      <header className={styles.header}>
        <h2>Add a task</h2>
        <button type="button" className={styles.close} onClick={onClose}>Close</button>
      </header>

      {!done && view === null && (
        <div className={styles.form}>
          <label className={styles.field}>
            <span>What should the new task do?</span>
            <textarea
              value={text}
              maxLength={MAX_TASK_TEXT_CHARS}
              onChange={(event: ChangeEvent<HTMLTextAreaElement>) => setText(event.target.value)}
            />
          </label>
          <label className={styles.field}>
            <span>It must follow</span>
            <select value={afterId} onChange={(event: ChangeEvent<HTMLSelectElement>) => setAfterId(event.target.value)}>
              <option value={PLANNER_PLACEMENT_VALUE}>{PLANNER_PLACEMENT_LABEL}</option>
              {tasks.map((task) => (
                <option key={task.id} value={task.id}>{task.label}</option>
              ))}
            </select>
          </label>
          <button
            type="button"
            className={styles.draftPill}
            disabled={sending || text.trim() === ""}
            onClick={handleDraft}
          >
            Draft
          </button>
        </div>
      )}

      {!done && view !== null && (
        <div className={styles.review} data-ui="add-task-review">
          <h3>{view.title}</h3>
          <p className={styles.goal}>{view.goal}</p>
          {view.acceptance.length > 0 && (
            <ul className={styles.acceptance}>
              {view.acceptance.map((line, at) => <li key={at}>{line}</li>)}
            </ul>
          )}
          {view.size !== "" && <p className={styles.detail}>{view.size}</p>}
          {view.placement !== "" && <p className={styles.detail}>{view.placement}</p>}
          {view.cost !== "" && <p className={styles.detail}>{view.cost}</p>}
          {view.fenceWarnings.map((warning, at) => (
            <p key={at} className={styles.fenceWarning}>{warning}</p>
          ))}
          {view.kind === "drafted" ? (
            <div className={styles.actions}>
              <button
                type="button"
                className={styles.confirmPill}
                disabled={sending || !view.confirmToken}
                onClick={handleConfirm}
              >
                Confirm
              </button>
              <button type="button" className={styles.ghostButton} onClick={handleDiscard}>
                Discard
              </button>
            </div>
          ) : (
            <div className={styles.actions} data-ui="add-task-shortfall">
              <p className={styles.question}>{view.question}</p>
              {view.options.map((option) => (
                <button
                  key={option.option}
                  type="button"
                  className={styles.ghostButton}
                  disabled={sending}
                  onClick={() => handleAnswer(option.option)}
                >
                  {option.label}
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      <p aria-live="polite" className={styles.result}>{resultSentence}</p>
    </section>
  );
}

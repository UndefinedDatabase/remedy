import { useEffect, useState } from "react";
import type { DecisionOutcomeMessage } from "../../api/decisionOutcome";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { DiffEnvelope } from "../../api/diffViewModel";
import type { HunkDecisions, HunkState } from "../../api/hunkDecisions";
import { sendHunkDecision } from "../../api/hunkDecisionSend";
import type { HunkDraft } from "../../api/hunkDecisionView";
import {
  hunkControlsBlocked,
  hunkDecisionArgs,
  hunkDraftChanged,
  hunkDraftOf,
  hunkIsDecidable,
  hunkTally,
} from "../../api/hunkDecisionView";
import { loadHunkDecisions } from "../../api/remedyApi";
import styles from "./HunkDecisionPanel.module.css";

/** What the panel says while the recorded decision is in flight. */
const RECORD_PENDING_TEXT = "Reading the decisions already recorded for this change…";
/** What it says for a hunk the server sent no id for. */
const UNNAMED_HUNK_TEXT = "This hunk has no id the server can name, so it cannot be decided here.";

const CHOICES: readonly { state: HunkState; label: string }[] = [
  { state: "approved", label: "Approve" },
  { state: "rejected", label: "Reject" },
  { state: "pending", label: "Undecided" },
];

/**
 * The hunk decisions of one diff (T5_F292 T003, DECISION F292 D7): beside the diff view, one row
 * per hunk with Approve, Reject with a reason, and Undecided, starting from the decision already
 * recorded for the attempt this diff shows (DECISION F292 D6), and Record, which sends the whole
 * decision through `patch.approve-hunks`, because the door replaces the record whole. Every rule
 * it applies lives in `api/hunkDecisionView.ts`; it reads the record through `loadHunkDecisions`
 * and reads it again after a decision is recorded.
 */
export function HunkDecisionPanel({ envelope, target }: { envelope: DiffEnvelope; target: DecisionSendTarget }) {
  const [recorded, setRecorded] = useState<HunkDecisions | null>(null);
  const [draft, setDraft] = useState<HunkDraft>({});
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState<DecisionOutcomeMessage | null>(null);
  const [readCount, setReadCount] = useState(0);

  // THE READ: the record of the attempt this envelope shows, again after every recorded decision.
  // `cancelled` drops an answer that arrives after the diff or the count moved on.
  useEffect(() => {
    let cancelled = false;
    setRecorded(null);
    void loadHunkDecisions({ jobId: target.jobId, token: target.serverToken, taskId: envelope.taskId }).then((read) => {
      if (!cancelled) {
        setRecorded(read);
        setDraft(hunkDraftOf(envelope, read));
      }
    });
    return () => { cancelled = true; };
  }, [envelope, target.jobId, target.serverToken, readCount]);

  const blocked = hunkControlsBlocked(envelope);
  if (blocked !== null) {
    return (
      <section className={styles.panel} aria-label="Hunk decisions" data-ui="hunk-decisions">
        <h3>Hunk decisions</h3>
        <p className={styles.quiet}>{blocked}</p>
      </section>
    );
  }

  const changed = recorded !== null && hunkDraftChanged(envelope, recorded, draft);
  const recordBlocked = sending ? "A decision is being recorded."
    : recorded === null ? RECORD_PENDING_TEXT
      : changed ? null : "Nothing has changed since the last record.";

  function choose(id: string, state: HunkState) {
    setDraft({ ...draft, [id]: { state, reason: draft[id]?.reason ?? "" } });
  }

  async function record() {
    if (recordBlocked !== null) return;
    const decision = hunkDecisionArgs(envelope, draft);
    if ("problem" in decision) {
      setMessage({ tone: "warn", sentence: decision.problem });
      return;
    }
    setSending(true);
    const outcome = await sendHunkDecision(target, decision.args);
    setSending(false);
    setMessage(outcome.message);
    if (outcome.recorded) setReadCount((count) => count + 1);
  }

  return (
    <section className={styles.panel} aria-label="Hunk decisions" data-ui="hunk-decisions">
      <h3>Hunk decisions</h3>
      {recorded === null ? (
        <p className={styles.quiet}>{RECORD_PENDING_TEXT}</p>
      ) : (
        <>
          <p className={styles.tally} data-ui="hunk-tally">{hunkTally(envelope, draft)}</p>
          <ol className={styles.hunks}>
            {envelope.files.flatMap((file) => file.hunks.map((hunk) => (
              <li key={hunk.id} className={styles.hunk} data-hunk-id={hunk.id}>
                <code className={styles.header}>{file.path} {hunk.header}</code>
                {!hunkIsDecidable(hunk.id) ? (
                  <p className={styles.quiet}>{UNNAMED_HUNK_TEXT}</p>
                ) : (
                  <>
                    <div className={styles.choices} role="group" aria-label={`Decision on ${file.path} ${hunk.header}`}>
                      {CHOICES.map((choice) => (
                        <button key={choice.state} type="button"
                          className={draft[hunk.id]?.state === choice.state ? styles.choiceOn : styles.choice}
                          aria-pressed={draft[hunk.id]?.state === choice.state} disabled={sending}
                          onClick={() => choose(hunk.id, choice.state)}>{choice.label}</button>
                      ))}
                    </div>
                    {draft[hunk.id]?.state === "rejected" && (
                      <input type="text" className={styles.reason} aria-label={`Reason for rejecting ${file.path} ${hunk.header}`}
                        placeholder="Why this hunk is rejected" value={draft[hunk.id].reason}
                        onChange={(e) => setDraft({ ...draft, [hunk.id]: { state: "rejected", reason: e.target.value } })} />
                    )}
                  </>
                )}
              </li>
            )))}
          </ol>
        </>
      )}
      <p className={styles.message} role="status" data-ui="hunk-decision-message" data-tone={message?.tone ?? ""}>
        {message?.sentence ?? ""}
      </p>
      <button type="button" className={styles.record} disabled={recordBlocked !== null}
        title={recordBlocked ?? undefined} onClick={() => { void record(); }}>Record decisions</button>
    </section>
  );
}

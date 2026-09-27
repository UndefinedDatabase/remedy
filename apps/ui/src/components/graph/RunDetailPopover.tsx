// The L2 run detail graph_spec.md §10 anchors to its node: the run's verdict,
// round, tokens, duration and retries, and the Diff, Why and Rerun buttons —
// Diff and Why open the L3 evidence panel on their tab (DECISION F023 D5).
// The words come from runDetailModel.ts; this file only loads the task's
// per-round facts through the rounds door and lays the detail out. It sits
// beside the stage's centre, where the L2 camera has just placed the run
// (zoomView.ts), and it is not a dialog: Escape walks the zoom back and
// closes it with the level (DECISION F023 D4).
import { useEffect, useState } from "react";
import { loadTaskRunRounds } from "../../api/remedyApi";
import { sendRerunSubtree } from "../../api/rerunSend";
import { rerunAnswerView } from "../../api/rerunView";
import type { TaskRunRounds } from "../../api/taskRunRounds";
import type { RemedyPromptTraceItem } from "../../api/types";
import type { BrainEventRow, BrainNode } from "./brainOntology";
import { runDetailOf } from "./runDetailModel";
import type { RunFact } from "./runDetailModel";
import type { EvidenceTab } from "./semanticZoom";
import styles from "./RunDetailPopover.module.css";

/** Why Rerun is disabled when it is: DECISION F029 D6 gates the whole feature
 *  on the live page's own server token, the one credential every other send in
 *  this cockpit already requires. */
const RERUN_TOKEN_REASON = "Rerunning needs the live page's server token.";

/** DECISION F029 D6: what the Rerun control shows after a send answers — the
 *  one sentence `rerunAnswerView` or `describeRerunResult` produced, plus
 *  whichever buttons that outcome earns. `null` is "nothing sent yet, or the
 *  operator cancelled". */
type RerunOutcome =
  | { kind: "needs_confirmation"; sentence: string }
  | { kind: "prepared"; sentence: string; runCommand: string }
  | { kind: "message"; sentence: string };

function Fact({ label, fact }: { label: string; fact: RunFact }) {
  return (
    <div className={styles.fact}>
      <dt>{label}</dt>
      {"value" in fact ? <dd>{fact.value}</dd> : <dd className={styles.missing}>{fact.missing}</dd>}
    </div>
  );
}

export function RunDetailPopover({ node, rows, promptItems, jobId, token, onOpenEvidence, onClose }: {
  node: Pick<BrainNode, "id" | "kind" | "state" | "parentId" | "seq" | "meta">;
  rows: readonly BrainEventRow[];
  promptItems: readonly RemedyPromptTraceItem[];
  jobId: string;
  token: string;
  onOpenEvidence: (tab: EvidenceTab) => void;
  onClose: () => void;
}) {
  const taskId = (node.parentId ?? "").replace(/^task:/, "");
  // The report last read, with the task it was read for: a report that arrives
  // after the focus moved to another task's run is never shown under it.
  const [loaded, setLoaded] = useState<TaskRunRounds | null>(null);
  useEffect(() => {
    let cancelled = false;
    void loadTaskRunRounds({ jobId, taskId, token }).then((rounds) => {
      if (!cancelled) setLoaded(rounds);
    });
    return () => { cancelled = true; };
  }, [jobId, taskId, token]);
  const rounds = loaded !== null && loaded.taskId === taskId ? loaded : null;
  const detail = runDetailOf({ node, rows, rounds, promptItems });
  const reasonId = `run-detail-rerun-${node.id}`;

  const [rerunModel, setRerunModel] = useState("");
  const [rerunSending, setRerunSending] = useState(false);
  const [rerunOutcome, setRerunOutcome] = useState<RerunOutcome | null>(null);
  const rerunDisabled = token === "";

  const sendRerun = async (confirmCost: boolean) => {
    if (rerunSending) {
      return;
    }
    setRerunSending(true);
    const outcome = await sendRerunSubtree(
      { jobId, serverToken: token }, taskId, { model: rerunModel, confirmCost });
    setRerunSending(false);
    const answerView = rerunAnswerView(outcome.answer);
    if (answerView === null) {
      setRerunOutcome({ kind: "message", sentence: outcome.message.sentence });
      return;
    }
    setRerunOutcome(answerView.kind === "prepared"
      ? { kind: "prepared", sentence: answerView.sentence, runCommand: answerView.runCommand }
      : { kind: "needs_confirmation", sentence: answerView.sentence });
  };
  const rerunSentence = rerunOutcome === null
    ? null
    : rerunOutcome.kind === "prepared"
      ? `${rerunOutcome.sentence} Run it with: ${rerunOutcome.runCommand}`
      : rerunOutcome.sentence;

  return (
    <aside className={styles.popover} aria-label="Run detail" data-ui="run-detail">
      <header className={styles.header}>
        <div>
          <h3 className={styles.title}>{detail.title}</h3>
          <p className={styles.subtitle}>
            {detail.round !== null ? `Round ${detail.round} of task ${detail.taskId}` : `Task ${detail.taskId}`}
          </p>
        </div>
        <button type="button" className={styles.close} onClick={onClose} aria-label="Close run detail">×</button>
      </header>
      <p className={styles.verdict} data-ui="run-verdict">{detail.verdict}</p>
      <dl className={styles.facts}>
        <Fact label="Tokens" fact={detail.tokens} />
        <Fact label="Duration" fact={detail.duration} />
        <Fact label="Retries" fact={detail.retries} />
      </dl>
      <label className={styles.modelField}>
        <span>Model for the rerun (optional)</span>
        <input
          type="text"
          maxLength={128}
          value={rerunModel}
          onChange={(event) => setRerunModel(event.target.value)}
        />
      </label>
      <div className={styles.actions}>
        <button type="button" className={styles.action} onClick={() => onOpenEvidence("diff")}>Open diff</button>
        <button
          type="button"
          className={styles.action}
          disabled={detail.promptItemId === null}
          title={detail.promptItemId === null ? "No prompt was recorded for this run." : undefined}
          onClick={() => { if (detail.promptItemId !== null) onOpenEvidence("prompt"); }}
        >
          Why
        </button>
        <button
          type="button"
          className={styles.action}
          disabled={rerunDisabled || rerunSending}
          title={rerunDisabled ? RERUN_TOKEN_REASON : undefined}
          aria-describedby={rerunDisabled ? reasonId : undefined}
          onClick={() => void sendRerun(false)}
        >
          Rerun
        </button>
      </div>
      {rerunDisabled && <p id={reasonId} className={styles.reason}>{RERUN_TOKEN_REASON}</p>}
      {rerunSentence !== null && <p className={styles.rerunOutcome} aria-live="polite">{rerunSentence}</p>}
      {rerunOutcome?.kind === "needs_confirmation" && (
        <div className={styles.actions}>
          <button
            type="button"
            className={styles.action}
            disabled={rerunSending}
            onClick={() => void sendRerun(true)}
          >
            Rerun anyway
          </button>
          <button
            type="button"
            className={styles.action}
            disabled={rerunSending}
            onClick={() => setRerunOutcome(null)}
          >
            Cancel
          </button>
        </div>
      )}
    </aside>
  );
}

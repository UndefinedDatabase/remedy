// The L2 run detail graph_spec.md §10 anchors to its node: the run's verdict,
// round, tokens, duration and retries, and the Diff, Why and Rerun buttons.
// The words come from runDetailModel.ts; this file only loads the task's
// per-round facts through the rounds door and lays the detail out. It sits
// beside the stage's centre, where the L2 camera has just placed the run
// (zoomView.ts), and it is not a dialog: Escape walks the zoom back and
// closes it with the level (DECISION F023 D4).
import { useEffect, useState } from "react";
import { loadTaskRunRounds } from "../../api/remedyApi";
import type { TaskRunRounds } from "../../api/taskRunRounds";
import type { RemedyPromptTraceItem } from "../../api/types";
import type { BrainEventRow, BrainNode } from "./brainOntology";
import { runDetailOf } from "./runDetailModel";
import type { RunFact } from "./runDetailModel";
import styles from "./RunDetailPopover.module.css";

/** Why Rerun is disabled: no command the dashboard may send re-runs one step. */
export const RERUN_NOT_YET = "Running one step again is not offered from the dashboard yet.";

function Fact({ label, fact }: { label: string; fact: RunFact }) {
  return (
    <div className={styles.fact}>
      <dt>{label}</dt>
      {"value" in fact ? <dd>{fact.value}</dd> : <dd className={styles.missing}>{fact.missing}</dd>}
    </div>
  );
}

export function RunDetailPopover({ node, rows, promptItems, jobId, token, onOpenDiff, onOpenPrompt, onClose }: {
  node: Pick<BrainNode, "id" | "kind" | "state" | "parentId" | "seq" | "meta">;
  rows: readonly BrainEventRow[];
  promptItems: readonly RemedyPromptTraceItem[];
  jobId: string;
  token: string;
  onOpenDiff: (taskId: string) => void;
  onOpenPrompt: (promptItemId: string) => void;
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
      <div className={styles.actions}>
        <button type="button" className={styles.action} onClick={() => onOpenDiff(detail.taskId)}>Open diff</button>
        <button
          type="button"
          className={styles.action}
          disabled={detail.promptItemId === null}
          title={detail.promptItemId === null ? "No prompt was recorded for this run." : undefined}
          onClick={() => { if (detail.promptItemId !== null) onOpenPrompt(detail.promptItemId); }}
        >
          Why
        </button>
        <button type="button" className={styles.action} disabled title={RERUN_NOT_YET} aria-describedby={reasonId}>
          Rerun
        </button>
      </div>
      <p id={reasonId} className={styles.reason}>{RERUN_NOT_YET}</p>
    </aside>
  );
}

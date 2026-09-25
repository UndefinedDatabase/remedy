import { useState, type FormEvent } from "react";
import type { DecisionSendTarget } from "../../api/decisionSend";
import { sendTaskEdit } from "../../api/taskEditSend";
import { changedTaskFields, type TaskEditAction } from "../../api/taskSpecView";
import styles from "./DetailPopover.module.css";

/** DECISION F026 D4 clause 1 — the size bands `task_edit_runtime.py` accepts
 *  for `est_tokens_band` (the same closed set the plan itself is authored
 *  against): S, M, L, XL, in that order. */
const SIZE_BANDS = ["S", "M", "L", "XL"] as const;

const RELAUNCH_NOTE =
  "Saving puts this task back in the queue; relaunch the job to run it.";

/** DECISION F026 D4 clauses 1 and 2 — the "Edit task" affordance: closed, a
 *  ghost button; open, a form prefilled from `action.current`, sending only
 *  what changed through `sendTaskEdit`. Mounted by `DetailPopover.tsx` ONLY
 *  when `taskEditAction(dashboard, task.id)` answers non-null, so this
 *  component itself never re-derives eligibility — it trusts the action it
 *  was handed. `jobId` names the job the relaunch note and the send both
 *  belong to; `target` carries the credential `sendTaskEdit` spends. */
export function TaskEditForm({ target, jobId, action }: {
  target: DecisionSendTarget;
  jobId: string;
  action: TaskEditAction;
}) {
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState(action.current.title);
  const [goal, setGoal] = useState(action.current.goal);
  const [band, setBand] = useState(action.current.estTokensBand);
  const [acceptance, setAcceptance] = useState(action.current.acceptance.join("\n"));
  const [files, setFiles] = useState(action.current.filesHint.join("\n"));
  const [sending, setSending] = useState(false);
  const [resultSentence, setResultSentence] = useState("");

  if (!open) {
    return (
      <button type="button" className={styles.ghostButton} onClick={() => setOpen(true)}>
        Edit task
      </button>
    );
  }

  const draft = { title, goal, band, acceptance, files };
  const fields = changedTaskFields(action.current, draft);
  const disabled = Object.keys(fields).length === 0 || sending;

  async function handleSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (disabled) return;
    setSending(true);
    const message = await sendTaskEdit(target, action.taskId, fields, action.specVersion);
    setSending(false);
    setResultSentence(message.sentence);
  }

  function handleCancel() {
    setOpen(false);
    setResultSentence("");
  }

  return (
    <form className={styles.editForm} aria-label="Edit task" data-ui="task-edit-form"
          data-job-id={jobId} onSubmit={handleSave}>
      <h3>Edit task</h3>

      <label className={styles.editField}>
        <span>Title</span>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} />
      </label>

      <label className={styles.editField}>
        <span>Goal</span>
        <textarea value={goal} onChange={(e) => setGoal(e.target.value)} />
      </label>

      <label className={styles.editField}>
        <span>Acceptance, one per line</span>
        <textarea value={acceptance} onChange={(e) => setAcceptance(e.target.value)} />
      </label>

      <label className={styles.editField}>
        <span>Size band</span>
        <select value={band} onChange={(e) => setBand(e.target.value)}>
          {SIZE_BANDS.map((b) => <option key={b} value={b}>{b}</option>)}
        </select>
      </label>

      <label className={styles.editField}>
        <span>Files, one per line</span>
        <textarea value={files} onChange={(e) => setFiles(e.target.value)} />
      </label>

      {action.editState === "failed" && <p className={styles.editNote}>{RELAUNCH_NOTE}</p>}

      <div className={styles.editActions}>
        <button type="submit" className={styles.savePill} disabled={disabled}>Save</button>
        <button type="button" className={styles.ghostButton} onClick={handleCancel}>Cancel</button>
      </div>

      <p aria-live="polite" className={styles.editResult}>{resultSentence}</p>
    </form>
  );
}

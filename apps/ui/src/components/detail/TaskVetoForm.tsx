import { useState, type FormEvent } from "react";
import type { DecisionSendTarget } from "../../api/decisionSend";
import { sendVetoTask } from "../../api/vetoSend";
import type { TaskVetoAction } from "../../api/vetoView";
import styles from "./DetailPopover.module.css";

/** The reason's own maximum length — `task_veto.MAX_VETO_REASON_CHARS`'s
 *  mirror in this browser, the same rule `taskSpecView.ts`'s size bands
 *  follow: a second copy kept here so the input's own `maxLength` agrees with
 *  what the door would refuse anyway. */
const MAX_REASON_CHARS = 500;

const VETO_NOTE =
  "A veto cannot be undone. Tasks that depend on this one will not run, and a "
  + "replan proposal goes to the decision inbox.";

/** DECISION F027 D8 (4) — the "Veto task" affordance: closed, a ghost button;
 *  open, a form with one required reason, sending it through `sendVetoTask`.
 *  Mounted by `DetailPopover.tsx` ONLY when `taskVetoAction(dashboard,
 *  task.id)` answers non-null, so this component never re-derives
 *  eligibility — it trusts the action it was handed, `TaskEditForm.tsx`'s own
 *  rule. */
export function TaskVetoForm({ target, action }: {
  target: DecisionSendTarget;
  action: TaskVetoAction;
}) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");
  const [sending, setSending] = useState(false);
  const [resultSentence, setResultSentence] = useState("");

  if (!open) {
    return (
      <button type="button" className={styles.ghostButton} onClick={() => setOpen(true)}>
        Veto task
      </button>
    );
  }

  const disabled = reason.trim() === "" || sending;

  async function handleSend(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (disabled) return;
    setSending(true);
    const message = await sendVetoTask(target, action.taskId, reason);
    setSending(false);
    setResultSentence(message.sentence);
  }

  function handleCancel() {
    setOpen(false);
    setResultSentence("");
  }

  return (
    <form className={styles.editForm} aria-label="Veto task" data-ui="task-veto-form" onSubmit={handleSend}>
      <h3>Veto task</h3>

      <label className={styles.editField}>
        <span>Reason (required)</span>
        <input
          type="text"
          value={reason}
          maxLength={MAX_REASON_CHARS}
          onChange={(e) => setReason(e.target.value)}
        />
      </label>

      <p className={styles.editNote}>{VETO_NOTE}</p>

      <div className={styles.editActions}>
        <button type="submit" className={styles.savePill} disabled={disabled}>Veto</button>
        <button type="button" className={styles.ghostButton} onClick={handleCancel}>Cancel</button>
      </div>

      <p aria-live="polite" className={styles.editResult}>{resultSentence}</p>
    </form>
  );
}

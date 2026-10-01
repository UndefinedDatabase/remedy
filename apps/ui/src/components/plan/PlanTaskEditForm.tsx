import { useState, type FormEvent } from "react";
import type { PlanTaskFields } from "../../api/planEditSend";
import {
  PLAN_TOKEN_BANDS,
  changedPlanTaskFields,
  planTaskDraftOf,
  planTaskDraftProblem,
} from "../../api/planEditView";
import type { RemedyPlanTask } from "../../api/types";
import styles from "./PlanView.module.css";

/**
 * One planned task's edit form (T5_F292 T002, DECISION F292 D3): its title, goal and size,
 * prefilled from the task as the plan view shows it. Save hands only the changed fields to the
 * plan view, which sends them against the version it shows; a draft that is incomplete or
 * changes nothing is answered here and never sent. `blockedReason` is the plan view's own
 * reason the controls cannot be used right now, or `null`.
 */
export function PlanTaskEditForm({ task, blockedReason, onSave, onCancel }: {
  task: RemedyPlanTask;
  blockedReason: string | null;
  onSave: (fields: PlanTaskFields) => void;
  onCancel: () => void;
}) {
  const [draft, setDraft] = useState(() => planTaskDraftOf(task));
  const [problem, setProblem] = useState<string | null>(null);

  function handleSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (blockedReason !== null) return;
    const wrong = planTaskDraftProblem(draft);
    if (wrong !== null) {
      setProblem(wrong);
      return;
    }
    const fields = changedPlanTaskFields(task, draft);
    if (Object.keys(fields).length === 0) {
      setProblem("Nothing changed.");
      return;
    }
    setProblem(null);
    onSave(fields);
  }

  return (
    <form className={styles.form} aria-label={`Edit ${task.id}`} data-ui="plan-task-form" onSubmit={handleSave}>
      <label className={styles.field}>
        <span>Title</span>
        <input type="text" value={draft.title} onChange={(e) => setDraft({ ...draft, title: e.target.value })} />
      </label>
      <label className={styles.field}>
        <span>Goal</span>
        <textarea value={draft.goal} onChange={(e) => setDraft({ ...draft, goal: e.target.value })} />
      </label>
      <label className={styles.field}>
        <span>Size</span>
        <select value={draft.band} onChange={(e) => setDraft({ ...draft, band: e.target.value })}>
          {PLAN_TOKEN_BANDS.map((band) => <option key={band} value={band}>{band}</option>)}
        </select>
      </label>
      <div className={styles.formActions}>
        <button type="submit" className={styles.save} disabled={blockedReason !== null}
          title={blockedReason ?? undefined}>Save</button>
        <button type="button" className={styles.ghost} onClick={onCancel}>Cancel</button>
      </div>
      {problem !== null && <p className={styles.problem} role="alert">{problem}</p>}
    </form>
  );
}

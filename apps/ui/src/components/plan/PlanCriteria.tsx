import { useState, type FormEvent } from "react";
import type { PlanEdit } from "../../api/planEditSend";
import { planEditAcceptanceEdit } from "../../api/planEditSend";
import { planCriterionProblem, planCriterionRemoveBlocked } from "../../api/planEditView";
import type { RemedyPlanTask } from "../../api/types";
import styles from "./PlanView.module.css";

/**
 * One planned task's acceptance criteria (T5_F292 T001 and T002, DECISIONS F292 D2 and D4), each
 * under the index the plan edits address. While the plan is open for editing (`editable`), each
 * criterion can be changed or removed and a criterion can be added at the end; `open` is the
 * criterion whose form is open — its index, `null` for the add form, `undefined` for none — and
 * the plan view owns it, so one control is open at a time across the whole plan.
 */
export function PlanCriteria({ task, editable, open, blockedReason, onOpen, onSubmit }: {
  task: RemedyPlanTask;
  editable: boolean;
  open: number | null | undefined;
  blockedReason: string | null;
  onOpen: (index: number | null | undefined) => void;
  onSubmit: (edit: PlanEdit) => void;
}) {
  const removeBlocked = blockedReason ?? planCriterionRemoveBlocked(task);
  return (
    <>
      <ol className={styles.criteria} aria-label={`Acceptance criteria of ${task.id}`}>
        {task.acceptance.map((criterion, index) => (
          <li key={index} className={styles.criterion}>
            <span className={styles.index}>{index}</span>
            {open === index ? (
              <CriterionForm initial={criterion} label={`Change criterion ${index} of ${task.id}`}
                blockedReason={blockedReason} onCancel={() => onOpen(undefined)}
                onSave={(text) => onSubmit(planEditAcceptanceEdit(task.id, "edit", index, text))} />
            ) : (
              <span>{criterion}</span>
            )}
            {editable && open !== index && (
              <span className={styles.criterionActions}>
                <button type="button" className={styles.mini} disabled={blockedReason !== null}
                  title={blockedReason ?? undefined} aria-label={`Change criterion ${index} of ${task.id}`}
                  onClick={() => onOpen(index)}>Change</button>
                <button type="button" className={styles.mini} disabled={removeBlocked !== null}
                  title={removeBlocked ?? undefined} aria-label={`Remove criterion ${index} of ${task.id}`}
                  onClick={() => onSubmit(planEditAcceptanceEdit(task.id, "remove", index, ""))}>Remove</button>
              </span>
            )}
          </li>
        ))}
      </ol>
      {editable && (open === null ? (
        <CriterionForm initial="" label={`Add a criterion to ${task.id}`} blockedReason={blockedReason}
          onCancel={() => onOpen(undefined)}
          onSave={(text) => onSubmit(planEditAcceptanceEdit(task.id, "add", null, text))} />
      ) : (
        <button type="button" className={styles.mini} disabled={blockedReason !== null}
          title={blockedReason ?? undefined} onClick={() => onOpen(null)}>Add a criterion</button>
      ))}
    </>
  );
}

/** The one-line form a criterion is written in: Save hands the trimmed text on, unless it is
 *  empty or unchanged, which is answered here and never sent. */
function CriterionForm({ initial, label, blockedReason, onSave, onCancel }: {
  initial: string;
  label: string;
  blockedReason: string | null;
  onSave: (text: string) => void;
  onCancel: () => void;
}) {
  const [text, setText] = useState(initial);
  const [problem, setProblem] = useState<string | null>(null);

  function handleSave(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (blockedReason !== null) return;
    const wrong = planCriterionProblem(text);
    if (wrong !== null) {
      setProblem(wrong);
      return;
    }
    if (text.trim() === initial) {
      setProblem("Nothing changed.");
      return;
    }
    setProblem(null);
    onSave(text.trim());
  }

  return (
    <form className={styles.criterionForm} aria-label={label} data-ui="plan-criterion-form" onSubmit={handleSave}>
      <input type="text" aria-label={label} value={text} onChange={(e) => setText(e.target.value)} />
      <button type="submit" className={styles.save} disabled={blockedReason !== null}
        title={blockedReason ?? undefined}>Save</button>
      <button type="button" className={styles.ghost} onClick={onCancel}>Cancel</button>
      {problem !== null && <p className={styles.problem} role="alert">{problem}</p>}
    </form>
  );
}

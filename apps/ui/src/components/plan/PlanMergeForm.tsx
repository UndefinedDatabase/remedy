import { useState, type FormEvent } from "react";
import { planMergeIds, planMergeSummary } from "../../api/planEditView";
import type { RemedyPlan, RemedyPlanTask } from "../../api/types";
import styles from "./PlanView.module.css";

/**
 * The merge form of one planned task (T5_F292 T002, DECISION F292 D5): the plan's other tasks to
 * choose from, and, once one is chosen, what the merge will do in one sentence. Merge hands the
 * chosen tasks, in plan order with this one, to the plan view, which sends them against the
 * version it shows; a merge with nothing chosen is answered here and never sent.
 */
export function PlanMergeForm({ plan, task, blockedReason, onMerge, onCancel }: {
  plan: RemedyPlan;
  task: RemedyPlanTask;
  blockedReason: string | null;
  onMerge: (taskIds: string[]) => void;
  onCancel: () => void;
}) {
  const [chosen, setChosen] = useState<string[]>([]);
  const [problem, setProblem] = useState<string | null>(null);
  const ids = planMergeIds(plan, task.id, chosen);
  const summary = planMergeSummary(plan, ids);

  function toggle(id: string) {
    setChosen(chosen.includes(id) ? chosen.filter((c) => c !== id) : [...chosen, id]);
    setProblem(null);
  }

  function handleMerge(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (blockedReason !== null) return;
    if ("problem" in summary) {
      setProblem(summary.problem);
      return;
    }
    onMerge(ids);
  }

  return (
    <form className={styles.form} aria-label={`Merge ${task.id}`} data-ui="plan-merge-form" onSubmit={handleMerge}>
      <fieldset className={styles.choices}>
        <legend>Merge {task.id} with</legend>
        {plan.tasks.filter((other) => other.id !== task.id).map((other) => (
          <label key={other.id} className={styles.choice}>
            <input type="checkbox" checked={chosen.includes(other.id)} onChange={() => toggle(other.id)} />
            <span>{other.id} — {other.title}</span>
          </label>
        ))}
      </fieldset>
      {"text" in summary && <p className={styles.preview} data-ui="plan-merge-preview">{summary.text}</p>}
      <div className={styles.formActions}>
        <button type="submit" className={styles.save} disabled={blockedReason !== null}
          title={blockedReason ?? undefined}>Merge tasks</button>
        <button type="button" className={styles.ghost} onClick={onCancel}>Cancel</button>
      </div>
      {problem !== null && <p className={styles.problem} role="alert">{problem}</p>}
    </form>
  );
}

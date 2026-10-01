import { useState, type FormEvent } from "react";
import { planSplitDefaultParts, planSplitPartition, planSplitSummary } from "../../api/planEditView";
import type { RemedyPlan, RemedyPlanTask } from "../../api/types";
import styles from "./PlanView.module.css";

/**
 * The split form of one planned task (T5_F292 T002, DECISION F292 D5): each criterion with the
 * part it goes into, and what the split will do in one sentence. It opens with the last
 * criterion in a second part, so it starts on a split the planner would take. Split hands the
 * partition to the plan view, which sends it against the version it shows; a partition with one
 * part is answered here and never sent.
 */
export function PlanSplitForm({ plan, task, blockedReason, onSplit, onCancel }: {
  plan: RemedyPlan;
  task: RemedyPlanTask;
  blockedReason: string | null;
  onSplit: (partition: number[][]) => void;
  onCancel: () => void;
}) {
  const [parts, setParts] = useState<number[]>(() => planSplitDefaultParts(task));
  const [problem, setProblem] = useState<string | null>(null);
  const partition = planSplitPartition(parts);
  const summary = planSplitSummary(plan, task, partition);
  const choices = task.acceptance.map((_, index) => index + 1);

  function handleSplit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (blockedReason !== null) return;
    if ("problem" in summary) {
      setProblem(summary.problem);
      return;
    }
    onSplit(partition);
  }

  return (
    <form className={styles.form} aria-label={`Split ${task.id}`} data-ui="plan-split-form" onSubmit={handleSplit}>
      <fieldset className={styles.choices}>
        <legend>Which part each criterion goes into</legend>
        {task.acceptance.map((criterion, index) => (
          <label key={index} className={styles.choice}>
            <select value={parts[index]} aria-label={`Part of criterion ${index}`}
              onChange={(e) => { setParts(parts.map((p, at) => (at === index ? Number(e.target.value) : p))); setProblem(null); }}>
              {choices.map((part) => <option key={part} value={part}>Part {part}</option>)}
            </select>
            <span>{criterion}</span>
          </label>
        ))}
      </fieldset>
      {"text" in summary && <p className={styles.preview} data-ui="plan-split-preview">{summary.text}</p>}
      <div className={styles.formActions}>
        <button type="submit" className={styles.save} disabled={blockedReason !== null}
          title={blockedReason ?? undefined}>Split task</button>
        <button type="button" className={styles.ghost} onClick={onCancel}>Cancel</button>
      </div>
      {problem !== null && <p className={styles.problem} role="alert">{problem}</p>}
    </form>
  );
}

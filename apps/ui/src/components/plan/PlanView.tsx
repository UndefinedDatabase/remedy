import { useEffect } from "react";
import type { RemedyPlan } from "../../api/types";
import {
  PLAN_ABSENT_TEXT,
  PLAN_UNREADABLE_TEXT,
  planBody,
  planDependencyText,
  planEntryText,
  planHeadline,
  planWindowText,
} from "../../api/planView";
import styles from "./PlanView.module.css";

/**
 * The plan view (T5_F292 T001, DECISION F292 D2): the job's stored plan as the dashboard's `plan`
 * section serves it, the same read `remedy job plan-show --json` prints — its version and
 * approval, whether it is open for editing, and each planned task with what it waits for and its
 * acceptance criteria under the index the plan edits address. It reads the dashboard it is given
 * and sends nothing; every sentence it shows is decided in `api/planView.ts`.
 */
export function PlanView({ plan, onClose }: { plan: RemedyPlan; onClose: () => void }) {
  // Esc closes the view, as the reference's sheets and popovers do.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  const body = planBody(plan);
  return (
    <section className={styles.overlay} role="dialog" aria-label="Plan" data-ui="plan-view">
      <header className={styles.header}>
        <h2>Plan</h2>
        <button type="button" className={styles.close} onClick={onClose}>Close plan</button>
      </header>
      {body === "unreadable" ? (
        <p className={styles.quiet}>{PLAN_UNREADABLE_TEXT}</p>
      ) : body === "absent" ? (
        <p className={styles.quiet}>{PLAN_ABSENT_TEXT}</p>
      ) : (
        <div className={styles.body}>
          <p className={styles.headline} data-ui="plan-headline">{planHeadline(plan)}</p>
          <p className={plan.editable ? styles.windowOpen : styles.window} data-ui="plan-window">
            {planWindowText(plan)}
          </p>
          <ol className={styles.tasks} aria-label="Planned tasks">
            {plan.tasks.map((task) => (
              <li key={task.id} className={styles.task} data-plan-task={task.id}>
                <div className={styles.taskHead}>
                  <span className={styles.taskId}>{task.id}</span>
                  <span className={styles.taskTitle}>{task.title}</span>
                  {task.estTokensBand !== "" && <span className={styles.band}>Size {task.estTokensBand}</span>}
                </div>
                {task.goal !== "" && <p className={styles.goal}>{task.goal}</p>}
                <p className={styles.meta}>{planDependencyText(task)} · {planEntryText(task)}</p>
                <ol className={styles.criteria} aria-label={`Acceptance criteria of ${task.id}`}>
                  {task.acceptance.map((criterion, index) => (
                    <li key={index} className={styles.criterion}>
                      <span className={styles.index}>{index}</span>
                      <span>{criterion}</span>
                    </li>
                  ))}
                </ol>
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  );
}

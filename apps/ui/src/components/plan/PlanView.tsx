import { useEffect, useState } from "react";
import type { DecisionOutcomeMessage } from "../../api/decisionOutcome";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { PlanEdit } from "../../api/planEditSend";
import { planDeleteTaskEdit, planEditTaskEdit, sendPlanEdit } from "../../api/planEditSend";
import type { PlanEditGate } from "../../api/planEditView";
import { planDeleteQuestion, planEditBlockedReason } from "../../api/planEditView";
import type { RemedyPlan, RemedyPlanTask } from "../../api/types";
import {
  PLAN_ABSENT_TEXT,
  PLAN_UNREADABLE_TEXT,
  planBody,
  planDependencyText,
  planEntryText,
  planHeadline,
  planWindowText,
} from "../../api/planView";
import { PlanTaskEditForm } from "./PlanTaskEditForm";
import styles from "./PlanView.module.css";

/** Which control a task has open: its edit form, or the question its delete asks first. */
type OpenControl = { taskId: string; kind: "fields" | "delete" } | null;

/**
 * The plan view (T5_F292 T001 and T002, DECISIONS F292 D2 and D3): the job's stored plan as the
 * dashboard's `plan` section serves it, the same read `remedy job plan-show --json` prints — its
 * version and approval, whether it is open for editing, and each planned task with what it waits
 * for and its acceptance criteria under the index the plan edits address. While the plan is open
 * for editing, each task can be edited or deleted; every edit is sent against the version shown
 * through `sendPlanEdit`, its outcome is said in one sentence, and an accepted edit asks the
 * cockpit to read the dashboard again (`onReload`). Every sentence and rule it shows is decided
 * in `api/planView.ts` and `api/planEditView.ts`.
 */
export function PlanView({ plan, target, onReload, onClose }: {
  plan: RemedyPlan;
  target: DecisionSendTarget;
  onReload?: () => void;
  onClose: () => void;
}) {
  const [gate, setGate] = useState<PlanEditGate>({ sending: false, awaitingVersion: null });
  const [message, setMessage] = useState<DecisionOutcomeMessage | null>(null);
  const [open, setOpen] = useState<OpenControl>(null);

  // Esc closes the view, as the reference's sheets and popovers do.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  const blockedReason = planEditBlockedReason(plan, gate);

  async function submit(edit: PlanEdit) {
    if (blockedReason !== null) return;
    setGate({ sending: true, awaitingVersion: gate.awaitingVersion });
    const outcome = await sendPlanEdit(target, edit, plan.version);
    setMessage(outcome.message);
    setGate({ sending: false, awaitingVersion: outcome.version ?? gate.awaitingVersion });
    if (outcome.version !== null) {
      setOpen(null);
      onReload?.();
    }
  }

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
          <p className={styles.message} role="status" data-ui="plan-edit-message" data-tone={message?.tone ?? ""}>
            {message?.sentence ?? ""}
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
                {plan.editable && (
                  <TaskControls plan={plan} task={task} open={open} blockedReason={blockedReason}
                    onOpen={setOpen} onSubmit={submit} />
                )}
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  );
}

function TaskControls({ plan, task, open, blockedReason, onOpen, onSubmit }: {
  plan: RemedyPlan;
  task: RemedyPlanTask;
  open: OpenControl;
  blockedReason: string | null;
  onOpen: (control: OpenControl) => void;
  onSubmit: (edit: PlanEdit) => void;
}) {
  const mine = open !== null && open.taskId === task.id ? open.kind : null;
  if (mine === "fields") {
    return (
      <PlanTaskEditForm task={task} blockedReason={blockedReason}
        onSave={(fields) => onSubmit(planEditTaskEdit(task.id, fields))} onCancel={() => onOpen(null)} />
    );
  }
  if (mine === "delete") {
    return (
      <div className={styles.confirm} role="group" aria-label={`Delete ${task.id}`} data-ui="plan-delete-confirm">
        <p>{planDeleteQuestion(plan, task)}</p>
        <div className={styles.formActions}>
          <button type="button" className={styles.danger} disabled={blockedReason !== null}
            title={blockedReason ?? undefined} onClick={() => onSubmit(planDeleteTaskEdit(task.id))}>Delete task</button>
          <button type="button" className={styles.ghost} onClick={() => onOpen(null)}>Keep it</button>
        </div>
      </div>
    );
  }
  return (
    <div className={styles.actions}>
      <button type="button" className={styles.ghost} disabled={blockedReason !== null} title={blockedReason ?? undefined}
        onClick={() => onOpen({ taskId: task.id, kind: "fields" })}>Edit</button>
      <button type="button" className={styles.ghost} disabled={blockedReason !== null} title={blockedReason ?? undefined}
        onClick={() => onOpen({ taskId: task.id, kind: "delete" })}>Delete</button>
    </div>
  );
}

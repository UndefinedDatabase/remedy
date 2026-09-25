import { useState } from "react";
import type { DecisionSendTarget } from "../../api/decisionSend";
import type { DecisionOutcomeMessage, DecisionOutcomeTone } from "../../api/decisionOutcome";
import { JOB_PAUSE_COMMAND_ID, JOB_UNPAUSE_COMMAND_ID, sendPauseCommand } from "../../api/pauseSend";
import { pauseActionLabel, type PauseAction } from "../../api/pauseView";
import styles from "./RightLivePanel.module.css";

/** The tone of the last send, toned the way `ChatInput.tsx` tones its own
 *  outcome line. */
const OUTCOME_CLASS: Record<DecisionOutcomeTone, string> = {
  ok: styles.pauseOutcomeOk,
  warn: styles.pauseOutcomeWarn,
  error: styles.pauseOutcomeError,
};

/** THE PAUSE/RESUME CONTROL (DECISION F025 D4): one button and its sentence,
 *  mounted below the NowCard for the job and inside `DetailPopover` for a
 *  task. It reaches the network only through `api/pauseSend.ts`'s flow, and
 *  holds only whether a send is in flight and the last sentence — the same
 *  shape `ChatInput.tsx` holds for the steering input. `scope` is `"job"` for
 *  the job's own control, or the task id for one task's; `action` is
 *  `api/pauseView.ts`'s own answer, and `null` renders nothing at all, so a
 *  job that is not running and a task that is done offer no control. */
export function PauseControl({ target, scope, action }: {
  target: DecisionSendTarget;
  scope: "job" | string;
  action: PauseAction | null;
}) {
  const [sending, setSending] = useState(false);
  const [outcome, setOutcome] = useState<DecisionOutcomeMessage | null>(null);

  if (action === null) {
    return null;
  }

  const isJob = scope === "job";
  const label = pauseActionLabel(isJob ? "job" : "task", action);
  const command = action === "pause" ? JOB_PAUSE_COMMAND_ID : JOB_UNPAUSE_COMMAND_ID;
  const taskId = isJob ? undefined : scope;

  const send = async () => {
    if (sending) {
      return;
    }
    setSending(true);
    const answer = await sendPauseCommand(target, command, taskId);
    setSending(false);
    setOutcome(answer);
  };

  return (
    <div className={styles.pauseControl}>
      <button type="button" className={styles.pauseButton} disabled={sending} onClick={() => void send()}>
        {label}
      </button>
      <p
        className={outcome ? `${styles.pauseOutcome} ${OUTCOME_CLASS[outcome.tone]}` : styles.pauseOutcome}
        aria-live="polite"
      >
        {outcome ? outcome.sentence : ""}
      </p>
    </div>
  );
}

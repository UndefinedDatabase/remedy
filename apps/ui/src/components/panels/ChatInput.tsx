import { useState } from "react";
import type { DecisionOutcomeMessage, DecisionOutcomeTone } from "../../api/decisionOutcome";
import styles from "./RightLivePanel.module.css";

/** The tone of the last send, as the class the outcome line wears. */
const OUTCOME_CLASS: Record<DecisionOutcomeTone, string> = {
  ok: styles.chatOutcomeOk,
  warn: styles.chatOutcomeWarn,
  error: styles.chatOutcomeError,
};

/** The steering input (T5_F264, DECISION F264 D3), where ux_spec.md §11.3 places it:
 *  the bottom of the activity card.
 *
 *  It is LIVE only when the card hands it an `onSend` and does not disable it; a
 *  disabled input stays visible with its honest reason, because the design
 *  reference's rule is visible honesty over hidden UI. Every rule about what may be
 *  sent and what a reply means lives in `api/steeringSend.ts`; this component holds
 *  only what the operator typed, whether a send is in flight, and the last sentence.
 *  The text is cleared only after the job ACCEPTED it, so a refused message is
 *  never lost. `placeholder` and `hint` are the card's own copy (F030 T003,
 *  DECISION F030 D3): this component renders them and decides nothing about what
 *  they say. */
export function ChatInput({ disabled, reason, onSend, placeholder, hint }: {
  disabled: boolean;
  reason: string;
  onSend?: (text: string) => Promise<DecisionOutcomeMessage>;
  placeholder?: string;
  hint?: string;
}) {
  const [text, setText] = useState("");
  const [sending, setSending] = useState(false);
  const [outcome, setOutcome] = useState<DecisionOutcomeMessage | null>(null);
  const inert = disabled || onSend === undefined;
  const busy = inert || sending;

  const send = async () => {
    if (busy || onSend === undefined || text.trim() === "") {
      return;
    }
    setSending(true);
    const answer = await onSend(text);
    setSending(false);
    setOutcome(answer);
    if (answer.tone === "ok") {
      setText("");
    }
  };

  return (
    <div className={styles.chatInputRow} data-ui="chat-input-row">
      <input
        className={styles.chatInput}
        type="text"
        placeholder={placeholder}
        value={text}
        onChange={(event) => setText(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            void send();
          }
        }}
        disabled={inert}
        title={inert ? reason : hint}
        aria-describedby={inert ? "remedy-chat-input-reason" : undefined}
      />
      <button
        type="button"
        className={styles.chatSend}
        disabled={busy}
        title={inert ? reason : undefined}
        aria-label="Send"
        onClick={() => void send()}
      >
        ↑
      </button>
      {inert ? (
        <p id="remedy-chat-input-reason" className={styles.chatInputReason}>{reason}</p>
      ) : (
        <p className={outcome ? `${styles.chatOutcome} ${OUTCOME_CLASS[outcome.tone]}` : styles.chatOutcome}
          aria-live="polite">
          {outcome ? outcome.sentence : ""}
        </p>
      )}
    </div>
  );
}

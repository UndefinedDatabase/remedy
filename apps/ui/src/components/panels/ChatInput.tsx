import styles from "./RightLivePanel.module.css";

/** The steering input, rendered but DISABLED until its backing feature exists.
 *
 *  Remedy deliberately ships this VISIBLE AND INERT rather than hiding it.
 *  ux_spec.md §11.3 places it at the bottom of the activity card, and the
 *  design reference's rule for a not-yet feature is visible honesty over
 *  hidden UI: a reader who can see the box and read why it is off learns
 *  something a missing box would have hidden.
 *
 *  `onSend` is declared and deliberately NOT destructured. component_spec.md
 *  ("SteeringInput / ChatInput") fixes the props so that enabling this later
 *  is a change here and not at every call site, but this component cannot
 *  honestly call a handler while it has no text to send — it holds no state,
 *  because a disabled input has nothing to hold. F030 adds the state and the
 *  call together; `noUnusedLocals` is why the binding is absent rather than
 *  unused. */
export function ChatInput({ disabled, reason }: {
  disabled: boolean;
  reason: string;
  onSend?: (text: string) => void;
}) {
  return (
    <div className={styles.chatInputRow}>
      <input
        className={styles.chatInput}
        type="text"
        placeholder="Ask something…"
        disabled={disabled}
        title={disabled ? reason : undefined}
        aria-describedby={disabled ? "remedy-chat-input-reason" : undefined}
      />
      <button
        type="button"
        className={styles.chatSend}
        disabled={disabled}
        title={disabled ? reason : undefined}
        aria-label="Send"
      >
        ↑
      </button>
      {disabled ? (
        <p id="remedy-chat-input-reason" className={styles.chatInputReason}>{reason}</p>
      ) : null}
    </div>
  );
}

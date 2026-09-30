// T5_F044 T001, DECISION F044 D4 (2) — the chat sheet: a glass dialog, anchored right on the
// overlay layer exactly as the learning overlay is, that ROUTES a question from the bar's Ask
// row to the grounded chat of DECISION F038 D12. It builds no chat of its own: it mounts
// `EvidenceChatTab` as it is and reads and sends nothing itself.
import { useEffect } from "react";
import { EvidenceChatTab } from "../graph/EvidenceChatTab";
import type { EvidenceTab } from "../graph/semanticZoom";
import styles from "./ChatSheet.module.css";

export const CHAT_SHEET_TITLE = "Ask the chat";

export function ChatSheet({ jobId, serverToken, taskId, question, onClose, onOpenTab }: {
  jobId: string;
  serverToken: string;
  taskId: string;
  question: string;
  onClose: () => void;
  onOpenTab: (tab: EvidenceTab) => void;
}) {
  // Esc closes the sheet, as the reference's sheets and popovers do (the learning overlay's own
  // listener is the precedent).
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  return (
    <section className={styles.sheet} role="dialog" aria-label={CHAT_SHEET_TITLE} data-ui="chat-sheet">
      <header className={styles.header}>
        <h2>{CHAT_SHEET_TITLE}</h2>
        <button type="button" className={styles.close} onClick={onClose}>Close chat</button>
      </header>
      <EvidenceChatTab jobId={jobId} token={serverToken} taskId={taskId} onTab={onOpenTab} initialQuestion={question} />
    </section>
  );
}

import { useEffect, useState } from "react";
import { previewPollDelayMs, previewCardView, PREVIEW_LOADING_LINE } from "../../api/artifactPreview";
import type { PreviewView } from "../../api/artifactPreview";
import { loadPreviewView } from "../../api/remedyApi";
import { usePageVisible } from "../graph/usePageVisible";
import { JOB_PREVIEW_START_COMMAND_ID, JOB_PREVIEW_STOP_COMMAND_ID, sendPreviewCommand } from "../../api/previewSend";
import styles from "./ArtifactsPanel.module.css";

/**
 * The job's app preview card (F041 T003, DECISION F041 D5): a small glass tile inside the
 * results panel that reads `preview_control.py`'s own state machine and offers the one button
 * its state allows. It reuses `ArtifactsPanel.module.css` rather than carrying a stylesheet of
 * its own, since both live on the one glass surface the panel opens.
 *
 * THE ONE TIMER. While the page is visible, the effect below reads the preview view once and
 * schedules its own next read after `previewPollDelayMs` of the answer it just got — fast while
 * a start is still under way, slow once the state has settled. Hiding the tab (DECISION F025 D3's
 * own `usePageVisible`) cancels the poll outright rather than letting it run unseen, and coming
 * back re-arms it through the SAME effect, keyed on `visible` alone. `tick` is the poll's own
 * clock: incrementing it is the only thing the scheduled timeout or a sent command ever does.
 */
export function AppPreviewCard({ jobId, serverToken }: { jobId: string; serverToken: string }) {
  const visible = usePageVisible();
  const [view, setView] = useState<PreviewView | null | undefined>(undefined);
  const [tick, setTick] = useState(0);
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!visible) return;
    let cancelled = false;
    let timeoutId: number | undefined;
    void loadPreviewView({ jobId, token: serverToken }).then((answer) => {
      if (cancelled) return;
      setView(answer);
      timeoutId = window.setTimeout(() => setTick((current) => current + 1), previewPollDelayMs(answer));
    });
    return () => {
      cancelled = true;
      window.clearTimeout(timeoutId);
    };
  }, [jobId, serverToken, visible, tick]);

  const card = view === undefined ? null : previewCardView(view);
  const line = card === null ? PREVIEW_LOADING_LINE : card.line;
  const detail = card?.detail ?? "";
  const link = card?.link ?? null;
  const action = card?.action ?? null;
  const actionLabel = card?.actionLabel ?? "";

  async function handleClick() {
    if (action === null) return;
    setSending(true);
    const commandId = action === "start" ? JOB_PREVIEW_START_COMMAND_ID : JOB_PREVIEW_STOP_COMMAND_ID;
    const outcome = await sendPreviewCommand({ jobId, serverToken }, commandId);
    setSending(false);
    setMessage(outcome.sentence);
    setTick((current) => current + 1);
  }

  return (
    <section
      data-ui="app-preview-card"
      aria-label="App preview"
      data-state={view ? view.state : "unknown"}
      className={styles.card}
    >
      <p className={styles.cardLine}>{line}</p>
      {detail !== "" && <p className={styles.cardDetail}>{detail}</p>}
      {link !== null && (
        <a data-ui="app-preview-link" className={styles.link} href={link} target="_blank" rel="noopener noreferrer">
          Open app
        </a>
      )}
      <div className={styles.cardActions}>
        {action !== null && (
          <button type="button" disabled={sending} onClick={() => void handleClick()}>
            {actionLabel}
          </button>
        )}
      </div>
      <p aria-live="polite">{message}</p>
    </section>
  );
}

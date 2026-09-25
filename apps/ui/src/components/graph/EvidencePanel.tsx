// L3 of semantic zoom: the evidence side panel for the focused run, with the
// tabs T5_F023.md names — diff, prompt trace, chat. A tab loads its content
// only when it is the open one: the diff is read through the task-run diff
// route when the diff tab opens, and the prompt trace is the dashboard's own.
// Like the run detail, it is not a dialog: Escape walks back to L2 and closes
// it (DECISION F023 D5).
import { useEffect, useRef, useState } from "react";
import { loadDiffEnvelope } from "../../api/remedyApi";
import type { DiffEnvelope } from "../../api/diffViewModel";
import type { RemedyPromptTraceItem } from "../../api/types";
import { DiffFileSidebar } from "../diff/DiffFileSidebar";
import { DiffView } from "../diff/DiffView";
import { PromptTracePanel } from "../prompt/PromptTracePanel";
import type { BrainEventRow, BrainNode } from "./brainOntology";
import { EVIDENCE_CHAT_NOT_YET, EVIDENCE_TABS, evidencePromptsOf } from "./evidencePanel";
import { runDetailOf } from "./runDetailModel";
import type { EvidenceTab } from "./semanticZoom";
import styles from "./EvidencePanel.module.css";

const DIFF_PENDING = "Loading the change for this task run.";
const DIFF_UNAVAILABLE = "No diff is available for this task run.";

function DiffTab({ jobId, token, taskId }: { jobId: string; token: string; taskId: string }) {
  // The envelope with the task it was read for, so a slow read never paints
  // one task's change under another's name.
  const [loaded, setLoaded] = useState<{ taskId: string; envelope: DiffEnvelope } | null>(null);
  useEffect(() => {
    let cancelled = false;
    void loadDiffEnvelope({ jobId, token, taskId }).then((envelope) => {
      if (!cancelled) setLoaded({ taskId, envelope });
    });
    return () => { cancelled = true; };
  }, [jobId, token, taskId]);
  const envelope = loaded !== null && loaded.taskId === taskId ? loaded.envelope : null;
  if (envelope === null) return <p className={styles.note}>{DIFF_PENDING}</p>;
  if (!envelope.available) {
    return <p className={styles.note}>{envelope.reason === null ? DIFF_UNAVAILABLE : `${DIFF_UNAVAILABLE} ${envelope.reason}`}</p>;
  }
  return (
    <div className={styles.diff}>
      <DiffFileSidebar envelope={envelope} />
      <DiffView envelope={envelope} />
    </div>
  );
}

export function EvidencePanel({ node, tab, rows, promptItems, jobId, token, onTab, onClose }: {
  node: Pick<BrainNode, "id" | "kind" | "state" | "parentId" | "seq" | "meta">;
  tab: EvidenceTab;
  rows: readonly BrainEventRow[];
  promptItems: readonly RemedyPromptTraceItem[];
  jobId: string;
  token: string;
  onTab: (tab: EvidenceTab) => void;
  onClose: () => void;
}) {
  const detail = runDetailOf({ node, rows, rounds: null, promptItems });
  const prompts = evidencePromptsOf(promptItems, detail.taskId);
  const bodyRef = useRef<HTMLDivElement>(null);

  // "Why" lands on the prompt trace with the run's own prompt in view.
  useEffect(() => {
    if (tab !== "prompt" || detail.promptItemId === null) return;
    const card = bodyRef.current?.querySelector(`[data-prompt-id="${CSS.escape(detail.promptItemId)}"]`);
    card?.scrollIntoView({ block: "nearest" });
  }, [tab, detail.promptItemId]);

  return (
    <aside className={styles.panel} aria-label="Evidence" data-ui="evidence-panel">
      <header className={styles.header}>
        <div>
          <h2 className={styles.title}>{detail.title}</h2>
          <p className={styles.subtitle}>
            {detail.round !== null ? `Round ${detail.round} of task ${detail.taskId}` : `Task ${detail.taskId}`} · {detail.verdict}
          </p>
        </div>
        <button type="button" className={styles.close} onClick={onClose} aria-label="Close evidence">×</button>
      </header>
      <div className={styles.tabs} role="tablist" aria-label="Evidence">
        {EVIDENCE_TABS.map((t) => (
          <button
            key={t.tab}
            type="button"
            role="tab"
            aria-selected={t.tab === tab}
            className={styles.tab}
            onClick={() => onTab(t.tab)}
          >
            {t.label}
          </button>
        ))}
      </div>
      <div className={styles.body} ref={bodyRef} role="tabpanel">
        {tab === "diff" && <DiffTab jobId={jobId} token={token} taskId={detail.taskId} />}
        {tab === "prompt" && <PromptTracePanel prompts={prompts} selectedPromptId={detail.promptItemId} />}
        {tab === "chat" && <p className={styles.note}>{EVIDENCE_CHAT_NOT_YET}</p>}
      </div>
    </aside>
  );
}

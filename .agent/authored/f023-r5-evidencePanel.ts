// Owns what the L3 evidence panel lists: its tabs in order with their labels,
// the prompts its trace tab shows for a run's task, and the sentence its chat
// tab says until chat about a run exists. PURE, so each is goldened headless
// (T5_F023.md: "L3 EvidencePanel side panel: tabs diff | prompt trace | chat";
// DECISION F023 D5).
import type { RemedyPromptTraceItem } from "../../api/types";
import type { EvidenceTab } from "./semanticZoom";

/** The panel's tabs, in the order T5_F023.md names them. */
export const EVIDENCE_TABS: readonly { tab: EvidenceTab; label: string }[] = [
  { tab: "diff", label: "Diff" },
  { tab: "prompt", label: "Prompt trace" },
  { tab: "chat", label: "Chat" },
];

/** The chat tab's honest answer: nothing to talk to about a single run yet. */
export const EVIDENCE_CHAT_NOT_YET =
  "Talking about a single run arrives with its own feature. The job's steering box, in the right panel, already reaches the running job.";

/** The prompts the trace tab lists for a task: that task's own, in the order
 *  they were sent — by round, then the builder before the reviewer. */
export function evidencePromptsOf(items: readonly RemedyPromptTraceItem[], taskId: string): RemedyPromptTraceItem[] {
  const order = (role: string) => (role === "builder" ? 0 : role === "reviewer" ? 1 : 2);
  return items
    .filter((p) => p.taskId === taskId)
    .sort((a, b) => a.round - b.round || order(a.role) - order(b.role) || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

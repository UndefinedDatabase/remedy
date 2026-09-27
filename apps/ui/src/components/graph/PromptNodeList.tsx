// DECISION F288 D6, graph_spec.md §14 — the keyboard's own parallel list of
// the live picture's prompt nodes. `ForceBrainGraph.tsx`'s canvas is hidden
// from assistive tech (its own header comment names the attribute), so
// every prompt `synapse` it draws also gets a native, focusable button
// here: Tab reaches it, Enter and Space select it, and a screen reader
// hears its label and state instead of a canvas pixel. Hidden while
// nothing inside it has focus (its style module), so a pointer user sees
// the same live picture as before.
import type { PromptListEntry } from "./brainView";
import styles from "./PromptNodeList.module.css";

export function PromptNodeList({ entries, selectedId, onSelect }: {
  entries: readonly PromptListEntry[];
  selectedId: string | null;
  onSelect: (promptId: string) => void;
}) {
  if (entries.length === 0) return null;
  return (
    <nav className={styles.nav} aria-label="Prompts in the live graph" data-ui="prompt-node-list">
      <ul className={styles.list}>
        {entries.map((entry) => (
          <li key={entry.nodeId} className={styles.item}>
            <button
              type="button"
              className={styles.button}
              aria-label={`${entry.label} — ${entry.state}`}
              aria-pressed={entry.nodeId === selectedId}
              onClick={() => onSelect(entry.promptId)}
            >
              {entry.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}

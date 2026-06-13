import { useState } from "react";
import type { RemedyNextAction } from "../../api/types";
import { SparkGlyph, ArrowSendGlyph } from "../icons/RemedyGlyphs";
import styles from "./CommandBar.module.css";

export function CommandBar({
  nextAction,
  onJump,
}: {
  nextAction: RemedyNextAction;
  onJump?: (query: string) => void;   // Shell: filters tasks + focuses the matching graph node
}) {
  const [query, setQuery] = useState("");
  const submit = () => { if (query.trim() && onJump) onJump(query.trim()); };

  return (
    <section className={styles.commandBar} aria-label="Jump to anything" data-ui="command-bar">
      <div className={styles.spark}><SparkGlyph style={{ width: 16, height: 16 }} /></div>
      <input
        aria-label="Jump to a task or file"
        value={query}
        placeholder='Jump to anything (e.g., "error handling")'
        onChange={e => setQuery(e.target.value)}
        onKeyDown={e => { if (e.key === "Enter") submit(); }}
      />
      <span className={styles.hint} title={`Next safe action: ${nextAction.command}`}>
        next: {nextAction.label}
      </span>
      <button
        type="button"
        className={styles.actionBtn}
        aria-label="Copy next safe command"
        title={`Copy: ${nextAction.command}`}
        onClick={() => navigator.clipboard?.writeText(nextAction.command)}
      >
        <ArrowSendGlyph style={{ width: 16, height: 16 }} />
      </button>
    </section>
  );
}

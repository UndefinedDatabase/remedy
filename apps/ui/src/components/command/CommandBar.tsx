import type { RemedyNextAction } from "../../api/types";
import { SparkGlyph, CopyGlyph } from "../icons/RemedyGlyphs";
import styles from "./CommandBar.module.css";

export function CommandBar({ nextAction }: { nextAction: RemedyNextAction }) {
  return (
    <section className={styles.commandBar} aria-label="Command search" data-ui="command-bar">
      <div className={styles.spark}><SparkGlyph style={{ width: 16, height: 16 }} /></div>
      <input readOnly aria-label="Ask Remedy" value="" placeholder="Ask Remedy anything or search tasks..." />
      <button type="button" aria-label="Copy suggested command" title={`Copy command: ${nextAction.command}`} onClick={() => navigator.clipboard?.writeText(nextAction.command)}>
        <CopyGlyph style={{ width: 16, height: 16 }} />
      </button>
    </section>
  );
}

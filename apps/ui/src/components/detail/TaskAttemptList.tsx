import { useState } from "react";
import type { TaskAttemptRow } from "../../api/attemptView";
import { attemptFactsSentence } from "../../api/attemptView";
import styles from "./DetailPopover.module.css";

/** DECISION F029 D5 (2), (3) — the popover's Attempts list, shaped as
 *  `TaskVersionList.tsx`: one row per `taskAttemptRows` (`attemptView.ts`)
 *  hands in, each earlier row a button that opens the facts that changed
 *  from the row before it — one row's diff open at a time — the row's own
 *  facts sentence beneath its button whether open or not, and the current
 *  row last, never openable. Renders nothing for a task with no attempt
 *  fan, where `rows` is `[]`. */
export function TaskAttemptList({ rows }: { rows: readonly TaskAttemptRow[] }) {
  const [openAttempt, setOpenAttempt] = useState<number | null>(null);

  if (rows.length === 0) return null;

  return (
    <section className={styles.section}>
      <h3>Attempts</h3>
      <ul className={styles.versionList} aria-label="Attempts">
        {rows.map((row) => {
          const disabled = row.changes.length === 0;
          const isOpen = !disabled && openAttempt === row.attempt;
          return (
            <li key={row.attempt} className={styles.versionRow}>
              <button
                type="button"
                aria-expanded={isOpen}
                disabled={disabled}
                onClick={() => setOpenAttempt(isOpen ? null : row.attempt)}
              >
                {row.label}
              </button>
              <p className={styles.detail}>{attemptFactsSentence(row.facts)}</p>
              {isOpen && (
                <dl className={styles.versionDiff}>
                  {row.changes.map((change) => (
                    <div key={change.label}>
                      <dt>{change.label}</dt>
                      <dd>
                        <del>{change.before}</del>
                        {" → "}
                        <ins>{change.after}</ins>
                      </dd>
                    </div>
                  ))}
                </dl>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}

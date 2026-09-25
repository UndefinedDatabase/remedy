import { useState } from "react";
import type { TaskSpecVersionRow } from "../../api/taskSpecView";
import styles from "./DetailPopover.module.css";

/** `v<n> · replaced while <state>` for an archived row, `v<n> · current` for
 *  the current one (DECISION F026 D3 clause 3). */
function rowLabel(row: TaskSpecVersionRow): string {
  return row.current ? `v${row.specVersion} · current` : `v${row.specVersion} · replaced while ${row.state}`;
}

/** DECISION F026 D3 clause 3 — the popover's Versions list: one row per spec
 *  version `specVersionRows` (`taskSpecView.ts`) hands in, each a button that
 *  opens the fields that changed from the row before it — one row's diff
 *  open at a time. Renders nothing for a task never edited at runtime, where
 *  `rows` is `[]`. */
export function TaskVersionList({ rows }: { rows: readonly TaskSpecVersionRow[] }) {
  const [openVersion, setOpenVersion] = useState<number | null>(null);

  if (rows.length === 0) return null;

  return (
    <section className={styles.section}>
      <h3>Versions</h3>
      <ul className={styles.versionList} aria-label="Spec versions">
        {rows.map((row) => {
          const disabled = row.changes.length === 0;
          const isOpen = !disabled && openVersion === row.specVersion;
          return (
            <li key={row.specVersion} className={styles.versionRow}>
              <button
                type="button"
                aria-expanded={isOpen}
                disabled={disabled}
                onClick={() => setOpenVersion(isOpen ? null : row.specVersion)}
              >
                {rowLabel(row)}
              </button>
              {isOpen && (
                <dl className={styles.versionDiff}>
                  {row.changes.map((change) => (
                    <div key={change.field}>
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

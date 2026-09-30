// The '?' panel (T5_F043 T003, DECISION F043 D3): every catalog entry, searchable, placed by its
// key's first word. Its rows carry `data-term-entry` and never `data-term`, because a panel that
// lists every key by construction would make the audit's dead-key direction pass for keys no
// surface renders — `data-term` stays the mark of a SURFACE actually showing a term.
import { useEffect, useState } from "react";
import { TERM_CATALOG } from "../../api/terminology";
import { searchTermEntries, termPlace } from "../../api/termSearch";
import styles from "./TermPanel.module.css";

export const TERM_PANEL_LABEL = "Terms";
export const TERM_SEARCH_LABEL = "Search the terms";

/** What an empty search result says, the query quoted back so a stray space reads correctly. */
export function termPanelEmptyLine(query: string): string {
  return `No term matches “${query.trim()}”.`;
}

/** The panel's optional re-launch of the first-run tour (DECISION F043 D4): the shell hands
 *  this only when it can relaunch the tour, since a term panel opened from elsewhere carries
 *  no such capability. */
export function TermPanel({ onClose, onStartTour }: { onClose: () => void; onStartTour?: () => void }) {
  const [query, setQuery] = useState("");
  const rows = searchTermEntries(TERM_CATALOG, query);

  // Escape closes the panel, as the learning overlay's sheet does.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  return (
    <section className={styles.panel} role="dialog" aria-label={TERM_PANEL_LABEL} data-ui="term-panel">
      <header className={styles.header}>
        <h2>{TERM_PANEL_LABEL}</h2>
        <button type="button" className={styles.close} onClick={onClose}>Close terms</button>
      </header>
      <p className={styles.quiet}>What the cockpit's words mean. Press ? anywhere to open this list.</p>
      {onStartTour && (
        <button type="button" className={styles.tour} onClick={onStartTour}>Take the tour</button>
      )}
      <input
        type="search"
        className={styles.search}
        aria-label={TERM_SEARCH_LABEL}
        placeholder="Search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        autoFocus
      />
      {rows.length === 0 ? (
        <p className={styles.quiet}>{termPanelEmptyLine(query)}</p>
      ) : (
        <dl className={styles.list}>
          {rows.map(({ key, entry }) => (
            <div key={key} className={styles.item} data-term-entry={key}>
              <dt>{entry.title}</dt>
              <dd className={styles.place}>{termPlace(key)}</dd>
              <dd>{entry.body}</dd>
            </div>
          ))}
        </dl>
      )}
    </section>
  );
}

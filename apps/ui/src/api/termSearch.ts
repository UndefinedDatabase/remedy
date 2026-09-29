// The '?' panel's pure rules (T5_F043 T003, DECISION F043 D3): what the search keeps, where a
// key's family is shown, and which key press opens the panel. Nothing here touches the DOM; the
// panel component reads these and renders.
import type { TermEntry } from "./terminology";

/** One catalog entry, carried with its key so a search result can be listed and placed. */
export interface TermListing {
  readonly key: string;
  readonly entry: TermEntry;
}

/** Every entry whose lower-cased title and body, joined by a space, hold every white-space-
 *  separated word of the lower-cased query — never the key or the source, so a search cannot
 *  be gamed by an implementation detail the operator never reads. Sorted by lower-cased title
 *  and then by key, so the same query always lists the same order. */
export function searchTermEntries(
  catalog: Readonly<Record<string, TermEntry>>,
  query: string,
): TermListing[] {
  const words = query.trim().toLowerCase().split(/\s+/).filter((word) => word.length > 0);
  const rows = Object.entries(catalog)
    .map(([key, entry]) => ({ key, entry }))
    .filter(({ entry }) => {
      const haystack = `${entry.title} ${entry.body}`.toLowerCase();
      return words.every((word) => haystack.includes(word));
    });
  rows.sort((a, b) => {
    const byTitle = a.entry.title.toLowerCase().localeCompare(b.entry.title.toLowerCase());
    return byTitle !== 0 ? byTitle : a.key.localeCompare(b.key);
  });
  return rows;
}

/** Where a family of keys is shown, by the key's first dotted word. */
export const TERM_PLACES: Readonly<Record<string, string>> = {
  agent: "Right panel",
  graph: "Graph",
  metric: "Metrics bar",
  panel: "Right panel",
  phase: "Timeline",
  status: "Live status",
  task: "Task list",
};

/** The place of the key's first dotted word, by an OWN key of `TERM_PLACES` — never a
 *  prototype member (`toString`, `constructor`) — or "" when the table names no such family. */
export function termPlace(key: string): string {
  const family = key.split(".")[0];
  return Object.prototype.hasOwnProperty.call(TERM_PLACES, family) ? TERM_PLACES[family] : "";
}

/** The minimal shape of the element a key press came from, read off `event.target`. */
export interface KeyTarget {
  readonly tagName?: string;
  readonly isContentEditable?: boolean;
}

/** True only for "?" with no target, or a target that is not content-editable and whose
 *  upper-cased tag is none of INPUT, TEXTAREA and SELECT — so a typed question mark stays text
 *  wherever one could be typed. */
export function isHelpShortcut(key: string, target: KeyTarget | null): boolean {
  if (key !== "?") return false;
  if (target === null) return true;
  if (target.isContentEditable) return false;
  const tag = (target.tagName ?? "").toUpperCase();
  return tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT";
}

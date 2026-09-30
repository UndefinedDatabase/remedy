// The term audit (T5_F043 T002, DECISION F043 D1): a two-direction check between the terms a
// rendered surface carries and the catalog's keys, over plain strings — no DOM, no React — so it
// runs the same over server-rendered markup in a test and over the real shell in a browser.

/** The terms a used set lacks from the catalog, and the catalog keys nothing uses. */
export interface TermAudit {
  readonly missing: readonly string[];
  readonly dead: readonly string[];
}

// A `data-term="…"` attribute, written as white space then the attribute then its quoted value.
// The leading `\s` is what keeps this off the tooltip's own `data-term-tip="…"` (nothing between
// `data-term` and `-tip` for `\s` to match) and off plain text that merely reads `data-term="…"`
// (preceded by a tag's `>`, not white space).
const DATA_TERM_ATTR = /\sdata-term="([^"]*)"/g;

/** Every `data-term` value the markup carries, each once, sorted. */
export function collectDataTerms(markup: string): string[] {
  const found = new Set<string>();
  for (const match of markup.matchAll(DATA_TERM_ATTR)) {
    found.add(match[1]);
  }
  return [...found].sort();
}

/** The used terms the catalog lacks (`missing`) and the catalog keys nothing uses (`dead`), each
 *  sorted. */
export function auditTermUse(used: Iterable<string>, catalogKeys: Iterable<string>): TermAudit {
  const usedSet = new Set(used);
  const keySet = new Set(catalogKeys);
  const missing = [...usedSet].filter((term) => !keySet.has(term)).sort();
  const dead = [...keySet].filter((key) => !usedSet.has(key)).sort();
  return { missing, dead };
}

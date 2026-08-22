// Which stream events count as the agent DOING something, for the NowCard.
// Remedy deliberately classifies by EXCLUSION over a suffix rule rather than by
// an allow-list of the catalog's kinds: eleven run-log writers compute their
// kind at runtime, so an allow-list would silently demote every kind it has not
// heard of and the NowCard would go quiet exactly when the agent did something
// new. An unknown kind is therefore an ACTION until it is proven bookkeeping.
import type { FeedRow } from "./feedRow";

/** Suffixes of kinds where the agent LOOKED at something rather than changed
 *  it. These are the bookkeeping half T5_F021 excludes from the NowCard. */
const BOOKKEEPING_SUFFIXES: readonly string[] = [
  "_inspected", "_read", "_loaded", "_recalled", "_assessed",
];

/** Bookkeeping kinds no suffix rule catches, named one by one so that adding
 *  one stays a decision someone made rather than a pattern that drifted. */
const BOOKKEEPING_KINDS: readonly string[] = [
  "brain_viewer_prepared",
  "context_budget_optimized",
  "source_context_injected",
  "stream_cap_reached",
  "token_policy_applied",
];

/** True when a kind is the agent acting. Unknown kinds are ACTION on purpose. */
export function isActionKind(kind: string): boolean {
  if (BOOKKEEPING_KINDS.includes(kind)) {
    return false;
  }
  return !BOOKKEEPING_SUFFIXES.some(suffix => kind.endsWith(suffix));
}

/** The newest row the NowCard should show, or null when the stream has produced
 *  nothing but bookkeeping. Scans from the END: `recent` is oldest-first, so the
 *  last ACTION row in it is the newest one. */
export function newestActionRow(recent: readonly FeedRow[]): FeedRow | null {
  for (let i = recent.length - 1; i >= 0; i -= 1) {
    if (isActionKind(recent[i].kind)) {
      return recent[i];
    }
  }
  return null;
}

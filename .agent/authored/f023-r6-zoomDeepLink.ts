// Owns the zoom's deep link: `?focus=<node id>&level=<0-3>&tab=<tab>` on the
// page's own URL, read once when the stage opens and kept in step with the
// state afterwards, so a link restores what its sender was looking at and a
// timeline or feed jump can land on a node (T5_F023.md). There is no router:
// the query is read with URLSearchParams and written with history.replaceState
// by useZoomDeepLink.ts, and every other parameter — the job, the token — is
// kept as it was (DECISION F023 D6). PURE: strings in, strings and events out.
import type { EvidenceTab, ZoomEvent, ZoomState } from "./semanticZoom";

/** What a link asks for: a node to focus and, at L3, a tab of its evidence. */
export interface ZoomLink {
  focusId: string;
  tab: EvidenceTab | null;
}

const TABS: readonly EvidenceTab[] = ["diff", "prompt", "chat"];

/** The link a query string carries, or null. A link needs a focus and a level
 *  from 1 to 3; the tab is read at level 3 only, and defaults to the diff. */
export function zoomLinkFromSearch(search: string): ZoomLink | null {
  const params = new URLSearchParams(search);
  const focusId = params.get("focus") ?? "";
  const level = params.get("level");
  if (focusId === "" || (level !== "1" && level !== "2" && level !== "3")) return null;
  if (level !== "3") return { focusId, tab: null };
  const tab = params.get("tab");
  return { focusId, tab: TABS.includes(tab as EvidenceTab) ? (tab as EvidenceTab) : "diff" };
}

/** The machine events that restore a link: the click that focuses its node
 *  and, for an L3 link, the tab. Every check a click gets — the node exists,
 *  a run has a task — applies to a link exactly as it does to a click. */
export function zoomLinkEvents(link: ZoomLink): ZoomEvent[] {
  const events: ZoomEvent[] = [{ type: "click", nodeId: link.focusId }];
  if (link.tab !== null) events.push({ type: "open_evidence", tab: link.tab });
  return events;
}

/** `search` with the zoom's three parameters set from `state`, or removed at
 *  L0, and every other parameter left in place and in order. */
export function searchWithZoom(search: string, state: ZoomState): string {
  const params = new URLSearchParams(search);
  params.delete("focus");
  params.delete("level");
  params.delete("tab");
  if (state.level > 0 && state.focusId !== null) {
    params.set("focus", state.focusId);
    params.set("level", String(state.level));
    if (state.tab !== null) params.set("tab", state.tab);
  }
  const text = params.toString();
  return text === "" ? "" : `?${text}`;
}
